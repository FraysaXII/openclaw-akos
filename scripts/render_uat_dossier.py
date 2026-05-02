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
    DossierSectionResult,
    is_tier_b_opted_in,
    resolve_max_dossier_usd,
    resolve_run_dir,
)
from akos.dossier.sections import SECTION_CLASSES, Section01ExecutiveSummary, Section11TrendLines

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


def _extract_gh_pr_comment_body(md: str) -> str:
    """Slice Section 1 markdown for ``gh pr comment`` (GitHub 65k limit)."""
    lines = md.splitlines()
    start: int | None = None
    for i, line in enumerate(lines):
        if line.startswith("## Section 1 "):
            start = i
            break
    if start is None:
        return md[:65000]
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## Section ") and not lines[j].startswith("## Section 1 "):
            end = j
            break
    body = "\n".join(lines[start:end])
    footer = (
        "\n\n---\n_Auto-generated executive summary from "
        "`py scripts/render_uat_dossier.py --gh-pr-comment` (Initiative 48)._"
    )
    return (body + footer)[:65000]


def _build_dossier(args: argparse.Namespace) -> DossierRun:
    """Instantiate DossierRun + invoke each Section in SECTION_CLASSES order.

    Per dossier-section-spec.md: Section 1 (Executive summary) is computed LAST
    after Sections 2-12 have gathered, then placed FIRST in render order
    (DossierRun.to_markdown() handles the ordering invariant).

    Section 11 is gathered after Sections 2-10 and 12 so a synthetic *current*
    rollup can be appended to history for sparklines (P7).
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
            trend_window=int(args.trend_window) if getattr(args, "trend_window", None) else DEFAULT_TREND_WINDOW,
        ),
    )
    started_perf = time.perf_counter()

    prior_results: list[DossierSectionResult] = []
    from akos.dossier.sources import gather_trend_sparklines

    for cls in SECTION_CLASSES:
        if cls.section_id in (1, 11):
            continue
        section = cls()
        if not args.quiet:
            sys.stderr.write(f"  [Section {section.section_id:02d}] gathering {section.name}...\n")
        result = section.execute(mode=run.mode, filter=run.filter)
        prior_results.append(result)
        run.add(result)

    s11 = Section11TrendLines()
    if not args.quiet:
        sys.stderr.write(f"  [Section {s11.section_id:02d}] gathering {s11.name}...\n")
    d11 = gather_trend_sparklines(
        trend_window=run.filter.trend_window,
        since=run.filter.since,
        prior_section_results=list(prior_results),
        current_started_at=run.started_at,
    )
    r11 = DossierSectionResult(
        section_id=11,
        name=s11.name,
        status=s11._infer_status(d11),
        markdown=s11.render_markdown(d11),
        metrics=s11.metrics_for_trend(d11),
        data_age_seconds=0.0,
        placeholder=d11.placeholder,
        error=d11.error,
    )
    prior_results.append(r11)
    run.add(r11)

    section1 = Section01ExecutiveSummary()
    if not args.quiet:
        sys.stderr.write("  [Section 01] computing executive summary from prior sections...\n")
    data = section1.gather(mode=run.mode, filter=run.filter, prior_results=prior_results)
    md = section1.render_markdown(data)
    metrics = section1.metrics_for_trend(data)
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
        # P5: full render_dossier_html (markdown library + brand CSS + collapsible details + inline SVG sparkline support).
        from akos.dossier.html_render import render_dossier_html
        html_text = render_dossier_html(run)
        html_path = out_dir / "dossier.html"
        html_path.write_text(html_text, encoding="utf-8")
        written["html"] = html_path

        # Operator Console (post-closure enhancement): qualitative companion
        # with charts, persona heatmap, scenario cards, decision log, cassette
        # samples. Standalone HTML; same brand SSOT; no JS / no CDN.
        try:
            from akos.dossier.console_render import render_console_html
            console_text = render_console_html(run)
            console_path = out_dir / "dossier-console.html"
            console_path.write_text(console_text, encoding="utf-8")
            written["console"] = console_path
        except Exception as exc:  # noqa: BLE001 - console is best-effort
            logger.warning("console render skipped: %s", exc)

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
    if "console" in written and written["console"].is_file():
        import hashlib as _hashlib
        console_text = written["console"].read_text(encoding="utf-8")
        manifest.setdefault("files", {})["dossier-console.html"] = {
            "sha256": _hashlib.sha256(console_text.encode("utf-8")).hexdigest(),
            "char_count": len(console_text),
        }
    from akos.dossier.dossier_run_writer import write_dossier_run_row
    md_sha = (manifest.get("files", {}).get("dossier.md") or {}).get("sha256") or ""
    stats = write_dossier_run_row(
        run_id=run.run_id,
        started_at=run.started_at,
        mode=run.mode,
        git_sha=run.git_sha,
        section_metrics=manifest.get("section_metrics") or {},
        manifest_sha256=md_sha,
    )
    manifest["dossier_run_writer"] = stats
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    written["manifest"] = manifest_path

    return written




def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    refuse = _refuse_tier_b_without_optin(args)
    if refuse is not None:
        return refuse

    if args.gh_pr_comment:
        args.quiet = True
        run = _build_dossier(args)
        sys.stdout.write(_extract_gh_pr_comment_body(run.to_markdown()))
        sys.stdout.write("\n")
        return 0

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
