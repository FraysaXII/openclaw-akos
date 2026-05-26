"""Unit tests for the 5 Collaborator-Share Pydantic models (D-IH-86-DA)."""

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
    DEFAULT_BD_INTRO_HOLISTIKA_PCT,
    DEFAULT_BD_INTRO_COLLABORATOR_PCT,
    DEFAULT_JOINT_VENTURE_HOLISTIKA_PCT,
    DEFAULT_JOINT_VENTURE_COLLABORATOR_PCT,
    DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_SOLO,
    DEFAULT_CONSULTING_DIRECT_COLLABORATOR_PCT_SOLO,
    DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_WITH_OVERLAY,
    DEFAULT_BD_COMMISSION_OVERLAY_PCT,
    DEFAULT_BILL_MODE_PER_SERVICE_CLASS,
    MARKET_RATE_VARIANCE_TOLERANCE_PCT,
    METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS,
    VALID_COLLABORATOR_SHARE_CHECK_CODES,
    VALID_METHODOLOGY_READINESS,
    VALID_OVERLAY_BASE_PAIRINGS,
    VALID_OVERRIDE_KINDS,
    VALID_SHARE_OVERLAYS,
    VALID_SHARE_PATTERNS,
    CollaboratorShareRegistryRow,
    HolistikaVendorServicesBilledRow,
    PartnerOverlapExclusionClauseRow,
    CollaboratorMarketRateReferenceRow,
    CollaboratorRateOverrideRow,
    across_rows_sum_to_100,
    bd_commission_overlay_default_holds,
    bd_intro_default_split_holds,
    bill_mode_matches_default,
    consulting_direct_solo_default_holds,
    consulting_direct_with_overlay_default_holds,
    default_split_holds,
    joint_venture_default_split_holds,
    methodology_permits_share_pattern,
    methodology_readiness_is_valid,
    overlay_base_pairing_is_valid,
    rate_within_market_band,
    share_overlay_is_valid,
    share_pattern_is_valid,
    split_sums_to_100,
    variance_pct_signed,
)


# =============================================================================
# Fieldname tuples (header SSOT)
# =============================================================================


pytestmark = pytest.mark.unit


class TestFieldnameTuples:
    def test_share_registry_fieldnames_locked(self) -> None:
        # 20-tuple per Wave R+2 Commit 2 (D-IH-86-EJ + D-IH-86-EN + D-IH-86-EK):
        # share_overlay added at idx 5 (stackable overlay enum;
        # bd_commission_overlay or empty); methodology_readiness added at
        # idx 10 (4-value enum: methodology_trained / methodology_in_progress
        # / methodology_naive / methodology_not_applicable) so the share_pattern
        # eligibility matrix gates against collaborator readiness BEFORE
        # commercial commit; parallel_invoice_stream_indicator appended at idx
        # 19 (bool; default False) per the 2026-05-13 post-handshake debrief
        # grounding (F-PI-01) so settlement + invoicing tooling can branch on
        # parallel-billing-stream engagements explicitly rather than by
        # inference.
        assert COLLABORATOR_SHARE_REGISTRY_FIELDNAMES == (
            "share_id",
            "engagement_id",
            "collaborator_id",
            "engagement_model_id",
            "share_pattern",
            "share_overlay",
            "holistika_share_pct",
            "collaborator_share_pct",
            "collaborator_billed_rate",
            "collaborator_billed_rate_currency",
            "collaborator_role_class",
            "methodology_readiness",
            "share_override_decision_id",
            "status",
            "signed_at",
            "signed_by_collaborator",
            "signed_by_holistika",
            "last_review_at",
            "notes",
            "parallel_invoice_stream_indicator",
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
            "share_pattern": "deep_partner_65_35",
            "share_overlay": "",
            "holistika_share_pct": 65,
            "collaborator_share_pct": 35,
            "collaborator_billed_rate": 100.0,
            "collaborator_billed_rate_currency": "EUR",
            "collaborator_role_class": "EFA Operator Lead",
            "methodology_readiness": "methodology_trained",
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
        assert row.share_overlay == ""
        assert row.methodology_readiness == "methodology_trained"

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

    # -- New tests at Wave R+2 Commit 2: pre-rewrite enum values rejected --

    def test_pre_rewrite_orchestration_broker_pattern_rejected(self) -> None:
        # orchestration_broker_thin_margin was removed at D-IH-86-EJ rewrite;
        # the value must no longer parse so migration pressure surfaces loudly.
        payload = self._valid_payload()
        payload["share_pattern"] = "orchestration_broker_thin_margin"
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)

    def test_pre_rewrite_custom_pattern_rejected(self) -> None:
        # custom was removed at D-IH-86-EJ rewrite (replaced by the 4-base
        # enumeration; deviations route through bd_commission_overlay or
        # OVERRIDE rows).
        payload = self._valid_payload()
        payload["share_pattern"] = "custom"
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)

    # -- New tests: 4 base patterns accepted --

    def test_bd_intro_only_pattern_accepted(self) -> None:
        payload = self._valid_payload()
        payload["share_pattern"] = "bd_intro_only"
        payload["holistika_share_pct"] = 85
        payload["collaborator_share_pct"] = 15
        row = CollaboratorShareRegistryRow(**payload)
        assert row.share_pattern == "bd_intro_only"

    def test_joint_venture_aventure_pattern_accepted(self) -> None:
        payload = self._valid_payload()
        payload["share_pattern"] = "joint_venture_aventure"
        payload["holistika_share_pct"] = 50
        payload["collaborator_share_pct"] = 50
        row = CollaboratorShareRegistryRow(**payload)
        assert row.share_pattern == "joint_venture_aventure"

    def test_consulting_direct_solo_pattern_accepted(self) -> None:
        payload = self._valid_payload()
        payload["share_pattern"] = "consulting_direct"
        payload["holistika_share_pct"] = 100
        payload["collaborator_share_pct"] = 0
        row = CollaboratorShareRegistryRow(**payload)
        assert row.share_pattern == "consulting_direct"
        assert row.share_overlay == ""

    # -- New tests: share_overlay enum --

    def test_bd_commission_overlay_accepted_on_consulting_direct(self) -> None:
        # SUEZ POC corrected shape: consulting_direct base + overlay sibling row
        payload = self._valid_payload()
        payload["share_pattern"] = "consulting_direct"
        payload["share_overlay"] = "bd_commission_overlay"
        payload["holistika_share_pct"] = 0
        payload["collaborator_share_pct"] = 15
        row = CollaboratorShareRegistryRow(**payload)
        assert row.share_overlay == "bd_commission_overlay"

    def test_unknown_share_overlay_rejected(self) -> None:
        payload = self._valid_payload()
        payload["share_overlay"] = "made_up_overlay"
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)

    # -- New tests: methodology_readiness enum (all 4 values + invalid) --

    def test_methodology_in_progress_accepted(self) -> None:
        payload = self._valid_payload()
        payload["methodology_readiness"] = "methodology_in_progress"
        row = CollaboratorShareRegistryRow(**payload)
        assert row.methodology_readiness == "methodology_in_progress"

    def test_methodology_naive_accepted_on_bd_intro_pattern(self) -> None:
        # methodology_naive is permissible for bd_intro_only per the
        # permissibility matrix; chassis-level Literal accepts it; helper
        # methodology_permits_share_pattern enforces the gating in CS-08.
        payload = self._valid_payload()
        payload["share_pattern"] = "bd_intro_only"
        payload["holistika_share_pct"] = 85
        payload["collaborator_share_pct"] = 15
        payload["methodology_readiness"] = "methodology_naive"
        row = CollaboratorShareRegistryRow(**payload)
        assert row.methodology_readiness == "methodology_naive"

    def test_methodology_not_applicable_accepted(self) -> None:
        payload = self._valid_payload()
        payload["share_pattern"] = "consulting_direct"
        payload["holistika_share_pct"] = 100
        payload["collaborator_share_pct"] = 0
        payload["methodology_readiness"] = "methodology_not_applicable"
        row = CollaboratorShareRegistryRow(**payload)
        assert row.methodology_readiness == "methodology_not_applicable"

    def test_unknown_methodology_readiness_rejected(self) -> None:
        payload = self._valid_payload()
        payload["methodology_readiness"] = "methodology_godlike"
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)

    def test_methodology_readiness_required(self) -> None:
        # Field is non-optional; missing must FAIL validation.
        payload = self._valid_payload()
        del payload["methodology_readiness"]
        with pytest.raises(ValidationError):
            CollaboratorShareRegistryRow(**payload)

    # -- New tests: parallel_invoice_stream_indicator (D-IH-86-EK) --

    def test_parallel_invoice_stream_indicator_defaults_false(self) -> None:
        # The historical default is single-billing-entity (Holistika invoices
        # the customer for 100% then settles the collaborator share). New
        # rows that omit the field must inherit False so pre-rewrite CSV rows
        # parse cleanly once Commit 5 adds the column.
        payload = self._valid_payload()
        assert "parallel_invoice_stream_indicator" not in payload
        row = CollaboratorShareRegistryRow(**payload)
        assert row.parallel_invoice_stream_indicator is False

    def test_parallel_invoice_stream_indicator_true_accepted(self) -> None:
        # When True, the engagement bills via two parallel invoice streams
        # (Holistika + collaborator each invoice the end customer for their
        # share). Materially changes VAT + dispute-resolution surface; the
        # indicator MUST be explicit.
        payload = self._valid_payload()
        payload["parallel_invoice_stream_indicator"] = True
        row = CollaboratorShareRegistryRow(**payload)
        assert row.parallel_invoice_stream_indicator is True

    def test_parallel_invoice_stream_indicator_false_explicit_accepted(
        self,
    ) -> None:
        payload = self._valid_payload()
        payload["parallel_invoice_stream_indicator"] = False
        row = CollaboratorShareRegistryRow(**payload)
        assert row.parallel_invoice_stream_indicator is False

    def test_parallel_invoice_stream_indicator_rejects_non_bool_string(
        self,
    ) -> None:
        # Pydantic strict-ish bool: free-form strings like "maybe" must FAIL.
        # (Standard "true" / "false" / "1" / "0" coercions are accepted by
        # Pydantic v2 and are tested elsewhere if needed.)
        payload = self._valid_payload()
        payload["parallel_invoice_stream_indicator"] = "maybe"
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
            "ratifying_decision_id": "D-IH-86-DC",
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
            "ratifying_decision_id": "D-IH-86-DG",
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

    def test_overlay_pct_deviation_override_accepted(self) -> None:
        # Added at Wave R+2 Commit 2 (D-IH-86-EJ): when a
        # bd_commission_overlay row deviates from its 15% default anchor,
        # the OVERRIDE row uses override_kind=overlay_pct_deviation to
        # surface the deviation distinctly from the base row's
        # share_split_deviation.
        payload = self._valid_payload()
        payload["override_kind"] = "overlay_pct_deviation"
        payload["actual_value"] = 20.0  # 20% overlay instead of default 15%
        payload["variance_pct"] = 33.33
        row = CollaboratorRateOverrideRow(**payload)
        assert row.override_kind == "overlay_pct_deviation"

    def test_share_split_deviation_override_still_accepted(self) -> None:
        # Pre-existing override_kind preserved at chassis update (not a
        # regression).
        payload = self._valid_payload()
        payload["override_kind"] = "share_split_deviation"
        row = CollaboratorRateOverrideRow(**payload)
        assert row.override_kind == "share_split_deviation"


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


# =============================================================================
# Wave R+2 Commit 2 additions — 4-base + 1-overlay + methodology gating
# (per D-IH-86-EJ + D-IH-86-EN)
# =============================================================================


class TestNewPatternConstants:
    def test_valid_share_patterns_is_4_base_enum(self) -> None:
        # Pre-rewrite values orchestration_broker_thin_margin + custom MUST
        # no longer appear; the 4-base enumeration is the new SSOT.
        assert VALID_SHARE_PATTERNS == frozenset({
            "deep_partner_65_35",
            "bd_intro_only",
            "joint_venture_aventure",
            "consulting_direct",
        })

    def test_orchestration_broker_pattern_removed(self) -> None:
        assert "orchestration_broker_thin_margin" not in VALID_SHARE_PATTERNS

    def test_custom_pattern_removed(self) -> None:
        assert "custom" not in VALID_SHARE_PATTERNS

    def test_valid_share_overlays_is_singleton(self) -> None:
        # Stage-1 doctrine ships with one overlay only; future overlay
        # families would extend this frozenset.
        assert VALID_SHARE_OVERLAYS == frozenset({"bd_commission_overlay"})

    def test_overlay_base_pairings_table_permits_only_safe_bases(self) -> None:
        # bd_commission_overlay must NOT pair with bd_intro_only (circular)
        # OR joint_venture_aventure (conflates symmetry with asymmetry).
        permitted = VALID_OVERLAY_BASE_PAIRINGS["bd_commission_overlay"]
        assert "consulting_direct" in permitted
        assert "deep_partner_65_35" in permitted
        assert "bd_intro_only" not in permitted
        assert "joint_venture_aventure" not in permitted

    def test_valid_methodology_readiness_is_4_value_enum(self) -> None:
        assert VALID_METHODOLOGY_READINESS == frozenset({
            "methodology_trained",
            "methodology_in_progress",
            "methodology_naive",
            "methodology_not_applicable",
        })

    def test_methodology_permissibility_matrix_covers_all_4_states(self) -> None:
        assert set(METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS.keys()) == \
            VALID_METHODOLOGY_READINESS

    def test_methodology_trained_unlocks_all_4_base_patterns(self) -> None:
        # methodology_trained collaborators get full pattern flexibility.
        assert METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS["methodology_trained"] == \
            VALID_SHARE_PATTERNS

    def test_methodology_in_progress_excludes_joint_venture(self) -> None:
        # Symmetric framing requires equal bench; an in-progress
        # collaborator cannot anchor symmetrically.
        permitted = METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS["methodology_in_progress"]
        assert "joint_venture_aventure" not in permitted
        assert "deep_partner_65_35" in permitted  # in-progress can still earn a 35% share

    def test_methodology_naive_excludes_deep_partner(self) -> None:
        # 35% share presumes methodology contribution; naive cannot fulfil.
        permitted = METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS["methodology_naive"]
        assert "deep_partner_65_35" not in permitted
        assert "joint_venture_aventure" not in permitted
        assert "bd_intro_only" in permitted
        assert "consulting_direct" in permitted

    def test_per_pattern_default_anchors_sum_correctly(self) -> None:
        # bd_intro_only: 85 + 15 = 100 (across-rows when paired with
        # holistika-corporate placeholder; for the single billed
        # collaborator row anchor IS 85/15).
        assert DEFAULT_BD_INTRO_HOLISTIKA_PCT + DEFAULT_BD_INTRO_COLLABORATOR_PCT == 100
        # joint_venture_aventure: 50/50 symmetric
        assert DEFAULT_JOINT_VENTURE_HOLISTIKA_PCT + \
            DEFAULT_JOINT_VENTURE_COLLABORATOR_PCT == 100
        # consulting_direct solo: 100/0
        assert DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_SOLO + \
            DEFAULT_CONSULTING_DIRECT_COLLABORATOR_PCT_SOLO == 100
        # consulting_direct + bd_commission_overlay across-rows:
        # 85 + 0 (base) + 0 + 15 (overlay) = 100
        assert (
            DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_WITH_OVERLAY
            + 0
            + 0
            + DEFAULT_BD_COMMISSION_OVERLAY_PCT
        ) == 100


class TestNewPatternHelpers:
    # -- bd_intro_only --

    def test_bd_intro_default_holds_for_85_15(self) -> None:
        assert bd_intro_default_split_holds(85, 15) is True

    def test_bd_intro_default_false_for_80_20(self) -> None:
        assert bd_intro_default_split_holds(80, 20) is False

    # -- joint_venture_aventure --

    def test_joint_venture_default_holds_for_50_50(self) -> None:
        assert joint_venture_default_split_holds(50, 50) is True

    def test_joint_venture_default_false_for_60_40(self) -> None:
        assert joint_venture_default_split_holds(60, 40) is False

    # -- consulting_direct solo --

    def test_consulting_direct_solo_default_holds_for_100_0(self) -> None:
        assert consulting_direct_solo_default_holds(100, 0) is True

    def test_consulting_direct_solo_default_false_for_85_0(self) -> None:
        # 85/0 is the WITH-overlay anchor, NOT the solo anchor; the
        # solo helper must distinguish.
        assert consulting_direct_solo_default_holds(85, 0) is False

    # -- consulting_direct + overlay --

    def test_consulting_direct_with_overlay_default_holds_for_85_0(self) -> None:
        assert consulting_direct_with_overlay_default_holds(85, 0) is True

    def test_consulting_direct_with_overlay_default_false_for_100_0(self) -> None:
        # 100/0 is the SOLO anchor; with-overlay helper must reject.
        assert consulting_direct_with_overlay_default_holds(100, 0) is False

    # -- bd_commission_overlay row anchor --

    def test_bd_commission_overlay_default_holds_for_0_15(self) -> None:
        assert bd_commission_overlay_default_holds(0, 15) is True

    def test_bd_commission_overlay_default_false_for_0_20(self) -> None:
        assert bd_commission_overlay_default_holds(0, 20) is False

    # -- across-rows sum-to-100 (multi-row engagements) --

    def test_across_rows_sum_to_100_holds_for_bd_intro(self) -> None:
        # bd_intro: row1 = 85/0 holistika-corporate; row2 = 0/15 BD partner
        # → sum = 85 + 0 + 0 + 15 = 100
        rows = [(85, 0), (0, 15)]
        assert across_rows_sum_to_100(rows) is True

    def test_across_rows_sum_to_100_holds_for_joint_venture(self) -> None:
        rows = [(50, 0), (0, 50)]
        assert across_rows_sum_to_100(rows) is True

    def test_across_rows_sum_to_100_holds_for_consulting_plus_overlay(self) -> None:
        # SUEZ corrected commercial: 85/0 base + 0/15 overlay
        rows = [(85, 0), (0, 15)]
        assert across_rows_sum_to_100(rows) is True

    def test_across_rows_sum_to_100_fails_when_short(self) -> None:
        rows = [(80, 0), (0, 15)]  # 95 total
        assert across_rows_sum_to_100(rows) is False

    def test_across_rows_sum_to_100_empty_list_returns_false(self) -> None:
        assert across_rows_sum_to_100([]) is False

    # -- enum validity helpers --

    def test_share_pattern_is_valid_for_4_base(self) -> None:
        assert share_pattern_is_valid("deep_partner_65_35") is True
        assert share_pattern_is_valid("bd_intro_only") is True
        assert share_pattern_is_valid("joint_venture_aventure") is True
        assert share_pattern_is_valid("consulting_direct") is True

    def test_share_pattern_is_valid_rejects_pre_rewrite_values(self) -> None:
        assert share_pattern_is_valid("orchestration_broker_thin_margin") is False
        assert share_pattern_is_valid("custom") is False

    def test_share_overlay_is_valid_accepts_empty(self) -> None:
        # Empty string means no overlay declared — must not flag CS-08 FAIL.
        assert share_overlay_is_valid("") is True

    def test_share_overlay_is_valid_accepts_bd_commission(self) -> None:
        assert share_overlay_is_valid("bd_commission_overlay") is True

    def test_share_overlay_is_valid_rejects_unknown(self) -> None:
        assert share_overlay_is_valid("made_up_overlay") is False

    def test_methodology_readiness_is_valid_for_4_states(self) -> None:
        for value in VALID_METHODOLOGY_READINESS:
            assert methodology_readiness_is_valid(value) is True

    def test_methodology_readiness_is_valid_rejects_unknown(self) -> None:
        assert methodology_readiness_is_valid("methodology_oracle") is False

    # -- overlay-base pairing (CS-09 mechanical core) --

    def test_overlay_base_pairing_valid_for_consulting_direct(self) -> None:
        assert overlay_base_pairing_is_valid(
            "bd_commission_overlay", ["consulting_direct"]
        ) is True

    def test_overlay_base_pairing_valid_for_deep_partner(self) -> None:
        assert overlay_base_pairing_is_valid(
            "bd_commission_overlay", ["deep_partner_65_35"]
        ) is True

    def test_overlay_base_pairing_invalid_for_bd_intro_only(self) -> None:
        # Forbidden pairing: circular (overlay would restate the BD pattern).
        assert overlay_base_pairing_is_valid(
            "bd_commission_overlay", ["bd_intro_only"]
        ) is False

    def test_overlay_base_pairing_invalid_for_joint_venture(self) -> None:
        # Forbidden pairing: conflates symmetry with intro-asymmetry.
        assert overlay_base_pairing_is_valid(
            "bd_commission_overlay", ["joint_venture_aventure"]
        ) is False

    def test_overlay_base_pairing_no_overlay_returns_true(self) -> None:
        # No overlay declared → no constraint to verify.
        assert overlay_base_pairing_is_valid("", ["bd_intro_only"]) is True

    def test_overlay_base_pairing_empty_base_list_with_overlay_returns_false(self) -> None:
        # An overlay row without a sibling base row is structurally invalid.
        assert overlay_base_pairing_is_valid("bd_commission_overlay", []) is False

    # -- methodology permissibility (CS-08 extension) --

    def test_methodology_permits_share_pattern_trained_x_deep_partner(self) -> None:
        assert methodology_permits_share_pattern(
            "methodology_trained", "deep_partner_65_35"
        ) is True

    def test_methodology_permits_share_pattern_trained_x_joint_venture(self) -> None:
        assert methodology_permits_share_pattern(
            "methodology_trained", "joint_venture_aventure"
        ) is True

    def test_methodology_permits_share_pattern_naive_x_deep_partner_blocked(self) -> None:
        # Load-bearing test for the operator's "35% bridges a methodology
        # gap" failure mode prevention.
        assert methodology_permits_share_pattern(
            "methodology_naive", "deep_partner_65_35"
        ) is False

    def test_methodology_permits_share_pattern_naive_x_bd_intro_allowed(self) -> None:
        assert methodology_permits_share_pattern(
            "methodology_naive", "bd_intro_only"
        ) is True

    def test_methodology_permits_share_pattern_in_progress_x_joint_venture_blocked(
        self,
    ) -> None:
        assert methodology_permits_share_pattern(
            "methodology_in_progress", "joint_venture_aventure"
        ) is False

    def test_methodology_permits_share_pattern_rejects_unknown_pattern(self) -> None:
        assert methodology_permits_share_pattern(
            "methodology_trained", "orchestration_broker_thin_margin"
        ) is False

    def test_methodology_permits_share_pattern_rejects_unknown_readiness(self) -> None:
        assert methodology_permits_share_pattern(
            "methodology_godlike", "deep_partner_65_35"
        ) is False


class TestCheckCodeEnumExtension:
    def test_cs_09_check_code_registered(self) -> None:
        assert "CS-09-OVERLAY-BASE-PAIRING-VALIDITY" in \
            VALID_COLLABORATOR_SHARE_CHECK_CODES

    def test_cs_08_check_code_still_registered(self) -> None:
        # CS-08 is preserved; the rewrite extends it semantically (overlay +
        # methodology validity) but the check_code string stays the same.
        assert "CS-08-SHARE-PATTERN-ENUM-VALIDITY" in \
            VALID_COLLABORATOR_SHARE_CHECK_CODES

    def test_all_9_check_codes_present(self) -> None:
        # CS-01..CS-09 — the post-rewrite full enum.
        assert len(VALID_COLLABORATOR_SHARE_CHECK_CODES) == 9

    def test_override_kind_enum_includes_overlay_pct_deviation(self) -> None:
        assert "overlay_pct_deviation" in VALID_OVERRIDE_KINDS

    def test_override_kind_enum_has_3_values(self) -> None:
        # market_rate_excursion + share_split_deviation +
        # overlay_pct_deviation
        assert len(VALID_OVERRIDE_KINDS) == 3
