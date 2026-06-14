# I96 Preview L3.5 — experiential capture (2026-06-14, v2 recapture)

**Scope:** Operator + Director @1280 · discover → triage → drawer-open → audit · Vercel PR preview host  
**Tools:** Cursor Browser MCP (operator magic-link session) — **parent agent foreground only**  
**Preview URL:** https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app  
**PR:** https://github.com/FraysaXII/hlk-erp/pull/36 · SHA **`eedcd1d`**

## v1 incident (do not repeat)

Subagent marked 8/8 VALID without reading PNGs. Director `06`/`08` were byte-identical; director shots were expanded-sidebar crops (~22KB). Operator drawer v1 was blurry.

## v2 canonical journey files

| File | Verdict | Notes |
|:---|:---:|:---|
| `01-operator-discover-1280-magiclink.png` | VALID | v1 retained |
| `02-operator-triage-1280-magiclink.png` | VALID | v1 retained |
| `03-operator-drawer-open-1280-magiclink-v2.png` | VALID | supersedes v1 |
| `04-operator-audit-1280-magiclink.png` | VALID | v1 retained |
| `05-director-discover-1280-magiclink-v2.png` | VALID | PREVIEW badge; supersedes v1 |
| `06-director-triage-1280-magiclink-v2.png` | VALID | P10-T2 PAUSED card |
| `07-director-drawer-open-1280-magiclink-v2.png` | VALID | drawer phase blocker |
| `08-director-audit-1280-magiclink-v2.png` | VALID | WIP research packs panel |

**Mechanical gate:** `py scripts/validate_uat_screenshot_evidence.py --session-dir .` → **PASS**  
**Visual review:** [`agent_visual_review.json`](agent_visual_review.json)  
**SOP:** [`SOP-EXPERIENTIAL_UAT_AGENT_VISUAL_REVIEW_001.md`](../../../docs/wip/planning/96-research-data-plane-and-research-center/reports/SOP-EXPERIENTIAL_UAT_AGENT_VISUAL_REVIEW_001.md)

## Capture hygiene (binding)

1. CDP viewport 1280×800  
2. **Collapse sidebar** before shutter  
3. Scroll audit region into view for audit-stage shots  
4. Parent agent reads every PNG — no subagent visual sign-off
