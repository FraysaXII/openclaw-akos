"""Tests for the I71 P2 Pack A2 brand Gantt confidence validator.

Covers:

- ``akos/brand_voice_register.py`` Pack A2 chassis additions: ``GanttConfidenceRule``
  (with cross-field ``label_matches_band`` model_validator), ``AudienceQuadrantRule``,
  ``BrandGanttPack``.
- Parser helpers: ``parse_gantt_confidence_rules``, ``parse_audience_quadrant_rules``,
  ``parse_gantt_pack_yaml``.
- ``scripts/validate_brand_gantt_confidence.py``: frontmatter parser, surface-class
  detection, three detection classes (band invalid; variant-quadrant mismatch;
  confidence inflation), pack-override semantics, empty-roots + --strict-empty.

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
    AudienceQuadrantRule,
    BrandGanttPack,
    GanttConfidenceRule,
    parse_audience_quadrant_rules,
    parse_gantt_confidence_rules,
    parse_gantt_pack_yaml,
)

import scripts.validate_brand_gantt_confidence as gantt_validator  # noqa: E402


# ---------------------------------------------------------------------------
# Chassis model tests
# ---------------------------------------------------------------------------


class TestChassisModels:
    def test_canonical_paths_carry_gantt_pack_entries(self) -> None:
        assert "gantt_pack_yaml" in CANONICAL_PATHS
        assert "gantt_discipline" in CANONICAL_PATHS

    def test_gantt_confidence_rule_accepts_matching_band_label(self) -> None:
        rule = GanttConfidenceRule(
            band=3,
            label="Posture",
            allowed_variants=("A", "C"),
            display_rule="dotted bar",
        )
        assert rule.band == 3
        assert rule.label == "Posture"
        assert rule.default_severity == "error"

    def test_gantt_confidence_rule_rejects_mismatched_band_label(self) -> None:
        with pytest.raises(ValueError, match="band 3 expects label 'Posture'"):
            GanttConfidenceRule(
                band=3,
                label="Confirmed",
                allowed_variants=("A", "C"),
                display_rule="x",
            )

    def test_gantt_confidence_rule_rejects_out_of_range_band(self) -> None:
        with pytest.raises(ValueError):
            GanttConfidenceRule(
                band=6,
                label="Confirmed",
                allowed_variants=("B",),
                display_rule="x",
            )

    def test_audience_quadrant_rule_carries_canonical_section(self) -> None:
        rule = AudienceQuadrantRule(
            variant="A",
            audience_facing="customer",
            data_maturity="low",
            forbidden_in_customer_pack=False,
            forbidden_in_operator_pack=True,
        )
        assert rule.canonical_section == "BRAND_GANTT_DISCIPLINE.md §2"
        assert rule.default_severity == "error"


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_gantt_confidence_rules_returns_five_bands(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["gantt_discipline"]
        rules = parse_gantt_confidence_rules(path)
        assert len(rules) == 5
        band_to_label = {r.band: r.label for r in rules}
        assert band_to_label == {
            1: "Reserved",
            2: "Hypothesis",
            3: "Posture",
            4: "Probable",
            5: "Confirmed",
        }

    def test_parse_gantt_confidence_rules_allowed_variants(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["gantt_discipline"]
        rules = parse_gantt_confidence_rules(path)
        by_band = {r.band: r for r in rules}
        assert by_band[1].allowed_variants == ("A",)
        assert by_band[2].allowed_variants == ("C",)
        assert by_band[3].allowed_variants == ("A", "C")
        assert by_band[4].allowed_variants == ("B",)
        assert by_band[5].allowed_variants == ("B",)

    def test_parse_gantt_confidence_rules_absent_canonical(self, tmp_path: Path) -> None:
        rules = parse_gantt_confidence_rules(tmp_path / "missing.md")
        assert rules == []

    def test_parse_audience_quadrant_rules_returns_four_quadrants(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["gantt_discipline"]
        rules = parse_audience_quadrant_rules(path)
        assert len(rules) == 4
        variants = {r.variant for r in rules}
        assert variants == {"A", "B", "C", "D"}

    def test_parse_audience_quadrant_rules_customer_constraints(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["gantt_discipline"]
        rules = parse_audience_quadrant_rules(path)
        by_variant = {r.variant: r for r in rules}
        # Customer-pack only ships A or B; C and D are forbidden.
        assert by_variant["A"].forbidden_in_customer_pack is False
        assert by_variant["B"].forbidden_in_customer_pack is False
        assert by_variant["C"].forbidden_in_customer_pack is True
        assert by_variant["D"].forbidden_in_customer_pack is True
        # Operator-internal only ships C or D; A and B are forbidden.
        assert by_variant["A"].forbidden_in_operator_pack is True
        assert by_variant["B"].forbidden_in_operator_pack is True
        assert by_variant["C"].forbidden_in_operator_pack is False
        assert by_variant["D"].forbidden_in_operator_pack is False

    def test_parse_gantt_pack_yaml_loads_default_pack(self) -> None:
        path = REPO_ROOT / CANONICAL_PATHS["gantt_pack_yaml"]
        pack = parse_gantt_pack_yaml(path)
        assert isinstance(pack, BrandGanttPack)
        assert pack.pack_version.startswith("v")
        assert pack.layers_enabled.get("confidence_band_validity") is True
        assert pack.gantt_confidence_rules == ()
        assert pack.audience_quadrant_rules == ()

    def test_parse_gantt_pack_yaml_absent_returns_none(self, tmp_path: Path) -> None:
        assert parse_gantt_pack_yaml(tmp_path / "missing.yml") is None


# ---------------------------------------------------------------------------
# Frontmatter + surface class
# ---------------------------------------------------------------------------


class TestFrontmatterAndSurface:
    def test_parse_frontmatter_extracts_keys(self) -> None:
        text = textwrap.dedent(
            """\
            ---
            gantt_variant: B
            confidence_band: 4
            ratify_cadence: weekly
            ---

            # Body
            """
        )
        fm = gantt_validator._parse_frontmatter(text)
        assert fm == {
            "gantt_variant": "B",
            "confidence_band": "4",
            "ratify_cadence": "weekly",
        }

    def test_parse_frontmatter_handles_missing_block(self) -> None:
        text = "# No frontmatter here\n"
        assert gantt_validator._parse_frontmatter(text) == {}

    def test_surface_class_customer(self, tmp_path: Path) -> None:
        path = tmp_path / "Clients" / "2026-x" / "02-customer-pack" / "gantt.customer.fr.md"
        assert gantt_validator._surface_class(path) == "customer"

    def test_surface_class_operator(self, tmp_path: Path) -> None:
        path = tmp_path / "Clients" / "2026-x" / "01-operator-pack" / "gantt.operator.md"
        assert gantt_validator._surface_class(path) == "operator"

    def test_surface_class_unknown(self, tmp_path: Path) -> None:
        path = tmp_path / "random" / "gantt.md"
        assert gantt_validator._surface_class(path) == "unknown"


# ---------------------------------------------------------------------------
# Detection classes (synthetic fixtures)
# ---------------------------------------------------------------------------


def _write_gantt(
    root: Path,
    surface_subpath: str,
    frontmatter: dict[str, str] | None,
    filename: str = "gantt.customer.fr.md",
) -> Path:
    folder = root / surface_subpath
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / filename
    if frontmatter is None:
        file_path.write_text("# No frontmatter\n", encoding="utf-8")
        return file_path
    lines = ["---"]
    for k, v in frontmatter.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append("# Body")
    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return file_path


@pytest.fixture()
def chassis_rules():
    canonical = REPO_ROOT / CANONICAL_PATHS["gantt_discipline"]
    return (
        parse_gantt_confidence_rules(canonical),
        parse_audience_quadrant_rules(canonical),
    )


class TestDetectionClasses:
    def test_valid_variant_b_high_confidence_passes(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"gantt_variant": "B", "confidence_band": "4", "ratify_cadence": "weekly"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        assert hits == []

    def test_missing_frontmatter_emits_error(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            None,
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        assert len(hits) == 1
        assert hits[0].rule_id == "frontmatter-missing"
        assert hits[0].severity == "error"

    def test_band_out_of_ladder(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"gantt_variant": "B", "confidence_band": "7"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "confidence-band-out-of-ladder" in rule_ids

    def test_band_non_integer(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"gantt_variant": "B", "confidence_band": "high"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "confidence-band-non-integer" in rule_ids

    def test_band_missing(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"gantt_variant": "B"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "confidence-band-missing" in rule_ids

    def test_variant_missing(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"confidence_band": "4"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "variant-missing" in rule_ids

    def test_variant_invalid(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"gantt_variant": "X", "confidence_band": "4"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "variant-invalid" in rule_ids

    def test_variant_d_in_customer_pack_fails(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"gantt_variant": "D", "confidence_band": "4"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "variant-quadrant-mismatch" in rule_ids

    def test_variant_a_in_operator_pack_fails(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/01-operator-pack",
            {"gantt_variant": "A", "confidence_band": "1"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "variant-quadrant-mismatch" in rule_ids

    def test_confidence_inflation_variant_a_band_5(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"gantt_variant": "A", "confidence_band": "5"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "confidence-inflation" in rule_ids

    def test_confidence_inflation_variant_c_band_5(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/01-operator-pack",
            {"gantt_variant": "C", "confidence_band": "5"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        rule_ids = {h.rule_id for h in hits}
        assert "confidence-inflation" in rule_ids

    def test_valid_variant_a_posture_passes(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/02-customer-pack",
            {"gantt_variant": "A", "confidence_band": "3", "ratify_cadence": "discovery_week_1"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        assert hits == []

    def test_valid_variant_c_hypothesis_passes(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        path = _write_gantt(
            tmp_path,
            "Clients/2026-x/01-operator-pack",
            {"gantt_variant": "C", "confidence_band": "2"},
        )
        hits = gantt_validator.scan_gantt_file(path, conf_rules, quad_rules)
        assert hits == []


# ---------------------------------------------------------------------------
# Pack override semantics
# ---------------------------------------------------------------------------


class TestPackOverrides:
    def test_disabled_layer_drops_confidence_rules(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        pack = BrandGanttPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Test",
            canonical_source_refs=("test",),
            layers_enabled={"confidence_band_validity": False, "variant_quadrant_consistency": True},
        )
        conf, quad = gantt_validator._apply_pack_overrides(conf_rules, quad_rules, pack)
        assert conf == []
        assert quad == quad_rules

    def test_disabled_layer_drops_quadrant_rules(self, tmp_path: Path, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        pack = BrandGanttPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Test",
            canonical_source_refs=("test",),
            layers_enabled={"confidence_band_validity": True, "variant_quadrant_consistency": False},
        )
        conf, quad = gantt_validator._apply_pack_overrides(conf_rules, quad_rules, pack)
        assert conf == conf_rules
        assert quad == []

    def test_pack_extra_rules_appended(self, chassis_rules) -> None:
        conf_rules, quad_rules = chassis_rules
        extra_quadrant = AudienceQuadrantRule(
            variant="A",
            audience_facing="customer",
            data_maturity="low",
            forbidden_in_customer_pack=False,
            forbidden_in_operator_pack=True,
            default_severity="warning",
        )
        pack = BrandGanttPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Test",
            canonical_source_refs=("test",),
            layers_enabled={},
            audience_quadrant_rules=(extra_quadrant,),
        )
        _, quad = gantt_validator._apply_pack_overrides(conf_rules, quad_rules, pack)
        assert len(quad) == len(quad_rules) + 1
        assert quad[-1].default_severity == "warning"


# ---------------------------------------------------------------------------
# End-to-end CLI
# ---------------------------------------------------------------------------


class TestCLI:
    def test_strict_empty_exits_one_when_no_files(self, tmp_path: Path) -> None:
        rc = gantt_validator.main(
            [
                "--engagement-root",
                str(tmp_path),
                "--strict-empty",
            ]
        )
        assert rc == 1

    def test_empty_roots_pass_without_strict(self, tmp_path: Path) -> None:
        rc = gantt_validator.main(
            [
                "--engagement-root",
                str(tmp_path),
            ]
        )
        assert rc == 0

    def test_clean_fixture_passes(self, tmp_path: Path) -> None:
        _write_gantt(
            tmp_path,
            "Clients/2026-clean/02-customer-pack",
            {"gantt_variant": "B", "confidence_band": "4", "ratify_cadence": "weekly"},
            filename="gantt.customer.fr.md",
        )
        rc = gantt_validator.main(
            [
                "--engagement-root",
                str(tmp_path),
            ]
        )
        assert rc == 0

    def test_inflation_fixture_fails(self, tmp_path: Path) -> None:
        _write_gantt(
            tmp_path,
            "Clients/2026-bad/02-customer-pack",
            {"gantt_variant": "A", "confidence_band": "5"},
            filename="gantt.customer.fr.md",
        )
        rc = gantt_validator.main(
            [
                "--engagement-root",
                str(tmp_path),
            ]
        )
        assert rc == 1
