---
intellectual_kind: doctrine_articulation_for_research_first_posture
sharing_label: internal_only
authored: 2026-05-27
last_review: 2026-05-27
parent_initiative: I86
parent_tranche: wave-r-plus-4-research-grounded-brand-ops-mktops-investor-disambiguation
linked_decisions:
  - D-IH-86-EU
  - D-IH-86-AU
  - D-IH-86-AS
linked_canonicals:
  - akos-applied-research-discipline.mdc
  - RESEARCH_HEAD_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - PEOPLE_DESIGN_PATTERN_REGISTRY.csv
  - RESEARCH_BACKLOG_TRELLO_REGISTRY.md
status: drafting
role_owner: System Owner (assistant in donde-r capacity per operator R&D-name doctrine)
co_owner_role: PMO
audience: J-OP, J-AIC
language: en
---

# Research-first as Holistika's strategic identity-anchor — the operator-named pipeline doctrine

## TL;DR (for J-OP)

The operator named verbatim at the 2026-05-27 Wave R+4 ratify gate:

> *"we are people who will go saying our NAME is R&D, how can i not come as donde-r and ask for a deep research to enrich, prove, disprove, discover, ingest, reference, optimize, wire, whatever we want to do with our plans? research goes always first and give to the organisation what we need strategically tactically and operationally, then the areas do their thing. why would we have in those research if i can't use it to take decisions. what can i flex about when i flex we're a research based company"*

This file articulates that framing as a **doctrine candidate** — naming the pipeline shape the operator named, mapping it to existing Holistika canonicals (which already carry the underlying discipline at a more individual-agent tier), and proposing the gates that would justify formal promotion from craft-on-individual-agent tier to org-wide strategic-posture tier.

Whether the formal promotion happens is a **C2 governance commit decision**, gated on C1 research findings (this file is part of C1; the question gets answered AT C2 with the research in hand, not before).

## The pipeline the operator named (verbatim)

> *"ingest → rate → rank → govern → implement → test → iterate"*

Eight verbs naming a 7-stage research-to-decision pipeline. Each stage carries a specific operational commitment:

| Stage | Verb | Operational meaning | Existing Holistika carrier |
|:---|:---|:---|:---|
| 1 | **Ingest** | Capture external research (industry sources / academic / practitioner / YouTube / podcasts / books) into a durable, retrievable format. | KiRBe knowledge platform (active dev); `RESEARCH_BACKLOG_TRELLO_REGISTRY.md` (existing infrastructure); Supabase research playlists table (operator mentioned existence; AKOS does not yet have ingest pipeline wired). |
| 2 | **Rate** | Apply confidence + source-quality grading (per `confidence_levels.md` + `source_taxonomy.md`). NOT every source carries equal weight; a peer-reviewed academic paper outranks a Twitter thread on the same topic. | `confidence_levels.md` (canonical; CL1-CL5 enum) + `source_taxonomy.md` (canonical; source-class taxonomy). |
| 3 | **Rank** | Sort rated sources by relevance to the org's current strategic / tactical / operational priorities. A high-confidence source on an irrelevant topic ranks lower than a medium-confidence source on a load-bearing topic. | No existing single carrier; this stage is currently done craft-on-individual-agent. Candidate: a `RESEARCH_PRIORITIZATION_REGISTER.csv` or extension to `RESEARCH_BACKLOG_TRELLO_REGISTRY.md`. |
| 4 | **Govern** | Decide which ranked findings get authoritatively absorbed into Holistika canonicals (cursor rules / specialty doctrines / SOPs / templates) vs which stay as Tier 1 WIP intelligence vs which get archived as out-of-scope. | `PRECEDENCE.md` governs canonical-vs-mirrored-vs-reference; `akos-applied-research-discipline.mdc` RULE 1-3 governs internal+external evidence sweeps + citation contracts; `RESEARCH_HEAD_DISCIPLINE.md` governs the discipline at canonical level. |
| 5 | **Implement** | Translate governed findings into concrete area-owned outputs: brand-ops processes; mktops runbooks; channel doctrines; SOPs; canonical-CSV rows; cursor rules; skills. | Area-specific (Marketing / People / System Owner / RevOps); operationalised via `akos-executable-process-catalog.mdc` paired SOP+runbook discipline. |
| 6 | **Test** | Validate that the implementation actually produces the strategic / tactical / operational outcome the research predicted. Self-tests + field-tests + observability signals per `akos-uat-discipline.mdc` + closure-loop test contract from `akos-synthesis-before-tranche.mdc` SYN-09. | UAT discipline (canonical); synthesis-before-tranche closing-loop test; release-gate INFO ramp; validator self-tests at pre_commit. |
| 7 | **Iterate** | Feed test outcomes back to step 1 (ingest amended findings) + step 4 (govern amendments to canonicals) — the loop closes. Wave-close cadence per `akos-inter-wave-regression.mdc`; index-freshness cadence per `akos-index-integrity.mdc`. | Wave-close discipline; pattern-registry maintenance; specialty-promotion ramp gates. |

## Holistika already carries the discipline (at sub-org-wide tier)

The pipeline above is NOT a new doctrine. Every stage maps to an existing canonical or cursor rule. What the operator's 2026-05-27 framing names is not the **shape** of the discipline but its **tier of governance**:

- **Current tier (pre-Wave-R+4):** craft-on-individual-agent. The discipline is articulated in canonicals + rules, but its application is at the discretion of the individual agent / role-owner working on a given tranche. Some tranches execute it diligently (Wave R+1 12th specialty mint cited 3 prongs of external research; Wave R+3 SUEZ POC SEND PACK absorbed the 13/05 transcript before authoring); some tranches execute it shallowly (the rejected v1 investor stability dossier did NOT execute external research on investor sub-personas before drafting).
- **Candidate tier (post-Wave-R+4 if C1 validates):** org-wide strategic-posture. Research-first becomes a binding upstream gate for every strategic / tactical / operational decision class — equivalent to how `akos-synthesis-before-tranche.mdc` is binding for every tranche, `akos-uat-discipline.mdc` is binding for every closure UAT, `akos-quality-fabric.mdc` is binding for every quality-bound artifact.

The promotion path would mint:

1. A formal amendment to `akos-applied-research-discipline.mdc` adding RULE 4 (org-wide upstream-gate posture) + cross-reference to this pipeline file.
2. A formal amendment to `RESEARCH_HEAD_DISCIPLINE.md` §"Promotion gates" with the gate criteria (≥ 3 worked-example tranches demonstrating the 7-stage pipeline applied cleanly + operator-explicit decision row).
3. A new candidate file at `docs/wip/planning/_candidates/i-nn-research-first-as-strategic-posture.md` IF the promotion is deferred per gate-criteria not yet met.
4. OR a successor decision row D-IH-86-EU2 (or later) ratifying the promotion at C2 IF the gate-criteria are met.

## Why this matters for Wave R+4 itself

Wave R+4 IS the first worked-example of the pipeline applied end-to-end at strategic-posture tier:

- **C1 (this commit)** — Ingest + Rate + Rank stages: 7-prong outwards research sweep absorbing industry practice + operator-named YouTube sources + Holistika internal precedent.
- **C2** — Govern stage: AUDIENCE_REGISTRY J-IN sub-personas + MARKETING_LIFECYCLE_TAXONOMY mint + MARKETING_AREA_M3_REDESIGN amendment, EACH grounded in C1 research findings cited in decision-row rationale.
- **C3** — Implement stage: MKTOPS_DISCIPLINE charter→active flip + 4 channel doctrines mint, EACH carrying research-grounded best-practices from C1.
- **C4** — Implement + Test stages: 4+1 investor briefs, EACH research-grounded in C1 + ratified via closing-loop test (validator + render-trail + brand-baseline drift sweep).
- **C5** — Iterate stage: KB integrity drain + finding-disposition + noise cleanup; informs next-wave research priorities.

If Wave R+4 ships cleanly across all 5 commits with research-grounding citations preserved in every governance decision, it becomes the **1st of 3 worked-examples** the promotion gates would require. Subsequent waves (e.g., Wave T or R+5 if a future engagement-class tranche applies the pipeline) become 2nd + 3rd worked-examples.

## The 6-sub-persona hypothesis as a worked example of why research-first matters

The operator's 2026-05-27 message named 6 investor sub-personas at the scope-lock gate. The temptation (and the assistant's first reflex at the scope-lock AskQuestion) was to ratify 6 as the authoritative N at C2 governance authoring time.

The operator's correction (2026-05-27 ratify response):

> *"option A because but as i said, research goes first because of those things, i really can't say 6 because i asked for a research for those things too. why would we have in those research if i can't use it to take decisions"*

The correction names the operationalisation of research-first: the 6-sub-persona hypothesis goes INTO C1 prong-C as a hypothesis to validate / amend / extend, and C2 acts on the research-validated answer (which might be 6, or 4, or 7, or a different decomposition entirely — e.g., a 2x3 matrix of "engagement-mode × decision-window"). The flex on 6 IS the demonstration that the org is research-based.

## Failure modes the pipeline protects against

1. **Opinion-grounded authoring.** An agent / role-owner authors a canonical based on intuition + prior precedent alone, without checking whether industry practice has evolved past Holistika's prior assumptions. Pipeline protection: stage 1 (ingest) gates authoring on external sweep; stage 2 (rate) prevents low-confidence sources from masquerading as load-bearing.
2. **Research-as-ornament.** An agent cites external research AFTER authoring to retrospectively justify a conclusion that was reached opinion-first. Pipeline protection: stage 4 (govern) requires citation chains that demonstrate research INFORMED the decision, not justified it.
3. **Research-as-procrastination.** An agent spends infinite cycles on research and never authors. Pipeline protection: stage 5 (implement) is a binding gate; the sweep ends at the C2 governance commit deadline.
4. **Ungoverned ingestion.** External research gets absorbed into Tier 1 WIP intelligence but never promoted to canonical or archived; the WIP folder grows unbounded. Pipeline protection: stage 4 (govern) MUST decide canonical-vs-WIP-vs-archive per finding.
5. **Implementation without test.** A canonical lands but never gets exercised against the outcome it predicted. Pipeline protection: stage 6 (test) ties to UAT discipline + closing-loop test contract.
6. **Tested but never iterated.** Wave closes with findings but next wave doesn't ingest those findings. Pipeline protection: stage 7 (iterate) ties to wave-close cadence + index-freshness sweeps.

## Pipeline cadence per work-class

| Work class | Pipeline application cadence | Authoritative rule |
|:---|:---|:---|
| Specialty canonical mint | Full 7-stage pipeline applied at mint commit | `akos-people-discipline-of-disciplines.mdc` + this doctrine |
| Cursor rule mint or amendment | Full 7-stage pipeline applied at mint / amendment commit | This doctrine + cursor-rule discipline |
| Closure UAT report | Stage 2-7 (research already absorbed at prior commits); stage 1 only if novel UAT pattern | `akos-uat-discipline.mdc` |
| Tranche execution | Stage 4-7 (research absorbed at tranche charter; tranche commits do govern → implement → test → iterate) | `akos-synthesis-before-tranche.mdc` |
| Engagement work | Stage 1-7 per engagement charter; counterparty research counts as stage 1 ingest | `akos-applied-research-discipline.mdc` + engagement-discipline charters |
| Bug-fix / hygiene commit | Stage 6 only (test the fix works) — pipeline overhead waived per scope | Existing chore-commit exemption |

## Cross-references

- `.cursor/rules/akos-applied-research-discipline.mdc` (RULE 1-3) — the discipline this pipeline operationalises end-to-end.
- `RESEARCH_HEAD_DISCIPLINE.md` — the canonical-tier carrier; promotion candidate.
- `HOLISTIKA_ORGANISING_DOCTRINE.md` — the People manifesto; R&D-as-strategic-posture would slot into the manifesto's identity-statements.
- `RESEARCH_BACKLOG_TRELLO_REGISTRY.md` — the existing research-tracking infrastructure (already authored 2026; covers stages 1-3 for the Trello backlog surface).
- `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` — `pattern_research_first_pipeline` would be the new pattern row IF promotion happens at C2.
- D-IH-86-EU — Wave R+4 charter ratifying decision; surfaces this doctrine as a candidate promotion.
- D-IH-86-AU + D-IH-86-AS — parent fabric + UAT-discipline canonization decisions; ancestor lineage.

## Recommended next steps (C1 sweep)

1. Complete the 7-prong sweep per `README.md` file index.
2. Author `master-synthesis.md` 1-pager with the rollup + C2-governance-commit recommendations (including: ratify 6 sub-personas / amend to N / extend; ratify research-first promotion / defer to next wave / hold at current tier).
3. Surface the doctrine-promotion question as an explicit inline-ratify gate at C2 entry, with this file as the load-bearing evidence base.
