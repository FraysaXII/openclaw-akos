# P-G6 production UAT workflow notes (2026-06-14)

## Deploy poll

- `dpl_5ZdeDLcYqaUFYFJ6AR9JYo9vmw4Y` → **READY** @ `3787f06` (B2.4 Realtime)
- Vercel MCP `get_deployment` + `list_deployments` corroborated

## Walk outcome

| Check | Result |
|:---|:---|
| Charter host `erp.holistikaresearch.com/research-center` | **FAIL** — legacy v1 UI |
| `/sign-in?next=%2Fresearch-center` on charter host | **404** |
| Production badge on charter host | **Absent** |
| Vercel production URL `hlk-erp-git-main-holistika.vercel.app` | Redirects to magic-link sign-in (expected B1.5+) |
| `get_project` domains for `hlk-erp` | Only `*.vercel.app` — **no** `erp.holistikaresearch.com` |
| Journey PNGs 8/8 @1280 | **0/8** — BLOCKED |

## Operator actions required

1. **Attach** `erp.holistikaresearch.com` to Vercel `hlk-erp` production deployment (DNS + Vercel domain settings) so custom domain serves `3787f06` not legacy stack.
2. **Re-walk** after propagation: open `https://erp.holistikaresearch.com/sign-in?next=%2Fresearch-center`, enter work email, click magic link from inbox, then confirm Production badge + v2 Research Center.
3. **Re-run** P-G6 capture session — full 8 journey PNGs + L3.0 visual review.

## Validator expectation

`validate_uat_screenshot_evidence.py` → **FAIL** (0 journey files) — expected; verdict is honest FAIL not fake PASS.
