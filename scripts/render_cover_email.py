#!/usr/bin/env python3
"""Render a `cover_email_*.md` to a deterministic HTML body for SMTP send.

Per `akos-external-render-discipline.mdc` RULE 4 mail heuristic + paired skill
`.cursor/skills/external-render-craft/SKILL.md` Surface 4 Pattern A. The
output HTML is meant to be embedded inline in the email body itself, not
attached as a file. Every render writes a sidecar `.manifest.json` with the
source + render sha256 trail (Initiative 24 G-24-3 closure trail shape).

Usage::

    py scripts/render_cover_email.py \\
        docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md \\
        --out artifacts/exports/cover_email_es-2026-05-19.html

When ``--out`` is omitted, defaults to::

    artifacts/exports/<source-stem>-<ISO-DATE>.html

Exit codes:
    0 — HTML written + manifest sidecar
    1 — refusal (source missing / unreadable)
    2 — usage error
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import logging
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos import log  # noqa: E402

log.setup_logging()
logger = logging.getLogger(__name__)

DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "exports"

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _strip_frontmatter(text: str) -> str:
    return FRONTMATTER_PATTERN.sub("", text, count=1)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _render_markdown(body: str) -> str:
    """Render markdown body to HTML via markdown-it (canonical) with fallback."""
    try:
        from markdown_it import MarkdownIt  # type: ignore[import-not-found]
        md = MarkdownIt("commonmark", {"breaks": True, "html": False})
        return md.render(body)
    except ImportError:
        try:
            import markdown  # type: ignore[import-not-found]
            return markdown.markdown(body, extensions=["extra", "smarty"])
        except ImportError:
            logger.warning(
                "Neither markdown-it nor markdown installed; emitting <pre>-wrapped body. "
                "Install via: pip install markdown-it-py"
            )
            return f"<pre>{body}</pre>"


HTML_ENVELOPE = (
    '<!DOCTYPE html>\n'
    '<html lang="{lang}">\n'
    '<head>\n'
    '  <meta charset="UTF-8">\n'
    '  <meta name="generator" content="render_cover_email.py">\n'
    '  <title>{title}</title>\n'
    '  <style>\n'
    '    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; '
    'font-size: 16px; line-height: 1.55; color: #1a1a1a; max-width: 640px; margin: 0; padding: 0; }}\n'
    '    h1, h2, h3 {{ font-weight: 600; }}\n'
    '    a {{ color: #0a4ec9; text-decoration: underline; }}\n'
    '    blockquote {{ border-left: 3px solid #d0d0d0; margin: 1em 0; padding: 0.4em 1em; color: #555; }}\n'
    '    code {{ background: #f4f4f4; padding: 0.1em 0.3em; border-radius: 3px; font-family: monospace; }}\n'
    '  </style>\n'
    '</head>\n'
    '<body>\n'
    '{body}\n'
    '</body>\n'
    '</html>\n'
)


def _extract_language(frontmatter: str) -> str:
    match = re.search(r"^language\s*:\s*(.+?)$", frontmatter, re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"').strip("'")
    return "en"


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Cover email"


def render(*, source: Path, out: Path, dry_run: bool = False) -> int:
    if not source.is_file():
        logger.error("source not found: %s", source)
        return 1

    try:
        source_bytes = source.read_bytes()
    except OSError as exc:
        logger.error("source unreadable: %s — %s", source, exc)
        return 1

    text = source_bytes.decode("utf-8")
    fm_match = FRONTMATTER_PATTERN.match(text)
    frontmatter = fm_match.group(1) if fm_match else ""
    body = _strip_frontmatter(text)
    language = _extract_language(frontmatter)
    title = _extract_title(body)

    inner_html = _render_markdown(body)
    full_html = HTML_ENVELOPE.format(lang=language, title=title, body=inner_html)

    source_sha = _sha256(source_bytes)
    html_bytes = full_html.encode("utf-8")
    html_sha = _sha256(html_bytes)

    if dry_run:
        logger.info(
            "dry_run: would write %s (%d bytes; html_sha256=%s..)",
            out, len(html_bytes), html_sha[:16],
        )
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(html_bytes)

    manifest = {
        "source_path": source.relative_to(REPO_ROOT).as_posix(),
        "source_sha256": source_sha,
        "rendered_html": out.relative_to(REPO_ROOT).as_posix() if out.is_relative_to(REPO_ROOT) else str(out),
        "render_sha256": html_sha,
        "rendered_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "render_tool": "markdown_it",
        "render_version": _detect_markdown_version(),
        "language": language,
        "title": title,
    }
    manifest_path = out.with_suffix(out.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    logger.info(
        "render_cover_email: wrote %s (%d bytes; html_sha256=%s..)",
        out.relative_to(REPO_ROOT) if out.is_relative_to(REPO_ROOT) else out,
        len(html_bytes),
        html_sha[:16],
    )
    return 0


def _detect_markdown_version() -> str:
    try:
        import markdown_it  # type: ignore[import-not-found]
        return f"markdown-it-py-{getattr(markdown_it, '__version__', 'unknown')}"
    except ImportError:
        try:
            import markdown  # type: ignore[import-not-found]
            return f"markdown-{getattr(markdown, '__version__', 'unknown')}"
        except ImportError:
            return "fallback-pre-tag"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path, help="Source cover_email_*.md file")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help=(
            "Output .html path. Defaults to "
            "artifacts/exports/<source-stem>-<ISO-DATE>.html"
        ),
    )
    p.add_argument("--dry-run", action="store_true", help="Compute hashes only; do not write")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source = args.source.resolve()
    if args.out is None:
        date_stamp = _dt.datetime.now(_dt.timezone.utc).date().isoformat()
        out = DEFAULT_OUT_DIR / f"{source.stem}-{date_stamp}.html"
    else:
        out = args.out.resolve()
    return render(source=source, out=out, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
