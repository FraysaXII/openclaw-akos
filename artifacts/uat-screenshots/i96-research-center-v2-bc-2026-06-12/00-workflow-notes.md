# I96 Phase B Wave B1 — L1 journey smoke (2026-06-13)

**Scope:** Operator lens @1280 after hlk-erp Wave B1 (journey chrome + Operator T2 BFF cards).

| Shot | Journey stage | Components visible |
|:---|:---|:---|
| `journey-operator-discover-1280.png` | Discover | POV switcher, JourneyStepIndicator, FreshnessStrip micro-CTAs, ProngStrip |
| `journey-operator-triage-1280.png` | Triage | InsightRailHeader (lens + count + ≤7 hint), insight card rail |
| `journey-operator-act-1280.png` | Act | Drill-down Sheet — runbook Act block |
| `journey-operator-audit-1280.png` | Verify/Audit | v1 accordion expanded |

**Mechanical:** `npm run typecheck` PASS (hlk-erp). Live URL: `http://localhost:3010/research-center?pov=operator`.

**Note:** Staleness / env_deploy cards emit only when radar overdue or planning reader unset — this localhost run showed remediation trio + strip micro-CTAs (Gate B live-only).

---

# I96 Phase B Wave B2 — L1 Director smoke (2026-06-13)

**Scope:** Director lens @1280 after hlk-erp Wave B2 (ledger completion + phase blocker + intent-criticality BFF + POV sort).

| Shot | Journey stage | Components visible |
|:---|:---|:---|
| `journey-director-discover-1280.png` | Discover | POV Director selected, journey indicator, freshness strip, prong strip |
| `journey-director-triage-1280.png` | Triage | Director rail — ledger completion + phase blocker cards (5 signals when env gaps add remediation) |
| `journey-director-act-1280.png` | Act | Drill-down Sheet on director card |
| `journey-director-audit-1280.png` | Verify/Audit | v1 accordion |

**Mechanical:** `npm run typecheck` PASS (hlk-erp). Live URL: `http://localhost:3010/research-center?pov=director`.

**Note:** Intent-criticality card uses latest `artifacts/index-sweep-*.json` when `AKOS_REPO_ROOT` resolves; otherwise live radar/ledger signals only (Gate B — no fixture). This capture had ledger reader returning 0 rows — remediation cards rank after director tactical cards per BFF sort.
