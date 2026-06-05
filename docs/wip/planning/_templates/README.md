---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-17
role_owner: PMO
classification: fact
ssot: true
---

# Planning templates — index

The three files in this folder are the SSOT for how Holistika initiatives are discovered, planned, ratified, and executed inside Cursor. Previous trio + per-initiative kickoff files (`initiative-planning-prompts.md` + `i71..i76-kickoff-prompt.md`) are **superseded** as of 2026-05-15 (see §"Legacy artefacts" below).

## Compendium SSOT

> [`PLANNING_COMPENDIUM.md`](PLANNING_COMPENDIUM.md) — the discipline.

~1500 lines. The single source of truth for initiative discipline: 12-row plan-quality bar (with self-critique gate + CHANGELOG entry as Rows 11 & 12), Discovery / Plan-Author / Pre-flight pipelines, inline-ratify authoring guide, external-research bar (≥4 sources with full schema), per-phase deep-section template, decision-log + risk-register preview format, mermaid diagram discipline, anti-patterns. §11 is the per-initiative appendix (one section per active or candidate initiative; points at canonicals rather than re-encoding content).

Read end-to-end at the start of any planning session.

## Executor packet (Composer seat)

> [`executor-packet-template.md`](executor-packet-template.md) — bounded execution brief for
> thinking-seat → Composer handoffs. **Worked example:** Finance F1 at
> `docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-executor-packet-f1-2026-06-05.md`
> + paired workflow `finance-area-two-seat-workflow-2026-06-05.md`.

Pair every packet with a one-page tranche charter and run
`py scripts/synthesis_before_tranche_check.py --check-charter <path>` before dispatch.

## Kickstart paste-snippet

> [`UNIVERSAL_KICKSTART.md`](UNIVERSAL_KICKSTART.md) — the paste-snippet.

~120 lines. Paste this into a fresh Cursor chat. Routes the agent through:

1. Mandatory read-pass (the compendium + the dep map).
2. Mode routing (fresh / gated_operator activation / mid-execution / TRIGGER-watch).
3. Per-mode entry checklist.
4. Self-critique gate hand-off.
5. Inline-ratify discipline reminder.
6. Phase + commit discipline reminder.

## Dependency map

> [`INITIATIVE_DEPENDENCIES.md`](INITIATIVE_DEPENDENCIES.md) — the dep map.

Mermaid graph LR covering I59..I87 + per-initiative blocker table + cross-strand linkages section. Read this alongside the compendium during compendium §3.2 read-pass.

Updated every time an initiative is promoted, closed, or has a TRIGGER-watch state change.

## Per-initiative state (at a glance)

| Initiative | Slug | State | Blockers (today) | Compendium appendix |
|:---|:---|:---|:---|:---|
| **I70** | Holistika OS Self-Governance | closed (2026-05-13) | — | [§11.1](PLANNING_COMPENDIUM.md#§111-i70--holistika-os-self-governance-foundation-closed-2026-05-13) |
| **I71** | CICD Discipline + AIOps Baseline Maturity | closed (2026-05-14) | — | [§11.2](PLANNING_COMPENDIUM.md#§112-i71--cicd-discipline-and-aiops-baseline-maturity-closed-2026-05-14) |
| **I72** | Marketing Area Governance + Persona Registry + IntelligenceOps + RevOps + Process Catalog | closed (2026-05-14) | — | [§11.3](PLANNING_COMPENDIUM.md#§113-i72--marketing-area-governance--persona-registry--intelligenceops--revops--process-catalog-closed-2026-05-14) |
| **I73** | People Operations + Engagement Models + Methodology IP (mega-initiative) | closed (2026-05-15) | — | [§11.4](PLANNING_COMPENDIUM.md#§114-i73--people-operations--engagement-models--methodology-ip-active) |
| **I74** | Brand-tooling productization | candidate (TRIGGER-watch) | TRIGGER-2 not fired (0 external requests) | [§11.5](PLANNING_COMPENDIUM.md#§115-i74--brand-tooling-productization-candidate--trigger-watch) |
| **I75** | Research area governance | candidate | I73 closed (MET); Research Director / KM framing commits still pending | [§11.6](PLANNING_COMPENDIUM.md#§116-i75--research-area-governance-candidate) |
| **I76** | MADEIRA elevation | candidate | Strand A external research + AIC architecture ratification (PENDING) | [§11.7](PLANNING_COMPENDIUM.md#§117-i76--madeira-elevation-candidate) |
| **I77** | Impeccable Brand-Bridge Refresh + Drift Gate | closed (2026-05-16 `D-IH-77-CLOSURE-V2`) | — | [§11.8](PLANNING_COMPENDIUM.md#§118-i77--impeccable-brand-bridge-refresh--drift-gate-closed-2026-05-16) |
| **I78** | Brand-voice LLM-as-judge advisory | **active** (`INIT-OPENCLAW_AKOS-78`; `D-IH-78-A`) | P1 judge chassis + CLI pending; [`master-roadmap.md`](../78-brand-voice-llm-as-judge/master-roadmap.md) | [§11.9](PLANNING_COMPENDIUM.md#§119-i78--brand-voice-llm-as-judge-advisory-layer-active--execution) |
| **I79** | People Manifesto + Knowledge Hygiene + Cross-area Design Patterns + AI Governance (mega-initiative; follow-up to I73 doctrinal layer) | closed 2026-05-15 (`D-IH-79-CLOSURE`) | P0–P8 mega-initiative six strands + UAT + integration verification; 24/1165 process_list FK seeds; anti-jargon drift gate operational | [`docs/wip/planning/79-people-manifesto-and-pattern-library/master-roadmap.md`](../79-people-manifesto-and-pattern-library/master-roadmap.md) |
| **I80** | I79 Lessons-Learned (SOP Body/Addendum Pattern + Stakeholder Lenses + Inline-Ratify Craft Skill) | **CLOSED 2026-05-16** (`D-IH-80-CLOSURE`) | All P0..P7 phases shipped: pattern minted + 8 paired-file instantiations + inline-ratify skill + UAT + I81 forward-charter | [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../80-i79-lessons-learned/master-roadmap.md) |
| **I81** | Vault integrity + Compliance layout + named-milestone schema + SOP retrofit | **active** (`INIT-OPENCLAW_AKOS-81`; charter 2026-05-16) | Operator gates per P2 tranche; see roadmap Verification | [`docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/master-roadmap.md`](../81-vault-integrity-layout-milestones-retrofit/master-roadmap.md) |
| **I82** | Holistika Capability Doctrine + Commercial Readiness | **active** (`INIT-OPENCLAW_AKOS-82`) | `baseline_organisation` Talent tranche + registry mint gates | [`docs/wip/planning/82-holistika-capability-doctrine/master-roadmap.md`](../82-holistika-capability-doctrine/master-roadmap.md) |
| **I83** | AI Archivist + KiRBe Ingestor (Tech-area-led; consumes I82 use case archive + I80 P6.5 KNOWLEDGE_PAIRING_REGISTRY; 9-12d MVP) | candidate (stub minted at I80 P7) | I82 P4 closed (use case archive minted); Tech Lab Lead bandwidth; framework choice + schema home + Composio adoption ratifications | [`docs/wip/planning/_candidates/i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) |
| **I84** | Substrate Doctrine + Commercial Readiness | **closed** (2026-05-17 `D-IH-84-CLOSURE`) | Quarterly substrate-audit cadence (operational); SOP `status: review` until process_list row | [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md`](../84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) |
| **I85** | Audience-tag canonicalization | **active** (`INIT-OPENCLAW_AKOS-85`) | P2 tag-migration tranche approvals | [`docs/wip/planning/85-audience-tag-canonicalization/master-roadmap.md`](../85-audience-tag-canonicalization/master-roadmap.md) |
| **I86** | Initiative Cluster Execution Coordinator | **active** (`INIT-OPENCLAW_AKOS-86`) | Siblings not all closed | [`docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md`](../86-initiative-cluster-execution-coordinator/master-roadmap.md) |
| **I87** | OpenClaw operator-runtime hardening | **active** (`INIT-OPENCLAW_AKOS-87`) | Phases P1–P6 per roadmap | [`docs/wip/planning/87-openclaw-operator-runtime-hardening/master-roadmap.md`](../87-openclaw-operator-runtime-hardening/master-roadmap.md) |

State truth: [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) + candidate files under [`_candidates/`](../_candidates/). The compendium appendix sub-sections point at these canonicals; this table is a navigation surface, not a state SSOT.

## Plan-scope principle (binding)

**One Cursor plan per INITIATIVE — not per phase, not per strand, not per execution slice.** The reference shape is `~/.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md` — one ~4 300-line strategic plan covering 17 phases, 5 regression rounds, verbatim operator-quote capture, inline `AskQuestion` ratification throughout. Filename `<initiative-slug>_<8hex>.plan.md` (no phase prefix). Depth grows via regression rounds **inside the same file**, not by spawning sibling files.

Per `PLANNING_COMPENDIUM.md` §12.1, phase-scoped or strand-scoped plan files are an explicit anti-pattern.

## Legacy artefacts (SUPERSEDED)

The following files are kept as 10-line redirect stubs only. They were the prior generic-trio + per-initiative kickoff templates, superseded by the compendium + universal kickstart pair on 2026-05-15:

- [`initiative-planning-prompts.md`](initiative-planning-prompts.md) — generic Discovery / Plan-Author / Pre-flight trio. Now → `PLANNING_COMPENDIUM.md` §3-§5.
- [`i71-kickoff-prompt.md`](i71-kickoff-prompt.md) — I71 per-initiative template. Initiative closed; appendix § now in compendium §11.2.
- [`i72-kickoff-prompt.md`](i72-kickoff-prompt.md) — I72 per-initiative template. Initiative closed; appendix § now in compendium §11.3.
- [`i73-kickoff-prompt.md`](i73-kickoff-prompt.md) — I73 per-initiative template. Initiative active (P0 ratified 2026-05-15); appendix § now in compendium §11.4. `fresh` mode no longer needed for I73 (use `mid-execution` mode in `UNIVERSAL_KICKSTART.md`).
- [`i74-kickoff-prompt.md`](i74-kickoff-prompt.md) — I74 per-initiative template. Now → compendium §11.5 (TRIGGER-watch).
- [`i75-kickoff-prompt.md`](i75-kickoff-prompt.md) — I75 per-initiative template. Now → compendium §11.6.
- [`i76-kickoff-prompt.md`](i76-kickoff-prompt.md) — I76 per-initiative template. Now → compendium §11.7.

Each stub points at the relevant compendium anchor + carries frontmatter `status: superseded`, `superseded_by: docs/wip/planning/_templates/PLANNING_COMPENDIUM.md`, `superseded_date: 2026-05-15`.

## Cursor rules (always-applied) that operationalise this folder

- [`.cursor/rules/akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — plan-quality bar, master-roadmap mirror, UAT vs automated smoke, files-modified CSV.
- [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — inline `AskQuestion`; never `OPERATOR PAUSE POINT`.
- [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — phase + commit discipline; SCOPE / PREREQUISITES / DELIVERABLES / VERIFICATION.
- [`.cursor/rules/akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — operator pause-point contract + agent self-checkpoint contract.
- [`.cursor/rules/akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc) — AKOS-as-SSOT for external repos.
