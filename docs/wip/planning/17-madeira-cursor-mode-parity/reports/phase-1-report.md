# Phase 1 report — Initiative 17

**Date:** 2026-04-21  
**Scope:** Control plane endpoints, `/madeira/control` UI, SOUL redeploy hooks in bootstrap / switch-model / sync-runtime / `POST /switch`, Langfuse + log-watcher fields.

## Verification

- `py -m pytest tests/test_api.py tests/test_madeira_interaction.py -v`
- `py scripts/assemble-prompts.py` (after `model-tiers.json` overlay changes)

## UAT

Qualitative WebChat checks: pending `reports/uat-madeira-mode-*.md` when operator signs off on `/madeira/control` + dashboard session behaviour.
