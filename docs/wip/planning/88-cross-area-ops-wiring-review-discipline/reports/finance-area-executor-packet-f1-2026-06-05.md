---
packet_id: FINANCE-F1-2026-06-05
initiative_id: INIT-OPENCLAW_AKOS-88
program: FINANCE-AREA-FULL
phase: F1
seat: execution
model_pin: composer-2.5
tranche_class: internal_governance
operator_gates:
  - process_list.csv
  - CANONICAL_REGISTRY.csv
prerequisites:
  - reports/research-finance-full-governed-area-2026-06-05/master-synthesis.md
  - reports/finance-area-f1-tranche-charter.md
  - synthesis_before_tranche_check.py PASS on tranche charter
paired_workflow: finance-area-two-seat-workflow-2026-06-05.md
authored: 2026-06-05
author_seat: thinking
status: ready_for_composer
---

# F1 executor packet — Finance area shell (Composer 2.5)

> **Functional name:** the bounded execution brief that turns the Finance full-area
> programme from research into vault artefacts — without the execution model
> re-deciding scope, doctrine, or operator gates.
>
> **Binding rule:** Change **only** what §3 lists. On validator FAIL, ambiguity, or
> missing operator approval for a gated CSV → stop per
> [`.cursor/agents/executor.md`](../../../../.cursor/agents/executor.md).

---

## 0. F0 assumptions locked for this packet (operator ratified 2026-06-05)

F0 AskQuestion was deferred; the operator instructed **full F1 execution**. Lock these
until a formal `DECISION_REGISTER` row is minted at F0 closure:

| # | Decision | Locked value | Functional meaning |
|:---:|:---|:---|:---|
| A | Programme scope | **FINANCE-AREA-FULL F0–F4** | Finance becomes second full governed area after Data (I93), Volvo operational bar |
| B | FINOPS CSV SSOT home | **`People/Compliance/canonicals/finops/`** unchanged | Git CSVs + Pydantic validators stay in Compliance; Finance owns **doctrine** |
| C | FINOPS doctrine home | **`Finance/Governance/canonicals/FINOPS_DISCIPLINE.md`** | Mirror of Data/DataOps split (D-IH-93-C pattern) |
| D | Area charter home | **`Finance/canonicals/FINANCE_AREA_CHARTER.md`** | Seven-section charter; `inherited_pattern_id=pattern_area_buildout` |
| E | M2 counterparty ops threshold | **Document in charter §6; probe at F3** | Do not invent production monetary facts in F1 |
| F | I88 P1 sweep | **Spine evidence only** | Superseded for area bar by this programme |
| G | I88 P3 canonical | **After F4 + P2** | Do not mint `CROSS_AREA_OPS_WIRING_DISCIPLINE` in F1 |

**Escalate (stop)** if vault evidence contradicts A–G.

---

## 1. Mission

Create the **Finance area shell** so `validate_area_completeness.py` scores Finance
**≥65%** and clears gaps **AREA-02** (charter), **AREA-03** (discipline), **AREA-13**
(README), **AREA-12** (Quality Fabric cross-ref), **AREA-14** (pattern on umbrellas).

**Not in F1:** pricing/tax registries, data contracts, CONF seeds, mirrors, cursor
rule/skill, live `registered_fact`, I88 P3 canonical.

---

## 2. In scope / out of scope

| In | Out |
|:---|:---|
| Folder + README + charter + FINOPS discipline (status `charter`) | F2 CSV dimension registries |
| `process_list` +1 row; pattern on 5 umbrella `item_id`s | `runbook_path` backfill on 16 processes (F2) |
| `CANONICAL_REGISTRY` +2 rows | `baseline_organisation.csv` |
| QF §6 forward row `compose_FINOPS` | `akos-finance-ops.mdc` (F3) |
| Evidence base sections (≥3 internal + ≥2 external per canonical) | Supabase DML |
| Planning evidence stub (optional, ≤30 lines) | DECISION_REGISTER row (F0 chore) |

---

## 3. Files to create / edit (strict order)

| # | Action | Path |
|:---:|:---|:---|
| 1 | CREATE dirs | `docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/` |
| 2 | CREATE | `docs/references/hlk/v3.0/Admin/O5-1/Finance/README.md` |
| 3 | CREATE | `docs/references/hlk/v3.0/Admin/O5-1/Finance/canonicals/FINANCE_AREA_CHARTER.md` |
| 4 | CREATE | `docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/FINOPS_DISCIPLINE.md` |
| 5 | EDIT | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv` |
| 6 | EDIT | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv` |
| 7 | EDIT | `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md` (§6 table only) |
| 8 | EDIT | `docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-buildout-roadmap.md` (F1 status + links) |
| 9 | CREATE (optional) | `docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-f1-execution-evidence-2026-06-05.md` |

**Do not edit** `PRECEDENCE.md`, `KNOWLEDGE_PAIRING_REGISTRY.csv`, or Compliance `finops/*.csv` in F1.

---

## 4. Canonical specs

### 4.1 `Finance/README.md` (AREA-13)

Mirror [`Data/README.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/README.md) structure:

- Title: `# Finance area — v3.0 vault index`
- Link charter: `canonicals/FINANCE_AREA_CHARTER.md`
- Sub-domains table:

| Sub-domain | Path | Purpose |
|:---|:---|:---|
| **Governance** | `Governance/canonicals/` | FINOPS discipline, future rev-rec / tax policy (F2+) |
| **Business Controller** | `Business Controller/` | Existing SOPs (counterparty maintenance, etc.) |

- Key canonicals table (charter + FINOPS discipline paths)
- Note: Compliance SSOT for `FINOPS_*` CSVs under `People/Compliance/canonicals/finops/`
- Verification block:

```powershell
py scripts/validate_area_completeness.py --matrix
py scripts/validate_hlk.py
py scripts/validate_finops_ledger.py --self-test
```

### 4.2 `FINANCE_AREA_CHARTER.md` (AREA-02)

**Frontmatter** (match DATA charter keys):

```yaml
language: en
status: charter
canonical: true
role_owner: CFO + Business Controller
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-06-05
last_review: 2026-06-05
last_review_at: 2026-06-05
last_review_by: Business Controller
last_review_decision_id: D-IH-88-A
methodology_version_at_review: v3.1
inherited_pattern_id: pattern_area_buildout
ratifying_decisions:
  - D-IH-88-A
  - D-IH-93-B
linked_canonicals:
  - ../Governance/canonicals/FINOPS_DISCIPLINE.md
  - ../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
  - ../../../People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv
  - ../../../Data/Governance/canonicals/DATA_CONTRACT_STANDARD.md
companion_to:
  - ../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
```

**Seven sections (required prose):**

#### §1 Mission

Finance owns **operational finance truth** at the Volvo bar: semantic counterparty
MDM, governed monetary facts, and cross-area contracts so Marketing, RevOps, Legal,
People, and Data consume the same IDs and metric definitions. Finance **governs**
FINOPS planes; it does not own every area's campaign copy or legal instruments.

#### §2 Roles + sub-domains

| Role | Entity | Notes |
|:---|:---|:---|
| **CFO** | Think Big | Area head; entity gate partner (`thi_finan_dtp_306`) |
| **Business Controller** | Think Big | Register stewardship, data-contract co-owner |
| **PMO** | Holistika | Process-cost mapping (`thi_finan_dtp_273`) |
| **RevOps Manager** | HLK Tech Lab | Engagement revenue chain consumer |

Sub-domains: **Governance** (`Finance/Governance/`), **Business Controller** (existing role tree).

#### §3 Boundary

| Finance owns | Finance does not own |
|:---|:---|
| FINOPS discipline, counterparty golden record, rev-rec **policy** (F2), pricing/tax **registries** (F2) | Marketing campaign creative, Legal contract text, Data global contract **standard** |
| Five FINOPS planes (doctrine names them; F2+ populates) | Full ERP replacement |
| Cross-area DC-* **consumer** obligations | Supabase DDL (Tech/System Owner executes) |

**Internal-first (D-IH-81-P):** roles may be AIC-absorbed until humans hired; gates
remain in SOPs.

#### §4 Five FINOPS planes (I81 model)

| Plane | Name | F1 status | F-phase |
|:---:|:---|:---|:---|
| 1 | Counterparty / party MDM | **Live** (register + mirror + Stripe) | F1 charter declares |
| 2 | Revenue recognition + pricing SSOT | schema/doctrine partial | F2 |
| 3 | Tax + statutory calendar | counsel-held | F2 |
| 4 | O2C / cash / AR | org-planned | F2–F4 |
| 5 | PTP / capex / spend | org-planned | F2–F4 |

#### §5 Process catalog (initial)

List umbrella processes (names + `item_id` only — full pairing at F2):

| Process | `item_id` |
|:---|:---|
| Think Big Finance Architecture (project) | `thi_finan_prj_1` |
| Financial Forecast (workstream) | `thi_finan_ws_1` |
| Revenue Operations (workstream) | `thi_finan_ws_2` |
| Founder Capital Governance (workstream) | `thi_finan_ws_3` |
| FINOPS and counterparty economics (workstream) | `thi_finan_ws_4` |
| Finance area buildout completeness sweep | `hol_finan_dtp_area_buildout_001` |
| FINOPS counterparty register maintenance | `thi_finan_dtp_303` |

#### §6 Activation cadence

- **F1 (this packet):** shell + discipline at `charter` status; matrix ≥65%.
- **F2:** registries + DC-* + CONF seeds + rev-rec policy.
- **F3:** mirror evidence + finance cursor rule + first recon / fact or documented SKIP.
- **F4:** matrix 88% / 0 gaps + closure UAT + I88 P1b re-grade.

**M1–M5 gates** (falsifiable): copy table from
[`master-synthesis.md`](research-finance-full-governed-area-2026-06-05/master-synthesis.md)
§ "Closure gates".

#### §7 Cross-references

I88 roadmap, I93 area meta-process, research pack, traceability inventory, F1 packet.

#### Evidence base (§8 or appendix — required)

≥3 internal paths + ≥2 external citations, e.g.:

- Internal: `DATA_AREA_CHARTER.md`, `AREA_GOVERNANCE_DISCIPLINE.md`, `thi_finan_dtp_303` SOP, research master synthesis
- External: DAMA MDM, R2R maturity (cite IDs from source-ledger-v2)

### 4.3 `FINOPS_DISCIPLINE.md` (AREA-03, AREA-12)

**Frontmatter:** `status: charter`; `role_owner: Business Controller`; link charter,
counterparty SOP, `validate_finops_ledger.py`, DATA contract standard, AREA_GOVERNANCE.

**Sections (mirror DATAOPS shape, FINOPS content):**

1. **Purpose** — dual-plane FINOPS (Compliance CSV SSOT + Supabase mirrors +
   `holistika_ops` Stripe links). Prevents counterparty drift and orphan monetary facts.
2. **Five FINOPS quality dimensions** (name FIN-* codes, map to DATA-01..07 where applicable):

| Dim | Property | Measurement | Drift signal |
|:---:|:---|:---|:---|
| FIN-01 | Register integrity | `validate_finops_ledger.py` | CSV/schema FAIL |
| FIN-02 | Mirror parity | DATA-02 probe (F3) | Row count mismatch |
| FIN-03 | Join spine | `finops_counterparty_id` on Stripe/customer links | Orphan payments |
| FIN-04 | Entity gate | `thi_finan_dtp_306` before production amounts | Facts without entity |
| FIN-05 | Cross-area contract | DC-* rows (F2) | Ad-hoc finance bridges |

3. **Plane ownership table** — same five planes as charter §4 with steward roles.
4. **compose_FINOPS** — forward declare Quality Fabric specialty (active at F3/F4).
5. **Cadence** — event_triggered at CSV mint; monthly recon (F3); annual rationalization (`thi_finan_dtp_307`).
6. **Cross-references** — do not duplicate Compliance CSV column specs (link SOP maintenance).

**Evidence base:** same bar as charter (≥3 internal + ≥2 external).

### 4.4 `HOLISTIKA_QUALITY_FABRIC.md` §6 row (AREA-12)

Add one table row after DATAOPS row pattern:

| Specialty | Canonical path | Status | compose() |
|:---|:---|:---|:---|
| **FINOPS (counterparty / monetary facts / FINOPS mirror spine)** | `Finance/Governance/canonicals/FINOPS_DISCIPLINE.md` | **charter** (F1); promote **active** at F4 | `compose_FINOPS(audience, channel, scenario, brand, governance) → FIN-01..05 bar` |

Do **not** bump specialty count enum in prose unless validator requires — forward reference only.

---

## 5. Canonical CSV edits

### 5.1 `process_list.csv` — ADD one row

Append **one** row (adjust only if column count differs — verify header row 1):

```csv
Internal,Employee,Think Big,Finance,CFO,Business Controller,Think Big Finance Architecture,thi_finan_prj_1,FINOPS and counterparty economics,thi_finan_ws_4,Finance area buildout completeness sweep,hol_finan_dtp_area_buildout_001,process,4,2,8,Run the 14-component area-completeness matrix for Finance at charter mint OR CSV tranche per AREA_GOVERNANCE_DISCIPLINE (People meta-process D-IH-93-B). Second worked example after Data I93 P1. compose_AREA probes AREA-01..AREA-14; conservative skip AREA-10 mirrors until F3.,docs/references/hlk/v3.0/Admin/O5-1/Finance/canonicals/FINANCE_AREA_CHARTER.md,Paired runbook: scripts/validate_area_completeness.py (--matrix --strict). Cursor rule: .cursor/rules/akos-area-governance.mdc. Skill: .cursor/skills/area-governance-craft/SKILL.md. AC-HUMAN: CFO or Business Controller walks AREA_GOVERNANCE_DISCIPLINE section 2 (30-45 min). AC-AUTOMATION: --self-test at pre_commit.,Safe,finance-area-charter-or-csv-tranche,event_triggered,Per AREA_GOVERNANCE SOP; Finance matrix ≥65% at F1 commit.,2026-06-05,Business Controller,D-IH-88-A,v3.1,,,,event_triggered,,,,pattern_area_buildout
```

### 5.2 `process_list.csv` — SET `inherited_pattern_id`

On **existing rows only**, set last column to `pattern_area_buildout` (leave other
columns unchanged):

| `item_id` | `item_granularity` |
|:---|:---|
| `thi_finan_prj_1` | project |
| `thi_finan_ws_1` | workstream |
| `thi_finan_ws_2` | workstream |
| `thi_finan_ws_3` | workstream |
| `thi_finan_ws_4` | workstream |

**Do not** mass-update every `thi_finan_dtp_*` in F1 — F2 pairs runbooks.

### 5.3 `CANONICAL_REGISTRY.csv` — ADD two rows

| canonical_id | title | owning_area | role_owner | path | format | … | status | notes |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `finance_area_charter` | Finance Area Charter | Finance | CFO | `docs/references/hlk/v3.0/Admin/O5-1/Finance/canonicals/FINANCE_AREA_CHARTER.md` | md | … | charter | F1 second `pattern_area_buildout` example |
| `finops_discipline` | FINOPS Discipline | Finance | Business Controller | `docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/FINOPS_DISCIPLINE.md` | md | … | charter | FIN-* dimensions; CSV SSOT stays Compliance/finops |

Copy column set from `data_area_charter` row (line ~140); fill empty cells consistently.

---

## 6. Verification matrix (run in order; all must PASS)

```powershell
# 0. Tranche synthesis (should already PASS from thinking seat)
py scripts/synthesis_before_tranche_check.py --check-charter docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-f1-tranche-charter.md

# 1. HLK validators
py scripts/validate_hlk.py

# 2. Area matrix — capture Finance line to evidence file
py scripts/validate_area_completeness.py --matrix

# 3. FINOPS chassis unchanged
py scripts/validate_finops_ledger.py --self-test

# 4. Pre-commit profile
py scripts/verify.py pre_commit
```

**F1 acceptance thresholds:**

| Check | Pass criterion |
|:---|:---|
| Finance matrix score | **≥65%** (target **≥70%** if AREA-12 moves partial→pass) |
| AREA-02, AREA-03, AREA-13 | **gap → pass** |
| AREA-14 | **partial → pass** (umbrella pattern wired) |
| `validate_hlk.py` | exit 0 |
| No broken `linked_canonicals` | manual grep charter ↔ discipline paths |

---

## 7. Acceptance criteria (checkboxes for operator)

- [ ] `Finance/README.md` resolves from vault index
- [ ] `FINANCE_AREA_CHARTER.md` has 7 sections + evidence base + frontmatter `pattern_area_buildout`
- [ ] `FINOPS_DISCIPLINE.md` has FIN-01..05 + five planes + evidence base
- [ ] `hol_finan_dtp_area_buildout_001` row present; 5 umbrellas carry `pattern_area_buildout`
- [ ] `CANONICAL_REGISTRY` contains `finance_area_charter` + `finops_discipline`
- [ ] QF §6 cites FINOPS discipline at `charter`
- [ ] Matrix Finance ≥65%; AREA-02/03/13 gaps cleared
- [ ] Single commit; no secrets; no mirror SQL

---

## 8. Stop conditions

| Trigger | Executor action |
|:---|:---|
| `validate_hlk.py` FAIL on `process_list` | Stop — do not partial-commit CSV |
| Finance matrix &lt;65% after mint | Stop — list remaining AREA-* codes |
| Operator gate not confirmed for CSV | Stop — emit `=== COMPOSER BLOCKED -> SWITCH TO OPUS ===` |
| Need new decision ID / scope change | Stop — thinking seat authors AskQuestion |
| Temptation to add F2 registry CSV | Stop — out of scope |

---

## 9. Commit

```
feat(i88-finance-f1): Finance area shell — charter, FINOPS discipline, pattern_area_buildout
```

One commit only. Update `files-modified.csv` in I88 folder if that initiative tracks tranches.

---

## 10. Composer thread bootstrap (paste below into Holistika — Execute mode)

```text
=== OPUS DONE -> SWITCH TO COMPOSER ===

You are the execution seat. Model must be composer-2.5.
Execute packet: docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-executor-packet-f1-2026-06-05.md
Tranche charter: docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-f1-tranche-charter.md
Operator approved canonical-CSV gate for process_list + CANONICAL_REGISTRY in this tranche.

Return: files changed, commands + exit codes, Finance matrix line before/after, open questions.
On FAIL: === COMPOSER BLOCKED -> SWITCH TO OPUS ===
On PASS: === COMPOSER DONE — operator review ===
```

---

## 11. Next packets

| Phase | Packet (stub until authored) |
|:---|:---|
| F2a | `finance-area-executor-packet-f2a-revrec-pricing-2026-06-05.md` — DC rows + CONF + rev-rec |
| F2b | `finance-area-executor-packet-f2b-tax-calendar-2026-06-05.md` — tax registry + OPS-81-13 |
| F3 | `finance-area-executor-packet-f3-tech-plane-2026-06-05.md` — mirrors + cursor rule |
| F4 | `finance-area-executor-packet-f4-closure-2026-06-05.md` — UAT + matrix 88% |

Workflow SSOT: [`finance-area-two-seat-workflow-2026-06-05.md`](finance-area-two-seat-workflow-2026-06-05.md).
