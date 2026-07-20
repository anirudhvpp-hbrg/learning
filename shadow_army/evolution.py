"""Evolution engine — XP math, tier advancement, branch choice, synergy checks."""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .shadow import Shadow

TIER_THRESHOLDS: dict[str, int] = {
    "Knight": 0,
    "Elite Knight": 150,
    "Commander": 400,
    "Marshal": 900,
    "Sovereign": 2000,
}

TIER_ORDER = list(TIER_THRESHOLDS.keys())

RANK_BASE_XP: dict[str, int] = {
    "E": 10, "D": 25, "C": 50, "B": 100, "A": 200, "S": 500,
}

QUALITY_MULTIPLIERS = [
    (0.8, 1.0),
    (0.5, 0.75),
    (0.3, 0.50),
    (0.1, 0.25),
    (0.0, 0.10),
]

FLEET_SYNERGIES = [
    {
        "name": "Forge & Blade",
        "condition": {"axiom_prime": "Commander", "thresher": "Commander"},
        "effect": "Builds and compresses in a single pass; output is always attach-and-ship.",
    },
    {
        "name": "Oracle Network",
        "condition": {"analyst_prime": "Commander", "strategist_prime": "Commander"},
        "effect": "Research findings auto-feed strategic implications in real time.",
    },
    {
        "name": "Narrative Resonance",
        "condition": {"quill_prime": "Commander", "visionary_prime": "Commander"},
        "effect": "Written artifacts carry foresight weight; communication lands at strategic depth.",
    },
    {
        "name": "Iron Citadel",
        "condition": {"sentinel_prime": "Commander", "titan_prime": "Commander"},
        "effect": "Delivery under adversarial conditions; pressure and defense compound.",
    },
    {
        "name": "Eternal Compass",
        "condition": {"strategist_prime": "Marshal", "visionary_prime": "Marshal"},
        "effect": "Long-range foresight married to tactical execution.",
    },
    {
        "name": "Grandmaster Triad",
        "condition": {"axiom_prime": "Marshal", "sentinel_prime": "Marshal", "thresher": "Marshal"},
        "effect": "S-Rank Stage access unlocked; fleet can handle system-redesign class problems.",
    },
    {
        "name": "Shadow Army Awakening",
        "condition": {sid: "Commander" for sid in [
            "axiom_prime", "sentinel_prime", "thresher", "strategist_prime",
            "genius_prime", "visionary_prime", "analyst_prime", "titan_prime",
            "steward_prime", "quill_prime", "coach_prime",
        ]},
        "effect": "Monarch gains Arise Protocol; fleet self-coordinates without explicit dispatch.",
    },
]


def _tier_gte(tier: str, minimum: str) -> bool:
    return TIER_ORDER.index(tier) >= TIER_ORDER.index(minimum)


def calculate_xp(stage_rank: str, quality_score: float, out_of_domain: bool, xp_bonus_pct: float) -> int:
    base = RANK_BASE_XP.get(stage_rank, 10)
    multiplier = 0.10
    for threshold, mult in QUALITY_MULTIPLIERS:
        if quality_score >= threshold:
            multiplier = mult
            break
    if out_of_domain:
        multiplier *= 0.75
    raw = base * multiplier * (1 + xp_bonus_pct)
    return max(1, round(raw))


def next_tier(current: str) -> Optional[str]:
    idx = TIER_ORDER.index(current)
    if idx + 1 < len(TIER_ORDER):
        return TIER_ORDER[idx + 1]
    return None


def check_tier_advancement(shadow: "Shadow") -> list[str]:
    """Advance tier(s) if XP threshold crossed. Returns list of advancement event strings."""
    events: list[str] = []
    while True:
        nt = next_tier(shadow.tier)
        if nt is None:
            break
        if shadow.xp >= TIER_THRESHOLDS[nt]:
            shadow.tier = nt
            events.append(f"⚡ {shadow.name} advanced to {nt}!")
        else:
            break
    return events


def score_branch(shadow: "Shadow") -> dict[str, float]:
    """Score branches A/B/C based on battle record distribution."""
    from .shadow import SHADOW_REGISTRY
    criteria = SHADOW_REGISTRY[shadow.id].get("branch_criteria", {})
    if not criteria:
        return {}

    counts: dict[str, int] = {k: 0 for k in criteria}
    total = 0
    rank_weights = {"S": 2, "A": 2, "B": 1, "C": 1, "D": 1, "E": 1}

    for cap in shadow.capabilities.values():
        for br in cap.battle_records:
            if br.out_of_domain or br.branch_contribution is None:
                continue
            w = rank_weights.get(br.stage_rank, 1)
            for branch, tags in criteria.items():
                if br.task_class in tags or any(t in br.task_class for t in tags):
                    counts[branch] = counts.get(branch, 0) + w
                    total += w
                    break

    if total == 0:
        return {k: 0.0 for k in criteria}
    return {k: v / total for k, v in counts.items()}


def resolve_branch_choice(shadow: "Shadow") -> tuple[str, str]:
    """
    Return (branch_letter, reason).
    Uses the 3-step tie-breaker from v1.1:
      1. High-rank weight (already baked into score_branch via 2x weights)
      2. Recency (most recent 5 battle records)
      3. Monarch selects → default to highest-scoring
    """
    from .shadow import SHADOW_REGISTRY
    criteria = SHADOW_REGISTRY[shadow.id].get("branch_criteria", {})
    scores = score_branch(shadow)

    if not scores:
        return "A", "no branch criteria — defaulting to A"

    best = max(scores, key=lambda k: scores[k])
    best_score = scores[best]

    # Check if best exceeds 60%
    if best_score >= 0.60:
        branch_name = SHADOW_REGISTRY[shadow.id]["branch_names"].get(best, best)
        return best, f"battle history: {best_score:.0%} toward {branch_name}"

    # Recency tiebreaker: last 5 in-domain records
    recency: dict[str, int] = {k: 0 for k in criteria}
    checked = 0
    for cap in shadow.capabilities.values():
        for br in reversed(cap.battle_records):
            if br.out_of_domain or checked >= 5:
                continue
            for branch, tags in criteria.items():
                if br.task_class in tags or any(t in br.task_class for t in tags):
                    recency[branch] = recency.get(branch, 0) + 1
                    checked += 1
                    break

    rec_best = max(recency, key=lambda k: recency[k]) if recency else best
    branch_name = SHADOW_REGISTRY[shadow.id]["branch_names"].get(rec_best, rec_best)
    return rec_best, f"recency tiebreaker: {branch_name} (no branch exceeded 60%)"


def check_synergies(shadows: dict[str, "Shadow"], active_synergies: list[str]) -> list[dict]:
    """Return newly activated synergies not already in active_synergies."""
    newly_active = []
    for syn in FLEET_SYNERGIES:
        if syn["name"] in active_synergies:
            continue
        met = all(
            sid in shadows and _tier_gte(shadows[sid].tier, min_tier)
            for sid, min_tier in syn["condition"].items()
        )
        if met:
            newly_active.append(syn)
    return newly_active


def parse_battle_record_from_output(raw_output: str, shadow_id: str, stage_rank: str, task_class: str, quality_score: float, xp_awarded: int, out_of_domain: bool, branch_contribution: Optional[str]) -> "BattleRecord":
    """Parse the BATTLE_RECORD block appended by the shadow to its output."""
    from .shadow import BattleRecord

    br = BattleRecord(
        shadow_id=shadow_id,
        stage_rank=stage_rank,
        task_class=task_class,
        quality_score=quality_score,
        xp_awarded=xp_awarded,
        out_of_domain=out_of_domain,
        branch_contribution=branch_contribution,
        failure_flag=quality_score < 0.5,
    )

    section = ""
    for line in raw_output.splitlines():
        line = line.strip()
        if line.startswith("WORKED:"):
            section = "worked"
            val = line[7:].strip()
            if val:
                br.what_worked.append(val)
        elif line.startswith("FAILED:"):
            section = "failed"
            val = line[7:].strip()
            if val:
                br.what_failed.append(val)
        elif line.startswith("SURPRISE:"):
            section = "surprise"
            val = line[9:].strip()
            if val:
                br.surprises.append(val)
        elif line.startswith("HEURISTIC:"):
            section = "heuristic"
            val = line[10:].strip()
            if val:
                br.heuristics.append(val)
        elif line.startswith("- ") and section:
            val = line[2:].strip()
            if section == "worked":
                br.what_worked.append(val)
            elif section == "failed":
                br.what_failed.append(val)
            elif section == "surprise":
                br.surprises.append(val)
            elif section == "heuristic":
                br.heuristics.append(val)

    # Trim to spec limits
    br.what_worked = br.what_worked[:3]
    br.what_failed = br.what_failed[:3]
    br.surprises = br.surprises[:2]
    br.heuristics = br.heuristics[:3]

    return br
