"""Tests for scripts/compose_adviser_message.py (Initiative 24 P4)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "compose_adviser_message.py"


@pytest.fixture(scope="module")
def composer():
    spec = importlib.util.spec_from_file_location("compose_adviser_message_module", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("compose_adviser_message_module", module)
    spec.loader.exec_module(module)
    return module


def test_voice_register_precedence_recipient_wins(composer):
    """Recipient's voice_register beats discipline default beats brand default beats global."""
    rec = {"voice_register": "formal_legal"}
    disc = {"default_voice_register": "peer_consulting"}
    register, source = composer.resolve_voice_register(rec, disc, brand_ready=True)
    assert register == "formal_legal"
    assert source == "recipient"


def test_voice_register_precedence_discipline_when_recipient_empty(composer):
    rec = {"voice_register": ""}
    disc = {"default_voice_register": "regulator_neutral"}
    register, source = composer.resolve_voice_register(rec, disc, brand_ready=True)
    assert register == "regulator_neutral"
    assert source == "discipline"


def test_voice_register_precedence_brand_when_discipline_empty(composer):
    rec = {"voice_register": ""}
    disc = {"default_voice_register": ""}
    register, source = composer.resolve_voice_register(rec, disc, brand_ready=True)
    assert source == "brand"
    assert register == "peer_consulting"  # current brand-ready default


def test_voice_register_precedence_global_when_brand_unready(composer):
    rec = {"voice_register": ""}
    disc = {"default_voice_register": ""}
    register, source = composer.resolve_voice_register(rec, disc, brand_ready=False)
    assert register == composer.GLOBAL_DEFAULT_REGISTER
    assert source == "global"


def test_resolve_language_default(composer):
    assert composer.resolve_language({}) == composer.GLOBAL_DEFAULT_LANGUAGE
    assert composer.resolve_language({"language_preference": "es"}) == "es"


def test_resolve_pronoun_empty_when_unset(composer):
    assert composer.resolve_pronoun({}) == ""
    assert composer.resolve_pronoun({"pronoun_register": "tu"}) == "tu"


def test_resolve_sharing_label(composer):
    assert composer.resolve_sharing_label({"sensitivity": "restricted"}) == "internal_only"
    assert composer.resolve_sharing_label({"sensitivity": "confidential"}) == "counsel_and_named_counterparty"
    assert composer.resolve_sharing_label({"sensitivity": "public"}) == "counsel_ok"
    assert composer.resolve_sharing_label({"sensitivity": "internal"}) == "counsel_ok"


def test_render_md_emits_frontmatter_and_layers(composer):
    rec = {
        "ref_id": "POI-LEG-ENISA-LEAD-2026",
        "sensitivity": "internal",
        "lens": "entity_readiness",
        "class": "external_adviser",
    }
    disc = {"discipline_id": "legal", "discipline_code": "LEG", "discipline_name": "Legal"}
    md = composer.render_md(
        recipient=rec,
        discipline=disc,
        program={"program_id": "PRJ-HOL-FOUNDING-2026", "program_code": "FND", "program_name": "X"},
        voice_register="peer_consulting",
        voice_source="recipient",
        language="es",
        pronoun="tu",
        sharing_label="counsel_ok",
        evidence_path=None,
    )
    assert "recipient_ref_id: POI-LEG-ENISA-LEAD-2026" in md
    assert "Layer 1 — Brand voice" in md
    assert "Layer 2 — Concept" in md
    assert "Layer 3 — Use-case" in md
    assert "Layer 4 — Eloquence" in md
    assert "voice_register: peer_consulting" in md
    assert "Pre-flight checklist" in md


def test_render_text_strips_mermaid_and_markdown(composer):
    md = "---\na: b\n---\n# Title\n\n```mermaid\ngraph TD; A-->B\n```\n\n**Bold** and `code`.\n"
    text = composer.render_text(md)
    assert "mermaid" not in text
    assert "graph TD" not in text
    assert "**Bold**" not in text
    assert "Bold" in text
    assert "Title" in text


def test_render_html_wraps_body(composer):
    md = "# Hello\nworld"
    html = composer.render_html(md)
    assert "<!doctype html>" in html
    assert "<body>" in html
    assert "Hello" in html


def test_main_refuses_unknown_recipient(composer, capsys, monkeypatch):
    rc = composer.main([
        "--recipient", "POI-DOES-NOT-EXIST-2026",
        "--discipline", "LEG",
        "--dry-run",
        "--allow-scaffold-tokens",
    ])
    assert rc == 2
    err = capsys.readouterr().err
    assert "unknown recipient" in err


def test_main_refuses_brand_scaffold_without_flag(composer, capsys):
    """When BRAND_VOICE_FOUNDATION.md is scaffold-staged, default refusal."""
    ready, status = composer.brand_foundation_status()
    if ready:
        pytest.skip("brand foundation is active; this test only runs while scaffold-staged")
    rc = composer.main([
        "--recipient", "POI-LEG-ENISA-LEAD-2026",
        "--discipline", "LEG",
        "--dry-run",
    ])
    assert rc == 1
    err = capsys.readouterr().err
    assert "BRAND_FOUNDATION_NOT_READY" in err


def test_main_dry_run_succeeds_with_scaffold_tokens(composer, capsys):
    rc = composer.main([
        "--recipient", "POI-LEG-ENISA-LEAD-2026",
        "--discipline", "LEG",
        "--program-id", "PRJ-HOL-FOUNDING-2026",
        "--dry-run",
        "--allow-scaffold-tokens",
    ])
    assert rc == 0
    out = capsys.readouterr().out
    assert "POI-LEG-ENISA-LEAD-2026" in out
    assert "Layer 4" in out


def test_main_unknown_program_id_returns_2(composer, capsys):
    rc = composer.main([
        "--recipient", "POI-LEG-ENISA-LEAD-2026",
        "--discipline", "LEG",
        "--program-id", "PRJ-HOL-NONEXISTENT-9999",
        "--dry-run",
        "--allow-scaffold-tokens",
    ])
    assert rc == 2
    err = capsys.readouterr().err
    assert "unknown program_id" in err
