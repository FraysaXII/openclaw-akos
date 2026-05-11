---
language: en
status: active
phase: P13.0
phase_kind: synthesis-checkpoint
parent_initiative: workspace-blueprint-2026
related_initiative_intelligence: 2026-05-10-suez-webuy-procure-to-pay
authored: 2026-05-11
role_owner: PMO
ssot: false
companion_to:
  - ../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  - ../README.md
---

# P13.0 — Canonical dig synthesis (read-only)

> Read-only synthesis checkpoint for P13 workspace-blueprint initiative. No CSV mutation; no folder mutation. The findings here drive P13.1 (canonical blueprint authoring), P13.2 (enum reconciliation pause), P13.3 (engagement templates), P13.4 (CSV tranche pause), P13.5 (cross-link sweep + Projects/ retirement), and P13.6 (closure).

## 1. Why this dig

The SUEZ WeBuy engagement (I12) was the first real customer-engagement folder. Its shape was invented inline (`00-internal/ + 01-operator-pack/ + 02-customer-pack/ + _external_marks/ + _archive/ + _exports/`) and worked, but two things have surfaced since:

1. The next two engagement candidates (sister's hospitality SME advisory; founder-incorporation legal advisers) do not cleanly fit the SUEZ shape — one is a related-party outbound; the other is an *inbound* engagement where Holistika is the customer, not the provider.
2. The GOI/POI class enum has drifted (`collaborator` vs `partner`; the related-party pattern has no flag); the trainee role has no canonical home in `baseline_organisation.csv`; and the role-owner canonical vs `compliance/`-mirror split reads as duplicated rather than as a deliberate canonical-plus-tightened-mirror pair.

P13 lands the blueprint, the two operator-gated CSV tranches, the inbound + outbound templates, and the cross-link sweep — in seven small bisectable commits.

## 2. Ontology summary (drives blueprint §3 / §4)

### Five engagement types, two physical roots, three semantic directions

| # | Type | Semantic direction | Folder home | Counterparty class (GOI/POI) |
|:---|:---|:---|:---|:---|
| 1 | Customer engagement | Outbound (external) | `Think Big/Clients/<YYYY>-<slug>/` | `client_org` |
| 2 | Partner collaboration | Outbound (external, mutual) | `Think Big/Clients/<YYYY>-<slug>/` | `partner` |
| 3 | Product engagement | Outbound (external; SaaS shape) | `Think Big/Clients/<YYYY>-<slug>/` | `client_org` |
| 4 | Adviser engagement | Inbound | `Think Big/Advisers/<YYYY>-<slug>/` | `external_adviser` / `banking_channel` / `public_authority` |
| 5 | Internal capacity | Outbound (internal) | `Think Big/Clients/<YYYY>-internal-<slug>/` | optional / sparse |

Load-bearing distinction (D-W13-F + D-W13-I): there are five engagement **types**, but only **two physical roots** under `Think Big/`. Outbound-internal collapses to `Clients/` plus a slug-prefix convention (`internal-<topic>`). The `Think Big/Projects/` tree is **retired**: everything under Think Big is a project-shaped engagement.

### Four persistence channels (drives blueprint §1)

| Channel | Role | Tracks |
|:---|:---|:---|
| **Git** ([`docs/references/hlk/`](../../../../references/hlk/)) | Versioned SSOT | Markdown sources + branded PDFs (per `_exports/` policy reversal 2026-05-11) + canonical CSVs |
| **Google Drive** | Passive folder-sync mirror | PDFs viewable directly by non-technical readers |
| **SQL mirror** ([`supabase/migrations/`](../../../../../supabase/migrations/)) | `governance.*` views over canonical CSVs | Future `governance.engagement_registry` reserved as SQL projection target |
| **HLK-ERP incremental** | Operator panels reading the SQL mirror | Future `/governance/engagements` panel reserved (out of scope for P13) |

### Three sub-mark functional roles (drives blueprint §2)

| Sub-mark | Function | Engagement role |
|:---|:---|:---|
| **Holistika** (umbrella + R&S) | Canon, intel, SOPs, capabilities for the whole company | Vertical provider — NOT itself an engagement counterparty |
| **HLK Tech Lab** | Tech for everyone (internal + external) | Tech delivery layer — powers product + internal tooling |
| **Think Big** | Engagement projects (outbound + inbound) | Engagement arm — the only sub-mark with engagement folder roots |

Once doctrine: Think Big is unambiguously *the* engagement arm; Holistika and HLK Tech Lab are vertical providers feeding into Think Big folders. The previous `Think Big/Projects/` tree is removed entirely — its placeholder `.gitkeep` is deleted in P13.5.

## 3. GOI/POI gap analysis

[`docs/references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv`](../../../../references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv) currently holds **10 data rows** distributed across three engagement clusters:

| Cluster | Rows | Classes used | Engagement direction |
|:---|:---|:---|:---|
| Founder-incorporation (inbound advisers) | 6 (1 GOI + 5 POI) | `external_adviser`, `banking_channel` | Inbound — Holistika is the customer |
| SUEZ WeBuy via EFA partnership | 4 (2 GOI + 2 POI) | `partner`, `client_org` | Outbound external — Holistika provides |

### Gaps surfaced by this dig

1. **No `related_party` flag.** The sister's hospitality-advisory SME (planned `GOI-CUS-ASES-2026`) is an outbound customer engagement *with* a related-party disclosure. The schema has no machine-readable way to express that today. P13.4 adds an optional `related_party` column (`true` / `false` / empty); default empty preserves backwards compatibility.
2. **`collaborator` vs `partner` enum drift.** The validator allows both ([`scripts/validate_goipoi_register.py`](../../../../../scripts/validate_goipoi_register.py) lines 34-52). No row in the current register uses `collaborator`; the EFA pair uses `partner` (correctly, per D-12-7). The two terms encode a real maturity distinction (informal/one-off vs strategic/contractual/co-branded) but the SOP does not yet write down the sharp boundary. P13.2 (operator gate #1) confirms whether to sharpen via SOP edit (Option A, recommended) or collapse.
3. **No GOI row for the sister's SME yet.** Lands in P13.4 (operator gate #2) as `GOI-CUS-ASES-2026` with `class=client_org`, `related_party=true`, `lens=customer_engagement`, `program_id=` empty (no formal program track until engagement starts).

### What is NOT a gap

- Adviser-cluster rows (`external_adviser`, `banking_channel`) are correctly classed; they fall under the new inbound `Think Big/Advisers/` root introduced in P13.3 + P13.5. No row mutation needed.
- Distance-band invariants (I31 P2.2) are all set (`distance_assessed_date` populated; bridge_via FK valid for the N2 SUEZ pair). Untouched by P13.
- Voice-profile columns (I24 P2): SUEZ rows have language preference empty (FR is not yet in the language_preference enum; the rows record this in notes). Untouched by P13.

## 4. process_list engagement coverage

[`docs/references/hlk/compliance/process_list.csv`](../../../../references/hlk/compliance/process_list.csv) contains **4 active `hol_eng_prc_*` engagement-operations rows**, all under `Engagement Operations` workstream (parent `hol_res_prj_engagement_ops_001`):

| Item ID | Title | Role owner | Notes |
|:---|:---|:---|:---|
| `hol_eng_prc_discovery_questionnaire_001` | Discovery questionnaire ops | Holistik Researcher | Per D-IH-66-R; research-led discovery |
| `hol_eng_prc_proposal_001` | Proposal generation | Brand Manager | Brand-derived deliverable |
| `hol_eng_prc_engagement_design_001` | Engagement design (multi-cell) | Holistik Researcher | Multi-cell methodology orchestration |
| `hol_eng_prc_estimation_001` | Engagement estimation discipline | Project Manager | PMO-owned; per SOP-ENG_ESTIMATION_DISCIPLINE_001 |

### Engagement-types matrix coverage

All five engagement types reuse these four processes (the processes are direction-agnostic). No new process row is required for P13. The inbound `Think Big/Advisers/` folders cross-link the *same* `hol_eng_prc_*` rows, plus the existing `hol_peopl_dtp_*` / `thi_legal_dtp_*` / `thi_finan_dtp_*` adviser-cluster rows already used by the founder-incorporation GOI/POI rows.

The internal-program engagement (slug-prefix `internal-`) is also covered: no new process row, just operator discipline at the folder-naming layer.

## 5. Folder-shape inventory

### Existing under `docs/references/hlk/v3.0/Think Big/` (pre-P13)

```
Think Big/
├── README.md                               # describes Clients/ + Projects/ (Projects/ to be retired)
├── Clients/
│   ├── README.md                           # references _engagement-template/ (P13.3 placeholder); references 2026-asesoria-hosteleria/ as P13.4 placeholder
│   ├── .gitkeep
│   └── 2026-suez-webuy/                    # only real engagement; shape invented inline at I12 P12
│       ├── README.md
│       ├── 00-internal/                    # operator-only briefs + objection banks
│       ├── 01-operator-pack/               # proposal + deck + CDC + discovery (operator + EFA)
│       ├── 02-customer-pack/               # customer proposal + deck + tarification
│       ├── _external_marks/                # EFA Académie logo assets
│       ├── _archive/2026-05-10-pre-efa-collab/   # dated pre-co-branding snapshot
│       └── _exports/                       # branded PDFs (tracked per 2026-05-11 .gitignore reversal) + render-manifest.json
└── Projects/
    └── .gitkeep                            # placeholder only; no real content; RETIRED in P13.5
```

### Findings

- **No template skeleton.** Future engagements either copy from SUEZ or invent inline. P13.3 lands two templates (outbound under `Clients/_engagement-template/`; inbound under `Advisers/_engagement-template/`).
- **No `Advisers/` root.** The founder-incorporation advisers have no unified vault entry — they live entirely as cross-links from `Admin/O5-1/People/Compliance/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md` and the GOI/POI register. P13.5 lays the shell `Think Big/Advisers/2026-holistika-incorporation/` as a unified entry point (cross-links only — no canonical content moves).
- **`Projects/` is empty.** Only a `.gitkeep`. Deleted in P13.5 per D-W13-I.
- **Internal-program convention is undocumented.** The slug-prefix `internal-<topic>` (e.g. `2026-internal-trainee-cohort-01/`) is codified in P13.1 blueprint §3/§4 and reinforced in `Clients/README.md`.
- **`_exports/` PDF tracking is in force.** Per the 2026-05-11 `.gitignore` reversal (commit `186b1cc`), PDFs + `render-manifest.json` are tracked; markdown sidecars in `_exports/` stay ignored (drift risk vs canonical sources in `01-operator-pack/` and `02-customer-pack/`).

## 6. Role-owner canonical vs `compliance/` tightened-mirror contract

User-clarified contract (drives blueprint §6):

| Asset class | Home | Authority | Audience |
|:---|:---|:---|:---|
| **Role-owner canonical** (SOPs, topic indexes, narrative SSOTs) | `docs/references/hlk/v3.0/<Area>/<role-folder>/<file>.md` | Authoritative SOURCE — human-readable canonical the role-owner edits | Operators, agents reading prose |
| **`compliance/` tightened mirror** (CSV registers) | `docs/references/hlk/compliance/*.csv` + `dimensions/*.csv` | Tightened MACHINE-READABLE companion — what validators / SQL mirrors / ERP panels consume | Validators, mirrors, downstream tooling |

### Cross-reference invariants

1. **On conflict between SOP prose and CSV row**, the canonical SOP wins (authoritative source); the CSV is corrected to match.
2. **CSV rows reference SOPs via `sop_url` / `linked_canonicals`**; SOPs reference CSV rows via `process_id` / `role_owner` frontmatter.
3. **Future fusion is on the table.** The two-folder split was inherited from earlier methodology where machine-readable and human-readable trees were strictly separated. As tooling matures (Pydantic models, mirror DDL, ERP projections), the two MAY fuse into a single tree where SOPs carry inline structured frontmatter and CSVs become a derived view. **Out of scope for P13** — P13 only DOCUMENTS the contract as-is and reserves the fusion as a future-initiative candidate (R-W13-6).
4. **Role-owner folders become less convoluted.** Once the contract is explicit, the "where does this belong, here or there?" confusion goes away: SOP folder is authoritative narrative; `compliance/` folder is tightened mirror.

## 7. Baseline observations (validators, before P13 changes land)

### `validate_hlk_vault_links.py` — PASS

```
validate_hlk_vault_links: PASS (no broken internal .md links)
```

### `validate_hlk.py` — pre-existing FAIL (NOT caused by P13)

The composite HLK validator reports one pre-existing failure in `INITIATIVE_REGISTRY`:

```
INIT-OPENCLAW_AKOS-68: inception_decision_id 'D-IH-66-AC' not in DECISION_REGISTER.csv
```

Root cause: commit `4fd7369` (I68 Round-2 enrichment, 2026-05-10) populated `inception_decision_id=D-IH-66-AC` for `INIT-OPENCLAW_AKOS-68`, but the highest `D-IH-66-*` row in `DECISION_REGISTER.csv` is `D-IH-66-T`. This is a typo or a never-registered decision from I68 housekeeping, not a P13 artifact.

**P13 does not touch `INITIATIVE_REGISTRY.csv`** — every P13 commit will inherit this failure when running `validate_hlk.py`. Two options for the operator:

| Option | Action | Trade-off |
|:---|:---|:---|
| **A (recommended)** | Patch the row in a separate hygiene commit before P13.4 (the first P13 phase that mutates compliance CSVs) — set `inception_decision_id=D-IH-66-T` or blank | One-line cleanup; keeps verification matrix green for the rest of P13 |
| B | Leave as-is; accept the pre-existing FAIL across all P13 commits; document in P13.6 closure for separate follow-up | No code change; clean P13 scope; technical-debt carryover |

Recommendation: option A (one-line fix in a dedicated `chore(hlk): fix INIT-OPENCLAW_AKOS-68 inception_decision_id reference` commit ahead of P13.4). Out of P13 scope strictly, but a five-second cleanup that unblocks the canonical verification matrix for the rest of the initiative. Operator decides at P13.4 gate.

### Other validators not run in P13.0

- `validate_hlk_km_manifests.py` — not in scope; no KM manifests change.
- `validate_goipoi_register.py` — exercised by P13.4; expected to PASS for current 10 rows.
- `compliance_mirror_emit` — exercised by P13.4 after DDL migration lands.

## 8. Recommendations (preview of P13.1 — P13.6 commitments)

### Canonical asset to create in P13.1

[`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/) — ten sections; encodes D-W13-A/B/F/G/H/I.

### Operator gates

- **P13.2** (gate #1) — `collaborator` vs `partner` enum. Recommendation A: keep both; sharpen definitions in SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001 §"Class enum maturity ramp". No CSV mutation.
- **P13.4** (gate #2) — combined canonical-CSV tranche: (a) Asesoría placement via `related_party` column + `GOI-CUS-ASES-2026` row; (b) trainee placement via new `Holistik Researcher Trainee` baseline row. Both lands at one operator confirmation. Includes mirror DDL migration.

### Folder-shape commitments

- **P13.3** (outbound + inbound templates) — two parallel literal-copy-target templates at `Clients/_engagement-template/` and `Advisers/_engagement-template/`. No scaffolding script in scope.
- **P13.5** — new `Think Big/Advisers/README.md`; new `Think Big/Advisers/2026-holistika-incorporation/` shell (cross-links only); **delete** `Think Big/Projects/` per D-W13-I; update Think Big root README, `v3.0/index.md`, PMO hub, candidate engagements file.

### Closure

- **P13.6** — `p13-closure-2026-05-11.md` checkpoint + consolidated CHANGELOG row + drop `_savepoint_phase_walk_2026-05-10` branch.

## 9. Decisions encoded by this dig (preview)

| ID | Decision | Confirmed by |
|:---|:---|:---|
| D-W13-A | Five engagement types | This dig §2 |
| D-W13-B | Blueprint canonical lives at `Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md` | This dig §8 |
| D-W13-C | Keep both `collaborator` + `partner`; sharpen via SOP maturity ramp | P13.2 (operator gate) |
| D-W13-D | Sister-business via `client_org` + `related_party=true` | P13.4 (operator gate) |
| D-W13-E | Trainee via new `Holistik Researcher Trainee` baseline row | P13.4 (operator gate) |
| D-W13-F | Five types; two physical roots (`Clients/` + `Advisers/`); three semantic directions | This dig §2 |
| D-W13-G | Role-owner canonical wins on conflict; mirror is the tightened companion; fusion deferred | This dig §6 |
| D-W13-H | Holistika provides canon/intel/SOPs/capabilities; HLK Tech Lab provides tech; Think Big is the engagement arm | This dig §2 |
| D-W13-I | Retire `Think Big/Projects/` — everything at Think Big is a project | This dig §2 |

## 10. Cross-references

- Plan: [`p13_workspace_blueprint_2e0b0c57.plan.md`](../../../../../.cursor/plans/) (Cursor plan; not vault-tracked)
- Predecessor checkpoint: [`p12-closing-2026-05-10.md`](p12-closing-2026-05-10.md) — closes the SUEZ I12 work that surfaced the blueprint need
- Brand architecture context: [`BRAND_ARCHITECTURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md) — sub-mark functional split derives from this canonical
- Co-branding pattern: [`BRAND_COBRANDING_PATTERN.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md) — host/guest semantics inform partner-class definition
- PMO hub: [`TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) — engagement portfolio canonical; P13.5 cross-link sweep target
- Precedence: [`PRECEDENCE.md`](../../../../references/hlk/compliance/PRECEDENCE.md) — canonical-vs-mirror contract authority

End of P13.0 synthesis.
