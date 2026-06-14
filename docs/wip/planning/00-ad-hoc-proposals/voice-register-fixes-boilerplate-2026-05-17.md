---
language: en
authored: 2026-05-17
authored_by: System Owner (regression-sweep subagent)
intended_for: operator (boilerplate sibling-repo PR flow)
status: forward-charter
target_repo: boilerplate
target_repo_url: https://github.com/FraysaXII/boilerplate
target_repo_local_path: c:/Users/Shadow/cd_shadow/root_cd/boilerplate
target_branch_recommendation: chore/voice-register-fixes-i77 (off i32-akos-mirror-seed or main once i32 lands)
detection_validator: scripts/validate_brand_voice_register.py
detection_canonical_rules: BRAND_ENGLISH_PATTERNS.md §5.1; BRAND_LLM_TONE_TELLS.md; BRAND_COPYWRITING_DISCIPLINE.md §2
---

# Boilerplate voice-register fixes — operator handoff (2026-05-17)

> AKOS-as-SSOT discipline per [`akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc): the brand voice canonical lives in AKOS (`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ENGLISH_PATTERNS.md` + `BRAND_LLM_TONE_TELLS.md` + `BRAND_COPYWRITING_DISCIPLINE.md`); sibling-repo edits go through the operator's normal PR flow. This document is a forward-charter — 4 specific copy-paste rewrites the operator applies in the next sibling-repo i18n commit.

## Why this is a forward-charter (not a direct edit)

The 2026-05-17 mechanical regression sweep ran `py scripts/validate_brand_voice_register.py` against the boilerplate i18n bundles (resolved at `c:/Users/Shadow/cd_shadow/root_cd/boilerplate/i18n/messages/*.json`). The validator flagged 4 forbidden register patterns across 2 files. The boilerplate local checkout is currently on branch `i32-akos-mirror-seed` with **uncommitted operator WIP** on `i18n/messages/{en,es,fr}.json` (operator is adding a new `contact` CTA key on the hero section — different keys from the violations, but the same files). Applying the fixes from a subagent and creating a new branch would:

- Risk capturing the operator's WIP in an unrelated branch (or losing it on stash gymnastics).
- Surprise the operator with an unexpected branch they would need to integrate manually into their in-flight `i32-akos-mirror-seed` work.
- Cross the AKOS-as-SSOT rule of "sibling-repo edits stay with the operator's normal flow".

So this proposals doc records the exact 4 rewrites with copy-paste-ready JSON snippets and operator-applies them when the i32 branch lands or in the next i18n PR.

## Validator output (mechanical evidence)

```
[INFO] BRAND_VOICE_REGISTER loaded 54 total rule(s) across locales: en=31, es=9, fr=14
[ERROR] root_cd/boilerplate/i18n/messages/en.json [en] techLab.platforms.kirbe.description: 'enterprise-grade' — EN MBA-deck jargon — replace with 'the specific reliability claim' (Stack-vendor language) (canonical: BRAND_ENGLISH_PATTERNS.md §5.1)
[ERROR] root_cd/boilerplate/i18n/messages/en.json [en] manifiesto.holistika.sections.pincerEffect.content3: 'llm_tone_tell:T-3-delve-into' — LLM tone tell — One of the strongest LLM-tells in 2024-2026 EN-corporate prose. (replace with: `look at`, `study`, `examine`, `dig into`) (canonical: BRAND_LLM_TONE_TELLS.md)
[ERROR] root_cd/boilerplate/i18n/messages/en.json [en] manifiesto.kirbe.description: 'enterprise-grade' — EN MBA-deck jargon — replace with 'the specific reliability claim' (Stack-vendor language) (canonical: BRAND_ENGLISH_PATTERNS.md §5.1)
[ERROR] root_cd/boilerplate/i18n/messages/fr.json [fr] entities.title: 'tic_family:false_singularity' — AI-tone tic family F3 (false_singularity) — Keep concrete idiomatic uses (`une seule fois`, `une seule personne`); drop epigrammatic uses on H2 / cover slides. (canonical: BRAND_COPYWRITING_DISCIPLINE.md §2)
[ERROR] BRAND_VOICE_REGISTER: 4 forbidden register pattern(s) across 2 file(s)
```

## Per-violation rewrite table

| # | File | Line | JSON path | Violation | Current value | Recommended rewrite | Canonical rule |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `i18n/messages/en.json` | 423 | `techLab.platforms.kirbe.description` | `enterprise-grade` MBA-deck jargon | "Hybrid search combining keyword and semantic matching with intelligent ranking. **Enterprise-grade** access controls, usage metering, and compliance-ready audit logging for SMB knowledge management." | "Hybrid search combining keyword and semantic matching with intelligent ranking. **Role-scoped** access controls, usage metering, and compliance-ready audit logging for SMB knowledge management." | BRAND_ENGLISH_PATTERNS.md §5.1 |
| 2 | `i18n/messages/en.json` | 556 | `manifiesto.holistika.sections.pincerEffect.content3` | `delve into` LLM tone tell (T-3) | "This methodology is why Holistika does not need to specialize only in the services it currently offers—it can **delve into** any area of business it chooses." | "This methodology is why Holistika does not need to specialize only in the services it currently offers—it can **examine** any area of business it chooses." | BRAND_LLM_TONE_TELLS.md (T-3-delve-into) |
| 3 | `i18n/messages/en.json` | 650 | `manifiesto.kirbe.description` | `enterprise-grade` MBA-deck jargon | "Hybrid search combining keyword and semantic matching, **enterprise-grade** access controls, usage metering, and compliance-ready audit logging. The Intelligence Layer for semantic knowledge retrieval." | "Hybrid search combining keyword and semantic matching, **role-scoped** access controls, usage metering, and compliance-ready audit logging. The Intelligence Layer for semantic knowledge retrieval." | BRAND_ENGLISH_PATTERNS.md §5.1 |
| 4 | `i18n/messages/fr.json` | 29 | `entities.title` | `tic_family:false_singularity` epigrammatic three-beat on H2 | "Trois équipes. **Un seul objectif**." | "Trois équipes. **Un objectif commun**." | BRAND_COPYWRITING_DISCIPLINE.md §2 (F3) |

## Recommended rewrite rationale

- **#1 / #3 (`enterprise-grade` → `role-scoped`)**: the canonical specifies "Stack-vendor language: replace with the specific reliability claim". `role-scoped` names the actual access-control mechanism KiRBe ships (per `kirbe.*` RLS-anchored Supabase tables) without resorting to the MBA-deck adjective. Both occurrences of `enterprise-grade access controls` are the same noun phrase, so the rewrite is consistent.
- **#2 (`delve into` → `examine`)**: the canonical lists 4 acceptable replacements (`look at`, `study`, `examine`, `dig into`). `examine` carries the methodological-rigour register the surrounding sentence is doing ("Holistika ... can examine any area of business"); `look at` is too casual; `study` is too academic; `dig into` is too colloquial for a manifesto surface.
- **#4 (`Un seul objectif` → `Un objectif commun`)**: the `false_singularity` tic family flags the epigrammatic "Trois X. Un seul Y." pattern on H2 / cover surfaces. The canonical permits concrete idiomatic uses (`une seule fois`, `une seule personne`); it specifically flags epigrammatic uses on H2 / cover slides. `Un objectif commun` ("A common objective") preserves the sentence's meaning (three teams aligned to one shared goal) without the cover-slide tic.

## Copy-paste-ready JSON diffs

```diff
diff --git a/i18n/messages/en.json b/i18n/messages/en.json
@@ ~line 423 @@
-        "description": "Hybrid search combining keyword and semantic matching with intelligent ranking. Enterprise-grade access controls, usage metering, and compliance-ready audit logging for SMB knowledge management.",
+        "description": "Hybrid search combining keyword and semantic matching with intelligent ranking. Role-scoped access controls, usage metering, and compliance-ready audit logging for SMB knowledge management.",
@@ ~line 556 @@
-          "content3": "This methodology is why Holistika does not need to specialize only in the services it currently offers—it can delve into any area of business it chooses.",
+          "content3": "This methodology is why Holistika does not need to specialize only in the services it currently offers—it can examine any area of business it chooses.",
@@ ~line 650 @@
-      "description": "Hybrid search combining keyword and semantic matching, enterprise-grade access controls, usage metering, and compliance-ready audit logging. The Intelligence Layer for semantic knowledge retrieval."
+      "description": "Hybrid search combining keyword and semantic matching, role-scoped access controls, usage metering, and compliance-ready audit logging. The Intelligence Layer for semantic knowledge retrieval."
diff --git a/i18n/messages/fr.json b/i18n/messages/fr.json
@@ ~line 29 @@
-    "title": "Trois équipes. Un seul objectif.",
+    "title": "Trois équipes. Un objectif commun.",
```

## Verification command (operator-runnable post-edit)

```powershell
cd c:/Users/Shadow/cd_shadow/openclaw-akos
py scripts/validate_brand_voice_register.py
# expected: BRAND_VOICE_REGISTER: 0 forbidden register patterns across 0 files
```

## Operator-flow recommendation

**Option A (preferred): apply on i32-akos-mirror-seed branch**
The operator's existing in-flight branch `i32-akos-mirror-seed` is already editing the same files (`i18n/messages/{en,es,fr}.json`). Adding these 4 rewrites as a small follow-up commit on the same branch is the lowest-friction path. PR message: `chore(voice): voice register fixes per AKOS-as-SSOT rule (4 violations: 3 EN + 1 FR; refs AKOS BRAND_ENGLISH_PATTERNS.md §5.1 + BRAND_LLM_TONE_TELLS.md + BRAND_COPYWRITING_DISCIPLINE.md §2)`.

**Option B: standalone branch after i32 merges**
If the operator prefers a clean isolation (e.g. to land the voice fixes in a separate PR for review), wait until `i32-akos-mirror-seed` merges, then branch `chore/voice-register-fixes-i77` off `main`, apply the diffs, commit, push, PR.

Either way: per `akos-mirror-template.mdc`, AKOS stays SSOT for the canonical rules; the boilerplate fix is the mirror-side propagation.

## Cross-references

- AKOS canonicals:
  - [`BRAND_ENGLISH_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ENGLISH_PATTERNS.md) §5.1 — stack-vendor MBA-deck jargon list.
  - [`BRAND_LLM_TONE_TELLS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_LLM_TONE_TELLS.md) — T-3-delve-into.
  - [`BRAND_COPYWRITING_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_COPYWRITING_DISCIPLINE.md) §2 — tic family F3 (false_singularity).
- AKOS validator: [`scripts/validate_brand_voice_register.py`](../../../../scripts/validate_brand_voice_register.py).
- AKOS rule: [`akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc) — sibling-repo edits stay with operator flow.
- Sibling-repo target: `https://github.com/FraysaXII/boilerplate` (local clone: `c:/Users/Shadow/cd_shadow/root_cd/boilerplate`).
- Detection commit: 2026-05-17 mechanical-backlog regression sweep W3 workstream.
