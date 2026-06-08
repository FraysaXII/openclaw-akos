---
intellectual_kind: process_list_issue_inventory
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L2 — Capability de-densify (R2-01) — companion process_list data-quality sweep
authored: 2026-06-08
status: proposal
audience: J-OP;J-AIC
register: internal
control_confidence_level: Euclid
related_decisions:
  - D-IH-95-I   # ratified capability-collapse synthesis; §5 names THIS doc as the process_list cleanup scoper
  - D-IH-95-H   # de-densify method (6-step collapse + eviction rule) — reused here for process_list
  - D-IH-82-P   # CAPABILITY_REGISTRY 1:1 process-shadow seed (the shared-row coupling)
  - D-IH-71-CLOSURE   # the bulk seed-mint stamp carried by all 734 flagged rows
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COMPONENT_SERVICE_MATRIX.csv
note: >
  MADEIRA data-quality sweep of process_list.csv (1,207 rows). The capability
  de-densify (D-IH-95-H/-I) proved the CAPABILITY_REGISTRY was a 1:1 shadow of
  process_list; this doc quantifies the SAME pollution in the source register and
  proposes radical-but-governed dispositions. READONLY research + this one doc —
  NO canonical CSV is modified here. Every edit to process_list is the hardest-gated
  canonical change (operator approval + AskQuestion + validate_hlk) per
  akos-baseline-governance.mdc; this doc is the reviewable scope proposal for that gate.
---

# process_list.csv issue inventory + proposed radical cleanup (1,207 → ~473 clean)

> **Headline:** **734 of 1,207 rows (60.8%) are flagged** as data-quality pollution; **~473
> clean, stable, curated processes remain** after a radical cleanup. The pollution is one
> coherent thing: a **bulk Trello / mind-map import** (738 `gtm_*` rows, 571 of them
> task-grain micro-steps, all bilingual ES/EN, all stamped with the **same** seed-mint review
> id `D-IH-71-CLOSURE`, **zero** of them carrying any live engagement / persona / pattern /
> cadence wiring). It is the exact same inflation the capability de-densify found — because
> `CAPABILITY_REGISTRY` was seeded 1:1 off these very rows (D-IH-82-P). The good news for
> cleanup safety: the flagged rows form a **closed parent subtree** and **no active capability
> and no live-system column points at any of them**, so a radical cut orphans almost nothing.

This is a Tier-1 Research-area WIP finding (correct home: `docs/wip/intelligence/`, internal
register permitted). It is the process_list companion to the six capability collapse maps under
[`l2-collapse-maps/`](l2-collapse-maps/) and is explicitly named in the ratified collapse
synthesis [`_SYNTHESIS-2026-06-08.md`](l2-collapse-maps/_SYNTHESIS-2026-06-08.md) §5 (decision
**D-IH-95-I**). It modifies **no** canonical CSV — it is the reviewable scope proposal for the
operator's `process_list` cleanup gate.

## 0. What I scanned (so this is falsifiable + reproducible)

| Evidence read | What it told me |
|:---|:---|
| 6 capability collapse maps (`l2-collapse-maps/*.md`) | The de-densify already surfaced and dispositioned every pollution class at the *capability* layer. This doc consolidates their process-layer findings — it does **not** redo their work. |
| `process_list.csv` (1,207 rows) via `py` one-liners | Granularity: **15 project · 72 workstream · 459 process · 661 task**. Area: Operations 417 · Tech 404 · MKT 127+1 · People 103 · Research 92 · Data 26 · Finance 22 · Legal 15. |
| `CAPABILITY_REGISTRY.csv` (1,119 rows) | `lifecycle_status`: **117 active · 1,001 planned · 1 deprecated**. The 1,119 ≈ the 1,120 `process`+`task` rows: it is the 1:1 shadow (D-IH-82-P). The 87 `project`+`workstream` rows have no shadow. |
| Supabase migrations + `OPS_REGISTER.csv` + repo-wide grep | Mirror table `compliance.process_list_mirror` exists (RLS-denied); flagged ids appear only in the shadow registry, the mirror, historical reports, and two GTM-import scripts. |

Reproducible commands (run from repo root; `PL` = the process_list path):

```powershell
$PL="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
# granularity + area + gtm-family counts
py -c "import csv,collections as C;r=list(csv.DictReader(open(r'$PL',encoding='utf-8')));print(dict(C.Counter(x['item_granularity'] for x in r)));print(dict(C.Counter(x['area'] for x in r)))"
# the 734-row flagged partition (priority-ordered, disjoint) — see Section 2 for the rule set
```

## 1. Issue taxonomy (classes × count × examples × proposed RADICAL disposition)

Each row gets exactly **one** primary disposition (priority-ordered, so the table sums cleanly to
1,207 — see §2). "Plain meaning" is what a human would call the row; the code/family is kept for
the audit trail. Disposition verbs: **DELETE** (not an entity at all) · **EVICT-to-component**
(implementation internal → `COMPONENT_SERVICE_MATRIX`, then drop from the process catalog) ·
**MOVE-to-substrate** (a tool/SaaS → `SUBSTRATE_REGISTRY`) · **MOVE-to-TOPIC_REGISTRY** (a subject,
not a process) · **DEDUP-merge** (a duplicate of a kept row) · **RE-TAG-area** (real work, wrong
area) · **DEMOTE-to-backlog-doc** (real but task-grain micro-step → leaves the canonical catalog,
preserved in a build-out backlog as a capability *realization*) · **KEEP**.

| # | Issue class (plain meaning) | Count | Example item_ids | Proposed RADICAL disposition |
|:--|:--|--:|:--|:--|
| 1 | **trello-task-grain-backlog** — bilingual ES/EN company build-out micro-steps imported from Trello (`gtm_cl_/launch_/services_/ops_`); the single biggest source of inflation | **386** | `gtm_ops_dtp_5`, `gtm_launch_dtp_52`, `gtm_services_dtp_1`, `gtm_cl_028e05b3126789` (101 are hash-suffixed Trello card IDs) | **DEMOTE-to-backlog-doc** (Operations/GTM build-out backlog); capabilities cite the surviving *parent* workstream/process as the realization |
| 2 | **madeira-product-backlog** — MADEIRA/KiRBe RAG / eval / orchestration / persona delivery micro-tasks (`gtm_madeira_dtp_` minus the code/scenario/product slices below) | **115** | `gtm_madeira_dtp_54`, `_102`, `_108`, `_130` | **DEMOTE-to-backlog-doc** (MADEIRA delivery backlog) or KEEP the few process-grain anchors |
| 3 | **code-symbol-as-process** — verbatim software identifiers: classes, functions, HTTP endpoints, `__main__`, `MADEIRA_SYSTEM_PROMPT`, the LlamaIndex construction block, plus `Auth` and a stray "MADEIRA API surface item" | **61** | `gtm_madeira_dtp_191` (Close Db), `_197` (MADEIRA_SYSTEM_PROMPT), `_201` (POST madeira_query), `_209` (`__main__`), `_210` (Sentiment Analyzer), `_213` (LLMConfig); `gtm_madeira_dtp_159..190` (StorageContext, VectorStoreIndex…); `gtm_ops_dtp_124` (Auth); `gtm_brand_dtp_38` | **EVICT-to-component** (verify in `COMPONENT_SERVICE_MATRIX`, then DELETE from the process catalog — these are implementation internals, not processes) |
| 4 | **brand-todo-backlog** — bilingual brand/marketing micro-tasks (`gtm_brand_dtp_`) | **48** | `gtm_brand_dtp_1` (manifesto), `_16` (access unify), `_29` (traffic research) | **DEMOTE-to-backlog-doc** (Marketing brand backlog) |
| 5 | **radar-scenario-tags** — macro/geo/tech/AI/legal/social *scenario topics* the research radar covers, mis-seeded as MADEIRA processes (`gtm_madeira_dtp_1..28`) | **28** | `gtm_madeira_dtp_1`, `_14`, `_28` | **MOVE-to-TOPIC_REGISTRY** (scenario/subject corpus; cross-area → Research) |
| 6 | **team-todo-backlog** — bilingual People onboarding / collaborator-sourcing micro-tasks (`gtm_team_dtp_`) | **26** | `gtm_team_dtp_1` (flujo cuarta pared), `_11` (capacidades faltantes), `_19` (excel perfiles fiverr) | **DEMOTE-to-backlog-doc** (People build-out backlog) |
| 7 | **cross-area-mistag (product-GTM)** — market-requirements / business-case / positioning / alpha-beta-GA rows filed under MADEIRA but owned by GTM/Product (`gtm_madeira_dtp_29..49`) | **21** | `gtm_madeira_dtp_29`, `_44`, `_49` | **RE-TAG-area** → Go-to-Market & Brand (one-cell `area` edit; no delete) |
| 8 | **convention-(2)-duplicate** — byte-for-byte duplicate rows under a `(2)` naming convention | **19** | `gtm_research_dtp_22..33`, `gtm_madeira_dtp_66/70/105/120/165`, `gtm_ops_dtp_32` | **DEDUP-merge** (delete the `(2)`, keep the original) |
| 9 | **subject-tag-not-process** — research *coverage subjects* (People, Security & Intelligence, AI, Politics, Legal…), not abilities (`gtm_research_dtp_8/9/13..19`) | **9** | `gtm_research_dtp_8` (People), `_9` (Security & Intelligence), `_14` (AI), `_18` (Legal) | **MOVE-to-TOPIC_REGISTRY** (the L5 subject spine) |
| 10 | **mind-map-import** — board cards naming *other areas'* work, imported into the Research list (`gtm_research_dtp_3/5/6/7/10/11/12`) | **7** | `gtm_research_dtp_3` (Integrate into MADEIRA), `_5` (Data Governance), `_6` (Build UI), `_10` (Design) | **RE-TAG-area** → named area (AppliedAI / Data / Tech / GTM) or DELETE if pure noise |
| 11 | **tool/SaaS-name-as-process** — a product name where a process should be | **5** | `thi_mkt_dtp_57` (Mailchimp), `_58` (Calendly), `hol_peopl_dtp_114` (Terraform), `hol_peopl_dtp_157` (CUDA Framework), `thi_data_dtp_34` (RPA) | **MOVE-to-SUBSTRATE_REGISTRY** (tools, not abilities), then DELETE from the process catalog |
| 12 | **kanban-state-row** — workflow-state enum values, not processes | **3** | `hol_opera_dtp_163` (To do), `_164` (In process), `_165` (Done) | **DELETE** (a Kanban column is not a process) |
| 13 | **research-task (genuine)** — the 3 real research-process tasks in the Research import | **3** | `gtm_research_dtp_1` (Build Research Process), `_2` (Gather Channels), `_4` (Scrape Channels) | **KEEP** (or DEMOTE) as realizations of the Research methodology/OSINT capabilities |
| 14 | **placeholder-TBD** — an explicit "to be determined" stub | **1** | `tbd_tbd_dtp_130` (Exploit (TBD)) | **DELETE** (no definable process) |
| 15 | **deprecated-dup** — a deprecated Think-Big shadow of an active Holistika process | **1** | `thi_legal_dtp_303` (Trademark and Naming Governance ≡ active `hol_lgl_prc_trademark_naming_governance_001`) | **DEDUP-merge** → the active row |
| 16 | **trello-link-artifact** — a board cross-link card, not a process | **1** | `gtm_launch_dtp_36` ("Link a tarjeta Documentar infraestructura…") | **DELETE** |
| — | **KEEP — curated stable processes** (the clean register: projects, workstreams, governed processes with review stamps / pattern / cadence wiring) | **473** | `hol_resea_prj_1`, `tbi_mkt_prc_brand_canon_mtnce_001`, `hol_eng_prc_engagement_design_001`, all `env_tech_dtp_*` runtime SOPs | **KEEP** |
| | **TOTAL** | **1,207** | | **734 flagged · 473 keep** |

> **Sub-note — placeholder-id rows that are NOT deleted.** Three rows carry the `tbd_tbd_*`
> "owner/entity unknown" prefix but describe *real* activities folded by the Operations map
> (`tbd_tbd_dtp_73` Flow Design, `_74` Flow Parameter Input, `_138` Identify Resistances). They
> sit in **KEEP** but should be **re-keyed** (given a proper `area_role_dtp_NN` id) at the gate —
> a rename, not a delete. The mojibake `�` (a corrupted em-dash) seen in several `gtm_*` names
> (`gtm_madeira_dtp_209` "MADEIRA delivery � __main__", `gtm_research_dtp_8` "Research material �
> People") is further evidence of an uncurated raw import and should be normalized for any KEEP row.

---

## 2. Reconciliation — rows touched per disposition + the clean-process estimate

The 16 classes collapse into **7 disposition verbs**. The partition is **disjoint** (priority-ordered:
DELETE → EVICT → MOVE-substrate → DELETE-state → MOVE-topic → DEDUP → RE-TAG → DEMOTE → KEEP), so
the counts sum exactly to 1,207.

| Disposition verb | Rows | Where they end up | Still a "process"? |
|:--|--:|:--|:--|
| **KEEP** | **473** | stay in `process_list` as-is (curated core) | yes |
| **RE-TAG-area** | 28 | stay in `process_list`, one `area` cell changes (21 product-GTM + 7 mind-map-import) | yes |
| **DEMOTE-to-backlog-doc** | 578 | leave the canonical catalog → a build-out backlog md; survive as capability *realizations* (386 trello + 115 madeira + 48 brand + 26 team + 3 research) | as backlog, not canonical |
| **MOVE-to-TOPIC_REGISTRY** | 37 | rehome to the L5 subject/scenario spine (28 radar-scenario + 9 subject-tag) | no — they are subjects |
| **DEDUP-merge** | 20 | merge into the kept original, row removed (19 `(2)` + 1 deprecated) | no — duplicates |
| **EVICT-to-component** | 61 | verify in `COMPONENT_SERVICE_MATRIX`, then remove from process catalog | no — implementation internals |
| **MOVE-to-SUBSTRATE_REGISTRY** | 5 | rehome to the tool/substrate registry, row removed | no — tools |
| **DELETE** | 5 | removed outright (3 kanban + 1 TBD + 1 trello-link) | no — not entities |
| **TOTAL** | **1,207** | | |

**Surviving canonical register after a full radical cut** = KEEP (473) + RE-TAG (28) = **~501 stable
canonical processes**. Of those, **473 are the untouched curated core** and 28 are clean-but-re-tagged.
The other **706** rows either move out of the canonical catalog (578 demoted to a backlog doc; still
referenceable) or leave the register entirely (128 = 61 evict + 37 topic + 20 dedup + 5 substrate + 5
delete).

**Headline reconciliation:** **734 of 1,207 flagged (60.8%)** → after radical cleanup the canonical
`process_list` holds **~473–501 stable processes** (the curated core), a **~2.4x shrink** of the
catalog. This mirrors the capability de-densify almost exactly (1,119 capability rows → ~80 stable;
the process layer cleans to ~500 because it legitimately keeps finer task/workstream grain than the
strategy-layer capability map).

> **Why "DEMOTE" is the dominant verb (578 rows), not "DELETE".** The six collapse maps are explicit
> that the `gtm_*` task-grain rows are **not deleted** — they stay reachable as the *how* (the
> realization of a capability). Radical-but-governed means **moving them out of the canonical process
> catalog into a build-out backlog doc**, not destroying them. Only the 71 rows that are genuinely
> *not processes* (code-symbols, tools, kanban states, TBD, trello-link) leave for good; the 57
> dedup/topic rows rehome to their correct register.

---

## 3. Dependency risks — what must be re-pointed so cleanup orphans nothing

I checked every inbound reference path. The result is unusually clean: **the flagged set is a closed,
unwired, shadow-only subtree.** Four of five risk vectors are near-zero; the fifth (capability
coordination) is the one that needs care.

| # | Dependency vector | Finding | Risk | Action required |
|:--|:--|:--|:--|:--|
| D1 | **Active capabilities → `originating_process_ids`** | **0 of 117** active capabilities cite **any** flagged row. The 734 flagged rows shadow only `planned` capability rows. | very low | None for active caps. |
| D2 | **Internal `item_parent` pointers** | Flagged set is a **closed subtree**: 623 children-of-flagged rows are **all themselves flagged**; **0** non-flagged (clean) rows hang off a flagged parent. | very low | Demote/remove the subtree whole; no clean row is orphaned. |
| D3 | **Live-system columns** | **0** flagged rows carry `engagement_template_id`, `persona_id`, `inherited_pattern_id`, `cadence_type`, or revenue values. All 73 pattern + 65 cadence wirings sit on **non-flagged** rows. All 734 share the single bulk stamp `D-IH-71-CLOSURE`. | very low | Removing flagged rows breaks no live engagement / persona / pattern / cadence binding. |
| D4 | **Supabase mirror** (`compliance.process_list_mirror`) | Mirror table exists, RLS-denied to `anon`/`authenticated`. Any delete/demote must be re-emitted. | governed | After the gate: `py scripts/verify.py compliance_mirror_emit` → `pwsh scripts/apply_mirror_batches.ps1`. A re-sync obligation, **not** an orphan risk. |
| D5 | **Capability de-densify (D-IH-95-I) — shared rows** | The collapse maps wire `originating_process_ids` (N:N) to these very rows as *realizations*. Cleanup that hard-deletes a row a de-densified capability cites would orphan that realization edge. | **the real one** | **Co-sequence** (see §4): either run cleanup so capabilities point at the **surviving parent** workstream/process, or **demote (preserve id)** rather than delete any row a capability realizes. |
| D6 | **Other registers / scripts** | `OPS_REGISTER.csv` has only a backlog *note* (OPS-86-23, legacy SOP-pairing), no row-level FK. Two import scripts (`dedupe_ambiguous_process_item_names.py`, `refine_gtm_process_hierarchy.py`) reference the families — they are the *import tooling*, not live consumers. | low | None; optionally retire the import scripts post-cleanup. |

**Net dependency posture:** the only thing the cleanup must actively protect is the **realization
wiring the capability collapse is about to create** (D5). Because the collapse and the cleanup share
the same rows, they must be **co-sequenced** — which the ratified synthesis already anticipates
(`_SYNTHESIS-2026-06-08.md` §6 step 6: "process_list cleanup, coordinated, after its AskQuestion").

---

## 4. Recommended cleanup sequencing (safe-radical now vs needs-care)

Three tiers, ordered by dependency-safety. Every `process_list` edit is the **hardest-gated**
canonical change (operator approval + `AskQuestion` + `validate_hlk.py`), so the gates batch
**per area** to keep operator attention bounded.

### Tier A — safe-radical now (zero capability coordination; mechanical, reversible) — 34 rows
- **DELETE** the 5 non-entities (3 kanban states `hol_opera_dtp_163/164/165` + `tbd_tbd_dtp_130` + `gtm_launch_dtp_36`). Self-evidently not processes; 0 dependencies.
- **DEDUP-merge** the 20 duplicates (19 `(2)` rows + the deprecated `thi_legal_dtp_303`). Mechanical: keep the original, drop the `(2)`.
- **MOVE-to-TOPIC_REGISTRY** the 9 pure subject-tags (`gtm_research_dtp_8/9/13..19`). The Research map already recommends this exact L5 hand-off.
These can run **first / in parallel** with the capability pilot — they touch no realization wiring.

### Tier B — radical, but co-sequence with each per-area capability slice — ~672 rows
Run **inside** the synthesis §6 order (Data+Finance+Legal pilot → Marketing → Research → People →
Operations → Tech) so each area's capability rewrite and its process demote land **together** and
`originating_process_ids` wire to **survivors**:
- **DEMOTE-to-backlog-doc** the 578 task-grain rows → one build-out backlog md per area (Operations 386, MADEIRA 115, Marketing 48, People 26, Research 3). **Demote, do not delete** — they remain capability realizations (this is the D5 guardrail).
- **EVICT-to-component** the 61 code-symbols (the `gtm_madeira_dtp_191..217` block + 159..190 LlamaIndex + `Auth` + the brand API symbol) — verify in `COMPONENT_SERVICE_MATRIX` first, then remove (the D-IH-95-I ratified split).
- **MOVE-to-SUBSTRATE_REGISTRY** the 5 tools (Mailchimp, Calendly, Terraform, CUDA, RPA).
- **MOVE-to-TOPIC_REGISTRY** the 28 radar-scenario rows (`gtm_madeira_dtp_1..28`) — coordinate with the Research scenario corpus.
- **RE-TAG-area** the 28 cross-area rows (21 product-GTM `gtm_madeira_dtp_29..49` → GTM; 7 mind-map imports → named area).

### Tier C — closeout (after every slice)
Re-emit `compliance.process_list_mirror` (`compliance_mirror_emit` → `apply_mirror_batches`), run
`validate_hlk.py`, and run the capability-rollup audit (every surviving `originating_process_id`
resolves) before flipping any registry status.

### Decisions that need operator inline-ratify (judgment, not mechanical)
1. **DEMOTE-vs-KEEP boundary for the 153 process-grain `gtm_*` rows** (not all `gtm_*` is task-grain; some are real sub-processes). Spot-check per area.
2. **The People 14-row legacy-methodology fold** (four-wall / arrowhead / engage-pacify-hijack) — keep-as-one / split / evict-subset. Already flagged as the one residual judgment in the People map.
3. **TOPIC_REGISTRY vs a dedicated scenario registry** for the 28 radar rows.
4. **The Legal Privacy-split** option (would make Legal 11→4).
5. **Per-row eviction routing** (substrate vs component-matrix) confirmation — the class is ratified (D-IH-95-I); the per-row target is the spot-check.

---

## 5. "How radical" spectrum + recommendation

| Level | Scope | Rows touched | Canonical catalog after | What it buys / leaves |
|:--|:--|--:|--:|:--|
| **Conservative** | re-tag + dedup only | **48** (RE-TAG 28 + DEDUP 20) | ~1,159 | Fixes wrong area tags + removes duplicates. **Leaves** all 578 task-grain micro-steps, 61 code-symbols, 5 tools, 37 subjects in the catalog. Cosmetic; the register stays inflated 2.4×. |
| **Moderate** | + demote task-grain to a backlog doc + rehome tools/subjects | **+615** (DEMOTE 578 + MOVE-substrate 5 + MOVE-topic 37) → **663** | ~501–562 | Catalog becomes strategy-legible; build-out backlog preserved. **Leaves** the 61 code-symbols + 5 deletes pending (a second pass later). |
| **Radical** | + evict code-symbols + delete kanban/TBD/trello-link | **+71** (EVICT 61 + DELETE 5; the 5 substrate already in Moderate) → **734** | **~473–501** | Full clean: only curated, wired, reviewed processes remain. One pass, fully co-sequenced with the capability collapse. |

### Recommendation: **Radical — governed by two guardrails.**

I recommend the **Radical** level, because the dependency analysis (§3) shows it is *safe*, not just
desirable: **0** active capabilities reference the flagged rows, the set is a **closed subtree**, and
**0** rows carry live engagement/persona/pattern/cadence wiring — they are an uncurated bulk import
(one shared stamp `D-IH-71-CLOSURE`) that never entered the live system. Doing it Radical also means
**one pass**: the capability de-densify (D-IH-95-I) is already rewriting the shadow layer, so cleaning
the source layer in lockstep avoids a second disruption and a second operator gate.

The two guardrails that make "Radical" *governed* rather than reckless:

1. **DEMOTE, don't DELETE, the 578 task-grain rows.** They survive in per-area build-out backlog docs
   as capability *realizations* — so the collapse's `originating_process_ids` wiring (D5) stays valid.
   Hard DELETE is reserved for the **71 rows that are genuinely not processes** (code-symbols, tools,
   kanban, TBD, trello-link) + the 57 dedup/topic rehomes.
2. **Co-sequence per area** with the capability slices (synthesis §6 order), with an `AskQuestion`
   gate per area. Tier-A hygiene (34 rows) can go first/in-parallel.

**Net effect of the recommendation:** **734 of 1,207 rows flagged → a ~473–501 row clean canonical
`process_list`** (the curated, wired, reviewed core), achieved in one governed pass co-sequenced with
the capability de-densify. Conservative is too timid (leaves the 2.4× inflation that triggered this
sweep); pure-delete Radical would orphan capability realizations — the **demote-not-delete + co-sequence**
shape is the radical-but-governed answer the operator asked for.

---

## Cross-references
- Parent synthesis (names this doc): [`l2-collapse-maps/_SYNTHESIS-2026-06-08.md`](l2-collapse-maps/_SYNTHESIS-2026-06-08.md) §5 + §6 — **D-IH-95-I**.
- Method (reused): [`l2-capability-densify-findings-2026-06-07.md`](l2-capability-densify-findings-2026-06-07.md) — 6-step collapse + eviction rule — **D-IH-95-H**.
- Source-layer findings consolidated from the six maps: [`operations-`](l2-collapse-maps/operations-collapse-map.md) · [`tech-`](l2-collapse-maps/tech-collapse-map.md) · [`marketing-`](l2-collapse-maps/marketing-collapse-map.md) · [`people-`](l2-collapse-maps/people-collapse-map.md) · [`research-`](l2-collapse-maps/research-collapse-map.md) · [`data-finance-legal-collapse-map.md`](l2-collapse-maps/data-finance-legal-collapse-map.md).
- Source register (read, **not modified**): [`process_list.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv).
- Shadow register: [`CAPABILITY_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv) (1,119 rows; 117 active / 1,001 planned / 1 deprecated).
- Rehome targets: `dimensions/TOPIC_REGISTRY.csv` (subjects + scenarios) · `dimensions/COMPONENT_SERVICE_MATRIX.csv` (code-symbols) · `SUBSTRATE_REGISTRY` (tools).
- Mirror: `compliance.process_list_mirror` ([`supabase/migrations/20260503190000_i14_phase3_compliance_and_holistika_ops.sql`](../../../../supabase/migrations/20260503190000_i14_phase3_compliance_and_holistika_ops.sql)).
- Governing rules: `akos-baseline-governance.mdc` (canonical-CSV gate — `process_list` is the hardest-gated), `akos-inline-ratification.mdc` (the per-area `AskQuestion` gates), `akos-area-governance.mdc` RULE 2 (`MKT` not `Marketing`).
- Gate posture: this doc modifies **no** CSV. The actual cleanup is a gated canonical-CSV change requiring explicit operator approval per named tranche.
