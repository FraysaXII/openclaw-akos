---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P11
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P11 — Persona-conditioned MADEIRA prompts (D-IH-47-I)

## What shipped

### `prompts/overlays/PERSONA_OVERLAY.md` (NEW canonical template)

Lightweight section marker (113 chars) appended before the per-persona hint. Per R-47-14: "Invariants from MADEIRA_BASE always apply."

### Per-persona MADEIRA_HINTS.md (4 Tier-1 personas)

| Persona | Chars | Cap | Coverage |
|:---|:---:|:---:|:---|
| `PERSONA-INVESTOR-COLD` | 239 | ≤500 | en/es; N3-N4; 7d ack; ESCALATE cap-table/ARR/Madeira ZFM; REFUSE forecasts |
| `PERSONA-INVESTOR-WARM` | 275 | ≤500 | bridge-acknowledge; 1-week SLA; warm does NOT bypass qualification |
| `PERSONA-ADVISOR-REFERRAL` | 330 | ≤500 | es-dominant; ENISA pattern; PMO routes; Founder approves equity |
| `PERSONA-CUSTOMER-KIRBE-PROSPECT` | 461 | ≤500 | KiRBe trial; size + use-case qualifying; System Owner / Founder for Enterprise |

All 4 Tier-1 personas covered (Tier-2/Tier-3 personas can be added incrementally; soft-fail to default MADEIRA register if missing).

### `scripts/assemble-prompts.py` extension

- New `--persona <id>` flag — lazy-loads `prompts/overlays/PERSONA_OVERLAY.md` + `prompts/personas/<id>/MADEIRA_HINTS.md`
- Persona overlay only affects MADEIRA agent (other agents build unchanged)
- Soft-fail: missing `MADEIRA_HINTS.md` builds anyway with framework-only
- Persona-conditioned variant filename: `MADEIRA_PROMPT.<variant>.<persona_id>.md`
- **Architectural decision**: persona-conditioned MADEIRA SWAPS OUT `OVERLAY_HLK_GRAPH.md` (1241 chars). Persona context replaces graph traversal awareness for non-operator persona flows.

### bootstrapMaxChars discipline (R-47-9)

| Variant | Chars | Limit | Status |
|:---|:---:|:---:|:---:|
| MADEIRA_PROMPT.standard.md (no persona) | 19731 | 20000 | OK |
| MADEIRA_PROMPT.standard.PERSONA-INVESTOR-COLD.md | 18842 | 20000 | OK (1158 headroom) |
| MADEIRA_PROMPT.standard.PERSONA-INVESTOR-WARM.md | 18878 | 20000 | OK (1122 headroom) |
| MADEIRA_PROMPT.standard.PERSONA-ADVISOR-REFERRAL.md | 18933 | 20000 | OK (1067 headroom) |
| MADEIRA_PROMPT.standard.PERSONA-CUSTOMER-KIRBE-PROSPECT.md | 19064 | 20000 | OK (936 headroom) |

The graph-overlay-swap design preserves 936-1158 chars of headroom even with the largest persona hint.

## R-47-14 mitigation

`tests/test_persona_overlay.py::test_madeira_base_invariants_survive_persona_overlay` asserts that ≥15 of the first 20 substantive lines of MADEIRA_BASE persist in the persona-conditioned variant — structural verification that the persona overlay PREPENDS context, never OVERRIDES the base.

Combined with the `PERSONA_OVERLAY.md` framework's explicit invariant claim ("Invariants from MADEIRA_BASE always apply"), this closes R-47-14 ("Persona-conditioned prompts diverge from MADEIRA_BASE doctrine").

## Verification

- 22 new tests in `tests/test_persona_overlay.py` PASS:
  - File-existence + size discipline (5 tests)
  - CLI surface (1 test)
  - bootstrapMaxChars under each persona (4 tests)
  - OVERLAY_HLK_GRAPH swap-out per persona (4 tests)
  - Per-persona hint header inclusion (4 tests)
  - Soft-fail for missing persona (1 test)
  - Non-MADEIRA agents not affected (1 test)
  - MADEIRA_BASE invariants survive (1 test) + parametrized
- All 4 persona-conditioned MADEIRA standard variants build successfully under 20000-char bootstrapMaxChars
- Persona overlay does not affect other agents (MADEIRA-only)

## Cross-references

- D-IH-47-I (RICE A: persona-conditioned MADEIRA prompts; user-mandated)
- R-47-9 (bootstrapMaxChars overflow — mitigated via OVERLAY_HLK_GRAPH swap)
- R-47-14 (persona overlay invariant survival — verified by test)
- I46 P7 OVERLAY_HLK_GRAPH shrink (the original lesson that motivated the headroom approach)
- I47 P10 ScoreRow.persona_id (downstream consumer of persona context for scoring)
