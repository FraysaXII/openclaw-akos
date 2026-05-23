"""I71 P4 — Tests for scripts/validate_review_stamps.py (Strand C2 review-stamp validator).

Covers:

- ``TestValidStamps`` — rows with all 4 columns populated; days-since-review < threshold.
- ``TestStaleRows`` — stamp populated but older than threshold; 179/180/181-day edge cases.
- ``TestMissingStamps`` — stamp empty AND row authored > 30 days ago → info advisory.
- ``TestInvalidDecisionRef`` — decision_ref points to non-existent decision_id → error.
- ``TestEmptyStampTolerance`` — newly-extended rows (all 4 empty) emit only info, never error.
- ``TestThresholdEdgeCases`` — custom thresholds via --threshold-days; exit code semantics.
- ``TestColumnExtensionMigration`` — 4 mirrored CSVs carry the 4 review-stamp columns at the
  expected trailing position; akos.* SSOT tuples align.
- ``TestInboxSurfacing`` — dated inbox section is written + idempotent re-render.

All tests use ``unittest.mock.patch`` to redirect _REGISTRY paths to fixture CSVs in tmp_path,
so the canonical CSVs in the repo are never mutated by the test suite.

Per ``CONTRIBUTING.md`` Python Code Standards: type hints; pytest fixtures; no module-level
side effects.

Marker: ``@pytest.mark.brand`` (chassis-precedent marker; review-stamp validator is sibling
to the brand-voice validator family that defined the marker at I71 P1).
"""

from __future__ import annotations

import csv
import importlib
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import target module + its registry primitives. Re-import via importlib ensures
# fresh module state in case prior tests mutated patched attrs.
import scripts.validate_review_stamps as vrs  # noqa: E402


pytestmark = pytest.mark.brand


# ---------------------------------------------------------------------------
# Fixtures — minimal CSV writers + a registry-substitute fixture
# ---------------------------------------------------------------------------


def _write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: (r.get(k) or "") for k in header})


def _stamp_columns() -> list[str]:
    return list(vrs.REVIEW_STAMP_COLUMNS)


def _decision_register_header() -> list[str]:
    return ["decision_id", "title", "decided_at", "notes", *_stamp_columns()]


def _initiative_registry_header() -> list[str]:
    return ["initiative_id", "title", "inception_date", "notes", *_stamp_columns()]


def _ops_register_header() -> list[str]:
    return ["ops_action_id", "title", "opened_at", "notes", *_stamp_columns()]


def _process_list_header() -> list[str]:
    return ["item_id", "item_name", "notes", *_stamp_columns()]


@pytest.fixture
def fixture_registry(tmp_path: Path):
    """Build a substitute _REGISTRY pointing at empty fixture CSVs in tmp_path."""
    decisions_csv = tmp_path / "DECISION_REGISTER.csv"
    initiatives_csv = tmp_path / "INITIATIVE_REGISTRY.csv"
    ops_csv = tmp_path / "OPS_REGISTER.csv"
    process_csv = tmp_path / "process_list.csv"

    _write_csv(decisions_csv, _decision_register_header(), [])
    _write_csv(initiatives_csv, _initiative_registry_header(), [])
    _write_csv(ops_csv, _ops_register_header(), [])
    _write_csv(process_csv, _process_list_header(), [])

    registry = (
        vrs.CanonicalSpec(
            csv_path=process_csv,
            fieldnames=tuple(_process_list_header()),
            pk_column="item_id",
            authored_date_column=None,
            label="process_list",
        ),
        vrs.CanonicalSpec(
            csv_path=decisions_csv,
            fieldnames=tuple(_decision_register_header()),
            pk_column="decision_id",
            authored_date_column="decided_at",
            label="decision_register",
        ),
        vrs.CanonicalSpec(
            csv_path=initiatives_csv,
            fieldnames=tuple(_initiative_registry_header()),
            pk_column="initiative_id",
            authored_date_column="inception_date",
            label="initiative_registry",
        ),
        vrs.CanonicalSpec(
            csv_path=ops_csv,
            fieldnames=tuple(_ops_register_header()),
            pk_column="ops_action_id",
            authored_date_column="opened_at",
            label="ops_register",
        ),
    )

    return {
        "registry": registry,
        "decisions_csv": decisions_csv,
        "initiatives_csv": initiatives_csv,
        "ops_csv": ops_csv,
        "process_csv": process_csv,
        "tmp_path": tmp_path,
    }


def _patch_registry(fixture_registry, monkeypatch):
    """Apply patches so vrs._REGISTRY + DECISION_REGISTER_CSV resolve to fixture paths."""
    monkeypatch.setattr(vrs, "_REGISTRY", fixture_registry["registry"])
    monkeypatch.setattr(vrs, "DECISION_REGISTER_CSV", fixture_registry["decisions_csv"])


def _extract_json(captured: str) -> str:
    """Pluck the JSON line from captured stdout (validator may emit a WARN line first)."""
    for line in captured.strip().splitlines()[::-1]:
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            return line
    return captured


# ---------------------------------------------------------------------------
# TestValidStamps
# ---------------------------------------------------------------------------


class TestValidStamps:
    def test_fresh_stamp_emits_no_advisory(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        stamp = (today - timedelta(days=10)).isoformat()
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-IH-71-Q", "title": "fresh", "decided_at": "2026-05-13",
              "last_review_at": stamp, "last_review_by": "PMO", "last_review_decision_id": "D-IH-71-Q",
              "methodology_version_at_review": "v3.1"}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--json-log"]
        with patch.object(sys, "stdout") as _:
            ec = vrs.main(argv)
        assert ec == 0

    def test_decision_register_alone_resolves_self_ref(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-IH-71-A", "title": "x", "decided_at": "2026-05-01",
              "last_review_at": "2026-05-10", "last_review_by": "PMO",
              "last_review_decision_id": "D-IH-71-A", "methodology_version_at_review": "v3.1"}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        assert ec == 0

    def test_multiple_fresh_rows_no_advisory(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        stamp = (today - timedelta(days=5)).isoformat()
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [
                {"decision_id": "D-A", "decided_at": "2026-05-01", "last_review_at": stamp},
                {"decision_id": "D-B", "decided_at": "2026-05-01", "last_review_at": stamp},
            ],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        assert ec == 0

    def test_fresh_stamp_with_no_decision_ref_ok(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-X-01", "inception_date": "2026-05-01",
              "last_review_at": "2026-05-13", "last_review_by": "PMO",
              "last_review_decision_id": "", "methodology_version_at_review": "v3.1"}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        assert ec == 0


# ---------------------------------------------------------------------------
# TestStaleRows + TestThresholdEdgeCases
# ---------------------------------------------------------------------------


class TestStaleRows:
    def test_stale_row_warning_at_threshold_plus_one(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        stamp = (today - timedelta(days=181)).isoformat()
        _write_csv(
            fixture_registry["ops_csv"],
            _ops_register_header(),
            [{"ops_action_id": "OPS-99-1", "opened_at": "2025-01-01", "last_review_at": stamp}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        # Warning is non-blocking by default; exit 0 unless error.
        assert ec == 0

    def test_stale_row_at_threshold_minus_one_ok(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        stamp = (today - timedelta(days=179)).isoformat()
        _write_csv(
            fixture_registry["ops_csv"],
            _ops_register_header(),
            [{"ops_action_id": "OPS-99-2", "opened_at": "2025-01-01", "last_review_at": stamp}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--json-log"]
        ec = vrs.main(argv)
        assert ec == 0

    def test_stale_row_exact_threshold_ok(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        stamp = (today - timedelta(days=180)).isoformat()
        _write_csv(
            fixture_registry["ops_csv"],
            _ops_register_header(),
            [{"ops_action_id": "OPS-99-3", "opened_at": "2025-01-01", "last_review_at": stamp}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        # 180 == threshold; "> threshold" is the stale condition; 180-day-old row is NOT stale yet
        assert ec == 0

    def test_strict_mode_fails_on_warning(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        stamp = (today - timedelta(days=181)).isoformat()
        _write_csv(
            fixture_registry["ops_csv"],
            _ops_register_header(),
            [{"ops_action_id": "OPS-99-4", "opened_at": "2025-01-01", "last_review_at": stamp}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--strict"]
        ec = vrs.main(argv)
        assert ec == 1


class TestThresholdEdgeCases:
    def test_custom_threshold_90_days(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        stamp = (today - timedelta(days=91)).isoformat()
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-T1", "decided_at": "2025-01-01", "last_review_at": stamp}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--threshold-days", "90", "--strict"]
        ec = vrs.main(argv)
        assert ec == 1

    def test_custom_threshold_loose_no_advisory(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        stamp = (today - timedelta(days=200)).isoformat()
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-T2", "decided_at": "2025-01-01", "last_review_at": stamp}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--threshold-days", "365"]
        ec = vrs.main(argv)
        assert ec == 0


# ---------------------------------------------------------------------------
# TestMissingStamps
# ---------------------------------------------------------------------------


class TestMissingStamps:
    def test_old_row_with_empty_stamp_emits_info(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        old_authored = (today - timedelta(days=60)).isoformat()
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-A", "decided_at": today.isoformat(), "last_review_at": today.isoformat()}],
        )
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-M-01", "inception_date": old_authored}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--json-log"]
        import io
        buf = io.StringIO()
        with patch.object(sys, "stdout", buf):
            ec = vrs.main(argv)
        assert ec == 0
        payload = json.loads(_extract_json(buf.getvalue()))
        rule_set = {a["rule"] for r in payload["reports"] for a in r["advisories"]}
        assert "missing-stamp" in rule_set

    def test_recent_row_with_empty_stamp_no_advisory(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        recent_authored = (today - timedelta(days=10)).isoformat()
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-A", "decided_at": today.isoformat(), "last_review_at": today.isoformat()}],
        )
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-M-02", "inception_date": recent_authored}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--json-log"]
        import io
        buf = io.StringIO()
        with patch.object(sys, "stdout", buf):
            ec = vrs.main(argv)
        assert ec == 0
        payload = json.loads(_extract_json(buf.getvalue()))
        rule_set = {(r["canonical"], a["rule"]) for r in payload["reports"] for a in r["advisories"]}
        assert ("initiative_registry", "missing-stamp") not in rule_set

    def test_process_list_row_always_flags_missing(self, fixture_registry, monkeypatch):
        """process_list rows have no authored-date proxy; missing-stamp fires unconditionally."""
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-A", "decided_at": today.isoformat(), "last_review_at": today.isoformat()}],
        )
        _write_csv(
            fixture_registry["process_csv"],
            _process_list_header(),
            [{"item_id": "hol_test_dtp_1", "item_name": "x"}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--json-log"]
        import io
        buf = io.StringIO()
        with patch.object(sys, "stdout", buf):
            ec = vrs.main(argv)
        assert ec == 0
        payload = json.loads(_extract_json(buf.getvalue()))
        process_report = next(r for r in payload["reports"] if r["canonical"] == "process_list")
        assert process_report["rows_missing_stamp"] == 1

    def test_strict_mode_fails_on_info(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        old = (today - timedelta(days=60)).isoformat()
        _write_csv(
            fixture_registry["ops_csv"],
            _ops_register_header(),
            [{"ops_action_id": "OPS-M-1", "opened_at": old}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--strict"]
        ec = vrs.main(argv)
        assert ec == 1


# ---------------------------------------------------------------------------
# TestInvalidDecisionRef
# ---------------------------------------------------------------------------


class TestInvalidDecisionRef:
    def test_invalid_decision_ref_emits_error_and_fails(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-IH-71-Q", "decided_at": "2026-05-14", "last_review_at": "2026-05-14"}],
        )
        _write_csv(
            fixture_registry["ops_csv"],
            _ops_register_header(),
            [{"ops_action_id": "OPS-X-1", "opened_at": "2026-05-01",
              "last_review_at": "2026-05-13",
              "last_review_decision_id": "D-IH-NOT-A-REAL-ID"}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        assert ec == 1  # error → exit 1 even without --strict

    def test_valid_decision_ref_no_advisory(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-IH-71-Q", "decided_at": "2026-05-14"}],
        )
        _write_csv(
            fixture_registry["ops_csv"],
            _ops_register_header(),
            [{"ops_action_id": "OPS-X-2", "opened_at": "2026-05-01",
              "last_review_at": "2026-05-13",
              "last_review_decision_id": "D-IH-71-Q"}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        assert ec == 0

    def test_empty_decision_ref_no_check(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-A", "decided_at": "2026-05-01"}],
        )
        _write_csv(
            fixture_registry["ops_csv"],
            _ops_register_header(),
            [{"ops_action_id": "OPS-X-3", "opened_at": "2026-05-01",
              "last_review_at": "2026-05-13", "last_review_decision_id": ""}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        assert ec == 0


# ---------------------------------------------------------------------------
# TestEmptyStampTolerance
# ---------------------------------------------------------------------------


class TestEmptyStampTolerance:
    def test_newly_extended_recent_row_no_advisory(self, fixture_registry, monkeypatch):
        """A row authored today with all 4 stamp columns empty is still within grace; no info."""
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-N-01", "inception_date": today.isoformat()}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox"]
        ec = vrs.main(argv)
        assert ec == 0

    def test_newly_extended_old_row_emits_only_info(self, fixture_registry, monkeypatch):
        """A row authored long ago with all 4 stamp columns empty emits info, never error."""
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        old = (today - timedelta(days=400)).isoformat()
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-A", "decided_at": today.isoformat(), "last_review_at": today.isoformat()}],
        )
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-N-02", "inception_date": old}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--json-log"]
        import io
        buf = io.StringIO()
        with patch.object(sys, "stdout", buf):
            ec = vrs.main(argv)
        assert ec == 0  # info-only is exit 0
        payload = json.loads(_extract_json(buf.getvalue()))
        severities = {a["severity"] for r in payload["reports"] for a in r["advisories"]}
        assert severities <= {"info"}  # no warning, no error

    def test_decision_register_old_row_with_empty_stamp_emits_info(self, fixture_registry, monkeypatch):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        old = (today - timedelta(days=200)).isoformat()
        _write_csv(
            fixture_registry["decisions_csv"],
            _decision_register_header(),
            [{"decision_id": "D-OLD-001", "decided_at": old}],
        )
        argv = ["--today", today.isoformat(), "--no-inbox", "--json-log"]
        import io
        buf = io.StringIO()
        with patch.object(sys, "stdout", buf):
            ec = vrs.main(argv)
        assert ec == 0
        payload = json.loads(_extract_json(buf.getvalue()))
        d_report = next(r for r in payload["reports"] if r["canonical"] == "decision_register")
        assert d_report["rows_missing_stamp"] == 1


# ---------------------------------------------------------------------------
# TestColumnExtensionMigration — verify the 4 real canonical CSVs carry the columns
# ---------------------------------------------------------------------------


class TestColumnExtensionMigration:
    def test_decision_register_carries_4_review_stamp_columns(self):
        from akos.hlk_decision_register_csv import DECISION_REGISTER_FIELDNAMES
        for col in vrs.REVIEW_STAMP_COLUMNS:
            assert col in DECISION_REGISTER_FIELDNAMES, f"DECISION_REGISTER_FIELDNAMES missing {col}"

    def test_initiative_registry_carries_4_review_stamp_columns(self):
        from akos.hlk_initiative_registry_csv import INITIATIVE_REGISTRY_FIELDNAMES
        for col in vrs.REVIEW_STAMP_COLUMNS:
            assert col in INITIATIVE_REGISTRY_FIELDNAMES, f"INITIATIVE_REGISTRY_FIELDNAMES missing {col}"

    def test_ops_register_carries_4_review_stamp_columns(self):
        from akos.hlk_ops_register_csv import OPS_REGISTER_FIELDNAMES
        for col in vrs.REVIEW_STAMP_COLUMNS:
            assert col in OPS_REGISTER_FIELDNAMES, f"OPS_REGISTER_FIELDNAMES missing {col}"

    def test_process_list_carries_4_review_stamp_columns(self):
        from akos.hlk_process_csv import PROCESS_LIST_FIELDNAMES
        for col in vrs.REVIEW_STAMP_COLUMNS:
            assert col in PROCESS_LIST_FIELDNAMES, f"PROCESS_LIST_FIELDNAMES missing {col}"

    def test_real_canonical_csvs_align_with_ssot_tuples(self):
        """Cross-link to validate_compliance_schema_drift.py logic; spot-check the 4 P4 CSVs."""
        canonicals_dir = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
        for filename, attr_name, module_name in (
            ("DECISION_REGISTER.csv", "DECISION_REGISTER_FIELDNAMES", "akos.hlk_decision_register_csv"),
            ("INITIATIVE_REGISTRY.csv", "INITIATIVE_REGISTRY_FIELDNAMES", "akos.hlk_initiative_registry_csv"),
            ("OPS_REGISTER.csv", "OPS_REGISTER_FIELDNAMES", "akos.hlk_ops_register_csv"),
            ("process_list.csv", "PROCESS_LIST_FIELDNAMES", "akos.hlk_process_csv"),
        ):
            csv_path = canonicals_dir / filename
            assert csv_path.exists(), f"{csv_path} missing"
            mod = importlib.import_module(module_name)
            tuple_attr = getattr(mod, attr_name)
            with csv_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                actual = next(reader)
            assert list(actual) == list(tuple_attr), f"{filename} header drift vs {attr_name}"


# ---------------------------------------------------------------------------
# TestInboxSurfacing
# ---------------------------------------------------------------------------


class TestInboxSurfacing:
    def test_inbox_writes_dated_section_with_markers(self, fixture_registry, monkeypatch, tmp_path):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-I-01", "inception_date": "2025-01-01"}],
        )
        inbox = tmp_path / "REVIEW_STAMP_INBOX.md"
        argv = ["--today", today.isoformat(), "--inbox-path", str(inbox)]
        ec = vrs.main(argv)
        assert ec == 0
        body = inbox.read_text(encoding="utf-8")
        assert "<!-- BEGIN REVIEW-STAMP-AUTO -->" in body
        assert "<!-- END REVIEW-STAMP-AUTO -->" in body
        assert "Last rendered: 2026-05-14 UTC" in body
        assert "missing-stamp" in body or "Missing review stamps" in body
        # Frontmatter present
        assert body.startswith("---\nlanguage: en")

    def test_inbox_idempotent_re_render_replaces_section(self, fixture_registry, monkeypatch, tmp_path):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-I-02", "inception_date": "2025-01-01"}],
        )
        inbox = tmp_path / "REVIEW_STAMP_INBOX.md"
        argv = ["--today", today.isoformat(), "--inbox-path", str(inbox)]
        vrs.main(argv)
        body_first = inbox.read_text(encoding="utf-8")
        # Re-run; output should be identical (no duplication of markers / sections)
        vrs.main(argv)
        body_second = inbox.read_text(encoding="utf-8")
        assert body_first == body_second
        # Single BEGIN and END marker (no duplication)
        assert body_second.count("<!-- BEGIN REVIEW-STAMP-AUTO -->") == 1
        assert body_second.count("<!-- END REVIEW-STAMP-AUTO -->") == 1

    def test_inbox_drops_backfilled_row(self, fixture_registry, monkeypatch, tmp_path):
        _patch_registry(fixture_registry, monkeypatch)
        today = date(2026, 5, 14)
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-I-03", "inception_date": "2025-01-01"}],
        )
        inbox = tmp_path / "REVIEW_STAMP_INBOX.md"
        argv_first = ["--today", today.isoformat(), "--inbox-path", str(inbox)]
        vrs.main(argv_first)
        body_first = inbox.read_text(encoding="utf-8")
        assert "INIT-I-03" in body_first

        # Backfill the row
        _write_csv(
            fixture_registry["initiatives_csv"],
            _initiative_registry_header(),
            [{"initiative_id": "INIT-I-03", "inception_date": "2025-01-01",
              "last_review_at": today.isoformat(), "last_review_by": "PMO",
              "methodology_version_at_review": "v3.1"}],
        )
        vrs.main(argv_first)
        body_second = inbox.read_text(encoding="utf-8")
        assert "INIT-I-03" not in body_second


# ---------------------------------------------------------------------------
# Smoke test — the actual canonical CSVs run cleanly (no error advisories)
# ---------------------------------------------------------------------------


class TestRealCanonicalsSmoke:
    def test_real_validate_review_stamps_no_error_advisories(self, tmp_path):
        """Smoke-check that the actual mirrored canonicals don't carry invalid-decision-ref errors."""
        inbox = tmp_path / "REVIEW_STAMP_INBOX.md"
        ec = vrs.main(["--inbox-path", str(inbox), "--json-log", "--no-inbox"])
        assert ec == 0  # exit 0 means no errors (info advisories OK)


# ---------------------------------------------------------------------------
# I71 P4 follow-up — Round-2 expansion (D-IH-71-R)
# ---------------------------------------------------------------------------


class TestRegistryExpansion:
    """Confirms the validator's _REGISTRY grew from 4 (P4) to 21 (P4 + follow-up) entries."""

    def test_registry_has_21_entries(self):
        assert len(vrs._REGISTRY) == 21

    def test_registry_includes_all_p4_followup_labels(self):
        labels = {spec.label for spec in vrs._REGISTRY}
        # P4 baseline (4)
        assert "process_list" in labels
        assert "decision_register" in labels
        assert "initiative_registry" in labels
        assert "ops_register" in labels
        # P4 follow-up (17)
        for label in (
            "baseline_organisation",
            "finops_counterparty_register",
            "goipoi_register",
            "adviser_engagement_disciplines",
            "adviser_open_questions",
            "founder_filed_instruments",
            "program_registry",
            "topic_registry",
            "persona_registry",
            "persona_scenario_registry",
            "channel_touchpoint_registry",
            "sourcing_register",
            "skill_registry",
            "touchpoint_kit_cell",
            "policy_register",
            "repo_health_snapshot",
            "repository_registry",
        ):
            assert label in labels, f"missing {label}"


class TestColumnExtensionMigrationExpanded:
    """One assertion per newly-extended SSOT tuple confirms it carries the 4 review-stamp columns."""

    def _assert_tuple_carries_stamps(self, fieldnames: tuple[str, ...], name: str) -> None:
        for col in vrs.REVIEW_STAMP_COLUMNS:
            assert col in fieldnames, f"{name} missing {col}"

    def test_baseline_organisation(self):
        from akos.hlk_baseline_org_csv import BASELINE_ORGANISATION_FIELDNAMES
        self._assert_tuple_carries_stamps(BASELINE_ORGANISATION_FIELDNAMES, "BASELINE_ORGANISATION_FIELDNAMES")

    def test_finops_counterparty_register(self):
        from akos.hlk_finops_counterparty_csv import FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES
        self._assert_tuple_carries_stamps(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES, "FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES")

    def test_goipoi_register(self):
        from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES
        self._assert_tuple_carries_stamps(GOIPOI_REGISTER_FIELDNAMES, "GOIPOI_REGISTER_FIELDNAMES")

    def test_adviser_engagement_disciplines(self):
        from akos.hlk_adviser_disciplines_csv import ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES
        self._assert_tuple_carries_stamps(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES, "ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES")

    def test_adviser_open_questions(self):
        from akos.hlk_adviser_questions_csv import ADVISER_OPEN_QUESTIONS_FIELDNAMES
        self._assert_tuple_carries_stamps(ADVISER_OPEN_QUESTIONS_FIELDNAMES, "ADVISER_OPEN_QUESTIONS_FIELDNAMES")

    def test_founder_filed_instruments(self):
        # I81 P2 T3 (D-IH-81-S, 2026-05-23): module renamed; legacy import shim still resolves for one initiative cycle.
        from akos.hlk_filed_instruments_csv import FILED_INSTRUMENTS_FIELDNAMES
        self._assert_tuple_carries_stamps(FILED_INSTRUMENTS_FIELDNAMES, "FILED_INSTRUMENTS_FIELDNAMES")
        # Verify deprecation shim still re-exports the legacy alias.
        from akos.hlk_founder_filed_instruments_csv import FOUNDER_FILED_INSTRUMENTS_FIELDNAMES
        assert FOUNDER_FILED_INSTRUMENTS_FIELDNAMES == FILED_INSTRUMENTS_FIELDNAMES

    def test_program_registry(self):
        from akos.hlk_program_registry_csv import PROGRAM_REGISTRY_FIELDNAMES
        self._assert_tuple_carries_stamps(PROGRAM_REGISTRY_FIELDNAMES, "PROGRAM_REGISTRY_FIELDNAMES")

    def test_topic_registry(self):
        from akos.hlk_topic_registry_csv import TOPIC_REGISTRY_FIELDNAMES
        self._assert_tuple_carries_stamps(TOPIC_REGISTRY_FIELDNAMES, "TOPIC_REGISTRY_FIELDNAMES")

    def test_persona_registry(self):
        from akos.hlk_persona_registry_csv import PERSONA_REGISTRY_FIELDNAMES
        self._assert_tuple_carries_stamps(PERSONA_REGISTRY_FIELDNAMES, "PERSONA_REGISTRY_FIELDNAMES")

    def test_persona_scenario_registry(self):
        from akos.hlk_persona_scenario_csv import PERSONA_SCENARIO_REGISTRY_FIELDNAMES
        self._assert_tuple_carries_stamps(PERSONA_SCENARIO_REGISTRY_FIELDNAMES, "PERSONA_SCENARIO_REGISTRY_FIELDNAMES")

    def test_channel_touchpoint_registry(self):
        from akos.hlk_channel_touchpoint_registry_csv import CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES
        self._assert_tuple_carries_stamps(CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES, "CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES")

    def test_sourcing_register(self):
        from akos.hlk_sourcing_register_csv import SOURCING_REGISTER_FIELDNAMES
        self._assert_tuple_carries_stamps(SOURCING_REGISTER_FIELDNAMES, "SOURCING_REGISTER_FIELDNAMES")

    def test_skill_registry(self):
        from akos.hlk_skill_registry_csv import SKILL_REGISTRY_FIELDNAMES
        self._assert_tuple_carries_stamps(SKILL_REGISTRY_FIELDNAMES, "SKILL_REGISTRY_FIELDNAMES")

    def test_touchpoint_kit_cell(self):
        from akos.hlk_touchpoint_kit_cell_csv import TOUCHPOINT_KIT_CELL_FIELDNAMES
        self._assert_tuple_carries_stamps(TOUCHPOINT_KIT_CELL_FIELDNAMES, "TOUCHPOINT_KIT_CELL_FIELDNAMES")

    def test_policy_register(self):
        from akos.hlk_policy_register_csv import POLICY_REGISTER_FIELDNAMES
        self._assert_tuple_carries_stamps(POLICY_REGISTER_FIELDNAMES, "POLICY_REGISTER_FIELDNAMES")

    def test_repo_health_snapshot(self):
        from akos.hlk_repo_health_csv import REPO_HEALTH_SNAPSHOT_FIELDNAMES
        self._assert_tuple_carries_stamps(REPO_HEALTH_SNAPSHOT_FIELDNAMES, "REPO_HEALTH_SNAPSHOT_FIELDNAMES")

    def test_repository_registry(self):
        from akos.hlk_repository_registry_csv import REPOSITORY_REGISTRY_FIELDNAMES
        self._assert_tuple_carries_stamps(REPOSITORY_REGISTRY_FIELDNAMES, "REPOSITORY_REGISTRY_FIELDNAMES")


class TestArtifactScan:
    """I71 P4 follow-up — Artifact subject class scan over CANONICAL_REGISTRY.csv."""

    def _write_canonical_registry(self, path: Path, rows: list[dict[str, str]]) -> None:
        header = [
            "canonical_id", "name", "owning_area", "owning_role", "file_path",
            "artifact_type", "supabase_schema", "mirror_table", "view_name",
            "panel_slot", "classification", "confidentiality", "last_review",
            "validator", "status", "notes",
        ]
        _write_csv(path, header, rows)

    def test_fresh_canonical_no_advisory(self, tmp_path, monkeypatch):
        today = date(2026, 5, 14)
        fixture = tmp_path / "CANONICAL_REGISTRY.csv"
        self._write_canonical_registry(fixture, [
            {"canonical_id": "brand_vision", "file_path": "docs/.../BRAND_VISION.md",
             "last_review": (today - timedelta(days=10)).isoformat(), "status": "active"},
        ])
        monkeypatch.setattr(vrs, "CANONICAL_REGISTRY_CSV", fixture)
        report = vrs._scan_canonical_md_artifacts(today=today, threshold_days=180, decision_ids=set())
        assert report.rows_total == 1
        assert report.rows_with_stamp == 1
        assert report.rows_stale == 0
        assert report.rows_missing_stamp == 0
        assert len(report.advisories) == 0

    def test_stale_canonical_emits_warning(self, tmp_path, monkeypatch):
        today = date(2026, 5, 14)
        fixture = tmp_path / "CANONICAL_REGISTRY.csv"
        self._write_canonical_registry(fixture, [
            {"canonical_id": "old_canonical", "file_path": "docs/.../OLD.md",
             "last_review": (today - timedelta(days=200)).isoformat(), "status": "active"},
        ])
        monkeypatch.setattr(vrs, "CANONICAL_REGISTRY_CSV", fixture)
        report = vrs._scan_canonical_md_artifacts(today=today, threshold_days=180, decision_ids=set())
        assert report.rows_stale == 1
        assert report.advisories[0].severity == "warning"
        assert report.advisories[0].rule == "stale-row"
        assert "OLD.md" in report.advisories[0].pk

    def test_missing_stamp_emits_info(self, tmp_path, monkeypatch):
        today = date(2026, 5, 14)
        fixture = tmp_path / "CANONICAL_REGISTRY.csv"
        self._write_canonical_registry(fixture, [
            {"canonical_id": "no_stamp_canonical", "file_path": "docs/.../NEW.md",
             "last_review": "", "status": "active"},
        ])
        monkeypatch.setattr(vrs, "CANONICAL_REGISTRY_CSV", fixture)
        report = vrs._scan_canonical_md_artifacts(today=today, threshold_days=180, decision_ids=set())
        assert report.rows_missing_stamp == 1
        assert report.advisories[0].severity == "info"
        assert report.advisories[0].rule == "missing-stamp"

    def test_proposed_canonical_without_path_skipped(self, tmp_path, monkeypatch):
        """status='proposed' rows with empty file_path must be skipped silently."""
        today = date(2026, 5, 14)
        fixture = tmp_path / "CANONICAL_REGISTRY.csv"
        self._write_canonical_registry(fixture, [
            {"canonical_id": "future_reserved", "file_path": "",
             "last_review": today.isoformat(), "status": "proposed"},
        ])
        monkeypatch.setattr(vrs, "CANONICAL_REGISTRY_CSV", fixture)
        report = vrs._scan_canonical_md_artifacts(today=today, threshold_days=180, decision_ids=set())
        assert report.rows_total == 0  # proposed/no-path row is silently skipped
        assert len(report.advisories) == 0

    def test_threshold_boundary_at_180_no_advisory(self, tmp_path, monkeypatch):
        """Exactly 180-day-old stamp is NOT stale (>threshold is the trigger)."""
        today = date(2026, 5, 14)
        fixture = tmp_path / "CANONICAL_REGISTRY.csv"
        self._write_canonical_registry(fixture, [
            {"canonical_id": "boundary_canonical", "file_path": "docs/.../BOUNDARY.md",
             "last_review": (today - timedelta(days=180)).isoformat(), "status": "active"},
        ])
        monkeypatch.setattr(vrs, "CANONICAL_REGISTRY_CSV", fixture)
        report = vrs._scan_canonical_md_artifacts(today=today, threshold_days=180, decision_ids=set())
        assert report.rows_stale == 0


class TestComplianceSchemaDriftRegression:
    """Regression: validate_compliance_schema_drift.py PASSes for all 22 registry CSVs after follow-up."""

    def test_drift_validator_passes_after_p4_followup(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate_compliance_schema_drift.py")],
            capture_output=True, text=True, timeout=60,
        )
        assert result.returncode == 0, f"drift validator FAILED:\n{result.stdout}\n{result.stderr}"
        assert "PASS: every canonical CSV header aligns" in result.stdout


class TestRealCanonicalsSmokeExpanded:
    """I71 P4 follow-up — smoke-check the validator runs cleanly across all 21 surfaces + Artifact."""

    def test_validator_exits_zero_post_followup(self, tmp_path):
        inbox = tmp_path / "REVIEW_STAMP_INBOX.md"
        ec = vrs.main(["--inbox-path", str(inbox), "--no-inbox"])
        assert ec == 0  # exit 0 means no errors (info advisories OK)

    def test_validator_reports_22_surfaces_in_human_output(self, tmp_path, capsys):
        ec = vrs.main(["--no-inbox"])
        assert ec == 0
        captured = capsys.readouterr()
        # 21 mirrors + 1 Artifact scan = 22 reports
        assert "checked 22 canonical CSVs" in captured.out

    def test_artifact_scan_label_present_in_output(self, tmp_path, capsys):
        ec = vrs.main(["--no-inbox"])
        assert ec == 0
        captured = capsys.readouterr()
        assert "canonical_registry_artifact" in captured.out
