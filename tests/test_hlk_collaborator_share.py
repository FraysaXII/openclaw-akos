"""Unit tests for the 5 Collaborator-Share Pydantic models (D-IH-86-CY-A)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from akos.hlk_collaborator_share import (
    COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
    HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
    PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES,
    COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES,
    COLLABORATOR_RATE_OVERRIDES_FIELDNAMES,
    DEFAULT_HOLISTIKA_SHARE_PCT,
    DEFAULT_COLLABORATOR_SHARE_PCT,
    DEFAULT_BILL_MODE_PER_SERVICE_CLASS,
    MARKET_RATE_VARIANCE_TOLERANCE_PCT,
    CollaboratorShareRegistryRow,
    HolistikaVendorServicesBilledRow,
    PartnerOverlapExclusionClauseRow,
    CollaboratorMarketRateReferenceRow,
    CollaboratorRateOverrideRow,
    default_split_holds,
    split_sums_to_100,
    bill_mode_matches_default,
    rate_within_market_band,
    variance_pct_signed,
)


# =============================================================================
# Fieldname tuples (header SSOT)
# =============================================================================


pytestmark = pytest.mark.unit


class TestFieldnameTuples:
    def test_share_registry_fieldnames_locked(self) -> None:
        assert COLLABORATOR_SHARE_REGISTRY_FIELDNAMES == (
            "share_id",
            "engagement_id",
            "collaborator_id",
            "engagement_model_id",
            "holistika_share_pct",
            "collaborator_share_pct",
            "collaborator_billed_rate",
            "collaborator_billed_rate_currency",
            "collaborator_role_class",
            "share_override_decision_id",
            "status",
            "signed_at",
            "signed_by_collaborator",
            "signed_by_holistika",
            "last_review_at",
            "notes",
        )

    def test_vendor_billed_fieldnames_locked(self) -> None:
        assert HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES == (
            "vendor_billing_id",
            "engagement_id",
            "holistika_service_class",
            "bill_mode",
            "billed_hours",
            "billed_rate",
            "billed_amount_computed",
            "justification_clause_id",
            "bill_mode_decision_id",
            "status",
            "last_review_at",
            "notes",
        )

    def test_overlap_clauses_fieldnames_locked(self) -> None:
        assert PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES == (
            "clause_id",
            "clause_name",
            "applicable_holistika_service_classes",
            "overlap_pattern_description",
            "internal_precedent",
            "industry_precedent_citation",
            "ratifying_decision_id",
            "last_review_at",
            "status",
            "notes",
        )

    def test_market_rate_fieldnames_locked(self) -> None:
        assert COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES == (
            "rate_id",
            "role_class",
            "region_code",
            "experience_band",
            "rate_currency",
            "rate_min_per_hour",
            "rate_typical_per_hour",
            "rate_max_per_hour",
            "rate_source",
            "last_review_at",
            "status",
            "notes",
        )

    def test_rate_overrides_fieldnames_locked(self) -> None:
        assert COLLABORATOR_RATE_OVERRIDES_FIELDNAMES == (
            "override_id",
            "override_kind",
            "engagement_id",
            "collaborator_id",
            "reference_rate_id",
            "reference_rate_value",
            "actual_value",
            "variance_pct",
            "justification_narrative",
            "ratifying_decision_id",
            "commercial_strategy_rationale",
            "expires_at",
            "last_review_at",
            "status",
            "notes",
        )


# =============================================================================
# Doctrine constants
# =============================================================================


class TestDoctrineConstants:
    def test_default_split_is_65_35(self) -> None:
        assert DEFAULT_HOLISTIKA_SHARE_PCT == 65
        assert DEFAULT_COLLABORATOR_SHARE_PCT == 35
        assert DEFAULT_HOLISTIKA_SHARE_PCT + DEFAULT_COLLABORATOR_SHARE_PCT == 100

    def test_market_rate_tolerance_is_25_pct(self) -> None:
        assert MARKET_RATE_VARIANCE_TOLERANCE_PCT == 25.0

    def test_default_bill_mode_per_service_class_covers_10_classes(self) -> None:
        assert len(DEFAULT_BILL_MODE_PER_SERVICE_CLASS) == 10

    def test_default_bill_modes_per_doctrine_section_2_2(self) -> None:
        # in-kind by default per doctrine §2.2
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["research_head_discipline"] == "in_kind"
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["mktops_marketing"] == "in_kind"
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["dataops_engineering"] == "in_kind"
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["madeira_ai_orchestration"] == "in_kind"
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["brand_render_machinery"] == "in_kind"
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["pmo_orchestration"] == "in_kind"
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["legal_template_handling"] == "in_kind"
        # billed by default per doctrine §2.2 (scope-bearing classes)
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["front_end_engineering"] == "billed"
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["ai_engineering_bespoke"] == "billed"
        assert DEFAULT_BILL_MODE_PER_SERVICE_CLASS["external_research_pass"] == "billed"


# =============================================================================
# CollaboratorShareRegistryRow
# =============================================================================


class TestShareRegistryRow:
    def _valid_payload(self) -> dict:
        return {
            "share_id": "SHARE-EFA-SUEZ-2026",
            "engagement_id": "2026-suez-webuy-aisha",
            "collaborator_id": "POI-PRT-EFA-LEAD-2026",
            "engagement_model_id": "eng_model_percentage_collaborator",
            "holistika_share_pct": 65,
            "collaborator_share_pct": 35,
            "collaborator_billed_rate": 100.0,
            "collaborator_billed_rate_currency": "EUR",
            "collaborator_role_class": "EFA Operator Lead",
            "share_override_decision_id": "",
            "status": "active",
            "signed_at": "2026-05-25",
            "signed_by_collaborator": "Aïsha",
            "signed_by_holistika": "Founder/CEO",
            "last_review_at": "2026-05-25",
            "notes": "",
        }

    def test_valid_default_split_row(self) -> None:
        row = CollaboratorShareRegistryRow(**self._valid_payload())
        assert row.holistika_share_pct == 65
        assert row.collaborator_share_pct == 35

    def test_share_id_pattern_enforced(self) -> None:
        payload = self._valid_payload()
        payload["share_id"] = "share-lowercase-bad"
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)

    def test_currency_must_be_iso_4217(self) -> None:
        payload = self._valid_payload()
        payload["collaborator_billed_rate_currency"] = "USDOLLAR"
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)

    def test_pct_range_enforced(self) -> None:
        payload = self._valid_payload()
        payload["holistika_share_pct"] = 150
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)

    def test_extra_fields_forbidden(self) -> None:
        payload = self._valid_payload()
        payload["bogus_field"] = "x"
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)


# =============================================================================
# HolistikaVendorServicesBilledRow
# =============================================================================


class TestVendorBilledRow:
    def _valid_payload(self) -> dict:
        return {
            "vendor_billing_id": "VBILL-SUEZ-MKTOPS-IN-KIND-2026",
            "engagement_id": "2026-suez-webuy-aisha",
            "holistika_service_class": "mktops_marketing",
            "bill_mode": "in_kind",
            "billed_hours": "",
            "billed_rate": "",
            "billed_amount_computed": "",
            "justification_clause_id": "",
            "bill_mode_decision_id": "",
            "status": "active",
            "last_review_at": "2026-05-25",
            "notes": "",
        }

    def test_valid_in_kind_row(self) -> None:
        row = HolistikaVendorServicesBilledRow(**self._valid_payload())
        assert row.bill_mode == "in_kind"

    def test_valid_billed_row(self) -> None:
        payload = self._valid_payload()
        payload["holistika_service_class"] = "front_end_engineering"
        payload["bill_mode"] = "billed"
        payload["billed_hours"] = 12.0
        payload["billed_rate"] = 150.0
        payload["billed_amount_computed"] = 1800.0
        row = HolistikaVendorServicesBilledRow(**payload)
        assert row.bill_mode == "billed"

    def test_unknown_service_class_rejected(self) -> None:
        payload = self._valid_payload()
        payload["holistika_service_class"] = "marketing_strategy"  # not in enum
        with pytest.raises(ValidationError):
            HolistikaVendorServicesBilledRow(**payload)


# =============================================================================
# PartnerOverlapExclusionClauseRow
# =============================================================================


class TestOverlapClauseRow:
    def _valid_payload(self) -> dict:
        return {
            "clause_id": "clause_partner_marketing_agency_overlap",
            "clause_name": "Partner-as-Marketing-Agency Overlap",
            "applicable_holistika_service_classes": "mktops_marketing",
            "overlap_pattern_description": "When partner is a marketing agency.",
            "internal_precedent": "2026 Websitz / Rushly engagement",
            "industry_precedent_citation": "OECD TPG 2022 chapter VI",
            "ratifying_decision_id": "D-IH-86-CY-C",
            "last_review_at": "2026-05-25",
            "status": "active",
            "notes": "Seed clause.",
        }

    def test_valid_clause(self) -> None:
        row = PartnerOverlapExclusionClauseRow(**self._valid_payload())
        assert row.clause_id == "clause_partner_marketing_agency_overlap"

    def test_clause_id_pattern_enforced(self) -> None:
        payload = self._valid_payload()
        payload["clause_id"] = "BadClauseIdWithCaps"
        with pytest.raises(ValidationError):
            PartnerOverlapExclusionClauseRow(**payload)


# =============================================================================
# CollaboratorMarketRateReferenceRow
# =============================================================================


class TestMarketRateRow:
    def _valid_payload(self) -> dict:
        return {
            "rate_id": "rate_fr_efa_operator_senior",
            "role_class": "EFA Operator Lead",
            "region_code": "FR",
            "experience_band": "senior",
            "rate_currency": "EUR",
            "rate_min_per_hour": 75.0,
            "rate_typical_per_hour": 100.0,
            "rate_max_per_hour": 130.0,
            "rate_source": "Malt FR senior data-class freelancer survey 2026 Q1",
            "last_review_at": "2026-05-25",
            "status": "active",
            "notes": "",
        }

    def test_valid_row(self) -> None:
        row = CollaboratorMarketRateReferenceRow(**self._valid_payload())
        assert row.rate_typical_per_hour == 100.0

    def test_region_must_be_iso_3166_alpha_2(self) -> None:
        payload = self._valid_payload()
        payload["region_code"] = "FRA"  # alpha-3 rejected
        with pytest.raises(ValidationError):
            CollaboratorMarketRateReferenceRow(**payload)

    def test_typical_rate_must_be_positive(self) -> None:
        payload = self._valid_payload()
        payload["rate_typical_per_hour"] = 0
        with pytest.raises(ValidationError):
            CollaboratorMarketRateReferenceRow(**payload)


# =============================================================================
# CollaboratorRateOverrideRow
# =============================================================================


class TestRateOverrideRow:
    def _valid_payload(self) -> dict:
        return {
            "override_id": "OVERRIDE-SUEZ-RATE-2026-05",
            "override_kind": "market_rate_excursion",
            "engagement_id": "2026-suez-webuy-aisha",
            "collaborator_id": "POI-PRT-EFA-LEAD-2026",
            "reference_rate_id": "rate_fr_efa_operator_senior",
            "reference_rate_value": 100.0,
            "actual_value": 130.0,
            "variance_pct": 30.0,
            "justification_narrative": "Strategic POC engagement.",
            "ratifying_decision_id": "D-IH-86-CY-F",
            "commercial_strategy_rationale": "Aisha brings flagship SUEZ deal.",
            "expires_at": "2027-05-25",
            "last_review_at": "2026-05-25",
            "status": "active",
            "notes": "",
        }

    def test_valid_market_rate_override(self) -> None:
        row = CollaboratorRateOverrideRow(**self._valid_payload())
        assert row.variance_pct == 30.0

    def test_unknown_override_kind_rejected(self) -> None:
        payload = self._valid_payload()
        payload["override_kind"] = "exotic_kind"
        with pytest.raises(ValidationError):
            CollaboratorRateOverrideRow(**payload)


# =============================================================================
# Helper functions
# =============================================================================


class TestHelpers:
    def test_default_split_holds_for_65_35(self) -> None:
        assert default_split_holds(65, 35) is True

    def test_default_split_holds_false_for_70_30(self) -> None:
        assert default_split_holds(70, 30) is False

    def test_split_sums_to_100(self) -> None:
        assert split_sums_to_100(65, 35) is True
        assert split_sums_to_100(70, 30) is True
        assert split_sums_to_100(60, 30) is False

    def test_bill_mode_matches_default_in_kind(self) -> None:
        assert bill_mode_matches_default("mktops_marketing", "in_kind") is True
        assert bill_mode_matches_default("mktops_marketing", "billed") is False

    def test_bill_mode_matches_default_billed(self) -> None:
        assert bill_mode_matches_default("front_end_engineering", "billed") is True
        assert bill_mode_matches_default("front_end_engineering", "in_kind") is False

    def test_bill_mode_unknown_service_class(self) -> None:
        assert bill_mode_matches_default("unknown_class", "billed") is False

    def test_rate_within_market_band_passes_at_25_pct(self) -> None:
        # 125 vs typical 100 is exactly 25% — within band
        assert rate_within_market_band(125.0, 100.0) is True
        # 100 vs typical 100 is 0% — within band
        assert rate_within_market_band(100.0, 100.0) is True

    def test_rate_within_market_band_fails_above_25_pct(self) -> None:
        # 130 vs typical 100 is 30% — outside band
        assert rate_within_market_band(130.0, 100.0) is False

    def test_rate_within_market_band_fails_below_minus_25_pct(self) -> None:
        # 70 vs typical 100 is -30% — outside band
        assert rate_within_market_band(70.0, 100.0) is False

    def test_rate_within_market_band_handles_zero_reference(self) -> None:
        assert rate_within_market_band(50.0, 0) is False

    def test_variance_pct_signed_positive(self) -> None:
        assert variance_pct_signed(130.0, 100.0) == pytest.approx(30.0)

    def test_variance_pct_signed_negative(self) -> None:
        assert variance_pct_signed(70.0, 100.0) == pytest.approx(-30.0)

    def test_variance_pct_signed_zero_reference(self) -> None:
        assert variance_pct_signed(100.0, 0) == 0.0
