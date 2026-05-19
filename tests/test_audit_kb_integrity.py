"""Tests for akos/hlk_kb_integrity.py + scripts/audit_kb_integrity.py per I81 P1."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from akos.hlk_kb_integrity import (
    ITEM_ID_RE,
    KbIntegrityAuditSummary,
    KbIntegrityMatrixRow,
    PROCESS_LIST_REL,
    repo_root,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "audit_kb_integrity.py"


def _load_script_module():
    spec = importlib.util.spec_from_file_location("audit_kb_integrity", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("audit_kb_integrity", module)
    spec.loader.exec_module(module)
    return module


# -----------------------------------------------------------------------------
# Pydantic chassis tests (akos/hlk_kb_integrity.py)
# -----------------------------------------------------------------------------


@pytest.mark.hlk
class TestKbIntegrityMatrixRow:
    def _valid_kwargs(self) -> dict:
        return {
            "item_id": "tbi_mkt_prc_brand_canon_mtnce_001",
            "area": "MKT",
            "role_owner": "Brand & Narrative Manager",
            "item_granularity": "process",
            "item_name": "Brand canon maintenance",
            "knowledge_pairing_status": "matched",
            "paired_sop_status": "matched",
            "mirror_coverage_status": "covered_by_emit",
            "audience_tags_status": "matched",
            "cadence_status": "declared",
            "verdict": "pass",
            "gap_summary": "",
        }

    def test_minimal_pass_row_validates(self):
        row = KbIntegrityMatrixRow(**self._valid_kwargs())
        assert row.verdict == "pass"

    def test_invalid_granularity_rejected(self):
        kw = self._valid_kwargs()
        kw["item_granularity"] = "project"
        with pytest.raises(ValidationError):
            KbIntegrityMatrixRow(**kw)

    def test_unknown_kp_status_rejected(self):
        kw = self._valid_kwargs()
        kw["knowledge_pairing_status"] = "partial"
        with pytest.raises(ValidationError):
            KbIntegrityMatrixRow(**kw)

    def test_unknown_verdict_rejected(self):
        kw = self._valid_kwargs()
        kw["verdict"] = "skip"
        with pytest.raises(ValidationError):
            KbIntegrityMatrixRow(**kw)

    def test_extra_field_rejected(self):
        kw = self._valid_kwargs()
        kw["surprise"] = "boom"
        with pytest.raises(ValidationError):
            KbIntegrityMatrixRow(**kw)

    def test_row_is_frozen(self):
        row = KbIntegrityMatrixRow(**self._valid_kwargs())
        with pytest.raises(ValidationError):
            row.verdict = "fail"  # type: ignore[misc]


@pytest.mark.hlk
class TestComputeVerdict:
    def test_all_good_returns_pass(self):
        v, gap = KbIntegrityMatrixRow.compute_verdict(
            "matched", "matched", "covered_by_emit", "matched", "declared"
        )
        assert v == "pass"
        assert gap == ""

    def test_mirror_skip_returns_fail(self):
        v, gap = KbIntegrityMatrixRow.compute_verdict(
            "matched", "matched", "mirror_skip", "matched", "declared"
        )
        assert v == "fail"
        assert "mirror_skip" in gap

    def test_one_missing_signal_returns_partial(self):
        v, gap = KbIntegrityMatrixRow.compute_verdict(
            "unmatched", "matched", "covered_by_emit", "matched", "declared"
        )
        assert v == "partial"
        assert gap == "knowledge_pairing"

    def test_multiple_missing_signals_collected(self):
        v, gap = KbIntegrityMatrixRow.compute_verdict(
            "unmatched", "unmatched", "covered_by_emit", "deferred", "undeclared"
        )
        assert v == "partial"
        # Order is fixed by compute_verdict implementation: KP, SOP, audience, cadence
        gap_list = gap.split(";")
        assert "knowledge_pairing" in gap_list
        assert "paired_sop" in gap_list
        assert "audience_tags_deferred" in gap_list
        assert "cadence_undeclared" in gap_list

    def test_p1_baseline_state_is_partial(self):
        # P1 baseline: KP unmatched / SOP unmatched / mirror covered / audience deferred / cadence undeclared
        v, gap = KbIntegrityMatrixRow.compute_verdict(
            "unmatched", "unmatched", "covered_by_emit", "deferred", "undeclared"
        )
        assert v == "partial"


@pytest.mark.hlk
class TestKbIntegrityAuditSummary:
    def _valid_kwargs(self) -> dict:
        return {
            "matrix_csv_path": "reports/i81/kb-integrity-matrix-2026-05-19.csv",
            "audit_date": "2026-05-19",
            "executable_row_count": 1000,
            "pass_count": 10,
            "partial_count": 980,
            "fail_count": 10,
            "pass_rate": 0.01,
            "meets_threshold": False,
            "knowledge_pairing_matched_count": 7,
            "paired_sop_matched_count": 50,
            "audience_tags_deferred_count": 1000,
            "cadence_undeclared_count": 970,
        }

    def test_minimal_validates(self):
        s = KbIntegrityAuditSummary(**self._valid_kwargs())
        assert s.pass_threshold == 0.95

    def test_negative_count_rejected(self):
        kw = self._valid_kwargs()
        kw["pass_count"] = -1
        with pytest.raises(ValidationError):
            KbIntegrityAuditSummary(**kw)

    def test_invalid_date_rejected(self):
        kw = self._valid_kwargs()
        kw["audit_date"] = "not-iso"
        with pytest.raises(ValidationError):
            KbIntegrityAuditSummary(**kw)

    def test_out_of_range_pass_rate_rejected(self):
        kw = self._valid_kwargs()
        kw["pass_rate"] = 1.5
        with pytest.raises(ValidationError):
            KbIntegrityAuditSummary(**kw)

    def test_extra_field_rejected(self):
        kw = self._valid_kwargs()
        kw["surprise"] = True
        with pytest.raises(ValidationError):
            KbIntegrityAuditSummary(**kw)


@pytest.mark.hlk
class TestItemIdRegex:
    def test_valid_item_id_matches(self):
        for iid in (
            "tbi_mkt_prc_brand_canon_mtnce_001",
            "hol_ops_dtp_72",
            "env_tech_dtp_external_render_gate_promotion_001",
        ):
            assert ITEM_ID_RE.match(iid), iid

    def test_valid_sop_prefixed_item_id_matches(self):
        # Legacy SOP-prefixed rows exist in the real corpus and are legitimate.
        for iid in ("SOP-META_PROCESS_MGMT_001", "SOP-EXTERNAL_REPO_BLESSING_001"):
            assert ITEM_ID_RE.match(iid), iid

    def test_invalid_item_id_rejected(self):
        for iid in ("1_starts_with_digit", "has spaces", "", "_starts_underscore"):
            assert not ITEM_ID_RE.match(iid), iid


# -----------------------------------------------------------------------------
# Script-level tests (scripts/audit_kb_integrity.py)
# -----------------------------------------------------------------------------


@pytest.mark.hlk
class TestAuditScriptHelpers:
    def test_build_matrix_rows_filters_to_executable(self):
        script = _load_script_module()
        pl_rows = [
            {
                "item_id": "iid_task_a",
                "item_granularity": "task",
                "area": "MKT",
                "role_owner": "Brand Manager",
                "item_name": "Task A",
                "cadence_type": "on_demand",
            },
            {
                "item_id": "iid_process_b",
                "item_granularity": "process",
                "area": "Tech",
                "role_owner": "System Owner",
                "item_name": "Process B",
                "cadence_type": "",
            },
            {
                "item_id": "iid_project_c",
                "item_granularity": "project",
                "area": "Ops",
                "role_owner": "PMO",
                "item_name": "Project C",
                "cadence_type": "",
            },
            {
                "item_id": "iid_workstream_d",
                "item_granularity": "workstream",
                "area": "Ops",
                "role_owner": "PMO",
                "item_name": "Workstream D",
                "cadence_type": "",
            },
        ]
        rows = script.build_matrix_rows(pl_rows, pairing_matched={"iid_task_a"}, sop_matched=set())
        assert len(rows) == 2  # only task + process kept
        ids = {r.item_id for r in rows}
        assert ids == {"iid_task_a", "iid_process_b"}
        task_row = next(r for r in rows if r.item_id == "iid_task_a")
        assert task_row.knowledge_pairing_status == "matched"
        assert task_row.cadence_status == "declared"
        proc_row = next(r for r in rows if r.item_id == "iid_process_b")
        assert proc_row.knowledge_pairing_status == "unmatched"
        assert proc_row.cadence_status == "undeclared"

    def test_build_matrix_rows_skips_invalid_item_ids(self):
        script = _load_script_module()
        pl_rows = [
            {
                "item_id": "1bad_starts_with_digit",
                "item_granularity": "task",
                "area": "MKT",
                "role_owner": "x",
                "item_name": "y",
                "cadence_type": "",
            },
            {
                "item_id": "has spaces in id",
                "item_granularity": "task",
                "area": "MKT",
                "role_owner": "x",
                "item_name": "y",
                "cadence_type": "",
            },
            {
                "item_id": "",
                "item_granularity": "task",
                "area": "MKT",
                "role_owner": "x",
                "item_name": "y",
                "cadence_type": "",
            },
        ]
        rows = script.build_matrix_rows(pl_rows, pairing_matched=set(), sop_matched=set())
        assert rows == []

    def test_resolve_item_ids_in_pairing_rows_substring_scan(self):
        script = _load_script_module()
        kp_rows = [
            {
                "pairing_id": "pair_alpha_001",
                "parent_doc_path": "docs/HOLISTIKA_ALPHA.md",
                "companion_doc_paths": "docs/HOLISTIKA_ALPHA.addendum.md",
            },
            {
                "pairing_id": "pair_beta_001",
                "parent_doc_path": "docs/another_item_beta.md",
                "companion_doc_paths": "",
            },
        ]
        # 'alpha' appears in pairing_id + parent_doc_path; 'beta' appears in parent_doc_path
        matched = script._resolve_item_ids_in_pairing_rows(
            kp_rows, {"alpha", "beta", "gamma"}
        )
        assert matched == {"alpha", "beta"}

    def test_build_summary_aggregates_correctly(self):
        script = _load_script_module()
        rows = [
            KbIntegrityMatrixRow(
                item_id="a", area="MKT", role_owner="x", item_granularity="task",
                item_name="A",
                knowledge_pairing_status="matched",
                paired_sop_status="matched",
                mirror_coverage_status="covered_by_emit",
                audience_tags_status="matched",
                cadence_status="declared",
                verdict="pass",
                gap_summary="",
            ),
            KbIntegrityMatrixRow(
                item_id="b", area="Tech", role_owner="y", item_granularity="process",
                item_name="B",
                knowledge_pairing_status="unmatched",
                paired_sop_status="unmatched",
                mirror_coverage_status="covered_by_emit",
                audience_tags_status="deferred",
                cadence_status="undeclared",
                verdict="partial",
                gap_summary="knowledge_pairing;paired_sop;audience_tags_deferred;cadence_undeclared",
            ),
            KbIntegrityMatrixRow(
                item_id="c", area="Ops", role_owner="z", item_granularity="task",
                item_name="C",
                knowledge_pairing_status="matched",
                paired_sop_status="matched",
                mirror_coverage_status="mirror_skip",
                audience_tags_status="matched",
                cadence_status="declared",
                verdict="fail",
                gap_summary="mirror_skip (intentional or sync-flow gap)",
            ),
        ]
        summary = script.build_summary(rows, "matrix.csv", "2026-05-19")
        assert summary.executable_row_count == 3
        assert summary.pass_count == 1
        assert summary.partial_count == 1
        assert summary.fail_count == 1
        assert abs(summary.pass_rate - 1 / 3) < 1e-9
        assert summary.meets_threshold is False
        assert summary.knowledge_pairing_matched_count == 2
        assert summary.paired_sop_matched_count == 2
        assert summary.audience_tags_deferred_count == 1
        assert summary.cadence_undeclared_count == 1
        # Top gap signals should include the partial row's gaps
        assert any("knowledge_pairing" in g for g in summary.top_gap_signals)

    def test_write_matrix_csv_round_trip(self, tmp_path):
        script = _load_script_module()
        rows = [
            KbIntegrityMatrixRow(
                item_id="a", area="MKT", role_owner="x", item_granularity="task",
                item_name="A",
                knowledge_pairing_status="matched",
                paired_sop_status="matched",
                mirror_coverage_status="covered_by_emit",
                audience_tags_status="matched",
                cadence_status="declared",
                verdict="pass",
                gap_summary="",
            ),
        ]
        out = tmp_path / "subdir" / "matrix.csv"
        script.write_matrix_csv(rows, out)
        assert out.is_file()
        with out.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            read_rows = list(reader)
        assert len(read_rows) == 1
        assert read_rows[0]["item_id"] == "a"
        assert read_rows[0]["verdict"] == "pass"


@pytest.mark.hlk
class TestSmokeAgainstRealProcessList:
    def test_real_process_list_loads_with_executable_rows(self):
        """Smoke test: real process_list.csv loads + has ≥ 100 executable rows."""
        script = _load_script_module()
        pl_path = repo_root() / PROCESS_LIST_REL
        if not pl_path.is_file():
            pytest.skip(f"process_list.csv not present at {pl_path}")
        pl_rows = script._load_process_list(pl_path)
        executable = [
            r for r in pl_rows if r.get("item_granularity", "").strip() in ("task", "process")
        ]
        assert len(executable) >= 100  # repo had 1085 at I81 P1 mint

    def test_real_audit_emits_artifacts(self, tmp_path):
        """Smoke test: full audit run against real CSVs writes both artifacts."""
        script = _load_script_module()
        pl_path = repo_root() / PROCESS_LIST_REL
        if not pl_path.is_file():
            pytest.skip("Real process_list.csv missing; skipping smoke.")
        # Use the script's main() with --out-dir override
        argv = ["audit_kb_integrity.py", "--out-dir", str(tmp_path), "--date", "2026-05-19"]
        saved = sys.argv
        sys.argv = argv
        try:
            rc = script.main()
        finally:
            sys.argv = saved
        assert rc == 0
        matrix = tmp_path / "kb-integrity-matrix-2026-05-19.csv"
        narrative = tmp_path / "kb-integrity-audit-2026-05-19.md"
        assert matrix.is_file()
        assert narrative.is_file()
        # Matrix should have header + ≥ 100 data rows
        with matrix.open(encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            data_rows = list(reader)
        assert len(data_rows) >= 101  # 1 header + ≥ 100 data
        # Narrative should mention the I81 P1 frontmatter + key signals
        narrative_text = narrative.read_text(encoding="utf-8")
        assert "INIT-OPENCLAW_AKOS-81" in narrative_text
        assert "kb_integrity_audit" in narrative_text
        assert "D-IH-81-F" in narrative_text
