"""Tests for scripts/stripe_audit_metadata.py operator runbook.

Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W under D-IH-81-G umbrella, 2026-05-23).

Covers:
- Pydantic chassis: StripeMetadataFinding + StripeAuditReport construction + frozen.
- Classification predicates (PURE functions; no Stripe / Supabase calls):
  - classify_customer: orphan_customer_no_plane + customer_plane_holistika_no_engagement_id + healthy.
  - classify_subscription: subscription_plane_holistika_no_link + healthy kirbe path.
- Self-test path runs cleanly without external connections.
- CLI smoke: --self-test exits 0; missing mode flag exits non-zero.
- Output helpers: JSON + CSV round-trip.

These tests run under the default `py scripts/test.py all` collection via the implicit
`tests/test_*.py` glob.
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stripe_audit_metadata  # noqa: E402
from stripe_audit_metadata import (  # noqa: E402
    ALL_FINDING_CLASSES,
    StripeAuditReport,
    StripeMetadataFinding,
    classify_customer,
    classify_subscription,
    run_self_test,
)


# -----------------------------------------------------------------------------
# Pydantic chassis
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestPydanticChassis:
    def test_finding_valid(self) -> None:
        f = StripeMetadataFinding(
            finding_class="orphan_customer_no_plane",
            stripe_object_id="cus_test",
            stripe_object_type="customer",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            recommended_action="Set hlk_billing_plane",
        )
        assert f.finding_class == "orphan_customer_no_plane"
        assert f.metadata_snapshot == {}

    def test_finding_frozen(self) -> None:
        f = StripeMetadataFinding(
            finding_class="orphan_customer_no_plane",
            stripe_object_id="cus_x",
            stripe_object_type="customer",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            recommended_action="x",
        )
        with pytest.raises((TypeError, ValueError, ValidationError)):
            f.finding_class = "subscription_plane_holistika_no_link"  # type: ignore[misc]

    def test_finding_rejects_invalid_class(self) -> None:
        with pytest.raises(ValidationError):
            StripeMetadataFinding(
                finding_class="bogus_class",  # type: ignore[arg-type]
                stripe_object_id="cus_x",
                stripe_object_type="customer",
                livemode=False,
                created_at="2026-05-23T00:00:00+00:00",
                recommended_action="x",
            )

    def test_finding_rejects_invalid_object_type(self) -> None:
        with pytest.raises(ValidationError):
            StripeMetadataFinding(
                finding_class="orphan_customer_no_plane",
                stripe_object_id="cus_x",
                stripe_object_type="charge",  # type: ignore[arg-type]
                livemode=False,
                created_at="2026-05-23T00:00:00+00:00",
                recommended_action="x",
            )

    def test_report_default_factories(self) -> None:
        r = StripeAuditReport(env="at", audited_at="2026-05-23T00:00:00+00:00")
        assert r.findings == []
        assert r.finding_class_counts == {}
        assert r.blocking_errors == []

    def test_all_finding_classes_constant_complete(self) -> None:
        assert "orphan_customer_no_plane" in ALL_FINDING_CLASSES
        assert "subscription_plane_holistika_no_link" in ALL_FINDING_CLASSES
        assert "customer_plane_holistika_no_engagement_id" in ALL_FINDING_CLASSES
        assert len(ALL_FINDING_CLASSES) == 3


# -----------------------------------------------------------------------------
# classify_customer predicate
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestClassifyCustomer:
    def test_orphan_no_plane_label(self) -> None:
        findings = classify_customer(
            customer_id="cus_orphan",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={},
            has_stripe_customer_link=False,
        )
        assert len(findings) == 1
        assert findings[0].finding_class == "orphan_customer_no_plane"
        assert findings[0].stripe_object_id == "cus_orphan"

    def test_orphan_no_plane_with_other_metadata(self) -> None:
        findings = classify_customer(
            customer_id="cus_orphan2",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"random_key": "random_value"},
            has_stripe_customer_link=True,
        )
        assert len(findings) == 1
        assert findings[0].finding_class == "orphan_customer_no_plane"

    def test_orphan_short_circuits_other_checks(self) -> None:
        """Orphan finding returns immediately; no follow-on findings."""
        findings = classify_customer(
            customer_id="cus_orphan_no_eid",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={},
            has_stripe_customer_link=False,
        )
        assert len(findings) == 1  # only orphan; no "no_engagement_id" since no plane to check

    def test_holistika_plane_no_engagement_id_flagged(self) -> None:
        findings = classify_customer(
            customer_id="cus_holistika_no_eid",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"hlk_billing_plane": "holistika_ops"},
            has_stripe_customer_link=True,
        )
        assert len(findings) == 1
        assert findings[0].finding_class == "customer_plane_holistika_no_engagement_id"

    def test_holistika_alias_short_form_accepted(self) -> None:
        """The classifier should accept both 'holistika_ops' and 'holistika' as plane labels."""
        findings = classify_customer(
            customer_id="cus_holistika_alias",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"hlk_billing_plane": "holistika"},
            has_stripe_customer_link=True,
        )
        assert len(findings) == 1
        assert findings[0].finding_class == "customer_plane_holistika_no_engagement_id"

    def test_holistika_plane_with_engagement_id_healthy(self) -> None:
        findings = classify_customer(
            customer_id="cus_holistika_healthy",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={
                "hlk_billing_plane": "holistika_ops",
                "hlk_engagement_id": "eng_xyz_123",
            },
            has_stripe_customer_link=True,
        )
        assert findings == []

    def test_kirbe_plane_healthy_no_findings(self) -> None:
        findings = classify_customer(
            customer_id="cus_kirbe_user",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"hlk_billing_plane": "kirbe"},
            has_stripe_customer_link=False,
        )
        assert findings == []

    def test_plane_label_case_insensitive(self) -> None:
        """Plane label normalises to lowercase before comparison."""
        findings = classify_customer(
            customer_id="cus_holistika_upper",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"hlk_billing_plane": "HOLISTIKA_OPS"},
            has_stripe_customer_link=True,
        )
        assert len(findings) == 1
        assert findings[0].finding_class == "customer_plane_holistika_no_engagement_id"


# -----------------------------------------------------------------------------
# classify_subscription predicate
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestClassifySubscription:
    def test_holistika_subscription_no_link_flagged(self) -> None:
        findings = classify_subscription(
            subscription_id="sub_holistika_no_link",
            customer_id="cus_x",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"hlk_billing_plane": "holistika_ops"},
            customer_has_stripe_customer_link=False,
        )
        assert len(findings) == 1
        assert findings[0].finding_class == "subscription_plane_holistika_no_link"
        # Customer id is captured in metadata snapshot for operator triage
        assert findings[0].metadata_snapshot.get("_audit_customer_id") == "cus_x"

    def test_holistika_subscription_with_link_healthy(self) -> None:
        findings = classify_subscription(
            subscription_id="sub_holistika_linked",
            customer_id="cus_x",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"hlk_billing_plane": "holistika_ops"},
            customer_has_stripe_customer_link=True,
        )
        assert findings == []

    def test_kirbe_subscription_healthy_no_link_required(self) -> None:
        findings = classify_subscription(
            subscription_id="sub_kirbe",
            customer_id="cus_kirbe",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"hlk_billing_plane": "kirbe"},
            customer_has_stripe_customer_link=False,
        )
        assert findings == []

    def test_orphan_subscription_no_plane_not_flagged_at_subscription_level(self) -> None:
        """Orphan plane is a customer-level finding only; subscription-level orphans
        roll up through their customer record."""
        findings = classify_subscription(
            subscription_id="sub_orphan",
            customer_id="cus_orphan",
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={},
            customer_has_stripe_customer_link=False,
        )
        assert findings == []

    def test_subscription_with_null_customer_id_still_safe(self) -> None:
        findings = classify_subscription(
            subscription_id="sub_orphan_no_cust",
            customer_id=None,
            livemode=False,
            created_at="2026-05-23T00:00:00+00:00",
            metadata={"hlk_billing_plane": "holistika_ops"},
            customer_has_stripe_customer_link=False,
        )
        assert len(findings) == 1
        assert findings[0].metadata_snapshot.get("_audit_customer_id") == "<no_customer>"


# -----------------------------------------------------------------------------
# Self-test path
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestSelfTest:
    def test_self_test_passes(self, caplog: pytest.LogCaptureFixture) -> None:
        import logging

        logger = logging.getLogger("test_stripe_audit_metadata.self_test")
        caplog.set_level("INFO")
        assert run_self_test(logger) is True


# -----------------------------------------------------------------------------
# Output helpers
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestOutputHelpers:
    def _sample_report(self) -> StripeAuditReport:
        return StripeAuditReport(
            env="at",
            audited_at="2026-05-23T00:00:00+00:00",
            total_customers_scanned=10,
            total_subscriptions_scanned=5,
            findings=[
                StripeMetadataFinding(
                    finding_class="orphan_customer_no_plane",
                    stripe_object_id="cus_test_1",
                    stripe_object_type="customer",
                    livemode=False,
                    created_at="2026-05-23T00:00:00+00:00",
                    metadata_snapshot={},
                    recommended_action="set plane",
                ),
                StripeMetadataFinding(
                    finding_class="subscription_plane_holistika_no_link",
                    stripe_object_id="sub_test_1",
                    stripe_object_type="subscription",
                    livemode=False,
                    created_at="2026-05-23T00:00:00+00:00",
                    metadata_snapshot={"hlk_billing_plane": "holistika_ops"},
                    recommended_action="insert link row",
                ),
            ],
            finding_class_counts={
                "orphan_customer_no_plane": 1,
                "subscription_plane_holistika_no_link": 1,
            },
        )

    def test_json_output_roundtrip(self, tmp_path: Path) -> None:
        report = self._sample_report()
        output_path = tmp_path / "report.json"
        stripe_audit_metadata._write_report(report, output_path)
        assert output_path.exists()

        loaded = json.loads(output_path.read_text(encoding="utf-8"))
        assert loaded["env"] == "at"
        assert loaded["total_customers_scanned"] == 10
        assert len(loaded["findings"]) == 2

    def test_csv_output_has_header_and_rows(self, tmp_path: Path) -> None:
        report = self._sample_report()
        output_path = tmp_path / "report.csv"
        stripe_audit_metadata._write_report(report, output_path)
        assert output_path.exists()

        with output_path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            rows = list(reader)
        assert rows[0][0] == "finding_class"
        assert len(rows) == 1 + 2  # header + 2 findings


# -----------------------------------------------------------------------------
# CLI smoke (subprocess)
# -----------------------------------------------------------------------------


class TestCliSmoke:
    def test_self_test_cli_exits_zero(self) -> None:
        env = {**os.environ}
        for var in ("STRIPE_SECRET_KEY", "STRIPE_SECRET_KEY_AT", "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
            env.pop(var, None)
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "stripe_audit_metadata.py"), "--self-test"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            env=env,
        )
        assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

    def test_no_mode_flag_exits_nonzero(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "stripe_audit_metadata.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode != 0
