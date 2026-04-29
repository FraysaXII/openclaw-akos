# Initiative 26 — Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|:---|:-----|:----------:|:------:|:-----------|:------|:------:|
| **PR-26-1** | `mmdc` minor-version drift (e.g. `mermaid-cli` 11.4 → 11.5 changes default edge routing) renders the same `.mmd` differently across operators | medium | low | Pin to `^11`; document in CONTRIBUTING.md; if a future minor breaks renders, escalate to a stricter pin (`@11.4`) | Tech / DevOPS | OPEN |
| **PR-26-2** | Linux CI Chromium crashes silently when `libgbm1` / fonts missing — gives spurious render-failure signals | medium | medium | Document `apt-get install` line in CONTRIBUTING.md CI section; the `mermaid.ink` HTTP fallback in `render_km_diagrams.py` keeps degraded operation | Tech / DevOPS | OPEN |
| **PR-26-3** | Windows operator without GTK3 fails on `--format pdf` first try — silent fallback to fpdf2 hides the issue | low | low | CONTRIBUTING.md GTK3 section explains the fallback chain explicitly; `python -c "from weasyprint import HTML"` smoke test is the canary | Operator | OPEN |
| **PR-26-4** | `service_role` key rotation skipped or forgotten (quarterly cadence drifts to "annual or never") | medium | high | SOP-HLK_GOIPOI §6 calendar reminder pattern (last business day of each quarter); each rotation logged in I26 `decision-log.md` for audit | Compliance | OPEN |
| **PR-26-5** | Persistent re-eval-trigger templates rot — operator fills the trigger record but never reopens the underlying decision | low | medium | Each template has a "Trigger record" section with `fired_on` field; templates are reviewed during cursor-rules-hygiene check at every initiative closure (per `akos-planning-traceability.mdc`) | PMO | OPEN |
| **PR-26-6** | `compliance/<plane>/` physical relocation triggers (D-IH-15) but the cascade ripple breaks references | low when triggered | high | Cascade is documented in Wave-2 plan §"Initiative 26 P4": PRECEDENCE → akos modules → validators → `validate_hlk.py` → `sync_compliance_mirrors_from_csv.py` → mirror DDL → SOPs → tests; `git mv` for history; rollback = revert | Compliance + Tech | DEFERRED |
| **PR-26-7** | D-IH-18 trigger fires (graph reliance) but agent overlay promotion requires changes across `OVERLAY_HLK_GRAPH.md` + `OVERLAY_HLK_*` peers — risk of inconsistent agent ladder behaviour during transition | low when triggered | medium | Trigger template scoped narrowly: promote graph tools from "optional after CSV ids" to "mandatory after CSV ids"; do not change CSV-citation discipline. Document the overlay peer review in the trigger template | AI Engineer | DEFERRED |

## Burn-down

P0 closure target: 3 trigger templates + 4 standard artifacts (this file inclusive) live; PR-26-1..PR-26-7 all OPEN at P0 except those marked DEFERRED.

PR-26-1, PR-26-2 close when P1 (mmdc runbook) lands and is verified by an operator running the install fresh.
PR-26-3 closes when P3 (WeasyPrint runbook) lands.
PR-26-4 closes after first quarterly rotation cycle (Q3 2026).
PR-26-5 is a long-running discipline risk — closes only when all 3 trigger templates either fire-and-resolve or are explicitly retired.
PR-26-6 / PR-26-7 stay DEFERRED until the corresponding D-IH triggers fire.
