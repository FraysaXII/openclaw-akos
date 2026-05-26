"""Unit + integration tests for scripts/collaborator_share_calculate.py.

Wave R+2 doctrine rewrite (D-IH-86-EJ..EN; Commits 1-3) replaced the
pre-rewrite 3-shape share_pattern enum (deep_partner_65_35 /
orchestration_broker_thin_margin / custom) with a 4-base + 1-stackable-
overlay enum:

  Base patterns (4):
    - deep_partner_65_35       (65/35 per-row anchor)
    - bd_intro_only            (85/15 per-row anchor)
    - joint_venture_aventure   (50/50 per-row anchor)
    - consulting_direct        (100/0 SOLO anchor; 85/15 WITH overlay)
  Overlay (1; stackable):
    - bd_commission_overlay    (paired w/ consulting_direct or deep_partner)

The runbook is unified under TRUE-MARGIN: every pattern computes
benefits = revenue - costs and applies each SHARE_REGISTRY row's split
on benefits. Per-pattern behaviour surfaces ONLY as advisory notes
(default-anchor mismatch / methodology eligibility / overlay-base
pairing / parallel-invoice-stream).

This file covers the *runbook arithmetic + JSON shape + CLI surface +
markdown render*. Validator-CLI behaviour lives in
``tests/test_validate_collaborator_share.py``. Pure Pydantic model +
helper coverage lives in ``tests/test_hlk_collaborator_share.py``.

Covers:
- CLI surface (--self-test exits 0; --emit-json produces parseable JSON;
  required args error when missing).
- Pure-function ``calculate_settlement`` arithmetic for each of the 4
  base patterns via what-if CLI override path (no CSV rows present).
- TRUE-MARGIN cost-line collection (founder hours + direct passthroughs
  + vendor billed services).
- Overlay engagement: 2-row CSV fixture (consulting_direct base +
  bd_commission_overlay sibling) verifies per-row breakdown application
  AND across-rows sum-to-100 invariant.
- Advisory note generation for the four advisory classes:
  default-anchor mismatch, methodology-pattern incoherence,
  overlay-base pairing violation, parallel_invoice_stream_indicator.
- JSON output schema matches the new per_row_breakdowns shape.
- Markdown render shape (header table + per-row table + advisory section).
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

RUNBOOK_PATH = REPO_ROOT / "scripts" / "collaborator_share_calculate.py"
PYTHON = sys.executable


# ===========================================================================
# Helpers
# ===========================================================================

def _run_runbook(*args: str) -> subprocess.CompletedProcess:
    """Invoke the runbook CLI with the given args. Returns the CP."""
    return subprocess.run(
        [PYTHON, str(RUNBOOK_PATH), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def _build_share_registry_row(
    share_id: str,
    engagement_id: str,
    share_pattern: str = "deep_partner_65_35",
    share_overlay: str = "",
    holistika_pct: int = 65,
    collaborator_pct: int = 35,
    methodology_readiness: str = "methodology_trained",
    override_id: str = "",
    collaborator_id: str = "POI-PRT-PYTEST",
    collaborator_billed_rate: int = 250,
    parallel_invoice: str = "false",
) -> str:
    """Build a 20-column CSV row aligned with the Wave R+2 SSOT header
    per ``COLLABORATOR_SHARE_REGISTRY_FIELDNAMES``.

    Mirrors the helper in test_validate_collaborator_share.py so both
    test suites stay in lockstep with the chassis.
    """
    return (
        f"{share_id},{engagement_id},{collaborator_id},"
        f"eng_model_percentage_collaborator,{share_pattern},{share_overlay},"
        f"{holistika_pct},{collaborator_pct},"
        f"{collaborator_billed_rate},EUR,advisor,{methodology_readiness},"
        f"{override_id},active,2026-01-01,,,2026-01-01,pytest fixture,"
        f"{parallel_invoice}\n"
    )


def _seed_csv_fixture(
    tmp_path: Path,
    *,
    share_rows: list[str],
    vendor_rows: list[str] | None = None,
) -> tuple[Path, Path]:
    """Seed tmp_path with header-only SHARE_REGISTRY + VENDOR_BILLED CSVs.

    Returns (share_csv_path, vendor_csv_path).
    """
    from akos.hlk_collaborator_share import (
        COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
        HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
    )

    share_csv = tmp_path / "COLLABORATOR_SHARE_REGISTRY.csv"
    share_csv.write_text(
        ",".join(COLLABORATOR_SHARE_REGISTRY_FIELDNAMES) + "\n"
        + "".join(share_rows),
        encoding="utf-8",
    )
    vendor_csv = tmp_path / "HOLISTIKA_VENDOR_SERVICES_BILLED.csv"
    vendor_csv.write_text(
        ",".join(HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES) + "\n"
        + "".join(vendor_rows or []),
        encoding="utf-8",
    )
    return share_csv, vendor_csv


def _point_runbook_at_fixture(
    monkeypatch, csc_mod, share_csv: Path, vendor_csv: Path
) -> None:
    """Repoint the runbook's module-level CSV constants at fixture paths."""
    monkeypatch.setattr(csc_mod, "SHARE_REGISTRY_CSV", share_csv)
    monkeypatch.setattr(csc_mod, "VENDOR_BILLED_CSV", vendor_csv)


@pytest.fixture
def csc_mod():
    """Fresh import of the runbook module per test (so monkeypatched
    attrs reset between tests)."""
    if "scripts.collaborator_share_calculate" in sys.modules:
        return importlib.reload(sys.modules["scripts.collaborator_share_calculate"])
    return importlib.import_module("scripts.collaborator_share_calculate")


# ===========================================================================
# Runbook CLI surface
# ===========================================================================

class TestRunbookCLI:
    def test_runbook_script_exists(self):
        assert RUNBOOK_PATH.is_file(), f"runbook missing at {RUNBOOK_PATH}"

    def test_self_test_exits_zero(self):
        result = _run_runbook("--self-test")
        assert result.returncode == 0, (
            f"--self-test FAIL with exit code {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    def test_missing_required_args_errors(self):
        result = _run_runbook()
        assert result.returncode != 0, (
            "runbook should refuse to run without --engagement-id + "
            "--revenue (and not --self-test)"
        )
        assert (
            "--engagement-id" in result.stderr
            or "--revenue" in result.stderr
        ), f"expected required-args error; got stderr: {result.stderr!r}"

    def test_emit_json_produces_parseable_output(self):
        result = _run_runbook(
            "--engagement-id", "ENG-JSON-SMOKE-2026",
            "--revenue", "100000",
            "--share-pattern", "deep_partner_65_35",
            "--emit-json",
        )
        assert result.returncode == 0, (
            f"--emit-json failed (exit {result.returncode})\nstderr: {result.stderr}"
        )
        payload = json.loads(result.stdout)
        assert isinstance(payload, dict)
        # New per_row_breakdowns shape (Wave R+2; D-IH-86-EM).
        for key in (
            "engagement_id",
            "currency",
            "revenue",
            "cost_lines",
            "total_costs",
            "benefits",
            "primary_row_share_pattern",
            "per_row_breakdowns",
            "across_rows_total_holistika_pct",
            "across_rows_total_collaborator_pct",
            "across_rows_split_sums_to_100",
            "across_rows_holistika_amount",
            "across_rows_collaborator_amount",
            "share_row_present",
            "advisory_notes",
            "computed_at",
        ):
            assert key in payload, f"missing top-level key {key!r} in JSON output"
        assert isinstance(payload["per_row_breakdowns"], list)
        assert isinstance(payload["cost_lines"], list)
        assert isinstance(payload["advisory_notes"], list)

    def test_share_pattern_choices_constrained(self):
        # argparse should reject an unknown share_pattern value
        result = _run_runbook(
            "--engagement-id", "ENG-X",
            "--revenue", "1",
            "--share-pattern", "orchestration_broker_thin_margin",  # post-rewrite removed
        )
        assert result.returncode != 0
        assert "invalid choice" in result.stderr.lower(), (
            f"expected argparse 'invalid choice' rejection for legacy "
            f"share_pattern; got stderr: {result.stderr!r}"
        )


# ===========================================================================
# calculate_settlement — per-pattern arithmetic (what-if CLI override path;
# no CSV rows present)
# ===========================================================================

class TestPerPatternArithmetic:
    """Verify each of the 4 base patterns computes the right per-row
    split application on TRUE-MARGIN benefits when no SHARE_REGISTRY
    row exists yet (synthesized one-row breakdown from CLI override).

    Inputs: revenue=100k, direct_costs=[20k] => benefits=80k.
    """

    REVENUE = 100_000.0
    DIRECT_COST = 20_000.0
    EXPECTED_BENEFITS = 80_000.0

    def _compute(self, csc_mod, pattern: str, eng_id: str) -> dict[str, Any]:
        return csc_mod.calculate_settlement(
            engagement_id=eng_id,
            revenue=self.REVENUE,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[self.DIRECT_COST],
            currency="EUR",
            share_pattern_override=pattern,
        )

    def test_deep_partner_65_35_split(self, csc_mod, tmp_path, monkeypatch):
        # Empty CSVs so what-if path fires.
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = self._compute(csc_mod, "deep_partner_65_35", "ENG-DP-WHATIF")

        assert s["benefits"] == self.EXPECTED_BENEFITS
        assert s["total_costs"] == self.DIRECT_COST
        assert s["primary_row_share_pattern"] == "deep_partner_65_35"
        assert len(s["per_row_breakdowns"]) == 1
        b = s["per_row_breakdowns"][0]
        assert b["holistika_share_pct"] == 65
        assert b["collaborator_share_pct"] == 35
        assert b["holistika_share_amount"] == 52_000.0
        assert b["collaborator_share_amount"] == 28_000.0
        assert b["split_matches_anchor"] is True

    def test_bd_intro_only_split(self, csc_mod, tmp_path, monkeypatch):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = self._compute(csc_mod, "bd_intro_only", "ENG-BD-WHATIF")

        assert s["benefits"] == self.EXPECTED_BENEFITS
        b = s["per_row_breakdowns"][0]
        assert b["share_pattern"] == "bd_intro_only"
        assert b["holistika_share_pct"] == 85
        assert b["collaborator_share_pct"] == 15
        assert b["holistika_share_amount"] == 68_000.0
        assert b["collaborator_share_amount"] == 12_000.0

    def test_joint_venture_aventure_split(self, csc_mod, tmp_path, monkeypatch):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = self._compute(csc_mod, "joint_venture_aventure", "ENG-JV-WHATIF")

        assert s["benefits"] == self.EXPECTED_BENEFITS
        b = s["per_row_breakdowns"][0]
        assert b["share_pattern"] == "joint_venture_aventure"
        assert b["holistika_share_pct"] == 50
        assert b["collaborator_share_pct"] == 50
        assert b["holistika_share_amount"] == 40_000.0
        assert b["collaborator_share_amount"] == 40_000.0

    def test_consulting_direct_solo_split(self, csc_mod, tmp_path, monkeypatch):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = self._compute(csc_mod, "consulting_direct", "ENG-CD-WHATIF")

        assert s["benefits"] == self.EXPECTED_BENEFITS
        b = s["per_row_breakdowns"][0]
        assert b["share_pattern"] == "consulting_direct"
        assert b["holistika_share_pct"] == 100
        assert b["collaborator_share_pct"] == 0
        assert b["holistika_share_amount"] == 80_000.0
        assert b["collaborator_share_amount"] == 0.0
        # Solo (no overlay sibling row) → anchor is 100/0 not 85/15.
        assert b["anchor_holistika_pct"] == 100
        assert b["anchor_collaborator_pct"] == 0
        assert b["split_matches_anchor"] is True


# ===========================================================================
# TRUE-MARGIN cost-line collection (founder hours / direct passthroughs /
# vendor billed services)
# ===========================================================================

class TestTrueMarginCostCollection:
    def test_founder_hours_and_rate_produce_cost_line(
        self, csc_mod, tmp_path, monkeypatch
    ):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-FOUNDER-COST",
            revenue=50_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=40.0,
            founder_rate=250.0,
            direct_costs=[],
            currency="EUR",
            share_pattern_override="consulting_direct",
        )
        # 40 * 250 = 10,000 founder cost
        assert s["total_costs"] == 10_000.0
        assert s["benefits"] == 40_000.0
        founder_lines = [
            cl for cl in s["cost_lines"] if cl["kind"] == "founder_billed_time"
        ]
        assert len(founder_lines) == 1
        assert founder_lines[0]["amount"] == 10_000.0
        assert founder_lines[0]["hours"] == 40.0
        assert founder_lines[0]["rate"] == 250.0

    def test_multiple_direct_costs_aggregate(self, csc_mod, tmp_path, monkeypatch):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-DIRECT-COSTS",
            revenue=100_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[1_500.0, 2_500.0, 6_000.0],
            currency="EUR",
            share_pattern_override="consulting_direct",
        )
        assert s["total_costs"] == 10_000.0
        assert s["benefits"] == 90_000.0
        direct_lines = [
            cl for cl in s["cost_lines"] if cl["kind"] == "direct_pass_through"
        ]
        assert len(direct_lines) == 3
        assert sum(cl["amount"] for cl in direct_lines) == 10_000.0

    def test_zero_or_negative_direct_costs_dropped(
        self, csc_mod, tmp_path, monkeypatch
    ):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-ZERO-DIRECT",
            revenue=100_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[0.0, -100.0, 5_000.0],
            currency="EUR",
            share_pattern_override="consulting_direct",
        )
        direct_lines = [
            cl for cl in s["cost_lines"] if cl["kind"] == "direct_pass_through"
        ]
        assert len(direct_lines) == 1
        assert direct_lines[0]["amount"] == 5_000.0

    def test_vendor_billed_services_aggregated_from_csv(
        self, csc_mod, tmp_path, monkeypatch
    ):
        from akos.hlk_collaborator_share import (
            HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
        )

        # Build vendor-billed rows aligned with the SSOT 12-column header
        # (vendor_billing_id / engagement_id / holistika_service_class /
        # bill_mode / billed_hours / billed_rate / billed_amount_computed /
        # justification_clause_id / bill_mode_decision_id / status /
        # last_review_at / notes).
        def _vendor_row(
            engagement_id: str,
            service_class: str,
            bill_mode: str,
            billed_hours: float,
            billed_rate: float,
        ) -> str:
            cells = {fn: "" for fn in HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES}
            cells["vendor_billing_id"] = f"vbil-{service_class}-{engagement_id}"
            cells["engagement_id"] = engagement_id
            cells["holistika_service_class"] = service_class
            cells["bill_mode"] = bill_mode
            cells["billed_hours"] = str(billed_hours)
            cells["billed_rate"] = str(billed_rate)
            cells["billed_amount_computed"] = str(billed_hours * billed_rate)
            cells["status"] = "active"
            cells["last_review_at"] = "2026-01-01"
            cells["notes"] = "pytest fixture"
            return (
                ",".join(cells[fn] for fn in HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES)
                + "\n"
            )

        vendor_rows = [
            _vendor_row("ENG-VENDOR-BILLED", "tooling_provisioning", "billed", 10.0, 100.0),
            _vendor_row("ENG-VENDOR-BILLED", "methodology_design", "in_kind", 20.0, 250.0),
            _vendor_row("ENG-OTHER-ENGAGEMENT", "tooling_provisioning", "billed", 99.0, 999.0),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(
            tmp_path, share_rows=[], vendor_rows=vendor_rows
        )
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-VENDOR-BILLED",
            revenue=50_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
            share_pattern_override="consulting_direct",
        )
        vendor_lines = [
            cl for cl in s["cost_lines"] if cl["kind"] == "vendor_billed_service"
        ]
        # Only the billed row for THIS engagement should count.
        assert len(vendor_lines) == 1
        assert vendor_lines[0]["amount"] == 1_000.0  # 10 * 100
        assert s["total_costs"] == 1_000.0
        assert s["benefits"] == 49_000.0


# ===========================================================================
# Overlay engagement (2-row CSV fixture; consulting_direct + bd_commission_overlay)
# ===========================================================================

class TestOverlayEngagement:
    """Aïsha-on-SUEZ shape (D-IH-86-EG): two SHARE_REGISTRY rows for one
    engagement_id — Holistika consulting_direct base (85%) + collaborator
    bd_commission_overlay sibling (15%). Across-rows must sum to 100.
    """

    def _seed_overlay_fixture(self, tmp_path: Path) -> tuple[Path, Path]:
        eng_id = "ENG-OVERLAY-2026"
        rows = [
            # Base row: consulting_direct, Holistika 85%
            _build_share_registry_row(
                share_id="csh-base-001",
                engagement_id=eng_id,
                share_pattern="consulting_direct",
                share_overlay="",
                holistika_pct=85,
                collaborator_pct=0,
                collaborator_id="POI-HOL-FOUNDER",
            ),
            # Overlay row: consulting_direct + bd_commission_overlay, 0/15
            _build_share_registry_row(
                share_id="csh-overlay-001",
                engagement_id=eng_id,
                share_pattern="consulting_direct",
                share_overlay="bd_commission_overlay",
                holistika_pct=0,
                collaborator_pct=15,
                collaborator_id="POI-AISHA-2026",
                methodology_readiness="methodology_naive",
            ),
        ]
        return _seed_csv_fixture(tmp_path, share_rows=rows)

    def test_overlay_engagement_emits_two_breakdowns(
        self, csc_mod, tmp_path, monkeypatch
    ):
        share_csv, vendor_csv = self._seed_overlay_fixture(tmp_path)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-OVERLAY-2026",
            revenue=38_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[8_000.0],
            currency="EUR",
            share_pattern_override=None,  # CSV rows take precedence
        )
        assert s["benefits"] == 30_000.0
        assert len(s["per_row_breakdowns"]) == 2

    def test_overlay_engagement_per_row_split_arithmetic(
        self, csc_mod, tmp_path, monkeypatch
    ):
        share_csv, vendor_csv = self._seed_overlay_fixture(tmp_path)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-OVERLAY-2026",
            revenue=38_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[8_000.0],
            currency="EUR",
        )
        # benefits = 30k
        # Base row 85/0 -> H=25,500 / C=0
        # Overlay row 0/15 -> H=0 / C=4,500
        # Across-rows TOTAL pct = 85+0+0+15 = 100; sums_to_100 True.
        per_row = s["per_row_breakdowns"]
        base = next(b for b in per_row if b["share_overlay"] == "")
        overlay = next(b for b in per_row if b["share_overlay"] == "bd_commission_overlay")

        assert base["holistika_share_amount"] == 25_500.0
        assert base["collaborator_share_amount"] == 0.0
        assert overlay["holistika_share_amount"] == 0.0
        assert overlay["collaborator_share_amount"] == 4_500.0

        # CS-03 across-rows aggregate.
        assert s["across_rows_total_holistika_pct"] == 85
        assert s["across_rows_total_collaborator_pct"] == 15
        assert s["across_rows_split_sums_to_100"] is True
        assert s["across_rows_holistika_amount"] == 25_500.0
        assert s["across_rows_collaborator_amount"] == 4_500.0

    def test_overlay_engagement_uses_with_overlay_anchor_for_base(
        self, csc_mod, tmp_path, monkeypatch
    ):
        """Per ``_default_anchor_for_row``: when an overlay sibling row
        exists on a consulting_direct engagement, the base row anchor
        becomes 85/15 (WITH-OVERLAY) rather than 100/0 (SOLO). The base
        row's 85/0 split should therefore reflect the 85 anchor and a
        collaborator deviation of 0 vs anchor 15 (still a deviation, but
        rendered against the correct anchor)."""
        share_csv, vendor_csv = self._seed_overlay_fixture(tmp_path)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-OVERLAY-2026",
            revenue=38_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[8_000.0],
            currency="EUR",
        )
        per_row = s["per_row_breakdowns"]
        base = next(b for b in per_row if b["share_overlay"] == "")
        # WITH-OVERLAY anchor = (85, 15)
        assert base["anchor_holistika_pct"] == 85
        assert base["anchor_collaborator_pct"] == 15

    def test_drift_engagement_flags_cs03_violation(
        self, csc_mod, tmp_path, monkeypatch
    ):
        """A 2-row engagement that does NOT sum to 100 must surface
        CS-03 advisory + ``across_rows_split_sums_to_100`` False."""
        eng_id = "ENG-DRIFT-2026"
        rows = [
            _build_share_registry_row(
                share_id="csh-drift-base",
                engagement_id=eng_id,
                share_pattern="consulting_direct",
                holistika_pct=80,  # should be 85 with overlay
                collaborator_pct=0,
                collaborator_id="POI-HOL-FOUNDER",
            ),
            _build_share_registry_row(
                share_id="csh-drift-ovl",
                engagement_id=eng_id,
                share_pattern="consulting_direct",
                share_overlay="bd_commission_overlay",
                holistika_pct=0,
                collaborator_pct=15,
                collaborator_id="POI-AISHA-2026",
                methodology_readiness="methodology_naive",
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id=eng_id,
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        assert s["across_rows_split_sums_to_100"] is False
        assert s["across_rows_total_holistika_pct"] == 80
        assert s["across_rows_total_collaborator_pct"] == 15
        cs03_notes = [
            n for n in s["advisory_notes"] if "CS-03" in n and "95" in n
        ]
        assert cs03_notes, (
            f"expected CS-03 across-rows-sum advisory; got "
            f"{s['advisory_notes']}"
        )


# ===========================================================================
# Advisory note generation — the four advisory classes
# ===========================================================================

class TestAdvisoryNoteGeneration:
    def test_default_anchor_mismatch_without_override_flags_cs04(
        self, csc_mod, tmp_path, monkeypatch
    ):
        rows = [
            _build_share_registry_row(
                share_id="csh-anchor-drift",
                engagement_id="ENG-ANCHOR-DRIFT",
                share_pattern="deep_partner_65_35",
                holistika_pct=70,  # deviates from 65/35 anchor
                collaborator_pct=30,
                override_id="",  # no override -> CS-04 WARN
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-ANCHOR-DRIFT",
            revenue=100_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        b = s["per_row_breakdowns"][0]
        assert b["split_matches_anchor"] is False
        notes = b["advisory_notes"]
        assert any("CS-04" in n for n in notes), (
            f"expected CS-04 advisory note for unratified anchor deviation; "
            f"got {notes}"
        )

    def test_default_anchor_mismatch_with_override_named(
        self, csc_mod, tmp_path, monkeypatch
    ):
        rows = [
            _build_share_registry_row(
                share_id="csh-anchor-ratified",
                engagement_id="ENG-ANCHOR-RATIFIED",
                share_pattern="deep_partner_65_35",
                holistika_pct=70,
                collaborator_pct=30,
                override_id="D-IH-86-TEST-OVERRIDE",
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-ANCHOR-RATIFIED",
            revenue=100_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        b = s["per_row_breakdowns"][0]
        notes = b["advisory_notes"]
        assert any("D-IH-86-TEST-OVERRIDE" in n for n in notes), (
            f"expected operator-ratified deviation advisory naming the "
            f"override ID; got {notes}"
        )
        # When the deviation is ratified the note should NOT scream CS-04
        # WARN — it should name the override instead.
        assert not any("CS-04 WARN" in n for n in notes), notes

    def test_methodology_pattern_incoherence_flags_cs09(
        self, csc_mod, tmp_path, monkeypatch
    ):
        """methodology_naive does NOT permit deep_partner_65_35 per the
        permissibility matrix (CS-09 FAIL)."""
        rows = [
            _build_share_registry_row(
                share_id="csh-methodology-incoh",
                engagement_id="ENG-METHOD-INCOH",
                share_pattern="deep_partner_65_35",
                methodology_readiness="methodology_naive",
                holistika_pct=65,
                collaborator_pct=35,
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-METHOD-INCOH",
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        notes = s["per_row_breakdowns"][0]["advisory_notes"]
        assert any(
            "methodology_readiness" in n and "deep_partner_65_35" in n
            and "CS-09" in n
            for n in notes
        ), f"expected methodology-pattern incoherence advisory; got {notes}"

    def test_unknown_methodology_value_flags_cs08(
        self, csc_mod, tmp_path, monkeypatch
    ):
        rows = [
            _build_share_registry_row(
                share_id="csh-methodology-unknown",
                engagement_id="ENG-METHOD-UNKNOWN",
                share_pattern="consulting_direct",
                methodology_readiness="methodology_definitely_not_a_real_value",
                holistika_pct=100,
                collaborator_pct=0,
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-METHOD-UNKNOWN",
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        notes = s["per_row_breakdowns"][0]["advisory_notes"]
        assert any("CS-08" in n for n in notes), (
            f"expected CS-08 unknown-methodology advisory; got {notes}"
        )

    def test_overlay_base_pairing_violation_flags_cs09(
        self, csc_mod, tmp_path, monkeypatch
    ):
        """bd_commission_overlay is NOT permitted on
        joint_venture_aventure per VALID_OVERLAY_BASE_PAIRINGS."""
        rows = [
            _build_share_registry_row(
                share_id="csh-bad-pairing",
                engagement_id="ENG-BAD-PAIRING",
                share_pattern="joint_venture_aventure",
                share_overlay="bd_commission_overlay",
                holistika_pct=50,
                collaborator_pct=50,
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-BAD-PAIRING",
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        notes = s["per_row_breakdowns"][0]["advisory_notes"]
        assert any(
            "share_overlay" in n
            and "joint_venture_aventure" in n
            and "CS-09" in n
            for n in notes
        ), f"expected overlay-base pairing CS-09 advisory; got {notes}"

    def test_parallel_invoice_stream_indicator_emits_reconciliation_note(
        self, csc_mod, tmp_path, monkeypatch
    ):
        rows = [
            _build_share_registry_row(
                share_id="csh-parallel",
                engagement_id="ENG-PARALLEL-INVOICE",
                share_pattern="deep_partner_65_35",
                parallel_invoice="true",
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-PARALLEL-INVOICE",
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        b = s["per_row_breakdowns"][0]
        assert b["parallel_invoice_stream_indicator"] is True
        notes = b["advisory_notes"]
        assert any(
            "parallel_invoice_stream_indicator" in n and "D-IH-86-EK" in n
            for n in notes
        ), f"expected parallel-invoice reconciliation advisory; got {notes}"


# ===========================================================================
# What-if path edge cases
# ===========================================================================

class TestWhatIfPath:
    def test_csv_rows_take_precedence_over_cli_override(
        self, csc_mod, tmp_path, monkeypatch
    ):
        """When a SHARE_REGISTRY row exists for the engagement, the CLI
        --share-pattern override must be IGNORED in favour of the CSV
        row (the CSV is SSOT for live engagements)."""
        rows = [
            _build_share_registry_row(
                share_id="csh-precedence",
                engagement_id="ENG-PRECEDENCE",
                share_pattern="bd_intro_only",
                holistika_pct=85,
                collaborator_pct=15,
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-PRECEDENCE",
            revenue=100_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[20_000.0],
            currency="EUR",
            share_pattern_override="consulting_direct",  # should be ignored
        )
        b = s["per_row_breakdowns"][0]
        assert b["share_pattern"] == "bd_intro_only"
        assert b["holistika_share_pct"] == 85
        assert s["primary_row_share_pattern"] == "bd_intro_only"

    def test_whatif_advisory_note_flags_synthesized_row(
        self, csc_mod, tmp_path, monkeypatch
    ):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-WHATIF",
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
            share_pattern_override="deep_partner_65_35",
        )
        assert s["share_row_present"] is False
        notes = s["per_row_breakdowns"][0]["advisory_notes"]
        assert any("what-if" in n.lower() for n in notes), (
            f"expected what-if synthesised-row advisory; got {notes}"
        )

    def test_no_csv_rows_no_override_yields_zero_breakdowns(
        self, csc_mod, tmp_path, monkeypatch
    ):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-EMPTY",
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
            share_pattern_override=None,
        )
        # Benefits still compute (cost = 0 -> benefits = revenue)
        assert s["benefits"] == 10_000.0
        assert s["per_row_breakdowns"] == []
        assert s["across_rows_total_holistika_pct"] == 0
        assert s["across_rows_total_collaborator_pct"] == 0
        # An engagement w/ 0 rows is degenerate but the sum check is
        # advisory; CS-03 only fires for an existing-but-broken split.
        assert s["across_rows_split_sums_to_100"] is False


# ===========================================================================
# Markdown render shape (operator-readable §3-mechanical-evidence output)
# ===========================================================================

class TestMarkdownRender:
    def test_render_includes_true_margin_header_table(
        self, csc_mod, tmp_path, monkeypatch
    ):
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=[])
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-MD-RENDER",
            revenue=100_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[20_000.0],
            currency="EUR",
            share_pattern_override="deep_partner_65_35",
        )
        md = csc_mod.render_settlement_markdown(s)
        assert "# Collaborator Share Settlement" in md
        assert "ENG-MD-RENDER" in md
        assert "TRUE-MARGIN" in md
        assert "Revenue" in md
        assert "100000.00 EUR" in md
        assert "Benefits (= revenue - costs)" in md
        assert "80000.00 EUR" in md

    def test_render_includes_per_row_split_table(
        self, csc_mod, tmp_path, monkeypatch
    ):
        rows = [
            _build_share_registry_row(
                share_id="csh-md-1",
                engagement_id="ENG-MD-ROWS",
                share_pattern="deep_partner_65_35",
                holistika_pct=65,
                collaborator_pct=35,
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-MD-ROWS",
            revenue=100_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[20_000.0],
            currency="EUR",
        )
        md = csc_mod.render_settlement_markdown(s)
        assert "Per-row split application on benefits" in md
        assert "csh-md-1" in md
        assert "deep_partner_65_35" in md
        assert "CS-03 invariant holds" in md

    def test_render_flags_cs03_failure_when_split_does_not_sum(
        self, csc_mod, tmp_path, monkeypatch
    ):
        rows = [
            _build_share_registry_row(
                share_id="csh-md-bad-1",
                engagement_id="ENG-MD-BAD",
                share_pattern="deep_partner_65_35",
                holistika_pct=60,
                collaborator_pct=30,
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-MD-BAD",
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        md = csc_mod.render_settlement_markdown(s)
        assert s["across_rows_split_sums_to_100"] is False
        assert "WARNING" in md
        assert "CS-03 FAIL" in md

    def test_render_collates_per_row_advisory_notes(
        self, csc_mod, tmp_path, monkeypatch
    ):
        rows = [
            _build_share_registry_row(
                share_id="csh-md-advisory",
                engagement_id="ENG-MD-ADVISORY",
                share_pattern="deep_partner_65_35",
                methodology_readiness="methodology_naive",  # CS-09 trigger
                holistika_pct=65,
                collaborator_pct=35,
            ),
        ]
        share_csv, vendor_csv = _seed_csv_fixture(tmp_path, share_rows=rows)
        _point_runbook_at_fixture(monkeypatch, csc_mod, share_csv, vendor_csv)

        s = csc_mod.calculate_settlement(
            engagement_id="ENG-MD-ADVISORY",
            revenue=10_000.0,
            collaborator_id=None,
            collaborator_hours=None,
            founder_hours=None,
            founder_rate=None,
            direct_costs=[],
            currency="EUR",
        )
        md = csc_mod.render_settlement_markdown(s)
        assert "Advisory notes" in md
        assert "row `csh-md-advisory`" in md
        assert "methodology_readiness" in md


# ===========================================================================
# CLI end-to-end smoke (subprocess; exercises argparse + json + markdown)
# ===========================================================================

class TestCLIEndToEnd:
    def test_default_mode_prints_markdown_for_unknown_engagement(self):
        """Engagement w/ no SHARE_REGISTRY row falls back to what-if (when
        --share-pattern supplied) and prints the markdown table to stdout."""
        result = _run_runbook(
            "--engagement-id", "ENG-CLI-UNKNOWN-2026",
            "--revenue", "100000",
            "--share-pattern", "deep_partner_65_35",
        )
        assert result.returncode == 0, (
            f"runbook failed (exit {result.returncode})\nstderr: {result.stderr}"
        )
        assert "Collaborator Share Settlement" in result.stdout
        assert "ENG-CLI-UNKNOWN-2026" in result.stdout
        assert "TRUE-MARGIN" in result.stdout

    def test_emit_report_writes_to_tmp_path(self, tmp_path):
        report = tmp_path / "settlement.md"
        result = _run_runbook(
            "--engagement-id", "ENG-CLI-REPORT-2026",
            "--revenue", "50000",
            "--share-pattern", "consulting_direct",
            "--emit-report",
            "--report-path", str(report),
        )
        assert result.returncode == 0, (
            f"--emit-report failed (exit {result.returncode})\nstderr: {result.stderr}"
        )
        assert report.is_file(), f"expected report at {report}"
        body = report.read_text(encoding="utf-8")
        assert "ENG-CLI-REPORT-2026" in body
        assert "consulting_direct" in body

    def test_emit_json_for_consulting_direct_solo(self):
        result = _run_runbook(
            "--engagement-id", "ENG-CLI-JSON-CD",
            "--revenue", "40000",
            "--share-pattern", "consulting_direct",
            "--emit-json",
        )
        assert result.returncode == 0
        payload = json.loads(result.stdout)
        assert payload["primary_row_share_pattern"] == "consulting_direct"
        assert payload["benefits"] == 40_000.0  # no costs supplied
        assert len(payload["per_row_breakdowns"]) == 1
        b = payload["per_row_breakdowns"][0]
        assert b["holistika_share_pct"] == 100
        assert b["collaborator_share_pct"] == 0
        assert b["holistika_share_amount"] == 40_000.0
        assert b["collaborator_share_amount"] == 0.0
