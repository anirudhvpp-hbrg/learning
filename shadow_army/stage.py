"""Stage classification — 5-signal decision table from SHADOW_FLEET_EVOLUTION.md v1.1."""
from __future__ import annotations
from dataclasses import dataclass

STAGE_DROPS: dict[str, list[str]] = {
    "E": ["Battle Record"],
    "D": ["Battle Record", "Heuristic Fragment"],
    "C": ["Capability Crystal"],
    "B": ["Capability Crystal", "Branch Unlock"],
    "A": ["Evolution Catalyst"],
    "S": ["Monarch Ascension Event"],
}


@dataclass
class StageClassification:
    rank: str
    domain_count: int
    ambiguity: str       # complete / partial / incomplete
    shadow_count: int
    pattern_status: str  # known / novel_variant / first_encounter
    stakes: str          # recoverable / irreversible
    drops: list[str]
    reasoning: str


def classify_stage(task: str, known_task_classes: list[str]) -> StageClassification:
    """
    Apply 5-signal table. Signals inferred from task text heuristics.
    In production, Monarch's decomposition call would supply these directly.
    """
    task_lower = task.lower()

    # Signal 1 — domain count (rough heuristic from keyword density)
    domain_keywords = {
        "architecture": ["architect", "design", "system", "structure", "platform"],
        "analysis": ["analys", "research", "investigat", "pattern", "evidence"],
        "strategy": ["strateg", "stakeholder", "competitive", "position"],
        "writing": ["writ", "narrative", "communicat", "draft", "document"],
        "execution": ["deliver", "execut", "implement", "build", "sprint"],
        "commercial": ["commercial", "pricing", "proposal", "deal", "client"],
        "coaching": ["coach", "reflect", "feedback", "behav"],
    }
    domains_hit = sum(
        1 for kws in domain_keywords.values()
        if any(kw in task_lower for kw in kws)
    )
    domain_count = max(1, domains_hit)

    # Signal 2 — brief completeness
    completeness_signals = ["?", "unclear", "not sure", "explore", "help me", "somehow"]
    has_metric = any(w in task_lower for w in ["goal:", "metric:", "success:", "by ", "must"])
    if any(s in task_lower for s in completeness_signals):
        ambiguity = "incomplete"
    elif has_metric or (":" in task and len(task) > 40):
        ambiguity = "complete"
    else:
        ambiguity = "partial"

    # Signal 3 — shadows required (derived from domain_count)
    if domain_count >= 4:
        shadow_count = 5
    elif domain_count >= 2:
        shadow_count = min(domain_count + 1, 4)
    else:
        shadow_count = 1

    # Signal 4 — pattern status (known if task class in fleet's known classes)
    all_known = set()
    for tc in known_task_classes:
        all_known.add(tc)
    novelty_words = ["novel", "new approach", "never", "first time", "unprecedented", "invent"]
    if any(w in task_lower for w in novelty_words):
        pattern_status = "first_encounter"
    elif any(tc in task_lower.replace(" ", "_") for tc in all_known):
        pattern_status = "known"
    else:
        pattern_status = "novel_variant"

    # Signal 5 — stakes
    irreversible_words = ["publish", "present", "send to client", "ship", "announce", "launch", "irreversible"]
    stakes = "irreversible" if any(w in task_lower for w in irreversible_words) else "recoverable"

    # --- Decision table ---
    rank = _apply_decision_table(domain_count, ambiguity, shadow_count, pattern_status, stakes)

    return StageClassification(
        rank=rank,
        domain_count=domain_count,
        ambiguity=ambiguity,
        shadow_count=shadow_count,
        pattern_status=pattern_status,
        stakes=stakes,
        drops=STAGE_DROPS[rank],
        reasoning=(
            f"domains={domain_count}, brief={ambiguity}, shadows={shadow_count}, "
            f"pattern={pattern_status}, stakes={stakes}"
        ),
    )


def _apply_decision_table(domain_count: int, ambiguity: str, shadow_count: int,
                           pattern_status: str, stakes: str) -> str:
    # Override conditions first
    if pattern_status == "first_encounter" and stakes == "irreversible":
        return "S"
    if pattern_status == "first_encounter":
        return "A"
    if stakes == "irreversible":
        # Minimum B; may be higher from other signals
        floor = "B"
    else:
        floor = "E"

    # Main table
    if domain_count >= 4 or shadow_count >= 4:
        rank = "A"
    elif domain_count >= 2 and pattern_status == "novel_variant":
        rank = "B"
    elif domain_count >= 2:
        rank = "C"
    elif ambiguity == "partial":
        rank = "D"
    else:
        rank = "E"

    # Apply floor
    order = ["E", "D", "C", "B", "A", "S"]
    return order[max(order.index(rank), order.index(floor))]
