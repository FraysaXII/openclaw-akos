"""Tests for the I71 P2 Pack A3 brand multilingual locale-suffix validator.

Covers:

- ``akos/brand_voice_register.py`` Pack A3 chassis additions: ``LocaleSuffixRule``,
  ``ReadmeTriadRule``, ``BrandMultilingualPack``.
- Parser helpers: ``parse_locale_suffix_rules``, ``parse_readme_triad_rules``,
  ``parse_multilingual_pack_yaml``.
- ``scripts/validate_brand_multilingual.py``: frontmatter parser, engagement-folder
  walking, three detection classes (frontmatter cohesion; pointer skeleton when
  per-locale siblings exist; pointer target completeness), pack-override
  semantics, monolingual-engagement skip behaviour, --strict-empty.

Runs under ``pytest -m brand`` per ``pyproject.toml``.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

pytestmark = pytest.mark.brand

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.brand_voice_register import (  # noqa: E402
    CANONICAL_PATHS,
    BrandMultilingualPack,
    LocaleSuffixRule,
    ReadmeTriadRule,
    parse_locale_suffix_rules,
    parse_multilingual_pack_yaml,
    parse_readme_triad_rules,
)

import scripts.validate_brand_multilingual as multilingual_validator  # noqa: E402


# ---------------------------------------------------------------------------
# Chassis model tests
# ---------------------------------------------------------------------------


class TestChassisModels:
    def test_locale_suffix_rule_carries_canonical_section(self) -> None:
        rule = LocaleSuffixRule(
            locale="fr",
            expected_suffix=".fr.md",
            frontmatter_language_value="fr",
        )
        assert rule.canonical_section == "BRAND_MULTILINGUAL_CONTRACT.md §2"
        assert rule.default_severity == "error"

    def test_readme_triad_rule_defaults_to_warning(self) -> None:
        rule = ReadmeTriadRule()
        assert rule.default_severity == "warning"
        assert "Per-language READMEs:" in rule.required_pointer_keywords
        assert rule.per_locale_readme_required is True
        # "5-line pointer" is canonical prose; enforcement floor is 3 to
        # accommodate bilingual pointers (title + intro + 2 bullets = 4 lines)
        # while still rejecting trivial "just a title" placeholders.
        assert rule.pointer_line_count_min == 3
        assert rule.pointer_line_count_max == 12

    def test_brand_multilingual_pack_default_triad_severity(self) -> None:
        pack = BrandMultilingualPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Test",
            canonical_source_refs=("test",),
        )
        assert pack.default_triad_severity == "warning"
        assert pack.locale_suffix_rules == ()
        assert pack.readme_triad_rules == ()


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_locale_suffix_rules_returns_three(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["multilingual_contract"]
        rules = parse_locale_suffix_rules(path)
        assert len(rules) == 3
        locales = {r.locale for r in rules}
        assert locales == {"en", "fr", "es"}

    def test_parse_locale_suffix_rules_suffix_to_language(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["multilingual_contract"]
        rules = parse_locale_suffix_rules(path)
        by_locale = {r.locale: r for r in rules}
        assert by_locale["fr"].expected_suffix == ".fr.md"
        assert by_locale["en"].frontmatter_language_value == "en"

    def test_parse_locale_suffix_rules_absent_canonical(self, tmp_path: Path) -> None:
        assert parse_locale_suffix_rules(tmp_path / "missing.md") == []

    def test_parse_readme_triad_rules_returns_default_rule(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["multilingual_contract"]
        rules = parse_readme_triad_rules(path)
        assert len(rules) == 1
        assert rules[0].default_severity == "warning"

    def test_parse_multilingual_pack_yaml_loads_default_pack(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["multilingual_pack_yaml"]
        pack = parse_multilingual_pack_yaml(path)
        assert isinstance(pack, BrandMultilingualPack)
        assert pack.default_triad_severity in ("warning", "error")

    def test_parse_multilingual_pack_yaml_absent_returns_none(self, tmp_path: Path) -> None:
        assert parse_multilingual_pack_yaml(tmp_path / "missing.yml") is None


# ---------------------------------------------------------------------------
# Frontmatter + pointer detection helpers
# ---------------------------------------------------------------------------


class TestHelpers:
    def test_is_pointer_readme_detects_keyword(self) -> None:
        text = "# T\n\nFoo. Per-language READMEs:\n- [README.fr.md](README.fr.md)\n"
        assert multilingual_validator._is_pointer_readme(text) is True

    def test_is_pointer_readme_rejects_full_prose(self) -> None:
        text = "# T\n\nThis is a single-language README.\n"
        assert multilingual_validator._is_pointer_readme(text) is False

    def test_extract_pointer_link_targets(self) -> None:
        text = (
            "# T\n\nPer-language READMEs:\n"
            "- [README.fr.md](README.fr.md) — fr\n"
            "- [README.en.md](README.en.md) — en\n"
        )
        targets = multilingual_validator._extract_pointer_link_targets(text)
        assert targets == ["README.fr.md", "README.en.md"]


# ---------------------------------------------------------------------------
# Engagement scan fixtures
# ---------------------------------------------------------------------------


def _write_engagement(
    root: Path,
    name: str,
    files: dict[str, str],
) -> Path:
    folder = root / name
    folder.mkdir(parents=True, exist_ok=True)
    for fname, body in files.items():
        (folder / fname).write_text(body, encoding="utf-8")
    return folder


_VALID_POINTER = textwrap.dedent(
    """\
    ---
    language: en
    status: active
    role_owner: PMO
    last_review: 2026-05-12
    ---

    # Test engagement

    This engagement is bilingual (FR + EN) per `BRAND_MULTILINGUAL_CONTRACT.md`. Per-language READMEs:

    - [README.fr.md](README.fr.md) — version française
    - [README.en.md](README.en.md) — English version
    """
)
_VALID_FR = textwrap.dedent(
    """\
    ---
    language: fr
    status: active
    role_owner: PMO
    ---

    # Test engagement — version française

    Engagement réel.
    """
)
_VALID_EN = textwrap.dedent(
    """\
    ---
    language: en
    status: active
    role_owner: PMO
    ---

    # Test engagement — English

    Real engagement.
    """
)


@pytest.fixture()
def chassis_rules():
    canonical = REPO_ROOT / CANONICAL_PATHS["multilingual_contract"]
    return (
        parse_locale_suffix_rules(canonical),
        parse_readme_triad_rules(canonical),
    )


# ---------------------------------------------------------------------------
# Detection classes
# ---------------------------------------------------------------------------


class TestDetectionClasses:
    def test_clean_triad_passes(self, tmp_path: Path, chassis_rules) -> None:
        locale_rules, triad_rules = chassis_rules
        eng = _write_engagement(
            tmp_path,
            "2026-clean",
            {
                "README.md": _VALID_POINTER,
                "README.fr.md": _VALID_FR,
                "README.en.md": _VALID_EN,
            },
        )
        hits = multilingual_validator.scan_engagement(
            eng, locale_rules, triad_rules, "warning"
        )
        assert hits == []

    def test_monolingual_engagement_skipped(self, tmp_path: Path, chassis_rules) -> None:
        """Engagement with only README.md (no per-locale siblings) is skipped silently."""
        locale_rules, triad_rules = chassis_rules
        eng = _write_engagement(
            tmp_path,
            "2026-monolingual",
            {
                "README.md": "---\nlanguage: en\n---\n\n# Mono\n\nSingle-language readme.\n",
            },
        )
        hits = multilingual_validator.scan_engagement(
            eng, locale_rules, triad_rules, "warning"
        )
        assert hits == []

    def test_locale_frontmatter_mismatch_error(self, tmp_path: Path, chassis_rules) -> None:
        """README.fr.md declaring language: en is a frontmatter cohesion error."""
        locale_rules, triad_rules = chassis_rules
        bad_fr = _VALID_FR.replace("language: fr", "language: en")
        eng = _write_engagement(
            tmp_path,
            "2026-mismatch",
            {
                "README.md": _VALID_POINTER,
                "README.fr.md": bad_fr,
                "README.en.md": _VALID_EN,
            },
        )
        hits = multilingual_validator.scan_engagement(
            eng, locale_rules, triad_rules, "warning"
        )
        rule_ids = {h.rule_id for h in hits}
        assert "locale-frontmatter-mismatch" in rule_ids
        mismatch_hit = next(h for h in hits if h.rule_id == "locale-frontmatter-mismatch")
        assert mismatch_hit.severity == "error"

    def test_pointer_target_missing(self, tmp_path: Path, chassis_rules) -> None:
        """Pointer declares README.es.md but the file is absent."""
        locale_rules, triad_rules = chassis_rules
        pointer_with_es = _VALID_POINTER + "- [README.es.md](README.es.md) — español\n"
        eng = _write_engagement(
            tmp_path,
            "2026-missing-target",
            {
                "README.md": pointer_with_es,
                "README.fr.md": _VALID_FR,
                "README.en.md": _VALID_EN,
            },
        )
        hits = multilingual_validator.scan_engagement(
            eng, locale_rules, triad_rules, "warning"
        )
        rule_ids = {h.rule_id for h in hits}
        assert "pointer-target-missing" in rule_ids

    def test_full_prose_readme_with_per_locale_siblings(self, tmp_path: Path, chassis_rules) -> None:
        """README.md is full prose but per-locale siblings exist; triad violation."""
        locale_rules, triad_rules = chassis_rules
        eng = _write_engagement(
            tmp_path,
            "2026-not-pointer",
            {
                "README.md": "---\nlanguage: en\n---\n\n# Full prose\n\nNot a pointer.\n",
                "README.fr.md": _VALID_FR,
                "README.en.md": _VALID_EN,
            },
        )
        hits = multilingual_validator.scan_engagement(
            eng, locale_rules, triad_rules, "warning"
        )
        rule_ids = {h.rule_id for h in hits}
        assert "readme-not-a-pointer-with-per-locale-siblings" in rule_ids

    def test_missing_readme_with_per_locale_siblings(self, tmp_path: Path, chassis_rules) -> None:
        """Per-locale siblings exist but no README.md pointer."""
        locale_rules, triad_rules = chassis_rules
        eng = _write_engagement(
            tmp_path,
            "2026-missing-readme",
            {
                "README.fr.md": _VALID_FR,
                "README.en.md": _VALID_EN,
            },
        )
        hits = multilingual_validator.scan_engagement(
            eng, locale_rules, triad_rules, "warning"
        )
        rule_ids = {h.rule_id for h in hits}
        assert "readme-missing-with-per-locale-siblings" in rule_ids

    def test_locale_frontmatter_missing_language(self, tmp_path: Path, chassis_rules) -> None:
        """README.fr.md lacks language: frontmatter when triad exists."""
        locale_rules, triad_rules = chassis_rules
        fr_no_lang = "---\nstatus: active\nrole_owner: PMO\n---\n\n# T\n"
        eng = _write_engagement(
            tmp_path,
            "2026-no-lang",
            {
                "README.md": _VALID_POINTER,
                "README.fr.md": fr_no_lang,
                "README.en.md": _VALID_EN,
            },
        )
        hits = multilingual_validator.scan_engagement(
            eng, locale_rules, triad_rules, "warning"
        )
        rule_ids = {h.rule_id for h in hits}
        assert "locale-frontmatter-missing-language" in rule_ids


# ---------------------------------------------------------------------------
# Pack override semantics
# ---------------------------------------------------------------------------


class TestPackOverrides:
    def test_strict_severity_makes_pointer_violation_error(
        self, tmp_path: Path, chassis_rules
    ) -> None:
        """default_triad_severity = error flips triad violations to error."""
        locale_rules, triad_rules = chassis_rules
        pack = BrandMultilingualPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Test",
            canonical_source_refs=("test",),
            default_triad_severity="error",
        )
        _, _, severity = multilingual_validator._apply_pack_overrides(
            locale_rules, triad_rules, pack
        )
        assert severity == "error"

    def test_disabled_locale_layer_drops_rules(self, chassis_rules) -> None:
        locale_rules, triad_rules = chassis_rules
        pack = BrandMultilingualPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Test",
            canonical_source_refs=("test",),
            layers_enabled={"locale_suffix_cohesion": False, "readme_triad_pointer": True},
        )
        loc, tri, _ = multilingual_validator._apply_pack_overrides(
            locale_rules, triad_rules, pack
        )
        assert loc == []
        assert tri == triad_rules

    def test_disabled_triad_layer_drops_rules(self, chassis_rules) -> None:
        locale_rules, triad_rules = chassis_rules
        pack = BrandMultilingualPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Test",
            canonical_source_refs=("test",),
            layers_enabled={"locale_suffix_cohesion": True, "readme_triad_pointer": False},
        )
        loc, tri, _ = multilingual_validator._apply_pack_overrides(
            locale_rules, triad_rules, pack
        )
        assert loc == locale_rules
        assert tri == []


# ---------------------------------------------------------------------------
# Engagement walking + CLI
# ---------------------------------------------------------------------------


class TestEngagementWalk:
    def test_iter_skips_underscore_folders(self, tmp_path: Path) -> None:
        (tmp_path / "_engagement-template").mkdir()
        (tmp_path / "2026-real").mkdir()
        (tmp_path / "_archive").mkdir()
        engs = multilingual_validator._iter_engagements([tmp_path])
        names = {e.name for e in engs}
        assert names == {"2026-real"}

    def test_iter_skips_files(self, tmp_path: Path) -> None:
        (tmp_path / "2026-real").mkdir()
        (tmp_path / "README.md").write_text("not an engagement", encoding="utf-8")
        engs = multilingual_validator._iter_engagements([tmp_path])
        assert len(engs) == 1


class TestCLI:
    def test_strict_empty_exits_one_when_no_engagements(self, tmp_path: Path) -> None:
        rc = multilingual_validator.main(
            [
                "--engagement-root",
                str(tmp_path),
                "--strict-empty",
            ]
        )
        assert rc == 1

    def test_empty_root_passes_without_strict(self, tmp_path: Path) -> None:
        rc = multilingual_validator.main(
            [
                "--engagement-root",
                str(tmp_path),
            ]
        )
        assert rc == 0

    def test_clean_fixture_passes(self, tmp_path: Path) -> None:
        eng = _write_engagement(
            tmp_path,
            "2026-clean",
            {
                "README.md": _VALID_POINTER,
                "README.fr.md": _VALID_FR,
                "README.en.md": _VALID_EN,
            },
        )
        rc = multilingual_validator.main(
            [
                "--engagement-root",
                str(tmp_path),
            ]
        )
        assert rc == 0

    def test_mismatch_fixture_fails(self, tmp_path: Path) -> None:
        bad_fr = _VALID_FR.replace("language: fr", "language: en")
        _write_engagement(
            tmp_path,
            "2026-mismatch",
            {
                "README.md": _VALID_POINTER,
                "README.fr.md": bad_fr,
                "README.en.md": _VALID_EN,
            },
        )
        rc = multilingual_validator.main(
            [
                "--engagement-root",
                str(tmp_path),
            ]
        )
        assert rc == 1
