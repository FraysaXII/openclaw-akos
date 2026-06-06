---
title: People Design Pattern Library
language: en
intellectual_kind: people-canonical
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - People Operations Manager
  - Compliance Officer
last_review: 2026-05-16
last_review_by: People Operations Manager
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-C
  - D-IH-79-D
  - D-IH-80-B
  - D-IH-80-G
status: active
linked_csv: docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv
---

# People Design Pattern Library

This is the human-readable companion to [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv). The CSV is the machine-queryable single source of truth; this document is the narrative each pattern row resolves to.

People is the discipline of disciplines. It does not author the work of other areas; it authors the **patterns** other areas inherit when they do their own work. When a Marketing process and an Operations process and a Research process all reach for the same shape of register, the same shape of paired SOP-and-runbook, the same shape of drift gate — that shape lives here. Those areas read the pattern, instantiate it inside their own canonicals, and link back to the pattern row by `inherited_pattern_id` on `process_list.csv`.

The library exists for two reasons:

1. **Process singularity.** A new pattern is minted once, here, and propagates to every consuming area. Nobody reinvents the shape; nobody drifts away from the shape. When a process changes its parent pattern, every consuming area's row updates.
2. **Knowledge scalability.** A new collaborator can read the patterns and understand how Holistika thinks, without having to read every register, every SOP, and every Cursor rule. The patterns are the architectural layer; the instances are the implementation layer.

Each pattern below has a stable anchor (`#pattern-<slug>`). The CSV `pattern_md_anchor` column FKs into these anchors so the registry can deep-link from any consuming surface.

---

## How to read this library

Each pattern carries five fields you should always check before instantiating it:

- **What it is** — one paragraph explaining the shape.
- **When to reach for it** — the trigger condition that says "this pattern fits".
- **What it gives you** — the mechanical surface (files / validators / runbook) and the human surface (SOP / narrative).
- **How to instantiate it** — the minimum viable rows or files an area writes to inherit the pattern.
- **What it does not do** — the deliberate scope boundary; what to reach for instead when the trigger does not fit.

A pattern row in the CSV that has no narrative section here is a drift signal. The jargon-scan validator does not catch that drift directly today; the human review at `last_review` cadence does.

---

## Pattern: Register dimension as CSV + Pydantic + validator + Supabase mirror {#pattern-register-csv-pydantic-validator-mirror}

**What it is.** A canonical register lives as four artefacts in lockstep: a CSV file under `canonicals/dimensions/`, a Pydantic SSOT model under `akos/hlk_<name>_csv.py`, a Python validator under `scripts/validate_<name>.py`, and a Supabase mirror migration under `supabase/migrations/`. The CSV is authored by humans; the Pydantic model is the row contract; the validator enforces the contract in CI; the mirror projects the rows into Postgres so consuming areas can query them.

**When to reach for it.** When a new dimension of governed data emerges that needs to be queryable across areas. Examples: personas, channels, skills, engagement models, design patterns. If the data is one-off or scoped to a single SOP, do not reach for this pattern.

**What it gives you.** The mechanical surface is the four-artefact shape. The human surface is the canonical CSV that any area can read by browsing `canonicals/dimensions/`. Drift between the four artefacts is mechanically caught by the validator.

**How to instantiate it.** Copy the most-recent register's four files and rename. Update the field tuple to match your columns. Update the validator to reference your Pydantic model. Mint a migration that projects the rows into a `compliance.<name>_mirror` table. Wire the validator into `validate_hlk.py` and the smoke profile into `verification-profiles.json`.

**What it does not do.** It does not classify. The classification axes (access_level, confidence_level, source_taxonomy) live in [Pattern: Classification lattice](#pattern-classification-lattice) and every register inherits them as columns or frontmatter rather than reinventing them.

---

## Pattern: Paired SOP and runbook {#pattern-paired-sop-runbook}

**What it is.** Every executable process registered in `process_list.csv` carries two artefacts: a Markdown SOP that a human (or an agent acting as a role owner) can read to perform the work, and an executable runbook (Python script under `scripts/`, YAML catalog entry, or workflow) that an agent can fire unattended. The pair is the single source of truth for the process; neither artefact supersedes the other.

**When to reach for it.** Whenever a process is added to `process_list.csv` with a `cadence` column value. If the process can run on a schedule, on demand, on event, or behind an operator gate, it qualifies.

**What it gives you.** Acceptance criteria split into two columns: `acceptance_criteria_human` (a person can run via the SOP) and `acceptance_criteria_automation` (the runbook fires unattended). The dual surface guarantees the process is not locked into either AI-only or human-only execution.

**How to instantiate it.** Author the SOP under `<area>/<role>/canonicals/SOP-<purpose>_<NNN>.md` to the standard SOP shape (Purpose / Scope / Inputs / Steps / Outputs / Failure modes / Cross-references). Author the runbook under `scripts/<purpose>.py` per the standard Python contract. Cross-link both. Add the row to `process_list.csv` with both AC columns populated.

**What it does not do.** It does not classify the cadence. The cadence taxonomy is `on_demand`, `scheduled`, `event_triggered`, `gated_operator`, defined in the executable process catalog rule.

---

## Pattern: Engagement model taxonomy {#pattern-engagement-model-taxonomy}

**What it is.** Every working relationship Holistika enters with a person — internal hire, external hourly consultant, milestone consultant, percentage collaborator, apprentice learner, investor advisor, outsourced helper, operator self — is classified into one of seven engagement classes. Each class carries a fixed posture across four axes: retribution pattern, SOC posture, IP clause class, and knowledge access level. Onboarding and offboarding are also fixed per class.

**When to reach for it.** Whenever a new collaborator scenario surfaces and a question of "how do we engage them?" arises. The seven classes cover the full space; if a scenario does not fit, the question is "which class is closest, and what is the deviation?" not "do we mint a new class?"

**What it gives you.** A canonical posture per class so onboarding is mechanical. A SOC posture by default so security review is fast. An IP clause class by default so legal templates are pre-aligned. A knowledge access level so the knowledge base reveals only the cleared scope.

**How to instantiate it.** Read the engagement model registry. Pick the class that fits the new scenario. Apply the four axes by default; deviate only with explicit operator approval encoded in the engagement record.

**What it does not do.** It does not encode the per-engagement contract. The engagement registry (a sibling dimension) holds the per-engagement record; the model registry holds the class.

---

## Pattern: Persona registry {#pattern-persona-registry}

**What it is.** Every named persona Holistika encounters as part of any area's work — customer persona, advisor persona, investor persona, recruiter persona, regulator persona, partner persona — is registered in `PERSONA_REGISTRY.csv`. Each row carries the persona's role, decision authority, evidence appetite, and trust posture.

**When to reach for it.** Whenever a process needs to address a named class of stakeholder and that class will recur across more than one engagement. If the persona is one-off, do not register it.

**What it gives you.** A queryable cross-area dimension that any process can FK against. A shared vocabulary so Marketing and Research and Operations refer to the same persona by the same `persona_id`.

**How to instantiate it.** Add a row. Wire it into the consuming process via `persona_id` FK.

**What it does not do.** It does not encode the engagement with the persona. That is the `ENGAGEMENT_REGISTRY` (per-engagement) or `INTELLIGENCEOPS_REGISTER` (per-intelligence-collection-contract).

---

## Pattern: IntelligenceOps register {#pattern-intelligenceops-register}

**What it is.** Every contract Holistika has to collect intelligence on a named target — regulator, media outlet, recruiter, competitor — is registered in `INTELLIGENCEOPS_REGISTER.csv` with a target class, a contracted lifecycle, and an owning role.

**When to reach for it.** When a research or compliance process needs to commit to a structured discovery activity against a named target. Distinct from one-off lookups; this is the contract surface.

**What it gives you.** A target_class enum that is extensible by adding rows. A lifecycle stage so the process knows where the contract is in its arc.

**How to instantiate it.** Add a row. Wire it into the consuming research SOP via `target_id` FK.

**What it does not do.** It does not capture the persona of the target person. That is `PERSONA_REGISTRY`. The two registers are siblings, not parent-child.

---

## Pattern: Normalized adapter {#pattern-normalized-adapter}

**What it is.** Every external integration — CRM, billing, email, contract, scheduling, attribution, communication, file storage — is registered in a per-category adapter registry. Each row carries a status (active / inactive / planned / deprecated / experimental), a Data Owner role, and an invocation cadence. Multiple adapters of the same category coexist; the consuming process picks the active one or the one declared per engagement.

**When to reach for it.** Whenever a new external system is wired up. If only one vendor will ever be considered, the pattern still applies; you simply have one row at status `active` and zero at status `planned`.

**What it gives you.** A status enum that surfaces operator + agent decision-making about which adapter to invoke. A cadence taxonomy that classifies how the adapter fires. A Data Owner FK so accountability is clear.

**How to instantiate it.** Mint a per-category adapter registry under the consuming area's `canonicals/dimensions/`. Populate rows for every adapter (active and planned). Wire into the consuming process via `adapter_id` FK.

**What it does not do.** It does not own the integration code. The integration code lives under the consuming area's runbook or under a Tech Lab service shim; the adapter row is the metadata pointer.

---

## Pattern: Classification lattice {#pattern-classification-lattice}

**What it is.** Every artefact Holistika produces — register row, SOP, decision, plan, brief — carries three classification axes: `access_level` (0..6), `confidence_level` (A1..F6 per source-grading), `source_taxonomy` (a small enum of source classes). Together these form a lattice: a queryable position for the artefact in Holistika's information graph.

**When to reach for it.** Always. Every new canonical inherits the lattice as frontmatter or as columns. Every register row inherits it. Every SOP inherits it.

**What it gives you.** A standardised way to ask "who can see this?" (access_level), "how confident are we?" (confidence_level), "where did the input come from?" (source_taxonomy). The three axes compose so a single artefact carries a unique three-coordinate position.

**How to instantiate it.** Add the three frontmatter rows to the new canonical or the three columns to the new register. Use the canonical enums; do not invent new values.

**What it does not do.** It does not grade reliability automatically. The grader is a human; the canonical lattice is the vocabulary the human uses.

---

## Pattern: Dual register internal and external {#pattern-dual-register-internal-external}

**What it is.** Some canonicals come in twin form: an internal canonical that uses the discipline's full vocabulary (e.g., research methodology language, intelligence tradecraft language, organising-doctrine language), and an external canonical that translates the same content into language the audience reads as professional and clear. The pair is locked together; one cannot drift from the other.

**When to reach for it.** When the same content needs to reach both an internal audience (operator + cleared collaborator + agent) and an external audience (client / investor / advisor / regulator / partner). If only one audience consumes the content, do not split.

**What it gives you.** Two artefacts that say the same thing in two registers. A drift gate that mechanically catches when the internal vocabulary leaks into the external surface. A translation table the agent uses when generating prose.

**How to instantiate it.** Author the internal canonical first. Author the external canonical second. Author the translation table third. Wire a drift validator that scans the external surface for forbidden internal tokens.

**What it does not do.** It does not require both canonicals at the same access_level. The internal canonical typically sits at access_level 5 or 6; the external canonical sits at 1 or 2.

---

## Pattern: Drift gate validator {#pattern-drift-gate-validator}

**What it is.** A canonical surface is guarded by a Python validator that scans for forbidden tokens, schema violations, FK breaks, or cross-reference drift. The validator runs in CI as part of the `pre_commit` profile and fails the commit when the surface drifts.

**When to reach for it.** When a canonical carries a contract that is hard to enforce by review alone. Examples: an external surface must not carry internal vocabulary; a register must not have stale FKs; a manifest's paths must resolve.

**What it gives you.** Mechanical enforcement of the contract. A clear failure mode that is fast to diagnose: scan output names the file, line, and forbidden token.

**How to instantiate it.** Author the validator under `scripts/validate_<surface>_drift.py`. Enumerate the forbidden tokens or shape rules. Wire the validator into `verification-profiles.json` and the `pre_commit` profile.

**What it does not do.** It does not author the surface. It enforces a property of the surface.

---

## Pattern: Inline ratify via AskQuestion {#pattern-inline-ratify-via-askquestion}

**What it is.** When an execution-time decision requires operator input — evidence-dependent decision, spot-check decision, choice between candidate values — the agent asks via an inline question with structured options in the same chat session, instead of stopping and writing a pause record file. The operator answers; the agent continues.

**When to reach for it.** Whenever the decision is evidence-dependent (the agent must do work first, then surface options) or spot-check (the operator just confirms a generated artefact looks right). Not for canonical-CSV gates, trademark filings, or public-prose publishing — those use real-stop pauses with pause record files.

**What it gives you.** A faster operator loop. Decisions are made in the chat where the work happens, not in a follow-up review session.

**How to instantiate it.** When the agent reaches a ratification gate, run the prerequisite evidence sweep; distil findings into ranked options with rationale; surface via inline question; continue when the operator answers.

**What it does not do.** It does not replace pause records for canonical-CSV gates. Those are non-skippable.

---

## Pattern: Cross-area breakthrough propagation {#pattern-cross-area-breakthrough-propagation}

**What it is.** When People mints a new pattern row in this very registry — or revises the shape of an existing pattern — the change must propagate to every consuming area listed in the pattern row's `consumer_areas` column. The propagation runs through a paired SOP plus runbook: the SOP is a notification template addressed to the consuming area's role owner; the runbook fires the announcement and tracks acknowledgement.

**When to reach for it.** Whenever a pattern row is added or revised. Also when an upstream pattern shifts in a way that consuming-area instances need to migrate.

**What it gives you.** A mechanical channel for People-as-discipline-of-disciplines to act. The areas know when a pattern moves; the pattern moves do not silently rot.

**How to instantiate it.** Author the SOP at `SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`. Author the runbook that fires the notifications. Wire the runbook into the People-side process_list row.

**What it does not do.** It does not author the consuming-area's instance migration. The consuming area owns the migration; the propagation is the trigger.

---

## Pattern: Plane, program, topic forward layout {#pattern-program-topic-layout}

**What it is.** Every canonical surface that grows with new programs, planes, or topics uses the same directory layout: `compliance/<plane>/<csv>` for plane-scoped CSV registers, `_assets/<plane>/<program_id>/<topic_id>/` for knowledge-management Output 1 manifests, `<role>/programs/<program_id>/` for role-owned program containers. The layout is the same across People, Marketing, Research, Operations.

**When to reach for it.** When a new program or topic is added that needs canonical home. Existing flat surfaces stay until a dedicated migration moves them; new surfaces land directly in the forward layout.

**What it gives you.** Predictable paths. An author or agent navigating to a new program knows where to look without having to discover ad-hoc placement.

**How to instantiate it.** Mint the directories under the standard prefixes. Add the program row to `PROGRAM_REGISTRY.csv` and the topic row to `TOPIC_REGISTRY.csv`. Wire the manifest's `paths.mermaid` slot.

**What it does not do.** It does not require a flat-to-forward migration of existing surfaces. Migration is a separate initiative.

---

## Pattern: SOP body and addendum split {#pattern-sop-addendum-split}

**What it is.** Every SOP that carries supporting documentation beyond what an executor needs to perform the work is split into two paired files: the body (`SOP-XYZ_001.md`) and the addendum (`SOP-XYZ_001.addendum.md`). The body is plain-language and habilitates the executor end-to-end with the relevant context they need to do the work — nothing more. The addendum carries the rest: cross-area jargon, validator names, mirror table details, system-owner audit material, scoring rubrics, integration postures, infrastructure dimensions. Both files live as discrete metadata rows; both are canonical SSOT for their layer.

**When to reach for it.** Whenever an SOP would otherwise carry technical jargon from another area in its main body. Each area speaks its own dialect: Data canonicals speak data, Tech Lab canonicals speak tech, Finance canonicals speak finance, People canonicals speak plain language because People is for people. The body stays in the executor's home dialect. Cross-area depth lives in the addendum. If the SOP body is fully self-sufficient and has no addendum-worthy content, do not split — single-file is the degenerate case of the pattern.

**What it gives you.** Two independently consumable artefacts. The body reads like the manifesto reads — clear, navigable, executor-empowering. The addendum carries everything an auditor or system-owner needs without intruding on the executor's reading path. Each file carries its own complete frontmatter (access_level, register, role_owner, classification, last_review, ssot, intellectual_kind), so knowledge management systems consume them as discrete rows without parsing markdown structure. Independent review cadences become possible — body annual or per-cadence, addendum per-major-event. Anti-jargon drift gates apply only to the body; the addendum is exempt by file-suffix convention. Access tier separation becomes mechanical at the data layer — body might mirror at one access policy, addendum at another.

**How to instantiate it.** Author the body at `<area>/<role>/canonicals/SOP-<purpose>_<NNN>.md` to the standard SOP shape (Purpose / Scope / Inputs / Steps / Outputs / Failure modes / Cross-references) in the executor's home dialect. Identify the supporting content that does not belong in the body using the rubric from `SOP-META_PROCESS_MGMT_001.md` §"Body and Addendum split": (1) does the executor need this to perform the action — body; (2) does this name a system, validator, mirror, or cross-area artifact the executor doesn't operate — addendum; (3) does this carry jargon from another area — addendum unless the executor's role natively spans both areas; (4) does this require auditor or system-owner context for compliance evidence — addendum; (5) could a new hire in the executor's role complete the SOP without this — addendum if yes. Author the addendum at `<area>/<role>/canonicals/SOP-<purpose>_<NNN>.addendum.md` with frontmatter that mirrors the body's where appropriate (same `methodology_version_at_review`) and diverges where appropriate (own `access_level`, own `last_review`, own `last_review_decision_id`). Cross-link both: the body's frontmatter lists the addendum as a companion; the addendum's frontmatter lists the body as the parent. Anti-jargon validators glob-exclude `*.addendum.md` from scope.

**What it does not do.** It does not replace the paired-SOP-runbook contract. That pattern (sibling: [Pattern: Paired SOP and runbook](#pattern-paired-sop-runbook)) is about executable artefacts — the SOP a human reads to perform the work and the runbook an agent fires unattended. The body and addendum split is about reader-audience layering at the documentation level — the executor body and the auditor or system-owner addendum. The two patterns compose: a process can have a paired SOP and runbook AND a body and addendum split on the SOP itself.

---

## Pattern: Area buildout meta-process {#pattern-area-buildout}

**What it is.** The People-minted meta-process for creating or maturing any
O5-1 area at comparable depth: a **14-component completeness bar**
(charter, processes, roles, capability rows, canonical coverage, paired
SOP+runbook, cursor rule+skill, Quality Fabric row, and
`inherited_pattern_id` on processes) scored by
`scripts/validate_area_completeness.py --matrix` across Data, Tech,
Finance, Marketing, Operations, People, and Research.

**When to use it.** Before an area CSV tranche, area charter mint, or I93
P8 harmonization sweep. People owns the pattern (`pattern_area_buildout`);
each area owns its charter and local canonicals.

**How to instantiate it.** Read
[`AREA_GOVERNANCE_DISCIPLINE.md`](AREA_GOVERNANCE_DISCIPLINE.md) §2,
walk the components manually (30–45 min), then run
`py scripts/validate_area_completeness.py --matrix` and disposition
`gap`/`partial` findings via inline-ratify before commit. Register the
area process with `inherited_pattern_id=pattern_area_buildout`.

**What it does not do.** It does not author the Data area charter (I93 P1).
It does not prove Supabase mirror parity at P0 (AREA-10 stays `skip` until
live mirror evidence is in scope).

---

## Maintenance

This library and the paired CSV are reviewed at least annually by Compliance Officer plus People Operations Manager. The `last_review` and `last_review_by` columns on the CSV reflect the latest review per pattern. When a pattern is added or revised, the cross-area breakthrough propagation pattern fires and the consuming areas receive notification.

When a pattern is deprecated, the row's `status` flips to `deprecated`; consuming-area instances are migrated to the successor pattern; the row stays in the registry as historical context.

When a pattern's shape changes mid-life (e.g., a new column is added to the register-as-CSV pattern), the change is recorded in the CSV's `notes` column with the relevant ratifying decision, and the narrative section here is updated to match.

---

## Cross-references

- [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) — machine-queryable single source of truth.
- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) — the People manifesto that frames why this library exists.
- [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md) — registers this library as a canonical asset.
- [`process_list.csv`](../Compliance/canonicals/process_list.csv) — `inherited_pattern_id` column FKs into this registry's `pattern_id` (Initiative 79 P6 schema extension).
