#!/usr/bin/env python3
"""Render an HLK KM Mermaid source (`*.mmd`) to deterministic PNG + SVG sidecars.

Initiative 22 P5 deliverable. Reads the Mermaid source from a path under
`docs/references/hlk/v3.0/_assets/<plane>/<program_id>/<topic_id>/<topic_id>.mmd`
and writes `<topic_id>.png` and `<topic_id>.svg` next to it. Idempotent: re-running
with the same input produces output bytes that satisfy the manifest's
`file_sha256` after a single matching run.

Strategy:

1. **Preferred** — invoke `mmdc` (Mermaid CLI from `@mermaid-js/mermaid-cli`)
   when available on PATH. This is the deterministic, offline path.
2. **Fallback** — call the public `mermaid.ink` HTTP API (URL-base64-encoded
   source), which is deterministic for a given source string. The fallback is
   usable in CI where Node/`mmdc` may not be installed.

After rendering, optionally update the **`file_sha256`** field of the sibling
manifest file to match the new PNG hash (use `--update-manifest`).

Usage:

  py scripts/render_km_diagrams.py <path-to-.mmd>
  py scripts/render_km_diagrams.py <path-to-.mmd> --update-manifest

The path may be relative to the repository root.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MERMAID_INK_BASE = "https://mermaid.ink"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_bytes(path: Path, data: bytes) -> None:
    path.write_bytes(data)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _mmdc_available() -> str | None:
    return shutil.which("mmdc")


def _render_with_mmdc(mmdc: str, src: Path, out_png: Path, out_svg: Path) -> None:
    print(f"render_km_diagrams: using mmdc -> {mmdc}")
    for out, fmt_arg in ((out_png, "png"), (out_svg, "svg")):
        cmd = [mmdc, "-i", str(src), "-o", str(out), "-b", "transparent"]
        print("  $", " ".join(cmd))
        rc = subprocess.call(cmd)
        if rc != 0:
            raise SystemExit(f"mmdc returned {rc} for {fmt_arg}")


def _mermaid_ink_url(src_text: str, fmt: str) -> str:
    raw = src_text.encode("utf-8")
    b64 = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    if fmt == "png":
        return f"{MERMAID_INK_BASE}/img/{b64}?type=png&bgColor=transparent"
    if fmt == "svg":
        return f"{MERMAID_INK_BASE}/svg/{b64}"
    raise ValueError(fmt)


def _http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-akos render_km_diagrams/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            raise SystemExit(f"mermaid.ink returned status={resp.status} for {url}")
        return resp.read()


def _render_with_mermaid_ink(src_text: str, out_png: Path, out_svg: Path) -> None:
    print("render_km_diagrams: mmdc not on PATH; falling back to mermaid.ink")
    png_url = _mermaid_ink_url(src_text, "png")
    svg_url = _mermaid_ink_url(src_text, "svg")
    print(f"  GET {png_url[:80]}...")
    _write_bytes(out_png, _http_get(png_url))
    print(f"  GET {svg_url[:80]}...")
    _write_bytes(out_svg, _http_get(svg_url))


def _update_manifest_sha(manifest_path: Path, new_sha: str) -> bool:
    """Replace `file_sha256: "..."` in the manifest frontmatter. Idempotent."""
    text = manifest_path.read_text(encoding="utf-8")
    pat = re.compile(r'^(file_sha256:\s*")([0-9a-fA-F]{64})(")\s*$', re.MULTILINE)
    m = pat.search(text)
    if not m:
        print(f"  manifest: no file_sha256 line found in {manifest_path}; skipping update")
        return False
    if m.group(2).lower() == new_sha.lower():
        print(f"  manifest: file_sha256 already {new_sha[:16]}...; nothing to do")
        return True
    new_text = pat.sub(rf'\g<1>{new_sha}\g<3>', text, count=1)
    manifest_path.write_text(new_text, encoding="utf-8")
    print(f"  manifest: updated file_sha256 -> {new_sha[:16]}...")
    return True


def _render_one(
    src: Path,
    *,
    update_manifest: bool,
    prefer_mermaid_ink: bool,
    dry_run: bool,
) -> int:
    if not src.is_file():
        print(f"error: not a file: {src}", file=sys.stderr)
        return 2
    if src.suffix != ".mmd":
        print(f"error: expected .mmd extension, got {src.suffix}", file=sys.stderr)
        return 2

    out_png = src.with_suffix(".png")
    out_svg = src.with_suffix(".svg")
    src_text = _read_text(src)

    if dry_run:
        rel = src.relative_to(REPO_ROOT) if src.is_relative_to(REPO_ROOT) else src
        print(f"  [dry-run] would render {rel} -> .png + .svg ({len(src_text)} chars source)")
        return 0

    mmdc = None if prefer_mermaid_ink else _mmdc_available()
    if mmdc:
        _render_with_mmdc(mmdc, src, out_png, out_svg)
    else:
        _render_with_mermaid_ink(src_text, out_png, out_svg)

    png_sha = _sha256(out_png.read_bytes())
    svg_sha = _sha256(out_svg.read_bytes())
    print(f"  wrote {out_png.relative_to(REPO_ROOT)} ({out_png.stat().st_size} bytes, sha256={png_sha[:16]}...)")
    print(f"  wrote {out_svg.relative_to(REPO_ROOT)} ({out_svg.stat().st_size} bytes, sha256={svg_sha[:16]}...)")

    if update_manifest:
        manifest_path = src.with_name(src.stem + ".manifest.md")
        if not manifest_path.is_file():
            print(f"  manifest: not found at {manifest_path}; skipping --update-manifest")
        else:
            _update_manifest_sha(manifest_path, png_sha)
    return 0


def _discover_mmd_sources(root: Path) -> list[Path]:
    """Initiative 25 P8: find every .mmd under `_assets/` and `_meta/` for batch render.

    Excludes `.git/` and any `.mmd` outside the canonical `_assets/` tree.
    """
    out: list[Path] = []
    if not root.is_dir():
        return out
    for path in sorted(root.rglob("*.mmd")):
        if any(part == ".git" for part in path.parts):
            continue
        out.append(path)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "source",
        type=Path,
        nargs="?",
        default=None,
        help="Path to a Mermaid (.mmd) source file (omit when using --all)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Render every .mmd under docs/references/hlk/v3.0/_assets/ (Initiative 25 P8)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover sources but don't render or write — prints what would happen",
    )
    parser.add_argument(
        "--update-manifest",
        action="store_true",
        help="Update the sibling .manifest.md file_sha256 to match the new PNG hash",
    )
    parser.add_argument(
        "--prefer-mermaid-ink",
        action="store_true",
        help="Skip mmdc detection and use the mermaid.ink HTTP fallback directly",
    )
    args = parser.parse_args(argv)

    if args.all and args.source is not None:
        print("error: --all cannot be combined with a specific source path", file=sys.stderr)
        return 2
    if not args.all and args.source is None:
        print("error: provide a .mmd path or pass --all", file=sys.stderr)
        return 2

    if args.all:
        assets_root = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets"
        sources = _discover_mmd_sources(assets_root)
        if not sources:
            print("render_km_diagrams: no .mmd sources found under _assets/")
            return 0
        print(f"render_km_diagrams: --all discovered {len(sources)} source(s)")
        rc_any = 0
        for src in sources:
            print(f"\n--- {src.relative_to(REPO_ROOT)} ---")
            rc = _render_one(
                src.resolve(),
                update_manifest=args.update_manifest,
                prefer_mermaid_ink=args.prefer_mermaid_ink,
                dry_run=args.dry_run,
            )
            if rc != 0:
                rc_any = rc
        return rc_any

    return _render_one(
        args.source.resolve(),
        update_manifest=args.update_manifest,
        prefer_mermaid_ink=args.prefer_mermaid_ink,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
