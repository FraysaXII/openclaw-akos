#!/usr/bin/env python3
"""Initiative 48 -- Operator-facing UAT Dossier renderer (P2 snapshot mode).

Aggregates the existing CLI ecosystem into a single brand-aligned multi-format
artifact pack at ``artifacts/uat-dossier/uat-dossier-<UTC>/``:

- ``dossier.md``    -- canonical markdown body (12 sections per dossier-section-spec.md)
- ``dossier.pdf``   -- brand-aligned PDF (P4; reuses ``akos.hlk_pdf_render.render_pdf_branded``)
- ``dossier.html``  -- standalone styled HTML (P5; no JS / no CDN)
- ``manifest.json`` -- sha256 + per-section metrics + run config + git_sha + UTC

3 modes per D-IH-48-C:
- ``--mode snapshot`` (default; ~10s; reads existing artifacts only; offline-safe)
- ``--mode live`` (P3; ~5min; runs all 10 CLIs)
- ``--mode tier-b`` (P3+; ~15min + cost; opt-in via ``AKOS_DOSSIER_TIER_B=1``; D-IH-48-L)

Filters (P6) per D-IH-48-D:
- ``--initiative <NN>`` filter to one initiative
- ``--persona <id>`` filter to one persona's scenario library
- ``--since <YYYY-MM-DD>`` filter trend section to date window

Cost discipline (D-IH-48-L):
- ``MAX_DOSSIER_USD`` env caps spend (default $2/run; refuses to run when cap hit)
- ``--mode tier-b`` requires ``AKOS_DOSSIER_TIER_B=1`` env (env-gate same posture as I47 D-IH-47-L real-chaos)

Usage::

    py scripts/render_uat_dossier.py
    py scripts/render_uat_dossier.py --mode snapshot --format md
    py scripts/render_uat_dossier.py --mode snapshot --format all --persona PERSONA-INVESTOR-COLD
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier.run import (
    DEFAULT_TREND_WINDOW,
    VALID_FORMATS,
    VALID_MODES,
    DossierFilter,
    DossierRun,
    is_tier_b_opted_in,
    resolve_max_dossier_usd,
    resolve_run_dir,
)
from akos.dossier.sections import SECTION_CLASSES, Section01ExecutiveSummary

logger = logging.getLogger("scripts.render_uat_dossier")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    p.add_argument(
        "--mode", default="snapshot", choices=list(VALID_MODES),
        help="snapshot (offline; ~10s) | live (~5min; P3) | tier-b (~15min; P3+; env-gated)",
    )
    p.add_argument(
        "--format", default="md", choices=list(VALID_FORMATS),
        help="md | pdf (P4) | html (P5) | all",
    )
    # P6 filters
    p.add_argument("--initiative", default="",
                   help="Filter to one initiative (e.g. 47)")
    p.add_argument("--persona", default="",
                   help="Filter to one persona_id (e.g. PERSONA-INVESTOR-COLD)")
    p.add_argument("--since", default="",
                   help="Filter trend section to date window (YYYY-MM-DD)")
    # Cost + cache discipline
    p.add_argument("--max-staleness-hours", type=float, default=24.0,
                   help="Override per-section staleness threshold (default 24h)")
    p.add_argument("--max-spend", type=float, default=None,
                   help="Override MAX_DOSSIER_USD env cap (default $2/run for --mode tier-b)")
    p.add_argument("--trend-window", type=int, default=DEFAULT_TREND_WINDOW,
                   help=f"Section 11 trend N data points (default {DEFAULT_TREND_WINDOW})")
    # P3 opt-ins
    p.add_argument("--screenshots", action="store_true",
                   help="P3 opt-in: capture browser screenshots via Cursor MCP (best-effort)")
    # P8 CI flags
    p.add_argument("--gh-pr-comment", action="store_true",
                   help="P8: emit comment-friendly markdown for `gh pr comment` (truncated <65k chars)")
    # Output control
    p.add_argument("--out-dir", type=Path, default=None,
                   help="Override output directory (default artifacts/uat-dossier/uat-dossier-<UTC>/)")
    p.add_argument("--quiet", action="store_true",
                   help="Suppress per-section progress logging")
    p.add_argument("--json", action="store_true",
                   help="Emit JSON manifest to stdout instead of progress prose")
    return p.parse_args(argv)


def _resolve_git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT),
            text=True, timeout=3,
        ).strip()
    except Exception:
        return "unknown"


def _refuse_tier_b_without_optin(args: argparse.Namespace) -> int | None:
    """D-IH-48-L: tier-b mode requires AKOS_DOSSIER_TIER_B=1 env."""
    if args.mode != "tier-b":
        return None
    if not is_tier_b_opted_in():
        sys.stderr.write(
            "REFUSED: --mode tier-b requires AKOS_DOSSIER_TIER_B=1 env (D-IH-48-L cost discipline).\n"
            "         Set the env explicitly, or use --mode live (no Tier B; no cost) / --mode snapshot.\n"
        )
        return 10
    return None


def _build_dossier(args: argparse.Namespace) -> DossierRun:
    """Instantiate DossierRun + invoke each Section in SECTION_CLASSES order.

    Per dossier-section-spec.md: Section 1 (Executive summary) is computed LAST
    after Sections 2-12 have gathered, then placed FIRST in render order
    (DossierRun.to_markdown() handles the ordering invariant).
    """
    git_sha = _resolve_git_sha()
    run = DossierRun(
        git_sha=git_sha,
        mode=args.mode,
        formats=tuple([args.format] if args.format != "all" else ["md", "pdf", "html"]),
        filter=DossierFilter(
            initiative=(args.initiative or None),
            persona_id=(args.persona or None),
            since=(args.since or None),
        ),
    )
    started_perf = time.perf_counter()

    # Run sections 2-12 first (gather + render)
    prior_results = []
    for cls in SECTION_CLASSES:
        if cls.section_id == 1:
            continue  # defer Section 1 until end
        section = cls()
        if not args.quiet:
            sys.stderr.write(f"  [Section {section.section_id:02d}] gathering {section.name}...\n")
        result = section.execute(mode=run.mode, filter=run.filter)
        prior_results.append(result)
        run.add(result)

    # Now compute Section 1 from prior_results
    section1 = Section01ExecutiveSummary()
    if not args.quiet:
        sys.stderr.write("  [Section 01] computing executive summary from prior sections...\n")
    data = section1.gather(mode=run.mode, filter=run.filter, prior_results=prior_results)
    md = section1.render_markdown(data)
    metrics = section1.metrics_for_trend(data)
    from akos.dossier.run import DossierSectionResult
    section1_result = DossierSectionResult(
        section_id=1, name=section1.name,
        status=data.payload.get("status", "PASS"),
        markdown=md, metrics=metrics, data_age_seconds=0.0,
    )
    run.add(section1_result)

    run.elapsed_ms = int((time.perf_counter() - started_perf) * 1000)
    return run


def _write_outputs(run: DossierRun, args: argparse.Namespace) -> dict[str, Path]:
    """Write the requested formats to the per-run artifact directory.

    Returns ``{format: path}`` mapping for written files.
    """
    out_dir = args.out_dir or resolve_run_dir(run)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}

    md_text = run.to_markdown()
    md_path = out_dir / "dossier.md"
    md_path.write_text(md_text, encoding="utf-8")
    written["md"] = md_path

    if args.format in ("pdf", "all"):
        # P4: brand-aligned PDF via render_pdf_branded (D-IH-48-H + D-IH-48-H1).
        # Soft-success: WeasyPrint -> fpdf2 -> pandoc -> markdown-sidecar fallback.
        from akos.dossier.pdf_render import render_dossier_pdf
        pdf_path = out_dir / "dossier.pdf"
        rc = render_dossier_pdf(run, md_text, pdf_path)
        if pdf_path.is_file():
            written["pdf"] = pdf_path
        else:
            # Sidecar fallback wrote dossier.pdf.md instead
            sidecar = out_dir / "dossier.pdf.md"
            if sidecar.is_file():
                written["pdf_sidecar"] = sidecar

    if args.format in ("html", "all"):
        # P5 will wire full render_dossier_html; for P2 just emit a minimal HTML with sections via section_to_html_details.
        html_text = _render_minimal_html(run)
        html_path = out_dir / "dossier.html"
        html_path.write_text(html_text, encoding="utf-8")
        written["html"] = html_path

    screenshots: list[Path] = []
    if args.screenshots:
        from akos.dossier.runner import take_browser_screenshots
        screenshots = take_browser_screenshots(out_dir)
        written["screenshots_dir"] = out_dir / "screenshots"

    pdf_path = written.get("pdf")
    manifest = run.to_manifest(
        md_text=md_text,
        pdf_path=pdf_path if isinstance(pdf_path, Path) else None,
        html_text=written.get("html") and written["html"].read_text(encoding="utf-8") or None,
        screenshots=screenshots,
    )
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    written["manifest"] = manifest_path

    return written


def _render_minimal_html(run: DossierRun) -> str:
    """P2 placeholder HTML: sections via section_to_html_details + brand CSS variables.

    P5 will replace with full render_dossier_html() including markdown library
    invocation + sparkline embedding.
    """
    from akos.dossier.html_render import BRAND_CSS_VARS, section_to_html_details
    body_parts = []
    # SECTION_CLASSES is in 1..12 order; render in that order.
    for r in sorted(run.section_results, key=lambda x: x.section_id):
        # Find class by section_id to get default_open_html
        cls = next((c for c in SECTION_CLASSES if c.section_id == r.section_id), None)
        default_open = cls.default_open_html if cls else False
        body_parts.append(section_to_html_details(
            section_id=r.section_id, name=r.name,
            markdown_body=r.markdown, default_open=default_open,
        ))
    body = "\n".join(body_parts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AKOS Operator UAT Dossier — {run.run_id}</title>
<style>
{BRAND_CSS_VARS}
body {{ font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  background: var(--c-background); color: var(--c-foreground);
  max-width: 960px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; }}
h1 {{ color: var(--c-accent-primary); border-bottom: 2px solid var(--c-accent-primary); padding-bottom: 0.5rem; }}
details.dossier-section {{ background: var(--c-card); border: 1px solid var(--c-border);
  border-radius: 0.5rem; padding: 1rem 1.25rem; margin: 0.75rem 0; }}
details.dossier-section > summary {{ cursor: pointer; font-size: 1.05rem; }}
details.dossier-section > summary > strong {{ color: var(--c-accent-primary); }}
.dossier-section-body pre {{ white-space: pre-wrap; word-break: break-word; font-family: inherit;
  background: var(--c-secondary); padding: 0.75rem; border-radius: 0.25rem; overflow-x: auto; }}
header dl {{ display: grid; grid-template-columns: max-content 1fr; gap: 0.25rem 1rem; }}
header dt {{ color: var(--c-muted-foreground); }}
</style>
</head>
<body>
<header>
<h1>AKOS Operator UAT Dossier</h1>
<dl>
<dt>run_id</dt><dd><code>{_html_escape(run.run_id)}</code></dd>
<dt>started_at</dt><dd>{_html_escape(run.started_at)}</dd>
<dt>git_sha</dt><dd><code>{_html_escape(run.git_sha)}</code></dd>
<dt>mode</dt><dd><strong>{_html_escape(run.mode)}</strong></dd>
<dt>overall_status</dt><dd><strong>{_html_escape(run.overall_status)}</strong></dd>
<dt>elapsed_ms</dt><dd>{run.elapsed_ms}</dd>
</dl>
</header>
<main>
{body}
</main>
<footer style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--c-border); color: var(--c-muted-foreground); font-size: 0.85rem;">
<p>Generated by <code>py scripts/render_uat_dossier.py --mode {_html_escape(run.mode)}</code> (Initiative 48)</p>
</footer>
</body>
</html>
"""


def _html_escape(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    refuse = _refuse_tier_b_without_optin(args)
    if refuse is not None:
        return refuse

    cap = args.max_spend if args.max_spend is not None else resolve_max_dossier_usd()
    if not args.quiet:
        sys.stderr.write(
            f"\n  AKOS Operator UAT Dossier\n"
            f"  =========================\n"
            f"  mode: {args.mode}\n"
            f"  format: {args.format}\n"
            f"  filter: initiative={args.initiative or '-'}, persona={args.persona or '-'}, since={args.since or '-'}\n"
            f"  cost cap: ${cap:.2f}/run\n\n"
        )

    run = _build_dossier(args)
    written = _write_outputs(run, args)

    if args.json:
        sys.stdout.write(json.dumps(run.manifest, indent=2, sort_keys=True))
        sys.stdout.write("\n")
    else:
        sys.stdout.write(
            f"\n  DONE. Dossier written to:\n"
            + "\n".join(f"    - {_repo_relative(p)}" for p in written.values())
            + f"\n\n  Overall status: {run.overall_status}\n"
            + f"  Elapsed: {run.elapsed_ms}ms\n"
        )

    return 0 if run.overall_status != "FAIL" else 1


def _repo_relative(path: Path) -> str:
    """Best-effort relative path; falls back to absolute when path is outside REPO_ROOT (e.g. --out-dir to tmp)."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    sys.exit(main())
