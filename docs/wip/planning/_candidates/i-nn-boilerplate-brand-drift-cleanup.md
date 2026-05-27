---
language: en
intellectual_kind: initiative_candidate
sharing_label: internal_only
audience: J-OP
authored: 2026-05-27
last_review: 2026-05-27
status: candidate
parent_canonical: docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
forward_charter_source: I86 Wave R+3 SUEZ POC SEND PACK closing-loop release-gate verdict 2026-05-27
ratifying_decisions:
  - D-IH-86-ET
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ENGLISH_PATTERNS.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_FRENCH_PATTERNS.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_LLM_TONE_TELLS.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_COPYWRITING_DISCIPLINE.md
  - docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORY_REGISTRY.csv
external_references: []
---

# Candidate — I-NN: Boilerplate brand-voice register drift cleanup (sibling-repo i18n hygiene)

## Purpose

Address the 4 pre-existing brand-voice register drift errors surfaced
in the sibling `boilerplate` repository's i18n message files during
the I86 Wave R+3 SUEZ POC SEND PACK closing-loop release-gate
verification (2026-05-27). These errors are pre-existing (NOT
regressions from the SUEZ Wave R+3 tranche) but they fail the
`validate_brand_voice_register.py --strict` check at every cross-repo
release-gate run, which clutters the release-gate signal and prevents
clean cluster-coordinator closing-loop verdicts.

The 4 errors (from validator output 2026-05-27):

1. `root_cd/boilerplate/i18n/messages/en.json` →
   `techLab.platforms.kirbe.description` contains "enterprise-grade"
   (EN MBA-deck jargon; replace with the specific reliability claim
   per `BRAND_ENGLISH_PATTERNS.md` §5.1 Stack-vendor language rule).

2. `root_cd/boilerplate/i18n/messages/en.json` →
   `manifiesto.holistika.sections.pincerEffect.content3` contains
   `delve into` (LLM tone tell T-3 — one of the strongest LLM-tells
   in 2024-2026 EN-corporate prose; replace with `look at`, `study`,
   `examine`, or `dig into` per `BRAND_LLM_TONE_TELLS.md`).

3. `root_cd/boilerplate/i18n/messages/en.json` →
   `manifiesto.kirbe.description` contains "enterprise-grade" (same
   class as error 1; replace with the specific reliability claim).

4. `root_cd/boilerplate/i18n/messages/fr.json` →
   `entities.title` contains an AI-tone tic family F3 (false-singularity
   pattern; keep concrete idiomatic uses like `une seule fois` /
   `une seule personne` but drop epigrammatic uses on H2 / cover
   slides per `BRAND_COPYWRITING_DISCIPLINE.md` §2).

## Origin (forward-charter)

Surfaced as a categorised release-gate `[FAIL]` during the I86 Wave R+3
SUEZ POC SEND PACK closing-loop release-gate verification 2026-05-27.
The operator's standards-directive (*"are we sure that everything went
as we expected? Did you see every process involved correctly? Is it
impeccable? If it is, then continue directly with no stop, if it's
not, fix and continue but we have solid standards and we need to
uphold them. Everytime"*) prompted the categorisation of all 4
release-gate FAILs:

- **Test suite FAIL** → release-gate transient (standalone PASS = 3468/17/0).
- **Browser smoke FAIL** → environmental (local FastAPI dashboard +
  Docker Desktop not running).
- **BRAND voice register FAIL** → THIS candidate (sibling-repo i18n
  drift; not a Wave R+3 regression).
- **BRAND voice Vale sibling FAIL** → design-default per D-IH-71-O
  (Vale exit=2 expected when no Vale rules are configured against
  the JSON strings).

The Wave R+3 tranche scope (4 SUEZ engagement-class commits + 1 chore
hygiene) introduced ZERO of these 4 release-gate FAILs. Therefore
this candidate is surfaced as a durable forward-pointer rather than
folded into Wave R+3 scope (which would conflate engagement-class
work with sibling-repo brand-hygiene work).

Per `akos-conflict-surfacing-and-blocker-trackers.mdc` Option-5
default posture: surface the sibling-repo drift as a candidate file
rather than over-extend the in-flight tranche OR silently defer.

## Activation criteria (when this candidate promotes to an active initiative)

1. Operator confirms readiness to open a PR against the sibling
   `boilerplate` repository (per `REPOSITORY_REGISTRY.csv` bless
   pattern + `akos-mirror-template.mdc` AKOS-as-SSOT preservation).
2. The translation prose per error has been resolved (would benefit
   from operator sign-off on the replacement strings since they are
   user-facing copy).
3. A successor decision ID `D-IH-NN-A` is minted naming the cleanup
   tranche scope.

## Scope (when promoted)

Lightweight 1-commit initiative under `docs/wip/planning/<NN-slug>/`:

- **Files in scope (sibling repo `boilerplate`)**:
  - `i18n/messages/en.json` (2 edits: `techLab.platforms.kirbe.description`
    `enterprise-grade` → specific reliability claim;
    `manifiesto.kirbe.description` `enterprise-grade` → same shape;
    `manifiesto.holistika.sections.pincerEffect.content3` `delve into`
    → `look at` / `study` / `examine` / `dig into`).
  - `i18n/messages/fr.json` (1 edit: `entities.title` AI-tone tic
    family F3 false_singularity replacement).
- **Files in scope (AKOS-side bookkeeping)**:
  - `docs/wip/planning/<NN-slug>/master-roadmap.md` (single-phase
    roadmap with closure criteria = validator re-run PASS).
  - `docs/wip/planning/<NN-slug>/files-modified.csv` (per-initiative
    file-changes CSV per `akos-planning-traceability.mdc`).
  - `CHANGELOG.md` entry under `[Unreleased]`.
  - `DECISION_REGISTER.csv` +1 active row.
- **Verification**:
  - `py scripts/validate_brand_voice_register.py --strict` PASS
    (4 errors → 0).
  - `py scripts/release-gate.py` BRAND voice register check returns
    PASS instead of FAIL.

## Cross-references

- `BRAND_BASELINE_REALITY_MATRIX.md` (parent canonical; dual-register
  contract that this candidate operationalises in the sibling-repo
  prose surface).
- `BRAND_ENGLISH_PATTERNS.md` §5.1 (Stack-vendor jargon rule for
  errors 1 + 3).
- `BRAND_LLM_TONE_TELLS.md` (T-3 `delve-into` rule for error 2).
- `BRAND_FRENCH_PATTERNS.md` (FR register rule for error 4 — FR
  AI-tone tic family).
- `BRAND_COPYWRITING_DISCIPLINE.md` §2 (epigrammatic-on-cover-slides
  anti-pattern; error 4).
- `.cursor/rules/akos-brand-baseline-reality.mdc` (cursor rule for
  the dual-register contract).
- `.cursor/rules/akos-mirror-template.mdc` (sibling-repo bless
  discipline; AKOS-as-SSOT preservation).
- `REPOSITORY_REGISTRY.csv` (`boilerplate` repo entry; hosting +
  bless-pattern + CI baseline).
- `scripts/validate_brand_voice_register.py` (the validator that
  surfaced the 4 errors).
- I86 Wave R+3 SUEZ POC SEND PACK closing-loop release-gate verdict
  drain entry at `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md`
  (the originating context).
- D-IH-86-ET (ratifying decision row for the I86 Wave R+3 SUEZ POC
  SEND PACK tranche close, at which this candidate file was first
  authored).
