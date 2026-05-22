"""Shadow dataclasses — identity, capability profiles, battle records, serialization."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


SHADOW_REGISTRY: dict[str, dict] = {
    "axiom_prime": {
        "name": "Axiom Prime",
        "tier_label": "Grandmaster",
        "domain": "Build · Architect · Implement",
        "absorbed": ["Axiom", "Stark Architect", "Pioneer", "Stark Engineer", "Primal"],
        "knight_name": "Raw Architect",
        "task_classes": ["architecture", "system_design", "implementation", "sprint", "build"],
        "branch_criteria": {
            "A": ["architecture", "system_design", "structural_planning"],
            "B": ["implementation", "sprint", "rapid_build"],
        },
        "branch_names": {"A": "Prime Architect", "B": "Forge Incarnate", "C": "Awakened Engineer"},
    },
    "sentinel_prime": {
        "name": "Sentinel Prime",
        "tier_label": "Grandmaster",
        "domain": "Defend · Verify · Adversarial Audit",
        "absorbed": ["Warden", "Aegis", "Prosecutor", "Mirror", "Arbiter"],
        "knight_name": "Watchman",
        "task_classes": ["qa", "adversarial", "compliance", "pre_mortem", "bias_detection"],
        "branch_criteria": {
            "A": ["qa", "release_verification", "compliance"],
            "B": ["red_team", "stress_testing", "adversarial"],
            "C": ["pre_mortem", "bias_detection", "belief_calibration"],
        },
        "branch_names": {"A": "Iron Bastion", "B": "Inquisitor Prime", "C": "Mirror Sovereign"},
    },
    "thresher": {
        "name": "Thresher",
        "tier_label": "Grandmaster",
        "domain": "Compress · Deconstruct · Prune",
        "absorbed": [],
        "knight_name": "Cutter",
        "task_classes": ["compression", "brief_deconstruction", "gap_analysis", "context_pruning"],
        "branch_criteria": {
            "A": ["compression", "density_enforcement", "context_budget"],
            "B": ["brief_deconstruction", "rfp_analysis", "gap_extraction"],
        },
        "branch_names": {"A": "Void Blade", "B": "Signal Sovereign"},
    },
    "strategist_prime": {
        "name": "Strategist Prime",
        "tier_label": "Master",
        "domain": "Strategy · Foresight · Scenario",
        "absorbed": ["Strategist", "Oracle", "Stratagem"],
        "knight_name": "Tactician",
        "task_classes": ["strategy", "foresight", "scenario_planning", "stakeholder_analysis"],
        "branch_criteria": {
            "A": ["strategy", "competitor_mapping", "stakeholder_navigation", "terrain_analysis"],
            "B": ["scenario_trees", "foresight", "phase_change_detection", "probability_analysis"],
        },
        "branch_names": {"A": "War Sovereign", "B": "Oracle Sovereign"},
    },
    "genius_prime": {
        "name": "Genius Prime",
        "tier_label": "Master",
        "domain": "Innovation · Ideation · Novel Synthesis",
        "absorbed": ["Genius", "Innovator", "Alchemist"],
        "knight_name": "Spark",
        "task_classes": ["innovation", "ideation", "synthesis", "framework_building"],
        "branch_criteria": {
            "A": ["synthesis", "pattern_fusion", "framework_building", "cross_domain"],
            "B": ["assumption_breaking", "paradigm_challenge", "novel_path", "disruption"],
        },
        "branch_names": {"A": "Synthesis Sovereign", "B": "Disruption Engine"},
    },
    "visionary_prime": {
        "name": "Visionary Prime",
        "tier_label": "Master",
        "domain": "Foresight · Narrative · Inspiration",
        "absorbed": ["Visionary", "Explorer", "Probe", "Orator", "Illusionist", "Inspirer"],
        "knight_name": "Dreamer",
        "task_classes": ["narrative", "foresight", "communication", "reframing"],
        "branch_criteria": {
            "A": ["narrative", "story_architecture", "executive_communication", "persuasion"],
            "B": ["horizon_mapping", "futures_discovery", "long_range_signals", "foresight"],
        },
        "branch_names": {"A": "Narrative Sovereign", "B": "Foresight Master"},
    },
    "analyst_prime": {
        "name": "Analyst Prime",
        "tier_label": "Master",
        "domain": "Forensics · Pattern Recognition · Research",
        "absorbed": ["Analyst", "Cipher", "VEIL", "Detective", "Observant", "Stark Optimizer", "Argus"],
        "knight_name": "Scout",
        "task_classes": ["research", "analysis", "pattern_recognition", "evidence"],
        "branch_criteria": {
            "A": ["evidence_gathering", "case_building", "triangulation", "provenance"],
            "B": ["pattern_extraction", "synthesis", "hidden_signal_detection", "cross_context"],
        },
        "branch_names": {"A": "Detective Sovereign", "B": "Pattern Oracle"},
    },
    "titan_prime": {
        "name": "Titan Prime",
        "tier_label": "Master",
        "domain": "Execution · Delivery · Load-Bearing",
        "absorbed": ["Titan", "Defiance", "Load", "Brake"],
        "knight_name": "Worker",
        "task_classes": ["execution", "delivery", "throughput", "load_management"],
        "branch_criteria": {
            "A": ["delivery", "throughput", "first_pass_quality", "attach_and_ship"],
            "B": ["pressure_handling", "overload_absorption", "deadline_performance", "endurance"],
        },
        "branch_names": {"A": "Delivery God", "B": "Iron Will"},
    },
    "steward_prime": {
        "name": "Steward Prime",
        "tier_label": "Master",
        "domain": "Client · Commercial · Stakeholder",
        "absorbed": ["Steward", "Overseer"],
        "knight_name": "Liaison",
        "task_classes": ["commercial", "client", "stakeholder", "proposal"],
        "branch_criteria": {
            "A": ["pricing", "commercial_framing", "deal_structure", "margin_analysis"],
            "B": ["stakeholder_navigation", "relationship_building", "political_terrain", "confidence_management"],
        },
        "branch_names": {"A": "Commercial Sovereign", "B": "Trust Architect"},
    },
    "quill_prime": {
        "name": "Quill Prime",
        "tier_label": "Master",
        "domain": "Writing · Narrative · Communication",
        "absorbed": ["QUILL", "Transfer", "Prompter"],
        "knight_name": "Scribe",
        "task_classes": ["writing", "communication", "narrative", "documentation"],
        "branch_criteria": {
            "A": ["narrative_composition", "thought_leadership", "executive_communication", "persuasion"],
            "B": ["clarity", "compression", "technical_translation", "signal_extraction"],
        },
        "branch_names": {"A": "Narrative God", "B": "Precision Blade"},
    },
    "coach_prime": {
        "name": "Coach Prime",
        "tier_label": "Commander",
        "domain": "Reflection · Behavioral Coaching",
        "absorbed": ["Coach", "Wendy", "Candor", "Quirk"],
        "knight_name": "Observer",
        "task_classes": ["coaching", "reflection", "feedback", "behavioral_analysis"],
        "branch_criteria": {
            "A": ["growth_catalysis", "exemplar_production", "capability_feedback", "shadow_development"],
            "B": ["bias_detection", "candor_delivery", "pre_mortem", "assumption_challenging"],
        },
        "branch_names": {"A": "Growth Sovereign", "B": "Truth Mirror"},
    },
}


@dataclass
class BattleRecord:
    battle_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    shadow_id: str = ""
    stage_rank: str = "E"
    task_class: str = "general"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    what_worked: list[str] = field(default_factory=list)
    what_failed: list[str] = field(default_factory=list)
    surprises: list[str] = field(default_factory=list)
    heuristics: list[str] = field(default_factory=list)
    quality_score: float = 0.8
    boss_crystal_generated: Optional[str] = None
    xp_awarded: int = 0
    out_of_domain: bool = False
    branch_contribution: Optional[str] = None
    failure_flag: bool = False

    def to_dict(self) -> dict:
        return {
            "battle_id": self.battle_id,
            "shadow_id": self.shadow_id,
            "stage_rank": self.stage_rank,
            "task_class": self.task_class,
            "timestamp": self.timestamp,
            "what_worked": self.what_worked,
            "what_failed": self.what_failed,
            "surprises": self.surprises,
            "heuristics": self.heuristics,
            "quality_score": self.quality_score,
            "boss_crystal_generated": self.boss_crystal_generated,
            "xp_awarded": self.xp_awarded,
            "out_of_domain": self.out_of_domain,
            "branch_contribution": self.branch_contribution,
            "failure_flag": self.failure_flag,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "BattleRecord":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class CapabilityProfile:
    task_class: str
    battle_records: list[BattleRecord] = field(default_factory=list)
    hit_count: int = 0
    success_rate: float = 1.0

    def top_heuristics(self, n: int = 5) -> list[str]:
        """Return the most recent heuristics across battle records."""
        all_h: list[str] = []
        for br in reversed(self.battle_records):
            all_h.extend(br.heuristics)
            if len(all_h) >= n:
                break
        return list(dict.fromkeys(all_h))[:n]  # deduplicate, preserve order

    def top_worked(self, n: int = 3) -> list[str]:
        all_w: list[str] = []
        for br in reversed(self.battle_records):
            all_w.extend(br.what_worked)
        return list(dict.fromkeys(all_w))[:n]

    def top_failed(self, n: int = 3) -> list[str]:
        all_f: list[str] = []
        for br in reversed(self.battle_records):
            all_f.extend(br.what_failed)
        return list(dict.fromkeys(all_f))[:n]

    def to_dict(self) -> dict:
        return {
            "task_class": self.task_class,
            "battle_records": [br.to_dict() for br in self.battle_records],
            "hit_count": self.hit_count,
            "success_rate": self.success_rate,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CapabilityProfile":
        cp = cls(task_class=d["task_class"])
        cp.battle_records = [BattleRecord.from_dict(br) for br in d.get("battle_records", [])]
        cp.hit_count = d.get("hit_count", 0)
        cp.success_rate = d.get("success_rate", 1.0)
        return cp


@dataclass
class Shadow:
    id: str
    name: str
    tier: str = "Knight"          # Knight / Elite Knight / Commander / Marshal / Sovereign
    branch: Optional[str] = None  # A / B / C — set at 150 XP
    xp: int = 0
    capabilities: dict[str, CapabilityProfile] = field(default_factory=dict)
    boss_crystals: list[str] = field(default_factory=list)
    rebirth_count: int = 0
    xp_bonus_pct: float = 0.0     # 20% added per rebirth

    @property
    def registry(self) -> dict:
        return SHADOW_REGISTRY[self.id]

    @property
    def domain(self) -> str:
        return self.registry["domain"]

    @property
    def task_classes(self) -> list[str]:
        return self.registry["task_classes"]

    def build_system_prompt(self, task_class: str, task: str) -> str:
        """Inject battle history as system context — the Igris mechanic."""
        reg = self.registry
        lines = [
            f"You are {self.name} ({reg['tier_label']} tier), domain: {self.domain}.",
            f"Current tier: {self.tier}.",
        ]
        if self.branch:
            branch_name = reg["branch_names"].get(self.branch, self.branch)
            lines.append(f"Evolution branch: {branch_name}.")

        cap = self.capabilities.get(task_class)
        if cap and cap.battle_records:
            lines.append(f"\nBattle history for '{task_class}' ({cap.hit_count} prior engagements, {cap.success_rate:.0%} success):")
            heuristics = cap.top_heuristics()
            if heuristics:
                lines.append("Heuristics from prior battles:")
                for h in heuristics:
                    lines.append(f"  - {h}")
            worked = cap.top_worked()
            if worked:
                lines.append("What has worked:")
                for w in worked:
                    lines.append(f"  - {w}")
            failed = cap.top_failed()
            if failed:
                lines.append("What has failed:")
                for f in failed:
                    lines.append(f"  - {f}")
            if cap.battle_records[-1].boss_crystal_generated:
                lines.append(f"Boss Crystal active: {cap.battle_records[-1].boss_crystal_generated}")

        lines.append(f"\nTask: {task}")
        lines.append("\nDeliver a focused, concrete response. End with:")
        lines.append("BATTLE_RECORD:")
        lines.append("WORKED: <up to 3 bullet points of what succeeded>")
        lines.append("FAILED: <up to 3 bullet points of what didn't work or was ambiguous>")
        lines.append("SURPRISE: <up to 2 unexpected findings>")
        lines.append("HEURISTIC: <up to 3 rules extracted from this engagement>")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "tier": self.tier,
            "branch": self.branch,
            "xp": self.xp,
            "capabilities": {k: v.to_dict() for k, v in self.capabilities.items()},
            "boss_crystals": self.boss_crystals,
            "rebirth_count": self.rebirth_count,
            "xp_bonus_pct": self.xp_bonus_pct,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Shadow":
        s = cls(id=d["id"], name=d["name"])
        s.tier = d.get("tier", "Knight")
        s.branch = d.get("branch")
        s.xp = d.get("xp", 0)
        s.capabilities = {k: CapabilityProfile.from_dict(v) for k, v in d.get("capabilities", {}).items()}
        s.boss_crystals = d.get("boss_crystals", [])
        s.rebirth_count = d.get("rebirth_count", 0)
        s.xp_bonus_pct = d.get("xp_bonus_pct", 0.0)
        return s

    @classmethod
    def default(cls, shadow_id: str) -> "Shadow":
        reg = SHADOW_REGISTRY[shadow_id]
        return cls(id=shadow_id, name=reg["name"])
