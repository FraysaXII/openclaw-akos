/**
 * I96 Preview L3.5 experiential screenshots — Vercel PR preview host.
 * Run: node scripts/_one_off/i96_preview_l3_experiential_screenshots.mjs
 */
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..", "..");
const OUT_DIR = join(
  ROOT,
  "artifacts",
  "uat-screenshots",
  "i96-research-center-preview-2026-06-13",
);

const PREVIEW_BASE =
  process.env.I96_PREVIEW_BASE ??
  "https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app";
const BYPASS = (process.env.VERCEL_AUTOMATION_BYPASS_SECRET ?? "").trim();
const HEAD_SHA = process.env.I96_PREVIEW_SHA ?? "e47d8b9";
const DEPLOY_ID =
  process.env.I96_VERCEL_DEPLOY_ID ?? "dpl_8PobeHi92NB1gARScp4SHBXKSy5P";
const PR_URL =
  process.env.I96_PREVIEW_PR_URL ??
  "https://github.com/FraysaXII/hlk-erp/pull/36";

const CAPTURES = [
  ["01", "operator", "discover", "operator"],
  ["02", "operator", "triage", "operator"],
  ["03", "operator", "drawer-open", "operator"],
  ["04", "operator", "audit", "operator"],
  ["05", "director", "discover", "director"],
  ["06", "director", "triage", "director"],
  ["07", "director", "drawer-open", "director"],
  ["08", "director", "audit", "director"],
];

function sha256File(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function extraHeaders() {
  return BYPASS ? { "x-vercel-protection-bypass": BYPASS } : {};
}

function authUrl(pov) {
  const nextPath = `/research-center?pov=${pov}`;
  const encoded = encodeURIComponent(nextPath);
  let url = `${PREVIEW_BASE}/api/dev/sign-in?next=${encoded}`;
  if (BYPASS) {
    url += `&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass=${BYPASS}`;
  }
  return url;
}

async function main() {
  mkdirSync(OUT_DIR, { recursive: true });
  const capturedAt = new Date().toISOString();
  const manifestRows = [];
  const errors = [];

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    extraHTTPHeaders: extraHeaders(),
  });
  const page = await context.newPage();

  for (const [seq, lens, stage, pov] of CAPTURES) {
    const filename = `${seq}-${lens}-${stage}-1280-auth-dev-password.png`;
    const outPath = join(OUT_DIR, filename);
    const route = `/research-center?pov=${pov}`;

    try {
      if (stage === "discover") {
        await page.goto(authUrl(pov), { waitUntil: "networkidle", timeout: 90_000 });
        await page.getByRole("heading", { name: "Research Center" }).waitFor({
          timeout: 45_000,
        });
      } else {
        await page.goto(`${PREVIEW_BASE}${route}`, {
          waitUntil: "networkidle",
          timeout: 90_000,
        });
        await page.getByRole("heading", { name: "Research Center" }).waitFor({
          timeout: 45_000,
        });
        if (stage === "drawer-open") {
          const details = page.getByRole("button", { name: "Details" }).first();
          if (await details.count()) {
            await details.click();
          } else {
            await page.getByText("Details").first().click({ timeout: 5_000 });
          }
          await page.waitForTimeout(800);
        } else if (stage === "audit") {
          const accordion = page.getByText("v1 audit").first();
          if (await accordion.count()) {
            await accordion.click();
            await page.waitForTimeout(500);
          }
        }
      }

      const url = page.url();
      const title = await page.title();
      if (url.includes("vercel.com/login") || (title.includes("Vercel") && title.includes("Login"))) {
        throw new Error(`Vercel SSO wall at ${url}`);
      }

      await page.screenshot({ path: outPath, fullPage: false });
      manifestRows.push({
        file: filename,
        route,
        viewport: "1280x800",
        pov_lens: lens,
        journey_stage: stage,
        auth_state: "dev-sign-in-authenticated",
        screenshot_sha256: sha256File(outPath),
        captured_at: capturedAt,
        notes: `L3.5 Preview ${lens} — ${stage}`,
        supersedes: null,
      });
    } catch (err) {
      errors.push(`${filename}: ${err.message}`);
    }
  }

  await browser.close();

  const manifest = {
    initiative: "I96-research-center-v2",
    session: "2026-06-13-preview-l35-experiential",
    verdict_scope: "preview-operator-director-l35",
    capture_tool: "playwright",
    ladder_tier: "L3.5-Preview",
    deploy_tier: "preview",
    deploy_verification: {
      platform: "vercel",
      workflow: "feature-branch-pr",
      pr_url: PR_URL,
      deploy_id: DEPLOY_ID,
      source_sha: HEAD_SHA,
      hostname: PREVIEW_BASE,
      badge_expected: "Preview",
    },
    auth: "auth-dev-password",
    captured_at: capturedAt,
    captures: manifestRows,
    errors,
  };

  writeFileSync(join(OUT_DIR, "MANIFEST.json"), `${JSON.stringify(manifest, null, 2)}\n`);

  if (errors.length) {
    console.error("CAPTURE_ERRORS:");
    for (const e of errors) console.error(e);
    process.exit(1);
  }
  console.log(`OK: ${manifestRows.length} captures -> ${OUT_DIR}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
