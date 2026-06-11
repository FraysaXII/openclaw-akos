---
name: ssot-canonical-touch-craft
description: >-
  Use when minting or editing vault canonicals, PRECEDENCE rows, CANONICAL_REGISTRY,
  process_list pairing, or HCAM registries. Codifies the four-registry audit loop,
  AskQuestion touch-gate balance, and J-OP/J-AIC prose bar. Pairs with
  akos-ssot-canonical-touch.mdc. Triggers on SSOT audit, canonical touch gate,
  registry backfill, PRECEDENCE drift, CANONICAL_REGISTRY sweep.
---

# SSOT Canonical Touch — craft

## When to load

- New discipline, SOP, pillar, or registry row under `docs/references/hlk/v3.0/`
- Operator asks to "check canonicals", "wire SSOT", or "@ CANONICAL_REGISTRY"
- After a research pack promotes WIP → vault

## 1. Four-registry sweep (per mint)

```
PRECEDENCE row?  →  CANONICAL_REGISTRY row?  →  HCAM triple (if new link pattern)?
CGR row?         →  only if CSV/mirror surface
```

Record gaps in a short wiring note under `docs/wip/intelligence/<pack>/` or
initiative `reports/` — human prose, not a 40-row matrix.

## 2. Touch gate (AskQuestion)

**Before first Tier-A write in session**, unless operator already ratified scope:

- One question, 2–4 options (approve bundle / narrow scope / defer CSV / hold)
- Do **not** re-ask after ratification in the same thread
- Do **not** skip the gate when adding `process_list.csv` or `PRECEDENCE.md`
  silently

## 3. Operator summary shape (J-OP)

1. Opening sentence: what changed for the business of governing knowledge
2. Short paragraph: how it fits together
3. Optional: "audit trail" bullets with functional name + path
4. What still needs your OK (if anything)

**Avoid:** validator dump as the lead; tables where prose suffices.

## 4. Canonical prose shape (J-OP + J-AIC)

| Section | J-OP | J-AIC |
|:---|:---|:---|
| Purpose | Why this exists; what breaks without it | Same, one paragraph max |
| Steps / rules | Plain verbs | Numbered, falsifiable, runnable |
| Verification | What PASS means in human terms | Exact command lines |

Run a quick pass against BRAND_COPYWRITING 7 tic families before commit.

## 5. Periodic sweep (not only on mint)

Area-by-area pass (Research, Data, People, Finance, …):

- `PRECEDENCE` paths missing from `CANONICAL_REGISTRY`
- Active registry rows pointing at missing files (`validate_canonical_registry.py --strict`)
- `process_list` pairing debt for `hol_*` methodology processes

## Worked example

2026-06-10 Research Methodology mint: PRECEDENCE first, then `CANONICAL_REGISTRY`
backfill, HCAM TRP-061..063, CGR N/A for markdown — documented in
`methodology-cross-area-wiring-2026-06-10.md`.
