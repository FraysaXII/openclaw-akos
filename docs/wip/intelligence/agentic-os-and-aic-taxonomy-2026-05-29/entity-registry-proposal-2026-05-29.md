---
title: AGENTIC_ENTITY_REGISTRY — design proposal for operator gate (2026-05-29)
language: en
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP
authored: 2026-05-29
last_review: 2026-05-29
status: shape-ratified-pending-build
linked_research_sources:
  - docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/source-ledger.csv
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md
---

# Proposal: AGENTIC_ENTITY_REGISTRY.csv (Phase 2b)

> **Shape gate cleared 2026-05-29 → this is now the build spec.** DQ-TAX-05 =
> include-now means a new canonical database file — a **hard operator gate** per
> [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc)
> + [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc).
> The operator ratified the shape on 2026-05-29: **Option 1 (new dedicated
> registry) + demonstrator seed**. The design below is the build spec for the
> execution seat (Composer). Nothing is canonical yet — the bundle in
> §"Governance bundle" is what writes it and runs the validators + sweeps as it
> lands. Everything above that bundle stays reversible until the build commits.

## Decisions taken (recommended defaults; reversible)

- **Shape: Option 1** — a NEW `AGENTIC_ENTITY_REGISTRY.csv` for non-AIC +
  external entities. Keeps [`AIC_REGISTRY.csv`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_REGISTRY.csv)
  pure (it is the SSOT for agents holding **named Holistika roles**; RPA bots and
  serverless workers do not hold roles). The wider field gets its own table with
  the ratified capability-tier axis built in.
- **Seed breadth: demonstrator** — a few honest rows per class with `status` /
  `governance_posture` flags that reflect reality (we are cataloguing the field,
  not claiming integration). Mirrors how AIC_REGISTRY (5 rows) and the per-task
  registry (3 rows) seeded.
- **Name:** `AGENTIC_ENTITY_REGISTRY` (not `AGENTIC_WORKER`) because the taxonomy
  covers BOTH non-AIC workers AND third-party AICs (which are agents, just not
  Holistika's) — "entity" is the accurate superset. Rename on request.

## Proposed schema (14 columns; mirrors sibling-registry conventions)

| Column | Type / enum |
|:---|:---|
| `entity_id` | PK, shape `AENT-<NAME>` |
| `entity_name` | string |
| `entity_class` | `aic-third-party` / `rpa-bot` / `serverless-worker` / `agent-as-a-service` / `harness-as-a-service` / `text-only-agent` / `workflow-automation` |
| `capability_tier` | `chatbot` / `workflow` / `agent` / `autonomous` (DQ-TAX-02) |
| `substrate_or_vendor` | string (what it's made of / who runs it) |
| `holistika_relationship` | `integrated-consumer` / `evaluated` / `external-reference` / `competitor-watch` / `not-applicable` |
| `governance_posture` | `governed` / `inventoried` / `reference-only` (mirrors REPOSITORY_REGISTRY) |
| `status` | `active` / `candidate` / `reference` / `deprecated` |
| `notes` | string |
| `last_review_at` | date |
| `last_review_by` | role (must FK-resolve to baseline_organisation, or `Founder`) |
| `last_review_decision_id` | FK → DECISION_REGISTER |
| `methodology_version_at_review` | e.g. `v3.1` |
| `source_refs` | optional `;`-list → source-ledger.csv rows |

## Proposed demonstrator seed (6 honest rows; all `status=reference`)

| entity_id | entity_class | capability_tier | holistika_relationship | governance_posture |
|:---|:---|:---|:---|:---|
| `AENT-CURSOR-THIRD-PARTY-AGENTS` | aic-third-party | agent | integrated-consumer | inventoried |
| `AENT-CLOUDFLARE-WORKERS-AI` | serverless-worker | workflow | external-reference | reference-only |
| `AENT-RPA-CLASS-GENERIC` | rpa-bot | workflow | external-reference | reference-only |
| `AENT-AGENT-AS-A-SERVICE-GENERIC` | agent-as-a-service | agent | external-reference | reference-only |
| `AENT-HARNESS-AS-A-SERVICE-GENERIC` | harness-as-a-service | agent | external-reference | reference-only |
| `AENT-TEXT-ONLY-LLM-GENERIC` | text-only-agent | chatbot | external-reference | reference-only |

Honest posture: only the first row is something Holistika actually consumes
(third-party agents inside Cursor); the rest are field-catalogue reference rows.
No fake "integrated" claims.

## Governance bundle (runs ON your approval — the gated activation)

1. Place `AGENTIC_ENTITY_REGISTRY.csv` at `…/People/Compliance/canonicals/dimensions/`.
2. Pydantic chassis `akos/hlk_agentic_entity_registry_csv.py` (FIELDNAMES tuple = SSOT; enum frozensets) per `CONTRIBUTING.md`.
3. Validator `scripts/validate_agentic_entity_registry.py` (+ register in `validate_hlk.py` umbrella + `--self-test` in pre_commit).
4. PRECEDENCE.md canonical row.
5. Supabase mirror DDL + `validate_compliance_schema_drift.py` registry row [GG-2].
6. DECISION_REGISTER row — a formal `D-IH-86-*` covering the taxonomy ratification (DQ-TAX-01..05) + this expansion.
7. Synthesis-before-tranche sweep (canonical_csv_mint class) [GG-1] + index/regression sweeps [GG-3] before commit.
8. ARCHITECTURE.md HLK Registry + USER_GUIDE.md HLK Operator Model row (docs-config-sync).

## Operator gate — CLEARED 2026-05-29 (Option 1 + demonstrator seed)

The shape gate is cleared. **Build path:** push the build button with the
execution model (Composer) on the rollout plan's entity-registry phase, and
include this guardrail verbatim in the build instruction so the execution seat
does not repeat the stale-state miss from the 2026-05-29 regression:

> Before creating any CSV, Pydantic model, validator, PRECEDENCE row, or mirror
> table, **verify it does not already exist** (search the canonicals tree +
> `akos/` + `scripts/`). If it already exists, **extend** it instead of minting,
> and **stop and report** the collision. Run the synthesis-before-tranche +
> index + regression sweeps before commit.

The thinking seat (this session) recorded the clearance; the mechanical bundle is
the execution seat's job per the two-seat discipline
([`aic-delegation-craft`](../../../../.cursor/skills/aic-delegation-craft/SKILL.md)).
If you'd rather I build it here in this session instead of pushing build, just
say so — but your stated intent was to run it on Composer, and with the guardrail
above that is the right call.
