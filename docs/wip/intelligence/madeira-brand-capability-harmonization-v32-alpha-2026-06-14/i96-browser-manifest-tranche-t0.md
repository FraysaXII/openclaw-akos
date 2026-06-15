---
authored: 2026-06-14
tranche: T0 I96 manifest start
parent: t0-c-execution-spec
---

# I96 Research Center — browser manifest tranche (T0 start)

## Objective

Begin **experiential** evidence for Scenario B (parallel prep with Scenario A). Validator shape PASS is insufficient per experiential UAT charter.

## Manifest target

`artifacts/uat-screenshots/i96-research-center-v32-alpha-t0-2026-06-14/`

| # | Viewport | POV | State |
|:---:|:---:|:---|:---|
| 01 | 1280 | Operator | Discover |
| 02 | 1280 | Operator | Triage |
| 03 | 1280 | Operator | Drawer open |
| 04 | 1280 | Director | Discover |
| 05 | 375 | Operator | Discover |
| 06 | 768 | Operator | Discover |

## Preconditions

- `http://localhost:3010/sign-in?next=%2Fresearch-center` (dev password auth)
- HLK-ERP dev server on **3010**
- Post-login session (not anonymous smoke)

## Layers (charter stack)

1. Playwright anonymous smoke (existing spec) — mechanical
2. **This tranche** — Cursor Browser MCP walk
3. Impeccable disposition — after snapshots
4. axe scoped route
5. MANIFEST.json sha256

## Blockers

| Blocker | Owner | Carryover | Status 2026-06-15 |
|:---|:---|:---|:---|
| **hlk-erp path** | AIC | CO-MBH-006 | **Resolved** — `root_cd/hlk-erp`; dev on :3010; **6/6 captures VALID** |
| Auth / magic link localhost | AIC | Existing I96 notes | Dev path: `/api/dev/sign-in?next=/research-center` |
| BFF live data empty / KiRBe env | I96 | CO-96-001 | Expected on localhost (`KIRBE_API_URL` unset) — visible in drawer capture |
| SSL on production ERP | DevOps | Use localhost-first | Unchanged |

## Operator check-links

Update: `docs/wip/planning/96-research-data-plane-and-research-center/reports/operator-check-links-2026-06-12.md` when manifest lands.

## T0 scope note

T0 **starts** manifest plan + folder; full capture may complete in T0 or roll to T1 with **scheduled** posture on CO-MBH-006.
