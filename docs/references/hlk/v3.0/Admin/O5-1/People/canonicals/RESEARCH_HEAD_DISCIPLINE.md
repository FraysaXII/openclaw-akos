---
title: Research Head Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-CO
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder (acting as Holistik Researcher / Research Area Head)
  - System Owner
co_authors:
  - People Operations Manager
  - KM Officer
last_review: 2026-05-19
last_review_by: Founder/CEO
last_review_at: 2026-05-19
last_review_decision_id: D-IH-86-RH-A
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-RH-A
  - D-IH-86-RH-B
  - D-IH-86-RH-C
  - D-IH-86-RH-D
  - D-IH-86-RH-E
  - D-IH-86-RH-F
  - D-IH-86-RH-G
  - D-IH-86-RH-H
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
  - ../../Research/canonicals/RESEARCH_AREA_CHARTER.md
  - ../../Research/Methodology/canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md
  - ../../Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md
  - ../Compliance/canonicals/source_taxonomy.md
  - ../Compliance/canonicals/confidence_levels.md
linked_cursor_rules:
  - .cursor/rules/akos-applied-research-discipline.mdc
linked_skills:
  - .cursor/skills/inline-ratify-craft/SKILL.md
companion_to:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../../Research/canonicals/RESEARCH_AREA_CHARTER.md
---

# Research Head Discipline

> The People-area pattern that names how the **Research Head** authors canonical
> doctrine, cursor rules, decision rows, and skills — research-first, by
> default, every time. Codified at I86 Wave H from the operator's framing:
> *"I literally single-handedly created everything you see here at Holistika
> by researching. I noted some of them but never had a proper governance nor
> continuity."* This canonical IS that governance and continuity.

## 1. Purpose

Holistika's canonical doctrine — every v3.0 area charter, every cursor rule,
every doctrine canonical, every load-bearing decision-register row — has been
authored single-handedly by the operator (acting as Research Area Head per
`baseline_organisation.csv` Holistik Researcher row L12) through a tacit
discipline of research-first authoring: read the repo state, sweep the
relevant industry precedent, distil to a structured option set, ratify, then
write. This canonical names that discipline so it survives two transitions:

1. **Continuity** — the operator's existing practice becomes legible to
   future-self-reading-cold and to collaborators who join the area.
2. **AIC continuity** (per [`i76-madeira-elevation.md`](../../../../../wip/planning/_candidates/i76-madeira-elevation.md))
   — when a future AIC acts as Research Head (or as Research-Head co-steward),
   the discipline transmits without operator re-explanation. AICs read this
   canonical as a doctrine and inherit the pattern.

The discipline is grounded in the industry consensus that **applied research,
properly industrialised, is a competitive moat** (per the Bell Labs / Xerox
PARC / OpenAI lineage — innovation is abundant; the differentiator is the
transformation velocity from research to commercialised governance). This
canonical industrialises Holistika's applied-research practice.

## 2. Scope (when this canonical fires)

This canonical fires whenever any of the following surfaces are authored
or revised:

- A net-new **canonical CSV** is minted (per `akos-holistika-operations.mdc`
  §"New git-canonical compliance registers" pattern).
- A net-new **doctrine canonical** is authored (any `.md` under
  `docs/references/hlk/v3.0/**/canonicals/` carrying `intellectual_kind:
  doctrine|area_charter|discipline_charter|people-canonical|
  research-area-canonical|tech-canonical|brand-canonical`).
- A net-new **cursor rule** is minted at `.cursor/rules/akos-*.mdc`.
- A net-new **skill** is minted at `.cursor/skills/*/SKILL.md`.
- A **decision-register row** is appended to `DECISION_REGISTER.csv` that
  carries `novel_framing: yes` (forward-charter field; not yet in schema).
- Any of the above is **revised** in a non-mechanical way (i.e., not a typo
  fix, not a link-rot fix, not a formatting normalisation).

This canonical does NOT fire for:

- Mechanical authoring (typo fixes, link-rot, formatting).
- Bugfix commits.
- Refactors of already-researched canonicals (when the underlying research
  base does not change).
- Per-engagement WIP synthesis (covered by Research/Intelligence discipline
  charters + Tier 1 WIP rules at `docs/wip/intelligence/`).
- Code-only changes that do not touch canonical doctrine.

When fired, the canonical guides the authoring through the 5-pillar discipline
below + the cursor rule [`akos-applied-research-discipline.mdc`](../../../../../../.cursor/rules/akos-applied-research-discipline.mdc)
mechanically enforces the minimum bar.

## 3. The 5 Research-Head pillars

Holistika-fit reduction of the ResearchOps Community 8 Pillars (Environment /
Scope / People / Organisational context / Recruitment&admin / Data&knowledge /
Governance / Tools&infrastructure — Kate Towsey + ResearchOps Community 2018):
Holistika's substrate already covers Environment, People, Tools, Recruitment
via existing canonicals (WORKSPACE_BLUEPRINT, baseline_organisation, agentic
substrate registry, engagement model registry), so the 5 pillars below name
the **operator-Research-Head-specific discipline** that does not collapse into
those existing canonicals.

### 3.1 Inventory — what does the corpus already say?

Before authoring anything new, the Research Head sweeps the existing corpus
to find what the repo already commits to. Concretely:

- `Grep` + `Glob` + `Read` over `docs/references/hlk/v3.0/**/canonicals/`
  for the topic being authored.
- `Read` of all `linked_canonicals` named in the closest sibling canonical's
  frontmatter (these are pre-curated entry points).
- `Read` of `DECISION_REGISTER.csv` for any prior ratification on the topic.
- `Read` of the relevant `process_list.csv` rows.
- `Read` of `docs/wip/intelligence/` for any in-flight synthesis on the topic.

The inventory pass is **non-negotiable** — it is the Research Head equivalent
of the inline-ratify-craft Principle 1 "Run the evidence sweep first"
(`.cursor/skills/inline-ratify-craft/SKILL.md`).

Outcome: a short Inventory paragraph in the planning notes (or the canonical's
forward Evidence-base section) naming what the corpus already commits to,
what's deliberately silent, and what would conflict if the new authoring goes
forward as drafted. The Inventory pass typically collapses 2-3 plausible
authoring directions into 1 obvious one (per inline-ratify-craft Principle 1
quantitative claim).

### 3.2 Sourcing — what does the industry already say?

When the inventory surfaces a novel framing (something the repo does not
yet commit to), the Research Head opens a sourcing pass against external
industry precedent. Concretely:

- 3-10 `WebSearch` queries on the topic, scoped to the year the decision is
  being made (2026 today; future-dated for AIC continuity).
- 1-5 `WebFetch` calls on the most authoritative sources surfaced.
- Optional: targeted reads of named precedent documents (DAMA-DMBOK 3.0,
  ResearchOps Community publications, Kate Towsey *Research That Scales*,
  Allyson Berri's writing, McKinsey / Bain / DT consulting taxonomies, etc.).

The sourcing pass is **conditional on novelty** — if the inventory pass
already converged on an obvious authoring direction, sourcing can be light
(1-2 confirmatory queries). If the inventory surfaced genuine novelty,
sourcing is heavier (5-10 queries, multiple precedent sources).

Outcome: a Sourcing paragraph naming what the industry consensus is, where
Holistika converges with it, where Holistika diverges and why. The
divergence narrative is the load-bearing claim — when Holistika diverges
from industry consensus, the canonical names the divergence + the rationale
+ the conditions under which the divergence might be revisited.

### 3.3 Synthesis — what is Holistika's lived position?

Inventory + Sourcing feed Synthesis. Synthesis is the act of distilling:

- The corpus's pre-existing commitments (Inventory).
- The industry's precedent + best practice (Sourcing).
- The operator's lived experience and tacit knowledge (Founder corpus
  per `FOUNDER_CORPUS_INVENTORY` section paths; AIC inheritors read this
  FK-only per `D-IH-76-K` access posture).
- The engagement-as-org-diagnostic feedback loop (per
  [`DIAGNOSIS_DISCIPLINE_CHARTER.md`](../../Research/Diagnosis/canonicals/DIAGNOSIS_DISCIPLINE_CHARTER.md)
  §4 — every customer engagement stress-tests Holistika's own governance).

Into a **single Holistika-position statement** that the new canonical /
rule / skill / decision codifies. The Synthesis position is the canonical's
load-bearing claim — its `intellectual_kind: doctrine` core.

Synthesis output: the canonical's body itself; the cursor rule's body itself;
the skill's principles; or the decision-register row's rationale. The
Inventory + Sourcing passes' outputs are preserved in the canonical's
**Evidence base** section per §6 Backfill protocol below.

### 3.4 Governance — provenance, classification, access

Every research-backed claim in a Holistika canonical carries provenance
metadata so future readers (and validators) can audit the claim. Concretely:

- **`source_taxonomy`** annotation per claim (FK into
  [`source_taxonomy.md`](../Compliance/canonicals/source_taxonomy.md)):
  HUMINT / OSINT / internal-doctrine / vendor-doc / academic-paper /
  industry-publication / regulatory-text / etc.
- **`confidence_level`** annotation per claim (FK into
  [`confidence_levels.md`](../Compliance/canonicals/confidence_levels.md)):
  A1-F6 reliability + confidence scale.
- **`access_level`** annotation per canonical (FK into
  [`access_levels.md`](../Compliance/canonicals/access_levels.md)):
  the source-reading clearance required to verify the claim.
- **Audit URL or repo-path citation** per external source: every external
  source surfaces as a citeable URL (or repo-path if Holistika-internal).

This pillar inherits DAMA-DMBOK 3.0 Metadata Management semantics + Holistika's
existing source / confidence / access compliance canonicals. No new schema —
the existing compliance scaffolding is the surface.

### 3.5 Propagation — does the new claim trigger sister-canonical revision?

When a new canonical / rule / skill / decision lands, the Research Head
asks: does this trigger revision elsewhere? Concretely:

- Does a sibling canonical now carry a claim that contradicts the new one?
  (If so, surface as inline-ratify gate per
  [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc).)
- Does a cross-area canonical now need to cite the new one as `linked_canonicals`
  in its frontmatter? (If so, mint the cross-link in the same commit batch.)
- Does the cross-area breakthrough propagation SOP need to fire? (Per
  [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md)
  — applies when the new claim is itself a People pattern that other areas
  inherit.)
- Does the substrate-audit cadence need an off-cycle update? (Per
  [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](../../Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md)
  — applies when the new claim materially changes substrate posture.)

The propagation pillar is what distinguishes research-first authoring from
research-as-citation-decoration: research-first claims **change the
sibling-canonical surface**; decoration claims do not. If the new claim does
not propagate, the Research Head asks whether the claim is load-bearing or
ornamental — load-bearing claims propagate by construction; ornamental
claims are anti-pattern (§7 below).

## 4. Internal-research checklist (the inventory pass operationalised)

When opening a research-first authoring session, the Research Head walks this
checklist:

1. **Closest sibling canonical**: identify the existing canonical(s) in the
   same area + adjacent areas whose scope is closest to the new authoring.
   Read it / them fully.
2. **Linked canonicals**: read every canonical named in the sibling's
   `linked_canonicals` frontmatter.
3. **Decision-register lineage**: `grep` `DECISION_REGISTER.csv` for the topic
   + adjacent decision IDs; read the relevant rows.
4. **Process_list rows**: `grep` `process_list.csv` for the relevant area + topic.
5. **Baseline_organisation rows**: `grep` `baseline_organisation.csv` for the
   relevant role(s).
6. **Cursor rules**: `Glob .cursor/rules/akos-*.mdc` and read those whose names
   surface in the topic space.
7. **Skills**: `Glob .cursor/skills/*/SKILL.md` and read those relevant.
8. **WIP synthesis**: `Glob docs/wip/intelligence/**/*.md` for any in-flight
   work on the topic.
9. **Planning history**: `Glob docs/wip/planning/**/master-roadmap.md` for any
   initiative-level prior treatment.
10. **CHANGELOG**: `grep` CHANGELOG.md for the topic — what's already shipped.

This checklist is the operationalisation of pillar §3.1 Inventory. The output
is captured in the Inventory paragraph of the planning notes or the canonical's
Evidence-base section (§6).

## 5. External-research checklist (the sourcing pass operationalised)

When the inventory pass surfaces a novel framing, the Research Head walks the
external checklist:

1. **WebSearch with year-scoping**: 3-10 queries; always include the year
   (current = 2026) to filter for current consensus. Avoid pre-2024 searches
   when the topic is fast-moving (AI / agentic / ResearchOps tooling).
2. **WebFetch authoritative sources**: 1-5 fetches of the top results from
   WebSearch; prefer first-party (vendor docs, standard bodies, named
   practitioners) over second-party.
3. **Named precedent corpus**: read the relevant chapter / section of any
   standard reference (DAMA-DMBOK 3.0; ResearchOps Community publications;
   Kate Towsey *Research That Scales*; McKinsey / Bain / Deloitte / KPMG /
   Forrester / Gartner / IDC industry analyst notes; academic papers via
   arXiv / Google Scholar for technical claims).
4. **Citation discipline**: every external source surfaced is cited inline
   in the canonical's Evidence-base section with URL + retrieval date + a
   one-clause summary of the relevance.
5. **Divergence narrative**: when Holistika's drafted position diverges from
   the industry consensus, the canonical names the divergence + the rationale
   + the conditions under which it might be revisited. Divergence-without-
   rationale is the most-common research-as-ornament failure mode (§7).

## 6. Backfill protocol — Evidence-base section on existing canonicals

When revising an existing canonical that was authored before this discipline
was codified, the Research Head opens an Evidence-base section (frontmatter
slot + body section):

**Frontmatter slot** (added on revision):

```yaml
evidence_base:
  internal_sources:
    - path: <repo-relative path>
      relevance: <one-clause summary>
  external_sources:
    - url: <https://...>
      retrieved: YYYY-MM-DD
      relevance: <one-clause summary>
  inventory_pass_completed: YYYY-MM-DD
  sourcing_pass_completed: YYYY-MM-DD
  research_head: <name or role e.g. "Founder (acting as Holistik Researcher)">
```

**Body section** (added at end of canonical, before final `## Cross-references`):

```markdown
## Evidence base

This canonical's load-bearing claims are grounded in the following sources
(per the Research Head Discipline §6 Backfill protocol).

### Internal sources
- [`path/to/canonical.md`](path/to/canonical.md) — <one-clause>
- ...

### External sources
- [Source title](URL) (retrieved YYYY-MM-DD) — <one-clause>
- ...

### Provenance
- Inventory pass: YYYY-MM-DD by <role>
- Sourcing pass: YYYY-MM-DD by <role>
- Synthesis: this canonical body
- Last review: see frontmatter
```

The Evidence-base structure is **append-only by default** — revisions add
sources rather than rewriting. Removals are governance events that surface
in the decision register.

Backfill priority order (per §4 per-area gap analysis):

1. `Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md` (currently 0 research mentions).
2. `Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md` (link to SUBSTRATE_REGISTRY audit_source_url).
3. `Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md` (HUMINT tradecraft grounding made explicit).
4. `People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md` (Research-as-pillar mention upgraded from footnote).
5. `Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md` (DAMA-DMBOK 3.0 alignment posture).

Backfill is incremental, not big-bang. One canonical per wave is sustainable.

## 7. Anti-patterns

The Research Head Discipline is unforgiving on four anti-patterns:

### 7.1 Research-as-ornament

Citing a source that does not actually load-bear on the canonical's claims —
"according to McKinsey, X is important" without naming what McKinsey actually
said about X or how Holistika's claim relates. Anti-pattern because it
trains future readers to ignore citations as decoration.

Counter-test: remove the citation. Does the canonical's claim weaken? If no,
the citation was ornament. Remove it.

### 7.2 Research-after-the-fact-to-justify

Authoring a position from operator intuition + then sweeping the industry to
find supporting citations + adding them as if they motivated the position.
Anti-pattern because it inverts the discipline (justification → research)
which produces selection bias.

Counter-test: would the operator's position have changed had the sourcing
pass surfaced contradicting evidence? If no (i.e., the position was always
going to be ratified regardless), the sourcing was theater. Either the
position is genuinely operator-tacit-knowledge-derived (in which case name
that explicitly + skip sourcing claim) or surface the contradicting evidence
and address it.

### 7.3 Research-as-procrastination

Extending the inventory + sourcing passes indefinitely to defer the synthesis
write-up. Anti-pattern because perfect is the enemy of done; Holistika
canonicals are revisable (see Backfill protocol §6) — version 1 with thin
sourcing is more valuable than version 0 with planned-deep sourcing.

Counter-test: has the inventory pass converged on a stable picture (no new
sweep adds material claims)? If yes, write the synthesis. Has the sourcing
pass surfaced the dominant industry-consensus position + the major dissenting
positions? If yes, write the synthesis. Do not chase exhaustiveness.

### 7.4 Copy-paste-citations

Citing the same source across many canonicals without re-reading it on each
cite. Anti-pattern because cited claims drift from what the source actually
says as the citing canonicals proliferate.

Counter-test: when a source is cited for the third time, re-read the relevant
section of the source. Does the cite still hold? If yes, continue. If not,
correct all three cites in the same commit batch.

## 8. Cross-references

- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) §2
  (People is the discipline of disciplines) — the parent doctrine this
  canonical inherits from.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) — agentic
  is a discipline of disciplines, recursive; this canonical is the recursive
  application to research-first authoring.
- [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) —
  the human-readable pattern hub; a `research_first_canonical_authoring`
  pattern row should be added in a future People design pattern tranche
  (forward-charter C-NN-B).
- [`../../Research/canonicals/RESEARCH_AREA_CHARTER.md`](../../Research/canonicals/RESEARCH_AREA_CHARTER.md) —
  the Research area's 4-discipline charter; this canonical names the
  meta-discipline that operates above the four (the Research Head's
  doctrine-author discipline).
- [`../../Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) —
  the discipline-of-disciplines-applied-to-Research precedent
  (D-IH-84-G); this canonical extends the pattern from substrate audit
  to general canonical authoring.
- [`.cursor/rules/akos-applied-research-discipline.mdc`](../../../../../../.cursor/rules/akos-applied-research-discipline.mdc) —
  the always-applied cursor rule that mechanically enforces this discipline.
- [`.cursor/skills/inline-ratify-craft/SKILL.md`](../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md)
  Principle 1.5 — the skill extension that distinguishes evidence-sweep
  from research-sweep.
- [`.cursor/rules/akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) —
  the always-applied People rule that justifies this canonical's home in
  People (People mints patterns; Research authors processes from those
  patterns).
- ResearchOps Community 8 Pillars (https://researchops.community/about/) —
  industry-precedent for the discipline shape.
- Kate Towsey, *Research That Scales: The Research Operations Handbook*
  (Rosenfeld Media, 2024) — book canonicalisation of ResearchOps.
- D-IH-86-RH-A through D-IH-86-RH-H in `DECISION_REGISTER.csv`
  (operator blanket-ratified 2026-05-19 per Lane D Wave H sweep + design
  report recommended defaults).
