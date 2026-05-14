# I71 P1 Pack A1 — Operator UAT (inline-ratify)

> Authored 2026-05-14 at agent-mode P1.10 execution. Phase 1.10 of the Cursor plan at `.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md`. Records operator decisions on the 4 hits surfaced by the extended validator against consumer-repo i18n prose, plus the final commit/push ratification.

## 1. UAT context

The I71 P1 Pack A1 chassis expansion to 10 layers + strict-day-1 (`D-IH-71-F`) was wired to scan consumer-repo prose at `root_cd/boilerplate/i18n/messages/{en,es,fr}.json` (per pre-existing `DEFAULT_CONSUMER_ROOTS` in `scripts/validate_brand_voice_register.py`). The validator surfaced **4 positive hits** on the first run (P1.5 baseline + P1.9 confirmation). Per the inline-ratification pattern (`.cursor/rules/akos-inline-ratification.mdc`), these hits go to operator UAT here, before the atomic P1 commit lands.

Per `D-IH-71-F` operator override at plan finalization 2026-05-14 (strict-day-1; per-rule allow-listing via `register-pack.yml`; emergency soft-mode toggle preserved), each hit has three operator dispositions:

- **(a) FIX-IN-CONSUMER** — leave validator strict; operator opens a sibling-repo PR to remediate the prose.
- **(b) ALLOWLIST** — add an entry to `register-pack.yml` `rule_disables` (or category-level disable) to suppress this exact pattern, optionally with a justification comment in the YAML.
- **(c) ACCEPT-AS-ADVISORY** — leave the hit in the strict output; commit with `AKOS_BRAND_VOICE_REGISTER_SOFT=1` as a one-time bypass while consumer-repo fix is in flight.

## 2. The 4 hits

| # | Locale | Path | Token / Rule | Canonical | Severity | Surfaced layer |
|:---:|:---:|:---|:---|:---|:---:|:---|
| H1 | en | `boilerplate/i18n/messages/en.json` → `techLab.platforms.kirbe.description` | `enterprise-grade` (EN MBA-deck jargon — "Stack-vendor language; replace with the specific reliability claim") | `BRAND_ENGLISH_PATTERNS.md §5.1` | error | Layer 2 EN MBA-deck |
| H2 | en | `boilerplate/i18n/messages/en.json` → `manifiesto.holistika.sections.pincerEffect.content3` | `delve-into` LLM tone tell — "One of the strongest LLM-tells in 2024-2026 EN-corporate prose" (replace with `look at`, `study`, `examine`, `dig into`) | `BRAND_LLM_TONE_TELLS.md` | error | Layer 8 LLM tone tells |
| H3 | en | `boilerplate/i18n/messages/en.json` → `manifiesto.kirbe.description` | `enterprise-grade` (same rule as H1, different path) | `BRAND_ENGLISH_PATTERNS.md §5.1` | error | Layer 2 EN MBA-deck |
| H4 | fr | `boilerplate/i18n/messages/fr.json` → `entities.title` | `tic_family:false_singularity` (F3) — "Keep concrete idiomatic uses (`une seule fois`, `une seule personne`); drop epigrammatic uses on H2 / cover slides" | `BRAND_COPYWRITING_DISCIPLINE.md §2` | error | Layer 2 tic family F3 |

## 3. Operator decisions (recorded via inline `AskQuestion` at P1.10, 2026-05-14)

| # | Disposition | Operator rationale | Follow-up action |
|:---:|:---|:---|:---|
| H1 | **(a) FIX-IN-CONSUMER** | `enterprise-grade` in Kirbe description is Stack-vendor language; brand voice rejects it; consumer-repo PR will replace with the specific reliability claim. | Sibling-repo `boilerplate` PR (out of I71 P1 scope; tracked as a forward consumer-repo backlog item). |
| H2 | **(a) FIX-IN-CONSUMER** | `delve-into` is one of the strongest LLM-tells in 2024-2026 EN-corporate prose; consumer-repo PR will replace with `look at` / `study` / `examine` / `dig into`. | Sibling-repo `boilerplate` PR. |
| H3 | **(a) FIX-IN-CONSUMER** | Same rule as H1, different path; both Kirbe-description occurrences fixed in one consumer-repo PR. | Sibling-repo `boilerplate` PR (paired with H1). |
| H4 | **(a) FIX-IN-CONSUMER** | F3 false-singularity on `entities.title` reads as epigrammatic on a primary nav surface; consumer-repo PR will rephrase per BRAND_COPYWRITING_DISCIPLINE.md §2 guidance. | Sibling-repo `boilerplate` PR. |

**Consequence for the AKOS commit**: since all 4 dispositions are FIX-IN-CONSUMER, the AKOS commit does NOT need `AKOS_BRAND_VOICE_REGISTER_SOFT=1` as a one-time bypass. The AKOS validator + canonicals + chassis + tests all PASS strict-day-1 at the AKOS repo boundary. The 4 hits continue to surface as strict FAILs whenever the validator is invoked against the consumer-repo prose, which is the intended D-IH-71-F design — the validator's job is to surface real violations until the consumer-repo PRs land.

## 4. Commit + push ratification (recorded 2026-05-14)

**Operator verdict**: **YES — commit + push + verify Vercel deployment + visual UAT via Browser MCP with screenshots.**

Operator quote (verbatim, 2026-05-14): *"yes cmmit push mrge and delete branch, ensre depymentt ono verccel and tested. visallyy and via screeshots"*

Interpretation:
1. **Commit + push** — atomic single phase-scoped commit on `main` (per `akos-governance-remediation.mdc` "one commit per phase" rule; no feature branch in this workflow, so no merge/delete step is applicable).
2. **Vercel deployment verification** — AKOS-side; the operator wants confirmation that the Vercel target (if any) continues to deploy cleanly post-commit.
3. **Visual UAT via Browser MCP with screenshots** — sanity-pass of any AKOS UI surfaces post-deploy.

Commit SHA: _(filled in post-`git commit`)_  
Push status: _(filled in post-`git push`)_  
Vercel deployment status: _(filled in via Vercel MCP)_  
Visual UAT screenshots: _(filled in via Browser MCP)_

## 5. Cross-references

- `.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md` — Cursor plan (Round 1 + Round 2 + Round 3).
- [`p1-pack-a1-2026-05-14.md`](./p1-pack-a1-2026-05-14.md) — Pack A1 phase report (deliverables + P1.9 verification matrix results).
- [`p1-evidence-sweep-2026-05-14.md`](./p1-evidence-sweep-2026-05-14.md) — Pre-flight evidence sweep.
- `D-IH-71-F` — strict-day-1 enforcement decision (with emergency soft-mode escape hatch).
- `.cursor/rules/akos-inline-ratification.mdc` — inline-ratify gate authority.
