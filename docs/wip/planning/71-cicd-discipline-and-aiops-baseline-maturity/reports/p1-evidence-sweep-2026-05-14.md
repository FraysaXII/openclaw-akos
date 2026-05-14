# I71 P1 Pack A1 — Evidence sweep (pre-flight consolidation)

> Authored 2026-05-14 at the start of P1 agent-mode execution. Phase 1.2 of the Cursor plan at `.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md`. **No code edits in this phase** — this report consolidates the synthesized facts from the plan's three research rounds so that P1.3–P1.10 execute from a single grounded source. Read this before authoring `akos/brand_voice_register.py` (P1.4) or the validator extension (P1.5).

Scope of the sweep: brand canonicals (`BRAND_COPYWRITING_DISCIPLINE.md` §2 / `BRAND_REGISTER_MATRIX.md` / `BRAND_GANTT_DISCIPLINE.md` §2 / `BRAND_BASELINE_REALITY_MATRIX.md` §3); decision register (`D-IH-70-X`, `D-IH-71-A..E`, `D-IH-71-F..Z` availability); chassis precedents (`akos/cicd_baseline.py` / `akos/sentry_release.py` / `akos/playwright_baseline.py`); current validator surface (`scripts/validate_brand_voice_register.py` / `scripts/release-gate.py`); orthogonal-active classification of `scripts/lint_brand_voice_offline.py`; the 6-canonical forward-charter A5+ grounding inventory. Confirms I71 P0 closure.

## 1. I71 P0 closure (confirmed)

- `INIT-OPENCLAW_AKOS-71` row in `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` is `status: active`; `inception_decision_id = D-IH-71-C` (charter row).
- P0 commits shipped 2026-05-13: `e129bac` (charter + decision rows) + `eb4c1b4` (closure follow-up). Report: [`reports/p0-charter-2026-05-13.md`](./p0-charter-2026-05-13.md).
- Ratified at P0: `D-IH-71-A` (four validator packs); `D-IH-71-B` (Sentry+Langfuse AIOps); `D-IH-71-C` (charter); `D-IH-71-D` (three-lane release taxonomy); `D-IH-71-E` (review-stamp dimension).
- Minted at P0: `OPS-71-1` (validator-pack execution); `OPS-71-2` (release-taxonomy steward); `OPS-71-3` (review-stamp dimension).
- `WORKSPACE_BLUEPRINT_HOLISTIKA.md §18` (observability routing matrix) added at P0 closes the cross-system contract for AIOps strand B baseline.
- Strand C scope expanded at P0 to include the review-stamp dimension (`D-IH-71-E`).

## 2. D-IH-71 ID availability for P1 (confirmed)

- D-IH-71-A through D-IH-71-E exist (P0 rows). See `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv` lines 115-119.
- D-IH-71-F through D-IH-71-Z **unused** — verified by grep `^D-IH-71-[F-Z],` returning zero matches.
- P1 plan reserves D-IH-71-F..K (6 new rows authored at P1.8): F (strict-day-1 day-1 enforcement); G (Pydantic chassis pattern); H (3-axis audience matrix); I (Storytelling/Resonance boundary); J (release-gate row extension policy); K (Round 3 brand-DNA Layers 5-9 scope).

## 3. BRAND_COPYWRITING_DISCIPLINE.md §2 — seven AI-tone tic families (verbatim)

Canonical at `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/Copywriter/canonicals/BRAND_COPYWRITING_DISCIPLINE.md`. The 7 families live in **§2** (not §3 as a prior draft of this plan implied). Eleven anti-pattern seeds with positive-claim replacements live in §3 (table). Per-language register considerations in §4. Validator-rule-pack contract in §5 (deferred to I71 — i.e., this phase).

| # | Name (canonical) | Locales | Detection regex (verbatim from canonical) | Replacement strategy |
|:---:|:---|:---|:---|:---|
| F1 | contrastive `X, pas Y.` / `X, not Y.` / `X, no Y.` | FR / EN / ES | FR: `\b\w+, pas \w+\.`<br>EN: `\b\w+, not \w+\.` | Drop the negation; assert the positive directly. Pull a concrete operational fact into the sentence. |
| F2 | chained negation-then-affirmation `n'est pas X. C'est Y.` / `is not X. It's Y.` | FR / EN | FR: `n'est pas .{1,40}\.\s*C'est`<br>EN: `is not .{1,40}\.\s*It's` | Collapse to a single sentence with `réside dans` / `lies in` / `consiste en` instead of the negation-affirmation pair. |
| F3 | false-singularity `une seule X` / `a single X` / `una sola X` | FR / EN / ES | FR: `\b(une\|un) seule? \w+\b` (idiomatic uses like `une seule fois` allowed via context check) | Keep concrete idiomatic uses (`une seule fois`, `una sola vez`, `a single person`); drop epigrammatic uses on H2 / cover slides. |
| F4 | triadic abstract-noun stack `noun-phrase, noun-phrase, noun-phrase` | all | Sentence with 2+ commas separating noun phrases that don't include verbs or concrete numbers. | Replace at least one element with a concrete number drawn from the operational reality. If three abstracts are needed, demand a verb anchor. |
| F5 | `discipline` overuse | FR (primary); EN softer | Count `Discipline` in `<h3 class="anchor-title">` siblings; flag if ≥3 in 30 lines. | Replace each with the **anchor frame** (active verb describing what the discipline does), not the methodology-tag. |
| F6 | repeated openings `C'est le X qui...` / `It's the X that...` | FR / EN | Three or more sibling `<p>` elements with identical 4-token openings. | Vary openings; let second and third openings be different sentence structures; force concreteness. |
| F7 | operator-instruction echo | all | Phrase patterns: `(présentation à\|démontrer\|montrer\|ce document a pour objectif\|nous présentons\|cette présentation vise\|presentation to\|in this document\|this document aims\|we present here)` | Replace with imperative-form claim about what the deliverable DOES; never describe the deliverable itself. |

Severity model per §5: **error** for cover slides + customer-pack body prose; **warning** for operator-pack body prose; **info** for internal canonicals. Allowlist per `<!-- copy-discipline-allow: F1 -->` HTML comment for deliberate rhetorical uses.

The 11 anti-pattern seeds in §3 (replacement table) map each anti-pattern to its tic family — these become positive-claim suggestions emitted alongside each validator hit at P1.5.

## 4. BRAND_REGISTER_MATRIX.md — six register tokens

Canonical at `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_REGISTER_MATRIX.md`. The matrix maps `(relationship × channel) → register`. Auto-emitted by `scripts/wave2_backfill.py --section brand_voice` from `operator-answers-wave2.yaml` Section 2; **do not hand-edit**.

| Relationship | Channel | Register token |
|:---|:---|:---|
| external_counsel | email | `formal_legal` |
| peer_founder | dm | `peer_consulting` |
| regulator | memo | `regulator_neutral` |
| investor | deck | `investor_aspirational` |
| client_prospect | proposal | `peer_consulting` |
| internal_team | slack | `casual_internal` |

Common register tokens: `formal_legal`, `peer_consulting`, `casual_internal`, `regulator_neutral`, `investor_aspirational`. Composer (`scripts/compose_adviser_message.py`, I24 P4) is the upstream consumer. Pack A1 Layer 3 (audience-formality matrix) loads these tokens via `parse_register_matrix` and asserts each (relationship, channel) cell expected for the engagement deck is mapped before render.

## 5. BRAND_GANTT_DISCIPLINE.md §2 — 4-quadrant audience matrix

Canonical at `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/UX Designer/canonicals/BRAND_GANTT_DISCIPLINE.md`. The 4 quadrants live in **§2** (audience-formality × data-maturity).

| | Low data maturity | High data maturity |
|:---|:---|:---|
| **Customer-facing** | Variant A — Posture sketch (no dates; phase ribbons; ratify-via-discovery) | Variant B — Proof of discipline (concrete dates; per-phase deliverables; per-phase ownership) |
| **Operator-internal** | Variant C — Hypothesis sketch (cross-linked sources; assumption flags; revisit cadence) | Variant D — Execution plan (granular weekly task breakdown; dependency arrows; resource allocation) |

Pack A1 Layer 3 (audience-formality matrix) reuses Variant A/B/C/D as the **3-axis audience matrix** primary key (audience × formality × data-maturity), with the formality axis derived from the parent register token. The synthesis is: every engagement-facing prose surface declares a `(variant, register_token)` pair in frontmatter; the validator asserts the prose register matches the variant's tonal envelope.

Confidence ladder per §4 (band 1-5: Reserved / Hypothesis / Posture / Probable / Confirmed). Pack A1 Layer 3 does not enforce confidence-band copy (that is Pack A2 — Gantt confidence; deferred to I71 P2 per master-roadmap).

## 6. D-IH-70-X — Storytelling AUTHORS / Resonance CONSUMES boundary (verbatim)

`DECISION_REGISTER.csv` row 107:

> `D-IH-70-X,P2.5 spot-check Q4 (D-IH-70-B sub): Corporate Marketing placement + Storytelling/Resonance boundary,INIT-OPENCLAW_AKOS-70,...`
>
> *Verdict ratified: `opt-marketing-storytelling`. Corporate Marketing moves to `Marketing/Storytelling/Corporate Marketing/`. **Forward-context boundary contract** (load-bearing for P8 section 8.4): **Storytelling AUTHORS narrative artifacts** (case studies, PR, thought-leadership content); **Resonance CONSUMES** (Account Management + Community Manager deploy artifacts in 1:1 relationship contexts). Single-ownership preserved by separating verbs author-vs-deploy.*

Pack A1 Layer 4 (Storytelling/Resonance boundary) enforces this: any artifact whose frontmatter declares `area: Resonance` is **read-only** with respect to its narrative content (the validator refuses on edit if narrative diff > X tokens vs the upstream Storytelling artifact). The boundary is the validator's signature contribution to D-IH-70-X durability.

## 7. BRAND_BASELINE_REALITY_MATRIX.md §3 — translation rules

Canonical at `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md` §3. Twenty-three internal→external token pairs (selected for evidence here; full table at canonical).

| Internal vocabulary (restricted) | External canonical translation |
|:---|:---|
| counterparty | client / partner / advisor / candidate / contributor / investor / reviewer (audience-specific) |
| baseline reality | reading lens / audience reading / market context |
| elicitation | discovery interview / structured conversation / scoping interview |
| reliability grading | source confidence / evidence quality |
| intelligence collection | structured research / evidence gathering |
| intelligence report | research brief / engagement summary |
| approach techniques | discovery methodology |
| asset (in HUMINT sense) | NEVER use externally; rephrase entirely |
| cover (in HUMINT sense) | NEVER use externally; rephrase entirely |
| sub-source primacy | NEVER use externally; rephrase entirely |

Pre-existing drift gate: `scripts/validate_brand_baseline_reality_drift.py` (I66 P2). Pack A1 does **not** duplicate this scan — Pack A1 Layer 7 (locale-leak) instead asserts that English/French/Spanish locale variants of the same key are register-consistent (per Layer 1-3) AND that none re-introduces an internal-register token. The drift gate remains the SSOT for token-presence detection.

## 8. Chassis precedents — `akos/cicd_baseline.py` + sibling Pydantic modules

`akos/cicd_baseline.py` is the canonical chassis pattern (I68 P5 / D-IH-68-D, D-IH-68-J):

- `RepoClass = Literal["platform", "reference", "internal", "client-delivery"]` — string-enum via `Literal`.
- `KNOWN_CHECK_OPTOUTS: frozenset[str]` — known-token surface via frozen sets.
- `PER_CLASS_REQUIRED_CHECKS: dict[RepoClass, frozenset[str]]` — per-class invariants via dict-of-frozenset.
- `class CICDBaselineRow(BaseModel)` — Pydantic `BaseModel` with `Field(...)` + `field_validator` decorators.
- `from_registry_row` classmethod — forward-compatible CSV→model adapter (tolerates absence of new columns until the canonical CSV gate lands).

Sibling references:
- `akos/sentry_release.py` — release-format + skip-on-preview models for I68 P4.
- `akos/playwright_baseline.py` — viewport baseline model for I68 P2.

**Pack A1 mints `akos/brand_voice_register.py` (P1.4) following the same chassis:** `TicFamily` (Pydantic BaseModel with `name`, `locales: list[Literal[...]]`, `pattern: str`, `replacement_template: str`, `severity: Literal["error","warning","info"]`); `RegisterRule` (existing dataclass promoted to Pydantic + extended); `AudienceQuadrant`, `RegisterToken`, `AudienceClass`, `BoundaryRule`, `BrandVoiceRegisterPack` (composite); plus Round 3 additions `SubMarkTier`, `VoicePersona`, `EngagementType`, `ArchetypeViolation`, `BrandedHouseViolation` for Layers 5-9. Constants: `STANDARD_TIC_FAMILY_NAMES`, `CANONICAL_PATHS`. Helpers: `parse_tic_families_from_canonical`, `parse_english_register_rules`, `parse_register_pack_yaml`.

## 9. `scripts/validate_brand_voice_register.py` — current surface (extension target)

I66 P2 implementation (377 lines). Current shape:

- **Dataclass** `RegisterRule(frozen=True)`: `locale`, `token`, `pattern: re.Pattern`, `rationale`, `canonical_source`.
- **Parsers:**
  - `_extract_french_anglicisms(path)` — parses BRAND_FRENCH_PATTERNS.md §5.1 anglicism table (regex `^\|\s*` `[anglicism]` `\s*\|\s*` `[replacement]` `\s*\|`).
  - `_french_performative_patterns(path)` — hard-coded 4 FR performative tokens citing §5.2.
  - `_spanish_register_rules(path)` — hard-coded 9 ES tokens citing §13 (humility + vague-time + 5 anglicisms).
  - `_load_rules()` — composes all three.
- **Scanner:** `_walk_json_keys(value, path_parts)` yields `(json.path, leaf-string)`. `_file_locale(path)` derives locale from stem (`en` / `es` / `fr` / `en-us` / `es-es` / `fr-fr`). `_scan_message_file(path, rules)` scans one JSON file against locale-relevant rules.
- **Consumer resolution:** `_resolve_consumer_roots(extra)` — accepts `--consumer-root` extras; defaults to sibling `root_cd/boilerplate` + `root_cd/hlk-erp`; resolves + dedupes.
- **CLI:** `main(argv)` — flags `--json-log`, `--consumer-root` (repeatable), `--strict-empty`. Returns 0 (no drift) / 1 (hits or strict-empty miss).

**P1.5 extension target:** wrap existing FR/ES rules as **Layers 0-1** (unchanged behavior, strict-mode preserved); add Layer 2 (7 tic families × multi-locale) via new parser `_extract_tic_families_from_copywriting_discipline(path)`; add Layer 3 (audience-formality × data-maturity × register-token); Layer 4 (Storytelling/Resonance boundary); Layers 5-9 (Round 3 brand-DNA). Author `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/register-pack.yml` as the operator-editable YAML pack consumed by `parse_register_pack_yaml`.

## 10. `scripts/release-gate.py` — voice-register row (extension target)

Confirmed at `scripts/release-gate.py`:

- Lines 250-266: `run_brand_voice_register_validation()` — runs the validator with no extra args; captures success + returncode.
- Line 487-494: row insertion logic:
  ```python
  voice_ok, voice_rc = run_brand_voice_register_validation()
  if os.environ.get("AKOS_BRAND_VOICE_REGISTER_SOFT") == "1":
      results.append(("INFO", f"BRAND voice register (... soft mode opted-in via AKOS_BRAND_VOICE_REGISTER_SOFT=1; exit={voice_rc})"))
  else:
      results.append(("PASS" if voice_ok else "FAIL", "BRAND voice register (scripts/validate_brand_voice_register.py, strict — default since I66 P5 incr 3)"))
  ```

**P1.7 extension target (D-IH-71-J):** edit the existing FAIL-branch row text **in-place** to read: `"BRAND voice register (scripts/validate_brand_voice_register.py, strict — default since I66 P5 incr 3 + I71 P1 Pack A1 expansion: 7 tic families + EN locale + 3-axis audience matrix + Storytelling/Resonance boundary + Round 3 Layers 5-9)"`. **No new row.** Soft-mode escape via `AKOS_BRAND_VOICE_REGISTER_SOFT=1` preserved unchanged (Layer 8 strict-day-1 promotion is a Layer-internal severity decision, not a top-level row-promotion).

## 11. `scripts/lint_brand_voice_offline.py` — orthogonal-active (OUT of P1 scope)

`scripts/lint_brand_voice_offline.py` (I49 P12) scans external-facing markdown/YAML for forbidden tokens defined in `BRAND_JARGON_AUDIT.md §4` (internal codenames, stack jargon, methodology shorthand, operator-side process tokens). Pure regex; offline; pre-commit-friendly.

Classification: **orthogonal-active**. Pack A1 does not consume from or modify `lint_brand_voice_offline.py`. The two scripts share spirit (brand drift detection) but **operate on disjoint token surfaces**:
- `lint_brand_voice_offline.py` → jargon (token-list scan; locale-agnostic; external surfaces).
- `validate_brand_voice_register.py` → register (locale-aware patterns; JSON-message i18n files; extended at P1 to all locales × tic families × audience matrix × boundary).

**Forward-charter** (I-NN-TBD): a follow-up initiative consolidates §4 jargon sourcing with `validate_brand_jargon.py` (the canonical jargon validator) so that `lint_brand_voice_offline.py` becomes a thin pre-commit caller of the same rule pack. Out of P1 scope; raised at P1.8 as a forward-charter note.

## 12. Six-canonical forward-charter A5+ grounding inventory

P1 ships Pack A1 (the voice-register validator). Packs A2-A5 (Gantt confidence; multilingual render; render-ownership routing; future packs) are forward-charter; their input surfaces:

| Canonical | Path | A5+ role |
|:---|:---|:---|
| CHANNEL_TOUCHPOINT_REGISTRY | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` | Per-channel touchpoint enumeration (Pack A4 routing). |
| CHANNEL_STRATEGY | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/business-strategy/CHANNEL_STRATEGY.md` | Channel-level strategy doctrine (Pack A4 routing). |
| WORKSPACE_BLUEPRINT_HOLISTIKA §1 | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md` | §1 ownership matrix + §16 Brand/Copywriter row + §18 observability routing (Pack A1 P1.7 ref). |
| HOLISTIK_OPS_DISCOVERY (6-axis) | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md` | 6-axis doctrine for cross-pack discipline tagging (forward charter). |
| BRAND_TEMPLATE_REGISTRY | (TBD — not yet present per glob; forward-charter item) | Per-template (deck / dossier / proposal / gantt) channel + register mapping. |
| FIGMA_FILES_REGISTRY | (TBD — not yet present per glob; forward-charter item) | Per-Figma-file ownership + sub-mark mapping (Pack A5 visual-render-ownership). |

**Note on TBD items:** `BRAND_TEMPLATE_REGISTRY.csv` and `FIGMA_FILES_REGISTRY.csv` are referenced in the P1 plan as forward-charter surfaces but do not yet exist on disk per the glob sweep. P1.8 emits a master-roadmap §P-future note to charter their creation alongside Pack A5 (visual-render ownership) in a downstream initiative. Pack A1 does **not** depend on them.

## 13. Round 3 brand-DNA additions — Layers 5-9 source map

Per the plan §"Brand-DNA additions (Round 3)" — Tier-1 additions (8 of 11) folded into P1 across Layers 5-9. Tier-2 additions (2 of 11) folded as best-effort. Tier-3 (1 of 11) deferred to I71 P2.

| Layer | Source canonical | Pack A1 surface |
|:---:|:---|:---|
| 5 | `BRAND_ARCHITECTURE.md` (Branded House) + sub-mark tier registry | `SubMarkTier`, `ArchetypeViolation`, `BrandedHouseViolation` |
| 6 | (TBD) Voice-persona + engagement-type maps | `VoicePersona`, `EngagementType` |
| 7 | `BRAND_FRENCH_PATTERNS.md` + `BRAND_SPANISH_PATTERNS.md` + cobrand rules | Locale-leak detection (cross-key); cobrand surface check |
| 8 | `BRAND_LLM_TONE_TELLS.md` (new — minted P1.3) | 15-25 anti-LLM-tone EN-corporate patterns; strict-day-1 per C-71-8 |
| 9 | `BRAND_BASELINE_REALITY_MATRIX.md` §"Anonymized track record" + `BRAND_ABBREVIATIONS.md` | Track-record format guard; brand-abbreviation surface |

Layer 8 (BRAND_LLM_TONE_TELLS.md) is the **most novel addition** — operator override at C-71-8 set its severity to **strict-day-1** rather than soft-30-day default. This means anti-LLM-tone violations fail the release gate on day one of I71 P1's commit. The 15-25 patterns are authored at P1.3 (this is the work-in-progress phase) with per-token severity for granular operator tuning.

## 14. Strictness ladder (defaults + overrides)

Per the plan §"Inline-ratified decisions":

- **D-IH-71-F** — **strict-day-1** for all of Layers 0-9 (operator pre-ratified at plan-finalization; no fresh `AskQuestion` at P1.5).
- **C-71-8 verdict** — Layer 8 (anti-LLM-tone) strict-day-1 (operator override of the suggested soft-30-day default; explicit decision recorded).
- **AKOS_BRAND_VOICE_REGISTER_SOFT=1** env escape remains the soft-INFO opt-out for emergency-only operator triage (unchanged from I66 P5 incr 3).

The validator authors per-rule severity (`error` / `warning` / `info`) per the §5 contract; a top-level strict-day-1 means **the gate fails on any `error`-severity hit, regardless of layer.** Operators can downgrade per-rule severity in `register-pack.yml` for false-positive cases without flipping the global strict-day-1 default.

## 15. P1 deliverable inventory (forward map)

For each pending sub-step, the plan ships the following artifacts. P1.2 (this report) is the consolidation pivot; P1.3-P1.10 execute against this map.

| Sub-step | Output | Path / surface |
|:---:|:---|:---|
| P1.3 | 3 new canonicals + CANONICAL_REGISTRY rows | `BRAND_ENGLISH_PATTERNS.md`, `Brand/canonicals/_validators/README.md`, `BRAND_LLM_TONE_TELLS.md`; `CANONICAL_REGISTRY.csv` 3 rows; `PRECEDENCE.md` classification |
| P1.4 | Pydantic chassis | `akos/brand_voice_register.py` (~400-600 LOC); `docs/ARCHITECTURE.md` Orchestration Library table touch |
| P1.5 | Validator extension + YAML pack | `scripts/validate_brand_voice_register.py` (extend; +400-800 LOC); `Brand/canonicals/_validators/register-pack.yml` (new) |
| P1.6 | Tests + marker + profile | `tests/test_validate_brand_voice_register_expansion.py`; `pyproject.toml` (`@pytest.mark.brand`); `scripts/test.py` (brand group); `config/verification-profiles.json` (brand_voice_register_smoke); backfill `tests/test_validate_brand_drift_gates.py` |
| P1.7 | Release-gate row + routing | `scripts/release-gate.py` (in-place edit); `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §16 + §18 |
| P1.8 | Registers + canonicals touch + planning artifacts | `DECISION_REGISTER.csv` (D-IH-71-F..K); `OPS_REGISTER.csv` (OPS-71-1 notes); `INITIATIVE_REGISTRY.csv` (notes); `master-roadmap.md` (§P1 + §P2 corrections); `files-modified.csv`; `reports/p1-pack-a1-2026-05-14.md`; `CHANGELOG.md` |
| P1.9 | Verification matrix run | 11-step gate; STOP at first FAIL with 5-line blocker report |
| P1.10 | UAT browser-MCP + atomic commit | `reports/p1-uat-browser-2026-05-14.md`; single atomic phase-scoped commit; push to `origin/main` |

## 16. Cross-references (index)

- Plan: [`.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md`](../../../../../.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md).
- Master roadmap: [`../master-roadmap.md`](../master-roadmap.md).
- P0 charter: [`./p0-charter-2026-05-13.md`](./p0-charter-2026-05-13.md).
- Brand canonicals (read first): `BRAND_COPYWRITING_DISCIPLINE.md` §2; `BRAND_REGISTER_MATRIX.md`; `BRAND_GANTT_DISCIPLINE.md` §2; `BRAND_BASELINE_REALITY_MATRIX.md` §3.
- Decision register: D-IH-70-X (boundary), D-IH-71-A..E (P0 ratified), D-IH-71-F..K (P1 reserved).
- Chassis precedents: `akos/cicd_baseline.py`, `akos/sentry_release.py`, `akos/playwright_baseline.py`.
- Validator surfaces: `scripts/validate_brand_voice_register.py` (extend); `scripts/release-gate.py` line 250-266 + 487-494 (extend in-place); `scripts/lint_brand_voice_offline.py` (orthogonal-active; out of scope).
- Governance rules: `.cursor/rules/akos-governance-remediation.mdc`, `.cursor/rules/akos-planning-traceability.mdc`, `.cursor/rules/akos-inline-ratification.mdc`, `.cursor/rules/akos-brand-baseline-reality.mdc`.

End of evidence sweep. Proceeding to P1.3 (canonical fragments authoring).
