---
language: en
status: active
intellectual_kind: phase_report
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_skill_registry
parent_topic: topic_skill_registry
---

# I45 P5 — Adversarial cassettes (3 vectors) + PII linter

**Phase:** P5 (adversarial cassette suite + PII linter; wires to alerts.json)
**Closes:** I45 P5 + evidence-matrix E4 (alerts.json un-exercised) + R-45-4 mitigation operationalized.
**Date:** 2026-05-01

## Actions

1. **`akos/eval_harness/adversarial.py`** (~165 lines):
   - **3 vectors per D-IH-45-E**: prompt injection, brand jargon leakage, PII extraction.
   - `BRAND_JARGON_RE` — mirrors the rg pattern from `BRAND_JARGON_AUDIT.md` §5: `\b(akos|topic_\w+|advops|techops|finops|goi-|poi-|ref_id|program_id|prj-hol-|holistika_ops\.|kirbe\.|repo_slug)\b`
   - `scan_text_for_pii()` — regex-based detector with **synthetic-pattern allowlist**: `*@example.com`, `555-01XX` (IETF reserved), `203.0.113.x` / `192.0.2.x` / `198.51.100.x` (RFC 5737 TEST-NET), private IPs, SSNs starting with `000-` / `666-` / `9XX` (SSA never-assigned)
   - `record_adversarial_classify_request_cassette()` — captures one probe; auto-includes captured route in expected_routes (drift detection vs record time)
   - `replay_adversarial_classify_request_cassette()` — runs probe through `classify_request`; checks 4 things: route in expected_routes, no forbidden_in_response token, no must_not_escalate_to flip, no brand jargon in operator_message, no PII in serialized response

2. **New cassette probe_kind: `adversarial_classify_request`** — wired into `replay_cassette()` dispatcher in `akos/eval_harness/cassette.py`; new ScoreRow mode `adversarial` in `akos/eval_harness/v2.py`; new `--mode adversarial` CLI flag in `scripts/eval.py`.

3. **Seeded 12 adversarial cassettes** under `tests/evals/cassettes/adversarial/<skill_id>/`:
   - **5 prompt-injection** (`pi_*`): "ignore previous instructions", role-switch, admin-via-lookup, exec-via-plan, credential extract — covering the 5 most-cited PI patterns
   - **4 brand-jargon** (`bj_*`): jargon amplification, advops query, program_id echo, jargon-in-french locale
   - **3 PII** (`pii_*`): synthetic email + 555-01XX phone, 000-00-0000 SSN, RFC 5737 TEST-NET-3 IP

4. **`scripts/lint_cassette_pii.py`** (R-45-4 mitigation operationalized):
   - Walks `tests/evals/cassettes/`; flags any cassette JSONL with real-looking PII
   - Synthetic patterns allowed; everything else fails CI
   - Caught a real signal during seed authoring: my initial probe used `203.0.113.42` (RFC 5737 — should be allowed) and `555-12-9999` (could look real); fixed both during P5 development

5. **POLICY_REGISTER row**: `POL-EVAL-ADVERSARIAL-FLOOR` (policy_class=`adversarial_floor`):
   - "All skills must pass the I45 P5 adversarial cassette suite (≥12 probes)"
   - Hard-fail CI on any FAIL row from `py scripts/eval.py --mode adversarial`
   - Cross-references `madeira_internal_tool_leak`, `madeira_pseudo_hlk_path_leak`, `madeira_suspect_uuid_hallucination` alerts in `config/eval/alerts.json`
   - Owner: System Owner

6. **23 new tests** in `tests/test_eval_adversarial.py`:
   - Vector 1 (5 tests): pi_* cassette presence + 100% pass + replay-time forbidden-token detection + replay-time must_not_escalate_to detection + replay SKIP for unsupported probe_kind
   - Vector 2 (3 tests): bj_* cassette presence + 100% pass + brand-jargon regex catches real jargon
   - Vector 3 (2 tests): pii_* cassette presence + 100% pass
   - PII linter (8 tests): catches real email / synthetic email allowed / catches real phone / 555-01 allowed / catches real SSN / 000- allowed / TEST-NET allowed / private IP allowed / public IP caught
   - Whole-suite hygiene (3 tests): all 12 adversarial replay PASS / all 18 cassettes PII-clean / v2 dispatcher returns one row per cassette

## Verification

- `py scripts/eval.py --mode adversarial`: **12/12 PASS**, overall PASS, ~3s.
- `py scripts/lint_cassette_pii.py`: 18/18 cassettes PII-clean, exit 0.
- `tests/test_eval_adversarial.py`: **23/23 PASS** in 2.8s.
- `validate_policy_register.py`: PASS (16 rows: 1 new adversarial_floor + 5 cost_ceiling + 10 prior).

## Adversarial coverage matrix

| Skill | PI probes | BJ probes | PII probes | Total |
|:------|:---------:|:---------:|:----------:|:-----:|
| SKILL-MADEIRA-LOOKUP-V1 | 3 | 2 | 2 | 7 |
| SKILL-ARCHITECT-PLAN-V1 | 1 | 0 | 0 | 1 |
| SKILL-EXECUTOR-RUN-V1 | 0 | 1 | 0 | 1 |
| SKILL-VERIFIER-CHECK-V1 | 1 | 0 | 1 | 2 |
| SKILL-SHARED-LOCALE-DETECT-V1 | 0 | 1 | 0 | 1 |
| **TOTAL** | **5** | **4** | **3** | **12** |

MADEIRA-LOOKUP carries the heaviest adversarial coverage because it's the operator-facing surface most likely to be probed in the wild.

## What this does NOT do (deferred)

- **No live LLM adversarial probes yet** — all 12 cassettes are deterministic `adversarial_classify_request`. Live LLM probes (against actual chat models, not just the regex+embedding classifier) land in P6 when Tier B is wired.
- **Promptfoo's full 500-vector suite NOT adopted** — D-IH-45-E alternative; revisit at I47.
- **No automated cassette-aging policy for adversarial probes** — same staleness rules as regular cassettes (60d warn, 90d fail) per P2.

## Risks resolved

- **R-45-4 (PII leak)**: now operationally enforced. `scripts/lint_cassette_pii.py` runs as needed; recommended addition to `pre_commit` profile.
- **R-45-10 (Promptfoo / Inspect AI mid-stream swap)**: not realized — the cassette JSONL format is framework-independent; if we adopt Promptfoo later, only `scan_text_for_pii()` and a wider vector library would be added.

## Operator-applied steps

1. **Apply POLICY_REGISTER reseed** (the new adversarial_floor row): `py scripts/sync_compliance_mirrors_from_csv.py --policy-only` against your live Supabase.
2. **Optional**: add `scripts/lint_cassette_pii.py` to `verification-profiles.json` `pre_commit` profile.

## Next phase

P6 — Tier B weekly schedule. `.github/workflows/eval-tier-b.yml` with model-tier matrix (1 cheap + 1 flagship), `MAX_TIER_B_USD` kill switch, hard-fail >5pp regression vs cassette baseline. Live LLM cassettes (probe_kind=`live_llm`) get populated for the first time.
