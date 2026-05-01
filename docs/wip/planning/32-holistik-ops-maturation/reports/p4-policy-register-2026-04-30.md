---
language: en
status: complete
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P4
program_id: shared
plane: ops
authority: Compliance + System Owner
last_review: 2026-04-30
---

# P4 — Policy register

**Date:** 2026-04-30
**Status:** COMPLETED. 14 policies seeded across all 4 classes. **15/15 P4 tests PASS**. Topic registry now at 26.

## Action items

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P4-A1** | Schema + akos contract | DONE | [`akos/hlk_policy_register_csv.py`](../../../../akos/hlk_policy_register_csv.py): 11-field tuple + `VALID_POLICY_CLASSES` (4) + `VALID_CADENCES` (5). |
| **P4-A2** | Validator + FK | DONE | [`scripts/validate_policy_register.py`](../../../../scripts/validate_policy_register.py): policy_id regex, class enum, cadence enum, owner_role FK to baseline_organisation, last_review/next_review YYYY-MM-DD with `next_review >= last_review` invariant, topic_ids FK. |
| **P4-A3** | Mirror DDL | DONE (staged) | [`supabase/migrations/20260430233300_i32_policy_register_mirror.sql`](../../../../supabase/migrations/20260430233300_i32_policy_register_mirror.sql): PK policy_id; 4 indexes (synced_at, class, schema, partial on next_review where cadence in {quarterly, annual}); RLS deny anon + authenticated; service_role only. |
| **P4-A4** | 14 seed rows covering 4 classes | DONE | 9 RLS rows (compliance.* deny anon + auth, finops.* deny anon + auth, holistika_ops.lead_intake exception, plus per-mirror specifics for I32 P1/P2/P3/P4) + 1 service_role rotation (I26 P2 quarterly cadence) + 1 redaction (BRAND_JARGON_AUDIT) + 3 PII scope (GOI/POI display_name obfuscation, FINOPS no-amounts-in-git, language frontmatter mandatory). **Self-referential**: POL-RLS-POLICY-REGISTER-MIRROR-I32 is a policy_register row. |
| **P4-A5** | SOPs cite policy_id | DEFERRED | Cross-SOP citation backfill is operator/PMO work spanning ~15 SOP files. Captured as a follow-up; the I32 P14 governance moat metrics test will surface uncited policies after P14 lands. Not blocking I32 closure. |
| **P4-A6** | Tests | DONE | 15 tests in [`tests/test_policy_register.py`](../../../../tests/test_policy_register.py): all PASS. Seed-coverage tests assert all 4 classes are represented + the I26 quarterly rotation row exists + the BRAND_JARGON redaction row exists + the self-referential row exists. |

## Verification

- `py scripts/validate_policy_register.py` → PASS at 14 rows; by class: 9 rls / 1 service_role_rotation / 1 redaction / 3 pii_scope
- `py scripts/validate_topic_registry.py` → PASS at 26 rows
- `py scripts/validate_hlk.py` → PASS; new line: "POLICY_REGISTER: PASS"
- `py -m pytest tests/test_policy_register.py -v` → **15 passed in 3.40s**

## Notes

- **The policy register is the missing audit surface**: today RLS rules + rotation cadences + redaction policies + PII scope live across 5+ SOPs as paragraphs. After P4, every shipped policy resolves to one queryable row with `owner_role`, `cadence`, `last_review`, `next_review` for compliance dashboards.
- The seed is intentionally **representative**, not exhaustive. 9 RLS rows cover schema-level postures (compliance.* deny anon + auth + finops.* deny anon + auth + holistika_ops.lead_intake exception + 4 I32-mirror-specific rows). Per-table specifics for the existing 11 compliance.*_mirror tables can be added in a follow-up tranche; the contract scales.
- **Self-referential row** (POL-RLS-POLICY-REGISTER-MIRROR-I32): the policy register's own RLS rule is a policy_register row. Audit closure for "is the policy register itself governed?" → yes.
- **3-month review cadence** for all rows (next_review = 2026-07-31). Next-quarter cadence aligns with I26 P2 quarterly service_role rotation; the partial index on `(next_review)` where cadence in {quarterly, annual} powers a future "policies due for review" dashboard query.
- The cross-SOP `policy_id` citation backfill (P4-A5) is deferred but the validator is wired so the moment a SOP cites a policy_id, future drift on that SOP-policy mapping will be detectable.

## Next phase

P5 — Topic axis 6 promotion (HOLISTIK_OPS_DISCOVERY.md v2 + topic_ids column on 5 dimension CSVs).
