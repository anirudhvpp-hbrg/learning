"""Monarch orchestrator — task decomposition via tool_use, shadow dispatch, synthesis."""
from __future__ import annotations
import asyncio
import json
from datetime import datetime, timezone
from typing import Optional

import anthropic

from .fleet import Fleet
from .shadow import Shadow, SHADOW_REGISTRY
from .stage import StageClassification, classify_stage
from .evolution import (
    calculate_xp,
    parse_battle_record_from_output,
)

MONARCH_MODEL = "claude-sonnet-4-6"
SHADOW_MODEL = "claude-haiku-4-5-20251001"


# ── Tool definitions for Monarch decomposition ──────────────────────────────

DECOMPOSE_TOOLS = [
    {
        "name": "dispatch_shadow",
        "description": "Dispatch a shadow to execute a specific subtask. Call once per subtask.",
        "input_schema": {
            "type": "object",
            "properties": {
                "subtask": {"type": "string", "description": "The specific subtask to execute."},
                "task_class": {
                    "type": "string",
                    "description": "Task class label (e.g. 'research', 'architecture', 'writing', 'strategy', 'analysis').",
                },
                "preferred_shadow": {
                    "type": "string",
                    "description": "Optional shadow ID to prefer (e.g. 'analyst_prime').",
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "normal"],
                    "description": "Execution priority.",
                },
            },
            "required": ["subtask", "task_class"],
        },
    },
    {
        "name": "set_stage_rank",
        "description": "Override the auto-classified Stage rank if you have better context.",
        "input_schema": {
            "type": "object",
            "properties": {
                "rank": {"type": "string", "enum": ["E", "D", "C", "B", "A", "S"]},
                "reason": {"type": "string"},
            },
            "required": ["rank", "reason"],
        },
    },
]


class Monarch:
    def __init__(self, fleet: Fleet, client: Optional[anthropic.Anthropic] = None):
        self.fleet = fleet
        self.client = client or anthropic.Anthropic()

    async def run(self, task: str) -> dict:
        """
        Full Stage pipeline:
        1. Classify Stage
        2. Decompose task via tool_use
        3. Dispatch shadows concurrently
        4. Synthesize
        5. Award XP + record Battle Records
        6. Return result dict
        """
        print(f"\n👑 Monarch receiving task: {task[:80]}...")

        # Step 1 — classify stage
        known_classes = [tc for s in self.fleet.shadows.values() for tc in s.task_classes]
        stage = classify_stage(task, known_classes)
        print(f"   Stage classified: {stage.rank}-Rank ({stage.reasoning})")

        # Step 2 — decompose via tool_use
        dispatches, rank_override = await self._decompose(task, stage)

        if rank_override:
            stage.rank = rank_override["rank"]
            print(f"   Stage rank overridden to {stage.rank}: {rank_override['reason']}")

        if not dispatches:
            dispatches = [{"subtask": task, "task_class": "general", "preferred_shadow": None, "priority": "high"}]

        print(f"   Dispatching {len(dispatches)} subtask(s)...")

        # Step 3 — run shadows concurrently
        results = await self._run_shadows(dispatches, stage, task)

        # Step 4 — synthesize
        synthesis = await self._synthesize(task, results)

        # Step 5 — log stage
        stage_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task": task[:120],
            "stage_rank": stage.rank,
            "drops": stage.drops,
            "shadows_deployed": [r["shadow_id"] for r in results],
            "total_xp_awarded": sum(r["xp_awarded"] for r in results),
        }
        self.fleet.log_stage(stage_entry)

        return {
            "output": synthesis,
            "stage_rank": stage.rank,
            "drops": stage.drops,
            "shadow_results": results,
            "events": [e for r in results for e in r.get("events", [])],
        }

    async def _decompose(self, task: str, stage: StageClassification) -> tuple[list[dict], Optional[dict]]:
        """Use Monarch (claude-sonnet-4-6) with tool_use to decompose task into subtasks."""
        shadow_list = ", ".join(
            f"{sid} ({SHADOW_REGISTRY[sid]['domain']})"
            for sid in self.fleet.shadows
        )
        system = (
            f"You are the Monarch — sovereign orchestrator of the Shadow Fleet.\n"
            f"Available shadows: {shadow_list}\n"
            f"Stage rank: {stage.rank} | Required shadows: ~{stage.shadow_count}\n"
            f"Decompose the task into {stage.shadow_count} focused subtask(s). "
            f"Call dispatch_shadow once per subtask. "
            f"Match each subtask to the shadow whose domain fits best."
        )

        messages = [{"role": "user", "content": task}]
        dispatches: list[dict] = []
        rank_override: Optional[dict] = None

        # Tool use loop
        while True:
            response = self.client.messages.create(
                model=MONARCH_MODEL,
                max_tokens=1024,
                system=system,
                tools=DECOMPOSE_TOOLS,
                messages=messages,
            )

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        if block.name == "dispatch_shadow":
                            dispatches.append(block.input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": "Subtask queued.",
                            })
                        elif block.name == "set_stage_rank":
                            rank_override = block.input
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": "Stage rank updated.",
                            })

                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})
            else:
                break

        return dispatches, rank_override

    async def _run_shadows(self, dispatches: list[dict], stage: StageClassification, full_task: str) -> list[dict]:
        """Run all dispatched subtasks concurrently."""
        tasks = [
            self._run_single_shadow(d, stage, full_task)
            for d in dispatches
        ]
        return await asyncio.gather(*tasks)

    async def _run_single_shadow(self, dispatch: dict, stage: StageClassification, full_task: str) -> dict:
        """Execute one subtask with the best-fit shadow."""
        subtask = dispatch["subtask"]
        task_class = dispatch.get("task_class", "general")
        preferred = dispatch.get("preferred_shadow")

        # Select shadow
        if preferred and preferred in self.fleet.shadows:
            shadow = self.fleet.shadows[preferred]
            out_of_domain = task_class not in shadow.task_classes and not any(
                task_class in tc or tc in task_class for tc in shadow.task_classes
            )
        else:
            shadow = self.fleet.select_shadow(task_class)
            out_of_domain = False

        # Determine branch contribution for this record
        branch_contribution: Optional[str] = None
        if not out_of_domain and shadow.id in SHADOW_REGISTRY:
            criteria = SHADOW_REGISTRY[shadow.id].get("branch_criteria", {})
            for branch, tags in criteria.items():
                if any(tag in task_class for tag in tags) or task_class in tags:
                    branch_contribution = branch
                    break

        # Build system prompt with battle history
        system_prompt = shadow.build_system_prompt(task_class, subtask)

        # Run shadow (haiku)
        loop = asyncio.get_event_loop()
        raw_output = await loop.run_in_executor(None, self._call_shadow, system_prompt, subtask)

        # Score quality heuristically (length + structure signals)
        quality = self._score_quality(raw_output)

        # Calculate XP
        xp = calculate_xp(stage.rank, quality, out_of_domain, shadow.xp_bonus_pct)

        # Parse Battle Record from output
        br = parse_battle_record_from_output(
            raw_output, shadow.id, stage.rank, task_class,
            quality, xp, out_of_domain, branch_contribution,
        )

        # Check for Boss Crystal (first encounter of this task_class, B+ rank)
        boss_crystal = None
        is_first = task_class not in shadow.capabilities
        if is_first and stage.rank in ("B", "A", "S") and quality >= 0.6:
            boss_crystal = f"{shadow.id}_{task_class}_v1"
            br.boss_crystal_generated = boss_crystal
            shadow.boss_crystals.append(boss_crystal)
            self.fleet.boss_crystals[boss_crystal] = {
                "shadow": shadow.id,
                "task_class": task_class,
                "stage_rank": stage.rank,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Update capability profile
        if task_class not in shadow.capabilities:
            from .shadow import CapabilityProfile
            shadow.capabilities[task_class] = CapabilityProfile(task_class=task_class)
        cap = shadow.capabilities[task_class]
        cap.battle_records.append(br)
        cap.hit_count += 1
        prev_success = cap.success_rate
        n = cap.hit_count
        cap.success_rate = (prev_success * (n - 1) + (1.0 if quality >= 0.5 else 0.0)) / n

        # Award XP and collect events
        events = self.fleet.apply_xp(shadow, xp)

        # Strip battle record block from displayed output
        clean_output = raw_output.split("BATTLE_RECORD:")[0].strip()

        result = {
            "shadow_id": shadow.id,
            "shadow_name": shadow.name,
            "subtask": subtask,
            "task_class": task_class,
            "output": clean_output,
            "quality_score": quality,
            "xp_awarded": xp,
            "out_of_domain": out_of_domain,
            "boss_crystal": boss_crystal,
            "events": events,
        }

        xp_tag = f"+{xp}XP"
        if events:
            xp_tag += " " + " ".join(events)
        print(f"   ✓ {shadow.name} [{shadow.tier}] — {task_class} ({quality:.0%} quality, {xp_tag})")
        if boss_crystal:
            print(f"   💎 Boss Crystal forged: {boss_crystal}")

        return result

    def _call_shadow(self, system_prompt: str, subtask: str) -> str:
        """Synchronous shadow call — run in executor to avoid blocking event loop."""
        response = self.client.messages.create(
            model=SHADOW_MODEL,
            max_tokens=1200,
            system=system_prompt,
            messages=[{"role": "user", "content": subtask}],
        )
        return response.content[0].text

    async def _synthesize(self, original_task: str, results: list[dict]) -> str:
        """Monarch synthesizes all shadow outputs into final response."""
        combined = "\n\n".join(
            f"[{r['shadow_name']} — {r['task_class']}]\n{r['output']}"
            for r in results
        )
        system = (
            "You are the Monarch — sovereign synthesizer. "
            "Integrate the shadow outputs below into a single coherent response to the original task. "
            "Be direct. No preamble. First sentence carries full weight. "
            "Preserve the strongest insights from each shadow. Eliminate redundancy."
        )
        messages = [
            {
                "role": "user",
                "content": f"Original task: {original_task}\n\nShadow outputs:\n{combined}",
            }
        ]
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.messages.create(
                model=MONARCH_MODEL,
                max_tokens=1500,
                system=system,
                messages=messages,
            ),
        )
        return response.content[0].text

    @staticmethod
    def _score_quality(output: str) -> float:
        """Heuristic quality score — in production this would be a graded evaluation."""
        if not output or len(output) < 50:
            return 0.2
        has_structure = any(c in output for c in [":", "-", "\n"])
        has_battle_record = "BATTLE_RECORD:" in output
        length_score = min(len(output) / 800, 1.0)
        base = 0.55 + (0.15 if has_structure else 0) + (0.1 if has_battle_record else 0) + (length_score * 0.2)
        return min(base, 1.0)
