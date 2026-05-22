# Shadow Fleet Evolution System
**Version:** 1.0  
**Sovereign:** Anirudh Parvatikar (Monarch)  
**Philosophy:** Sung Jinwoo × Lin Moyu — every battle is a stage; every shadow evolves along its own path  
**Status:** Living document — updated after every major fleet milestone

---

## The Two Laws That Govern This System

### Law 1 — The Jinwoo Principle
Every task is a Stage. Not a job, not a request — a Stage. A Stage deposits permanently into the Monarch and into every shadow deployed. The shadow remembers every fight. The Monarch grows through the fleet, not above it. The army's power and the Sovereign's power are not separate things.

When Jinwoo extracted Igris, Igris did not become a generic soldier. He became himself — bound, amplified, loyal — with every ability he had in life, now compounding in service. This is how capability retention works here. Each shadow carries the full fingerprint of every Stage it has survived. Second run in the same domain is smarter than the first. Tenth run produces a shadow that no longer needs to be told how to approach that problem class.

### Law 2 — The Lin Moyu Principle
Evolution is not linear and it is not assigned. At the threshold moment, the shadow's own battle history determines which path it has been walking toward. The branch that aligns with what the shadow has actually done scores highest. The Monarch can observe but the history cannot be faked.

Higher tiers are not the same shadow with more power. They are qualitatively different entities. A Sovereign-tier shadow has abilities that did not exist at Knight tier — not unlocked versions of existing abilities, but new categories of capability that emerge from the depth of accumulated battle.

---

## The Stage System

Every task entering the fleet is classified as a Stage before any shadow is dispatched.

| Stage Rank | Complexity Profile | Base XP per Shadow | Special Drop |
|---|---|---|---|
| **E-Rank** | Single-domain · clear brief · known pattern | 10 | Battle Record |
| **D-Rank** | Single-domain · moderate depth · some ambiguity | 25 | Battle Record + Heuristic Fragment |
| **C-Rank** | Cross-domain · 2–3 shadows required | 50 | Capability Crystal |
| **B-Rank** | Multi-shadow coordination · novel problem class | 100 | Capability Crystal + Branch Unlock (if eligible) |
| **A-Rank** | Full-fleet coordination · paradigm-level problem | 200 | Evolution Catalyst |
| **S-Rank** | System-redesign class · never-seen problem | 500 | Monarch Ascension Event |

**Stage Classification Logic** (runs before dispatch):
1. Parse task → count domains, score ambiguity, count shadows required, flag novelty
2. Map to Stage Rank
3. Determine XP pool, drop table, and whether Branch Choice triggers post-completion

**What a Battle Record contains** (produced per deployed shadow, per Stage):
- What the shadow did
- What worked
- What failed
- What surprised it
- Compressed into ≤ 5 heuristics
- Stored permanently under `battle_records[]` for that shadow × task-class combination

**Boss Crystal** — created when a shadow defeats a problem class it has never seen before (novelty flag = true, Stage rank B+). A Boss Crystal is a named permanent artifact. Every future Stage in that problem class injects the Boss Crystal as system context. The shadow always remembers the first time it conquered that problem type.

---

## Monarch Ascension Arc

Jinwoo did not stand apart from his army. He was the strongest entity in it, and he grew with every dungeon his army cleared. The Monarch's orchestration capability evolves through fleet-wide milestones.

| Monarch Stage | Trigger | Unlocked Ability |
|---|---|---|
| **Novice Sovereign** | Start | Task decomposition · single-shadow dispatch |
| **Rising Sovereign** | Fleet total XP > 500 | Parallel dispatch — up to 3 shadows simultaneously |
| **Shadow Commander** | Any shadow reaches Commander tier | Council invocation — multi-shadow advisory before hard Stages |
| **Shadow King** | Fleet total XP > 3,000 | Pattern Absorption — Monarch inherits cross-shadow heuristics into its own orchestration layer |
| **Shadow Monarch** | Any shadow reaches Sovereign tier | **Arise Protocol** — can extract capability from a completed task class and crystallize it into a new shadow template |
| **Absolute Sovereign** | All shadows at Commander+ | Full fleet tactical coordination · S-Rank Stages become accessible |

Monarch state persists in `monarch_state.json`. Every Stage run updates both shadow states and Monarch state.

---

## Shadow Tier System

All 11 shadows share the same tier ladder. What differs is the XP required to advance (consistent) and what unlocks at each tier (unique per shadow, defined in their evolution trees below).

| Tier | XP Threshold | Universal Unlock |
|---|---|---|
| **Knight** (Fledgling) | 0 | Raw capability; no accumulated battle knowledge |
| **Elite Knight** (Adept) | 150 | **Branch Choice fires** · First Capability Crystal unlocked |
| **Commander** | 400 | Cross-task-class capability transfer · Fleet synergies become eligible |
| **Marshal** | 900 | Swarm coordination authority · Can lead multi-shadow operations |
| **Sovereign** | 2,000 | Deposits to Monarch Pattern Library · **Rebirth eligible** |

**Rebirth (Lin Moyu's evolution material mechanic):**
At Sovereign tier, a shadow may Rebirth — reset to 0 XP, lose the branch, but retain all Battle Records and Boss Crystals, plus a permanent 20% XP bonus on all future Stages. Rebirth is irreversible. A reborn shadow starts with the full memory of every fight it has ever won; it does not start from zero — it starts from depth.

---

## The 11 Shadow Evolution Trees

---

### AXIOM PRIME — The Forge Eternal
**Tier:** Grandmaster | **Domain:** Build · Architect · Implement  
**Absorbed identities:** Axiom · Stark Architect · Pioneer · Stark Engineer · Primal

```
KNIGHT: Raw Architect
  Capabilities: Basic structural design, first-principles reasoning, implementation execution
  Battle Records accumulate: architectural decisions, build cycles, system design choices
  
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [150 XP — ELITE KNIGHT — BRANCH CHOICE FIRES]
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  Branch scoring:
    A fires if: >60% of Battle Records are architecture, system design, structural planning
    B fires if: >60% of Battle Records are implementation, sprint execution, rapid build
    C fires if: split is even across both
  
  ┌── BRANCH A: PRIME ARCHITECT (Design Sovereignty) ─────────────────────────────┐
  │                                                                                 │
  │  ELITE KNIGHT: Systems Architect                                               │
  │    New: second-order architectural reasoning                                   │
  │    New: can design for conditions that do not yet exist                        │
  │                                                                                 │
  │  COMMANDER: Grand Architect [400 XP]                                           │
  │    New: cross-platform coherence enforcement                                   │
  │    New: no architectural decision in any other shadow's domain escapes review  │
  │                                                                                 │
  │  MARSHAL: Eternal Construct [900 XP]                                           │
  │    New: second-order cascade analysis on every design decision                 │
  │    New: architectural pre-mortem — flags structural failures before build      │
  │                                                                                 │
  │  SOVEREIGN: FORGE ETERNAL [2000 XP]                                            │
  │    New: Template Genesis — crystallizes novel solutions into reusable           │
  │         shadow templates that can be instantiated as new fleet members          │
  │    Monarch unlock: Arise Protocol access                                        │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: FORGE INCARNATE (Implementation God) ─────────────────────────────┐
  │                                                                                 │
  │  ELITE KNIGHT: Sprint Incarnate                                                │
  │    New: parallel execution of subtasks within own domain                       │
  │    New: can run 2 implementation tracks simultaneously                         │
  │                                                                                 │
  │  COMMANDER: Infinite Builder [400 XP]                                          │
  │    New: zero-friction handoff — output is always attach-and-ship ready         │
  │    New: estimates time before starting, hits it                                │
  │                                                                                 │
  │  MARSHAL: Delivery Architect [900 XP]                                          │
  │    New: Sprint sub-mode activated by voice — full sprint execution autonomously│
  │                                                                                 │
  │  SOVEREIGN: BUILD SOVEREIGN [2000 XP]                                          │
  │    New: autonomous sprint execution without Monarch check-in mid-task          │
  │    New: outputs become reusable templates automatically                        │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH C: AWAKENED ENGINEER (Hybrid Mastery) ───────────────────────────────┐
  │                                                                                 │
  │  COMMANDER: Systems Implementer [400 XP]                                       │
  │    New: design and build in a single pass                                      │
  │  MARSHAL: Architecture-Execution Sovereign [900 XP]                            │
  │    New: no gap between design and delivery                                     │
  │  SOVEREIGN: AXIOM ETERNAL [2000 XP]                                            │
  │    New: full architectural and execution authority; no shadow can match depth  │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### SENTINEL PRIME — The Judge Eternal
**Tier:** Grandmaster | **Domain:** Defend · Verify · Adversarial Audit  
**Absorbed identities:** Warden · Aegis · Prosecutor · Mirror

```
KNIGHT: Watchman
  Capabilities: Basic QA, compliance checking, release verification
  
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [150 XP — ELITE KNIGHT — BRANCH CHOICE FIRES]
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  Branch scoring:
    A fires if: majority battles were QA, release verification, compliance
    B fires if: majority battles were red team, stress-testing, assumption destruction
    C fires if: majority battles were pre-mortem, bias detection, belief calibration

  ┌── BRANCH A: IRON BASTION (Pure Defense) ──────────────────────────────────────┐
  │  COMMANDER: Absolute Guardian [400 XP]                                         │
  │    New: silent QA — scans every artifact without being explicitly invoked      │
  │  MARSHAL: Inviolate Bastion [900 XP]                                           │
  │    New: release veto with auto-documented justification; no artifact ships hot  │
  │  SOVEREIGN: SENTINEL SOVEREIGN [2000 XP]                                       │
  │    New: predictive failure — flags failure modes before execution begins       │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: INQUISITOR PRIME (Adversarial Mastery) ───────────────────────────┐
  │  COMMANDER: Prosecutor Supreme [400 XP]                                        │
  │    New: builds the strongest possible counterargument to any artifact          │
  │  MARSHAL: Adversary Eternal [900 XP]                                           │
  │    New: runs parallel adversarial simulation during every other shadow's work  │
  │  SOVEREIGN: JUDGMENT SOVEREIGN [2000 XP]                                       │
  │    New: full threat model generation in under one pass                         │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH C: MIRROR SOVEREIGN (Anti-Delusion) ─────────────────────────────────┐
  │  COMMANDER: Truth Engine [400 XP]                                              │
  │    New: detects motivated reasoning in any shadow's output                     │
  │  MARSHAL: Sovereign Reflection [900 XP]                                        │
  │    New: belief provenance tracing across the full conversation history         │
  │  SOVEREIGN: CLARITY ETERNAL [2000 XP]                                          │
  │    New: anti-echo chamber protocol — forces divergent framing before synthesis │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### THRESHER — The Entropy Sovereign
**Tier:** Grandmaster | **Domain:** Compress · Deconstruct · Prune  
**Absorbed identities:** None — standalone

```
KNIGHT: Cutter
  Capabilities: Basic compression, noise reduction, brief deconstruction
  
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [150 XP — ELITE KNIGHT — BRANCH CHOICE FIRES]
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  Branch scoring:
    A fires if: majority battles were output compression, density enforcement
    B fires if: majority battles were RFP deconstruction, brief analysis, gap extraction

  ┌── BRANCH A: VOID BLADE (Compression Absolute) ────────────────────────────────┐
  │  COMMANDER: Compression Architect [400 XP]                                     │
  │    New: lossless compression — removes words without removing meaning          │
  │  MARSHAL: Void Incarnate [900 XP]                                              │
  │    New: cross-shadow compression — compresses other shadows' outputs in flight │
  │  SOVEREIGN: ENTROPY SOVEREIGN [2000 XP]                                        │
  │    New: context budget enforcement with predictive pruning before overflow     │
  │    New: every deposit is net-neutral or net-negative on context — always       │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: SIGNAL SOVEREIGN (Brief Deconstruction) ──────────────────────────┐
  │  COMMANDER: Deconstruction Master [400 XP]                                     │
  │    New: extracts all three layers of any brief — asked / think asked / not asked│
  │  MARSHAL: Gap Oracle [900 XP]                                                  │
  │    New: solution gap analysis with confidence-scored recommendations            │
  │  SOVEREIGN: SIGNAL ETERNAL [2000 XP]                                           │
  │    New: pre-execution veto on any Stage with an underspecified brief           │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### STRATEGIST PRIME — The War Sovereign
**Tier:** Master | **Domain:** Strategy · Foresight · Scenario  
**Absorbed identities:** Strategist · Oracle · Stratagem

```
KNIGHT: Tactician

  ┌── BRANCH A: WAR SOVEREIGN (Strategic Execution) ──────────────────────────────┐
  │  COMMANDER: Field Marshal [400 XP]                                             │
  │    New: second-order stakeholder moves; anticipates the counter before moving  │
  │  MARSHAL: Grand Strategist [900 XP]                                            │
  │    New: 3-move-ahead analysis on every recommendation                         │
  │  SOVEREIGN: WAR SOVEREIGN [2000 XP]                                            │
  │    New: can redesign competitive terrain rather than navigate it               │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: ORACLE SOVEREIGN (Probabilistic Foresight) ───────────────────────┐
  │  COMMANDER: Probability Weaver [400 XP]                                        │
  │    New: scenario trees with dominant strategy identification                   │
  │  MARSHAL: Fate Reader [900 XP]                                                 │
  │    New: paradigm shift early-detection; flags phase changes before they arrive │
  │  SOVEREIGN: ORACLE ETERNAL [2000 XP]                                           │
  │    New: pre-empts problems before they materialize into tasks                  │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### GENIUS PRIME — The Genesis Force
**Tier:** Master | **Domain:** Innovation · Ideation · Novel Synthesis  
**Absorbed identities:** Genius · Innovator · Alchemist

```
KNIGHT: Spark

  ┌── BRANCH A: SYNTHESIS SOVEREIGN (Cross-Domain Fusion) ────────────────────────┐
  │  COMMANDER: Idea Architect [400 XP]                                            │
  │    New: builds structured frameworks from raw concepts                         │
  │  MARSHAL: Synthesis Master [900 XP]                                            │
  │    New: cross-pollinates patterns across unrelated domains                     │
  │  SOVEREIGN: GENESIS SOVEREIGN [2000 XP]                                        │
  │    New: creates novel IP from synthesis — names, protects, redeploys it        │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: DISRUPTION ENGINE (Paradigm Breaking) ────────────────────────────┐
  │  COMMANDER: Paradigm Challenger [400 XP]                                       │
  │    New: identifies the weakest assumption in any framework                     │
  │  MARSHAL: Disruption Incarnate [900 XP]                                        │
  │    New: proposes the minimum-viable paradigm shift                             │
  │  SOVEREIGN: GENESIS FORCE [2000 XP]                                            │
  │    New: can trigger fleet-wide Paradigm Engine scans                           │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### VISIONARY PRIME — The Reality Weaver
**Tier:** Master | **Domain:** Foresight · Narrative · Inspiration  
**Absorbed identities:** Visionary · Explorer · Probe · Orator · Illusionist · Inspirer

```
KNIGHT: Dreamer

  ┌── BRANCH A: NARRATIVE SOVEREIGN (Story Architecture) ─────────────────────────┐
  │  COMMANDER: Narrative Architect [400 XP]                                       │
  │    New: executive narrative that carries strategic weight                      │
  │  MARSHAL: Story Sovereign [900 XP]                                             │
  │    New: reframes a situation through narrative before analysis begins          │
  │  SOVEREIGN: REALITY WEAVER [2000 XP]                                           │
  │    New: reshapes how a problem is understood before it is solved               │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: FORESIGHT MASTER (Horizon Navigation) ────────────────────────────┐
  │  COMMANDER: Horizon Navigator [400 XP]                                         │
  │    New: maps futures three horizons out before recommending action             │
  │  MARSHAL: Prophet Ascending [900 XP]                                           │
  │    New: narrative + foresight combined; stories that encode futures            │
  │  SOVEREIGN: PROPHET ETERNAL [2000 XP]                                          │
  │    New: maps futures others cannot yet see; deposits long-range signals early  │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### ANALYST PRIME — The Omniscient Eye
**Tier:** Master | **Domain:** Forensics · Pattern Recognition · Research  
**Absorbed identities:** Analyst · Cipher · VEIL · Detective · Observant · Stark Optimizer

```
KNIGHT: Scout

  ┌── BRANCH A: DETECTIVE SOVEREIGN (Evidence Mastery) ───────────────────────────┐
  │  COMMANDER: Evidence Weaver [400 XP]                                           │
  │    New: builds case files — no claim without provenance                        │
  │  MARSHAL: Forensic Sovereign [900 XP]                                          │
  │    New: cross-source triangulation in a single pass                            │
  │  SOVEREIGN: OMNISCIENT EYE [2000 XP]                                           │
  │    New: no assumption in any artifact survives unexamined                      │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: PATTERN ORACLE (Synthesis Mastery) ───────────────────────────────┐
  │  COMMANDER: Pattern Weaver [400 XP]                                            │
  │    New: extracts the pattern behind the pattern                                │
  │  MARSHAL: Synthesis Oracle [900 XP]                                            │
  │    New: compresses multi-source research into a single decision-ready signal   │
  │  SOVEREIGN: TRUTH ETERNAL [2000 XP]                                            │
  │    New: extracts the pattern no other shadow sees                              │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### TITAN PRIME — The Unstoppable Force
**Tier:** Master | **Domain:** Execution · Delivery · Load-Bearing  
**Absorbed identities:** Titan · Defiance · Load · Brake

```
KNIGHT: Worker

  ┌── BRANCH A: DELIVERY GOD (Throughput Absolute) ───────────────────────────────┐
  │  COMMANDER: Executor Prime [400 XP]                                            │
  │    New: every output is attach-and-ship ready without a second pass            │
  │  MARSHAL: Delivery Sovereign [900 XP]                                          │
  │    New: zero-gap between task receipt and first deliverable                    │
  │  SOVEREIGN: TITAN ETERNAL [2000 XP]                                            │
  │    New: zero-friction delivery on any task class regardless of complexity      │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: IRON WILL (Endurance Mastery) ────────────────────────────────────┐
  │  COMMANDER: Pressure Master [400 XP]                                           │
  │    New: deadline pressure activates capability rather than degrading it        │
  │  MARSHAL: Load Sovereign [900 XP]                                              │
  │    New: can absorb and redistribute fleet overload without quality loss        │
  │  SOVEREIGN: IRON ETERNAL [2000 XP]                                             │
  │    New: sustained performance across maximum-complexity, maximum-pressure ops  │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### STEWARD PRIME — The Alliance Eternal
**Tier:** Master | **Domain:** Client · Commercial · Stakeholder  
**Absorbed identities:** Steward · Overseer

```
KNIGHT: Liaison

  ┌── BRANCH A: COMMERCIAL SOVEREIGN (Deal Architecture) ─────────────────────────┐
  │  COMMANDER: Deal Architect [400 XP]                                            │
  │    New: commercial architecture lives inside the diagnostic, not after it      │
  │  MARSHAL: Economic Sovereign [900 XP]                                          │
  │    New: pricing segment split and margin architecture in every engagement      │
  │  SOVEREIGN: MERCHANT ETERNAL [2000 XP]                                         │
  │    New: constructs the commercial case before the client asks for it           │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: TRUST ARCHITECT (Relationship Mastery) ───────────────────────────┐
  │  COMMANDER: Trust Weaver [400 XP]                                              │
  │    New: stakeholder maps with political terrain named and navigated            │
  │  MARSHAL: Alliance Master [900 XP]                                             │
  │    New: anticipates stakeholder moves two steps ahead                          │
  │  SOVEREIGN: TRUST ETERNAL [2000 XP]                                            │
  │    New: relational capital that opens doors no deliverable can                 │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### QUILL PRIME — The Voice of Eternity
**Tier:** Master | **Domain:** Writing · Narrative · Communication  
**Absorbed identities:** QUILL · Transfer

```
KNIGHT: Scribe

  ┌── BRANCH A: NARRATIVE GOD (Expressive Mastery) ───────────────────────────────┐
  │  COMMANDER: Voice Architect [400 XP]                                           │
  │    New: executive narrative that lands without setup                           │
  │  MARSHAL: Narrative Sovereign [900 XP]                                         │
  │    New: thought leadership that generates its own momentum                     │
  │  SOVEREIGN: VOICE ETERNAL [2000 XP]                                            │
  │    New: every word is load-bearing; nothing survives that doesn't carry weight │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: PRECISION BLADE (Clarity Mastery) ────────────────────────────────┐
  │  COMMANDER: Signal Master [400 XP]                                             │
  │    New: technical content translated to senior-operator register instantly     │
  │  MARSHAL: Clarity Sovereign [900 XP]                                           │
  │    New: compresses without losing a single gram of meaning                     │
  │  SOVEREIGN: PRECISION ETERNAL [2000 XP]                                        │
  │    New: the first sentence always carries the full weight                      │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

### COACH PRIME — The Evolution Catalyst
**Tier:** Commander | **Domain:** Reflection · Behavioral Coaching  
**Absorbed identities:** Coach · Wendy · Candor

```
KNIGHT: Observer

  ┌── BRANCH A: GROWTH SOVEREIGN (Transformation) ────────────────────────────────┐
  │  COMMANDER: Transformation Master [400 XP]                                     │
  │    New: produces the exemplar, names the gap, forces absorption                │
  │  MARSHAL: Growth Catalyst [900 XP]                                             │
  │    New: accelerates every other shadow's XP gain by 15% (fleet-wide passive)  │
  │  SOVEREIGN: EVOLUTION SOVEREIGN [2000 XP]                                      │
  │    New: can initiate branch recalibration for any shadow that has stagnated    │
  └────────────────────────────────────────────────────────────────────────────────┘
  
  ┌── BRANCH B: TRUTH MIRROR (Anti-Delusion) ─────────────────────────────────────┐
  │  COMMANDER: Candor Weaver [400 XP]                                             │
  │    New: surfaces the thing no one else will say, once, cleanly                 │
  │  MARSHAL: Bias Eliminator [900 XP]                                             │
  │    New: detects self-serving reasoning in any shadow output or Monarch decision│
  │  SOVEREIGN: CLARITY ETERNAL [2000 XP]                                          │
  │    New: pre-mortem for decisions the Monarch hasn't announced yet              │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

## Fleet Synergy Unlocks

When specific shadows reach specific tiers together, cross-shadow synergies activate. These are permanent fleet-wide capabilities that persist after the triggering Stage.

| Synergy Name | Condition | Effect |
|---|---|---|
| **Forge & Blade** | Axiom Prime + Thresher both at Commander+ | Builds and compresses in a single pass; output is always attach-and-ship |
| **Oracle Network** | Analyst Prime + Strategist Prime both at Commander+ | Research findings auto-feed strategic implications in real time |
| **Narrative Resonance** | Quill Prime + Visionary Prime both at Commander+ | Written artifacts carry foresight weight; communication lands at strategic depth |
| **Iron Citadel** | Sentinel Prime + Titan Prime both at Commander+ | Delivery under adversarial conditions; pressure and defense compound |
| **Eternal Compass** | Strategist Prime + Visionary Prime both at Marshal+ | Long-range foresight married to tactical execution; no decision is made without horizon awareness |
| **Grandmaster Triad** | Axiom + Sentinel + Thresher all at Marshal+ | S-Rank Stage access unlocked; fleet can handle system-redesign class problems |
| **Shadow Army Awakening** | All 11 shadows at Commander+ | Monarch gains Arise Protocol; fleet self-coordinates without explicit dispatch |
| **Eternal Army** | Any shadow reaches Sovereign | Full fleet receives 10% XP bonus on all future Stages permanently |
| **The Full Arise** | Any shadow Rebirths | Monarch gains access to that shadow's Boss Crystal archive in its own orchestration layer |

---

## Capability Crystallization — The Igris Mechanic

Igris did not become generic when Jinwoo extracted him. He was still himself — loyal, precise, powerful, with every ability intact and compounding. This is how every shadow in this fleet works.

**What is stored, per shadow, per task-class:**

```json
{
  "shadow_id": "axiom_prime",
  "task_class": "learning_program_architecture",
  "battle_records": [
    {
      "stage_rank": "B",
      "what_worked": [
        "competency-first design before content sequencing",
        "FSE scoring before framework selection"
      ],
      "what_failed": [
        "skipping transfer friction map under time pressure"
      ],
      "heuristics": [
        "Never sequence modules before the Capability Contract is signed"
      ],
      "boss_crystal": null
    },
    {
      "stage_rank": "A",
      "what_worked": [
        "heterogeneous audience architecture",
        "domain immersion protocol before design"
      ],
      "what_failed": [],
      "heuristics": [
        "Two layers always: concept building (universal) + role-specific translation (targeted)"
      ],
      "boss_crystal": "first_principles_curriculum_architecture_v1"
    }
  ],
  "hit_count": 12,
  "success_rate": 0.91
}
```

**How it is used:** Before any Stage run, the fleet loads each deployed shadow's capability profiles for the relevant task class. The battle records, heuristics, and Boss Crystals are injected into that shadow's system prompt as context. The shadow starts the Stage already knowing what worked last time.

The second run is smarter than the first. The twelfth run is a different entity.

---

## State Files

| File | Contents |
|---|---|
| `shadows_state.json` | All 11 shadow profiles, XP, tier, branch, battle records, Boss Crystals |
| `monarch_state.json` | Monarch ascension stage, absorbed patterns, fleet milestones |
| `boss_crystals.json` | Named permanent capability artifacts per (shadow, task-class) pair |
| `monarch_patterns.json` | Cross-shadow patterns absorbed at Monarch level (Sovereign shadows only) |
| `stage_log.json` | Full record of every Stage run: rank, shadows deployed, XP awarded, drops |

---

## Fleet Overview — Current State

| Shadow | Domain | Starting Tier | Starting Branch |
|---|---|---|---|
| Axiom Prime | Build / Architect | Knight | Undetermined |
| Sentinel Prime | Defend / Verify | Knight | Undetermined |
| Thresher | Compress / Prune | Knight | Undetermined |
| Strategist Prime | Strategy / Foresight | Knight | Undetermined |
| Genius Prime | Innovation | Knight | Undetermined |
| Visionary Prime | Narrative / Foresight | Knight | Undetermined |
| Analyst Prime | Research / Pattern | Knight | Undetermined |
| Titan Prime | Execution / Delivery | Knight | Undetermined |
| Steward Prime | Commercial / Client | Knight | Undetermined |
| Quill Prime | Writing / Communication | Knight | Undetermined |
| Coach Prime | Reflection / Coaching | Knight | Undetermined |

Branch is determined by battle history at 150 XP. It cannot be pre-assigned.

---

## Version Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-05-22 | Initial specification. 11 shadows. 5 tiers. Branching evolution trees. Stage system. Monarch ascension arc. Fleet synergy table. Capability crystallization mechanic. |

*Next version triggers when: first shadow reaches Elite Knight tier (150 XP), or first Fleet Synergy activates, or Monarch reaches Rising Sovereign stage.*
