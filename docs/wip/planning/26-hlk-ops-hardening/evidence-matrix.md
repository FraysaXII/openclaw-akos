# Initiative 26 — Evidence matrix

Initiative 26 is **driven by accumulated deferral debt** from Wave-2 decisions, not by audit findings or observed drift. The evidence is the **set of decisions that explicitly punted** to a later "ops-hardening" cycle:

| Source decision | Decision | Why deferred at decision time | Evidence routed to |
|:----------------|:---------|:------------------------------|:-------------------|
| **D-IH-14** (Wave-2 plan) | FINOPS / TECHOPS second-CSV = NOT NEEDED | Stripe FDW already authoritative for SaaS contracts; `COMPONENT_SERVICE_MATRIX.csv` `api_spec_pointer` + `REPOSITORIES_REGISTRY.md` already cover API metadata. No third-source-of-truth need surfaced. | `reports/re-eval-trigger-finops-techops-second-csv.md` |
| **D-IH-15** (Wave-2 plan) | `compliance/<plane>/` physical relocation = DEFERRED | Initiative 22 D-IH-1 elected convention-only relocation; deprecation alias map already documents the forward path. No physical `git mv` until program 2 friction OR 2nd canonical CSV in a plane. KIR onboarded smoothly in I23-P6 — no friction surfaced. | `reports/re-eval-trigger-compliance-plane-relocation.md` |
| **D-IH-18** (Wave-2 plan) | Neo4j graph as canonical graph DDL surface; promotion to "mandatory in agent ladder" = DEFERRED | Initiative 23 P-graph shipped graph projection, but agent overlay (`OVERLAY_HLK_GRAPH.md`) keeps graph as **optional multi-hop** after CSV-backed ids. Promotion to mandatory tier requires UAT evidence of operator reliance. | `reports/re-eval-trigger-graph-mcp-tooling-promotion.md` |

## Independent ops-debt items (not deferral-driven)

These were captured as ops items during Wave-2 plan authoring, with operator-facing friction observed in I22-P5 (mmdc), I22-P6 (WeasyPrint), and I21-P7 (service_role posture):

| Item | Friction observed | Routed to phase |
|:-----|:------------------|:----------------|
| `mmdc` install non-determinism | Different operators rendered slightly different PNGs from the same `.mmd` source (Mermaid 10 vs 11 default theme + edge routing) | P1 — pinned `@^11` install runbook |
| Linux CI Chromium crashes | Bundled Chromium (puppeteer) silently crashes on Ubuntu without `libgbm1`/fonts/`--no-sandbox` | P1 — Linux CI extras documented |
| WeasyPrint GTK3 friction (Windows) | Operator-only friction; renderer chain falls back to fpdf2 transparently but PDF fidelity drops | P3 — Windows-specific GTK3 install runbook |
| `service_role` rotation hygiene | No quarterly rotation cadence documented; key longevity creates exposure surface | P2 — SOP-HLK_GOIPOI §6 procedure |

## What "evidence" looks like for I26 closure

Unlike compliance-CSV initiatives, I26 evidence is **operational confirmability**, not registry rows:

- **P0**: 3 templates exist + decision log seeded.
- **P1**: `mmdc --version` reports `^11.x` after running the documented install command.
- **P2**: First quarterly rotation entry recorded in I26 `decision-log.md` with date + operator initials (or in the SOP-HLK_GOIPOI §6 itself).
- **P3**: `python -c "from weasyprint import HTML"` succeeds after the documented install (Windows operator slot).
- **P4**: Either trigger fires (cascade ships) OR template stays "trigger not met" with operator confirmation.
- **P5 UAT**: Verification matrix passes; cursor-rules-hygiene checkbox confirmed.
