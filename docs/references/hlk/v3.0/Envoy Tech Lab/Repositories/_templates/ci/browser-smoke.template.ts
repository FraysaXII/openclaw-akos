/**
 * AKOS template — post-deploy live URL smoke for {{REPO_SLUG}} via the Cursor IDE Browser MCP.
 *
 * Rendered by bless into <repo>/scripts/browser-smoke.ts. Runs after a Vercel
 * deploy on `main` (or against PR previews) using the Cursor IDE Browser MCP
 * to navigate the deployed URL, snapshot, and assert key DOM elements.
 *
 * Mirrors AKOS's scripts/browser-smoke.py for the Node world. Skips gracefully
 * when the MCP is not configured in the runner — this is interactive by design,
 * never a hard CI gate.
 */

import { execSync } from "node:child_process"
import { existsSync } from "node:fs"
import { resolve } from "node:path"

interface SmokeAssertion {
  name: string
  selector: string
  must_contain?: string
}

interface SmokePlan {
  url: string
  assertions: SmokeAssertion[]
}

const PRODUCTION_PLAN: SmokePlan = {
  url: process.env.SMOKE_BASE_URL ?? "https://{{REPO_SLUG}}.example.com",
  assertions: [
    { name: "page-title", selector: "h1", must_contain: "{{REPO_SLUG}}" },
    { name: "freshness-ribbon", selector: "[data-testid=freshness-ribbon]" },
  ],
}

function mcpAvailable(): boolean {
  // Heuristic: MCP usage in this repo implies a `.cursor/mcp.json` or env var.
  if (process.env.CURSOR_BROWSER_MCP === "1") return true
  if (existsSync(resolve(process.cwd(), ".cursor", "mcp.json"))) return true
  return false
}

async function main() {
  if (!mcpAvailable()) {
    console.warn("[browser-smoke] Cursor IDE Browser MCP not configured; skipping (non-blocking).")
    process.exit(0)
  }
  console.log(`[browser-smoke] live url ${PRODUCTION_PLAN.url}; ${PRODUCTION_PLAN.assertions.length} assertion(s)`)
  // The actual MCP-driven smoke runs interactively from inside Cursor.
  // CI invocation is a stub: it logs the plan and exits 0. The plan file is
  // the source of truth that the operator runs through the IDE before merging.
  for (const a of PRODUCTION_PLAN.assertions) {
    console.log(`  - ${a.name}: ${a.selector}` + (a.must_contain ? ` ~ "${a.must_contain}"` : ""))
  }
  process.exit(0)
}

main().catch((err) => {
  console.error("[browser-smoke] unexpected error:", err)
  process.exit(1)
})
