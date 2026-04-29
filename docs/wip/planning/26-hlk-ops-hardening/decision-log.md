# Initiative 26 — Decision log

| ID | Date | Decision | Rationale | Status |
|:---|:-----|:---------|:----------|:-------|
| **D-IH-26-A** | 2026-04-29 | **Pin `@mermaid-js/mermaid-cli` to `^11`** in the install runbook (`npm i -g @mermaid-js/mermaid-cli@^11`). | Non-pinned installs produce non-deterministic renders across operators (mmdc emits Mermaid version banner; Mermaid 10→11 changed default theme + edge-routing engine). Pinning to `^11` keeps minor updates flowing while locking the major. | **Approved** |
| **D-IH-26-B** | 2026-04-29 | **Linux CI extras for puppeteer-bundled Chromium**: `libgbm1 fonts-liberation fonts-noto-color-emoji` apt packages + `--no-sandbox` flag where the runner refuses unprivileged sandbox. | Without these, `mmdc` crashes silently on Ubuntu CI runners with `Failed to launch the browser process`. Documented in CONTRIBUTING.md so any new repo hosting `render_km_diagrams.py` can copy-paste the runbook. | **Approved** |
| **D-IH-26-C** | 2026-04-29 | **WeasyPrint GTK3 runbook is Windows-specific** in CONTRIBUTING.md (Linux/macOS get GTK3 from system packages or Homebrew). | The renderer chain is WeasyPrint → fpdf2 → pandoc; only Windows hits the GTK3 friction at runtime. Cross-link to `requirements-export.txt` (Initiative 22 P6 opt-in dependency). | **Approved** |
| **D-IH-26-D** | 2026-04-29 | **`service_role` rotation cadence = quarterly** unless an incident triggers earlier rotation. | Industry baseline; longer windows accumulate exposure surface; shorter windows produce operator fatigue + sync gaps. SOP-HLK_GOIPOI §6 carries the calendar reminder pattern (last business day of each quarter). | **Approved** |
| **D-IH-26-E** | 2026-04-29 | **`compliance/<plane>/` physical relocation = DEFERRED.** Trigger contract in `reports/re-eval-trigger-compliance-plane-relocation.md`. | Per Wave-2 plan D-IH-15 + Initiative 22 D-IH-1: the convention is documented, the deprecation alias map exists in `compliance/README.md`, but physical `git mv` is reserved for a dedicated initiative when (a) program 2 onboarding surfaces friction OR (b) a second canonical CSV joins a plane. As of 2026-04-29 (I23 P6 closed with KIR onboarded smoothly), neither trigger has fired. | **Deferred** |

## Re-evaluation triggers (cross-initiative, persistent)

The 3 templates created in P0 are persistent — they live as reports/ until the underlying decision is reopened:

- **D-IH-14** (FINOPS/TECHOPS second CSV) → [`reports/re-eval-trigger-finops-techops-second-csv.md`](reports/re-eval-trigger-finops-techops-second-csv.md)
- **D-IH-15** (compliance/<plane>/ physical relocation) → [`reports/re-eval-trigger-compliance-plane-relocation.md`](reports/re-eval-trigger-compliance-plane-relocation.md)
- **D-IH-18** (Neo4j graph MCP tooling promotion) → [`reports/re-eval-trigger-graph-mcp-tooling-promotion.md`](reports/re-eval-trigger-graph-mcp-tooling-promotion.md)

When any trigger fires:

1. Operator records the trigger event in the corresponding template's "Trigger record" section.
2. Spawn a focused initiative (or fold into the next ops-hardening cycle).
3. After the action lands, mark the template "FIRED + RESOLVED on `<YYYY-MM-DD>`" and link to the closure PR.
