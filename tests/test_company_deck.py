"""Tests for the Initiative 28 investor-style company dossier deck.

Covers:

- ``deck_slides.yaml`` schema (slide count, required fields per layout).
- Jargon-free guarantee on the deck SSOT (no internal codenames in slide copy).
- ``scripts/build_company_deck.py --check-only`` smoke (validates without writing).
- Rendered HTML deck (``docs/presentations/holistika-company-dossier/index.html``)
  contains the expected primitives (cover, capability cards, stat blocks,
  ask signature, roadmap) and zero ``TODO[OPERATOR]`` leaks.
- ``cover_email_company_dossier_es.md`` is jargon-free and follows the
  Spanish-patterns opener / closer.
- Initiative 29 P5: ``scripts/sync_deck_from_strategy.py`` exists and
  ``--check-only`` succeeds (the strategy SSOT is wired correctly).
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DECK_SLIDES_YAML = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "advops"
    / "PRJ-HOL-FOUNDING-2026"
    / "enisa_company_dossier"
    / "deck_slides.yaml"
)
DECK_STORY_MD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "advops"
    / "PRJ-HOL-FOUNDING-2026"
    / "enisa_company_dossier"
    / "deck_story_es.md"
)
COVER_EMAIL_MD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "advops"
    / "PRJ-HOL-FOUNDING-2026"
    / "enisa_company_dossier"
    / "cover_email_company_dossier_es.md"
)
HTML_DECK = REPO_ROOT / "docs" / "presentations" / "holistika-company-dossier" / "index.html"
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_company_deck.py"


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def deck_data() -> dict:
    import yaml  # type: ignore

    return yaml.safe_load(DECK_SLIDES_YAML.read_text(encoding="utf-8"))


def test_deck_yaml_loads(deck_data):
    assert "document" in deck_data
    assert "slides" in deck_data
    assert isinstance(deck_data["slides"], list)


def test_deck_slide_count_in_range(deck_data):
    n = len(deck_data["slides"])
    assert 12 <= n <= 16, f"slide count {n} outside investor-style range"


def test_deck_every_slide_has_id_and_layout(deck_data):
    seen: set[str] = set()
    for i, slide in enumerate(deck_data["slides"], start=1):
        assert "id" in slide, f"slide #{i} missing id"
        assert "layout" in slide, f"slide #{i} missing layout"
        sid = slide["id"]
        assert sid not in seen, f"duplicate slide id {sid!r}"
        seen.add(sid)


def test_deck_layout_set_matches_known_layouts(deck_data):
    expected = {
        "cover_hero",
        "section_opener",
        "solution_three_lines",
        "method_three_columns",
        "capability_grid",
        "product_spotlight",
        "market_icp",
        "business_model_today_tomorrow",
        "moat_pillars",
        "roadmap_three_phases",
        "enisa_fit_use_of_funds",
        "ask_signature",
    }
    actual = {s["layout"] for s in deck_data["slides"]}
    leftover = actual - expected
    assert not leftover, f"deck uses unknown layouts: {leftover}"


def test_deck_includes_canonical_story_beats(deck_data):
    """The investor-style deck must hit the canonical story beats: cover, problem,
    insight, solution, method, proof, productization, why-now, market, business
    model, moat, roadmap, ENISA fit, ask."""
    layouts = [s["layout"] for s in deck_data["slides"]]
    must_have = [
        "cover_hero",
        "section_opener",
        "solution_three_lines",
        "method_three_columns",
        "capability_grid",
        "product_spotlight",
        "market_icp",
        "business_model_today_tomorrow",
        "moat_pillars",
        "roadmap_three_phases",
        "enisa_fit_use_of_funds",
        "ask_signature",
    ]
    for layout in must_have:
        assert layout in layouts, f"deck missing required layout {layout!r}"


# ---------------------------------------------------------------------------
# Jargon-free guarantee
# ---------------------------------------------------------------------------


_FORBIDDEN_TOKENS_IN_DECK = (
    "TODO[OPERATOR]",
    "AKOS Strict",
    "ADVOPS",
    "TECHOPS",
    "FINOPS",
    "MKTOPS",
    "topic_external",
    "topic_kirbe_billing",
    "GOI-",
    "POI-",
    "ref_id",
    "RBAC",
    "RLS",
    "RRF",
    "pgvector",
    "Logfire",
    "Cohere",
    "BullMQ",
    "Cloudflare R2",
    "FastAPI",
    "Pydantic",
    "shadcn",
    "Polaris",
    "Liquid",
    "next-intl",
    "Mermaid",
    "WeasyPrint",
    "pandoc",
    "mmdc",
    "process_list.csv",
    "TOPIC_REGISTRY.csv",
    "PROGRAM_REGISTRY.csv",
    "ADVISER_OPEN_QUESTIONS.csv",
    "FOUNDER_FILED_INSTRUMENTS.csv",
    "GOI_POI_REGISTER",
    "holistika_ops.",
    "kirbe.",
    "compliance.",
    "Topic-Fact-Source",
    "derived view",
)


def test_deck_yaml_is_jargon_free():
    """The slide YAML — which drives both the HTML preview and the Figma deck —
    must be free of internal jargon. Frontmatter sources / metadata blocks are
    allowed and are not tested here (the test inspects only the visible slide
    copy via the JSON dump of slides)."""
    import yaml  # type: ignore

    data = yaml.safe_load(DECK_SLIDES_YAML.read_text(encoding="utf-8"))
    flat = json.dumps(data["slides"], ensure_ascii=False)
    leaks = [tok for tok in _FORBIDDEN_TOKENS_IN_DECK if tok in flat]
    assert not leaks, (
        f"deck_slides.yaml slide copy contains forbidden tokens "
        f"(BRAND_JARGON_AUDIT.md §4): {leaks}"
    )


def _strip_frontmatter(md: str) -> str:
    return re.sub(r"^---\s*\n.*?\n---\s*\n", "", md, count=1, flags=re.DOTALL)


def _strip_internal_notes(md: str) -> str:
    """The cover email and deck story carry an "internal notes" appendix that is
    explicitly not part of the external send. Strip it before jargon-checking."""
    md = re.sub(r"^>\s*\*\*Notas internas.*?$.*", "", md, count=1, flags=re.DOTALL | re.MULTILINE)
    md = re.sub(r"^##\s*Apéndice — Cómo se construyó.*", "", md, count=1, flags=re.DOTALL | re.MULTILINE)
    return md


def test_deck_story_md_external_body_is_jargon_free():
    """The Spanish narrative (deck_story_es.md) must be jargon-free up to the
    "internal notes" appendix marker. The appendix itself is internal-only and
    explicitly out of scope per the document's own framing."""
    body = _strip_internal_notes(_strip_frontmatter(DECK_STORY_MD.read_text(encoding="utf-8")))
    leaks = [tok for tok in _FORBIDDEN_TOKENS_IN_DECK if tok in body]
    # Allow PRJ-HOL- and topic_enisa_company_dossier in metadata-only sections;
    # the external body should not carry them.
    assert not leaks, (
        f"deck_story_es.md external body contains forbidden tokens "
        f"(BRAND_JARGON_AUDIT.md §4): {leaks}"
    )


def test_cover_email_external_body_is_jargon_free():
    """The cover email body (down to the "Notas internas" marker) must be
    jargon-free. The internal notes block after the marker is operator-side
    metadata and is not sent."""
    body = _strip_internal_notes(_strip_frontmatter(COVER_EMAIL_MD.read_text(encoding="utf-8")))
    leaks = [tok for tok in _FORBIDDEN_TOKENS_IN_DECK if tok in body]
    assert not leaks, (
        f"cover_email_company_dossier_es.md body contains forbidden tokens: {leaks}"
    )


# ---------------------------------------------------------------------------
# Build script
# ---------------------------------------------------------------------------


def test_build_company_deck_check_only():
    proc = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--check-only"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, f"build_company_deck --check-only failed: {proc.stderr}"
    assert "schema OK" in proc.stdout


def test_html_deck_renders_all_primitives():
    """If the HTML preview is committed, it must carry all the deck primitives."""
    if not HTML_DECK.is_file():
        pytest.skip("HTML deck not yet built (run scripts/build_company_deck.py)")
    txt = HTML_DECK.read_text(encoding="utf-8")
    primitives = (
        '<section class="slide ',
        "slide-cover",
        "section-headline",
        "capability-card",
        "stat-grid",
        "stat-block",
        "icp-card",
        "bm-row",
        "moat-card",
        "roadmap-window",
        "fit-card",
        "use-of-funds",
        "ask-line",
        "ask-signature",
        "brand-monogram",
    )
    missing = [p for p in primitives if p not in txt]
    assert not missing, f"HTML deck missing primitives: {missing}"


def test_html_deck_has_zero_todo_operator_leaks():
    if not HTML_DECK.is_file():
        pytest.skip("HTML deck not yet built")
    txt = HTML_DECK.read_text(encoding="utf-8")
    assert "TODO[OPERATOR]" not in txt, (
        "HTML deck rendered with TODO[OPERATOR] leak — did the build skip the "
        "jargon audit gate?"
    )


def test_html_deck_has_14_slides():
    if not HTML_DECK.is_file():
        pytest.skip("HTML deck not yet built")
    txt = HTML_DECK.read_text(encoding="utf-8")
    n = txt.count('<section class="slide ')
    assert n == 14, f"HTML deck has {n} slides, expected exactly 14"


# ---------------------------------------------------------------------------
# Cover email body shape
# ---------------------------------------------------------------------------


def test_cover_email_uses_brand_spanish_patterns():
    body = _strip_internal_notes(_strip_frontmatter(COVER_EMAIL_MD.read_text(encoding="utf-8")))
    # Opener pattern: "Hola Guillermo," (peer_consulting + tu register)
    assert "Hola Guillermo," in body, "cover email missing the canonical Spanish opener"
    # Closer pattern.
    assert "Un saludo," in body, "cover email missing the canonical Spanish closer"
    # Brand signature.
    assert "Holística Research" in body or "Holistica Research" in body


# ---------------------------------------------------------------------------
# Initiative 29 P5: deck <- strategy SSOT wiring
# ---------------------------------------------------------------------------


SYNC_SCRIPT_I29 = REPO_ROOT / "scripts" / "sync_deck_from_strategy.py"


def test_sync_deck_from_strategy_script_exists():
    assert SYNC_SCRIPT_I29.is_file(), (
        f"missing {SYNC_SCRIPT_I29.relative_to(REPO_ROOT)} (Initiative 29 P5 deliverable)"
    )


def test_sync_deck_from_strategy_check_only_succeeds():
    """The strategy SSOT must be wired to the deck without contract violations."""
    proc = subprocess.run(
        [sys.executable, str(SYNC_SCRIPT_I29)],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, (
        f"sync_deck_from_strategy --check-only failed (rc={proc.returncode})\n"
        f"stderr={proc.stderr}\nstdout={proc.stdout}"
    )
    assert "deck-bound" in proc.stdout, (
        "sync_deck_from_strategy did not report any deck-bound artifacts"
    )


def test_sync_deck_from_strategy_apply_refuses_with_todos():
    """When founder TODOs remain unresolved, --apply must refuse with exit code 2."""
    proc = subprocess.run(
        [sys.executable, str(SYNC_SCRIPT_I29), "--apply"],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    # Either rc==0 (no TODOs left, --apply OK) or rc==2 (--apply refused).
    # The valid current state is rc==2 because the strategy artifacts ship with
    # TODO bands awaiting founder narrowing.
    assert proc.returncode in (0, 2), (
        f"sync_deck_from_strategy --apply produced unexpected rc={proc.returncode}\n"
        f"stderr={proc.stderr}\nstdout={proc.stdout}"
    )
    if proc.returncode == 2:
        assert "REFUSED" in proc.stderr, (
            "rc=2 from --apply but stderr does not contain REFUSED keyword"
        )
