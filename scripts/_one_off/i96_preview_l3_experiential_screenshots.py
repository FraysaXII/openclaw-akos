#!/usr/bin/env python3
"""I96 Preview L3.5 experiential screenshots — Vercel PR preview host."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "artifacts" / "uat-screenshots" / "i96-research-center-preview-2026-06-13"

PREVIEW_BASE = os.environ.get(
    "I96_PREVIEW_BASE",
    "https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app",
)
BYPASS = os.environ.get("VERCEL_AUTOMATION_BYPASS_SECRET", "").strip()
HEAD_SHA = os.environ.get("I96_PREVIEW_SHA", "e47d8b9")
DEPLOY_ID = os.environ.get("I96_VERCEL_DEPLOY_ID", "dpl_8PobeHi92NB1gARScp4SHBXKSy5P")
PR_URL = os.environ.get("I96_PREVIEW_PR_URL", "https://github.com/FraysaXII/hlk-erp/pull/36")

CAPTURES = [
    ("01", "operator", "discover", "operator"),
    ("02", "operator", "triage", "operator"),
    ("03", "operator", "drawer-open", "operator"),
    ("04", "operator", "audit", "operator"),
    ("05", "director", "discover", "director"),
    ("06", "director", "triage", "director"),
    ("07", "director", "drawer-open", "director"),
    ("08", "director", "audit", "director"),
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extra_headers() -> dict[str, str]:
    if not BYPASS:
        return {}
    return {"x-vercel-protection-bypass": BYPASS}


def auth_url(pov: str) -> str:
    next_path = f"/research-center?pov={pov}"
    base = f"{PREVIEW_BASE}/api/dev/sign-in?next={next_path.replace('/', '%2F').replace('?', '%3F').replace('=', '%3D')}"
    if BYPASS:
        return f"{base}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS}"
    return base


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    captured_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    manifest_rows: list[dict] = []
    errors: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            extra_http_headers=extra_headers(),
        )
        page = context.new_page()

        for seq, lens, stage, pov in CAPTURES:
            filename = f"{seq}-{lens}-{stage}-1280-auth-dev-password.png"
            out_path = OUT_DIR / filename
            route = f"/research-center?pov={pov}"

            try:
                if stage == "discover":
                    page.goto(auth_url(pov), wait_until="networkidle", timeout=90_000)
                    page.wait_for_selector("h1:has-text('Research Center')", timeout=45_000)
                elif stage == "triage":
                    page.goto(f"{PREVIEW_BASE}{route}", wait_until="networkidle", timeout=90_000)
                    page.wait_for_selector("h1:has-text('Research Center')", timeout=45_000)
                elif stage == "drawer-open":
                    page.goto(f"{PREVIEW_BASE}{route}", wait_until="networkidle", timeout=90_000)
                    page.wait_for_selector("h1:has-text('Research Center')", timeout=45_000)
                    details = page.get_by_role("button", name="Details").first
                    if details.count():
                        details.click()
                        page.wait_for_timeout(800)
                    else:
                        page.get_by_text("Details", exact=False).first.click(timeout=5_000)
                        page.wait_for_timeout(800)
                elif stage == "audit":
                    page.goto(f"{PREVIEW_BASE}{route}", wait_until="networkidle", timeout=90_000)
                    page.wait_for_selector("h1:has-text('Research Center')", timeout=45_000)
                    accordion = page.get_by_text("v1 audit", exact=False).first
                    if accordion.count():
                        accordion.click()
                        page.wait_for_timeout(500)

                title = page.title()
                url = page.url
                if "vercel.com/login" in url or "Login" in title and "Vercel" in title:
                    raise RuntimeError(f"Vercel SSO wall at {url}")

                page.screenshot(path=str(out_path), full_page=False)
                manifest_rows.append(
                    {
                        "file": filename,
                        "route": route,
                        "viewport": "1280x800",
                        "pov_lens": lens,
                        "journey_stage": stage,
                        "auth_state": "dev-sign-in-authenticated",
                        "screenshot_sha256": sha256_file(out_path),
                        "captured_at": captured_at,
                        "notes": f"L3.5 Preview {lens} — {stage}",
                        "supersedes": None,
                    }
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{filename}: {exc}")

        browser.close()

    manifest = {
        "initiative": "I96-research-center-v2",
        "session": "2026-06-13-preview-l35-experiential",
        "verdict_scope": "preview-operator-director-l35",
        "capture_tool": "playwright",
        "ladder_tier": "L3.5-Preview",
        "deploy_tier": "preview",
        "deploy_verification": {
            "platform": "vercel",
            "workflow": "feature-branch-pr",
            "pr_url": PR_URL,
            "deploy_id": DEPLOY_ID,
            "source_sha": HEAD_SHA,
            "hostname": PREVIEW_BASE,
            "badge_expected": "Preview",
        },
        "auth": "auth-dev-password",
        "captured_at": captured_at,
        "captures": manifest_rows,
        "errors": errors,
    }
    (OUT_DIR / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if errors:
        print("CAPTURE_ERRORS:")
        for err in errors:
            print(err)
        return 1
    print(f"OK: {len(manifest_rows)} captures -> {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
