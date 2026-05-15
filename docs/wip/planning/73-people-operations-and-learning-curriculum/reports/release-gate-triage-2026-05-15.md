# Release gate triage — 2026-05-15 (I73 Part C)

**Verdict after fixes:** `py scripts/release-gate.py` ends **exit code 1** (FAIL).

Raw captured output from an earlier full run lives beside this note at [`release-gate-raw-2026-05-15.txt`](release-gate-raw-2026-05-15.txt) if present; duplicate summaries below reflect the latest deterministic `[PASS]` / `[FAIL]` rows printed by `scripts/release-gate.py`.

## Resolved in-repo this wave (no longer failing full suite)

- **Test suite:** Slide 11 ENISA deck pillar metrics synced to canonical CSV counts (`1.160` procesos, `67` roles); dossier governance fixture asserts persona row-count vs `PERSONA_REGISTRY.csv` instead of hardcoded `16`; engagement estimation role mixes updated after baseline merger absorbed **`UX Designer`** into **`Brand & Narrative Manager`** / **`Front-End Developer`** (fixes Suez schedule `KeyError`).
- **Operator inbox:** Regenerated [`OPERATOR_INBOX.md`](../../OPERATOR_INBOX.md) so `--check-only` matches OPS/initiative state.

## Remaining FAIL rows (must green individually before gate exits 0)

| Gate row | Owner | Next action |
|:---------|:------|:------------|
| **[FAIL] Browser smoke** (`scripts/browser-smoke.py --playwright`) | Tech / CI env | Control plane not reachable at expected bind (`connection refused` on localhost dashboard URL during gate — start Madeira/control-plane listener **or** document SKIP-only posture per workspace playbook). Docker Desktop pipe also skipped on this host (WARNING); unrelated strict blocker unless smoke expects Docker. |
| **[FAIL] BRAND voice register** (`scripts/validate_brand_voice_register.py`) | Brand Manager (`Brand & Narrative Manager`) | Triage emitted violations against repo-local canonical prose **and** any sibling-repo paths (e.g. `boilerplate/` messages). Bulk remediation belongs on Brand backlog unless violations point at stale AKOS canon copies only. |
| **[FAIL] BRAND voice Vale sibling** (deterministic NLP; `vale exit=2`) | Brand Manager + CI maintainer | Run Vale with repo-standard profile on failing paths; align prose/vocabulary packs **or** adjust Vale manifest exclusions **only** with governance ratification (I71 Pack posture — strict-by-default). |

## Advisory INFO rows observed

- Active initiative freshness canary — four stale initiatives (&gt;14 days): INIT 03 / 11 / 13 / 17 (`scripts/check_active_initiative_freshness.py`).
- Render ownership WARNINGS on engagement README frontmatter vs WORKSPACE_BLUEPRINT §16 matrix (`scripts/validate_render_ownership.py`).

---
**Decision stub:** Remaining FAIL surfaces above recorded under initiative bookkeeping (`operator_inline_default_accepted_via_skip` posture stops at mechanical AKOS fixes; browser + brand strict lanes remain operator-/Brand-owned unless reopened).
