"""Tests for akos/orthography.py ``apply_smart_quotes`` (Wave G Bundle B-G1).

Per D-IH-86-R (2026-05-19): the render-step auto-curl helper transforms
straight ASCII quotes into locale-correct curly typography while preserving
code blocks, URLs, and HTML attribute values. These tests lock the public
contract of ``apply_smart_quotes(text, language)``:

- EN: ``"...".`` → ``\\u201c...\\u201d.`` and ``'`` → ``\\u2019`` (apostrophe)
  with leading ``'`` after whitespace becoming ``\\u2018`` (opening single).
- ES + FR: ``"..."`` → ``«...»``; single quotes follow the EN rule for nested.
- Protected regions never get curled: ``<pre>``, ``<code>``, HTML tags
  (including their attribute values), URLs, HTML comments, markdown fenced
  code, and markdown inline code.
- Already-curly text is idempotent (no double-conversion).

The function is hooked into ``akos.hlk_pdf_render.render_pdf_branded`` (so
the rendered HTML body carries curly quotes pre-WeasyPrint) and into
``scripts/validate_locale_orthography._scan_en_smart_quotes`` (so the
delivery-gate semantics count post-curl straight quotes).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.orthography import apply_smart_quotes  # noqa: E402


pytestmark = pytest.mark.brand


# Curly-quote codepoints used for assertion clarity throughout the file.
LDQ = "\u201c"  # left double quote
RDQ = "\u201d"  # right double quote
LSQ = "\u2018"  # left single quote
RSQ = "\u2019"  # right single quote / apostrophe
LAQ = "\u00ab"  # left guillemet «
RAQ = "\u00bb"  # right guillemet »


class TestEnglishSmartQuotes:
    """EN smart-quote conversion per BRAND_ENGLISH_PATTERNS §10."""

    def test_basic_double_quote_pair(self):
        result = apply_smart_quotes('He said "hello" loudly.', language="en")
        assert result == f"He said {LDQ}hello{RDQ} loudly."

    def test_single_apostrophe_contraction(self):
        result = apply_smart_quotes("Holistika's vision is clear.", language="en")
        assert result == f"Holistika{RSQ}s vision is clear."

    def test_multiple_balanced_quote_pairs(self):
        result = apply_smart_quotes(
            'A "first" and a "second" and a "third".', language="en"
        )
        assert result == f"A {LDQ}first{RDQ} and a {LDQ}second{RDQ} and a {LDQ}third{RDQ}."

    def test_nested_single_inside_double(self):
        result = apply_smart_quotes(
            'He said "she replied \'yes\' to me".', language="en"
        )
        assert LDQ in result and RDQ in result
        assert LSQ in result and RSQ in result


class TestSpanishSmartQuotes:
    """ES smart-quote conversion per BRAND_SPANISH_PATTERNS §3 reference exchange."""

    def test_basic_guillemet_pair(self):
        result = apply_smart_quotes(
            'El estudio "definitivo" del año.', language="es"
        )
        assert result == f"El estudio {LAQ}definitivo{RAQ} del año."

    def test_multiple_guillemet_pairs(self):
        result = apply_smart_quotes(
            'Llamado "primero" y "segundo".', language="es"
        )
        assert result == f"Llamado {LAQ}primero{RAQ} y {LAQ}segundo{RAQ}."

    def test_apostrophe_becomes_right_single(self):
        result = apply_smart_quotes("Don't worry.", language="es")
        assert result == f"Don{RSQ}t worry."


class TestFrenchSmartQuotes:
    """FR smart-quote conversion per BRAND_FRENCH_PATTERNS §4 patterns."""

    def test_basic_guillemet_pair(self):
        result = apply_smart_quotes(
            'Notre méthode "intégrée" est claire.', language="fr"
        )
        assert result == f"Notre méthode {LAQ}intégrée{RAQ} est claire."

    def test_apostrophe_in_french_prose(self):
        result = apply_smart_quotes("L'équipe d'Holistika.", language="fr")
        assert result == f"L{RSQ}équipe d{RSQ}Holistika."


class TestProtectedRegions:
    """Code blocks, URLs, HTML attribute values must NOT be curled."""

    def test_pre_block_protected(self):
        result = apply_smart_quotes(
            'Prose "before". <pre>code = "untouched";</pre> Prose "after".',
            language="en",
        )
        assert '"untouched"' in result
        assert LDQ in result and RDQ in result

    def test_code_inline_protected(self):
        result = apply_smart_quotes(
            'Use <code>x = "y"</code> in code.', language="en"
        )
        assert '"y"' in result
        assert '<code>' in result

    def test_html_attribute_value_protected_double(self):
        result = apply_smart_quotes(
            '<a href="https://example.com">click here</a>', language="en"
        )
        assert 'href="https://example.com"' in result

    def test_html_attribute_value_protected_single(self):
        result = apply_smart_quotes(
            "<a href='https://example.com' title='link'>click</a>", language="en"
        )
        assert "href='https://example.com'" in result

    def test_url_protected_in_bare_text(self):
        result = apply_smart_quotes(
            'See "this paper" at https://example.com/path?q=foo for details.',
            language="en",
        )
        assert "https://example.com/path?q=foo" in result
        assert LDQ + "this paper" + RDQ in result

    def test_html_comment_protected(self):
        result = apply_smart_quotes(
            '<!-- note: "internal" reference --> Visible "prose".',
            language="en",
        )
        assert '"internal"' in result  # inside comment, untouched
        assert f"Visible {LDQ}prose{RDQ}" in result  # visible prose curled

    def test_markdown_fenced_code_protected(self):
        result = apply_smart_quotes(
            'Prose "before".\n```python\nx = "untouched"\n```\nProse "after".',
            language="en",
        )
        assert '"untouched"' in result
        assert f"Prose {LDQ}before{RDQ}" in result

    def test_markdown_inline_code_protected(self):
        result = apply_smart_quotes(
            'Use `x = "y"` for assignment.', language="en"
        )
        assert '`x = "y"`' in result


class TestIdempotenceAndEdgeCases:
    """Round-trip stability and edge-case behavior."""

    def test_already_curly_unchanged(self):
        original = f"Already {LDQ}curly{RDQ} text and {LSQ}single{RSQ}."
        result = apply_smart_quotes(original, language="en")
        assert result == original

    def test_empty_string_returns_empty(self):
        assert apply_smart_quotes("", language="en") == ""

    def test_no_quotes_returns_unchanged(self):
        body = "No quotes anywhere in this sentence."
        assert apply_smart_quotes(body, language="en") == body

    def test_unknown_language_is_noop(self):
        body = 'Has "quotes" inside.'
        assert apply_smart_quotes(body, language="zz") == body

    def test_mixed_html_structure_preserved(self):
        body = (
            '<p>A paragraph with "quotes".</p>'
            '<p>Another with <a href="https://x">link</a> and "more".</p>'
        )
        result = apply_smart_quotes(body, language="en")
        assert "<p>" in result and "</p>" in result
        assert 'href="https://x"' in result
        assert f"{LDQ}quotes{RDQ}" in result
        assert f"{LDQ}more{RDQ}" in result

    def test_unicode_text_preserved(self):
        body = 'Año "información" — décision'
        result = apply_smart_quotes(body, language="en")
        assert "Año" in result
        assert "información" in result
        assert "décision" in result
        assert f"{LDQ}información{RDQ}" in result

    def test_leading_apostrophe_after_space_opens(self):
        result = apply_smart_quotes("In the '80s, things were different.", language="en")
        assert f"In the {LSQ}80s" in result


class TestValidatorIntegrationPostCurlCount:
    """End-to-end: the validator's EN scan now counts POST-curl quotes."""

    def test_balanced_prose_curls_to_zero(self):
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        import validate_locale_orthography as v
        body = 'A "quoted" word and "another" one.'
        assert v._scan_en_smart_quotes(body) == 0

    def test_protected_attr_quotes_survive(self):
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        import validate_locale_orthography as v
        body = (
            '<a href="https://x">a</a><a href="https://y">b</a>'
            '<a href="https://z">c</a><a href="https://w">d</a>'
        )
        assert v._scan_en_smart_quotes(body) >= 4
