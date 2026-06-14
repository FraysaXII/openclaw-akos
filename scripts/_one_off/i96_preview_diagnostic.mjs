import { chromium } from "playwright";

const BASE =
  "https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app";
const BYPASS = (process.env.VERCEL_AUTOMATION_BYPASS_SECRET ?? "").trim();
const OUT = "artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/00-diagnostic.png";

const urls = [
  `${BASE}/api/dev/sign-in?next=%2Fresearch-center%3Fpov%3Doperator`,
  `${BASE}/research-center?pov=operator`,
  `${BASE}/sign-in?next=%2Fresearch-center`,
];

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1280, height: 800 },
  extraHTTPHeaders: BYPASS ? { "x-vercel-protection-bypass": BYPASS } : {},
});
const page = await context.newPage();

for (const url of urls) {
  try {
    const resp = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60_000 });
    await page.waitForTimeout(2000);
    console.log("URL:", url);
    console.log("  final:", page.url());
    console.log("  title:", await page.title());
    console.log("  status:", resp?.status());
    const text = (await page.locator("body").innerText()).slice(0, 400).replace(/\s+/g, " ");
    console.log("  body:", text);
    console.log("---");
  } catch (e) {
    console.log("URL:", url, "ERR", e.message);
  }
}

await page.screenshot({ path: OUT, fullPage: true });
console.log("wrote", OUT);
await browser.close();
