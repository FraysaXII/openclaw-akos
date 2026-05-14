"""Tests for I71 P5 Pack A4 — render-pipeline ownership coverage validator.

Covers:
- Chassis Pydantic model validation (RenderOwnershipRule + RenderOwnershipPack).
- Parser correctness (9 canonical rules from WORKSPACE_BLUEPRINT_HOLISTIKA.md §16).
- Engagement-folder walking (synthetic fixtures via tmp_path).
- Detection classes (mismatch / undeclared / transition-trigger advisory).
- Pack override semantics (rule replacement, transition-hint surfacing,
  layer disabling).
- CLI behavior (strict-empty + empty-roots; argument parsing).

Marker: ``brand`` (registered in pyproject.toml at I71 P1; folds Pack A4 into
the existing brand validator-pack family for `pytest -m brand` runs).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from akos.brand_voice_register import (  # noqa: E402
    RenderOwnershipPack,
    RenderOwnershipRule,
    STANDARD_DELIVERABLE_KINDS,
    parse_render_ownership_pack_yaml,
    parse_render_ownership_rules,
)

from scripts.validate_render_ownership import (  # noqa: E402
    PMO_TO_REVOPS_THRESHOLD,
    _aggregate_transition_hints,
    _apply_pack_overrides,
    _find_deliverable_files,
    _iter_engagements,
    _parse_frontmatter,
    main as validator_main,
    scan_engagement,
)


pytestmark = pytest.mark.brand


WORKSPACE_BLUEPRINT_PATH = (
    ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Operations"
    / "PMO"
    / "canonicals"
    / "WORKSPACE_BLUEPRINT_HOLISTIKA.md"
)


# -----------------------------------------------------------------------------
# Chassis model validation
# -----------------------------------------------------------------------------


class TestRenderOwnershipRuleModel:
    def test_minimal_valid_construction(self) -> None:
        rule = RenderOwnershipRule(
            deliverable_kind="deck",
            expected_role_owner="Copywriter",
            surface_pattern="02-customer-pack/deck.customer.*.md",
        )
        assert rule.deliverable_kind == "deck"
        assert rule.expected_role_owner == "Copywriter"
        assert rule.default_severity == "warning"
        assert rule.canonical_section == "WORKSPACE_BLUEPRINT_HOLISTIKA.md §16"

    def test_severity_promotion_to_error(self) -> None:
        rule = RenderOwnershipRule(
            deliverable_kind="gantt",
            expected_role_owner="UX Designer",
            surface_pattern="02-customer-pack/gantt.*.md",
            default_severity="error",
        )
        assert rule.default_severity == "error"

    def test_invalid_deliverable_kind_rejected(self) -> None:
        with pytest.raises(ValidationError):
            RenderOwnershipRule(
                deliverable_kind="newsletter",  # type: ignore[arg-type]
                expected_role_owner="Copywriter",
                surface_pattern="02-customer-pack/*.md",
            )

    def test_empty_role_owner_rejected(self) -> None:
        with pytest.raises(ValidationError):
            RenderOwnershipRule(
                deliverable_kind="deck",
                expected_role_owner="",
                surface_pattern="02-customer-pack/deck.customer.*.md",
            )

    def test_frozen_model_immutable(self) -> None:
        rule = RenderOwnershipRule(
            deliverable_kind="proposal",
            expected_role_owner="PMO",
            surface_pattern="02-customer-pack/proposal.*.md",
        )
        with pytest.raises(ValidationError):
            rule.expected_role_owner = "Brand Manager"  # type: ignore[misc]


class TestRenderOwnershipPackModel:
    def _minimal_kwargs(self) -> dict:
        return {
            "pack_version": "v0.1.0",
            "last_edited": "2026-05-14",
            "last_edited_by": "Founder",
            "canonical_source_refs": ("WORKSPACE_BLUEPRINT_HOLISTIKA.md §16",),
        }

    def test_minimal_valid_construction(self) -> None:
        pack = RenderOwnershipPack(**self._minimal_kwargs())
        assert pack.pack_version == "v0.1.0"
        assert pack.render_ownership_rules == ()
        assert pack.transition_trigger_hints == ()

    def test_invalid_pack_version_rejected(self) -> None:
        kwargs = self._minimal_kwargs()
        kwargs["pack_version"] = "0.1.0"
        with pytest.raises(ValidationError):
            RenderOwnershipPack(**kwargs)

    def test_invalid_last_edited_rejected(self) -> None:
        kwargs = self._minimal_kwargs()
        kwargs["last_edited"] = "May 14, 2026"
        with pytest.raises(ValidationError):
            RenderOwnershipPack(**kwargs)

    def test_pack_with_override_rules(self) -> None:
        override = RenderOwnershipRule(
            deliverable_kind="deck",
            expected_role_owner="Brand Manager",
            surface_pattern="02-customer-pack/deck.customer.*.md",
            default_severity="error",
        )
        kwargs = self._minimal_kwargs()
        kwargs["render_ownership_rules"] = (override,)
        kwargs["transition_trigger_hints"] = ("PMO -> RevOps test hint",)
        pack = RenderOwnershipPack(**kwargs)
        assert len(pack.render_ownership_rules) == 1
        assert pack.render_ownership_rules[0].default_severity == "error"
        assert pack.transition_trigger_hints == ("PMO -> RevOps test hint",)


# -----------------------------------------------------------------------------
# Parser correctness
# -----------------------------------------------------------------------------


class TestParser:
    def test_parser_emits_nine_canonical_rules(self) -> None:
        rules = parse_render_ownership_rules(WORKSPACE_BLUEPRINT_PATH)
        assert len(rules) == 9
        kinds = {r.deliverable_kind for r in rules}
        assert kinds == set(STANDARD_DELIVERABLE_KINDS)

    def test_parser_returns_empty_on_missing_canonical(self, tmp_path: Path) -> None:
        rules = parse_render_ownership_rules(tmp_path / "nonexistent.md")
        assert rules == []

    def test_parser_role_owner_mapping(self) -> None:
        rules = parse_render_ownership_rules(WORKSPACE_BLUEPRINT_PATH)
        by_kind = {r.deliverable_kind: r for r in rules}
        # Canonical §16.1 deliverable -> role_owner assignment
        assert by_kind["deck"].expected_role_owner == "Copywriter"
        assert by_kind["proposal"].expected_role_owner == "PMO"
        assert by_kind["tarification"].expected_role_owner == "PMO"
        assert by_kind["gantt"].expected_role_owner == "UX Designer"
        assert by_kind["dossier"].expected_role_owner == "PMO"
        assert by_kind["counterparty_brief"].expected_role_owner == "Copywriter"
        assert by_kind["objections"].expected_role_owner == "Account Manager"
        assert by_kind["press"].expected_role_owner == "Storytelling Manager"
        assert by_kind["advisor_email"].expected_role_owner == "PMO"

    def test_parser_surface_patterns_are_engagement_relative(self) -> None:
        rules = parse_render_ownership_rules(WORKSPACE_BLUEPRINT_PATH)
        for rule in rules:
            assert rule.surface_pattern.endswith(".md"), rule
            assert not rule.surface_pattern.startswith("/"), rule

    def test_pack_yaml_returns_none_when_absent(self, tmp_path: Path) -> None:
        assert parse_render_ownership_pack_yaml(tmp_path / "absent.yml") is None

    def test_pack_yaml_parses_canonical_pack(self) -> None:
        pack_path = (
            ROOT
            / "docs"
            / "references"
            / "hlk"
            / "v3.0"
            / "Admin"
            / "O5-1"
            / "Marketing"
            / "Brand"
            / "canonicals"
            / "_validators"
            / "render-ownership-pack.yml"
        )
        pack = parse_render_ownership_pack_yaml(pack_path)
        assert pack is not None
        assert pack.pack_version == "v0.1.0"
        assert pack.last_edited_by == "Founder"
        assert pack.layers_enabled.get("render_ownership_coverage") is True


# -----------------------------------------------------------------------------
# Frontmatter parsing
# -----------------------------------------------------------------------------


class TestFrontmatter:
    def test_parse_empty_returns_empty_dict(self) -> None:
        assert _parse_frontmatter("plain body no frontmatter") == {}

    def test_parse_simple_frontmatter(self) -> None:
        text = "---\nrole_owner: Copywriter\nlanguage: fr\n---\nbody\n"
        fm = _parse_frontmatter(text)
        assert fm == {"role_owner": "Copywriter", "language": "fr"}

    def test_parse_strips_quotes(self) -> None:
        text = "---\nrole_owner: 'PMO'\n---\n"
        assert _parse_frontmatter(text)["role_owner"] == "PMO"

    def test_parse_skips_comments_and_blanks(self) -> None:
        text = "---\n# comment\nrole_owner: PMO\n\nlanguage: en\n---\n"
        fm = _parse_frontmatter(text)
        assert fm == {"role_owner": "PMO", "language": "en"}


# -----------------------------------------------------------------------------
# Engagement walking + deliverable discovery
# -----------------------------------------------------------------------------


def _make_engagement(root: Path, name: str) -> Path:
    eng = root / name
    eng.mkdir(parents=True, exist_ok=True)
    (eng / "02-customer-pack").mkdir(exist_ok=True)
    (eng / "01-operator-pack").mkdir(exist_ok=True)
    return eng


class TestEngagementWalk:
    def test_iter_engagements_skips_underscore_prefixed(self, tmp_path: Path) -> None:
        clients = tmp_path / "Clients"
        clients.mkdir()
        _make_engagement(clients, "2026-foo")
        _make_engagement(clients, "_engagement-template")
        _make_engagement(clients, "_archive")
        engagements = _iter_engagements([clients])
        assert len(engagements) == 1
        assert engagements[0].name == "2026-foo"

    def test_iter_engagements_handles_missing_root(self, tmp_path: Path) -> None:
        assert _iter_engagements([tmp_path / "nonexistent"]) == []

    def test_find_deliverable_files_resolves_subdir_glob(self, tmp_path: Path) -> None:
        eng = _make_engagement(tmp_path, "2026-foo")
        (eng / "02-customer-pack" / "deck.customer.fr.md").write_text("---\n---\n")
        (eng / "02-customer-pack" / "deck.customer.en.md").write_text("---\n---\n")
        rule = RenderOwnershipRule(
            deliverable_kind="deck",
            expected_role_owner="Copywriter",
            surface_pattern="02-customer-pack/deck.customer.*.md",
        )
        files = _find_deliverable_files(eng, rule)
        assert {f.name for f in files} == {"deck.customer.fr.md", "deck.customer.en.md"}

    def test_find_deliverable_files_root_pattern(self, tmp_path: Path) -> None:
        eng = _make_engagement(tmp_path, "2026-foo")
        (eng / "README.md").write_text("---\n---\n")
        (eng / "README.fr.md").write_text("---\n---\n")
        rule = RenderOwnershipRule(
            deliverable_kind="counterparty_brief",
            expected_role_owner="Copywriter",
            surface_pattern="README*.md",
        )
        files = _find_deliverable_files(eng, rule)
        assert {f.name for f in files} == {"README.md", "README.fr.md"}


# -----------------------------------------------------------------------------
# Detection classes
# -----------------------------------------------------------------------------


class TestDetection:
    def _build_canonical_rules(self) -> list[RenderOwnershipRule]:
        return parse_render_ownership_rules(WORKSPACE_BLUEPRINT_PATH)

    def test_undeclared_role_owner_emits_info(self, tmp_path: Path) -> None:
        eng = _make_engagement(tmp_path, "2026-foo")
        deck = eng / "02-customer-pack" / "deck.customer.fr.md"
        deck.write_text("---\nlanguage: fr\n---\nbody\n")
        hits, _ = scan_engagement(eng, self._build_canonical_rules())
        target = [h for h in hits if h.rule_id == "render-ownership-undeclared"]
        assert len(target) == 1
        assert target[0].severity == "info"
        assert target[0].deliverable_kind == "deck"

    def test_mismatched_role_owner_emits_warning(self, tmp_path: Path) -> None:
        eng = _make_engagement(tmp_path, "2026-foo")
        deck = eng / "02-customer-pack" / "deck.customer.fr.md"
        deck.write_text("---\nrole_owner: Brand Manager\nlanguage: fr\n---\n")
        hits, _ = scan_engagement(eng, self._build_canonical_rules())
        target = [h for h in hits if h.rule_id == "render-ownership-mismatch"]
        assert len(target) == 1
        assert target[0].severity == "warning"
        assert "Copywriter" in target[0].rationale

    def test_matched_role_owner_emits_no_hit(self, tmp_path: Path) -> None:
        eng = _make_engagement(tmp_path, "2026-foo")
        deck = eng / "02-customer-pack" / "deck.customer.fr.md"
        deck.write_text("---\nrole_owner: Copywriter\nlanguage: fr\n---\n")
        hits, _ = scan_engagement(eng, self._build_canonical_rules())
        target = [h for h in hits if h.deliverable_kind == "deck"]
        assert target == []

    def test_case_insensitive_role_comparison(self, tmp_path: Path) -> None:
        eng = _make_engagement(tmp_path, "2026-foo")
        deck = eng / "02-customer-pack" / "deck.customer.fr.md"
        deck.write_text("---\nrole_owner: copywriter\n---\n")
        hits, _ = scan_engagement(eng, self._build_canonical_rules())
        target = [
            h
            for h in hits
            if h.rule_id == "render-ownership-mismatch" and h.deliverable_kind == "deck"
        ]
        assert target == []

    def test_owner_field_fallback_accepted(self, tmp_path: Path) -> None:
        """`owner:` is accepted as a fallback for `role_owner:`."""
        eng = _make_engagement(tmp_path, "2026-foo")
        deck = eng / "02-customer-pack" / "deck.customer.fr.md"
        deck.write_text("---\nowner: Copywriter\n---\n")
        hits, _ = scan_engagement(eng, self._build_canonical_rules())
        target = [h for h in hits if h.deliverable_kind == "deck"]
        assert target == []

    def test_cardinality_aggregation(self, tmp_path: Path) -> None:
        eng = _make_engagement(tmp_path, "2026-foo")
        (eng / "02-customer-pack" / "proposal.fr.md").write_text(
            "---\nrole_owner: PMO\n---\n"
        )
        (eng / "02-customer-pack" / "tarification.fr.md").write_text(
            "---\nrole_owner: PMO\n---\n"
        )
        _, cardinality = scan_engagement(eng, self._build_canonical_rules())
        assert cardinality.get("proposal", 0) == 1
        assert cardinality.get("tarification", 0) == 1


# -----------------------------------------------------------------------------
# Transition-trigger hints (§16.3 advisories)
# -----------------------------------------------------------------------------


class TestTransitionHints:
    def test_pmo_to_revops_threshold_fires(self) -> None:
        hits = _aggregate_transition_hints(
            cardinality_totals={"proposal": 1, "tarification": 1, "dossier": 1},
            n_engagements=PMO_TO_REVOPS_THRESHOLD,
            pack_hints=(),
        )
        ids = [h.rule_id for h in hits]
        assert "transition-trigger-pmo-to-revops" in ids
        target = [h for h in hits if h.rule_id == "transition-trigger-pmo-to-revops"][0]
        assert target.severity == "info"

    def test_pmo_to_revops_below_threshold_silent(self) -> None:
        hits = _aggregate_transition_hints(
            cardinality_totals={"proposal": 1},
            n_engagements=1,
            pack_hints=(),
        )
        assert all(h.rule_id != "transition-trigger-pmo-to-revops" for h in hits)

    def test_pmo_to_revops_no_pmo_deliverables_silent(self) -> None:
        hits = _aggregate_transition_hints(
            cardinality_totals={"deck": 5},
            n_engagements=10,
            pack_hints=(),
        )
        assert all(h.rule_id != "transition-trigger-pmo-to-revops" for h in hits)

    def test_operator_hint_surfaces(self) -> None:
        hits = _aggregate_transition_hints(
            cardinality_totals={},
            n_engagements=1,
            pack_hints=("Render tooling complexity exceeds operator-handled threshold",),
        )
        target = [h for h in hits if h.rule_id == "transition-trigger-operator-hint"]
        assert len(target) == 1
        assert target[0].severity == "info"


# -----------------------------------------------------------------------------
# Pack overrides
# -----------------------------------------------------------------------------


class TestPackOverrides:
    def _canonical_rules(self) -> list[RenderOwnershipRule]:
        return parse_render_ownership_rules(WORKSPACE_BLUEPRINT_PATH)

    def test_none_pack_passes_through(self) -> None:
        rules = self._canonical_rules()
        out_rules, hints = _apply_pack_overrides(rules, None)
        assert out_rules == rules
        assert hints == ()

    def test_layer_disable_zeroes_rules(self) -> None:
        rules = self._canonical_rules()
        pack = RenderOwnershipPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Founder",
            canonical_source_refs=("WORKSPACE_BLUEPRINT §16",),
            layers_enabled={"render_ownership_coverage": False},
        )
        out_rules, _ = _apply_pack_overrides(rules, pack)
        assert out_rules == []

    def test_operator_rule_replaces_by_kind(self) -> None:
        rules = self._canonical_rules()
        override = RenderOwnershipRule(
            deliverable_kind="deck",
            expected_role_owner="Brand Manager",
            surface_pattern="02-customer-pack/deck.*.md",
            default_severity="error",
        )
        pack = RenderOwnershipPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Founder",
            canonical_source_refs=("WORKSPACE_BLUEPRINT §16",),
            render_ownership_rules=(override,),
        )
        out_rules, _ = _apply_pack_overrides(rules, pack)
        deck_rules = [r for r in out_rules if r.deliverable_kind == "deck"]
        assert len(deck_rules) == 1
        assert deck_rules[0].expected_role_owner == "Brand Manager"
        assert deck_rules[0].default_severity == "error"

    def test_transition_hints_surface(self) -> None:
        rules = self._canonical_rules()
        pack = RenderOwnershipPack(
            pack_version="v0.1.0",
            last_edited="2026-05-14",
            last_edited_by="Founder",
            canonical_source_refs=("WORKSPACE_BLUEPRINT §16",),
            transition_trigger_hints=("HLK Tech Lab productization trigger fired",),
        )
        _, hints = _apply_pack_overrides(rules, pack)
        assert hints == ("HLK Tech Lab productization trigger fired",)


# -----------------------------------------------------------------------------
# CLI behavior
# -----------------------------------------------------------------------------


class TestCLI:
    def test_empty_root_returns_zero_by_default(self, tmp_path: Path) -> None:
        rc = validator_main(["--engagement-root", str(tmp_path / "empty")])
        assert rc == 0

    def test_strict_empty_returns_one_when_no_engagements(self, tmp_path: Path) -> None:
        empty_root = tmp_path / "empty-clients"
        empty_root.mkdir()
        rc = validator_main(
            ["--engagement-root", str(empty_root), "--strict-empty"]
        )
        assert rc == 1

    def test_real_canonical_smoke_pass(self) -> None:
        """End-to-end smoke against the real Think Big roots.

        The Pack A4 default posture is advisory (warning + info; no error);
        running against the real engagement set should never exit non-zero
        in the default configuration.
        """
        rc = validator_main([])
        assert rc == 0

    def test_synthetic_engagement_passes_with_matched_owner(self, tmp_path: Path) -> None:
        eng = _make_engagement(tmp_path / "Clients", "2026-foo")
        (eng / "02-customer-pack" / "deck.customer.fr.md").write_text(
            "---\nrole_owner: Copywriter\n---\n"
        )
        rc = validator_main(["--engagement-root", str(tmp_path / "Clients")])
        assert rc == 0
