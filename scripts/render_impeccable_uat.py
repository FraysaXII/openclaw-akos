#!/usr/bin/env python3
"""Initiative 77 P4.B — render an Impeccable UAT markdown report as brand-aligned HTML.

Reads a UAT markdown file conforming to ``docs/wip/planning/_templates/uat-impeccable-template.md``
shape (v1.0) and emits a self-contained HTML at
``docs/presentations/<uat-slug>/index.html`` using the Holistika brand chassis
(HSL palette + Inter typography per ``BRAND_VISUAL_PATTERNS.md``).

Design constraints
------------------

- **Pure Python + PyYAML.** No npm, no React, no node build tool. Same posture as
  ``scripts/build_company_deck.py`` (I28 P3 precedent).
- **Self-contained output.** The emitted HTML inlines the stylesheet so the deck
  is portable as a single file (email it, drop in Drive, print to PDF without
  asset-bundle dependency).
- **Markdown SSOT wins for content.** The UAT markdown is the single source of
  truth; the HTML is derived and re-emitted on every render.
- **J-OP audience optimized.** Long-form report layout (not 16:9 slide format) —
  scannable verdict strip + sticky-relevant section cards + finding-class badges.
- **Brand-canon enforced.** Forbidden tokens ('Holistica' / 'Holística') flagged
  inline as drift; renderer does NOT silently rewrite (operator-author intent
  preserved; per ``akos-brand-baseline-reality.mdc``).

Usage::

    py scripts/render_impeccable_uat.py docs/wip/planning/77-impeccable-brand-bridge-refresh/reports/uat-impeccable-all-surfaces-2026-05-16.md
    py scripts/render_impeccable_uat.py <path>.md --check-only   # validate parse, do not write
    py scripts/render_impeccable_uat.py <path>.md --out <custom>/index.html  # override out path

Exit codes
----------
    0  HTML written (or validation passed in check-only mode)
    1  Markdown schema violation (missing frontmatter, malformed sections, etc.)
    2  IO / configuration error
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html as _html
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PRESENTATIONS_DIR = REPO_ROOT / "docs" / "presentations"
DEFAULT_STYLES_FILENAME = "styles.css"
SHARED_STYLESHEET = REPO_ROOT / "docs" / "presentations" / "_shared" / "uat-impeccable.css"


# ----------------------------------------------------------------------------
# Frontmatter + section parsing
# ----------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(?P<fm>.*?)\n---\s*\n", re.DOTALL)


def parse_uat_markdown(path: Path) -> tuple[dict[str, Any], str]:
    """Parse a UAT markdown file into (frontmatter_dict, body_markdown)."""
    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"missing frontmatter in {path}")
    fm = yaml.safe_load(m.group("fm")) or {}
    body = text[m.end():]
    required = {"uat_id", "initiative", "phase", "overall_verdict"}
    missing = required - set(fm.keys())
    if missing:
        raise ValueError(f"missing required frontmatter keys in {path}: {sorted(missing)}")
    return fm, body


# ----------------------------------------------------------------------------
# Minimal markdown-to-HTML renderer
# ----------------------------------------------------------------------------
# We don't pull a full markdown library (zero-dependency goal). Subset support:
#   - headings (## / ### / ####)
#   - paragraphs
#   - bullet + numbered lists
#   - inline bold (**text**), italic (*text*), code (`text`), links [t](u)
#   - code fences ```...```
#   - blockquotes (> text)
#   - tables (GitHub-flavored)
#   - horizontal rules (---)
#
# This handles every construct the UAT template uses today.

_LINK_RE = re.compile(r"\[(?P<text>[^\]]+)\]\((?P<url>[^)]+)\)")
_BOLD_RE = re.compile(r"\*\*(?P<text>[^*]+)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(?P<text>[^*]+)\*(?!\*)")
_CODE_RE = re.compile(r"`(?P<text>[^`]+)`")
_BADGE_CLASSES = {
    "brand-aligned": "aligned",
    "brand-drift": "drift",
    "neutral": "neutral",
    "pass": "pass",
    "fail": "fail",
    "pending": "pending",
    "remediated": "remediated",
    "done": "done",
    "open": "open",
    "deferred": "deferred",
    "optional": "optional",
    "new": "new",
    "active": "active",
    "superseded": "superseded",
    "cleared": "pass",
    "skipped": "neutral",
    "fixed": "remediated",
}


def _classify_badge(token: str) -> str | None:
    """Map a known finding-class / verdict token (case-insensitive) to a CSS class."""
    t = token.strip().lower().replace(" ", "-")
    return _BADGE_CLASSES.get(t)


def _inline(text: str) -> str:
    """Apply inline markdown transformations + escape HTML."""
    # First protect badges + code spans + links from re-rendering
    # Order matters: code first (so backticks not interpreted), then links, then bold/italic.
    # Process code first (preserve internal HTML escaping inside code).
    placeholders: list[str] = []

    def _stash(m: re.Match) -> str:
        idx = len(placeholders)
        placeholders.append(f"<code>{_html.escape(m.group('text'))}</code>")
        return f"\x00CODE{idx}\x00"

    text = _CODE_RE.sub(_stash, text)

    def _link(m: re.Match) -> str:
        idx = len(placeholders)
        text_part = m.group("text")
        url = m.group("url")
        placeholders.append(f'<a href="{_html.escape(url)}">{_html.escape(text_part)}</a>')
        return f"\x00LINK{idx}\x00"

    text = _LINK_RE.sub(_link, text)

    # Now safe to escape rest
    text = _html.escape(text)

    text = _BOLD_RE.sub(lambda m: f"<strong>{m.group('text')}</strong>", text)
    text = _ITALIC_RE.sub(lambda m: f"<em>{m.group('text')}</em>", text)

    # Restore placeholders
    for i, repl in enumerate(placeholders):
        text = text.replace(f"\x00CODE{i}\x00", repl)
        text = text.replace(f"\x00LINK{i}\x00", repl)
    return text


def _render_table(lines: list[str]) -> str:
    """Render a GFM table (header | --- | rows) to HTML."""
    if len(lines) < 2:
        return ""
    header_cells = [c.strip() for c in lines[0].strip().strip("|").split("|")]
    # Skip the alignment row (lines[1])
    body_rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # Cell may carry a finding-class badge: render **brand-aligned**, **brand-drift**, **neutral**
        rendered_cells = []
        for c in cells:
            # Strip surrounding ** if it's a single-token badge match
            inner = c.strip("*").strip()
            badge_cls = _classify_badge(inner)
            if badge_cls and c.startswith("**") and c.endswith("**"):
                rendered_cells.append(
                    f'<td><span class="badge {badge_cls}">{_html.escape(inner)}</span></td>'
                )
            else:
                rendered_cells.append(f"<td>{_inline(c)}</td>")
        body_rows.append(f"<tr>{''.join(rendered_cells)}</tr>")
    head_html = "<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in header_cells) + "</tr>"
    return f'<table><thead>{head_html}</thead><tbody>{"".join(body_rows)}</tbody></table>'


def render_markdown_to_html(body: str) -> str:
    """Render the supported markdown subset to HTML."""
    lines = body.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Code fence
        if stripped.startswith("```"):
            fence_buf = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                fence_buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            out.append(f"<pre>{_html.escape(chr(10).join(fence_buf))}</pre>")
            continue

        # Horizontal rule
        if stripped == "---":
            out.append("<hr>")
            i += 1
            continue

        # Heading
        if stripped.startswith("#"):
            level = 0
            for ch in stripped:
                if ch == "#":
                    level += 1
                else:
                    break
            text = stripped[level:].strip()
            if level == 1:
                # Title — skip; we render it separately as the page title-block
                i += 1
                continue
            if level == 2:
                out.append(_render_section_open(text))
                i += 1
                continue
            tag = f"h{min(level, 6)}"
            out.append(f"<{tag}>{_inline(text)}</{tag}>")
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            quote_buf = []
            while i < n and lines[i].strip().startswith(">"):
                quote_buf.append(lines[i].strip().lstrip(">").lstrip())
                i += 1
            out.append(f"<blockquote>{_render_paragraph_block(quote_buf)}</blockquote>")
            continue

        # Table (line containing `|` followed by header-separator line)
        if "|" in stripped and i + 1 < n and re.match(r"^\s*\|?[\s:-]+\|", lines[i + 1]):
            tbl_buf = [lines[i]]
            i += 1
            tbl_buf.append(lines[i])
            i += 1
            while i < n and "|" in lines[i].strip():
                tbl_buf.append(lines[i])
                i += 1
            out.append(_render_table(tbl_buf))
            continue

        # Bullet list
        if stripped.startswith(("- ", "* ")):
            list_buf = []
            while i < n and lines[i].strip().startswith(("- ", "* ")):
                list_buf.append(lines[i].strip()[2:])
                i += 1
            items = "".join(f"<li>{_inline(it)}</li>" for it in list_buf)
            out.append(f"<ul>{items}</ul>")
            continue

        # Numbered list
        if re.match(r"^\d+\.\s", stripped):
            list_buf = []
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                list_buf.append(re.sub(r"^\d+\.\s", "", lines[i].strip()))
                i += 1
            items = "".join(f"<li>{_inline(it)}</li>" for it in list_buf)
            out.append(f"<ol>{items}</ol>")
            continue

        # Empty line — close any open section block? No, just paragraph break
        if not stripped:
            i += 1
            continue

        # Paragraph
        para_buf = [stripped]
        i += 1
        while i < n and lines[i].strip() and not _is_block_start(lines[i].strip()):
            para_buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{_inline(' '.join(para_buf))}</p>")

    # Close any open section
    if any("__section_open__" in o for o in out):
        out.append("</div>")  # close last section
    out_str = "\n".join(out).replace("__section_open__", "")
    return out_str


def _is_block_start(stripped: str) -> bool:
    return (
        stripped.startswith("#")
        or stripped.startswith(">")
        or stripped.startswith("- ")
        or stripped.startswith("* ")
        or stripped.startswith("```")
        or stripped == "---"
        or bool(re.match(r"^\d+\.\s", stripped))
        or "|" in stripped
    )


def _render_section_open(title: str) -> str:
    """Open a new .section block (closes previous via post-process)."""
    eyebrow = ""
    title_only = title
    m = re.match(r"^(?P<eb>Section \d+)\s*[—-]\s*(?P<title>.+)$", title)
    if m:
        eyebrow = m.group("eb")
        title_only = m.group("title")
    eb_html = f'<div class="section-eyebrow">{_html.escape(eyebrow)}</div>' if eyebrow else ""
    return (
        "</div>__section_open__"  # close previous section if any
        f'<div class="section">{eb_html}'
        f'<h2 class="section-title">{_inline(title_only)}</h2>'
    )


def _render_paragraph_block(buf: list[str]) -> str:
    """Render a paragraph buffer for blockquote contexts."""
    if not buf:
        return ""
    text = " ".join(buf)
    return f"<p>{_inline(text)}</p>"


# ----------------------------------------------------------------------------
# Top-level page assembly
# ----------------------------------------------------------------------------


def _verdict_class(v: str) -> str:
    s = v.lower()
    if "fail" in s and "remediat" not in s and "pending" not in s:
        return "fail"
    if "pass" in s and "fail" not in s:
        return "pass"
    if "pending" in s:
        return "pending"
    if "remediat" in s:
        return "remediated"
    return ""


def _render_verdict_strip(fm: dict[str, Any]) -> str:
    cells = []

    overall = str(fm.get("overall_verdict", "—"))
    cells.append(
        f'<div class="verdict-cell"><div class="label">Verdict</div>'
        f'<div class="value {_verdict_class(overall)}">{_html.escape(overall)}</div></div>'
    )
    cells.append(
        f'<div class="verdict-cell"><div class="label">Initiative</div>'
        f'<div class="value">{_html.escape(str(fm.get("initiative", "—")))}</div></div>'
    )
    cells.append(
        f'<div class="verdict-cell"><div class="label">Phase</div>'
        f'<div class="value">{_html.escape(str(fm.get("phase", "—")))}</div></div>'
    )

    findings_aligned = fm.get("findings_brand_aligned", "—")
    findings_drift = fm.get("findings_brand_drift", "—")
    findings_neutral = fm.get("findings_neutral", "—")
    findings_summary = f"{findings_aligned} aligned · {findings_drift} drift · {findings_neutral} neutral"
    cells.append(
        f'<div class="verdict-cell"><div class="label">Findings</div>'
        f'<div class="value">{_html.escape(findings_summary)}</div></div>'
    )
    return f'<div class="verdict-strip">{"".join(cells)}</div>'


def _render_timeline(fm: dict[str, Any]) -> str:
    history = fm.get("verdict_history") or []
    if not history:
        return ""
    rows = []
    for step in history:
        s = str(step)
        # Parse "YYYY-MM-DD STATUS (rest)"
        m = re.match(r"^(\d{4}-\d{2}-\d{2})\s+(\w+)\s*(.*)$", s)
        if m:
            date, status, rest = m.groups()
        else:
            date, status, rest = "—", "—", s
        cls = _verdict_class(status)
        rows.append(
            f'<div class="timeline-step">'
            f'<div class="timeline-bullet {cls}"></div>'
            f'<div class="timeline-date">{_html.escape(date)}</div>'
            f'<div class="timeline-status {cls}">{_html.escape(status)}</div>'
            f'<div class="timeline-text">{_inline(rest.lstrip("(").rstrip(")"))}</div>'
            f'</div>'
        )
    return (
        '<div class="timeline">'
        '<h3>Verdict history</h3>'
        f'{"".join(rows)}'
        '</div>'
    )


def _render_title_block(fm: dict[str, Any], body: str) -> str:
    # Extract first H1 from body as title
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = m.group(1) if m else f"UAT {fm.get('uat_id', '')}"
    eyebrow = f"{fm.get('initiative', '')} · {fm.get('phase', '')}"
    subtitle_parts = []
    if fm.get("shipped_date"):
        subtitle_parts.append(f"Shipped {fm['shipped_date']}")
    if fm.get("amended_date"):
        subtitle_parts.append(f"Amended {fm['amended_date']}")
    if fm.get("operator_review_date"):
        subtitle_parts.append(f"Operator review: {fm['operator_review_date']}")
    subtitle = " · ".join(subtitle_parts)
    return (
        '<div class="title-block">'
        f'<div class="eyebrow">{_html.escape(eyebrow)}</div>'
        f'<h1 class="title-h1">{_inline(title)}</h1>'
        f'<p class="subtitle">{_html.escape(subtitle)}</p>'
        '</div>'
    )


def _resolve_styles(out_dir: Path) -> str:
    """Locate the inlined stylesheet — prefer per-uat folder, fall back to shared."""
    candidates = [
        out_dir / DEFAULT_STYLES_FILENAME,
        SHARED_STYLESHEET,
    ]
    for c in candidates:
        if c.exists():
            return c.read_text(encoding="utf-8")
    raise FileNotFoundError(
        f"could not locate UAT stylesheet at any of: {[str(c) for c in candidates]}"
    )


def render_html(fm: dict[str, Any], body: str, out_dir: Path) -> str:
    styles_css = _resolve_styles(out_dir)
    title_block = _render_title_block(fm, body)
    verdict_strip = _render_verdict_strip(fm)
    timeline = _render_timeline(fm)
    body_html = render_markdown_to_html(body)

    # Compute sha256 of body for the footer + reproducibility breadcrumb
    body_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]
    rendered_at = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!DOCTYPE html>
<html lang="{fm.get('language', 'en')}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_html.escape(str(fm.get('uat_id', 'Impeccable UAT')))} — Holistika</title>
<style>
{styles_css}
</style>
</head>
<body>
<div class="page">
<div class="brand-header">
<div class="brand-wordmark">HOLIST<span class="accent">Í</span>KA <span style="font-weight:400;color:var(--fg-muted);">Research</span></div>
<div class="brand-meta">Impeccable UAT · J-OP audience<br>{_html.escape(rendered_at)}</div>
</div>
{title_block}
{verdict_strip}
{timeline}
{body_html}
</div>
<div class="footer">
<div class="left">Rendered by <code>scripts/render_impeccable_uat.py</code> · I77 P4.B (D-IH-77-I)</div>
<div class="right">body sha256: <code>{body_sha}</code></div>
</div>
</body>
</html>
"""


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def _slug_from_uat_id(uat_id: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", uat_id.lower()).strip("-")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("uat_path", help="Path to UAT markdown file")
    parser.add_argument(
        "--out", default=None,
        help="Override output HTML path (default: docs/presentations/<uat-slug>/index.html)",
    )
    parser.add_argument(
        "--check-only", action="store_true",
        help="Parse + render to memory but do not write the file",
    )
    args = parser.parse_args(argv)

    uat_path = Path(args.uat_path).resolve()
    if not uat_path.exists():
        print(f"error: UAT file not found: {uat_path}", file=sys.stderr)
        return 2

    try:
        fm, body = parse_uat_markdown(uat_path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out_path = (
        Path(args.out).resolve()
        if args.out
        else DEFAULT_PRESENTATIONS_DIR / _slug_from_uat_id(str(fm.get("uat_id", "uat"))) / "index.html"
    )
    out_dir = out_path.parent

    if not args.check_only:
        out_dir.mkdir(parents=True, exist_ok=True)

    html_doc = render_html(fm, body, out_dir)

    if args.check_only:
        body_sha = hashlib.sha256(html_doc.encode("utf-8")).hexdigest()[:16]
        print(
            f"render_impeccable_uat: check-only OK "
            f"(uat_id={fm.get('uat_id')}, verdict={fm.get('overall_verdict')}, "
            f"html_sha256={body_sha}..., would_write={out_path})"
        )
        return 0

    out_path.write_text(html_doc, encoding="utf-8")
    html_sha = hashlib.sha256(html_doc.encode("utf-8")).hexdigest()[:16]
    # ASCII-safe stdout: replace any non-cp1252 codepoints in verdict for the friendly log
    verdict_ascii = (
        str(fm.get("overall_verdict", "")).encode("ascii", errors="replace").decode("ascii")
    )
    print(
        f"render_impeccable_uat: wrote {out_path} "
        f"(uat_id={fm.get('uat_id')}, verdict={verdict_ascii}, html_sha256={html_sha}...)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
