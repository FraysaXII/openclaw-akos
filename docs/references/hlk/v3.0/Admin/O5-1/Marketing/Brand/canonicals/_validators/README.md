---
language: en
status: active
role_owner: Brand & Narrative Manager
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: brand_asset
authority: Founder + Brand Manager
last_review: 2026-05-14
ssot: true
authored: 2026-05-14
---

# Brand `canonicals/_validators/` — operator-editable rule packs (index)

> **Status — Active (Initiative 71 P1; minted alongside `register-pack.yml`).** This folder is the brand-wide home for **operator-editable rule packs** that customize the brand-voice-register validator's behavior. Rule packs in this folder are YAML; consumed by the `parse_register_pack_yaml` helper in `akos/brand_voice_register.py` at runtime; loaded by `scripts/validate_brand_voice_register.py` (extended at I71 P1 Pack A1) before the per-locale scan.

## Why this folder exists

Three reasons:

1. **Operator override surface.** The canonical markdown documents (`BRAND_COPYWRITING_DISCIPLINE.md`, `BRAND_ENGLISH_PATTERNS.md`, `BRAND_LLM_TONE_TELLS.md`, `BRAND_FRENCH_PATTERNS.md`, `BRAND_SPANISH_PATTERNS.md`) are the authoritative catalogs — they declare which patterns exist and what their default severity is. The operator may need to **downgrade** a specific pattern's severity (false-positive in a particular surface), **upgrade** a warning to error (when a specific surface needs stricter enforcement), or **allowlist** a specific token within a specific surface. The YAML pack is the operator-editable surface for these overrides.
2. **Source-of-truth separation.** Markdown canonicals are human-authored prose; YAML packs are machine-parsed configuration. Mixing them in a single file creates churn (every operator override forces a markdown-canonical edit; every catalog expansion forces a YAML touch). Separation lets each evolve at its own cadence.
3. **Validator-internal SSOT for runtime rule resolution.** The validator's `parse_register_pack_yaml` reads the pack at scan-time, applies overrides over the canonical defaults, and emits the final per-rule severity map. The YAML pack is the **final word** at runtime; markdown is the source of truth for the canonical list.

## Contents (as of I71 P1)

| File | Role | Updated by |
|:---|:---|:---|
| `register-pack.yml` | Single YAML pack covering all 10 layers of the brand voice register validator (FR / ES / EN locale rules; tic families; audience matrix; Storytelling/Resonance boundary; Round 3 brand-DNA Layers 5-9). | I71 P1 Pack A1; subsequent operator edits per `MAINTENANCE.md` (forward-charter). |

Forward-charter (deferred to future initiatives):

- `MAINTENANCE.md` — operator-facing guide for editing `register-pack.yml` (when to downgrade / upgrade severity; allowlist syntax; how to test overrides locally; how to PR the change).
- Per-pack split (`tic-families-pack.yml`, `llm-tone-tells-pack.yml`, `audience-matrix-pack.yml`) — if the consolidated `register-pack.yml` grows beyond comfortable single-file editing.
- `_meta/version-history.yml` — operator-changelog for each override applied (who; when; rationale; rollback if needed).

## Schema (high-level)

The `register-pack.yml` carries the following top-level keys:

- `metadata:` — pack version, last-edited timestamp, last-edited-by role, canonical-source references.
- `layers:` — per-layer enable/disable flags + strict-mode flags (default: all `true` per D-IH-71-F strict-day-1).
- `tic_families:` — per-family overrides (severity downgrade; allowlist tokens; surface-specific exemptions).
- `register_tokens:` — overrides for the BRAND_REGISTER_MATRIX 6 register tokens.
- `audience_quadrants:` — overrides for BRAND_GANTT_DISCIPLINE §2 Variant A/B/C/D audience matrix.
- `boundary_rules:` — overrides for the D-IH-70-X Storytelling AUTHORS / Resonance CONSUMES boundary.
- `llm_tone_tells:` — per-token severity overrides for BRAND_LLM_TONE_TELLS §3-§7 catalog (Layer 8; strict-day-1 default per C-71-8).
- `locale_leak_rules:` — Layer 7 cross-locale leak detection overrides.
- `cobrand_rules:` — Layer 7 cobrand surface check overrides.
- `track_record_rules:` — Layer 9 anonymized track-record format overrides.
- `brand_abbreviation_rules:` — Layer 9 brand-abbreviation surface check overrides.

Full schema is defined in `akos/brand_voice_register.py` via the `BrandVoiceRegisterPack` Pydantic model (P1.4 mint). Schema drift is detected at validator-startup; mismatches between the YAML pack and the model fail-fast with operator-readable error messages.

## Authoritative reading order (for new contributors)

1. **First, read the canonical markdown sources** to understand which patterns exist and why:
   - [`../BRAND_COPYWRITING_DISCIPLINE.md`](../../Copywriter/canonicals/BRAND_COPYWRITING_DISCIPLINE.md) §2 — 7 AI-tone tic families (structural).
   - [`../BRAND_ENGLISH_PATTERNS.md`](../BRAND_ENGLISH_PATTERNS.md) §5 — EN MBA-deck jargon + performative-EN.
   - [`../BRAND_FRENCH_PATTERNS.md`](../BRAND_FRENCH_PATTERNS.md) §5 — FR anglicism + performative-FR.
   - [`../BRAND_SPANISH_PATTERNS.md`](../BRAND_SPANISH_PATTERNS.md) §13 — ES anglicism + performative-ES.
   - [`../BRAND_LLM_TONE_TELLS.md`](../BRAND_LLM_TONE_TELLS.md) §3-§7 — EN-corporate-LLM lexical signature.
   - [`../BRAND_REGISTER_MATRIX.md`](../BRAND_REGISTER_MATRIX.md) — `(relationship, channel) → register` lookup.
   - [`../../UX Designer/canonicals/BRAND_GANTT_DISCIPLINE.md`](../../UX%20Designer/canonicals/BRAND_GANTT_DISCIPLINE.md) §2 — 4-quadrant audience matrix.
2. **Then, read the validator code** to understand how the YAML pack feeds into runtime rule resolution:
   - [`scripts/validate_brand_voice_register.py`](../../../../../../../scripts/validate_brand_voice_register.py) — extended at I71 P1 Pack A1.
   - [`akos/brand_voice_register.py`](../../../../../../../akos/brand_voice_register.py) — Pydantic chassis (minted at I71 P1 Pack A1 P1.4).
3. **Then, inspect `register-pack.yml`** to see the current operator-applied overrides.
4. **For testing local edits:** run `py scripts/validate_brand_voice_register.py --pack-path docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/register-pack.yml --strict-empty` after editing.

## Maintenance

- **Edit-then-PR.** Any change to `register-pack.yml` requires a pull request with operator approval (Brand Manager or Founder). The PR description should explain the override's rationale and link to the deliverable that surfaced the false-positive (if applicable).
- **No silent canonical updates.** Operator overrides in `register-pack.yml` do **not** update the canonical markdown — the canonical remains the source of truth for "what exists". Pattern additions or removals must edit the markdown first; the YAML pack lags.
- **Release-gate integration.** The validator runs at release-gate per `scripts/release-gate.py` (line 250-266 + 487-494; strict-FAIL by default since I66 P5 incr 3; soft-INFO via `AKOS_BRAND_VOICE_REGISTER_SOFT=1`). YAML-pack overrides apply before the release-gate decision.
- **Annual review.** Reviewed in lockstep with `BRAND_COPYWRITING_DISCIPLINE.md` (Brand Manager cadence) + `BRAND_LLM_TONE_TELLS.md` (joint Copywriter cadence).

## Cross-references

- I71 P1 plan: [`.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md`](../../../../../../../../.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md).
- I71 P1 evidence sweep: [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-evidence-sweep-2026-05-14.md`](../../../../../../../wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-evidence-sweep-2026-05-14.md).
- D-IH-71-F (strict-day-1 enforcement): `DECISION_REGISTER.csv` (P1.8).
- D-IH-71-G (Pydantic chassis pattern): `DECISION_REGISTER.csv` (P1.8).
- D-IH-71-H (3-axis audience matrix): `DECISION_REGISTER.csv` (P1.8).
- D-IH-71-I (Storytelling/Resonance boundary): `DECISION_REGISTER.csv` (P1.8).
- D-IH-71-J (release-gate row extension policy): `DECISION_REGISTER.csv` (P1.8).
- D-IH-71-K (Round 3 brand-DNA Layers 5-9 scope): `DECISION_REGISTER.csv` (P1.8).
