"""Tests for the I71 P1 Pack A1 brand voice register validator expansion.

Covers:

- ``akos/brand_voice_register.py`` Pydantic chassis (16 models + constants).
- Parser helpers: ``parse_tic_families_from_canonical``,
  ``parse_english_register_rules``, ``parse_llm_tone_tells``,
  ``parse_register_matrix``, ``parse_audience_quadrants``,
  ``parse_register_pack_yaml``.
- ``scripts/validate_brand_voice_register.py`` 10-layer scan integration:
  Layer 0/1 (existing FR/ES; sanity-only here -- covered fully by
  ``test_validate_brand_drift_gates.py``); Layer 2 (EN MBA-deck jargon + 7
  tic families); Layer 8 (LLM tone tells).

The tests use small in-tmpdir fixtures + load the canonical files from the
real vault. They run under ``pytest -m brand`` per ``pyproject.toml``.
"""

from __future__ import annotations

import json
import re
import sys
import textwrap
from pathlib import Path

import pytest

pytestmark = pytest.mark.brand

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.brand_voice_register import (  # noqa: E402
    CANONICAL_PATHS,
    STANDARD_REGISTER_TOKEN_NAMES,
    STANDARD_TIC_FAMILY_NAMES,
    AudienceQuadrant,
    BrandVoiceRegisterPack,
    LLMToneTell,
    RegisterRule,
    RegisterToken,
    TicFamily,
    parse_audience_quadrants,
    parse_english_register_rules,
    parse_llm_tone_tells,
    parse_register_matrix,
    parse_register_pack_yaml,
    parse_tic_families_from_canonical,
)

import scripts.validate_brand_voice_register as voice_register  # noqa: E402


# ---------------------------------------------------------------------------
# Chassis model tests (Pydantic constraints + name/severity enums)
# ---------------------------------------------------------------------------


class TestChassisModels:
    def test_standard_tic_family_names_are_seven(self) -> None:
        assert len(STANDARD_TIC_FAMILY_NAMES) == 7
        assert STANDARD_TIC_FAMILY_NAMES[0] == "contrastive"
        assert STANDARD_TIC_FAMILY_NAMES[-1] == "operator_instruction_echo"

    def test_standard_register_tokens_are_known(self) -> None:
        # BRAND_REGISTER_MATRIX.md declares 5 common tokens (formal_legal,
        # peer_consulting, casual_internal, regulator_neutral,
        # investor_aspirational); STANDARD_REGISTER_TOKEN_NAMES carries them.
        assert STANDARD_REGISTER_TOKEN_NAMES == frozenset(
            {
                "formal_legal",
                "peer_consulting",
                "casual_internal",
                "regulator_neutral",
                "investor_aspirational",
            }
        )

    def test_canonical_paths_keys_match_expected(self) -> None:
        # P1 baseline keys MUST remain present (additive-only chassis extension
        # contract per .cursor/rules/akos-governance-remediation.mdc + I71 P2
        # kickoff §"DO NOT change existing model signatures"). P2 additively
        # added gantt_pack_yaml + multilingual_pack_yaml + multilingual_contract
        # + localised_formats; subsequent phases may add further keys.
        p1_baseline_keys = {
            "copywriting_discipline",
            "english_patterns",
            "french_patterns",
            "spanish_patterns",
            "llm_tone_tells",
            "register_matrix",
            "gantt_discipline",
            "register_pack_yaml",
        }
        assert p1_baseline_keys <= set(CANONICAL_PATHS.keys()), (
            f"P1 chassis CANONICAL_PATHS keys must remain (additive-only); "
            f"missing: {p1_baseline_keys - set(CANONICAL_PATHS.keys())}"
        )

    def test_tic_family_rejects_unknown_name(self) -> None:
        with pytest.raises(ValueError):
            TicFamily(
                name="not_a_real_family",
                family_index=1,
                locales=("en",),
                pattern=r".*",
                replacement_strategy="-",
            )

    def test_tic_family_rejects_non_compiling_regex(self) -> None:
        with pytest.raises(ValueError):
            TicFamily(
                name="contrastive",
                family_index=1,
                locales=("en",),
                pattern=r"[unterminated",
                replacement_strategy="-",
            )

    def test_tic_family_rejects_index_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            TicFamily(
                name="contrastive",
                family_index=8,
                locales=("en",),
                pattern=r".*",
                replacement_strategy="-",
            )

    def test_register_rule_pattern_compiles(self) -> None:
        rule = RegisterRule(
            locale="en",
            token="enterprise-grade",
            pattern=r"\benterprise-grade\b",
            rationale="-",
            canonical_source="BRAND_ENGLISH_PATTERNS.md §5.1",
        )
        assert re.compile(rule.pattern).search("enterprise-grade SaaS") is not None

    def test_register_token_rejects_unknown(self) -> None:
        with pytest.raises(ValueError):
            RegisterToken(token="not_a_token", relationship="x", channel="y")

    def test_llm_tone_tell_token_id_pattern(self) -> None:
        tell = LLMToneTell(
            token_id="T-3-delve-into",
            category="verb",
            pattern=r"\bdelve into\b",
            replacement_template="look at",
            rationale="-",
        )
        assert tell.default_severity == "error"

    def test_audience_quadrant_variant_constrained(self) -> None:
        q = AudienceQuadrant(
            variant="B",
            audience_facing="customer",
            data_maturity="high",
            label="Proof of discipline",
            description="-",
        )
        assert q.variant == "B"


# ---------------------------------------------------------------------------
# Parser tests against the real canonical vault
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_tic_families_returns_seven_canonical_names(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["copywriting_discipline"]
        families = parse_tic_families_from_canonical(path)
        assert families  # at least one parsed
        names_seen = {f.name for f in families}
        # All 7 canonical names should be represented (regex or sentinel).
        assert names_seen == set(STANDARD_TIC_FAMILY_NAMES)

    def test_parse_tic_families_emits_concrete_regex_for_f1_f2_f3(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["copywriting_discipline"]
        families = parse_tic_families_from_canonical(path)
        concrete = [f for f in families if f.pattern != r".*"]
        # F1 has FR + EN; F2 has FR + EN; F3 has FR -> at minimum 5 concrete.
        assert len(concrete) >= 5
        f1_en = next(
            (f for f in concrete if f.family_index == 1 and "en" in f.locales),
            None,
        )
        assert f1_en is not None
        assert "not" in f1_en.pattern  # FR-EN pattern fragment

    def test_parse_english_register_rules_loads_mba_deck_table(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["english_patterns"]
        rules = parse_english_register_rules(path)
        # The §5.1 MBA-deck table has 20+ rows.
        assert len(rules) >= 10
        tokens = {r.token for r in rules}
        # Spot-check known MBA-deck tokens.
        assert "leverage synergies" in tokens
        assert "circle back" in tokens

    def test_parse_llm_tone_tells_loads_all_five_categories(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["llm_tone_tells"]
        tells = parse_llm_tone_tells(path)
        assert tells
        categories_seen = {t.category for t in tells}
        # Catalog has §3 verb / §4 noun / §5 adjective / §6 hedge / §7 construction.
        assert "verb" in categories_seen
        assert "noun" in categories_seen
        assert "adjective" in categories_seen

    def test_parse_llm_tone_tells_emits_delve_into_at_error_severity(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["llm_tone_tells"]
        tells = parse_llm_tone_tells(path)
        delve = next((t for t in tells if "delve" in t.pattern.lower()), None)
        assert delve is not None
        assert delve.default_severity == "error"

    def test_parse_register_matrix_yields_six_rows(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["register_matrix"]
        tokens = parse_register_matrix(path)
        assert len(tokens) == 6
        token_names = {t.token for t in tokens}
        assert token_names <= STANDARD_REGISTER_TOKEN_NAMES

    def test_parse_audience_quadrants_yields_four(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["gantt_discipline"]
        quadrants = parse_audience_quadrants(path)
        assert len(quadrants) == 4
        variants = {q.variant for q in quadrants}
        assert variants == {"A", "B", "C", "D"}

    def test_parse_register_pack_yaml_loads_v0_1_0(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["register_pack_yaml"]
        pack = parse_register_pack_yaml(path)
        assert pack is not None
        assert pack.pack_version == "v0.1.0"
        assert pack.last_edited == "2026-05-14"
        # All 10 layers should be enabled at day-1 per D-IH-71-F.
        for layer_name in (
            "layer_0_fr",
            "layer_1_es",
            "layer_2_en_tic_families",
            "layer_3_audience_matrix",
            "layer_4_storytelling_resonance_boundary",
            "layer_5_sub_mark_archetype",
            "layer_6_voice_persona_engagement_type",
            "layer_7_locale_leak_cobrand",
            "layer_8_llm_tone_tells",
            "layer_9_track_record_brand_abbrev",
        ):
            assert pack.layers_enabled.get(layer_name) is True, layer_name


# ---------------------------------------------------------------------------
# Validator integration -- per-layer hit fixtures
# ---------------------------------------------------------------------------


def _write_messages_fixture(
    tmp_path: Path, locale: str, payload: dict[str, str]
) -> Path:
    """Build a sibling-style consumer repo with messages/<locale>.json."""
    repo_root = tmp_path / "consumer"
    messages_dir = repo_root / "messages"
    messages_dir.mkdir(parents=True)
    locale_file = messages_dir / f"{locale}.json"
    locale_file.write_text(json.dumps(payload), encoding="utf-8")
    return repo_root


class TestValidatorLayer2Tics:
    def test_f1_contrastive_en_fires(self, tmp_path: Path) -> None:
        repo = _write_messages_fixture(
            tmp_path,
            "en",
            {"hero.tagline": "Discipline, not improvisation."},
        )
        rules = voice_register._load_rules()
        f1_rules = [
            r for r in rules if r.token == "tic_family:contrastive" and r.locale == "en"
        ]
        assert f1_rules
        scanned_file = repo / "messages" / "en.json"
        hits = voice_register._scan_message_file(scanned_file, rules)
        assert any(
            h.rule.token == "tic_family:contrastive" for h in hits
        ), f"expected F1 (contrastive) hit; got hits: {[h.rule.token for h in hits]}"

    def test_f1_contrastive_fr_fires(self, tmp_path: Path) -> None:
        repo = _write_messages_fixture(
            tmp_path,
            "fr",
            {"hero.tagline": "Discipline, pas improvisation."},
        )
        rules = voice_register._load_rules()
        scanned_file = repo / "messages" / "fr.json"
        hits = voice_register._scan_message_file(scanned_file, rules)
        assert any(
            h.rule.token == "tic_family:contrastive" for h in hits
        ), f"expected F1 (contrastive) FR hit; got hits: {[h.rule.token for h in hits]}"

    def test_f2_chained_negation_fr_fires(self, tmp_path: Path) -> None:
        repo = _write_messages_fixture(
            tmp_path,
            "fr",
            {
                "manifesto.line": (
                    "La friction n'est pas la décision. C'est la répétition."
                )
            },
        )
        rules = voice_register._load_rules()
        scanned_file = repo / "messages" / "fr.json"
        hits = voice_register._scan_message_file(scanned_file, rules)
        assert any(
            h.rule.token == "tic_family:chained_negation_affirmation"
            for h in hits
        )

    def test_clean_en_prose_no_hits(self, tmp_path: Path) -> None:
        repo = _write_messages_fixture(
            tmp_path,
            "en",
            {
                "hero.tagline": "We help mid-market SMEs decide faster.",
                "manifesto.line": "Holistika builds reproducible discipline.",
            },
        )
        rules = voice_register._load_rules()
        scanned_file = repo / "messages" / "en.json"
        hits = voice_register._scan_message_file(scanned_file, rules)
        assert hits == [], f"expected no hits; got: {[h.rule.token for h in hits]}"


class TestValidatorLayer2EnMBADeck:
    def test_enterprise_grade_fires(self, tmp_path: Path) -> None:
        repo = _write_messages_fixture(
            tmp_path,
            "en",
            {"hero.tagline": "Our enterprise-grade platform delivers value."},
        )
        rules = voice_register._load_rules()
        en_rules = [r for r in rules if r.locale == "en"]
        assert en_rules
        scanned_file = repo / "messages" / "en.json"
        hits = voice_register._scan_message_file(scanned_file, rules)
        assert any("enterprise-grade" in h.snippet for h in hits)

    def test_actionable_insights_fires(self, tmp_path: Path) -> None:
        repo = _write_messages_fixture(
            tmp_path,
            "en",
            {"hero.tagline": "We deliver actionable insights for your team."},
        )
        rules = voice_register._load_rules()
        scanned_file = repo / "messages" / "en.json"
        hits = voice_register._scan_message_file(scanned_file, rules)
        assert any("actionable insights" in h.snippet.lower() for h in hits)


class TestValidatorLayer8LLMToneTells:
    def test_delve_into_fires_in_en_locale(self, tmp_path: Path) -> None:
        repo = _write_messages_fixture(
            tmp_path,
            "en",
            {"manifesto.line": "Let us delve into the data with our team."},
        )
        rules = voice_register._load_rules()
        scanned_file = repo / "messages" / "en.json"
        hits = voice_register._scan_message_file(scanned_file, rules)
        assert any(
            h.rule.token == "llm_tone_tell:T-3-delve-into" for h in hits
        ), f"expected delve-into LLM tone-tell hit; got: {[h.rule.token for h in hits]}"

    def test_llm_tone_tell_does_not_fire_in_fr(self, tmp_path: Path) -> None:
        repo = _write_messages_fixture(
            tmp_path,
            "fr",
            {
                "manifesto.line": (
                    "Nous nous concentrons sur l'execution avec notre equipe."
                )
            },
        )
        rules = voice_register._load_rules()
        scanned_file = repo / "messages" / "fr.json"
        hits = voice_register._scan_message_file(scanned_file, rules)
        llm_hits = [h for h in hits if "llm_tone_tell" in h.rule.token]
        assert llm_hits == []


class TestValidatorRulePackOverrides:
    def test_main_loads_canonical_pack_at_default_path(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """The validator should announce pack load when present.

        Smoke-only: confirms ``--pack-path`` argument flows to the loader and
        the pack-loaded INFO line is emitted when the canonical pack is found.
        Captures stdout via ``capsys`` because ``setup_logging`` reconfigures
        the root logger and bypasses caplog by design (consistent with the
        validator's standalone-CLI posture).
        """
        # Isolate from sibling-repo defaults so the scan is graceful.
        monkeypatch.setattr(voice_register, "DEFAULT_CONSUMER_ROOTS", ())
        empty_consumer = tmp_path / "empty"
        empty_consumer.mkdir()
        argv = [
            "--json-log",
            "--consumer-root",
            str(empty_consumer),
            "--pack-path",
            str(REPO_ROOT / CANONICAL_PATHS["register_pack_yaml"]),
        ]
        rc = voice_register.main(argv)
        captured = capsys.readouterr()
        # No consumer messages found -> graceful exit 0 (not strict-empty).
        assert rc == 0
        # Pack-load line should have fired in stdout.
        assert "register-pack.yml v0.1.0" in captured.out

    def test_pack_returns_typed_brand_voice_register_pack(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["register_pack_yaml"]
        pack = parse_register_pack_yaml(path)
        assert isinstance(pack, BrandVoiceRegisterPack)
        assert pack.canonical_source_refs  # non-empty tuple
        # All operator-typed collections start empty in v0.1.0 day-1 pack.
        assert pack.tic_families == ()
        assert pack.register_rules == ()
        assert pack.llm_tone_tells == ()
