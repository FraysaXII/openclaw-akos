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
  - People Operations Lead
last_review: 2026-05-20
last_review_by: Founder/CEO
last_review_at: 2026-05-20
last_review_decision_id: D-IH-86-AV
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-AV
status: charter
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - RESEARCH_HEAD_DISCIPLINE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv
  - ../Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
  - ../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - ../../Marketing/Brand/canonicals/dimensions/FIGMA_FILES_REGISTRY.csv
linked_cursor_rules:
  - .cursor/rules/akos-planning-traceability.mdc
  - .cursor/rules/akos-external-render-discipline.mdc
  - .cursor/rules/akos-brand-baseline-reality.mdc
  - .cursor/rules/akos-applied-research-discipline.mdc
  - .cursor/rules/akos-people-discipline-of-disciplines.mdc
linked_skills:
  - .cursor/skills/inline-ratify-craft/SKILL.md
  - .cursor/skills/external-render-craft/SKILL.md
  - .cursor/skills/impeccable/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
  - RESEARCH_HEAD_DISCIPLINE.md
forward_charters:
  - SOP-PEOPLE_UAT_GOVERNANCE_001.md (paired SOP + addendum + runbook validate_uat_report.py)
  - process_list.csv row hol_peopl_dtp_uat_governance_001
  - PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_uat_class_taxonomy
  - .cursor/rules/akos-uat-discipline.mdc (mechanical drift gate companion to akos-quality-fabric.mdc)
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
Quality Fabric axes:

```
classes = []
if governance.is_initiative_closure(artifact): classes += [closure]
if brand.is_branded(artifact): classes += [brand]
if channel.is_send_channel(artifact): classes += [send, render]
if audience.is_external(artifact): classes += [render]
if governance.has_validator_suite(artifact): classes += [regression]
if scenario.is_persona_conditioned(artifact): classes += [persona]
if governance.touches_sibling_repo(artifact): classes += [deploy]
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
  mint).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
@docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/dimensions/FIGMA_FILES_REGISTRY.csv
@.cursor/rules/akos-planning-traceability.mdc
