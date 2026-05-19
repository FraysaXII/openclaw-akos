"""Tests for scripts/validate_locale_orthography.py and akos/orthography.py.

Per Wave F Strand 3a (I86; B1 ratify). Pairs with tests/test_external_render_trail.py
for the orthography sister validator.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_locale_orthography as validator  # noqa: E402
from akos.orthography import (  # noqa: E402
    ANTI_PATTERNS_BY_LOCALE,
    ES_ANTI_PATTERNS,
    EN_ANTI_PATTERNS,
    FR_ANTI_PATTERNS,
    OrthographyAntiPattern,
    VALID_LOCALES,
    extract_language,
    strip_non_prose,
)


pytestmark = pytest.mark.brand


class TestOrthographyChassisShape:
    """akos/orthography.py Pydantic chassis structural integrity."""

    def test_valid_locales_frozenset(self):
        assert VALID_LOCALES == frozenset({"es", "fr", "en"})

    def test_es_anti_patterns_nonempty(self):
        assert len(ES_ANTI_PATTERNS) >= 20

    def test_fr_anti_patterns_nonempty(self):
        assert len(FR_ANTI_PATTERNS) >= 20

    def test_en_anti_patterns_empty_by_design(self):
        assert EN_ANTI_PATTERNS == ()

    def test_es_patterns_all_locale_es(self):
        for pattern in ES_ANTI_PATTERNS:
            assert pattern.locale == "es"

    def test_fr_patterns_all_locale_fr(self):
        for pattern in FR_ANTI_PATTERNS:
            assert pattern.locale == "fr"

    def test_anti_patterns_frozen(self):
        pattern = ES_ANTI_PATTERNS[0]
        with pytest.raises(Exception):
            pattern.ascii_form = "mutated"

    def test_anti_patterns_by_locale_indexed(self):
        assert "es" in ANTI_PATTERNS_BY_LOCALE
        assert "fr" in ANTI_PATTERNS_BY_LOCALE
        assert "en" in ANTI_PATTERNS_BY_LOCALE
        assert ANTI_PATTERNS_BY_LOCALE["es"] == ES_ANTI_PATTERNS

    def test_high_consequence_es_word_ano(self):
        forms = {p.ascii_form for p in ES_ANTI_PATTERNS}
        assert "ano" in forms
        assert "anos" in forms

    def test_high_consequence_fr_word_francais(self):
        forms = {p.ascii_form for p in FR_ANTI_PATTERNS}
        assert "francais" in forms


class TestExtractLanguage:
    """Language frontmatter extraction tolerance."""

    def test_simple_es(self):
        assert extract_language("language: es\n") == "es"

    def test_simple_fr(self):
        assert extract_language("language: fr\n") == "fr"

    def test_simple_en(self):
        assert extract_language("language: en\n") == "en"

    def test_quoted_value(self):
        assert extract_language('language: "es"\n') == "es"

    def test_locale_variant_es_es(self):
        assert extract_language("language: es-ES\n") == "es"

    def test_locale_variant_fr_fr(self):
        assert extract_language("language: fr-FR\n") == "fr"

    def test_missing_returns_none(self):
        assert extract_language("audience: J-IN\n") is None

    def test_invalid_locale_returns_none(self):
        assert extract_language("language: zz\n") is None


class TestStripNonProse:
    """Body-prose preparation strips frontmatter, code, URLs, link targets."""

    def test_strips_frontmatter(self):
        text = "---\nlanguage: es\n---\n\nHola mañana."
        result = strip_non_prose(text)
        assert "language:" not in result
        assert "Hola mañana." in result

    def test_strips_fenced_code(self):
        text = "Body text.\n```python\nano = 5\n```\nMore body."
        result = strip_non_prose(text)
        assert "ano" not in result
        assert "Body text." in result
        assert "More body." in result

    def test_strips_inline_code(self):
        text = "The `ano` variable refers to year."
        result = strip_non_prose(text)
        assert "ano" not in result
        assert "year" in result

    def test_strips_urls(self):
        text = "See https://holistikaresearch.com/manana for details."
        result = strip_non_prose(text)
        assert "https://" not in result
        assert "details" in result

    def test_strips_link_targets_keeps_anchor(self):
        text = "[click here](https://example.com/manana)"
        result = strip_non_prose(text)
        assert "click here" in result
        assert "example.com" not in result

    def test_strips_html_comments(self):
        text = "Body.\n<!-- ano: invalid -->\nMore body."
        result = strip_non_prose(text)
        assert "ano: invalid" not in result


class TestSpanishAntiPatternScan:
    """ES word-list scan with word-boundary correctness."""

    def _build_md(self, body: str, locale: str = "es") -> str:
        return f"---\nlanguage: {locale}\n---\n\n{body}"

    def test_ano_detected(self, tmp_path):
        md = tmp_path / "cover_email_es.md"
        md.write_text(self._build_md("Hace un ano que trabajamos."), encoding="utf-8")
        body = strip_non_prose(md.read_text(encoding="utf-8"))
        hits = validator._scan_word_list(body, ES_ANTI_PATTERNS)
        forms = {p.ascii_form for p, _ in hits}
        assert "ano" in forms

    def test_anos_detected_distinct_from_ano(self, tmp_path):
        body = "Llevamos diez anos en este sector."
        hits = validator._scan_word_list(body, ES_ANTI_PATTERNS)
        forms = {p.ascii_form for p, _ in hits}
        assert "anos" in forms

    def test_word_boundary_no_substring_false_positive(self):
        body = "El piano del salon es nuevo."
        hits = validator._scan_word_list(body, ES_ANTI_PATTERNS)
        forms = {p.ascii_form for p, _ in hits}
        assert "ano" not in forms

    def test_correct_spelling_no_false_positive(self):
        body = "Hace un año que trabajamos con la organización."
        hits = validator._scan_word_list(body, ES_ANTI_PATTERNS)
        assert hits == []

    def test_multiple_anti_patterns_distinct(self):
        body = "Necesitamos la informacion sobre la gestion de la decision."
        hits = validator._scan_word_list(body, ES_ANTI_PATTERNS)
        forms = {p.ascii_form for p, _ in hits}
        assert "informacion" in forms
        assert "gestion" in forms
        assert "decision" in forms

    def test_count_aggregates_repeats(self):
        body = "La decision. Otra decision. Una decision mas."
        hits = validator._scan_word_list(body, ES_ANTI_PATTERNS)
        decision_hits = [(p, c) for p, c in hits if p.ascii_form == "decision"]
        assert len(decision_hits) == 1
        assert decision_hits[0][1] == 3


class TestFrenchAntiPatternScan:
    """FR word-list scan with cedilla + diacritic discipline."""

    def test_francais_detected(self):
        body = "Nous sommes francais et bien établis."
        hits = validator._scan_word_list(body, FR_ANTI_PATTERNS)
        forms = {p.ascii_form for p, _ in hits}
        assert "francais" in forms

    def test_cybersecurite_detected(self):
        body = "Nous travaillons en cybersecurite."
        hits = validator._scan_word_list(body, FR_ANTI_PATTERNS)
        forms = {p.ascii_form for p, _ in hits}
        assert "cybersecurite" in forms

    def test_correct_spelling_no_false_positive(self):
        body = "Nous sommes français et travaillons en cybersécurité."
        hits = validator._scan_word_list(body, FR_ANTI_PATTERNS)
        assert hits == []

    def test_metier_apres_methode(self):
        body = "Notre metier est de réduire le risque apres la methode."
        hits = validator._scan_word_list(body, FR_ANTI_PATTERNS)
        forms = {p.ascii_form for p, _ in hits}
        assert "metier" in forms
        assert "apres" in forms
        assert "methode" in forms


class TestEnglishSmartQuoteScan:
    """EN smart-quote threshold heuristic."""

    def test_below_threshold_clean(self):
        body = 'A single "quoted" word is fine.'
        assert validator._scan_en_smart_quotes(body) == 2

    def test_above_threshold_flags(self):
        body = '"One" "two" "three" "four" "five"'
        count = validator._scan_en_smart_quotes(body)
        assert count == 10
        assert count >= validator.EN_STRAIGHT_QUOTE_THRESHOLD

    def test_curly_quotes_not_flagged(self):
        body = "Curly \u201cone\u201d and \u201ctwo\u201d and \u201cthree\u201d."
        assert validator._scan_en_smart_quotes(body) == 0


class TestValidatorEndToEnd:
    """End-to-end validator invocation with synthetic surfaces."""

    def _write_advops_surface(self, tmp_repo: Path, name: str, locale: str, body: str) -> Path:
        target = tmp_repo / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "advops" / "test" / "engagement"
        target.mkdir(parents=True, exist_ok=True)
        path = target / name
        path.write_text(
            f"---\naudience: J-AD\nlanguage: {locale}\n---\n\n{body}",
            encoding="utf-8",
        )
        return path

    def test_clean_surface_passes(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
        self._write_advops_surface(
            tmp_path,
            "cover_email_es.md",
            "es",
            "Estimado Sr. García, le envío la información solicitada. Saludos cordiales.",
        )
        exit_code = validator.validate(strict=True)
        assert exit_code == 0

    def test_dirty_surface_fails_in_strict(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
        self._write_advops_surface(
            tmp_path,
            "cover_email_es.md",
            "es",
            "Estimado Sr. Garcia, le envio la informacion. Saludos.",
        )
        exit_code = validator.validate(strict=True)
        assert exit_code == 1

    def test_dirty_surface_passes_in_advisory(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
        self._write_advops_surface(
            tmp_path,
            "cover_email_es.md",
            "es",
            "Estimado Sr. Garcia, le envio la informacion. Saludos.",
        )
        exit_code = validator.validate(strict=False)
        assert exit_code == 0

    def test_per_locale_strict_es_only(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
        self._write_advops_surface(
            tmp_path,
            "cover_email_es.md",
            "es",
            "Sin informacion clara.",
        )
        self._write_advops_surface(
            tmp_path,
            "cover_email_fr.md",
            "fr",
            "Notre metier est important.",
        )
        es_only = validator.validate(strict_es=True)
        assert es_only == 1

    def test_per_locale_strict_fr_only_misses_es(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
        self._write_advops_surface(
            tmp_path,
            "cover_email_es.md",
            "es",
            "Sin informacion clara.",
        )
        fr_only = validator.validate(strict_fr=True)
        assert fr_only == 0

    def test_no_language_frontmatter_skipped(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
        target = tmp_path / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "advops" / "test" / "engagement"
        target.mkdir(parents=True, exist_ok=True)
        (target / "cover_email_es.md").write_text(
            "---\naudience: J-AD\n---\n\nSin informacion clara mañana.",
            encoding="utf-8",
        )
        exit_code = validator.validate(strict=True)
        assert exit_code == 0

    def test_env_var_strict(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
        monkeypatch.setenv("AKOS_LOCALE_ORTHOGRAPHY_STRICT", "1")
        self._write_advops_surface(
            tmp_path,
            "cover_email_es.md",
            "es",
            "Sin informacion clara.",
        )
        exit_code = validator.validate()
        assert exit_code == 1


class TestRepoScopeScan:
    """Run against the real repo SCAN_GLOBS to surface any current hits.

    This test does NOT assert PASS/FAIL — it documents the current state so
    future drift surfaces explicitly. Use ``pytest -k repo_scope -v -s`` to
    see the per-locale counts.
    """

    def test_advisory_mode_completes(self):
        exit_code = validator.validate(strict=False)
        assert exit_code == 0
