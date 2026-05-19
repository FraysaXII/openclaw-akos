"""Tests for ``akos/hlk_operator_voice.py`` per I76 P3 Lane C.

PROSE-FIRST canonical mint per operator ratify 2026-05-19 21:00 (`D-IH-76-G`
through `D-IH-76-M`). These tests lock the Pydantic chassis:

- 9-trait closed vocabulary per `D-IH-76-H` (5 founder + 4 system-owner).
- 3-class v1 audience-constraint set per `D-IH-76-I` (J-OP / J-AD-post-NDA / J-CO).
- Anti-sycophancy threshold defaults to 3 (`D-IH-76-J`).
- Knowledge-test cadence defaults to 90 days quarterly (`D-IH-76-L`).
- 2 seed profiles in ``STANDARD_VOICE_PROFILES`` (founder + system_owner).
- Frozen model contract (mutation raises).
- Methodology version pattern (^v\\d+\\.\\d+$).
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from akos.hlk_operator_voice import (
    FOUNDER_TRAITS,
    OperatorVoiceProfile,
    STANDARD_AUDIENCE_CONSTRAINTS,
    STANDARD_TRAIT_VOCABULARY,
    STANDARD_VOICE_PROFILES,
    SYSTEM_OWNER_TRAITS,
    get_profile,
)

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Closed vocabulary contract (D-IH-76-H)
# ---------------------------------------------------------------------------


class TestStandardTraitVocabulary:
    def test_vocabulary_size_is_exactly_9(self) -> None:
        """D-IH-76-H ratify: 9 traits, closed at v1."""
        assert len(STANDARD_TRAIT_VOCABULARY) == 9

    def test_vocabulary_is_frozenset(self) -> None:
        assert isinstance(STANDARD_TRAIT_VOCABULARY, frozenset)

    def test_vocabulary_contains_all_5_founder_traits(self) -> None:
        for trait in FOUNDER_TRAITS:
            assert trait in STANDARD_TRAIT_VOCABULARY

    def test_vocabulary_contains_all_4_system_owner_traits(self) -> None:
        for trait in SYSTEM_OWNER_TRAITS:
            assert trait in STANDARD_TRAIT_VOCABULARY

    def test_founder_traits_tuple_length_is_5(self) -> None:
        assert len(FOUNDER_TRAITS) == 5

    def test_system_owner_traits_tuple_length_is_4(self) -> None:
        assert len(SYSTEM_OWNER_TRAITS) == 4

    def test_no_trait_overlap_between_founder_and_system_owner(self) -> None:
        """5 + 4 = 9 distinct traits per D-IH-76-H closure."""
        assert set(FOUNDER_TRAITS).isdisjoint(set(SYSTEM_OWNER_TRAITS))

    def test_specific_traits_present(self) -> None:
        """Spot-check the exact trait labels operator ratified per D-IH-76-H."""
        expected = {
            "methodology-checkpoint-explicit",
            "cite-by-file-path-and-line",
            "numbered-explicit-lists",
            "multilingual-en-fr-es",
            "lowercase-casual",
            "validator-first",
            "evidence-citation-required",
            "decision-id-explicit",
            "pause-point-conscious",
        }
        assert STANDARD_TRAIT_VOCABULARY == frozenset(expected)


# ---------------------------------------------------------------------------
# Audience-constraint v1 set (D-IH-76-I)
# ---------------------------------------------------------------------------


class TestStandardAudienceConstraints:
    def test_v1_set_size_is_3(self) -> None:
        assert len(STANDARD_AUDIENCE_CONSTRAINTS) == 3

    def test_v1_set_is_frozenset(self) -> None:
        assert isinstance(STANDARD_AUDIENCE_CONSTRAINTS, frozenset)

    def test_v1_set_exact_membership(self) -> None:
        """D-IH-76-I ratify: J-OP / J-AD-post-NDA / J-CO."""
        assert STANDARD_AUDIENCE_CONSTRAINTS == frozenset(
            {"J-OP", "J-AD-post-NDA", "J-CO"}
        )


# ---------------------------------------------------------------------------
# OperatorVoiceProfile chassis enforcement
# ---------------------------------------------------------------------------


def _make_valid_profile(**overrides: object) -> OperatorVoiceProfile:
    base = dict(
        profile_id="voice_akos_test_2026",
        profile_name="Test Voice 2026",
        description="Test profile.",
        traits=("methodology-checkpoint-explicit",),
        audience_constraint=("J-OP",),
        corpus_paths=("docs/test/path.md",),
        methodology_version="v3.1",
    )
    base.update(overrides)
    return OperatorVoiceProfile(**base)  # type: ignore[arg-type]


class TestProfileIdPattern:
    def test_valid_profile_id_lower_snake(self) -> None:
        p = _make_valid_profile(profile_id="voice_akos_founder_2026")
        assert p.profile_id == "voice_akos_founder_2026"

    def test_invalid_profile_id_missing_voice_prefix(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(profile_id="akos_founder_2026")

    def test_invalid_profile_id_uppercase(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(profile_id="voice_AKOS_2026")

    def test_invalid_profile_id_with_dash(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(profile_id="voice-akos-2026")


class TestTraitsField:
    def test_traits_non_empty_required(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(traits=())

    def test_traits_subset_of_vocabulary_enforced(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(traits=("not-a-real-trait",))  # type: ignore[arg-type]

    def test_traits_duplicate_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(
                traits=("validator-first", "validator-first")
            )

    def test_traits_accepts_multiple_valid_traits(self) -> None:
        p = _make_valid_profile(
            traits=(
                "validator-first",
                "decision-id-explicit",
                "pause-point-conscious",
            )
        )
        assert len(p.traits) == 3


class TestAudienceConstraintField:
    def test_audience_non_empty_required(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(audience_constraint=())

    def test_audience_subset_of_v1_set_enforced(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(audience_constraint=("J-IN",))  # type: ignore[arg-type]

    def test_audience_duplicate_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(audience_constraint=("J-OP", "J-OP"))

    def test_audience_accepts_full_v1_set(self) -> None:
        p = _make_valid_profile(
            audience_constraint=("J-OP", "J-AD-post-NDA", "J-CO")
        )
        assert len(p.audience_constraint) == 3


class TestAntiSycophancyThreshold:
    def test_default_threshold_is_3(self) -> None:
        """D-IH-76-J: 3 consecutive agreement turns triggers friction."""
        p = _make_valid_profile()
        assert p.anti_sycophancy_threshold == 3

    def test_threshold_zero_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(anti_sycophancy_threshold=0)

    def test_threshold_negative_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(anti_sycophancy_threshold=-1)

    def test_custom_threshold_accepted(self) -> None:
        p = _make_valid_profile(anti_sycophancy_threshold=5)
        assert p.anti_sycophancy_threshold == 5


class TestKnowledgeTestCadenceDays:
    def test_default_cadence_is_90_days(self) -> None:
        """D-IH-76-L: quarterly = 90 days default."""
        p = _make_valid_profile()
        assert p.knowledge_test_cadence_days == 90

    def test_cadence_below_30_days_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(knowledge_test_cadence_days=7)

    def test_cadence_30_days_accepted_boundary(self) -> None:
        p = _make_valid_profile(knowledge_test_cadence_days=30)
        assert p.knowledge_test_cadence_days == 30

    def test_cadence_180_days_accepted(self) -> None:
        p = _make_valid_profile(knowledge_test_cadence_days=180)
        assert p.knowledge_test_cadence_days == 180


class TestMethodologyVersionPattern:
    def test_v3_dot_1_accepted(self) -> None:
        p = _make_valid_profile(methodology_version="v3.1")
        assert p.methodology_version == "v3.1"

    def test_v3_alone_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(methodology_version="v3")

    def test_bare_3_dot_1_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(methodology_version="3.1")

    def test_v10_dot_25_accepted(self) -> None:
        """Pattern supports multi-digit major+minor."""
        p = _make_valid_profile(methodology_version="v10.25")
        assert p.methodology_version == "v10.25"


class TestCorpusPathsField:
    def test_corpus_paths_non_empty_required(self) -> None:
        with pytest.raises(ValidationError):
            _make_valid_profile(corpus_paths=())

    def test_corpus_paths_accepts_multiple(self) -> None:
        p = _make_valid_profile(
            corpus_paths=("docs/a.md", "docs/b.md")
        )
        assert len(p.corpus_paths) == 2


class TestFrozenContract:
    def test_mutation_raises(self) -> None:
        """frozen=True per CONTRIBUTING.md — direct attribute set raises."""
        p = _make_valid_profile()
        with pytest.raises((ValidationError, AttributeError, TypeError)):
            p.profile_id = "voice_changed"  # type: ignore[misc]

    def test_extra_field_forbidden(self) -> None:
        """extra=forbid per CONTRIBUTING.md."""
        with pytest.raises(ValidationError):
            OperatorVoiceProfile(
                profile_id="voice_akos_test_2026",
                profile_name="Test",
                description="Test.",
                traits=("validator-first",),
                audience_constraint=("J-OP",),
                corpus_paths=("docs/test.md",),
                methodology_version="v3.1",
                unknown_field="rogue",  # type: ignore[call-arg]
            )


# ---------------------------------------------------------------------------
# STANDARD_VOICE_PROFILES seed contract
# ---------------------------------------------------------------------------


class TestStandardVoiceProfiles:
    def test_dict_contains_founder_profile(self) -> None:
        assert "voice_akos_founder_2026" in STANDARD_VOICE_PROFILES

    def test_dict_contains_system_owner_profile(self) -> None:
        assert "voice_akos_system_owner_2026" in STANDARD_VOICE_PROFILES

    def test_dict_size_is_2_at_v1(self) -> None:
        """v1 = 2 seed profiles per D-IH-76-G PROSE-FIRST mint."""
        assert len(STANDARD_VOICE_PROFILES) == 2

    def test_each_profile_round_trips(self) -> None:
        """Each seed profile validates against the model."""
        for profile_id, profile in STANDARD_VOICE_PROFILES.items():
            assert isinstance(profile, OperatorVoiceProfile)
            assert profile.profile_id == profile_id


class TestFounderProfileShape:
    def test_founder_has_all_5_founder_traits(self) -> None:
        p = STANDARD_VOICE_PROFILES["voice_akos_founder_2026"]
        for trait in FOUNDER_TRAITS:
            assert trait in p.traits

    def test_founder_audience_is_full_v1_set(self) -> None:
        p = STANDARD_VOICE_PROFILES["voice_akos_founder_2026"]
        assert set(p.audience_constraint) == {"J-OP", "J-AD-post-NDA", "J-CO"}

    def test_founder_methodology_version_v3_1(self) -> None:
        p = STANDARD_VOICE_PROFILES["voice_akos_founder_2026"]
        assert p.methodology_version == "v3.1"

    def test_founder_default_threshold_3(self) -> None:
        p = STANDARD_VOICE_PROFILES["voice_akos_founder_2026"]
        assert p.anti_sycophancy_threshold == 3

    def test_founder_default_cadence_90(self) -> None:
        p = STANDARD_VOICE_PROFILES["voice_akos_founder_2026"]
        assert p.knowledge_test_cadence_days == 90


class TestSystemOwnerProfileShape:
    def test_system_owner_has_all_4_system_owner_traits(self) -> None:
        p = STANDARD_VOICE_PROFILES["voice_akos_system_owner_2026"]
        for trait in SYSTEM_OWNER_TRAITS:
            assert trait in p.traits

    def test_system_owner_shares_cite_by_file_path_and_line(self) -> None:
        """System Owner inherits the shared 'cite-by-file-path-and-line' trait."""
        p = STANDARD_VOICE_PROFILES["voice_akos_system_owner_2026"]
        assert "cite-by-file-path-and-line" in p.traits

    def test_system_owner_audience_is_j_op_only(self) -> None:
        p = STANDARD_VOICE_PROFILES["voice_akos_system_owner_2026"]
        assert set(p.audience_constraint) == {"J-OP"}

    def test_system_owner_total_trait_count_is_5(self) -> None:
        """4 system-owner traits + 1 shared = 5 total."""
        p = STANDARD_VOICE_PROFILES["voice_akos_system_owner_2026"]
        assert len(p.traits) == 5


# ---------------------------------------------------------------------------
# get_profile helper
# ---------------------------------------------------------------------------


class TestGetProfile:
    def test_get_profile_returns_founder(self) -> None:
        p = get_profile("voice_akos_founder_2026")
        assert p.profile_id == "voice_akos_founder_2026"

    def test_get_profile_returns_system_owner(self) -> None:
        p = get_profile("voice_akos_system_owner_2026")
        assert p.profile_id == "voice_akos_system_owner_2026"

    def test_get_profile_unknown_raises_keyerror(self) -> None:
        with pytest.raises(KeyError):
            get_profile("voice_unknown_xxx")
