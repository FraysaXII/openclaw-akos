"""Tests for the Initiative 27 ENISA dossier renderer.

Covers:
- ``akos.hlk_pdf_render`` brand token table mirrors ``BRAND_VISUAL_PATTERNS.md``
  (smoke + drift safeguard).
- ``scripts/render_dossier.py`` resolves the canonical dossier markdown and
  parses cleanly under ``--smoke``.
- ``dossier_es.md`` cites every concrete adviser question by ``Q-…`` row id
  (citation-discipline guardrail).
- ``compose_adviser_message.py --body cover_email_es.md`` inlines the
  hand-authored body into the Layer 4 block instead of emitting the TODO
  marker.
"""
from __future__ import annotations

import importlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DOSSIER_MD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "advops"
    / "PRJ-HOL-FOUNDING-2026"
    / "enisa_evidence"
    / "dossier_es.md"
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
    / "enisa_evidence"
    / "cover_email_es.md"
)
BRAND_VISUAL_PATTERNS_MD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Marketing"
    / "Brand"
    / "BRAND_VISUAL_PATTERNS.md"
)
ADVISER_QUESTIONS_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "ADVISER_OPEN_QUESTIONS.csv"
)
TOPIC_REGISTRY_CSV = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "compliance"
    / "dimensions"
    / "TOPIC_REGISTRY.csv"
)

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


# ---------- Brand token presence ---------------------------------------------


def test_brand_tokens_light_match_pattern_doc():
    """The Python-side BRAND_TOKENS_LIGHT must mirror BRAND_VISUAL_PATTERNS.md.

    Drift safeguard: when the brand pattern doc edits a token, this test fails
    until the constant table in ``akos/hlk_pdf_render.py`` is updated.

    The pattern-doc table cites HSL as ``168 55% 38%`` (the inner triple) inside
    backticks; the Python constants wrap them with ``hsl(...)``. Compare on the
    inner triple to stay format-tolerant.
    """
    mod = importlib.import_module("akos.hlk_pdf_render")
    md_text = BRAND_VISUAL_PATTERNS_MD.read_text(encoding="utf-8")

    for token_name, hsl_value in mod.BRAND_TOKENS_LIGHT.items():
        match = re.match(r"hsl\((.+)\)", hsl_value)
        assert match, f"{token_name} value {hsl_value!r} is not a hsl(...) string"
        inner = match.group(1)
        assert inner in md_text, (
            f"{token_name}=hsl({inner}) not present in BRAND_VISUAL_PATTERNS.md; "
            "either update the pattern doc or the constant table - they must agree."
        )


def test_brand_pdf_css_contains_all_dossier_classes():
    mod = importlib.import_module("akos.hlk_pdf_render")
    css = mod._brand_pdf_css(profile="dossier")
    for needed in (
        ".cover-hero",
        ".cover-monogram",
        ".cover-rule",
        ".cover-meta",
        "callout-operator",
        "callout-risk",
        "page-break-after: always",
        "Inter",
        "hsl(168 55% 38%)",
        "hsl(38 80% 50%)",
        "hsl(220 16% 7%)",
    ):
        assert needed in css, f"branded PDF CSS missing: {needed!r}"


def test_render_pdf_branded_signature():
    mod = importlib.import_module("akos.hlk_pdf_render")
    fn = mod.render_pdf_branded
    import inspect
    params = inspect.signature(fn).parameters
    for required in (
        "md_text",
        "out_path",
        "profile",
        "title",
        "subtitle",
        "program_id",
        "discipline",
        "issue_date",
        "status_label",
        "monogram_path",
    ):
        assert required in params, f"render_pdf_branded missing kwarg {required!r}"


# ---------- render_dossier.py smoke ------------------------------------------


def test_render_dossier_smoke_resolves_canonical_markdown():
    """``--smoke`` must report ``smoke OK`` for the default program/language."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "render_dossier.py"), "--smoke"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, f"render_dossier --smoke failed: {proc.stderr}\n{proc.stdout}"
    assert "smoke OK" in proc.stdout
    assert "PRJ-HOL-FOUNDING-2026" in proc.stdout
    assert "language=" not in proc.stdout or "es" in proc.stdout


def test_render_dossier_refuses_unknown_language():
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "render_dossier.py"),
            "--smoke",
            "--language",
            "en",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode != 0
    assert "REFUSED" in proc.stderr or "REFUSED" in proc.stdout


# ---------- Citation discipline -----------------------------------------------


def _question_ids() -> set[str]:
    if not ADVISER_QUESTIONS_CSV.is_file():
        return set()
    out: set[str] = set()
    for line in ADVISER_QUESTIONS_CSV.read_text(encoding="utf-8").splitlines()[1:]:
        if not line.strip():
            continue
        qid = line.split(",", 1)[0].strip()
        if qid:
            out.add(qid)
    return out


def test_dossier_cites_every_active_q_row():
    """Every ``Q-…`` row from ``ADVISER_OPEN_QUESTIONS.csv`` must appear in the
    dossier — citation discipline. If a row is added to the CSV, the dossier
    must learn about it before the next render.
    """
    md = DOSSIER_MD.read_text(encoding="utf-8")
    cited_in_md = set(re.findall(r"Q-[A-Z]{3}-\d{3}", md))
    canonical = _question_ids()
    if not canonical:
        pytest.skip("ADVISER_OPEN_QUESTIONS.csv unreadable")
    missing = canonical - cited_in_md
    assert not missing, (
        f"dossier_es.md must cite every Q-row in ADVISER_OPEN_QUESTIONS.csv; "
        f"missing: {sorted(missing)}"
    )


def test_dossier_cites_program_id_explicitly():
    md = DOSSIER_MD.read_text(encoding="utf-8")
    assert "PRJ-HOL-FOUNDING-2026" in md
    assert "program_id: PRJ-HOL-FOUNDING-2026" in md  # frontmatter SSOT


def test_dossier_includes_5_capability_cards():
    md = DOSSIER_MD.read_text(encoding="utf-8")
    for card_label in (
        "Holistika Boilerplate",
        "HLK ERP",
        "KiRBe SaaS",
        "Holistika × Websitz",
        "Rushly",
    ):
        assert card_label in md, f"capability card missing: {card_label!r}"


# ---------- Topic registry row ------------------------------------------------


def test_topic_registry_has_dossier_es_row():
    text = TOPIC_REGISTRY_CSV.read_text(encoding="utf-8")
    assert "topic_enisa_dossier_es" in text
    assert "parent_topic" in text.splitlines()[0]
    rows = [r for r in text.splitlines()[1:] if r.startswith("topic_enisa_dossier_es,")]
    assert len(rows) == 1
    row = rows[0]
    assert "PRJ-HOL-FOUNDING-2026" in row
    assert "advops" in row
    assert "topic_enisa_evidence" in row  # parent_topic
    assert "dossier_es.md" in row  # manifest_path


# ---------- Composer body inlining --------------------------------------------


def test_compose_adviser_inlines_body_file(composer=None):
    """``--body`` flag inlines the canonical Spanish body into Layer 4."""
    spec = importlib.util.spec_from_file_location(
        "_compose_adviser_message_inline", REPO_ROOT / "scripts" / "compose_adviser_message.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("_compose_adviser_message_inline", mod)
    spec.loader.exec_module(mod)

    rec = {"ref_id": "POI-LEG-ENISA-LEAD-2026", "lens": "legal_certification", "class": "external_legal_adviser", "sensitivity": "confidential"}
    disc = {"discipline_id": "legal", "discipline_code": "LEG", "discipline_name": "Legal Counsel"}
    md = mod.render_md(
        recipient=rec,
        discipline=disc,
        program=None,
        voice_register="peer_consulting",
        voice_source="recipient",
        language="es",
        pronoun="tu",
        sharing_label="counsel_and_named_counterparty",
        evidence_path=None,
        body_path=COVER_EMAIL_MD,
    )
    assert "## Layer 4 — Eloquence" in md
    assert "TODO operator" not in md
    assert "Buenos días, Guillermo" in md
    assert "Q-LEG-001" in md
    assert "Un saludo," in md


def test_compose_adviser_emits_todo_when_no_body():
    spec = importlib.util.spec_from_file_location(
        "_compose_adviser_message_inline_b", REPO_ROOT / "scripts" / "compose_adviser_message.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("_compose_adviser_message_inline_b", mod)
    spec.loader.exec_module(mod)

    rec = {"ref_id": "POI-LEG-ENISA-LEAD-2026", "lens": "legal_certification", "class": "external_legal_adviser", "sensitivity": "confidential"}
    disc = {"discipline_id": "legal", "discipline_code": "LEG", "discipline_name": "Legal Counsel"}
    md = mod.render_md(
        recipient=rec,
        discipline=disc,
        program=None,
        voice_register="peer_consulting",
        voice_source="recipient",
        language="es",
        pronoun="tu",
        sharing_label="counsel_and_named_counterparty",
        evidence_path=None,
        body_path=None,
    )
    assert "TODO operator" in md
