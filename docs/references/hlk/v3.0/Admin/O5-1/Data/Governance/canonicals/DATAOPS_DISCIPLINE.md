---
title: DataOps Discipline
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - Data Governance Lead
  - System Owner
  - PMO
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_at: 2026-06-04
last_review_decision_id: D-IH-93-C
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-BV
  - D-IH-90-AA
  - D-IH-93-C
  - D-IH-93-H
status: active
register: internal
linked_canonicals:
  - ../../canonicals/DATA_AREA_CHARTER.md
  - ../../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - ../../../People/canonicals/UAT_DISCIPLINE.md
  - ../../../People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md
  - ../../../People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../../../People/Compliance/canonicals/PRECEDENCE.md
linked_cursor_rules:
  - .cursor/rules/akos-dataops-discipline.mdc
  - .cursor/rules/akos-holistika-operations.mdc
  - .cursor/rules/akos-quality-fabric.mdc
  - .cursor/rules/akos-planning-traceability.mdc
companion_to:
  - ../../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - ../../canonicals/DATA_AREA_CHARTER.md
linked_runbooks:
  - scripts/dataops_quality_check.py
  - scripts/sync_compliance_mirrors_from_csv.py
  - scripts/apply_mirror_batches.ps1
  - docs/guides/holistika-mirror-dml-apply.md
linked_sops:
  - SOP-TECH_DATAOPS_QUALITY_001.md
---

# DataOps Discipline

> The **Data-area** meta-doctrine (Governance sub-domain) that names how
> every Holistika data artefact's quality bar is derived — across canonical
> CSVs, Supabase mirrors, FDW projections, and observability surfaces.
> Re-homed from People per **D-IH-93-C** / **D-IH-93-H** (I93 P1). Minted
> at Wave M P5 per **D-IH-86-BV**; promoted active at I90 P3c per
> **D-IH-90-AA**. Eighth Quality Fabric specialty materialisation of
> [`HOLISTIKA_QUALITY_FABRIC.md`](../../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md).

## 1. Purpose

Holistika operates on a **dual-plane data model**: git-canonical CSVs
under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`
(SSOT for governance) + Supabase mirrors / FDW projections / `holistika_ops`
operational tables (runtime + projection). When the two planes drift,
governance loses its grip — operators read stale projections, agents act
on out-of-date FK targets, and the audit trail decouples from the
authority.

DataOps Discipline names the quality bar that prevents drift across
**all data surfaces** — canonicals, mirrors, FDW, validators, manifests,
and the observability evidence trail. It instantiates the Quality
Fabric's `compose()` rule for the **data axis** specifically, in the
same way [`UAT_DISCIPLINE.md`](../../../People/canonicals/UAT_DISCIPLINE.md)
instantiates it for verification and
[`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md)
for multi-wave integrity.

The discipline is owned by **Data Governance Lead** (primary) with
**System Owner** and **DevOPS** as co-owners — **execution stays in Tech**
(validators, migrations, mirror jobs). It applies to every canonical CSV
mint, every mirror upsert, every FDW server addition, every Pydantic SSOT
extension, and every release-gate run.

## 2. The 7 data quality dimensions

| Dim | Quality property | Measurement | Drift signal |
|:---|:---|:---|:---|
| **DATA-01** FK integrity | Every FK column resolves into its registry | `validate_hlk.py` FK pass count vs registered FK count | Pydantic FK-violation in validator output |
| **DATA-02** Mirror parity | Canonical CSV row count = Supabase mirror row count | `compliance_mirror_emit --dry-run` diff with mirror SELECT count | Diff > 0 rows in either direction |
| **DATA-03** FDW health | External-API foreign servers (`stripe_gtm`, etc.) return live data | `SELECT count(*) FROM stripe_gtm.customers` succeeds | Connection error or empty when external account active |
| **DATA-04** Pipeline freshness | Last sync timestamp within freshness threshold | `holistika_ops.sync_log.last_synced_at` vs `now() - threshold` | `now() - last_synced_at > 24h` for daily; analogous for other cadences |
| **DATA-05** Schema drift | Pydantic SSOT field names = CSV header = mirror column names | Compare `akos/hlk_<X>_csv.py` `FIELDNAMES` tuple vs CSV header row vs mirror DDL | Any column rename or addition without coordinated update across 3 surfaces |
| **DATA-06** Lineage | Every mirror has explicit canonical SSOT FK; every derived view has explicit source FK | `PRECEDENCE.md` audit + manifest `paths.*` slot completeness | Mirror without canonical parent; derived view without source citation |
| **DATA-07** Quality metrics | Completeness, accuracy, consistency, timeliness, uniqueness, validity per DAMA-DMBOK 2.0 | Per-dimension validator output + sample audit | Failure on any of the 6 DAMA quality dimensions on any canonical CSV |

These 7 dimensions are **mandatory** at every wave-close that touches
canonical CSVs (per `akos-inter-wave-regression.mdc` RULE 1 inheritance
+ this discipline's RULE 1).

## 3. The compose_DATAOPS rule

```
compose_DATAOPS(audience, channel, scenario, brand, governance, *, data_surface)
  → data_quality_bar
```

Where `data_surface` is one of: `canonical_csv` / `mirror_table` /
`fdw_projection` / `manifest_md` / `pydantic_ssot` / `observability_evidence`.

The bar derives multiplicatively from the 5 fabric axes + the 7
discipline dimensions:

- **audience axis** → which dimensions are operator-visible vs
  agent-only (e.g., J-OP gets DATA-02 + DATA-04 + DATA-06 surfaced
  in dashboards; J-AIC gets all 7 surfaced in agent context).
- **channel axis** → where the quality signal is emitted (operator
  inbox / ERP panel / Sentry alert / release-gate output).
- **scenario axis** → which dimensions tighten for the scenario class
  (e.g., engagement-handoff dossier tightens DATA-06 lineage to
  per-counterparty audit trail).
- **brand axis** → consistency with brand-voice-canonized SSOT
  vocabulary (CORPINT vs translated; per
  `akos-brand-baseline-reality.mdc`).
- **governance axis** → which decisions/runbooks/cursor-rules cover
  the surface (e.g., `validate_hlk.py` + `compliance_mirror_emit`
  + `release-gate.py`).

The discipline does NOT prescribe a fixed pass threshold across all 7
dimensions; it prescribes the **derivation rule**. Threshold tightening
happens at promotion (`charter → active`).

## 4. Cadence

This discipline fires:

1. **At every canonical CSV mint** (per
   `akos-holistika-operations.mdc` §"New git-canonical compliance
   registers") — DATA-01 (FK), DATA-05 (schema drift), DATA-07 (DAMA
   quality metrics) are exercised pre-commit via `validate_hlk.py`.
2. **At every mirror upsert** — **emit** via `scripts/sync_compliance_mirrors_from_csv.py`
   or `py scripts/verify.py compliance_mirror_emit`; **apply** via
   [`docs/guides/holistika-mirror-dml-apply.md`](../../../../../../../docs/guides/holistika-mirror-dml-apply.md)
   (preferred: `scripts/apply_mirror_batches.ps1` → linked `supabase db query --linked -f`;
   **psql** valid alternative; **D-GTM-DB-6**). DATA-02 (parity) + DATA-04 (freshness)
   are exercised after apply.
3. **At every FDW server addition or external-API change** — DATA-03
   (health) is exercised; operator gates per `akos-holistika-operations.mdc`
   §"Operator SQL gate".
4. **At every wave-close** (per `akos-inter-wave-regression.mdc`
   RULE 1) — DIM-12 (canonical-CSV mirror parity in the inter-wave
   regression sweep) is exercised as the discipline's regression-class
   probe.
5. **At every Supabase advisor invocation** (`get_advisors security`) —
   DATA-06 (lineage) + DATA-07 (DAMA validity) catch RLS gaps and
   PostgREST exposure issues.

Post-promotion (**D-IH-90-AA**), mechanical enforcement via release-gate +
pre-commit profile.

## 5. Integration with sister disciplines

DataOps shares quality-bar territory with multiple sister disciplines;
the integration contract names what each owns:

- **[`UAT_DISCIPLINE.md`](../../../People/canonicals/UAT_DISCIPLINE.md)** —
  regression-class mechanical evidence; DataOps composes which validators
  fire per surface.
- **[`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md)** —
  DIM-12 mirror parity probe; DataOps defines the check.
- **[`TECHOPS_DISCIPLINE.md`](../../../People/canonicals/TECHOPS_DISCIPLINE.md)** —
  observability infrastructure; DataOps interprets data-quality signal.
- **`akos-holistika-operations.mdc`** — Supabase two-plane governance.

## 6. Cross-references

- Area charter: [`DATA_AREA_CHARTER.md`](../../canonicals/DATA_AREA_CHARTER.md).
- Quality Fabric parent: [`HOLISTIKA_QUALITY_FABRIC.md`](../../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md)
  §6 specialty row (this canonical materialises `compose_DATAOPS`).
- Paired SOP: [`SOP-TECH_DATAOPS_QUALITY_001.md`](SOP-TECH_DATAOPS_QUALITY_001.md).
- Paired cursor rule: [`.cursor/rules/akos-dataops-discipline.mdc`](../../../../../../../.cursor/rules/akos-dataops-discipline.mdc).
- Validator infrastructure: [`scripts/validate_hlk.py`](../../../../../../../scripts/validate_hlk.py),
  [`scripts/dataops_quality_check.py`](../../../../../../../scripts/dataops_quality_check.py).
- Decisions: **D-IH-86-BV**, **D-IH-90-AA**, **D-IH-93-C**, **D-IH-93-H**.

@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md
