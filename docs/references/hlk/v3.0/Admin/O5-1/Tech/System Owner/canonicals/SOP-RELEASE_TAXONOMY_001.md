---
language: en
status: active
canonical: true
sop_id: SOP-RELEASE_TAXONOMY_001
version: 1.0.0
role_owner: System Owner
classification: way_of_working
intellectual_kind: sop_canonical
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
companion_to:
  - ../../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  - ../../../../People/canonicals/LOGIC_CHANGE_LOG.md
  - ../../../../../../CHANGELOG.md
---

# SOP — Release Taxonomy (v1.0.0)

> **Document owner**: System Owner. **Authority**: ratified at I71 P3 via `D-IH-71-P` (this commit), discharging `OPS-71-2` and the deferral slot opened by `D-IH-70-CLOSURE`. **Companion to**: [`CHANGELOG.md`](../../../../../../CHANGELOG.md) (policy header points here), [`LOGIC_CHANGE_LOG.md`](../../../../People/canonicals/LOGIC_CHANGE_LOG.md) (methodology lane carrier), [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §10 + §16 (release-policy SSOT + render pipeline ownership).
>
> **Why this SOP exists.** Through I70 closure (`8ba8be9`, 2026-05-13), the repo accumulated methodology-grade work (v3.0 vault, federated canonicals, multilingual contract, brand sub-disciplines) but **no agreed criteria for what "release baseline" means** in this codebase. `D-IH-70-CLOSURE` explicitly deferred the annotated `v3.1` git tag because three distinct version-shaped surfaces were drifting against each other (methodology line in `LOGIC_CHANGE_LOG.md`; vault folder `v3.0/`; openclaw-akos SemVer in `CHANGELOG.md`) without a discipline binding them. I71 P0 ratified the three-lane model via `D-IH-71-D`; I71 P3 (this SOP) codifies the lane definitions, tag criteria, SemVer judgment, the `[Unreleased]` working-line discipline, the cross-lane non-implication rules, and — most load-bearing — the **customer-invisible versioning posture** that keeps version churn an operator-internal concern.
>
> **Why customer-invisible.** The operator-stated intent (paraphrase): *"intuitive clever versioning — do not let the customer know it's a new version."* Customer-facing rendered artefacts (SUEZ deck, Asesoría proposal, future engagement PDFs) must read as **the canonical artefact the customer asked for**, not as `v2 of the deck after refinements`. Versioning is operator-internal infrastructure (audit trail, methodology lineage, repo baseline). The SUEZ-style brand-failure mode that I71 P1 + P2 validator chassis closed is exactly the kind of "release event" this taxonomy must protect against: brand failures that leak into customer-facing PDFs are release events whether or not the operator stamps `v3.1` on the cover. The discipline separates **what the operator and agents track** (everything) from **what the customer sees on the artefact** (nothing version-shaped by default).

---

## 1. The three release lanes (ratified at P0 via D-IH-71-D)

Three independent surfaces carry version-shaped state in this repository. Each lane has its own carrier, its own bump trigger, and its own role in the repo's release story. **Bumping one lane does not imply bumping any other.**

| Lane | Carrier | Bump trigger | Tag in this repo? |
|:---|:---|:---|:---|
| **Methodology `major.minor`** | [`LOGIC_CHANGE_LOG.md`](../../../../People/canonicals/LOGIC_CHANGE_LOG.md) + `D-IH-*` rows (e.g., D-IH-70-Z, AA-AD describing v3.1-shaped schema work) | A breakthrough-driven re-versioning row per founder principle 2.6 (`LOGIC_CHANGE_LOG.md` §1 schema). **Not** a folder rename or a git tag. | No. Methodology version is methodology-internal. |
| **HLK vault folder path** | `docs/references/hlk/v3.0/` (the structural root of the canonical vault) | A vault-restructure initiative that warrants renaming (`v3.0/` → `v4.0/`). This is its own initiative, not an inference from methodology or tag bumps; high migration cost; out of scope for I71. | No. Vault folder is a structural path, not a git artefact. |
| **openclaw-akos SemVer + CHANGELOG + git tag** | [`CHANGELOG.md`](../../../../../../CHANGELOG.md) + `vMAJOR.MINOR.PATCH` annotated tags on `origin/main` | Conventional release judgment per §2 (tag criteria) + §3 (SemVer judgment). **Not** one-to-one with every `D-IH-*` row. | Yes (when ratified per §2). |

Each lane is operator-internal by design (per §6 customer-invisible versioning posture). The customer never sees a methodology version, a vault folder path, or a git tag stamped on a rendered PDF.

### 1.1 Lane carriers in detail

- **Methodology `major.minor`** lives in [`LOGIC_CHANGE_LOG.md`](../../../../People/canonicals/LOGIC_CHANGE_LOG.md). The schema (§1 of that canonical) carries one row per breakthrough-driven re-version per founder principle 2.6. Rows record `breakthrough_id + date + insight + version_increment + canonicals_added_or_modified`. The methodology version that ships today is the operator's working line; sibling `D-IH-*` rows in `DECISION_REGISTER.csv` describe the specific schema work that warrants the increment. The methodology lane has **no enforcement validator** — the operator owns this lane via the `LOGIC_CHANGE_LOG.md` author flow.
- **HLK vault folder path** is a structural fact: every canonical lives under `docs/references/hlk/v3.0/`. A rename to `v4.0/` would touch hundreds of files (canonicals + cross-references + render-script path constants + cursor rules + sibling-repo bless-files), warrant a dedicated migration initiative, and require its own decision (`D-IH-NN-*`) ratifying the rename scope. **Renaming is NOT inferred from methodology or git-tag bumps** — see §5.
- **openclaw-akos SemVer + CHANGELOG + git tag** is the only lane with a git-side artefact (an annotated tag on `origin/main`) and a markdown-side artefact ([`CHANGELOG.md`](../../../../../../CHANGELOG.md) `[Unreleased]` block). The bump trigger is conventional SemVer judgment per §3. Day-to-day, the working line accumulates in `[Unreleased]`; at tag ratification, `[Unreleased]` renames per §4.1.

---

## 2. Tag criteria — when to ratify a `vMAJOR.MINOR.PATCH` annotated tag

A git tag in this repo means **release baseline** — a coherent, externally-visible repo cut that the operator wants pinned. Tags lag methodology versioning by intent; they are operator-curated milestones, not automated checkpoints.

### 2.1 Legitimate tag triggers (examples)

- **Initiative-closure cut for a substantive initiative.** I71 P6 closure is a legitimate trigger candidate (the initiative has substantive scope: 4 validator packs + AIOps baseline + 2 governance disciplines + Tier 1 Vale sibling). I70 P11 closure was also a legitimate candidate; the operator deferred to I71 per `D-IH-70-CLOSURE`.
- **Public deploy event.** A coordinated cross-repo deploy that warrants a pinned baseline across `openclaw-akos` and its consumer repos (when one ships).
- **Major-version methodology bump that fundamentally restructures the doctrine.** A `LOGIC_CHANGE_LOG.md` row that re-versions to `v4.0` (e.g., the doctrine fundamentally restructures the 6-axis operating model or the canonical area taxonomy). MAJOR-level methodology change may, but does not automatically, warrant a tag.

### 2.2 Non-triggers (examples)

- Every `D-IH-*` row (most are governance fine-tuning; tagging each would defeat the purpose of "release baseline").
- Every commit, every PR merge.
- Every initiative closure of a small initiative (e.g., a chore-class candidate; a documentation-only refresh).
- Every brand-canonical addition or chassis extension.
- Every CSV row addition to a dimension register.

### 2.3 Operator discretion

Tags are operator-ratified, not automatic. When uncertain, **prefer holding `[Unreleased]`** over premature tagging — a missing tag costs nothing; a noisy tag history erodes the signal value of every prior tag. The default at planning-time for any forward closure is `hold`; the operator escalates to `tag` only when one of §2.1's triggers fires cleanly.

### 2.4 Historical context — the I70 closure deferral

`D-IH-70-CLOSURE` deferred the `v3.1` annotated tag at I70 P11 closure (2026-05-13) because:
- I70's scope was substantive (17 phases; OS-shaped governance foundation; federated canonicals).
- But the three lanes had no agreed binding contract at that point.
- Tagging without a contract would have set a confusing precedent (does v3.1 mean methodology v3.1 or repo v3.1?).

I71 P3 (this SOP) discharges that deferral. The C-71-3 inline-ratify gate at execution-time decides whether to tag now (at I71 P3 commit), at I71 P6 closure (default), or hold further. Either verdict ships this SOP; only the tag decision differs.

---

## 3. SemVer judgment — PATCH / MINOR / MAJOR

Tag judgment follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) and the [conventional-commits](https://www.conventionalcommits.org/en/v1.0.0/) magnitude convention.

| Level | Trigger class | Examples (this repo) |
|:---|:---|:---|
| **PATCH** (`x.y.Z`) | Fixes; validator pack rule additions without new contracts; documentation refinements that preserve all contracts. | Bug fix to a validator; new regex rule added to an existing pack via operator-editable YAML; SOP wording clarification with no scope change. |
| **MINOR** (`x.Y.0`) | Additive changes; new validator pack; new canonical; new dimension column; substantive initiative closure that adds capability without breaking existing contracts. | I71 closure (4 validator packs + AIOps baseline + 2 governance disciplines + Tier 1 Vale sibling); new canonical CSV; new `akos/*` module. |
| **MAJOR** (`X.0.0`) | Breaking changes; canonical model signature changes; vault folder restructure; methodology version bump in `LOGIC_CHANGE_LOG.md` that breaks doctrinal continuity. | Vault folder rename `v3.0/` → `v4.0/`; canonical CSV header rename or column removal; methodology `v3.x` → `v4.0` doctrinal restructure. |

**Cross-lane caveat.** A MAJOR-level repo tag does not imply a methodology major bump or a vault folder rename — and vice versa. See §5.

### 3.1 Worked examples (illustrative; not commitments)

- **`v3.0.1` PATCH** — a hypothetical bug fix to `validate_brand_voice_register.py`'s regex compilation that didn't affect rule contracts, packed-yaml schema, or any consumer-facing surface.
- **`v3.1.0` MINOR** — I71 P6 closure (proposed; gated on C-71-3 verdict). Adds 4 validator packs + AIOps baseline + release-taxonomy SOP + review-stamp dimension + Tier 1 Vale sibling — all additive; existing contracts preserved (I71's `DO NOT` plan contract forbids signature changes to existing Pydantic chassis).
- **`v4.0.0` MAJOR** — a hypothetical vault folder rename (`v3.0/` → `v4.0/`) coordinated with a doctrine restructure in `LOGIC_CHANGE_LOG.md` (methodology v3.x → v4.0). Breaking because every canonical path moves; every cross-reference updates; every render-script CANONICAL_PATHS constant rebases; every sibling-repo bless file refreshes.

### 3.2 The MINOR-default heuristic

When uncertain between PATCH and MINOR, **prefer MINOR**. A MINOR tag costs nothing and signals "this cut adds capability"; a misclassified PATCH tag can mislead consumers (or future-operator-self) into reading a substantive change as a fix. Conversely, when uncertain between MINOR and MAJOR, **prefer holding** until the change is clearly breaking (per §2.3 operator discretion).

---

## 4. CHANGELOG `[Unreleased]` working-line discipline

Day-to-day, [`CHANGELOG.md`](../../../../../../CHANGELOG.md) `[Unreleased]` is the working line. Per [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), entries accumulate under standard subsections:

- **Added** — new capabilities (e.g., I71 P2 validator packs).
- **Changed** — modifications to existing capabilities.
- **Deprecated** — capabilities slated for removal.
- **Removed** — capabilities deleted.
- **Fixed** — bug fixes.
- **Security** — security-relevant fixes.

### 4.1 Tag ratification renames `[Unreleased]`

When the operator ratifies a tag per §2, the `[Unreleased]` heading renames to `[vMAJOR.MINOR.PATCH] - YYYY-MM-DD` in the same commit. A fresh `[Unreleased]` heading is added immediately above for the next working line. Entry contents do not change; only the heading.

### 4.2 Policy header pointer

`CHANGELOG.md` carries a `## Policy` header pointer at the top of the file (above `[Unreleased]`) cross-linking back to this SOP. Operators reading the changelog land on the policy in one click.

### 4.3 Entry style and citation discipline

CHANGELOG entries follow these conventions (matching the existing CHANGELOG body's prose style):

- **Initiative-scoped entries** carry the initiative + phase prefix (e.g., `**I71 P3 — Strand C1 release-taxonomy SOP authored (2026-05-14):**`) and cite the relevant decisions (`D-IH-71-P`), ops rows (`OPS-71-2`), and canonical paths.
- **Cross-lane impact is called out explicitly.** If a change advances the methodology lane (`LOGIC_CHANGE_LOG.md` row added) or the vault folder lane (`v3.0/` rename initiative scoped), the CHANGELOG entry mentions both and links to the relevant initiative-scoped Cursor plan / master-roadmap.
- **No customer-facing prose in CHANGELOG.** The CHANGELOG is operator + agent + developer audience; per §6 customer-invisible posture, the customer never reads this file. Internal-register vocabulary (per `BRAND_BASELINE_REALITY_MATRIX.md`) is unrestricted here.

---

## 5. Cross-lane interaction — what one lane does NOT imply

The three lanes are independent. Each carries its own trigger; alignment of two or three lanes is occasionally meaningful but **never mandatory**.

| Lane bumped | Implies? |
|:---|:---|
| Methodology `major.minor` (e.g., v3.0 → v3.1 row in `LOGIC_CHANGE_LOG.md`) | **Does NOT imply** vault folder rename; **does NOT imply** git tag. Methodology lane is its own surface. |
| HLK vault folder path (e.g., `v3.0/` → `v4.0/`) | **Does NOT imply** methodology major bump (the methodology may have re-versioned long before the folder); **does NOT imply** git tag. Folder rename is its own initiative. |
| openclaw-akos SemVer + git tag (e.g., `v3.1.0`) | **Does NOT imply** methodology bump (tags lag methodology by intent); **does NOT imply** folder rename (folder lives at a structural path, not a release artefact). |

**Aligned alignment is a courtesy, not a contract.** A coordinated cut (methodology v3.1 + git tag v3.1.0) can be intentional for a clean closure narrative — but the operator decides; no validator infers one lane's state from another's.

### 5.1 Common confusions to avoid

- *"The folder says `v3.0/` so the methodology must be v3.0."* — No. The folder is structural; the methodology version is whatever the `LOGIC_CHANGE_LOG.md` rows describe today (e.g., v3.0 → v3.1-shaped via the I70 P9 rows). The folder lags the methodology by intent (renaming is expensive).
- *"We tagged `v3.1.0`, so we must rename the folder to `v3.1/`."* — No. The tag carries repo release-baseline semantics; the folder carries vault-structural semantics. Different surfaces; different bump triggers.
- *"Every `D-IH-*` row is a release event."* — No. `D-IH-*` rows are governance decisions; they accumulate in `[Unreleased]` and ride into the next tag if any. Most never warrant a tag of their own.
- *"The customer's PDF should carry the repo tag we ship under."* — No. Per §6 customer-invisible posture, customer-facing artefacts never carry repo / methodology / vault-folder version stamps.

---

## 6. Customer-invisible versioning posture (load-bearing)

> **Operator intent (codified verbatim):** *"intuitive clever versioning — do not let the customer know it's a new version."*

Versioning is **operator-internal infrastructure**. The customer's experience of a rendered artefact must be **the artefact they asked for**, not `revision 2 of the artefact after methodology refinements`. The posture below operationalises that intent across the five surfaces where version-shaped state could otherwise leak.

### 6.1 Five invariants

1. **Customer-facing engagement deliverables carry NO version stamp in the rendered PDF.** Cover page, footer, page headers, and embedded PDF metadata (PDF Producer, Author, Title, Subject, Keywords) carry no human-readable version number. The cover-strip 4-field carriage (per [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) `_build_cover_html()`) defines `engagement / discipline / language / date` — never `engagement / version / language / date`.
2. **Internal `LOGIC_CHANGE_LOG.md` + `D-IH-*` rows carry methodology version churn.** Operator and agents see this; customer does not. Per [`LOGIC_CHANGE_LOG.md`](../../../../People/canonicals/LOGIC_CHANGE_LOG.md) row schema, each breakthrough increments the methodology version with full audit trail.
3. **Git tag marks repo release baseline.** Developer-internal; the customer never sees `v3.1.0` stamped on a PDF, mentioned in cover-page metadata, or referenced in any customer-pack prose.
4. **Vault folder path (`v3.0/`) is structural.** Operator-internal; never surfaces in customer-facing prose. Path-portability rule per [`BRAND_COUNTERPARTY_README_CONTRACT.md`](../../../../Marketing/Brand/canonicals/BRAND_COUNTERPARTY_README_CONTRACT.md) Rule 2 forbids absolute repo paths in counterparty READMEs anyway.
5. **Rendered PDF metadata (Adobe PDF Producer / Author / Title / Subject / Keywords) optionally carries build-info for operator triage, but no human-readable version number.** Build-info may include a generated-at timestamp (`YYYY-MM-DD`) and the engagement_id (`ENG-SUEZ-WEBUY-2026`), which are operator-curated metadata, not version stamps. If the render pipeline ever needs to embed a build SHA for forensic traceability, it goes in a hidden technical metadata slot (e.g., `Keywords` or `Subject` field), not the human-readable cover or footer.

### 6.2 Customer-visible version churn happens via deliverable-name discipline only

When a customer asks for a revision (e.g., SUEZ requests proposal revisions after partner debrief), the operator may produce `proposal.customer.fr.v2.pdf` alongside (or replacing) the original `proposal.customer.fr.pdf`. The `vN` suffix is **operator-curated, never automatic**, and used only when the customer explicitly asked for revisions. Default deliverable-naming convention is **single canonical filename without `vN` suffix**; revisions are name-bumped only on operator instruction.

### 6.3 Worked example — I71 P6 closure (illustrative)

If I71 P6 closure ratifies a `v3.1.0` tag (operator decides at C-71-3 inline-ratify; default = hold for P6), the SUEZ deck (`deck.customer.fr.pdf`) re-renders to pick up any brand-canonical refinements that landed in I71 (e.g., Pack A1 strict-day-1 tic-family enforcement, Pack A2 Gantt confidence ladder, Addition 11 localised formats). The deck cover, footer, and PDF metadata carry **no "v3.1" stamp**. The customer opens the same `deck.customer.fr.pdf`, sees the canonical Holistika brand surface, and is unaware that the operator just tagged `v3.1.0` in `openclaw-akos`. The operator sees the version churn via internal `LOGIC_CHANGE_LOG.md` + `CHANGELOG.md` + `git log v3.1.0..HEAD`.

If the customer subsequently requests proposal revisions after a partner debrief (the SUEZ post-EFA-collaboration pattern from I12 P12), the operator-curated naming convention applies per §6.2: a deliberate `proposal.customer.fr.v2.pdf` may ship alongside the original — and only because the customer explicitly asked. The `v2` here is **engagement-side revision tracking**, not repo-side versioning; it has no relationship to the `v3.1.0` git tag or any methodology version.

### 6.4 Anti-patterns (the SUEZ-style leak posture this SOP closes)

The SUEZ deck's leaked AI-tone prose + leaked operator-instruction text at I70 P0 was a brand-failure release event masquerading as a documentation issue. The validator chassis shipped at I71 P1 + P2 (Pack A1 voice register + Pack A2 Gantt confidence + Pack A3 multilingual + Tier 1 Vale sibling) closes that failure mode at CI. This SOP's §6 closes the **versioning leak** version of the same failure class:

| Anti-pattern | Why it leaks | Mitigation |
|:---|:---|:---|
| Embedding `v3.1.0` in the customer-pack deck cover or footer | Customer reads "v3.1" as "this is the new version of my deck; what changed?" — opens a support conversation that did not need to exist. | §6.1 invariant 1: NO version stamp on cover / footer / page headers / PDF metadata. |
| Carrying methodology `v3.1` in cover-strip alongside `engagement` / `discipline` / `language` / `date` fields | Same leak; same customer reading. | §6.1 invariant 5: cover-strip carries operator-curated metadata only (engagement_id, discipline, language, date) — no version. |
| Render-script silently embedding the build SHA in PDF Title metadata | Adobe / preview apps surface this in a human-readable way; customer sees `<title>: openclaw-akos@a1b2c3d` and treats it as version drift. | §6.1 invariant 5: technical metadata (build SHA if any) lives in hidden Keywords / Subject fields; never human-readable Title / Author. |
| Renaming `deck.customer.fr.pdf` → `deck.customer.fr.v3-1-0.pdf` to "match the release" | Couples customer artefact filename to operator-internal version churn; future re-renders generate new filenames the customer must re-bookmark. | §6.2: filenames are operator-curated revisions only; never automatic; never coupled to repo tags. |

### 6.5 The five surfaces revisited (where leaks could happen)

The five invariants at §6.1 map to five concrete surfaces in the render pipeline + repo workflow where a leak could surface. Naming them explicitly makes review auditable:

1. **Cover-page surface** (slide 01 of decks; cover-hero of dossiers / proposals). Owned by Brand/Design + Brand/Copywriter; gated by §6.1 invariant 1.
2. **Footer / running-header surface** (every continuation page). Owned by Brand/Design via `_brand_pdf_css_slides()` primitives in `akos/hlk_pdf_render.py`. Gated by §6.1 invariant 1.
3. **PDF metadata surface** (Adobe PDF Producer / Author / Title / Subject / Keywords; surfaced by preview-app title bars and file-property dialogs). Owned by HLK Tech Lab (render-pipeline maintainer); gated by §6.1 invariant 5.
4. **Filename surface** (the literal PDF file name as it lands in `_exports/` and as it propagates through Drive sync). Owned by PMO + engagement lead; gated by §6.2 (operator-curated revision naming only).
5. **Cover-strip carriage surface** (the 4-field strip at the cover hero bottom; per `_build_cover_html()` carriage). Owned by Brand/Design + PMO; gated by §6.1 invariant 5 (no version field).

A render-pipeline review at PR time (per `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §16.2 per-deliverable owner-coverage check) MUST visit each of these five surfaces and confirm zero version leak before the engagement deliverable ships.

### 6.6 Cross-links to render-pipeline ownership

- [`BRAND_MULTILINGUAL_CONTRACT.md`](../../../../Marketing/Brand/canonicals/BRAND_MULTILINGUAL_CONTRACT.md) §3 — four-surface matrix; the customer-pack surface carries no operator-internal versioning surface.
- [`BRAND_COUNTERPARTY_README_CONTRACT.md`](../../../../Marketing/Brand/canonicals/BRAND_COUNTERPARTY_README_CONTRACT.md) — counterparty README carries engagement metadata, never repo or methodology version.
- [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) — render pipeline; metadata-field policy as codified at §6.1 invariant 5.
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §16 — render pipeline ownership; PMO + Brand co-own customer-visible artefacts. Per §16.1, the Brand/Copywriter row + PMO row are the two owners with hard veto rights on customer-visible prose; this SOP's §6 is the version-stamp policy they jointly enforce.

---

## 7. Cross-references

- [`CHANGELOG.md`](../../../../../../CHANGELOG.md) — openclaw-akos SemVer + `[Unreleased]` working line; policy header points to this SOP.
- [`LOGIC_CHANGE_LOG.md`](../../../../People/canonicals/LOGIC_CHANGE_LOG.md) — methodology `major.minor` lane carrier (per founder principle 2.6).
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §10 (release-policy SSOT cross-reference row) + §16 (render pipeline ownership matrix; per-deliverable owner-coverage check).
- I71 master-roadmap §P3: [`master-roadmap.md`](../../../../../../wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) — Strand C1 release-taxonomy ratification phase.
- I71 Cursor plan §P3: [`.cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_a71c0d6e.plan.md`](../../../../../../../.cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_a71c0d6e.plan.md) §P3 — full P3 plan body.
- `D-IH-71-D` — three-lane release-taxonomy ratification at I71 P0 (2026-05-13).
- `D-IH-71-P` — P3 ratification (this SOP authored + §6 customer-invisible versioning posture codified + C-71-3 tag-now-vs-hold verdict).
- `OPS-71-2` — closes at this commit with `closure_decision_id: D-IH-71-P` per `D-IH-71-D` discharge.
- Sibling I68 master-roadmap §release-cadence: [`master-roadmap.md`](../../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/master-roadmap.md) — consumer-repo CI baseline + InfraMonitor (own release cadence; cross-link only).
- Conventional commits convention: [`https://www.conventionalcommits.org/en/v1.0.0/`](https://www.conventionalcommits.org/en/v1.0.0/).
- Semantic Versioning 2.0.0: [`https://semver.org/spec/v2.0.0.html`](https://semver.org/spec/v2.0.0.html).
- Keep a Changelog 1.1.0: [`https://keepachangelog.com/en/1.1.0/`](https://keepachangelog.com/en/1.1.0/).
- [`PRECEDENCE.md`](../../../../People/Compliance/canonicals/PRECEDENCE.md) — canonical-vs-mirror authority contract; this SOP registers under "Canonical assets" with role_owner System Owner.
- [`CANONICAL_REGISTRY.csv`](../../../../People/Compliance/canonicals/CANONICAL_REGISTRY.csv) — row `sop_release_taxonomy_001` (added in this commit).
- I71 P3 phase report: [`reports/p3-release-taxonomy-2026-05-14.md`](../../../../../../wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p3-release-taxonomy-2026-05-14.md) — execution record + verification matrix.
- [`SOP-CICD_BASELINE_001.md`](SOP-CICD_BASELINE_001.md) — sibling System Owner SOP; defines per-class CI baseline (this SOP's release lanes complement that SOP's per-PR CI gates).

---

## 8. Maintenance + change control

This SOP follows the [`SOP-META_PROCESS_MGMT_001`](../../../../People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md) §4.5 review-and-maintenance cadence.

### 8.1 SOP version bumps follow §3 SemVer judgment applied to this SOP's own content

- **PATCH** — wording clarification; example refinement that preserves all contracts (e.g., adding a new anti-pattern row to §6.4 that codifies an existing prohibition; expanding §3.1 worked examples without changing the SemVer model).
- **MINOR** — additive sections (e.g., a new lane class introduced as a 4th lane; a new invariant in §6.1; a new section §9 covering new release surfaces such as Drive-distributed PDF release labelling).
- **MAJOR** — restructuring the three-lane model; changing the customer-invisible posture's load-bearing direction; breaking changes to the SemVer judgment table that would invalidate prior tag history reasoning. Operator-ratified breaking change required.

### 8.2 Operator review trigger

When this SOP's `last_review` is older than 12 months, or when any of the three lane carriers (LOGIC_CHANGE_LOG.md schema; vault folder; CHANGELOG.md) materially restructures, this SOP enters review. The reviewer is the role_owner (System Owner) with optional co-review from PMO (per WORKSPACE_BLUEPRINT §16) when the change touches render-pipeline ownership.

### 8.3 Validator hooks

This SOP has no dedicated validator (it is doctrine, not enforceable schema). The lane carriers have their own validators:
- `LOGIC_CHANGE_LOG.md` row schema is validated by the `validate_hlk.py` language frontmatter check and `last_review` cadence.
- `CHANGELOG.md` `[Unreleased]` discipline is reviewed by operator eye + the docs-config-sync cursor rule pattern; no script gate.
- Git tag presence on `origin/main` is observable via `git tag --list` and the operator's release-judgment ritual at C-71-3-shaped inline-ratify gates.
- The CSV-side reference for this SOP is registered in [`CANONICAL_REGISTRY.csv`](../../../../People/Compliance/canonicals/CANONICAL_REGISTRY.csv) row `sop_release_taxonomy_001` and tracked by `validate_canonical_registry.py`.

### 8.4 Forward-looking notes (not commitments)

- A future `validate_pdf_metadata_no_version_leak.py` validator could mechanically enforce §6.1 invariant 1 + invariant 5 at render-time, reading rendered PDFs in `_exports/` and asserting zero version-string matches in cover-strip / footer / metadata. Scoping deferred until either (a) a leak is observed in the wild, or (b) sibling I72 Marketing Area Governance RevOps activation surfaces the need.
- A future cross-lane coherence dashboard (one panel under `op_governance_release_coherence` in the HLK-ERP `/operator/governance/` namespace) could surface the three lanes side by side: latest methodology row, current vault folder, latest git tag — for operator at-a-glance. Reserved as an I72+ candidate; not in I71 scope.
- If `inframonitor.com` ever spins out per the I69 candidate, this SOP's customer-invisible posture extends naturally: an InfraMonitor SaaS customer should also never see their version in the rendered artefact (same five invariants apply; the tenant-isolation question is orthogonal).
