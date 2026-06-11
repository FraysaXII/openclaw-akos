---
title: SSOT Registry Audit Discipline
language: en
status: active
canonical: true
role_owner: Data Governance Office
classification: way_of_working
intellectual_kind: discipline_charter
access_level: 4
audience: J-OP;J-AIC
authored: 2026-06-10
last_review: 2026-06-10
last_review_by: Operator
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-94-A
linked_canonicals:
  - ../../../Architecture/canonicals/CANONICAL_ARTICULATION_MODEL.md
  - ../../../People/Compliance/canonicals/PRECEDENCE.md
  - ../../../People/Compliance/canonicals/CANONICAL_REGISTRY.csv
  - DATAOPS_DISCIPLINE.md
linked_runbooks:
  - scripts/validate_canonical_registry.py
  - scripts/validate_canonical_articulation.py
  - scripts/validate_hlk.py
---

# SSOT Registry Audit Discipline

## Why this exists

Holistika keeps governed knowledge in many files. Four registries tell us what
we own, how pieces connect, and what validators enforce. When a new discipline
lands in the vault but only appears in the precedence index, operators and
agents lose the map — and the same mistake gets repeated every mint.

This discipline is the **repeatable audit loop**, not a one-off cleanup. The
Research Methodology prong lattice (June 2026) was the first full pass; other
areas deserve the same treatment on a rolling basis.

## The four maps

Use these together. They answer different questions.

**Precedence** is the audit-facing index: what is SSOT, who owns it, which
decision ratified it. If it is not here, we do not treat the file as canonical
for compliance purposes.

**Canonical registry** is the inventory of artifacts: path, owner, validator,
active vs proposed. Agents and area-completeness checks use this to find orphans
and ghosts.

**Relationship registry** (HCAM) is how entity types link — composition, serving,
realization. Add a triple when you introduce a new wiring pattern, not for every
new markdown file.

**Governance registry** is for **CSV and mirror surfaces only** (Plane-1
validators, Plane-2 emit). Markdown doctrines live in git; they do not get a
governance-registry row.

The **canonical articulation model** document explains the metamodel. Update it
when the wiring doctrine itself changes.

## When to run the sweep

Run the four-map check whenever:

- A vault canonical is created or materially revised
- WIP intelligence promotes into `docs/references/hlk/v3.0/`
- An initiative closes and claims "doctrine is done"

Also run **area-by-area** reviews (Research, Data, People, Finance, Operations,
…) so older mints that pre-date the registry backfill do not sit in precedence
only.

## Recursive backfill rhythm (binding meta-rule)

Every forward tranche ends with a **look-back** before the next tranche ships.
When work at step N reveals gaps in steps 1..N−1 or parent initiatives (I86
cluster coordinator, I95 canonical articulation), **steer upward** — update
wiring docs, session recap, and registry rows, not only forward motion.

Minimum look-back per tranche:

1. Four-registry lens on **this tranche's mints** (PRECEDENCE → CANONICAL_REGISTRY → HCAM triples → CGR if CSV).
2. Cross-check deferred queue in the initiative wiring doc and session recap.
3. Run validators; record PASS/FAIL in the tranche regression or session recap.
4. If a gap blocks downstream work, close it in the same holistic bundle or
   file an explicit deferred row with owner initiative.

Worked example: methodology mint (2026-06-10) → process_list pairing → capability
promote → QF §6 row — each tranche looked back before Automation OS R2 resumed.

Verification:

```powershell
py scripts/validate_canonical_registry.py --strict
py scripts/validate_canonical_articulation.py --self-test
py scripts/validate_hlk.py
```

## Touch gate — ask before you write

The operator wants agents to **pause and ask** before changing vault canonicals
and canonical CSVs — and still wants canonical work to move forward. The balance:

**Ask first** (via inline `AskQuestion`) before the first Tier-A edit in a
session: vault markdown under `canonicals/`, `PRECEDENCE.md`, `process_list.csv`,
`CANONICAL_REGISTRY.csv`, and sibling compliance dimension CSVs.

**Proceed without re-asking** when the operator already said mint, commit, or
go ahead **for that scope** in the same conversation, or when they answered an
approval question. Bundle related files in one question; do not create approval
fatigue with six gates for one logical mint.

**Ask again** when scope grows — for example adding a process-list tranche to a
discipline-only request.

Tier-B WIP under `docs/wip/intelligence/` is lighter: research ingest can flow;
promotion to vault triggers Tier-A.

## How we talk about it (J-OP and J-AIC)

Summaries to the operator lead with what changed in plain language, then attach
IDs and paths for traceability. Avoid mechanical audit dumps: long tables of
DONE/N/A, identifier chains without functional names, or prose that reads like a
validator log.

Canonicals serve two readers:

- **J-OP** — you — need to understand intent and consequences
- **J-AIC** — agents — need executable steps and falsifiable gates

Internal SOPs still benefit from the copywriting discipline (concrete claims,
fewer AI-tone tics). See the brand copywriting canonical and operator
communication rule RULE 4.

## Agent wiring

Cursor rule: `.cursor/rules/akos-ssot-canonical-touch.mdc`  
Craft skill: `.cursor/skills/ssot-canonical-touch-craft/SKILL.md`

## Cross-references

- HCAM §8: methodology prong articulation worked example
- Wiring report: `docs/wip/intelligence/akos-automation-os-governance-2026-06-10/methodology-cross-area-wiring-2026-06-10.md`
