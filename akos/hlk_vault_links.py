"""HLK v3.0 vault markdown link extraction and validation (no Neo4j)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator
from urllib.parse import unquote

from akos.io import REPO_ROOT

VAULT_REL = Path("docs") / "references" / "hlk" / "v3.0"

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def iter_vault_markdown_files(vault_root: Path | None = None) -> Iterator[Path]:
    root = vault_root or (REPO_ROOT / VAULT_REL)
    if not root.is_dir():
        return
    for p in sorted(root.rglob("*.md")):
        if "imports" in p.parts:
            continue
        if p.is_file():
            yield p


def resolve_markdown_target(source_file: Path, target: str, repo_root: Path) -> Path | None:
    """Return resolved file path if target is a same-repo markdown link, else None."""
    raw = unquote(target.split("#", 1)[0].strip())
    if not raw or raw.startswith(("#", "http://", "https://", "mailto:")):
        return None
    resolved = (source_file.parent / raw).resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError:
        return None
    if resolved.suffix.lower() != ".md" or not resolved.is_file():
        return None
    return resolved


def iter_internal_md_edges(repo_root: Path | None = None) -> list[tuple[str, str]]:
    """Return (from_rel, to_rel) posix paths under *repo_root* for existing .md links."""
    root = repo_root or REPO_ROOT
    vault = root / VAULT_REL
    pairs: list[tuple[str, str]] = []
    for md in iter_vault_markdown_files(vault):
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            resolved = resolve_markdown_target(md, target, root)
            if resolved is None:
                continue
            if not resolved.is_file():
                continue
            try:
                tgt_rel = resolved.relative_to(root).as_posix()
                src_rel = md.relative_to(root).as_posix()
            except ValueError:
                continue
            if not tgt_rel.startswith("docs/references/hlk/"):
                continue
            pairs.append((src_rel, tgt_rel))
    return pairs


def validate_vault_internal_links(repo_root: Path | None = None) -> list[str]:
    """Return human-readable errors for broken internal markdown links under v3.0."""
    root = repo_root or REPO_ROOT
    vault = root / VAULT_REL
    errors: list[str] = []
    for md in iter_vault_markdown_files(vault):
        text = md.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in LINK_RE.finditer(line):
                target = m.group(1).strip()
                resolved = resolve_markdown_target(md, target, root)
                if resolved is None:
                    continue
                if not resolved.exists():
                    rel = md.relative_to(root).as_posix()
                    errors.append(f"{rel}:{lineno}: broken link target '{target}'")
    return errors


def all_vault_md_paths(repo_root: Path | None = None) -> set[str]:
    """All ``.md`` paths under the v3 vault (posix, relative to repo root)."""
    root = repo_root or REPO_ROOT
    vault = root / VAULT_REL
    out: set[str] = set()
    for md in iter_vault_markdown_files(vault):
        out.add(md.relative_to(root).as_posix())
    return out
