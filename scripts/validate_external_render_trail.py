"""Validate external-render trail per audience-class matrix (D-IH-86-P).

Per `akos-external-render-discipline.mdc` RULE 4 + RULE 6.

For every markdown surface under the rule's globs that carries an external
audience tag (J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO), this
validator looks for a paired render artifact via these heuristics, in order:

1. PDF heuristic — `artifacts/exports/<derived-stem>.pdf` OR `paths.pdf` slot
   in a sibling `*.manifest.md`.
2. Web heuristic — sibling `web-link.md` with non-empty `url:` on a registered
   domain OR `paths.web` slot.
3. ERP heuristic — sibling `erp-record.md` with non-empty UUID `record_id:` OR
   `paths.erp_record_id` slot.
4. Mail heuristic — for `cover_email_*.md`, look for paired `cover_email_*.html`
   OR sibling `mail-render.md`.
5. Slide heuristic — for `deck_*.md` / `deck_*.yaml`, look for sibling
   `figma-link.md` with non-empty Figma URL OR paired PDF in `artifacts/exports/`.
6. Broadcast heuristic — sibling `broadcast-link.md` OR `paths.broadcast` slot.

Surfaces tagged J-OP only are exempt.
Manifest-shaped surfaces (`*.manifest.md`, `topic_*.md` Output-1 manifests)
are exempt.
Engagement-template skeletons are exempt.

Exit code: 0 PASS or INFO (advisory); 1 FAIL when promoted.
The validator runs at INFO until the render-pending tracker reaches zero
entries (per RULE 6 backfill posture); promotes to FAIL at that closure.
"""
from __future__ import annotations

import csv
import logging
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos import log  # noqa: E402

log.setup_logging()
logger = logging.getLogger(__name__)

REGISTRY_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "dimensions"
    / "AUDIENCE_REGISTRY.csv"
)

PENDING_TRACKER_PATH = (
    REPO_ROOT
    / "docs" / "wip" / "planning" / "_trackers"
    / "external-render-pending-tracker.md"
)

EXPORTS_DIR = REPO_ROOT / "artifacts" / "exports"

SCAN_GLOBS: tuple[str, ...] = (
    "docs/references/hlk/v3.0/_assets/advops/**/*.md",
    "docs/references/hlk/v3.0/_assets/touchpoint-kit/**/*.md",
    "docs/references/hlk/v3.0/_assets/touchpoint_kits/**/*.md",
    "docs/references/hlk/v3.0/Think Big/Advisers/**/*.md",
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/**/*.md",
)

SKIP_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r"\.objections\.md$"),
    re.compile(r"\.counterparty-brief\.md$"),
    re.compile(r"\.manifest\.md$"),
    re.compile(r"^_template"),
    re.compile(r"/templates?/"),
    re.compile(r"/_engagement-template/"),
    re.compile(r"/_candidates/"),
    re.compile(r"/topic_[^/]*\.md$"),
    re.compile(r"/README\.md$", re.IGNORECASE),
)

EXTERNAL_AUDIENCE_CODES: frozenset[str] = frozenset({
    "J-IN", "J-CU", "J-PT", "J-AD", "J-ENISA", "J-RC", "J-CO",
})

REGISTERED_WEB_DOMAINS: tuple[str, ...] = (
    "holistikaresearch.com",
    "kirbe.com",
    "kirbe.app",
    "hlk-erp.app",
    "figma.com",
)

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
AUDIENCE_FIELD_PATTERN = re.compile(r"^audience\s*:\s*(.+?)$", re.MULTILINE)
AUDIENCE_LIST_INLINE = re.compile(r"^\s*\[(.+?)\]\s*$")
AUDIENCE_CODE_PATTERN = re.compile(r"J-[A-Z]{2,8}")
ARTIFACT_KIND_PATTERN = re.compile(r"^artifact_kind\s*:\s*(.+?)$", re.MULTILINE)
URL_PATTERN = re.compile(r"https?://[^\s<>\"'`]+", re.IGNORECASE)
UUID_PATTERN = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)
TEMPLATE_ARTIFACT_KINDS: frozenset[str] = frozenset({
    "deck_template", "dossier_template", "email_template",
    "handoff_template", "proposal_template", "template", "skeleton",
})


def _load_valid_audience_codes() -> set[str]:
    codes: set[str] = set()
    if not REGISTRY_PATH.exists():
        return codes
    with REGISTRY_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            code = (row.get("audience_code") or "").strip()
            if code:
                codes.add(code)
    return codes


def _should_skip(path: Path) -> bool:
    rel = path.as_posix()
    return any(pattern.search(rel) for pattern in SKIP_PATTERNS)


def _extract_audience(text: str) -> list[str] | None:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return None
    frontmatter = match.group(1)
    audience_match = AUDIENCE_FIELD_PATTERN.search(frontmatter)
    if not audience_match:
        return None
    raw_value = audience_match.group(1).strip()
    list_match = AUDIENCE_LIST_INLINE.match(raw_value)
    if list_match:
        codes = [c.strip() for c in list_match.group(1).split(",")]
        return [c for c in codes if c]
    if raw_value.startswith("J-"):
        return [raw_value.split()[0]]
    return AUDIENCE_CODE_PATTERN.findall(raw_value) or None


def _is_template_surface(text: str) -> bool:
    """Return True if frontmatter declares artifact_kind: <something>_template."""
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return False
    frontmatter = match.group(1)
    kind_match = ARTIFACT_KIND_PATTERN.search(frontmatter)
    if not kind_match:
        return False
    kind = kind_match.group(1).strip().strip('"').strip("'").lower()
    if kind in TEMPLATE_ARTIFACT_KINDS:
        return True
    return kind.endswith("_template") or kind.endswith("-template")


def _has_registered_url(text: str) -> bool:
    for url in URL_PATTERN.findall(text):
        for domain in REGISTERED_WEB_DOMAINS:
            if domain in url.lower():
                return True
    return False


def _has_uuid(text: str) -> bool:
    return bool(UUID_PATTERN.search(text))


def _load_manifest_source_paths() -> set[str]:
    """Reverse-lookup: collect every source path referenced by a manifest."""
    sources: set[str] = set()
    if not EXPORTS_DIR.exists():
        return sources
    import json
    for manifest in EXPORTS_DIR.rglob("*.manifest.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            continue
        for key in ("source_path", "source_md", "source_md_path",
                    "source_md_relpath", "source_html", "source_html_path"):
            value = data.get(key)
            if isinstance(value, str) and value:
                normalised = value.replace("\\", "/")
                if normalised.startswith(str(REPO_ROOT).replace("\\", "/")):
                    normalised = normalised[len(str(REPO_ROOT).replace("\\", "/")) + 1:]
                sources.add(normalised)
    return sources


_MANIFEST_SOURCES_CACHE: set[str] | None = None


def _manifest_sources() -> set[str]:
    global _MANIFEST_SOURCES_CACHE
    if _MANIFEST_SOURCES_CACHE is None:
        _MANIFEST_SOURCES_CACHE = _load_manifest_source_paths()
    return _MANIFEST_SOURCES_CACHE


def _check_pdf_heuristic(path: Path) -> bool:
    """Look for paired PDF in artifacts/exports/ keyed on stem-aware patterns
    with manifest reverse-lookup as the strongest signal."""
    if not EXPORTS_DIR.exists():
        return False

    rel_path = path.relative_to(REPO_ROOT).as_posix()
    if rel_path in _manifest_sources():
        return True

    stem = path.stem.lower()
    name = path.name.lower()
    candidates: list[str] = []

    if stem.startswith("dossier_") or stem.startswith("dossier-"):
        candidates.extend(["dossier-*.pdf", "dossier_*.pdf"])
    if stem.startswith("cover_email") or stem.startswith("cover-email") or "email-cover" in stem:
        candidates.extend(["email-cover-*.pdf", "cover_email-*.pdf", "email-*.pdf"])
    if stem.startswith("deck_") or "deck-" in stem or stem.startswith("deck-"):
        candidates.extend(["holistika-company-dossier-*.pdf", "*deck*.pdf"])
    if "handoff" in stem:
        candidates.extend(["adviser-handoff-*.pdf", "*-handoff-*.pdf", "handoff-*.pdf"])
    if "appendix" in stem:
        candidates.extend(["appendix-*.pdf", "*-appendix-*.pdf"])
    if "proposal" in name:
        candidates.append("proposal*.pdf")

    candidates.append(f"{path.stem}.pdf")
    candidates.append(f"{path.parent.name}-{path.stem}.pdf")

    for pattern in candidates:
        if "*" in pattern:
            for match in EXPORTS_DIR.rglob(pattern):
                if match.is_file():
                    return True
        else:
            if (EXPORTS_DIR / pattern).is_file():
                return True
    return False


def _check_sibling(path: Path, sibling_name: str) -> Path | None:
    sibling = path.parent / sibling_name
    return sibling if sibling.is_file() else None


def _check_web_heuristic(path: Path) -> bool:
    sibling = _check_sibling(path, "web-link.md")
    if sibling:
        try:
            text = sibling.read_text(encoding="utf-8")
            return _has_registered_url(text)
        except (OSError, UnicodeDecodeError):
            return False
    return False


def _check_erp_heuristic(path: Path) -> bool:
    sibling = _check_sibling(path, "erp-record.md")
    if sibling:
        try:
            text = sibling.read_text(encoding="utf-8")
            return _has_uuid(text)
        except (OSError, UnicodeDecodeError):
            return False
    return False


def _check_mail_heuristic(path: Path) -> bool:
    if not path.stem.startswith("cover_email"):
        return False
    html_pair = path.with_suffix(".html")
    if html_pair.is_file():
        return True
    return _check_sibling(path, "mail-render.md") is not None


def _check_slide_heuristic(path: Path) -> bool:
    name = path.name.lower()
    is_deck = name.startswith("deck_") or "deck-" in name or "deck-visual-system" in name
    if not is_deck:
        return False
    if _check_sibling(path, "figma-link.md") is not None:
        return True
    if EXPORTS_DIR.exists():
        for pdf in EXPORTS_DIR.glob("*deck*.pdf"):
            if pdf.is_file():
                return True
    return False


def _check_broadcast_heuristic(path: Path) -> bool:
    sibling = _check_sibling(path, "broadcast-link.md")
    if sibling:
        try:
            text = sibling.read_text(encoding="utf-8")
            return _has_registered_url(text)
        except (OSError, UnicodeDecodeError):
            return False
    return False


def _has_render_trail(path: Path) -> tuple[bool, list[str]]:
    """Return (has_trail, list_of_satisfied_heuristics)."""
    satisfied: list[str] = []
    if _check_pdf_heuristic(path):
        satisfied.append("pdf")
    if _check_web_heuristic(path):
        satisfied.append("web")
    if _check_erp_heuristic(path):
        satisfied.append("erp")
    if _check_mail_heuristic(path):
        satisfied.append("mail")
    if _check_slide_heuristic(path):
        satisfied.append("slide")
    if _check_broadcast_heuristic(path):
        satisfied.append("broadcast")
    return (len(satisfied) > 0, satisfied)


def _is_pending_in_tracker(rel_path: str) -> bool:
    if not PENDING_TRACKER_PATH.exists():
        return False
    try:
        text = PENDING_TRACKER_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return rel_path in text


def _iter_target_files() -> list[Path]:
    files: list[Path] = []
    for glob_pattern in SCAN_GLOBS:
        for path in REPO_ROOT.glob(glob_pattern):
            if path.is_file() and path.suffix == ".md" and not _should_skip(path):
                files.append(path)
    seen: set[Path] = set()
    deduped: list[Path] = []
    for path in files:
        if path not in seen:
            deduped.append(path)
            seen.add(path)
    return deduped


def validate(strict: bool = False) -> int:
    valid_codes = _load_valid_audience_codes()
    if not valid_codes:
        logger.error("FAIL: AUDIENCE_REGISTRY.csv unreadable or empty")
        return 1

    files_scanned = 0
    files_external = 0
    files_with_trail = 0
    files_pending = 0
    missing_trail: list[tuple[str, list[str]]] = []

    for path in _iter_target_files():
        files_scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        audience = _extract_audience(text)
        if audience is None:
            continue

        external = [c for c in audience if c in EXTERNAL_AUDIENCE_CODES]
        if not external:
            continue

        if _is_template_surface(text):
            logger.debug("template-surface exempt: %s", path.relative_to(REPO_ROOT))
            continue

        files_external += 1
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        has_trail, satisfied = _has_render_trail(path)

        if has_trail:
            files_with_trail += 1
            logger.debug("trail OK: %s -> %s", rel_path, satisfied)
        elif _is_pending_in_tracker(rel_path):
            files_pending += 1
            logger.info("render-pending (tracked): %s -> %s", rel_path, external)
        else:
            missing_trail.append((rel_path, external))

    is_strict = strict or os.environ.get("AKOS_RENDER_TRAIL_STRICT") == "1"
    is_fail = is_strict and missing_trail

    if missing_trail:
        for rel_path, audiences in missing_trail:
            level = logger.error if is_strict else logger.info
            level(
                "render-trail missing: %s tagged %s — needs PDF/Web/ERP/Mail/Slide/Broadcast paired artifact, OR entry in external-render-pending-tracker.md",
                rel_path,
                audiences,
            )

    summary_level = logger.error if is_fail else logger.info
    summary_level(
        "%s: validate_external_render_trail — scanned %d ; external-tagged %d ; with trail %d ; pending tracker %d ; missing trail %d (strict=%s)",
        "FAIL" if is_fail else "PASS",
        files_scanned,
        files_external,
        files_with_trail,
        files_pending,
        len(missing_trail),
        is_strict,
    )
    return 1 if is_fail else 0


def main() -> int:
    strict = "--strict" in sys.argv or "-S" in sys.argv
    return validate(strict=strict)


if __name__ == "__main__":
    sys.exit(main())
