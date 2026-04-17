# Initiative 13 — reports

## Intent benchmark (before / after)

1. **Baseline:** On the parent commit (or tag), run:
   - `py -m pytest tests/test_intent_golden.py -v` (regex + golden expectations; always in CI).
   - Optional local: with Ollama + embeddings available, run the same tests — embedding path exercises when `_get_classifier()` loads.
2. **After changes:** Re-run identical commands; save a short **delta** in a dated note or PR description (e.g. embedding match counts from pytest output).

**SOC:** Do not paste API keys, bearer tokens, or full system prompts into these files.

## UAT

When WebChat qualitative sign-off is in scope, add `uat-madeira-research-followthrough-<YYYYMMDD>.md` with PASS / SKIP / N/A and **Before / After** columns per scenario where applicable. Cross-reference [`docs/uat/hlk_admin_smoke.md`](../../../../uat/hlk_admin_smoke.md).
