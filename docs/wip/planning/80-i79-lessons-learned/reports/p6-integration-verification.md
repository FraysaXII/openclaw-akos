---
language: en
status: active
canonical: false
classification: way_of_working
intellectual_kind: phase_integration_verification
phase: P6
initiative: INIT-OPENCLAW_AKOS-80
authored: 2026-05-16
last_review: 2026-05-16
role_owner: People Operations Lead
ssot: false
companion_to:
  - ../master-roadmap.md
  - ../decision-log.md
  - p6-uat-2026-05-16.md
---

# I80 P6 — Integration verification (2026-05-16)

> Cross-reference matrix confirming I80's three tracks land coherently into the People area's existing canonicals + cursor rules + skills + planning surfaces. Companion to [`p6-uat-2026-05-16.md`](p6-uat-2026-05-16.md).

## 1. Track 1 — Stakeholder lenses paired files (P2)

| Surface | Integration check | Status |
|:---|:---|:---:|
| `HOLISTIKA_STAKEHOLDER_LENSES.md` body | Lands at `Admin/O5-1/People/canonicals/` (correct area; co-located with `HOLISTIKA_ORGANISING_DOCTRINE.md` and `HOLISTIKA_AGENTIC_DOCTRINE.md`) | **PASS** |
| `HOLISTIKA_STAKEHOLDER_LENSES.addendum.md` | Co-located with body; `parent_sop:` frontmatter points to body; `companion_to:` cross-references siblings | **PASS** |
| `PRECEDENCE.md` registration | Both files registered as canonical; addendum carries `intellectual_kind: people-canonical-addendum` | **PASS** |
| Jargon-scan body coverage | `HOLISTIKA_STAKEHOLDER_LENSES.md` added to `PEOPLE_CANONICALS_RELATIVE` scan list at I80 P2; scan PASS | **PASS** |
| Jargon-scan addendum exemption | Addendum suffix (`.addendum.md`) excluded from scan per `D-IH-80-F` (DAMA-aligned addendum-class exemption) | **PASS** |
| `process_list.csv` review row | `tbi_peopl_dtp_stakeholder_lenses_review_001` appended; cadence=scheduled (annual) + event_triggered; SOP-only acceptable per `D-IH-72-W` feature-flag posture | **PASS** |
| Forward read into I76 (Madeira elevation) | Apprentice + Cleared Collaborator lenses written to anticipate Madeira agent voicing; addendum §A founder reflection cites I76 forward-vision context | **PASS (forward-anchored)** |

## 2. Track 2 — SOP body/addendum pattern (P1 + P4 + P5)

### 2a. Pattern mint (P1)

| Surface | Integration check | Status |
|:---|:---|:---:|
| `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` | `pattern_sop_addendum_split` row appended; `pattern_class=documentation_layering` (the new 11th class) | **PASS** |
| `akos/hlk_design_pattern_csv.py` Pydantic model | `VALID_PATTERN_CLASSES` extended with `documentation_layering`; tests cover the new enum value | **PASS** |
| `tests/test_design_pattern_registry.py` | New tests for `documentation_layering` pattern class + `pattern_sop_addendum_split` row presence | **PASS** |
| `PEOPLE_DESIGN_PATTERN_LIBRARY.md` narrative section | `#pattern-sop-addendum-split` anchor authored; cross-references jargon-scan validator + addendum exemption rule | **PASS** |
| `SOP-META_PROCESS_MGMT_001.md` extension | New §"Body and Addendum split" formalises the pattern at SOP-authoring contract level (not just descriptive) | **PASS** |
| `validate_design_pattern_registry.py --jargon-scan` refinement | `*.addendum.md` files exempt from scan per `D-IH-80-F`; sibling addenda counted and reported as informational | **PASS** |
| `PRECEDENCE.md` addendum-class registration | Generic addendum-canonical-class entry added; per-pair entries follow at P2/P4/P5 | **PASS** |

### 2b. Pattern instantiations (running count after I80 P5)

| # | Body | Addendum | Phase | Pattern role |
|:---:|:---|:---|:---:|:---|
| 1 | `HOLISTIKA_STAKEHOLDER_LENSES.md` | `HOLISTIKA_STAKEHOLDER_LENSES.addendum.md` | P2 | First instantiation; founder-reflection-as-deeper-layer |
| 2 | `SOP-PEOPLE_AGENTIC_OPERATIONS_001.md` | `SOP-PEOPLE_AGENTIC_OPERATIONS_001.addendum.md` | P4 | I79 retrofit; Tech Lab posture moved to addendum |
| 3 | `SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md` | `SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.addendum.md` | P4 | I79 retrofit; KB tier integration matrix moved to addendum |
| 4 | `SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md` | `SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.addendum.md` | P5 | I73 retrofit; 7-class taxonomy rationale + FK posture |
| 5 | `SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md` | `SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.addendum.md` | P5 | I73 retrofit; enum semantics + Legal template routing |
| 6 | `SOP-ENGAGEMENT_ONBOARDING_001.md` | `SOP-ENGAGEMENT_ONBOARDING_001.addendum.md` | P5 | I73 retrofit; 4-channel persistence + access-level routing |
| 7 | `SOP-ENGAGEMENT_PAYROLL_OPS_001.md` | `SOP-ENGAGEMENT_PAYROLL_OPS_001.addendum.md` | P5 | I73 retrofit; FINOPS architecture + €400/mo cap rationale |
| 8 | `SOP-ENGAGEMENT_OFFBOARDING_001.md` | `SOP-ENGAGEMENT_OFFBOARDING_001.addendum.md` | P5 | I73 retrofit; round review + IP filing matrix |

**Total: 8 paired-file instantiations after I80 P5.** I81 forward-charter adds ~40 more (full-vault retrofit at ~30+ SOP body files across 11 areas; some areas may legitimately keep monolithic bodies per their register; expected paired count: 30-35).

### 2c. SOPs-readable-as-manifesto check

The operator's framing for this initiative ([Round-1 ratification](../decision-log.md#d-ih-80-d)): *"i'd like the SOPs to [read like the manifesto], it's our responsibility to make sure people understand what they read"*.

| Pair | Body register | Addendum register | Operator-readable test |
|:---|:---|:---|:---:|
| Pair 1 (stakeholder lenses) | Plain language; access_level 4 | Founder voice + agent narrative; access_level 5 | **PASS** (manifesto-class plain-language body; addendum is companion not gate) |
| Pair 2 (agentic operations) | Plain language; SOP register | Tech Lab framework jargon legitimately moved out of body | **PASS** (body now reads as People SOP without requiring framework knowledge) |
| Pair 3 (cross-area breakthrough) | Plain language; SOP register | KB tier integration + scoring depth in addendum | **PASS** (body reads as cross-area communication SOP; addendum carries the depth) |
| Pair 4-8 (engagement lifecycle) | People register; small frontmatter additions only | Cross-area depth (FINOPS + Compliance + Legal + Workspace) in addendum | **PASS (frontmatter-only retrofit)** — bodies were already plain-language at I73 closure; P5 retrofit adds the addendum companion without trimming bodies (small body content was already executor-readable). The retrofit demonstrates the pattern can be applied at low cost when the body is already clean. |

## 3. Track 3 — Inline-ratify craft skill (P3)

| Surface | Integration check | Status |
|:---|:---|:---:|
| `.cursor/skills/inline-ratify-craft/SKILL.md` | Created with `description:` trigger phrases (inline-ratify, AskQuestion, ratification gate, etc.); ratifying_decisions cite `D-IH-80-A` + `D-IH-80-E` | **PASS** |
| `.cursor/rules/akos-inline-ratification.mdc` extension | New §"Quality bar for inline-ratify calls" section cross-references the skill; updated cross-references section | **PASS** |
| Skill discoverability | `description:` field includes phrase triggers (`inline-ratify`, `AskQuestion`, `ratification gate`, `operator decision`, `option set`, `evidence sweep + ratify`, `gate_type of inline-ratify`) | **PASS** |
| Skill self-test | Skill renders correctly in Cursor agent skills panel (verified by `available_skills` enumeration; skill listed and accessible) | **PASS** |
| Cross-reference integrity | Skill cites I79 worked example (Phase 8 §8.7 GOI class regression hunt); rule cites skill back; both cite the I80 decision log | **PASS** |

## 4. Cross-rule + cross-doctrine integration

| Adjacent surface | Integration check | Status |
|:---|:---|:---:|
| `akos-planning-traceability.mdc` §"Plan-quality bar" | I80 master-roadmap meets the bar (multi-sentence YAML todos; phase dependencies; decision preview; risk register; per-phase deep sections) | **PASS** |
| `akos-governance-remediation.mdc` §"Commit and phase discipline" | One atomic commit per phase (P0 + P1 + P2 + P3 + P4 + P5 = 6 commits; P6 + P7 = remaining 2) | **PASS** |
| `akos-holistika-operations.mdc` §"New git-canonical compliance registers (pattern)" | I80 mints zero new canonical CSVs (no register additions); only extends `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` by 1 row + appends 1 process_list row | **PASS (out-of-scope; no register churn)** |
| `akos-executable-process-catalog.mdc` Rule 1 (SOP+runbook pairing) | I80 P2 added one SOP-only review row (`tbi_peopl_dtp_stakeholder_lenses_review_001`); SOP-only acceptable per `D-IH-72-W` feature-flag pattern (paired runbook is a future-initiative deferment) | **PASS (informational warning logged)** |
| `akos-mirror-template.mdc` (sibling-repo posture) | I80 ships zero sibling-repo changes; AKOS remains SSOT | **PASS** |
| `akos-agent-checkpoint-discipline.mdc` (pause-record cadence) | I80 is 7-phase / ~4 days; per heuristic table, recommended pause density = 2-3 pause points; I80 plans pause records at P3 (mid) + P7 (closure) — see master-roadmap | **PASS (per heuristic)** |
| `HOLISTIKA_ORGANISING_DOCTRINE.md` (organising principles) | I80 deliverables align with the access_level routing convention (level-4 body / level-5 addendum) and the cross-area-respect principle (no Tech jargon in People bodies) | **PASS** |
| `HOLISTIKA_AGENTIC_DOCTRINE.md` (agentic doctrine) | I80 P3 inline-ratify skill operationalises the agentic-doctrine rule that agents must compound operator reasoning rather than extract decisions | **PASS** |
| `PEOPLE_DESIGN_PATTERN_LIBRARY.md` (pattern library) | I80 P1 adds `pattern_sop_addendum_split` as the 13th pattern; library narrative integrity preserved | **PASS** |

## 5. New patterns adopted in I80

| Pattern | First instantiation | Subsequent instantiations |
|:---|:---|:---|
| `pattern_sop_addendum_split` (minted P1) | P2 (stakeholder lenses paired files) | P4 (2 SOPs) + P5 (5 SOPs) = **8 total** |
| `pattern_inline_ratify_via_askquestion` (existing) | I79 worked-example (Phase 8 §8.7) | I80 P3 codifies craft skill; I80 P0 used inline-ratify in 4 batched calls during charter |
| `pattern_paired_sop_runbook` (existing) | Many | I80 P2 SOP-only review row inherits the SOP-only legitimate variant per `D-IH-72-W` |

## 6. SOPs-readable-as-manifesto closure check (the operator's framing)

The operator's I79-closure framing: *"the goal of an SOP is to enable a person to execute the process e2e with relevant context and all, but all the supporting documentation can very well go into addendum, that way we can keep the extreme jargon weave in some SOPs out of the way, at least when it's jargon of another area"*.

I80 operationalises this as a *contract*:

1. **`pattern_sop_addendum_split` minted** (P1) — the pattern is now in the registry, narrative library, meta-SOP authoring contract, and Pydantic-validated. Future SOP authors must consider it.
2. **8 paired instantiations shipped** (P2 + P4 + P5) — the pattern has demonstrated coverage across 3 SOP families: doctrine (stakeholder lenses), People SOPs (agentic operations + cross-area breakthrough), and engagement-lifecycle SOPs (5-file batch).
3. **Jargon-scan validator extended** (P1) — addenda are excluded from People-canonical jargon scan, so technical depth in addenda doesn't block scan. Body files remain scan-strict.
4. **Forward-charter to full vault** (P6 / I81 candidate) — the remaining ~40 SOP bodies across 11 areas have an explicit retrofit roadmap. Conclusion: I80 closes with the operator's framing operationalised at *contract level*, not just at example level.

## 7. SOC posture

This integration verification report contains: zero secrets, zero API keys, zero raw GOI/POI mappings, zero full prompts, zero PII. All cross-references are public-naming-safe per the GOI/POI obfuscated-knowledge-dimension contract.

## Cross-references

- I80 master roadmap: [`master-roadmap.md`](../master-roadmap.md)
- I80 decision log: [`decision-log.md`](../decision-log.md)
- I80 P6 UAT: [`p6-uat-2026-05-16.md`](p6-uat-2026-05-16.md)
- I81 candidate stub: [`docs/wip/planning/_candidates/i81-full-vault-sop-addendum-retrofit.md`](../../_candidates/i81-full-vault-sop-addendum-retrofit.md)
- I79 P7 integration verification precedent: [`docs/wip/planning/79-people-manifesto-and-pattern-library/reports/p7-integration-verification.md`](../../79-people-manifesto-and-pattern-library/reports/p7-integration-verification.md)
