---
language: en
status: active
initiative: 65-akos-planning-workspace-panel
report_kind: risk-register
last_review: 2026-05-07
---

# Risk register — Initiative 65

| Id | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---|:---|:---|
| R-65-1 | GitHub API rate-limit exhaustion under heavy operator browsing | L | M | 60s TanStack Query cache + 5-min Supabase fallback cache; per-route shared loader; `If-None-Match` ETag use; capped concurrency in `lib/planning/github-reader.ts`. |
| R-65-2 | Markdown rendering exposes inline HTML / XSS | L | H | Server-side MDX compile with `remark-gfm` + `rehype-sanitize`; reject inline `<script>` and event-handler attributes; CSP header on `/operator/planning/*` disallows inline scripts. |
| R-65-3 | Operator confusion between `/operator/initiatives` (registry) and `/operator/planning/` (workspace) | M | M | Cross-link both ways: every `/operator/planning/<slug>` page has a "Registry view →" chip; every `/operator/initiatives` row has a "Workspace folder →" chip. README.md in `docs/wip/planning/` adds a section explaining the two views. |
| R-65-4 | Time-travel banner mistaken for live state | L | H | Pin banner to the top of the viewport with `--gov-warn` background and **explicit absolute date** (not relative); "back to live" chip is the only way to dismiss; print-stylesheet always shows the timestamp. |
| R-65-5 | Workspace markdown contains internal codenames that leak via showcase mode | L | M | `BRAND_JARGON_AUDIT.md` §4 enforced — but showcase mode shows fixture data, not real workspace markdown, so this risk is narrow. Add a dedicated `lint:jargon --route /operator/planning --mode showcase` check in P5. |
| R-65-6 | Slow markdown compile blocks the page | L | M | Streaming server-render; placeholder paragraph until MDX completes; stream individual reports as they finish; per-report budget 250ms. |
| R-65-7 | RLS bypass via cached path | L | H | Cache key includes `auth.uid()` and `access_level`; private content not cached across users; redaction layer in `lib/planning/redact.ts` runs after fetch and before cache write. |
| R-65-8 | Initiative folder rename breaks deeplinks | M | L | `lib/planning/redirect.ts` reads a small `_redirects.json` maintained per rename; archived links stay alive; new structure flagged for 30 days. |
