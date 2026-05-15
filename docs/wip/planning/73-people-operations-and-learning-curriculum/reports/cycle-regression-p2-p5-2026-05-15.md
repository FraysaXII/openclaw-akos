# I73 cycle regression — P2 through P5 (2026-05-15)

> Evidence artefact for the coordinated P2–P5 strand delivery against Initiative **OPENCLAW_AKOS-73**. Automated gates only — browser / qualitative UAT not in scope for this cycle.

## 1. SSOT map

| Artefact delivered | Upstream SSOT reused (not duplicated) |
|:---|:---|
| Learning charter + curriculum + `LEARNING_OPS_BACKLOG.csv` | [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv); [`ETHICAL_AUTOMATION_POSTURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md); [`PEOPLE_AREA_RESTRUCTURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_AREA_RESTRUCTURE.md); [`access_levels.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md) / [`source_taxonomy.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md) / [`confidence_levels.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md) |
| Engagement lifecycle SOPs + runbooks | [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv); [`ENGAGEMENT_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv); [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md); [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) |
| Historical case-law index | Same engagement-model registry; [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) cited as evidence-only (no verbatim employer/counterparty names in case-law doc) |
| Ethics + Learning quarterly SOP | [`ETHICAL_AUTOMATION_POSTURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) §2.5 + §5; [`LEARNING_CHARTER.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/LEARNING_CHARTER.md) |
| Brand foundation thesis paragraph | [`PEOPLE_AREA_RESTRUCTURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_AREA_RESTRUCTURE.md); [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) dual-register reminder |

## 2. Anti-duplication checklist

| Check | Verdict |
|:---|:---:|
| No second engagement-instance registry (instances remain `ENGAGEMENT_REGISTRY.csv` only) | PASS |
| No duplicate counterparty SSOT (FINOPS register remains sole counterparty metadata canonical) | PASS |
| No parallel KM taxonomy (research info-handling still points at existing `access_levels` / `source_taxonomy` / `confidence_levels`) | PASS |
| Engagement **models** stay in People Operations dimension CSV (not merged into Compliance engagement instances) | PASS |

## 3. `process_list.csv` continuity

- All **`TODO[I73-P2-SOP-PATH]`** and **`TODO[I73-P3-SOP-PATH]`** markers on the I73 engagement rows were cleared at commits **`4a0a7d3`** (P2 apprentice pairing + forward pointers) and **`663442c`** (P3 lifecycle/registry SOP paths + apprentice stub).
- Net-new **`hol_peopl_dtp_316`** (scheduled Ethics + Learning quarterly co-review) lands at commit **`17aa20d`** (P5); intentional scope split from P4 case-law (no process row in P4 commit **`155fa92`**).

## 4. Validator sweep (this cycle)

Commands run on Windows after P5 edits (representative gate set):

| Command | Verdict |
|:---|:---:|
| `py scripts/validate_hlk_language_frontmatter.py` | PASS |
| `py scripts/validate_hlk_vault_links.py` | PASS |
| `py scripts/validate_process_list_pairing.py` | PASS (16 cadence-bound paired rows after `hol_peopl_dtp_316`; includes `role_plain` pairing heuristic fix from P3 commit **`663442c`) |
| `py scripts/validate_hlk.py` | PASS |
| `py scripts/validate_engagement_model_registry.py` | PASS (invoked inside umbrella + standalone during iteration) |
| `py -m pytest tests/test_peopl_engagement_scripts_smoke.py tests/test_check_ethics_learning_review_due_smoke.py -v` | PASS (8 tests) |

**Release-gate (`py scripts/release-gate.py`):** not re-run end-to-end in this worker session; pre-existing FAIL carry-overs called out in [`CHANGELOG.md`](../../../../CHANGELOG.md) (test suite / browser smoke / sibling-repo drift) remain unless operator explicitly clears them.

## 5. Residual risks / next cycle

| Horizon | Notes |
|:---|:---|
| **P6** | Compliance vs Ethics boundary doc + `hol_peopl_*` orphan reassignments — depends on charters now landed at P2/P5. |
| **P7** | KB persona views + ERP routes — engagement-model mirrored posture assumed from registry + mirrors. |
| **P8** | Methodology IP minting path + brand-vs-name matrix (`D-IH-73-F`). |

## 6. Git SHAs (phase commits this session)

| Phase | Short SHA | Message |
|:---|:---|:---|
| P3 | `663442c` | `i73 p3 — engagement lifecycle sops + runbooks` |
| P4 | `155fa92` | `i73 p4 — historical engagement case law` |
| P5 | `17aa20d` | `i73 p5 — ethics+learning quarterly review sop` |

(P2 shipped earlier as `4a0a7d3` per initiative CHANGELOG continuity.)

## 7. Deferred TODOs (explicit)

- **Recruiter onboarding (`IO-REC-PLACEHOLDER-001`)** — closed AskQuestion **2026-05-15**: [`SOP-RECRUITER_ONBOARDING_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/People%20Operations/canonicals/SOP-RECRUITER_ONBOARDING_001.md) + [`scripts/peopl_recruiter_onboarding_checklist_stub.py`](../../../../../scripts/peopl_recruiter_onboarding_checklist_stub.py) + **`process_list.csv`** `tbi_peopl_dtp_recruiter_onboarding_001` (supersedes prior `TODO[I73-SOP-RECRUITER_ONBOARDING_001]` placeholder note).
