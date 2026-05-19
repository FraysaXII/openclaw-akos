---
intellectual_kind: canonical
sharing_label: internal_only
authored: 2026-05-19
last_review: 2026-05-19
owner_role: System Owner
co_owner_role: Founder
co_owner_role_2: PMO
authority: Founder + System Owner + PMO
status: active
language: en
linked_decisions:
  - D-IH-76-A
  - D-IH-76-B
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_MODE_PARITY.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md
linked_initiatives:
  - INIT-OPENCLAW_AKOS-76
paired_runbook:
  - scripts/madeira_methodology_checkpoint.py
---

# MADEIRA Methodology Mode — Specification

> The Methodology mode is the **MADEIRA delta** — what distinguishes Madeira-the-methodology from generic agent runtimes. It runs as an **always-on underlay** beneath every focused mode (Ask / Plan / Agent / Debug) and surfaces methodology-checkpoint candidates that the operator can ratify into the canonical record (LOGIC_CHANGE_LOG, DECISION_REGISTER, principle log). Persistence is **git-backed across sessions**. Brand-voice register check (per the dual-register contract) is mandatory.

## 1. Purpose

Methodology mode operationalises the [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md) commitment to **Madeira-as-methodology**: every operator-agent interaction is an opportunity to capture methodology (principles, patterns, decisions, brand-voice register usage) that compounds across sessions. Without methodology mode, an agent runtime is just a tool that executes tasks; with methodology mode, the runtime is a methodology-capture system that learns Holistika's way-of-working alongside the operator.

## 2. The three architectural commitments

### 2.1 Always-on underlay

Methodology mode runs CONCEPTUALLY underneath every focused mode (Ask, Plan, Agent, Debug). The operator does not need to explicitly transition to methodology mode to get methodology-checkpoint behavior — it surfaces underneath whatever focused mode is active.

**Implementation pattern**: every agent response that emits a non-trivial decision, principle, pattern recognition, or brand-voice register usage MAY end with one or more `[methodology candidate: ...]` annotations. The annotation surfaces the methodology-checkpoint row that WOULD land if the operator ratifies. Operator ratifies via explicit reply (e.g., "yes, mint that"; "land as decision row"; "add to LOGIC_CHANGE_LOG") or via the scratchpad-append pattern from the workflow-shape ratify of 2026-05-19.

**Explicit transition** to methodology mode happens when the operator wants to focus exclusively on methodology authoring:
- Principle-mint session (operator wants to extract principles from recent execution)
- Decision-row backfill (operator wants to walk recent decisions and decide what gets persisted)
- LOGIC_CHANGE_LOG audit (operator wants to review what's been captured)
- Cross-area breakthrough propagation per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md)

### 2.2 Persistent across sessions

The LOGIC_CHANGE_LOG is the canonical persistence vehicle. Every methodology candidate that the operator ratifies lands as a persistent artifact:

- **Decision rows** → [`DECISION_REGISTER.csv`](../../People/Compliance/canonicals/DECISION_REGISTER.csv) row (canonical CSV; requires operator gate per [`akos-governance-remediation.mdc`](../../../../../../.cursor/rules/akos-governance-remediation.mdc))
- **Principles** → principle log under `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/` (TBD by Initiative 79 follow-on; not yet a canonical CSV)
- **LOGIC_CHANGE_LOG rows** → forward canonical CSV (TBD by a future initiative; currently captured in commit messages + decision rows)
- **Scratchpad observations** → per-initiative `operator-scratchpad.md` files (e.g., [`docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md`](../../../../wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md))
- **Cross-area breakthroughs** → [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../../People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) row (per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md))

Methodology continuity across sessions is therefore **git-backed**, not chat-history-backed. A new chat session starts with full context of every prior session's ratified methodology via the canonical CSVs + scratchpad files.

### 2.3 Brand-voice register check is mandatory

Methodology mode is the **enforcement point** for the dual-register contract per [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc). Methodology authoring is where register drift is most likely (the operator is in CORPINT internal vocabulary; a draft slips out into customer-facing prose; jargon leaks).

**Implementation pattern**: every methodology-mode output that crosses a register boundary (CORPINT internal → translated external OR vice versa) is checked against the BBR matrix at [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md). Mismatches surface as `[register check: ...]` annotations alongside `[methodology candidate: ...]` annotations.

## 3. Methodology candidate row schema

Each methodology candidate that methodology mode surfaces follows this shape:

```yaml
candidate_type: decision_row | principle | logic_change_log_row | pattern | breakthrough | register_check
proposed_id: D-IH-NN-X | P-IH-NN-X | LCL-IH-NN-X | etc.
content: <one-sentence essence>
evidence:
  - <file path + line range>
  - <session quote / context>
recommended_action: mint | defer | reject
reversal_path: <how operator can reverse if minted in error>
```

Operator ratifies by reply or by appending to the relevant canonical CSV / scratchpad / log. Defer / reject also have explicit paths (scratchpad note; no-action; etc.).

## 4. Operator UX (how candidates surface; how operator ratifies)

### 4.1 In-line annotation (default)

Methodology candidates surface at the **end of an agent response** as bullet annotations:

> [methodology candidate: D-IH-NN-X — *"Operator ratified inline-streaming-as-norm at workflow gate"* — evidence: this chat 2026-05-19 ~15:30. Recommended: mint at next commit batch. Reversal: edit DECISION_REGISTER.csv row.]

The operator can ratify via reply ("mint that"), defer ("scratchpad it"), or reject ("not yet"). No mandatory action required — annotations are advisory.

### 4.2 Batched (end-of-wave)

At wave closure (or at explicit operator request), methodology mode produces a **batched candidate list** covering all surfaced-but-not-yet-ratified candidates from the wave. Operator walks the list in one batch.

### 4.3 Scratchpad-append (asynchronous)

Operator can append candidate ratifications to the scratchpad at any time, even mid-session. Methodology mode drains the scratchpad at next chat turn.

## 5. Cursor-rules + skill cross-references

This canonical operationalises:

- [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 3 (agentic-as-DoD)
- [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) (BBR register check; enforcement point)
- [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc) (methodology candidates ARE inline-ratify gates in mini)
- [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) (methodology mode surfaces conflicts as candidates)
- [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1 (paired runbook = [`scripts/madeira_methodology_checkpoint.py`](../../../../../../scripts/madeira_methodology_checkpoint.py) forward)
- Skill: [`inline-ratify-craft`](../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md) (methodology candidates use the same craft as full ratify gates, in miniature)

## 6. Verification

- Paired runbook [`scripts/madeira_methodology_checkpoint.py`](../../../../../../scripts/madeira_methodology_checkpoint.py) (forward — implementation deferred until methodology candidate emission is implemented in MADEIRA runtime per I76 P4+P5).
- Pydantic model [`akos/hlk_madeira_mode.py`](../../../../../../akos/hlk_madeira_mode.py) `MadeiraMode` enum includes `methodology` value.
- Mode parity validator [`scripts/validate_madeira_mode_parity.py`](../../../../../../scripts/validate_madeira_mode_parity.py) checks that methodology mode is present with `rbac_posture = methodology-checkpoint` and `persistence_default = persistent-across-sessions`.

## 7. Cross-references

- Sibling canonical: [`MADEIRA_MODE_PARITY.md`](./MADEIRA_MODE_PARITY.md) §3.2 (Methodology mode spec)
- Parent initiative: [I76 MADEIRA elevation](../../../../wip/planning/76-madeira-elevation/master-roadmap.md)
- Doctrinal anchor: [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md), [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md)
- Persistence canonicals: [`DECISION_REGISTER.csv`](../../People/Compliance/canonicals/DECISION_REGISTER.csv), [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../../People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv)
- BBR enforcement: [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md)
