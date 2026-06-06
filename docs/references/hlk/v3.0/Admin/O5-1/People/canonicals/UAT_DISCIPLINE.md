---
title: UAT Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
  - System Owner
co_authors:
  - PMO
  - People Operations Manager
last_review: 2026-05-24
last_review_by: PMO
last_review_at: 2026-05-24
last_review_decision_id: D-IH-86-CW
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-AV
  - D-IH-86-AS
  - D-IH-86-CW
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - RESEARCH_HEAD_DISCIPLINE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - SOP-PEOPLE_UAT_GOVERNANCE_001.md
  - SOP-PEOPLE_UAT_GOVERNANCE_001.addendum.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv
  - ../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - ../../Marketing/Brand/canonicals/dimensions/FIGMA_FILES_REGISTRY.csv
linked_runbooks:
  - scripts/validate_uat_report.py
linked_cursor_rules:
  - .cursor/rules/akos-uat-discipline.mdc
  - .cursor/rules/akos-planning-traceability.mdc
  - .cursor/rules/akos-quality-fabric.mdc
  - .cursor/rules/akos-external-render-discipline.mdc
  - .cursor/rules/akos-brand-baseline-reality.mdc
  - .cursor/rules/akos-applied-research-discipline.mdc
  - .cursor/rules/akos-people-discipline-of-disciplines.mdc
linked_skills:
  - .cursor/skills/uat-discipline-craft/SKILL.md
  - .cursor/skills/inline-ratify-craft/SKILL.md
  - .cursor/skills/external-render-craft/SKILL.md
  - .cursor/skills/impeccable/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
  - RESEARCH_HEAD_DISCIPLINE.md
  - SOP-PEOPLE_UAT_GOVERNANCE_001.md
forward_charters:
  - 3-wave field-test window monitoring obligation (Wave S + Wave T + Wave U closes); see field_test_window block below; revocation path in SOP-PEOPLE_UAT_GOVERNANCE_001.addendum.md §Field-test window revocation procedure
field_test_window:
  open_date: 2026-05-24
  open_decision_id: D-IH-86-CW
  open_wave: R+1
  close_target_wave: U
  close_target_date_estimate: 2026-06-14
  revocation_decision_id_template: D-IH-86-CW-revoke
  monitoring_obligation_owner: PMO
  monitoring_obligation_co_owner: AIC role_owner
  promotion_criteria:
    - code: FTW-UAT-01-THREE-CLOSURE-UATS
      statement: ">= 3 closure-UAT reports authored under the new bar across Waves S, T, U with verdict in PASS / PASS-WITH-FOLLOWUP and all 11 sections + mandatory frontmatter fields present."
    - code: FTW-UAT-02-FAIL-CEILING
      statement: "<= 2 cumulative validator FAIL findings across the 3 reports (after disposition + amendment commits land)."
    - code: FTW-UAT-03-NO-VALIDATOR-MISFIRES
      statement: "0 false-positive findings requiring accept-as-canon disposition for structural validator regex misfire (RULE 5 option 4 used exclusively for genuine validator/canonical schema drift, never to paper over a draft that forgot a section)."
    - code: FTW-UAT-04-PWF-RATIONALE-COMPLIANCE
      statement: "0 RULE-3 PWF-without-rationale findings on Waves S/T/U reports (the bar self-proves via the Wave R UAT amendment landing first, in the same commit-window as this promotion, as the canonical worked-example for the 12th/13th specialty enforcement)."
  revocation_triggers:
    - code: FTW-UAT-RT-01-VALIDATOR-MISFIRE
      statement: ">= 1 validator false-positive requiring structural regex amendment in < 3 waves (signal that the regex set is too strict / brittle; specialty needs re-grounding against more real-report variance)."
    - code: FTW-UAT-RT-02-PWF-DISCIPLINE-NOT-SINKING
      statement: ">= 2 RULE-3 PWF-without-rationale findings on Waves S/T/U reports (signal that PWF discipline is not sinking in across agent + operator authoring practice; 12th specialty needs revision or the 13th sibling specialty D-IH-86-CX needs sharpening)."
    - code: FTW-UAT-RT-03-OPERATOR-EXPLICIT
      statement: "Operator-explicit revocation (any wave, any reason; honored verbatim per operator-explicit override per akos-inline-ratification.mdc §Time-box recovery escape)."
  status: open
  last_observation_wave: null
  last_observation_date: null
  last_observation_summary: null
---

# UAT Discipline

> The People-area canonical that names how Holistika **verifies** every shipped
> artifact against its quality bar. First specialty instantiation of
> [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) (per D-IH-86-AV);
> codifies `compose_UAT(audience, channel, scenario, brand, governance)` →
> seven-class UAT shape.

## 1. Purpose

UAT in Holistika is not a single activity. It is a family of seven distinct
classes — closure / brand / send / render / regression / persona / deploy —
each with its own audience, evidence shape, and governance gate. The
discipline names the seven classes, the rule for picking which class fires
on a given artifact, and the bar each class must clear.

Codified at I86 Wave J (2026-05-20) from operator framing earlier the same
day:

> *"Visually the UAT is lacking. Technically the UAT is lacking because
> I don't know if you know but your push to main failed in @Vercel. I
> don't know if from the MKT/Tech side of things our UAT holds. Is figma
> involved in these processes or should it be? Is the UAT properly
> governed?"*

The four operator concerns map cleanly to the seven classes:

| Operator concern | Materialises as |
|:---|:---|
| Visually lacking | **Brand-class UAT** + **render-class UAT** §3.2 + §3.4 |
| Vercel deploy regression | **Deploy-class UAT** §3.7 (NEW; motivated by today's `ec3f883` evidence) |
| MKT/Tech holds the bar | **Cross-area inheritance contract** §6 |
| Properly governed | **Compose_UAT rule** §4 + **paired SOP + runbook** forward-charter |

## 2. Scope

This canonical applies to:

- Closure UAT for any initiative meeting the qualifying conditions in
  [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc)
  §"UAT quality bar" (≥ 5 phases OR canonical-CSV touch OR sibling-repo
  work OR I86 cluster sibling).
- Brand-touching artifacts (deck slides, dossiers, web pages, email
  bodies) → brand-class UAT.
- External-delivery artifacts (anything tagged `audience: J-IN | J-CU |
  J-PT | J-AD | J-ENISA | J-RC | J-CO`) → render-class UAT + send-class
  UAT.
- Sibling-repo deploys (`hlk-erp` / `boilerplate` / `kirbe-platform`) →
  deploy-class UAT.
- Persona / scenario evidence rollups (per I47 + MADEIRA quality
  evaluation) → persona-class UAT.
- Regression sweeps (validator suites + smoke tests + integration tests)
  → regression-class UAT.

It does **not** apply to:

- Code-only refactors with no human-facing surface change (regression-class
  validation suffices; closure UAT not required).
- Internal scratchwork (operator-scratchpad entries; agent
  self-checkpoints; debugging notes).
- Test fixtures and ephemeral artifacts.

## 3. The seven UAT classes

Each class has: a **trigger** (when it fires), a **bar** (what it must
demonstrate), an **internal precedent** (where the pattern was established),
and an **owning canonical** (which file or rule materialises the bar).

### 3.1 Closure-class UAT

**Trigger.** End-of-initiative gate; closing INITIATIVE_REGISTRY status
flip from `active` to `closed`. Required for any initiative ≥ 5 phases
OR with canonical-CSV touch OR shipping sibling-repo work.

**Bar.** Mandatory frontmatter (`verdict` / `closure_decision_source` /
`ratifying_decisions` / `linked_runbooks` / `verdict_history`). Mandatory
sections: §1 closure-criteria verification table; §2 mechanical evidence
with reproducible commands; §3 (when in scope) browser-evidence
audit-trail with screenshot + sha256 + accessibility snapshot at
decision points; §4-§9 per-dimension findings; §10 7-item operator
sign-off checklist. Per-row Target / Actual columns. PASS rows carry
reproducible command in plain text.

**Internal precedent.** [`uat-i87-closure-2026-05-19.md`](../../../../../wip/planning/87-openclaw-operator-runtime-hardening/reports/uat-i87-closure-2026-05-19.md)
+ [`uat-i85-closure-2026-05-19.md`](../../../../../wip/planning/85-audience-tag-canonicalization/reports/uat-i85-closure-2026-05-19.md).

**Owning canonical.** [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc)
§"UAT quality bar" + [`docs/wip/planning/_templates/uat-closure-template.md`](../../../../../wip/planning/_templates/uat-closure-template.md).

### 3.2 Brand-class UAT

**Trigger.** Any artifact touching brand identity (dossier prose, deck
slide bodies, web page bodies, email bodies, dashboard chrome,
identity assets like favicon / logo / typography). Fires whenever
brand-axis is non-default in the Quality Fabric compose() rule.

**Bar.** Per-surface findings table with three sub-axes:
- **Visual identity** (typography / spacing / colour / hierarchy
  conformance to design system; resolved against Figma source-of-truth
  when one exists in [`FIGMA_FILES_REGISTRY.csv`](../../../../Marketing/Brand/canonicals/dimensions/FIGMA_FILES_REGISTRY.csv)).
- **Voice** (DO / DON'T traits per [`BRAND_DO_DONT.md`](../../../../Marketing/Brand/canonicals/BRAND_DO_DONT.md);
  dual-register CORPINT-internal-vs-external per
  [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md)
  enforced by `validate_brand_baseline_reality_drift.py`).
- **Anti-jargon** (forbidden token list per
  `akos-people-discipline-of-disciplines.mdc` RULE 4 when surface is
  People-canonical-class).

**Internal precedent.** [`uat-impeccable-all-surfaces-2026-05-16.md`](../../../../../wip/planning/77-impeccable-brand-bridge-refresh/reports/uat-impeccable-all-surfaces-2026-05-16.md).

**Owning canonical.** [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc)
+ [`docs/wip/planning/_templates/uat-impeccable-template.md`](../../../../../wip/planning/_templates/uat-impeccable-template.md).

### 3.3 Send-class UAT

**Trigger.** Any external send (advisor handoff packs, ENISA dossier
sends, investor cover emails, customer outreach, partner pitches).
Fires whenever channel-axis maps to a send mechanism (mail / portal /
ERP record).

**Bar.** Pre-send: render-trail validated (per
`akos-external-render-discipline.mdc` RULE 4 heuristics). At-send:
sha256 manifest emitted (source + render hashes); SMTP message-ID
captured; envelope sender + recipient logged. Post-send: receipt
confirmation (where channel supports it); follow-up cadence row in
ops-register when human follow-up expected.

**Internal precedent.** [`docs/references/hlk/v3.0/_assets/advops/`](../../../../_assets/advops/)
adviser-handoff send pattern (per I24); ENISA dossier send pattern
(per I28).

**Owning canonical.** This canonical §3.3 + `akos-adviser-engagement.mdc`
+ `akos-external-render-discipline.mdc`.

### 3.4 Render-class UAT

**Trigger.** Any external-audience artifact requires render parity
(PDF / Web / ERP / Mail / Slide / Broadcast per
`akos-external-render-discipline.mdc` RULE 1 six-surface enum). Fires
whenever audience-axis is non-J-OP and non-J-AIC.

**Bar.** Render heuristic satisfied per RULE 4 (PDF + manifest, Web URL,
ERP record id, Mail rendered body, Slide deck export, Broadcast
registered URL). Manifest sha256 present. Render-pending tracker entry
filed if render parity not yet reached. Quality of the rendered
artifact verified against brand-class UAT bar (§3.2 inherits here).

**Internal precedent.** [`uat-render-quality-2026-05-19.md`](../../../../../wip/planning/86-initiative-cluster-execution-coordinator/reports/uat-render-quality-2026-05-19.md)
(multi-dimensional Orthography / Visual polish / Naturalness check) +
[`scripts/render_uat_dossier.py`](../../../../../../scripts/render_uat_dossier.py)
(brand-aligned UAT report rendering itself — UAT-on-UAT recursion).

**Owning canonical.** [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc)
+ [`.cursor/skills/external-render-craft/SKILL.md`](../../../../../../.cursor/skills/external-render-craft/SKILL.md).

### 3.5 Regression-class UAT

**Trigger.** Pre-merge / pre-release; runs continuously. Fires on every
PR + every release-gate invocation.

**Bar.** Validator suite PASS (governed by
`config/verification-profiles.json` `pre_commit` profile). Substrate
test suite PASS (`pytest -m <substrate-mark>`). HLK validators PASS
(`scripts/validate_hlk.py`). Smoke tests PASS
(`scripts/browser-smoke.py`). All counts captured in the UAT report
§3 mechanical-evidence section with reproducible commands.

**Internal precedent.** [`uat-i47-user-centric-uat-2026-05-02.md`](../../../../../wip/planning/47-user-centric-uat/reports/uat-i47-user-centric-uat-2026-05-02.md)
(persona-conditioned scenarios; cumulative test counts) +
`scripts/release-gate.py` invocations across all closure UAT.

**Owning canonical.** [`akos-governance-remediation.mdc`](../../../../../../.cursor/rules/akos-governance-remediation.mdc)
§"Verification matrix" + `config/verification-profiles.json`.

### 3.6 Persona-class UAT

**Trigger.** When MADEIRA (or a successor AIC) ships answers to a
persona-conditioned scenario AND the answers feed a quality rollup.
Also fires when a persona doctrine document changes substantively.

**Bar.** Per-persona scenario coverage table; per-scenario evidence
(answer transcript + ground-truth comparison + calibration tolerance);
quality dimensions A/B/C/D/E checklist per I47 evidence rollup.

**Internal precedent.** [`docs/uat/i86-p3-persona-rollup-acceptance.md`](../../../../uat/i86-p3-persona-rollup-acceptance.md)
+ I47 user-centric UAT closure.

**Owning canonical.** This canonical §3.6 + I47 closure UAT pattern +
`akos-madeira-management.mdc` (when minted).

### 3.7 Deploy-class UAT (NEW; codified at this mint)

**Trigger.** Any sibling-repo push that triggers a deploy (`hlk-erp` →
Vercel; `boilerplate` → Vercel; `kirbe-platform` → Render or
equivalent). Fires whenever a closure UAT touches a sibling-repo.

**Bar.** Pre-deploy: all gates from §3.5 regression-class. At-deploy:
deployment status verified at `READY` state via vendor MCP (Vercel
`get_deployment` returning `state: READY`; Render service status
green). Post-deploy: target URL fetched; HTTP 200 response captured;
critical-route smoke test executed (e.g., `/`, `/auth/login`,
`/planning/*` for `hlk-erp`); console logs captured for client-side
errors. **If the deploy goes ERROR → recovery hotfix is itself a deploy
UAT artifact** (the regression evidence trail closes the loop).

**Internal precedent.** **NEW class established 2026-05-20** by the
`hlk-erp` Vercel hotfix `ec3f883`:

- ERROR state: `dpl_6uNfwjKVUNwqqd2MZ65vySkvd834` at sha `71d3ebe`
  failed with `react-essentials#server-components` error
  (server-only-import bundle poisoning client components).
- Hotfix: extract `lib/planning/github-urls.ts` as client-safe URL
  helpers; migrate 4 client components; preserve back-compat re-export
  from `github-reader.ts`.
- READY state: `dpl_8N4pqRVEhhUCMMV82A8RUzYAfixo` at sha `ec3f883`
  reached production READY.
- Decision row: D-IH-86-AT.

**Why this class did not previously exist.** Prior to today, sibling-repo
deploys were treated as a sub-step of regression-class UAT (the build
passed locally → the deploy was assumed to follow). Vercel's
build-context (Next.js App Router server-only enforcement) is
stricter than `tsc` local; build-context-class regressions can reach
production despite local PASS. Deploy-class UAT names this gap and
closes it via vendor-MCP verification.

**Owning canonical.** This canonical §3.7 + future
`akos-uat-discipline.mdc` cursor rule (forward-charter; mechanical
contract: closure-UAT touching sibling-repo MUST include
deploy-verification section). Vendor-MCP integration:
[`user-vercel`](../../../../../../mcps/user-vercel/) for Vercel
deploys; [`plugin-render-render`](../../../../../../mcps/plugin-render-render/)
for Render deploys; equivalent MCP for any future deploy target.

## 4. Compose_UAT — the rule that picks the class

Given an artifact, the relevant UAT classes are derived from the five
Quality Fabric axes (7-class taxonomy at status: charter; 11-class
promotion gated on `D-IH-86-AY` per Wave K regression — see §4.1):

```
classes = []
if governance.is_initiative_closure(artifact): classes += [closure]
if brand.is_branded(artifact): classes += [brand]
if channel.is_send_channel(artifact): classes += [send, render]
if audience.is_external(artifact): classes += [render]
if governance.has_validator_suite(artifact): classes += [regression]
if scenario.is_persona_conditioned(artifact): classes += [persona]
if governance.touches_sibling_repo(artifact): classes += [deploy]
# 11-class extension (post-D-IH-86-AY promotion):
if artifact.has_locale_variants(): classes += [localisation]
if artifact.is_human_facing_ui_or_doc(): classes += [accessibility]
if artifact.has_load_or_render_budget(): classes += [performance]
if artifact.touches_pii_or_eu_data_subjects(): classes += [privacy]
```

Multiple classes may fire on the same artifact. When they do, the UAT
report must satisfy **every** class's bar — same multiplicative-AND
rule as the parent Quality Fabric §3.

**Worked example: I65 closure UAT (post-rework).** Audience = J-OP for
the closure report itself + J-CU for the rendered HLK-ERP planning
panel. Channel = ERP record (the panel itself). Scenario = AKOS
planning workspace consumption by future agents. Brand = brand-class
fires (the panel is branded). Governance = initiative closure +
sibling-repo touch (the `hlk-erp` deploy).

Resolved classes: closure + brand + render + regression + deploy. Five
of seven. The reworked uat-i65 must satisfy all five bars; this is why
the existing stub (regression + closure only) was insufficient and the
operator's call to rework it was correct.

### 4.1 11-class promotion (forward-charter at `D-IH-86-AY`)

Wave J regression G5 surfaced 4 missing UAT classes that 7-class
taxonomy folded ambiguously into existing classes. Wave K regression
operator-ratified `opt-promote-11` 2026-05-20 (per `D-IH-86-AY`):
when this canonical promotes from `status: charter` to `status: active`,
the taxonomy promotes from 7 → 11 classes by adding:

- **`localisation`** — per-language UAT verifying orthography +
  cultural register + word-list anti-patterns. Internal precedent:
  [`scripts/validate_locale_orthography.py`](../../../../../../scripts/validate_locale_orthography.py)
  (ES smart-quote + FR diacritics + EN word-list anti-patterns).
  External grounding: ISO 639-1 language codes; ICU locale rules;
  CLDR plural-forms specification. Fires when the artifact has
  `language:` frontmatter listing > 1 locale OR when its parent
  initiative spans multi-locale audiences (J-IN/J-CU/J-PT/J-AD/J-ENISA
  bands span en/es/fr per `AUDIENCE_REGISTRY.csv` `supported_languages`).
- **`accessibility`** — WCAG 2.2 AA verification for keyboard nav,
  screen reader semantics, color contrast, focus-visible state,
  text-reflow at zoom, motion-prefers-reduced. Internal precedent:
  Lane I-D `hlk-erp` Radix UI primitives (already AA-compliant by
  default); brand-class UAT references this when surface is
  human-facing UI. External grounding: WCAG 2.2 (W3C, 2023);
  Section 508 Refresh; EN 301 549 (EU public sector requirement).
  Fires for any output type that renders to a human-facing UI surface
  (Layer 1 OUTPUT_TYPE = OT-WEB-PAGE / OT-WEB-FORM / OT-PDF-DOCUMENT /
  OT-SLIDE-DECK).
- **`performance`** — Core Web Vitals (LCP / INP / CLS) + bundle size
  + load-time budgets for web/email-rendered surfaces. Internal
  precedent: `hlk-erp` deploy verification per `akos-quality-fabric.mdc`
  RULE 3 (Vercel deploy-evidence trail). External grounding: Lighthouse
  scoring; Web.dev Core Web Vitals thresholds; Vercel Speed Insights;
  Calibre Performance Budget patterns. Fires when the artifact's
  Layer 4 RENDER_SURFACE is `web` or `mail` (HTML rendering happens
  recipient-side and load-time matters).
- **`privacy`** — GDPR cookie consent verification + data-retention
  claim accuracy + PII redaction + DPIA-required-when-fires. Internal
  precedent: `holistika_ops` schema RLS posture + finops register PII
  exclusion patterns. External grounding: GDPR Art 5 (data minimisation)
  + Art 13-14 (transparency) + Art 35 (DPIA); ePrivacy Directive
  2002/58/EC; CNIL guidance. Fires when audience class is in
  EU-data-subject set (J-CU / J-PT / J-AD / J-ENISA / J-RC always; J-IN
  when EU-domiciled investor; J-CO when EU-based collaborator).

The 11-class promotion lands at this canonical's charter→active
transition. Until promotion, agents may choose to invoke the additional
4 classes voluntarily on artifacts that demand them (e.g., a J-ENISA
dossier should include privacy-class UAT today even though the formal
promotion has not happened).

## 5. Cross-area inheritance contract

UAT is People-owned doctrine, but every area's UAT inherits the seven
classes. Per [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc)
RULE 1: People owns the pattern; areas author their own UAT against
the pattern. The mapping:

| Area | Typical UAT classes that fire |
|:---|:---|
| **Tech (System Owner / Envoy Tech Lab)** | regression + deploy (every deploy of every sibling repo); occasional closure when an initiative is Tech-led |
| **Marketing (Brand / Reach / Resonance / Experimentation)** | brand + render + send (every external-touching artifact); closure when initiative is Marketing-led |
| **Research (Holistik Researcher / R&L)** | regression + persona (when MADEIRA scenarios fire); closure when initiative is Research-led |
| **Operations (PMO / RevOps / SMO / Intelligence Ops)** | closure + regression; send when adviser handoff fires |
| **People (this area's own UAT)** | closure + regression; persona when AIC role-class onboarding fires |
| **Legal (Legal Counsel)** | closure + send (when legal-template handoffs fire); render (PDF integrity for filed instruments) |
| **Compliance (Compliance Manager)** | closure + regression; send when ENISA / GDPR / regulator dossier fires; render (sealed-PDF integrity) |

Each area's owned canonicals + cursor rules MAY tighten the bar above
this canonical's default (e.g., compliance-area sends require sealed
sha256 + manifest sidecar; brand-area renders require Figma source
parity check). They MAY NOT loosen below the default. This is the same
operator-defaults-bind / area-extensions-tighten pattern as the rest
of HLK governance.

## 6. Figma involvement (operator question, answered)

The operator asked: *"Is figma involved in these processes or should it
be?"* The answer: **yes, materialised in brand-class UAT §3.2 +
deploy-class UAT §3.7 sub-routes**.

Specifically:

- **Brand-class UAT** references [`FIGMA_FILES_REGISTRY.csv`](../../../../Marketing/Brand/canonicals/dimensions/FIGMA_FILES_REGISTRY.csv)
  to resolve which Figma file is the source-of-truth for which surface.
  When a brand-touching artifact diverges from its Figma source, the
  brand-class UAT findings table flags it.
- **Render-class UAT** for slide-class surfaces references
  `figma-link.md` siblings + checks the Figma file URL is alive +
  permissions are correct (per
  `akos-external-render-discipline.mdc` RULE 4 heuristic 5).
- **Deploy-class UAT** for HLK-ERP / boilerplate routes verifies the
  deployed UI matches the Figma frame at the documented breakpoint
  (this is forward-charter scope; not yet implemented as a mechanical
  drift gate; relies on operator-walk for now).

Figma involvement is **scoped** — not every UAT class touches Figma.
Regression-class never does. Persona-class typically does not (unless
the persona scenarios output rendered artifacts). Closure-class only
when its constituent classes fire brand or render.

## 7. Self-discipline rules for agents

When authoring a UAT report:

1. **Resolve the 5 axes BEFORE drafting** (per Quality Fabric §8 rule).
   The frontmatter `audience:` + `channel:` (when known) tags drive
   which UAT classes fire.
2. **Compute the relevant classes via §4 compose_UAT rule** before
   choosing template structure. Use closure-template + impeccable-template
   in tandem when both closure-class and brand-class fire.
3. **For every PASS row, record a reproducible command.** Operator (or
   AIC role_owner) must be able to re-run the verification themselves.
4. **For every FAIL or PASS-WITH-FOLLOWUP row, record a remediation
   plan.** Either: a follow-up commit reference; OR a tracker entry
   (per `akos-conflict-surfacing-and-blocker-trackers.mdc`); OR a
   deferral decision row.
5. **For sibling-repo work, never skip §3.7 deploy-verification.** Even
   if the deploy is "expected to succeed", record the vendor-MCP
   verification (state: READY; HTTP 200 on hero route) as a row in
   the table. The cost of recording is low; the cost of skipping was
   demonstrated by `dpl_6uNfwjKVUNwqqd2MZ65vySkvd834`.
6. **Sign-off finality.** §10 of the report carries 7 items max.
   Operator (or AIC role_owner) must check every item personally before
   the verdict flips to PASS. Rubber-stamping is forbidden by the
   pattern.

## 8. Migration posture (charter → active)

This canonical lands at **`status: charter`** at mint time
(D-IH-86-AV, 2026-05-20). Promotion to **`status: active`** requires:

1. **First worked example** — uat-i65-2026-05-19.md reworked to satisfy
   five of seven classes (closure + brand + render + regression +
   deploy). Lands this Wave J P2.
2. **Cursor rule companion** — `.cursor/rules/akos-uat-discipline.mdc`
   minted with mechanical contracts (audience-tag presence;
   deploy-verification presence for sibling-repo touches; FIGMA
   reference for brand-class UAT). Lands this Wave J P3.
3. **Paired SOP + runbook** — `SOP-PEOPLE_UAT_GOVERNANCE_001.md` +
   `scripts/validate_uat_report.py` (Pydantic frontmatter validator).
   Forward-charter; lands in next Wave or successor initiative.
4. **Operator-explicit ratification** of the promotion.

Until promotion, this canonical is the durable record of the operator's
intent + the architecture future agents inherit. Charter status does
NOT prevent the worked example (uat-i65 rework) from instantiating
against it.

## 9. Cross-references

- Parent meta-doctrine: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md)
  (5-axis compose() architecture).
- Sister canonicals under People:
  [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md),
  [`RESEARCH_HEAD_DISCIPLINE.md`](RESEARCH_HEAD_DISCIPLINE.md),
  [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md).
- UAT-specific cursor rules + templates:
  [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc)
  §"UAT quality bar",
  [`docs/wip/planning/_templates/uat-closure-template.md`](../../../../../wip/planning/_templates/uat-closure-template.md),
  [`docs/wip/planning/_templates/uat-impeccable-template.md`](../../../../../wip/planning/_templates/uat-impeccable-template.md).
- External research grounding (per
  `akos-applied-research-discipline.mdc` RULE 2 — novel framing
  requires external citation):
  - **World Quality Report 2024** (cited via Yuri Kan
    [yrkan.com/blog/uat-documentation/](https://yrkan.com/blog/uat-documentation/)):
    structured UAT documentation reduces post-release defects 38% +
    project escalations 52%.
  - **Standish Group CHAOS Report 2023**: inadequate user involvement
    is the second most common cause of project failure (15% of
    failed IT projects); the §10 7-item operator checklist binds
    against this anti-pattern.
  - **Playwright MCP introduction** (playwright.dev/mcp): 2026 best
    practice for browser-based UAT pairs accessibility-snapshot
    execution with screenshot evidence at decision points; binds the
    §3.4 render-class browser-walk evidence pattern.
  - **PageBolt MCP audit-trail pattern**: API logs alone cannot prove
    what an operator saw on screen; binds the screenshot + sha256 +
    timestamp evidence requirement for browser-walk UAT.
  - **IEEE 829-2008 Standard for Software and System Test
    Documentation**: foundational test-documentation taxonomy.
  - **ISTQB Foundation Level Syllabus** (test-process structure;
    test-design technique catalogue): underpins regression-class +
    closure-class UAT bar.
- Decision lineage: D-IH-86-AV (this canonical's mint), D-IH-86-AS (UAT
  quality-bar canonization in `akos-planning-traceability.mdc`),
  D-IH-86-AT (Vercel deploy regression hotfix — the deploy-UAT class
  worked example), D-IH-86-AU (parent Quality Fabric architecture
  mint), **D-IH-86-CW** (this canonical's promotion charter→active +
  field-test window opening per META4-b operator ratification 2026-05-24).

## 10. Promotion log + field-test window observations

> Living governance log for this canonical's status transitions. The
> **machine-readable record** of the open field-test window — open date,
> close target, promotion criteria (4 conjunctive PASS clauses), revocation
> triggers (3 disjunctive demotion conditions), monitoring owner + co-owner,
> lifecycle status — lives in the frontmatter `field_test_window:` block
> at the top of this file (canonical schema: `akos.hlk_uat_report.
> CanonicalFieldTestWindow` Pydantic model). This §10 prose is the
> human-readable narrative complement; agents authoring observation
> entries (§10.1 / §10.2 / §10.3) MUST also bump
> `field_test_window.last_observation_*` fields in the same commit so
> the frontmatter stays the source of truth for tooling.

§10.1 — Wave S close observation (reserved; first FTW observation wave).

§10.2 — Wave T close observation (reserved; second FTW observation wave).

§10.3 — Wave U close + final field-test verdict (reserved; third + close-
target wave; `field_test_window.status` transitions `open` → `closing`
at Wave U entry, and `closing` → `closed` (or `revoked`) at the operator
sign-off gate per the per-status semantics in the
`CanonicalFieldTestWindow` Pydantic model).

### 10.4 Promotion to `status: active` (2026-05-24) — D-IH-86-CW

**Trigger.** I86 cluster Wave R+1 P1; operator ratification of the
META1..META6 batch (META4-b explicitly: clean PASS now + explicit
3-wave field-test window monitoring obligation, not a PWF deferral).

**Realized at this commit.** All four `forward_charters` rows from the
charter-status frontmatter have landed in the same commit-window as the
promotion:

1. [`SOP-PEOPLE_UAT_GOVERNANCE_001.md`](SOP-PEOPLE_UAT_GOVERNANCE_001.md)
   (paired SOP) + its [addendum](SOP-PEOPLE_UAT_GOVERNANCE_001.addendum.md)
   (auditor + System Owner depth + field-test window revocation procedure).
2. [`scripts/validate_uat_report.py`](../../../../../../scripts/validate_uat_report.py)
   (paired runbook; --self-test + --report + --all modes).
3. [`process_list.csv`](../../Compliance/canonicals/process_list.csv)
   row `hol_peopl_dtp_uat_governance_001`
   (35-column canonical-CSV gate; cadence_type=event_triggered;
   inherited_pattern_id=pattern_uat_class_taxonomy).
4. [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv)
   row `pattern_uat_class_taxonomy` (15-column row;
   class=quality_fabric_specialty_canonical; 12th specialty).
5. [`.cursor/rules/akos-uat-discipline.mdc`](../../../../../../.cursor/rules/akos-uat-discipline.mdc)
   (cursor rule governing the *when*; 8 binding rules + 1 advisory
   rule for the specialty mint contract).
6. [`.cursor/skills/uat-discipline-craft/SKILL.md`](../../../../../../.cursor/skills/uat-discipline-craft/SKILL.md)
   (paired skill governing the *how*; 7 principles + worked-example
   templates + 4 anti-patterns + recovery patterns).

**Field-test window opened, not closed.** The promotion is **provisional
for 3 observation waves** (S + T + U closes; `close_target_date_estimate`
2026-06-14). The window is fully described in the
`field_test_window:` frontmatter block above as a structured object —
NOT in prose here, by deliberate design per operator's META4-b feedback
(*"i was really worried that the UAT would get shallow or not governed
or not properly followed"*). Machine-readable frontmatter lets the
`validate_uat_report.py` runbook + future tooling FK-resolve the
window's status + emit dashboard entries + auto-prompt observation
authors when each wave's close report lands.

**Revocation path.** Documented operationally in
[`SOP-PEOPLE_UAT_GOVERNANCE_001.addendum.md`](SOP-PEOPLE_UAT_GOVERNANCE_001.addendum.md)
§"Field-test window revocation procedure". Tooling-side, the revocation
decision ID template is `D-IH-86-CW-revoke` (mint the suffixed decision
when revoking; flip `field_test_window.status` to `revoked` + flip
`status:` back to `charter` + cite the revoke decision in
`last_review_decision_id`).

**Field-test signal at promotion-time (worked example).** Within the
SAME session as this promotion, `scripts/validate_uat_report.py
--report reports/uat-wave-r-closure-2026-05-24.md` caught **1 real
FAIL** against the Wave R closure UAT that this very promotion's author
had authored just hours earlier:
**UAT-FM-11-PWF-WITHOUT-RATIONALE** — verdict was `PASS-WITH-FOLLOWUP`
but `verdict_followup_rationale:` frontmatter was missing.

Per
[`akos-uat-discipline.mdc`](../../../../../../.cursor/rules/akos-uat-discipline.mdc)
RULE 5 5-option disposition enum, the natural disposition is
`amend-followup-rationale`. The Wave R UAT amendment is being authored
in the *same* commit-window as this promotion (D-IH-86-CW Commit 3),
with `verdict_history:` v1→v2 + populated
`verdict_followup_rationale:` citing this validator finding as the
field-test signal that triggered the amendment.

**Closing loop.** The new validator caught a real gap on its first run
AND the gap is being closed in the same session that mints the
validator. The Wave R amendment is the **canonical worked-example
birth artifact** that future PWF-rationale audits will reference. It
also pre-validates **promotion criterion FTW-UAT-01-THREE-CLOSURE-UATS**
in advance (Wave R counts as a retroactive 4th data point alongside
S/T/U) and pre-validates **FTW-UAT-04-PWF-RATIONALE-COMPLIANCE** by
proving the discipline lands cleanly when the validator surfaces the
gap.

The closing-loop pattern (mint validator → catch real gap on first run →
amend offending artifact in same commit-window → cite finding as field-
test signal) is itself a transferable craft pattern that future specialty
mints should consider replicating; reserve the pattern name
`pattern_validator_field_test_closing_loop` for a future mint if the
Wave M (INTER_WAVE_REGRESSION) + Wave N (INDEX_INTEGRITY) + this
Wave R+1 (UAT_DISCIPLINE) third instantiation confirms it as canonical.

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UAT_GOVERNANCE_001.md
@docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/dimensions/FIGMA_FILES_REGISTRY.csv
@.cursor/rules/akos-uat-discipline.mdc
@.cursor/rules/akos-planning-traceability.mdc
@.cursor/skills/uat-discipline-craft/SKILL.md
