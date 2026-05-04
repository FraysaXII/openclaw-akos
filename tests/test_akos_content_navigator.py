"""Locks the AKOS Content Navigator guide contract.

The guide at ``docs/guides/akos_content_navigator.md`` is the operator-facing
index for "where do I see prompts / answers / test content / status". This
test asserts:

1. The guide exists.
2. Required H2 anchors are present (so the operator paths cheatsheet, three
   lights explainer, dossier console panel guide, etc. don't silently get
   removed).
3. Every link cited in the "Where do I look for X?" table resolves to a real
   path in the repo (a moved file would silently break operator workflow).
4. ``docs/README.md`` includes a markdown link to the navigator (so it is
   discoverable from the docs index).
5. ``docs/USER_GUIDE.md`` § 1 includes a "see also" pointer to the navigator.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAVIGATOR = ROOT / "docs" / "guides" / "akos_content_navigator.md"
DOCS_README = ROOT / "docs" / "README.md"
USER_GUIDE = ROOT / "docs" / "USER_GUIDE.md"


def test_navigator_exists() -> None:
    assert NAVIGATOR.is_file(), f"missing {NAVIGATOR.relative_to(ROOT)}"


def test_navigator_required_h2_anchors() -> None:
    """Pin the public structure operators rely on."""
    body = NAVIGATOR.read_text(encoding="utf-8")
    required = [
        "## 30-second health check",
        "## Where do I look for X?",
        "## The dossier console",
        "## Three-lights",
        "## Operator paths cheatsheet",
        "## When in doubt",
    ]
    for anchor in required:
        assert anchor in body, f"missing required anchor in navigator: {anchor!r}"


def test_navigator_cited_paths_resolve() -> None:
    """Every relative markdown link should point at an existing file or dir.

    External links (``http://`` / ``https://``) and anchor-only links
    (``#…``) are skipped; bash/PowerShell command snippets inside fenced
    blocks reference future-state output paths (``artifacts/uat-dossier/…``)
    so we explicitly skip ``artifacts/uat-dossier/uat-dossier-<UTC>/`` etc.
    """
    body = NAVIGATOR.read_text(encoding="utf-8")
    skipped_prefixes = ("http://", "https://", "#")
    skipped_substrings = (
        "uat-dossier-<UTC>",
        "<NN-initiative>",
        "<…>",
    )
    bad: list[str] = []
    base = NAVIGATOR.parent
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for raw in pattern.findall(body):
        link = raw.split("#", 1)[0]
        if not link:
            continue
        if link.startswith(skipped_prefixes):
            continue
        if any(sub in link for sub in skipped_substrings):
            continue
        target = (base / link).resolve()
        if not target.exists():
            bad.append(f"{link} -> {target}")
    assert not bad, "broken navigator links:\n  " + "\n  ".join(bad)


def test_docs_readme_links_navigator() -> None:
    body = DOCS_README.read_text(encoding="utf-8")
    assert "guides/akos_content_navigator" in body, (
        "docs/README.md must link to guides/akos_content_navigator.md"
    )


def test_user_guide_section_one_points_to_navigator() -> None:
    body = USER_GUIDE.read_text(encoding="utf-8")
    assert "akos_content_navigator" in body, (
        "docs/USER_GUIDE.md must include a see-also pointer to guides/akos_content_navigator.md"
    )
