# I86 — Asset classification

> Per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) and [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §HLK compliance governance. **I86 produces no new Holistika vault SSOT canonicals** under `docs/references/hlk/v3.0/Admin/O5-1/**/canonicals/` — it coordinates siblings that do.

## Canonical (edit here first)

| Asset | Path | Class rationale |
|:---|:---|:---|
| Initiative registry row | [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) | Standard INIT mint for governed initiative (`INIT-OPENCLAW_AKOS-86`). |
| Decision register rows | [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) | D-IH-86-A..E charter ratifications. |
| OPS register row | [`OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) | OPS-86-1 cluster coordination action (open until cluster closes). |

## Mirrored / derived

| Asset | Path | Class rationale |
|:---|:---|:---|
| (none in I86 scope) | — | No compliance mirror DDL for I86; no dimensional CSV mint. |

## Reference-only / planning-meta

| Asset | Path | Class rationale |
|:---|:---|:---|
| Initiative folder | `docs/wip/planning/86-initiative-cluster-execution-coordinator/**` | Planning traceability per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc); not operational SSOT for Holistika vault prose. |
| Dependency map | [`INITIATIVE_DEPENDENCIES.md`](../_templates/INITIATIVE_DEPENDENCIES.md) | Readable mirror of CSV + wave narrative; CSV wins on conflict. |
| I87 candidate stub | [`i87-openclaw-operator-runtime-hardening.md`](../_candidates/i87-openclaw-operator-runtime-hardening.md) | Candidate charter scaffold; promotion moves to `planning/87-*/` when numbered folder mints. |

## Doctrinal note

I86 is an **operational-initiative class** sibling to **I64** (Governance Mission Control) and **I65** (Planning Workspace Panel): it exists to **orchestrate execution posture**, not to mint compliance prose or dimensional registers. All substantive canonical mints in Waves 1-5 remain attributed to **I81, I84, I85, I82, I83, I74, I75, I76, I87** respectively.
