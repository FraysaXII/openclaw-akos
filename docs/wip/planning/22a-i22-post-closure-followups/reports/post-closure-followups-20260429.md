# I22 post-closure follow-ups + Wave-2 bootstrap (2026-04-29)

Status of the five items captured in [`master-roadmap.md`](../master-roadmap.md). I22 stays **CLOSED**; this is a fresh slot, not a reopening.

## Results table

| # | Item | Result | Owner | Evidence |
|:-:|:-----|:-------|:-----:|:---------|
| 1 | `supabase migration list` parity check | **PENDING (operator)** — run from operator CLI; paste one-line result into §1 below | Operator | §1 — empty until run |
| 2 | `mmdc` install (`@mermaid-js/mermaid-cli@^11`) | **PENDING (operator)** — `npm i -g @mermaid-js/mermaid-cli@^11` then `mmdc --version` ≥ 11.x | Operator | §2 — empty until installed |
| 3 | FINOPS / TECHOPS second-CSV assessment | **PASS** — recommendation **DO NOT ADD**; persistent trigger template scheduled for I26-P0 | Agent | §3 below |
| 4 | Planning README slot 27 reservation | **PASS** — `(reserved)` row added to `docs/wip/planning/README.md` | Agent | §4 below |
| 5 | Operator-answers YAML + scaffolder bootstrap | **PASS** — `operator-answers-wave2.yaml` pre-filled; `scripts/wave2_backfill.py` runnable; verify profile `wave2_backfill_check` wired | Agent | §5 below |

---

## §1 — `supabase migration list` parity check (PENDING, operator)

Run from operator CLI:

```bash
supabase link --project-ref <ref>   # if not already linked
supabase migration list
```

Paste the one-line result here when run:

```
date: <YYYY-MM-DD>
local: <count>
remote: <count>
match: <true|false>
notes: <e.g. "all i21 mirrors present remote"; or "drift on …">
```

Pass criteria: local and remote counts match (no drift). If they diverge, fix per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate" step 5 (break-glass) before any new wave-2 DDL.

## §2 — `mmdc` install (PENDING, operator)

Pinned install (per Wave-2 plan, I26-P1):

```bash
npm i -g @mermaid-js/mermaid-cli@^11
mmdc --version
where.exe mmdc        # Windows
which mmdc            # Linux/macOS
```

Paste the version string when installed:

```
date: <YYYY-MM-DD>
mmdc_version: <e.g. 11.4.2>
location: <path>
```

Linux CI extras (per Wave-2 plan): `libgbm1`, `fonts-liberation`, `fonts-noto-color-emoji`, `--no-sandbox` may be needed.

## §3 — FINOPS / TECHOPS second-CSV assessment

**Question.** Does FINOPS or TECHOPS need a *second* canonical compliance CSV beyond the existing `FINOPS_COUNTERPARTY_REGISTER.csv` and `COMPONENT_SERVICE_MATRIX.csv`?

**Answer: NO. Recommendation: DO NOT ADD.**

### FINOPS

- **Today owns.** `FINOPS_COUNTERPARTY_REGISTER.csv` (counterparty metadata) + `finops.registered_fact` (operational ledger facts, Initiative 19).
- **Candidate "second register".** `FINOPS_CONTRACT_REGISTER.csv` for SaaS contracts.
- **Why we do not add.** SaaS contract metadata already lives in `stripe_gtm` foreign tables (Stripe is authoritative). A vault row would duplicate Stripe SSOT and violate the "external system is authoritative for FDW reads" rule in [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Schema responsibilities (DAMA)".

### TECHOPS

- **Today owns.** `COMPONENT_SERVICE_MATRIX.csv` (CTO chain SSOT for systems, services, integrations, platforms).
- **Candidate "second register".** `TECHOPS_API_REGISTRY.csv` for API endpoints.
- **Why we do not add.** API metadata already joins through `REPOSITORIES_REGISTRY.md` and the matrix's `api_spec_pointer` column. The `env_tech_ws_api_1` API-lifecycle workstream + `SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md` already govern API lifecycle without a second CSV.

### Re-evaluation triggers (deferred)

Both decisions are reversible. The Wave-2 plan I26-P0 ships a **persistent re-eval-trigger template** at `docs/wip/planning/26-hlk-ops-hardening/reports/re-eval-trigger-finops-techops-second-csv.md` with the explicit conditions:

- **FINOPS reopen** when a third FINOPS use case surfaces beyond counterparty + ledger.
- **TECHOPS reopen** when API metadata cannot be expressed via existing matrix columns + repositories registry.

Until either trigger fires, no second CSV.

## §4 — Planning README slot 27 reservation

Added a `(reserved)` row to [`docs/wip/planning/README.md`](../../README.md) for the deferred `process_list.csv` per-plane re-architecture (Wave-2 plan §"Out of scope (explicit)"). This makes the deferred work an explicit, visible parking row so Wave-2 (initiatives 23-26) lands contiguously.

Numbering after Wave-2:

| Slot | Use |
|:----:|:----|
| 22 | Closed (I22) |
| **22a** | **This folder — post-closure follow-ups + wave-2 bootstrap** |
| 23 | Wave-2: Program Registry |
| 24 | Wave-2: Communication Methodology + Composer |
| 25 | Wave-2: Topic Graph + Graph Projection + KM Scalability |
| 26 | Wave-2: Ops hardening |
| 27 | Reserved — `process_list.csv` per-plane re-architecture (deferred until row count > ~3000 OR plane contention) |

## §5 — Operator-answers YAML + scaffolder bootstrap

The single artifact the rest of Wave-2 depends on. Three files landed:

1. **[`operator-answers-wave2.yaml`](../operator-answers-wave2.yaml)** — single source of operator decisions. Five sections:
   - **Section 1**: Program Registry (12 rows × 4 Tier-3 fields). Agent pre-filled `program_id`, `program_name`, `program_code`, `primary_owner_role`, `default_plane`, `process_item_id`. Operator fills `lifecycle_status`, `risk_class`, `start_date`, `target_close_date`, `consumes_program_ids`, `notes` per row.
   - **Section 2**: Brand voice foundation (operator-authored, ~90 min single sitting). Agent provides structure + inline examples.
   - **Section 3**: GOI/POI voice profiles (6 existing rows × 3 columns). Agent pre-filled defaults from Wave-2 plan D-IH-11; operator confirms or flips.
   - **Section 4**: KiRBe duality confirmations (5 cells, ~10 min).
   - **Section 5**: G-24-3 founder sign-off (only when ready to send the real adviser email).

2. **[`scripts/wave2_backfill.py`](../../../../scripts/wave2_backfill.py)** — single-command scaffolder.
   - `py scripts/wave2_backfill.py --check-only` — sentinel scan; reports pending per section; safe to run anytime.
   - `py scripts/wave2_backfill.py --dry-run` — print would-write diff; no file changes.
   - `py scripts/wave2_backfill.py --section programs` — process one section.
   - `py scripts/wave2_backfill.py` — full write; refuses if any `__OPERATOR_CONFIRM__` remains in a section that has downstream artifacts.

3. **Verify profile `wave2_backfill_check`** in [`config/verification-profiles.json`](../../../../config/verification-profiles.json) — runs `--check-only`. Always green at this stage (sentinels are expected until the operator fills the YAML).

### What the operator does next (3 things, in order)

1. **Run §1 + §2** above (parity check + mmdc install). Paste evidence inline.
2. **Begin filling Section 1 of `operator-answers-wave2.yaml`** — the Program Registry. Recommended batches: founder-cluster (3 rows, ~1h), product-cluster (3 rows, ~1h), internal-cluster (6 rows, ~1h). After each batch, run `py scripts/wave2_backfill.py --check-only --section programs` to see how many sentinels remain.
3. **Confirm pre-execution clearance scope** — review the 6-PR plan in the Wave-2 plan §"Pre-execution clearance" and approve OR propose splits / merges.

## Verification

| Check | Result |
|:------|:------:|
| `validate_hlk.py` | OPERATOR — run before commit |
| `validate_hlk_vault_links.py` | OPERATOR — run before commit |
| `python scripts/wave2_backfill.py --check-only` | informational (sentinels expected; `wave2_backfill_check` profile always green at this stage) |
| `pytest tests/test_wave2_backfill.py -v` | OPERATOR — run before commit |
