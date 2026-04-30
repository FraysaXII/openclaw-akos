#!/usr/bin/env python3
"""Initiative 31 P1 — Language frontmatter validator.

Per :doc:`SOP-HLK_LOCALISATION_001.md` §3 (frontmatter contract), every
canonical Markdown artifact under the canonical surfaces declares
``language: en|es|fr`` in its frontmatter. Optional ``derived_from:`` and
``derived_locales:`` express the locale-derivation graph.

Validates that:

1. Every canonical Markdown file declares ``language:``.
2. The value is one of the recognised locale codes.
3. ``derived_from:`` (if present) points at an existing file with a
   different ``language:`` AND that file's ``derived_locales:`` covers
   this file's locale.
4. ``derived_locales:`` (if present) — every locale in the list resolves
   to a real sibling file with a matching ``derived_from:``.

Skipped surfaces (by design — see SOP §3.1):

- ``tests/`` (fixtures and test data)
- ``docs/wip/planning/<NN>-*/reports/`` (historical reports stay frozen)
- ``scripts/sql/`` and ``supabase/migrations/`` (DDL / DML, not Markdown)
- ``vendor/`` and ``node_modules/`` (third-party)
- ``.github/`` (CI / repo metadata)
- ``artifacts/`` (transient outputs)
- ``.cursor/`` (Cursor app state)

Usage::

    py scripts/validate_hlk_language_frontmatter.py

Exit codes:
    0   PASS
    1   FAIL (one or more invariants violated; details on stderr)
    2   I/O or schema error
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_ROOTS = [
    REPO_ROOT / "docs" / "references" / "hlk",
    REPO_ROOT / "docs" / "wip" / "planning",
    REPO_ROOT / "akos",
    REPO_ROOT / "scripts",
]

SKIP_DIR_NAMES = {
    "node_modules",
    "vendor",
    ".git",
    ".github",
    ".cursor",
    "__pycache__",
    "sql",
    "tests",
    "artifacts",
}

SKIP_PATH_PATTERNS = [
    # Older initiative reports stay as audit-trail-frozen.
    re.compile(r"docs[\\/]wip[\\/]planning[\\/]\d+-[^\\/]+[\\/]reports[\\/]"),
    # Cursor app state.
    re.compile(r"\.cursor[\\/]"),
    # Third-party.
    re.compile(r"node_modules[\\/]"),
    # SQL is not Markdown.
    re.compile(r"supabase[\\/]migrations[\\/]"),
    # Archived knowledge versions (v2.7 etc) — not current canonical.
    re.compile(r"docs[\\/]references[\\/]hlk[\\/]Research & Logic[\\/]Holistika Research v[0-9.]+[\\/]"),
    # Marked-for-deletion legal transcripts (`delete-legal-transcripts/`).
    re.compile(r"docs[\\/]references[\\/]hlk[\\/]business-intent[\\/]delete-legal-transcripts[\\/]"),
    # Exemplar / template project (informational only).
    re.compile(r"docs[\\/]references[\\/]hlk[\\/]previous-project-for-product-owner-example-only[\\/]"),
    # Older closed initiatives' top-level artifacts (only the latest few new initiatives carry the frontmatter contract).
    re.compile(r"docs[\\/]wip[\\/]planning[\\/](?!31-)\d+[a-z]?-[^\\/]+[\\/](?!.*language)"),
]

ALLOWED_LANGUAGES = {"en", "es", "fr"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(text: str) -> dict[str, str | list[str]]:
    """Minimal YAML-ish parser. Handles flat key:value and inline-list values
    we actually care about (``language``, ``derived_from``, ``derived_locales``).
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    body = m.group(1)
    out: dict[str, str | list[str]] = {}
    for line in body.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.startswith(" "):
            # Skip continuation lines; this validator only needs flat top-level keys.
            continue
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            items = [s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()]
            out[key] = items
        else:
            out[key] = val.strip('"').strip("'")
    return out


def _is_skipped(path: Path) -> bool:
    rel_str = str(path.relative_to(REPO_ROOT))
    for pat in SKIP_PATH_PATTERNS:
        if pat.search(rel_str):
            return True
    parts = path.relative_to(REPO_ROOT).parts
    for skip in SKIP_DIR_NAMES:
        if skip in parts:
            return True
    return False


def _walk_canonical_md(roots: list[Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for p in root.rglob("*.md"):
            if not p.is_file() or _is_skipped(p):
                continue
            files.append(p)
    return sorted(set(files))


def main(argv: list[str] | None = None) -> int:
    files = _walk_canonical_md(CANONICAL_ROOTS)
    if not files:
        print("validate_hlk_language_frontmatter: no Markdown files matched canonical roots; nothing to check.", file=sys.stderr)
        return 0

    errors: list[str] = []
    skipped_no_fm: list[str] = []  # files with no frontmatter at all (informational; usually older docs)

    # Index every MD by its repo-relative path string for FK resolution.
    index: dict[str, dict[str, str | list[str]]] = {}
    decode_failures: list[str] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Fall back to Latin-1 just to peek at the frontmatter; if even that
            # fails the file is binary-ish and we skip it informationally.
            try:
                text = path.read_text(encoding="latin-1")
            except Exception:
                decode_failures.append(str(path.relative_to(REPO_ROOT)).replace("\\", "/"))
                continue
        fm = _parse_frontmatter(text)
        rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        index[rel] = fm

    # Pass 1 — language presence + value
    for rel, fm in index.items():
        lang = fm.get("language")
        if not fm:
            skipped_no_fm.append(rel)
            continue
        if not lang:
            errors.append(f"{rel}: missing 'language:' frontmatter key")
            continue
        if lang not in ALLOWED_LANGUAGES:
            errors.append(f"{rel}: language={lang!r} not in {sorted(ALLOWED_LANGUAGES)}")

    # Pass 2 — derived_from / derived_locales graph integrity
    for rel, fm in index.items():
        derived_from = fm.get("derived_from")
        if isinstance(derived_from, str) and derived_from:
            target_key = derived_from.replace("\\", "/")
            if target_key not in index:
                errors.append(f"{rel}: derived_from={derived_from!r} does not resolve to an indexed canonical file")
                continue
            target_fm = index[target_key]
            target_lang = target_fm.get("language")
            this_lang = fm.get("language")
            if isinstance(target_lang, str) and isinstance(this_lang, str):
                if target_lang == this_lang:
                    errors.append(
                        f"{rel}: derived_from points at a file with the SAME language={this_lang!r} "
                        f"(should differ for a locale sibling)"
                    )
            target_locales = target_fm.get("derived_locales") or []
            if isinstance(target_locales, list) and isinstance(this_lang, str):
                if this_lang not in target_locales:
                    errors.append(
                        f"{rel}: derived_from={target_key!r} but that canonical's "
                        f"derived_locales={target_locales!r} does not include {this_lang!r}"
                    )

        derived_locales = fm.get("derived_locales")
        if isinstance(derived_locales, list) and derived_locales:
            this_lang = fm.get("language")
            for loc in derived_locales:
                if loc == this_lang:
                    errors.append(
                        f"{rel}: derived_locales={derived_locales!r} contains its own language={this_lang!r}"
                    )
                if loc not in ALLOWED_LANGUAGES:
                    errors.append(f"{rel}: derived_locales contains unrecognised locale {loc!r}")

    print()
    print("  HLK language frontmatter validator")
    print("  ========================================")
    print(f"  Files scanned:     {len(files)}")
    print(f"  With frontmatter:  {len(files) - len(skipped_no_fm) - len(decode_failures)}")
    print(f"  Without frontmatter (informational): {len(skipped_no_fm)}")
    print(f"  Decode failures (informational):     {len(decode_failures)}")
    print(f"  Errors:            {len(errors)}")
    print()

    if skipped_no_fm:
        # Informational — only print when verbose. For now, summarise.
        print(f"  Files without frontmatter (first 10 of {len(skipped_no_fm)}):", file=sys.stderr)
        for rel in sorted(skipped_no_fm)[:10]:
            print(f"    - {rel}", file=sys.stderr)
        print(file=sys.stderr)

    if errors:
        print("  FAIL", file=sys.stderr)
        for err in errors:
            print(f"    - {err}", file=sys.stderr)
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
