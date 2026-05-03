# I53 / P0 — Bootstrap

**Date:** 2026-05-03
**Phase:** P0 (Governance scaffold)

## Deliverables

- `docs/wip/planning/53-graphrag-poc-closure/`:
  - `master-roadmap.md` — 8 phases (P0-P7), $20 envelope per R-46-1, decisions D-IH-53-A..D, gates G-53-1..3.
  - `decision-log.md` — 4 decisions seeded with defaults; reuse I52 multi-judge roster for accuracy axis (D-IH-53-A); 60% multi-hop / 40% single-hop golden set already encoded in I46 P3 (D-IH-53-B); non-additive trade-off thresholds (D-IH-53-C; partial-credit ship forbidden); rollback procedure (D-IH-53-D).
  - `evidence-matrix.md` — E1-E8 anchored to I46 P3-P7 reports + I52 closure + operator stance.
  - `risk-register.md` — R-53-1..4 with R-53-4 explicitly accepting the no-fire outcome as a governance event.
  - `asset-classification.md` — canonical/mirrored/reference-only/code/tests breakdown.
  - `reports/.gitkeep`.
- Planning README row (I53; Active).

## Cross-link

I53 closes **I46 P3-P7** (Open since 2026-05-01). I46 master-roadmap status flips to `Closed` at I53 P7.

## Verification

- `py scripts/check-drift.py` PASS (no drift).
- `py scripts/validate_hlk.py` PASS.

## Forward look

- P1 audits the I46 P3 golden set + scaffold; no live spend.
- P2 audits the PoC infra; no live spend.
- P3 either drives the live A/B (operator-funded) OR documents the no-fire outcome.
- P4-P7 follow the live-vs-no-fire branch from P3.
