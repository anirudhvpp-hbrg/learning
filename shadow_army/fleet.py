"""Fleet manager — state persistence, shadow selection, health metrics, initialization."""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from typing import Optional

from .shadow import Shadow, SHADOW_REGISTRY
from .evolution import check_synergies, check_tier_advancement, resolve_branch_choice

STATE_FILES = {
    "shadows": "shadows_state.json",
    "monarch": "monarch_state.json",
    "boss_crystals": "boss_crystals.json",
    "monarch_patterns": "monarch_patterns.json",
    "stage_log": "stage_log.json",
}

MONARCH_STAGES = [
    ("Novice Sovereign",    0,      "Task decomposition · single-shadow dispatch"),
    ("Rising Sovereign",    500,    "Parallel dispatch — up to 3 shadows simultaneously"),
    ("Shadow Commander",    -1,     "Council invocation — multi-shadow advisory before hard Stages"),  # triggered by tier event
    ("Shadow King",         3000,   "Pattern Absorption — inherits cross-shadow heuristics"),
    ("Shadow Monarch",      -1,     "Arise Protocol — crystallize completed task classes into new shadow templates"),
    ("Absolute Sovereign",  -1,     "Full fleet tactical coordination · S-Rank Stages accessible"),
]


class Fleet:
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.shadows: dict[str, Shadow] = {}
        self.monarch_state: dict = {}
        self.boss_crystals: dict = {}
        self.monarch_patterns: dict = {}
        self.stage_log: list = []
        self.active_synergies: list[str] = []
        self._stateless = False

    def _path(self, key: str) -> str:
        return os.path.join(self.base_dir, STATE_FILES[key])

    def load(self) -> list[str]:
        """Session initialization protocol — 9-step sequence. Returns list of events."""
        events: list[str] = []

        # Step 1 — shadows
        if os.path.exists(self._path("shadows")):
            with open(self._path("shadows")) as f:
                data = json.load(f)
            self.shadows = {sid: Shadow.from_dict(d) for sid, d in data.items()}
            events.append(f"Loaded {len(self.shadows)} shadows from state.")
        else:
            self.shadows = {sid: Shadow.default(sid) for sid in SHADOW_REGISTRY}
            events.append("No shadow state found — initializing fleet at Knight tier.")

        # Step 2 — monarch
        if os.path.exists(self._path("monarch")):
            with open(self._path("monarch")) as f:
                self.monarch_state = json.load(f)
        else:
            self.monarch_state = {
                "stage": "Novice Sovereign",
                "fleet_xp": 0,
                "absorbed_patterns": [],
                "active_synergies": [],
                "milestone_log": [],
            }
            events.append("Monarch initialized at Novice Sovereign.")

        # Step 3–5 — support files
        for key, default in [("boss_crystals", {}), ("monarch_patterns", {}), ("stage_log", [])]:
            if os.path.exists(self._path(key)):
                with open(self._path(key)) as f:
                    setattr(self, key.replace("_", "_"), json.load(f))
            else:
                setattr(self, key.replace("_", "_"), default)

        # Step 6 — deferred tier advancements
        for shadow in self.shadows.values():
            adv = check_tier_advancement(shadow)
            for e in adv:
                events.append(f"[deferred] {e}")

        # Step 7 — pending Branch Choices
        for shadow in self.shadows.values():
            if shadow.xp >= 150 and shadow.branch is None:
                branch, reason = resolve_branch_choice(shadow)
                shadow.branch = branch
                reg = SHADOW_REGISTRY[shadow.id]
                branch_name = reg["branch_names"].get(branch, branch)
                events.append(f"🌿 {shadow.name} → Branch {branch} ({branch_name}): {reason}")

        # Step 8 — fleet XP
        total_xp = sum(s.xp for s in self.shadows.values())
        self.monarch_state["fleet_xp"] = total_xp
        self.active_synergies = self.monarch_state.get("active_synergies", [])

        # Step 9 — synergy check
        new_syn = check_synergies(self.shadows, self.active_synergies)
        for syn in new_syn:
            self.active_synergies.append(syn["name"])
            events.append(f"✨ Synergy unlocked: {syn['name']} — {syn['effect']}")
        self.monarch_state["active_synergies"] = self.active_synergies

        # Monarch stage check
        monarch_evt = self._check_monarch_stage()
        if monarch_evt:
            events.append(monarch_evt)

        return events

    def save(self) -> None:
        self.monarch_state["fleet_xp"] = sum(s.xp for s in self.shadows.values())
        self.monarch_state["active_synergies"] = self.active_synergies

        with open(self._path("shadows"), "w") as f:
            json.dump({sid: s.to_dict() for sid, s in self.shadows.items()}, f, indent=2)
        with open(self._path("monarch"), "w") as f:
            json.dump(self.monarch_state, f, indent=2)
        with open(self._path("boss_crystals"), "w") as f:
            json.dump(self.boss_crystals, f, indent=2)
        with open(self._path("monarch_patterns"), "w") as f:
            json.dump(self.monarch_patterns, f, indent=2)
        with open(self._path("stage_log"), "w") as f:
            json.dump(self.stage_log, f, indent=2)

    def select_shadow(self, task_class: str, exclude: Optional[list[str]] = None) -> Shadow:
        """Select best shadow for task_class. Domain affinity × tier weight."""
        exclude = exclude or []
        candidates = [s for sid, s in self.shadows.items() if sid not in exclude]
        if not candidates:
            candidates = list(self.shadows.values())

        def score(s: Shadow) -> float:
            from .evolution import TIER_ORDER
            tier_score = TIER_ORDER.index(s.tier) * 10
            domain_match = any(tc in task_class or task_class in tc for tc in s.task_classes)
            cap = s.capabilities.get(task_class)
            history_score = (cap.hit_count * cap.success_rate) if cap else 0
            return tier_score + (50 if domain_match else 0) + history_score

        return max(candidates, key=score)

    def select_shadows_for_stage(self, task_class: str, count: int) -> list[Shadow]:
        """Select `count` best shadows without repetition."""
        selected: list[Shadow] = []
        excluded: list[str] = []
        for _ in range(min(count, len(self.shadows))):
            s = self.select_shadow(task_class, exclude=excluded)
            selected.append(s)
            excluded.append(s.id)
        return selected

    def apply_xp(self, shadow: Shadow, xp: int) -> list[str]:
        """Add XP, check advancement, check Branch Choice, check synergies. Return events."""
        events: list[str] = []
        shadow.xp += xp
        events.extend(check_tier_advancement(shadow))

        # Branch Choice
        if shadow.xp >= 150 and shadow.branch is None:
            branch, reason = resolve_branch_choice(shadow)
            shadow.branch = branch
            reg = SHADOW_REGISTRY[shadow.id]
            branch_name = reg["branch_names"].get(branch, branch)
            events.append(f"🌿 {shadow.name} chose Branch {branch} ({branch_name}): {reason}")

        # Fleet synergies
        new_syn = check_synergies(self.shadows, self.active_synergies)
        for syn in new_syn:
            self.active_synergies.append(syn["name"])
            events.append(f"✨ Synergy unlocked: {syn['name']} — {syn['effect']}")

        # Monarch stage
        evt = self._check_monarch_stage()
        if evt:
            events.append(evt)

        return events

    def _check_monarch_stage(self) -> Optional[str]:
        fleet_xp = sum(s.xp for s in self.shadows.values())
        current = self.monarch_state.get("stage", "Novice Sovereign")
        stage_names = [s[0] for s in MONARCH_STAGES]
        current_idx = stage_names.index(current) if current in stage_names else 0

        for i, (name, xp_req, ability) in enumerate(MONARCH_STAGES):
            if i <= current_idx:
                continue
            if xp_req > 0 and fleet_xp >= xp_req:
                self.monarch_state["stage"] = name
                self.monarch_state.setdefault("milestone_log", []).append({
                    "stage": name, "fleet_xp": fleet_xp,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return f"👑 Monarch ascended to {name}: {ability}"
        return None

    def log_stage(self, entry: dict) -> None:
        self.stage_log.append(entry)

    def fleet_report(self) -> str:
        lines = ["\n── Fleet Status ─────────────────────────────────"]
        lines.append(f"  Monarch: {self.monarch_state.get('stage', 'Novice Sovereign')} | Fleet XP: {sum(s.xp for s in self.shadows.values())}")
        if self.active_synergies:
            lines.append(f"  Active synergies: {', '.join(self.active_synergies)}")
        lines.append("")
        for s in self.shadows.values():
            branch_str = f" [{s.branch}]" if s.branch else " [?]"
            cap_count = len(s.capabilities)
            lines.append(f"  {s.name:<20} {s.tier:<14}{branch_str:<5}  XP:{s.xp:>5}  Caps:{cap_count}")
        lines.append("─────────────────────────────────────────────────")
        return "\n".join(lines)
