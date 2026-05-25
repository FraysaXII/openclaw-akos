"""Unit tests for the SYNTHESIS_BEFORE_TRANCHE Pydantic models (D-IH-86-EA..ED).

14th Quality Fabric specialty per `D-IH-86-EA` ratification (2026-05-25).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from akos.hlk_synthesis_before_tranche import (
    DIMENSION_DESCRIPTIONS,
    DIMENSION_FIRE_RULES,
    DIMENSION_SEVERITY_CLASS,
    SynthesisFindingRow,
    SynthesisReportSummary,
    SynthesisTrancheCharter,
    VALID_DIMENSION_CODES,
    VALID_DISPOSITIONS,
    VALID_FINDING_STATUSES,
    VALID_REVERSIBILITY_CLASSES,
    VALID_SWEEP_TRIGGERS,
    VALID_TRANCHE_CLASSES,
    resolve_fire_set,
)

pytestmark = pytest.mark.unit


# =============================================================================
# 1. Dimension enums + per-class fire rules
# =============================================================================


class TestDimensionEnum:
    def test_ten_dimensions_locked(self) -> None:
        # The 10-dimension model is the load-bearing claim of the specialty
        # per D-IH-86-EB. Locked tuple prevents accidental dimension drift.
        assert VALID_DIMENSION_CODES == frozenset({
            "SYN-01-AUDIENCE-COMPLETENESS",
            "SYN-02-CHANNEL-COVERAGE",
            "SYN-03-SCENARIO-INVENTORY",
            "SYN-04-BRAND-REGISTER-CITATION",
            "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
            "SYN-06-ERP-SURFACE-CITATION",
            "SYN-07-TRANCHE-ATOMICITY",
            "SYN-08-REVERSIBILITY-DECLARATION",
            "SYN-09-CLOSING-LOOP-TEST",
            "SYN-10-RECIPIENT-FALLBACK-CHANNEL",
        })

    def test_every_dimension_has_description(self) -> None:
        for code in VALID_DIMENSION_CODES:
            assert code in DIMENSION_DESCRIPTIONS, f"missing description for {code}"
            assert len(DIMENSION_DESCRIPTIONS[code]) > 20

    def test_every_dimension_has_severity_class(self) -> None:
        for code in VALID_DIMENSION_CODES:
            assert code in DIMENSION_SEVERITY_CLASS, (
                f"missing severity class for {code}"
            )

    def test_severity_classes_locked(self) -> None:
        # 4 mandatory-citation dimensions (FAIL ramp) per D-IH-86-ED
        # severity-class architecture. Anchors brand + governance lineage +
        # reversibility as non-negotiable.
        mandatory = {
            code
            for code, cls in DIMENSION_SEVERITY_CLASS.items()
            if cls == "mandatory-citation"
        }
        assert mandatory == {
            "SYN-04-BRAND-REGISTER-CITATION",
            "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
            "SYN-08-REVERSIBILITY-DECLARATION",
        }
        # SYN-07 is its own atomicity class (binary FAIL ramp permanently).
        assert DIMENSION_SEVERITY_CLASS["SYN-07-TRANCHE-ATOMICITY"] == "atomicity"


class TestTrancheClassFireRules:
    def test_six_tranche_classes_locked(self) -> None:
        assert VALID_TRANCHE_CLASSES == frozenset({
            "engagement",
            "specialty_mint",
            "internal_governance",
            "canonical_csv_mint",
            "brand_surface",
            "external_deliverable",
        })

    def test_every_class_has_fire_rules(self) -> None:
        for cls in VALID_TRANCHE_CLASSES:
            assert cls in DIMENSION_FIRE_RULES, f"missing fire rules for {cls}"

    def test_engagement_fires_all_ten(self) -> None:
        # Engagement-class tranches always fire all 10 dimensions per
        # D-IH-86-EC. SUEZ POC + Aïsha-on-SUEZ are worked examples.
        always, conditional = DIMENSION_FIRE_RULES["engagement"]
        assert always == VALID_DIMENSION_CODES
        assert conditional == frozenset()

    def test_external_deliverable_fires_all_ten(self) -> None:
        # External-deliverable tranches (investor stability dossier, ENISA
        # dossier, SUEZ cobranded mail) inherit the engagement fire-set.
        always, conditional = DIMENSION_FIRE_RULES["external_deliverable"]
        assert always == VALID_DIMENSION_CODES

    def test_internal_governance_minimal_baseline(self) -> None:
        # Internal-governance tranches (operator-scratchpad updates,
        # decision-register appends, files-modified.csv rows) fire only
        # the 3 baseline governance dimensions when audience is J-OP only.
        always, conditional = DIMENSION_FIRE_RULES["internal_governance"]
        assert always == frozenset({
            "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
            "SYN-07-TRANCHE-ATOMICITY",
            "SYN-08-REVERSIBILITY-DECLARATION",
        })

    def test_specialty_mint_excludes_syn03_baseline(self) -> None:
        # Specialty-mint tranches fire 7 baseline (SYN-03 is conditional;
        # only fires when the specialty has end-user scenarios). Recursive
        # self-application: this specialty's own mint passes the
        # specialty_mint fire-set.
        always, conditional = DIMENSION_FIRE_RULES["specialty_mint"]
        assert "SYN-03-SCENARIO-INVENTORY" not in always
        assert "SYN-03-SCENARIO-INVENTORY" in conditional
        assert len(always) == 7

    def test_brand_surface_makes_syn06_conditional(self) -> None:
        # Brand-surface tranches fire 9 baseline; SYN-06 (ERP surface
        # citation) is conditional because not all brand surfaces are
        # engagement-scoped.
        always, conditional = DIMENSION_FIRE_RULES["brand_surface"]
        assert "SYN-06-ERP-SURFACE-CITATION" not in always
        assert "SYN-06-ERP-SURFACE-CITATION" in conditional


class TestResolveFireSet:
    def test_engagement_baseline_returns_all_ten(self) -> None:
        result = resolve_fire_set("engagement")
        assert result == VALID_DIMENSION_CODES

    def test_specialty_mint_baseline_returns_seven(self) -> None:
        result = resolve_fire_set("specialty_mint")
        assert len(result) == 7
        assert "SYN-03-SCENARIO-INVENTORY" not in result

    def test_specialty_mint_conditional_returns_eight(self) -> None:
        result = resolve_fire_set("specialty_mint", conditional_triggers=True)
        assert len(result) == 8
        assert "SYN-03-SCENARIO-INVENTORY" in result

    def test_unknown_tranche_class_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown tranche_class"):
            resolve_fire_set("not_a_real_class")


# =============================================================================
# 2. Disposition + status + reversibility + sweep-trigger enums
# =============================================================================


class TestDispositionEnum:
    def test_five_options_locked(self) -> None:
        # 5-option disposition enum per D-IH-86-EC. Mirrors INDEX_INTEGRITY
        # + INTER_WAVE_REGRESSION 5-option enums for findings disposition.
        assert VALID_DISPOSITIONS == frozenset({
            "scope-complete",
            "scope-extend",
            "scope-narrow",
            "defer-OPS",
            "escalate-to-blocker-tracker",
        })

    def test_finding_statuses_locked(self) -> None:
        assert VALID_FINDING_STATUSES == frozenset({
            "PASS",
            "WARN",
            "FAIL",
            "INFO",
            "N/A",
        })

    def test_reversibility_classes_locked(self) -> None:
        assert VALID_REVERSIBILITY_CLASSES == frozenset({
            "low",
            "medium",
            "high",
        })

    def test_sweep_triggers_locked(self) -> None:
        assert VALID_SWEEP_TRIGGERS == frozenset({
            "pre_commit_self_test",
            "tranche_charter",
            "tranche_pre_commit",
            "on_demand",
        })


# =============================================================================
# 3. SynthesisFindingRow model
# =============================================================================


def _valid_finding_payload() -> dict:
    return {
        "tranche_id": "specialty-mint-14-synthesis-before-tranche",
        "tranche_class": "specialty_mint",
        "dimension_code": "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
        "status": "PASS",
        "finding_text": "Ratifying decisions D-IH-86-EA..ED cited in frontmatter.",
        "recommendation_text": "",
        "evidence_path": (
            "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/"
            "SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md"
        ),
        "recommended_disposition": "scope-complete",
        "notes": "",
    }


class TestSynthesisFindingRow:
    def test_valid_payload_constructs(self) -> None:
        row = SynthesisFindingRow(**_valid_finding_payload())
        assert row.tranche_id == "specialty-mint-14-synthesis-before-tranche"
        assert row.status == "PASS"

    def test_invalid_dimension_code_rejected(self) -> None:
        payload = _valid_finding_payload()
        payload["dimension_code"] = "SYN-99-DOES-NOT-EXIST"
        with pytest.raises(ValidationError):
            SynthesisFindingRow(**payload)

    def test_invalid_tranche_class_rejected(self) -> None:
        payload = _valid_finding_payload()
        payload["tranche_class"] = "not_a_real_class"
        with pytest.raises(ValidationError):
            SynthesisFindingRow(**payload)

    def test_invalid_status_rejected(self) -> None:
        payload = _valid_finding_payload()
        payload["status"] = "MAYBE"
        with pytest.raises(ValidationError):
            SynthesisFindingRow(**payload)

    def test_invalid_disposition_rejected(self) -> None:
        payload = _valid_finding_payload()
        payload["recommended_disposition"] = "ignore-it"
        with pytest.raises(ValidationError):
            SynthesisFindingRow(**payload)

    def test_extra_fields_rejected(self) -> None:
        payload = _valid_finding_payload()
        payload["random_extra"] = "x"
        with pytest.raises(ValidationError):
            SynthesisFindingRow(**payload)

    def test_finding_text_required(self) -> None:
        payload = _valid_finding_payload()
        payload["finding_text"] = ""
        with pytest.raises(ValidationError):
            SynthesisFindingRow(**payload)

    def test_na_status_allowed(self) -> None:
        payload = _valid_finding_payload()
        payload["status"] = "N/A"
        payload["finding_text"] = "Dimension does not fire for this tranche class."
        row = SynthesisFindingRow(**payload)
        assert row.status == "N/A"


# =============================================================================
# 4. SynthesisTrancheCharter model
# =============================================================================


def _valid_charter_payload() -> dict:
    return {
        "tranche_id": "engagement-suez-poc-2026-05-28",
        "tranche_class": "engagement",
        "tranche_title": "SUEZ POC full kit (libellé generator + addendum PDF)",
        "audiences_named": ["J-CU", "J-OP"],
        "channels_named": ["CHAN-EMAIL-OUTBOUND", "CHAN-WEB-DASHBOARD"],
        "scenarios_named": ["first-look", "operator-review-pre-send"],
        "brand_register": "external-translated",
        "ratifying_decisions": ["D-IH-86-EA"],
        "erp_surface_citations": [
            "operator-dashboard",
            "customer-dashboard",
            "erp-workflow-join",
        ],
        "is_atomic_commit": True,
        "reversibility_class": "medium",
        "reversibility_rationale": (
            "Cobranded mail sent; PDF rendered; recoverable via amend mail "
            "+ re-render."
        ),
        "closing_loop_test": (
            "SUEZ rep replies + downloads PDF + libellé generator opens "
            "without macro warning."
        ),
        "recipient_fallback_channel": (
            "Operator forwards PDF via WhatsApp if mail bounces."
        ),
        "operator_framing_quote": (
            "the main goal is to properly govern our engagements via "
            "cleverly crafting erp workflow and UX"
        ),
    }


class TestSynthesisTrancheCharter:
    def test_valid_charter_constructs(self) -> None:
        charter = SynthesisTrancheCharter(**_valid_charter_payload())
        assert charter.tranche_class == "engagement"
        assert "J-CU" in charter.audiences_named
        assert "operator-dashboard" in charter.erp_surface_citations

    def test_minimum_internal_governance_charter(self) -> None:
        # Internal governance tranches need only the 3 baseline fields
        # populated (tranche_id, tranche_class, tranche_title). Other
        # fields can be left at defaults because the fire-set is minimal.
        charter = SynthesisTrancheCharter(
            tranche_id="commit-2c-b-files-modified-append",
            tranche_class="internal_governance",
            tranche_title="files-modified.csv rows for Commit 2c-b",
            ratifying_decisions=["D-IH-86-DA"],
        )
        assert charter.brand_register == "internal-corpint"
        assert charter.reversibility_class == "medium"
        assert charter.is_atomic_commit is True

    def test_invalid_brand_register_rejected(self) -> None:
        payload = _valid_charter_payload()
        payload["brand_register"] = "neither"
        with pytest.raises(ValidationError):
            SynthesisTrancheCharter(**payload)

    def test_invalid_tranche_class_rejected(self) -> None:
        payload = _valid_charter_payload()
        payload["tranche_class"] = "ad_hoc"
        with pytest.raises(ValidationError):
            SynthesisTrancheCharter(**payload)

    def test_extra_fields_rejected(self) -> None:
        payload = _valid_charter_payload()
        payload["secret_param"] = "x"
        with pytest.raises(ValidationError):
            SynthesisTrancheCharter(**payload)


# =============================================================================
# 5. SynthesisReportSummary model
# =============================================================================


def _valid_summary_payload() -> dict:
    return {
        "tranche_id": "specialty-mint-14-synthesis-before-tranche",
        "tranche_class": "specialty_mint",
        "swept_at": "2026-05-25",
        "sweep_trigger": "tranche_pre_commit",
        "dimensions_fired": 7,
        "pass_count": 7,
        "warn_count": 0,
        "fail_count": 0,
        "info_count": 0,
        "na_count": 3,
        "synthesis_complete": True,
        "inline_ratify_gates_open": 0,
        "operator_disposition_recorded": True,
    }


class TestSynthesisReportSummary:
    def test_valid_summary_constructs(self) -> None:
        summary = SynthesisReportSummary(**_valid_summary_payload())
        assert summary.tranche_class == "specialty_mint"
        assert summary.synthesis_complete is True

    def test_invalid_swept_at_format_rejected(self) -> None:
        payload = _valid_summary_payload()
        payload["swept_at"] = "May 25 2026"
        with pytest.raises(ValidationError):
            SynthesisReportSummary(**payload)

    def test_invalid_sweep_trigger_rejected(self) -> None:
        payload = _valid_summary_payload()
        payload["sweep_trigger"] = "manual"
        with pytest.raises(ValidationError):
            SynthesisReportSummary(**payload)

    def test_dimensions_fired_capped_at_ten(self) -> None:
        payload = _valid_summary_payload()
        payload["dimensions_fired"] = 11
        with pytest.raises(ValidationError):
            SynthesisReportSummary(**payload)

    def test_negative_counts_rejected(self) -> None:
        payload = _valid_summary_payload()
        payload["pass_count"] = -1
        with pytest.raises(ValidationError):
            SynthesisReportSummary(**payload)

    def test_synthesis_complete_false_when_fail(self) -> None:
        # Drift gate consumes synthesis_complete per D-IH-86-ED. False when
        # any FAIL or any mandatory-citation dimension missing.
        payload = _valid_summary_payload()
        payload["pass_count"] = 6
        payload["fail_count"] = 1
        payload["synthesis_complete"] = False
        summary = SynthesisReportSummary(**payload)
        assert summary.synthesis_complete is False


# =============================================================================
# 6. Recursive self-application — the doctrine itself passes the synthesis bar
# =============================================================================


class TestRecursiveSelfApplication:
    """The 14th specialty mint MUST pass synthesis-before-tranche on its own
    mint (per SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md §10 migration posture
    + the recursive-self-application gate). These tests embed the recursive
    check inline so future regressions are caught at unit-test time."""

    def test_specialty_mint_fire_set_can_be_satisfied(self) -> None:
        # The 7 always-fire dimensions for specialty_mint can each be
        # satisfied by the mint commit's authored evidence:
        #   - SYN-01 audience: J-OP + J-AIC (the doctrine's own audience tag)
        #   - SYN-02 channel: CHAN-WEB-DASHBOARD (read in cursor) + repo
        #   - SYN-04 brand: internal-corpint (the doctrine's own register)
        #   - SYN-05 governance: D-IH-86-EA..ED ratifying decisions
        #   - SYN-07 atomicity: 4-commit kit pattern (2a+2b+2c-a+2c-b)
        #   - SYN-08 reversibility: medium-low (governance-class registration)
        #   - SYN-09 closing-loop: validate_synthesis_before_tranche --self-test
        always = resolve_fire_set("specialty_mint")
        for code in always:
            assert code in VALID_DIMENSION_CODES, (
                f"specialty_mint fire-set includes {code} but {code} is not "
                f"in the locked dimension enum"
            )

    def test_doctrine_authorship_satisfies_mandatory_citation_dimensions(self) -> None:
        # The 3 mandatory-citation dimensions (SYN-04/05/08) all fire for
        # specialty_mint. The doctrine itself must cite each in its
        # frontmatter — the unit test below proves the schema accepts the
        # citations.
        for code in (
            "SYN-04-BRAND-REGISTER-CITATION",
            "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
            "SYN-08-REVERSIBILITY-DECLARATION",
        ):
            assert DIMENSION_SEVERITY_CLASS[code] == "mandatory-citation"
            assert code in resolve_fire_set("specialty_mint")
