#!/usr/bin/env python3
"""Stripe metadata audit runbook — surface counterparty-resolution risk before it hits the writer.

Initiative 81 Phase 2 Bundle B-2b paired runbook (D-IH-81-W under D-IH-81-G umbrella,
2026-05-23). Paired with SOP-EXTERNAL_STRIPE_METADATA_AUDIT_001 (Bundle B-2c will mint
the SOP). Authored to the I72 P9 plan-quality bar (Pydantic models; type-annotated;
structured logging; pathlib + os.environ; tests at tests/test_stripe_audit_metadata.py).

PURPOSE
-------
The finops-writer-worker (Bundle B-2b) resolves counterparty ids via the R1 engagement-
model-aware router. The router's first two resolution strategies depend on Stripe metadata
being set correctly on Customer + Subscription objects:

  - ``metadata.hlk_engagement_id`` — direct hit (highest confidence; SaaS subscription class)
  - ``metadata.hlk_billing_plane`` — plane discriminator (``kirbe`` vs ``holistika_ops``)

When neither key is set, the router falls back to ``stripe_customer_link`` table lookup
(consultancy + RPP class) and finally to ``manual_review`` (emits OPS-NN row).

This runbook walks the Stripe AT environment + production environment looking for:

1. **Stripe Customers with no ``hlk_billing_plane``** — orphan customers; will route to
   default_kirbe and may end up in the wrong reconciliation bucket.
2. **Stripe Subscriptions with ``metadata.hlk_billing_plane = holistika_ops`` but no
   matching ``stripe_customer_link`` row in holistika_ops** — referential drift; the
   counterparty router will fall through to manual_review when these subscriptions
   eventually generate ``charge.succeeded`` events.
3. **Stripe Customers with ``hlk_billing_plane = holistika_ops`` but no
   ``hlk_engagement_id``** — works today via Layer 3 (stripe_customer_link), but loses
   high-confidence direct-hit resolution.

OUTPUT: a CSV/JSON report at ``artifacts/stripe-audit-metadata-<YYYY-MM-DD>.{csv,json}``
plus an optional OPS-NN row append (per --emit-ops) for each finding class.

EXIT CODES
----------
- ``0`` — clean exit (audit completed; findings present in report).
- ``1`` — operator-blocking error (Stripe / Supabase credentials missing; API rate limit).

USAGE
-----
::

    # Self-test (no Stripe / Supabase connection; verifies Pydantic chassis)
    py scripts/stripe_audit_metadata.py --self-test

    # Audit Stripe AT environment (test mode)
    py scripts/stripe_audit_metadata.py --env at --output artifacts/stripe-audit-metadata-AT-$(date +%F).json

    # Audit Stripe production (live mode)
    py scripts/stripe_audit_metadata.py --env prod --output artifacts/stripe-audit-metadata-PROD-$(date +%F).json

    # Append OPS-NN row per finding class (operator-explicit; never default)
    py scripts/stripe_audit_metadata.py --env at --emit-ops

CONTRACTS HONOURED
------------------
- ``akos-executable-process-catalog.mdc`` Rule 1 SOP+runbook pairing — SOP minted at
  Bundle B-2c with AC-HUMAN + AC-AUTOMATION acceptance.
- ``akos-holistika-operations.mdc`` two-plane model — never mutates compliance.* mirror
  data; reads from Stripe + holistika_ops.stripe_customer_link only.
- ``akos-brand-baseline-reality.mdc`` — output report uses internal CORPINT register
  (this is an operator-internal audit artifact; never rendered externally).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.log import setup_logging  # noqa: E402


# =============================================================================
# §1 — Pydantic models (FROZEN; per CONTRIBUTING.md §Python Code Standards)
# =============================================================================


FindingClass = Literal[
    "orphan_customer_no_plane",
    "subscription_plane_holistika_no_link",
    "customer_plane_holistika_no_engagement_id",
]

ALL_FINDING_CLASSES: tuple[FindingClass, ...] = (
    "orphan_customer_no_plane",
    "subscription_plane_holistika_no_link",
    "customer_plane_holistika_no_engagement_id",
)


class StripeMetadataFinding(BaseModel):
    """A single audit finding from the Stripe metadata sweep."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    finding_class: FindingClass = Field(..., description="enum; see ALL_FINDING_CLASSES")
    stripe_object_id: str = Field(..., min_length=1, description="cus_xxx or sub_xxx")
    stripe_object_type: Literal["customer", "subscription"]
    livemode: bool
    created_at: str = Field(..., description="ISO-8601 timestamp from Stripe")
    metadata_snapshot: dict[str, str] = Field(default_factory=dict, description="full metadata at time of audit")
    recommended_action: str = Field(..., description="operator-facing remediation hint")


class StripeAuditReport(BaseModel):
    """Aggregated report from a single audit run — header + finding list."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    env: Literal["at", "prod"]
    audited_at: str
    stripe_account_id: str | None = None
    total_customers_scanned: int = 0
    total_subscriptions_scanned: int = 0
    findings: list[StripeMetadataFinding] = Field(default_factory=list)
    finding_class_counts: dict[str, int] = Field(default_factory=dict)
    blocking_errors: list[str] = Field(default_factory=list)


# =============================================================================
# §2 — Environment + client construction (lazy)
# =============================================================================


def _stripe_key_env_var(env: str) -> str:
    """Return the env var name carrying the Stripe secret key for the given environment."""
    return "STRIPE_SECRET_KEY_AT" if env == "at" else "STRIPE_SECRET_KEY"


def _stripe_env_ok(env: str) -> tuple[bool, str]:
    """Return (ok, reason). Used by --self-test and by audit paths."""
    key_var = _stripe_key_env_var(env)
    if not os.environ.get(key_var, "").strip():
        return False, f"{key_var} not set"
    return True, ""


def _supabase_env_ok() -> tuple[bool, str]:
    if not os.environ.get("SUPABASE_URL", "").strip():
        return False, "SUPABASE_URL not set"
    if not os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip():
        return False, "SUPABASE_SERVICE_ROLE_KEY not set"
    return True, ""


def _make_stripe_client(env: str):  # pragma: no cover — runtime path
    try:
        import stripe
    except ImportError as exc:
        raise RuntimeError(
            "stripe python client is not installed; "
            "install via 'pip install stripe' before invoking audit paths.",
        ) from exc
    stripe.api_key = os.environ[_stripe_key_env_var(env)]
    return stripe


def _make_supabase_client():  # pragma: no cover — runtime path
    try:
        from supabase import create_client
    except ImportError as exc:
        raise RuntimeError(
            "supabase python client is not installed; "
            "install via 'pip install supabase' before invoking audit paths.",
        ) from exc
    return create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_ROLE_KEY"],
    )


# =============================================================================
# §3 — Per-object audit predicates (PURE; unit-testable)
# =============================================================================


def classify_customer(
    customer_id: str,
    livemode: bool,
    created_at: str,
    metadata: dict[str, str] | None,
    has_stripe_customer_link: bool,
) -> list[StripeMetadataFinding]:
    """Apply finding-class predicates to a single Stripe customer.

    Pure function: no Stripe API + no Supabase calls. Caller must supply pre-fetched
    metadata + has_stripe_customer_link flag. Test fixtures cover every branch.
    """
    findings: list[StripeMetadataFinding] = []
    metadata = metadata or {}
    plane = (metadata.get("hlk_billing_plane") or "").strip().lower()

    # Finding 1: orphan — no plane label at all.
    if plane == "":
        findings.append(
            StripeMetadataFinding(
                finding_class="orphan_customer_no_plane",
                stripe_object_id=customer_id,
                stripe_object_type="customer",
                livemode=livemode,
                created_at=created_at,
                metadata_snapshot=metadata,
                recommended_action=(
                    "Operator: set metadata.hlk_billing_plane to 'kirbe' or 'holistika_ops' "
                    "on the Stripe customer; re-run audit to confirm."
                ),
            )
        )
        return findings  # no further checks for orphan customers

    # Finding 3: customer is holistika_ops but no engagement_id (loses Layer 1 confidence).
    if plane in ("holistika_ops", "holistika"):
        if not metadata.get("hlk_engagement_id"):
            findings.append(
                StripeMetadataFinding(
                    finding_class="customer_plane_holistika_no_engagement_id",
                    stripe_object_id=customer_id,
                    stripe_object_type="customer",
                    livemode=livemode,
                    created_at=created_at,
                    metadata_snapshot=metadata,
                    recommended_action=(
                        "Operator: set metadata.hlk_engagement_id to the matching "
                        "ENGAGEMENT_REGISTRY id; preserves high-confidence direct-hit resolution."
                    ),
                )
            )
        # Note: stripe_customer_link absence is not a customer finding — only a subscription finding.
        # (Customer-level routing is plane → has_link → manual_review; absence is non-blocking.)
        _ = has_stripe_customer_link  # documented; not currently a customer-level finding

    return findings


def classify_subscription(
    subscription_id: str,
    customer_id: str | None,
    livemode: bool,
    created_at: str,
    metadata: dict[str, str] | None,
    customer_has_stripe_customer_link: bool,
) -> list[StripeMetadataFinding]:
    """Apply finding-class predicates to a single Stripe subscription.

    Pure function. Caller must supply pre-fetched metadata + customer link flag.
    """
    findings: list[StripeMetadataFinding] = []
    metadata = metadata or {}
    plane = (metadata.get("hlk_billing_plane") or "").strip().lower()

    # Finding 2: subscription plane is holistika but customer has no stripe_customer_link.
    # This is the high-risk finding — when the subscription generates charge events, the
    # router will fall through to manual_review and emit an OPS row per event.
    if plane in ("holistika_ops", "holistika") and not customer_has_stripe_customer_link:
        findings.append(
            StripeMetadataFinding(
                finding_class="subscription_plane_holistika_no_link",
                stripe_object_id=subscription_id,
                stripe_object_type="subscription",
                livemode=livemode,
                created_at=created_at,
                metadata_snapshot={
                    **metadata,
                    "_audit_customer_id": customer_id or "<no_customer>",
                },
                recommended_action=(
                    "Operator: insert a row into holistika_ops.stripe_customer_link for "
                    f"stripe_customer_id={customer_id} with the matching counterparty_id "
                    "before subscription generates charge events; otherwise every charge "
                    "will fall through to manual_review."
                ),
            )
        )

    return findings


# =============================================================================
# §4 — Self-test (verifies wiring without Stripe / Supabase connection)
# =============================================================================


def run_self_test(logger: logging.Logger) -> bool:
    """Exercise Pydantic chassis + classification predicates without external calls."""
    try:
        # Predicate 1: orphan customer
        findings_o = classify_customer(
            customer_id="cus_self_test_orphan",
            livemode=False,
            created_at="2026-05-23T12:00:00+00:00",
            metadata={},
            has_stripe_customer_link=False,
        )
        if len(findings_o) != 1 or findings_o[0].finding_class != "orphan_customer_no_plane":
            logger.error("self-test predicate 1 (orphan_customer) FAIL: got %s", findings_o)
            return False

        # Predicate 3: customer plane holistika no engagement_id
        findings_h = classify_customer(
            customer_id="cus_self_test_holistika_no_eid",
            livemode=False,
            created_at="2026-05-23T12:00:00+00:00",
            metadata={"hlk_billing_plane": "holistika_ops"},
            has_stripe_customer_link=True,
        )
        if (
            len(findings_h) != 1
            or findings_h[0].finding_class != "customer_plane_holistika_no_engagement_id"
        ):
            logger.error("self-test predicate 3 (no_eid) FAIL: got %s", findings_h)
            return False

        # Predicate 2: subscription plane holistika no link
        findings_s = classify_subscription(
            subscription_id="sub_self_test_no_link",
            customer_id="cus_self_test_x",
            livemode=False,
            created_at="2026-05-23T12:00:00+00:00",
            metadata={"hlk_billing_plane": "holistika_ops"},
            customer_has_stripe_customer_link=False,
        )
        if (
            len(findings_s) != 1
            or findings_s[0].finding_class != "subscription_plane_holistika_no_link"
        ):
            logger.error("self-test predicate 2 (no_link) FAIL: got %s", findings_s)
            return False

        # Healthy paths should yield no findings
        empty_findings_c = classify_customer(
            customer_id="cus_healthy",
            livemode=False,
            created_at="2026-05-23T12:00:00+00:00",
            metadata={
                "hlk_billing_plane": "holistika_ops",
                "hlk_engagement_id": "eng_xyz",
            },
            has_stripe_customer_link=True,
        )
        if len(empty_findings_c) != 0:
            logger.error("self-test healthy customer FAIL: got %s", empty_findings_c)
            return False

        empty_findings_s = classify_subscription(
            subscription_id="sub_healthy",
            customer_id="cus_healthy",
            livemode=False,
            created_at="2026-05-23T12:00:00+00:00",
            metadata={"hlk_billing_plane": "kirbe"},
            customer_has_stripe_customer_link=False,  # kirbe doesn't need a link
        )
        if len(empty_findings_s) != 0:
            logger.error("self-test healthy subscription FAIL: got %s", empty_findings_s)
            return False

        # Report assembly
        StripeAuditReport(
            env="at",
            audited_at=_now_utc_iso(),
            total_customers_scanned=2,
            total_subscriptions_scanned=2,
            findings=findings_o + findings_h + findings_s,
            finding_class_counts={
                "orphan_customer_no_plane": 1,
                "customer_plane_holistika_no_engagement_id": 1,
                "subscription_plane_holistika_no_link": 1,
            },
        )

    except Exception as exc:  # noqa: BLE001
        logger.error("self-test: chassis failure: %s", exc)
        return False

    logger.info(
        "self-test PASS: 3 finding predicates + 2 healthy paths + 1 report aggregate; %d finding classes total",
        len(ALL_FINDING_CLASSES),
    )
    return True


# =============================================================================
# §5 — Audit orchestrator (online; not unit-tested — integration tests cover this)
# =============================================================================


def run_audit(  # pragma: no cover — exercised by integration tests + manual runs
    logger: logging.Logger,
    env: Literal["at", "prod"],
    customer_limit: int = 100,
    subscription_limit: int = 100,
) -> StripeAuditReport:
    """Walk Stripe customers + subscriptions; classify; return report."""
    ok_s, reason_s = _stripe_env_ok(env)
    ok_sb, reason_sb = _supabase_env_ok()
    if not (ok_s and ok_sb):
        return StripeAuditReport(
            env=env,
            audited_at=_now_utc_iso(),
            blocking_errors=[r for r in (reason_s, reason_sb) if r],
        )

    stripe_client = _make_stripe_client(env)
    sb_client = _make_supabase_client()

    # Index existing stripe_customer_link rows once.
    link_rows = (
        sb_client.schema("holistika_ops")
        .from_("stripe_customer_link")
        .select("stripe_customer_id")
        .execute()
    )
    linked_customer_ids: set[str] = set()
    if link_rows.data:
        for r in link_rows.data:
            cid = (r or {}).get("stripe_customer_id")
            if cid:
                linked_customer_ids.add(cid)

    findings: list[StripeMetadataFinding] = []
    counts: dict[str, int] = {fc: 0 for fc in ALL_FINDING_CLASSES}
    customer_count = 0
    subscription_count = 0

    # Walk customers
    for cust in stripe_client.Customer.list(limit=customer_limit).auto_paging_iter():
        customer_count += 1
        these = classify_customer(
            customer_id=cust.id,
            livemode=getattr(cust, "livemode", env == "prod"),
            created_at=datetime.fromtimestamp(cust.created, tz=timezone.utc).isoformat(),
            metadata=dict(cust.metadata or {}),
            has_stripe_customer_link=(cust.id in linked_customer_ids),
        )
        for f in these:
            findings.append(f)
            counts[f.finding_class] += 1

    # Walk subscriptions
    for sub in stripe_client.Subscription.list(
        limit=subscription_limit, status="all"
    ).auto_paging_iter():
        subscription_count += 1
        cid_obj = getattr(sub, "customer", None)
        cid = cid_obj if isinstance(cid_obj, str) else getattr(cid_obj, "id", None)
        these = classify_subscription(
            subscription_id=sub.id,
            customer_id=cid,
            livemode=getattr(sub, "livemode", env == "prod"),
            created_at=datetime.fromtimestamp(sub.created, tz=timezone.utc).isoformat(),
            metadata=dict(sub.metadata or {}),
            customer_has_stripe_customer_link=(cid in linked_customer_ids if cid else False),
        )
        for f in these:
            findings.append(f)
            counts[f.finding_class] += 1

    return StripeAuditReport(
        env=env,
        audited_at=_now_utc_iso(),
        total_customers_scanned=customer_count,
        total_subscriptions_scanned=subscription_count,
        findings=findings,
        finding_class_counts={k: v for k, v in counts.items() if v > 0},
    )


# =============================================================================
# §6 — Output helpers
# =============================================================================


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_report(report: StripeAuditReport, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".csv":
        _write_report_csv(report, output_path)
    else:
        output_path.write_text(json.dumps(report.model_dump(), indent=2, sort_keys=True), encoding="utf-8")


def _write_report_csv(report: StripeAuditReport, output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "finding_class",
                "stripe_object_id",
                "stripe_object_type",
                "livemode",
                "created_at",
                "metadata_snapshot",
                "recommended_action",
            ]
        )
        for f in report.findings:
            writer.writerow(
                [
                    f.finding_class,
                    f.stripe_object_id,
                    f.stripe_object_type,
                    f.livemode,
                    f.created_at,
                    json.dumps(f.metadata_snapshot, sort_keys=True),
                    f.recommended_action,
                ]
            )


# =============================================================================
# §7 — CLI
# =============================================================================


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="stripe_audit_metadata",
        description=__doc__.splitlines()[0] if __doc__ else "Stripe metadata audit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true", help="verify chassis without external calls")
    mode.add_argument(
        "--env",
        choices=("at", "prod"),
        help="Stripe environment to audit: 'at' (test) or 'prod' (live)",
    )

    p.add_argument(
        "--output",
        type=Path,
        help="output path (default: artifacts/stripe-audit-metadata-<ENV>-<YYYY-MM-DD>.json)",
    )
    p.add_argument("--customer-limit", type=int, default=100)
    p.add_argument("--subscription-limit", type=int, default=100)
    p.add_argument(
        "--emit-ops",
        action="store_true",
        help="append OPS-NN row per finding class (operator-explicit; never default)",
    )
    p.add_argument("--json-log", action="store_true", help="JSON log output (machine-readable)")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(json_output=args.json_log)
    logger = logging.getLogger("stripe_audit_metadata")

    if args.self_test:
        return 0 if run_self_test(logger) else 1

    output = args.output or (
        REPO_ROOT
        / "artifacts"
        / f"stripe-audit-metadata-{args.env.upper()}-{datetime.now(timezone.utc).date().isoformat()}.json"
    )

    report = run_audit(
        logger,
        env=args.env,
        customer_limit=args.customer_limit,
        subscription_limit=args.subscription_limit,
    )
    if report.blocking_errors:
        for err in report.blocking_errors:
            print(f"BLOCKING: {err}", file=sys.stderr)
        return 1

    _write_report(report, output)
    print(f"audit complete: env={args.env} customers={report.total_customers_scanned} "
          f"subscriptions={report.total_subscriptions_scanned} findings={len(report.findings)}")
    print(f"report: {output}")
    if args.emit_ops and report.findings:
        print(
            "NOTE: --emit-ops requested but OPS_REGISTER append is handled by "
            "the Edge Function worker, not this runbook. Recommend the operator "
            "review the report + append per-finding-class OPS rows manually for "
            "this initial release window."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
