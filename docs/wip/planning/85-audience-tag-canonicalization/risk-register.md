---
initiative_id: I85
language: en
last_review: 2026-05-16
---

# I85 — Risk register

| ID | Risk | Likelihood | Impact | Owner | Mitigation | Status |
|:---|:---|:---|:---|:---|:---|:---|
| **R-IH-85-1** | Tag-migration sweep mis-classifies a surface (`audience: [J-IN]` where correct is `[J-CU]`) and silently lands wrong audience metadata | M | M | Brand Manager | P2 operator-batch-approve per tranche (D-IH-85-C); pre-tranche dry-run report surfaces inferences for review; spot-checks; rollback per-tranche if error rate > 5% | Open |
| **R-IH-85-2** | `BRAND_BASELINE_REALITY_MATRIX.md` adds a new J-* row later that drifts from `AUDIENCE_REGISTRY.csv` | L | M | Brand Manager | P1 SOP names matrix as SSOT for additions; addition workflow documented; drift gate covers FK at code level; periodic review at I81 P1 evidence pack | Open |
| **R-IH-85-3** | Multi-audience encoding `[J-IN, J-AD]` confuses downstream consumers expecting string | L | L | System Owner | P1 Pydantic validator + P2 drift gate enforce list; D-IH-85-B sets precedent; tests cover both single + multi audience cases | Open |
| **R-IH-85-4** | I85 P2 sweep stalls because tranche operator-approval bandwidth exceeds 1d budget | M | L | PMO | Phase split P2-a (advops) and P2-b (touchpoint-kit) acceptable per D-IH-85-C; cluster coordinator (I86) reschedules under D-IH-86-B 14-day quiet-period floor | Open |
| **R-IH-85-5** | I81 P1 evidence pack ships before I85 P1 canonical mint, breaking the forward-link wire | L | M | PMO | `INITIATIVE_DEPENDENCIES.md` records hard sequence; I86 D-IH-86-D mechanical cross-check verifies I85 P1 closed before I81 P1 can close | Open |

## Cross-cluster risk reference

- **R-IH-85-1** (mis-classification) overlaps with **I81 R-IH-81-N** (vault-sweep mis-classification) — both run mitigated by per-tranche operator approval; I86 sequencing puts I85 P2 before I81 P1 evidence pack so any mis-classification surfaces in the audience tranche before the integrity-matrix consumes it.
- **R-IH-85-5** (forward-link wire) is registered in **I86 R-IH-86-3** (substrate-decision lag) as a class of intra-cluster sequencing risks.
