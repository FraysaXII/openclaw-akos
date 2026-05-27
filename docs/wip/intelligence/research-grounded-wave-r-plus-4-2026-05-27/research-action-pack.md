---
language: en
status: draft
intellectual_kind: research_action_pack
sharing_label: internal_only
audience: J-OP;J-AIC
role_owner: Research Director + KM Officer
authored: 2026-05-27
last_review: 2026-05-27
linked_commit: f0928dd
linked_sources:
  - source-ledger.csv
  - master-synthesis.md
  - research-pipeline.md
linked_canonicals:
  - docs/wip/intelligence/README.md
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md
  - docs/references/hlk/v3.0/Research/Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md
---

# Wave R+4 Research Action Pack

## 1. Operator Correction Absorbed

The operator did not approve C2 after the first C1 substrate commit. The correction is load-bearing:

> Research cannot be a loose synthesis that immediately authorizes canonical edits. Research needs its own governed action layer: topic taxonomy, source categories, source format, Holistika reliability score, external-perceived credibility score, metadata, workflow, ERP/KB fit, and then decision questions surfaced after the findings are processed.

So C1 is **not closed** by commit `f0928dd`. That commit is a substrate capture. This C1.5 pack is the action layer that makes the research usable.

## 2. Placement Decision

The research folder lives under `docs/wip/intelligence/` because existing canon already says Research owns that path as Tier 1 WIP:

- `docs/wip/intelligence/README.md` says the folder is Research-owned cross-area research staging.
- `RESEARCH_AREA_CHARTER.md` says Research owns Tier 1 WIP and that other areas consume Research outputs.
- `INTELLIGENCE_DISCIPLINE_CHARTER.md` says Intelligence owns what we collect, while Validation owns what is true.

The operator's harmonization concern is still valid: the name `intelligence` can read narrower than the actual research-action need. The correct C1.5 disposition is **do not move folders mid-wave**. Instead, record a forward governance question:

> Should Tier 1 WIP stay named `docs/wip/intelligence/`, or should a future index/harmonization tranche rename or alias it as `docs/wip/research/` while preserving historical paths?

That question belongs in C5 KB integrity drain or a successor Research topology tranche, not inside C2 audience/lifecycle governance.

## 3. Metadata Schema for This Research Action

`source-ledger.csv` is the control surface for C1.5. It adds the metadata the first C1 synthesis lacked.

| Field | Meaning | Canonical anchor |
|:---|:---|:---|
| `source_id` | Stable ID inside this research action. | Local C1.5 ledger. |
| `prong` | Which research prong uses the source. | `README.md` and `master-synthesis.md`. |
| `topic_cluster` | The topic family the source informs. | Candidate for future `RESEARCH_PRIORITIZATION_REGISTER.csv`. |
| `source_title_or_owner` | Human-readable source name. | Local ledger. |
| `url` | Durable public URL. | Source citation. |
| `format` | Article, video transcript, report, book, podcast, dataset, internal transcript, or canonical. | Operator-requested info-format metadata. |
| `source_category` | OSINT / HUMINT / CORPINT / etc. | `source_taxonomy.md`. |
| `source_level` | Numeric source level. | `source_taxonomy.md` source-level ladder. |
| `holistika_reliability_score` | 1-5 internal reliability score: how much Holistika should trust/use this source for this decision. | `source_taxonomy.md` `intel_source_holistika_credibility`. |
| `external_perceived_credibility_score` | 1-5 expected outside-reader credibility: how persuasive this source looks to investors/advisors/customers. | `source_taxonomy.md` `intel_source_public_credibility`. |
| `control_confidence_level` | Safe / Euclid / Keter: control intensity, not truth certainty. | `confidence_levels.md`. |
| `decision_use` | Which downstream decision the source can support. | C2/C3/C4 wave plan. |
| `notes` | Why the source is useful or limited. | Research action judgment. |

Important correction: the first C1 synthesis used `CL2` / `CL3` / `CL4` as a shorthand confidence score. The actual `confidence_levels.md` canonical only has Safe / Euclid / Keter. C1.5 therefore separates:

- **Control confidence**: Safe / Euclid / Keter.
- **Source level**: source taxonomy level such as `4.3 Leading-Edge`.
- **Holistika reliability score**: internal 1-5.
- **External perceived credibility score**: public-reader 1-5.

This prevents a fake precision problem where "CL4" looks canonical but is not.

## 4. Operating Workflow

| Stage | Action | Output | Governance checkpoint |
|:---|:---|:---|:---|
| 1. Topic intake | Operator/AIC/role-owner names a research need. | Topic row candidate with scope and owner. | Research Director decides whether it is strategic, tactical, or operational. |
| 2. Source ingest | Collect sources and transcripts. | `source-ledger.csv` rows. | KM Officer checks source category + format + URL/transcript availability. |
| 3. Rate | Assign source level, Holistika reliability, external perceived credibility, and control confidence. | Rated source ledger. | Validation discipline reviews Keter-control items before canonical use. |
| 4. Rank | Rank sources by decision relevance, not just credibility. | Prong-level ranked list. | PMO checks which downstream decisions depend on the finding. |
| 5. Synthesize | Write claim-level synthesis with internal-canonical mapping. | Prong synthesis + master synthesis. | Research Director checks every claim has source + Holistika-fit translation. |
| 6. Govern | Surface canonical-change questions only after synthesis is processed. | AskQuestion batch or decision-row draft. | Canonical CSV gates fire only here, never at raw-research stage. |
| 7. Implement | Area owner authors canonical/process/output changes. | C2/C3/C4 commits. | Area-specific validators + `validate_hlk.py`. |
| 8. Test | Check outputs and user-facing surfaces. | Validator output + UAT/render trails. | UAT / render / inter-wave checks. |
| 9. Iterate | Promote, reject, defer, or keep as radar. | Decision row + tracker or candidate. | C5 KB integrity drain updates location and status. |

## 5. Research Radar Shape

The operator's desired future state is an agentic research radar, not a one-off dossier. C1.5 names the minimal shape:

| Radar object | Required fields | Notes |
|:---|:---|:---|
| Topic | `topic_id`, `topic_name`, `owner_role`, `strategic_question`, `decision_deadline`, `status`. | Existing `RESEARCH_BACKLOG_TRELLO_REGISTRY.md` is a partial seed. |
| Source | `source_id`, URL/path, source category, source level, format, ingested_at, transcript_path when any. | `source-ledger.csv` is the local prototype. |
| Finding | `finding_id`, claim, supporting sources, confidence/control class, contradicted_by, impacted_canonicals. | Should become queryable in KiRBe/ERP later. |
| Recommendation | `recommendation_id`, downstream decision, options, recommended default, reversibility, owner. | This is the bridge to `AskQuestion` and DECISION_REGISTER rows. |
| Implementation link | commit, files changed, validators, UAT/render evidence. | This closes the research-to-implementation loop. |

## 6. What C1.5 Adds to the First C1 Commit

| Gap in `f0928dd` | C1.5 correction |
|:---|:---|
| Sources cited but not governed as rows. | `source-ledger.csv` gives source IDs and metadata. |
| "CL3/CL4" shorthand not aligned to canonical `confidence_levels.md`. | This pack separates control confidence, source level, internal reliability, and external credibility. |
| Research folder placement not justified. | This pack cites Research Area + WIP ownership canon and surfaces a future harmonization question. |
| C2 AskQuestion asked too early. | This pack blocks C2 until the source ledger + workflow are processed. |
| ERP/KB implications implied but not named. | This pack names the research radar object model and workflow checkpoint surfaces. |

## 7. C2/C3/C4 Decision Questions Not Yet Ready

These are the questions C1.5 must answer before another ratification batch:

1. **Investor segmentation**: Does the source ledger justify `AUDIENCE_REGISTRY` sub-audience rows, or only `PERSONA_REGISTRY` / `PERSONA_SCENARIO_REGISTRY` rows? Also decide whether audience-code regex widening is worth the downstream validator/test cost.
2. **Lifecycle taxonomy**: Is the 8-stage Demand-to-Cash scaffold a canonical now, or does it first need a Research/Validation pass with more analyst-grade sources?
3. **Brand propagation**: Which channels are load-bearing now (Email outbound, LinkedIn DM, Web form, Cal schedule, Event meeting), and which role owns each artifact class?
4. **Research-first doctrine**: Is the doctrine promotion a People meta-discipline amendment, a Research-area process, or both? The operator explicitly rejected tying it to a random I86 task; it must be framed as organization-wide research operations if promoted.
5. **Investor outputs**: Which brief variants are justified by the source ledger, and which should be held as internal-only radar until Holistika has more public proof?

## 8. C1.5 Verdict

C1.5 turns C1 from "research summary" into "research action." It does not authorize C2 canonical edits yet.

Required before C2 resumes:

- `source-ledger.csv` exists and is reviewed.
- `master-synthesis.md` count/metadata language is corrected to match this pack.
- The operator receives a new, better ratification batch that starts from processed findings, not from pre-filled implementation choices.
