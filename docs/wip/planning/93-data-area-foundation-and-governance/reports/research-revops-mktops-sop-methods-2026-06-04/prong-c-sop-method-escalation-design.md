---
intellectual_kind: research_prong_synthesis
parent_pack: research-revops-mktops-sop-methods-2026-06-04
prong: C
feeds_decision: SOP method escalation pattern (001/002 vs addendum vs method library)
authored: 2026-06-04
sources: SRC-I93-RSM-011..014
---

# Prong C — SOP method escalation and documentation scaling

## Operator directive

Processes should have **methods**. Use `_001`, `_002`, `_XXX` — or addendum, or routing — so scenarios scale without hurting content. Design for many expected SOPs + human and AIC friendly execution.

## What the vault already does (internal sweep)

| Pattern | Example | Meaning in Holistika today |
|:---|:---|:---|
| **Sequential SOP IDs** | `SOP-GRAPHDB_NEO4J_001` → `SOP-KIRBE_GRAPHDB_NEO4J_002` | **Generational successor** — new generation of same domain, often separate `process_list` row |
| **Body + addendum split** | `SOP-META §4.6`, `pattern_sop_addendum_split` | **Depth escalation** — executor body vs auditor/cross-area depth |
| **Method library inside one SOP** | `SOP-ENG_ESTIMATION_DISCIPLINE_001` §3 | **Execution variants** — `method_id` rows + Pydantic registry + drift test |
| **Paired runbook per method** | `akos-executable-process-catalog` RULE 1 | SOP + script; AC-HUMAN + AC-AUTOMATION |
| **Adapter registry** | RPA `power_platform` vs `holistika_edge` | Tooling choice as registry row, not new SOP number |

## Problem diagnosed

Contributors (and P5b) used `_001` only for **first SOP in a family**, but operator intent is **`_001` = family umbrella** and **methods = rows inside** or **`_00N` = only when family forks**. Without explicit SOP-META guidance, agents default to new SOP files for CLI vs Browser — **wrong layer**.

## Recommended hybrid model (mint as SOP-META §4.7)

### Layer 1 — SOP family file (`SOP-<DOMAIN>_<PURPOSE>_001.md`)

One **process family** per outcome. Contains:

- §1 Purpose / §2 Scope
- **§3 Method selection** — decision tree ("when Method A vs B")
- **§4 Method library table** — see below
- §5 Common failure modes
- §6 Cross-references

`process_list.csv` row points to `_001` unless a true fork warrants `_002`.

### Layer 2 — Method library table (inside `_001`)

| method_id | label | executor | runbook_path | when |
|:---|:---|:---|:---|:---|
| `MS-DEMO-METHOD-A` | Azure CLI + PAC | AIC + operator gate | `scripts/ms_demo_cli.py` | Deterministic; CI-friendly |
| `MS-DEMO-METHOD-B` | Portal + Browser | AIC + operator watch | Composio Browser Tool | Licensing UI; screenshot capture |

**Pydantic SSOT:** `akos/hlk_<family>_methods.py` mirroring `engagement_estimation.py` METHODS registry.

**Validator:** method_ids in SOP == registry == runbook exists (or TODO marker per D-IH-72-W).

### Layer 3 — When to use `_002`, `_003` (numbered siblings)

Use **new SOP number** only when:

1. **Generational replacement** (v2 replaces v1 — KiRBe GraphDB pattern).
2. **Regulatory / audience fork** (e.g. customer-facing vs operator-facing **different process**, not just method).
3. **Separate process_list row** with different owner_role or cadence.

**Do NOT** use `_002` for "CLI path" when `_001` Method A suffices.

### Layer 4 — Addendum (unchanged SOP-META §4.6)

Addendum = **cross-area jargon, validator names, mirror DDL, audit rubrics** — NOT execution method variants.

### Layer 5 — Routing between SOP families

When outcome chains (scaffold → demo factory → PDF render):

```markdown
See `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001` §6 → invokes `SOP-DATA_MS_DEMO_FACTORY_001` when stream includes Power Platform.
```

Register pair in `KNOWLEDGE_PAIRING_REGISTRY.csv` (`pairing_class=doctrine_companion` or `sop_runbook`).

## Worked example — Microsoft demo factory (P5c target)

| File | Role |
|:---|:---|
| `SOP-DATA_MS_DEMO_FACTORY_001.md` | Family umbrella + method table (A=CLI, B=Browser) |
| `SOP-DATA_MS_DEMO_FACTORY_001.addendum.md` | Licensing SKUs, Azure tenant IDs policy, audit evidence |
| `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md` | Upstream — routes here when engagement declares Microsoft stack |
| `SOP-DATA_SUEZ_STREAM_B_LIBELLE_001.md` | **Rename/reframe** → engagement-specific **scenario** appendix referencing demo factory + Phase 1/2 handoff |

## Maintenance at scale (many SOPs expected)

| Concern | Mitigation |
|:---|:---|
| Method/runbook drift | Pydantic registry + `--self-test` per family |
| SOP proliferation | Default to method table; `_002` only on fork rubric |
| Human vs AIC | Each method row declares `executor_class: human | aic | hybrid` |
| Discoverability | `REVOPS_PROCESS_CATALOG.yaml` + `process_list` FK to `_001` |

## Forward mint list (not in this research commit)

1. Amend `SOP-META_PROCESS_MGMT_001.md` **§4.7 Method library within SOP families**
2. `pattern_sop_method_library` row in `PEOPLE_DESIGN_PATTERN_REGISTRY.csv`
3. Template block in `SOP-META` addendum A.1 template
4. Refactor P5b `SOP-DATA_SUEZ_STREAM_B_*` to scenario routing pattern
