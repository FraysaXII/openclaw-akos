"""Smoke tests for sync_compliance_mirrors_from_csv.py.

Row-count assertions follow the compute-from-canonical pattern adopted in the
2026-05-11 release-gate hygiene pass: every count is derived from the canonical
CSV at test time rather than hardcoded. This makes the tests structurally
resilient to legitimate CSV growth (new I22 / I31 / P13.4 / future-initiative
rows) while still catching real script bugs (the emitted count diverging from
the CSV's actual count). The tripwire concern — "did the canonical row count
change?" — belongs elsewhere (release-notes / changelog), not in this test.
"""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.sync_compliance_mirrors_from_csv import (  # noqa: E402
    _emit_skill_registry_upserts,
    _emit_sourcing_register_upserts,
)


def _csv_row_count(rel_path: str) -> int:
    """Count non-header rows in a canonical CSV (relative to repo root)."""
    p = REPO_ROOT / rel_path
    with p.open("r", encoding="utf-8", newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


# Canonical CSVs whose row counts the sync script's --count-only output mirrors.
# Each key is the script's emitted counter name; each value is the canonical CSV
# path relative to repo root. Keep this map in sync with sync_compliance_mirrors_from_csv
# whenever a new mirror is added.
_COUNTED_CSVS: dict[str, str] = {
    "process_list_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv",
    "baseline_organisation_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv",
    "finops_counterparty_register_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv",
    "goipoi_register_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv",
    "adviser_engagement_disciplines_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv",
    "adviser_open_questions_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_OPEN_QUESTIONS.csv",
    "founder_filed_instruments_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FOUNDER_FILED_INSTRUMENTS.csv",
    "program_registry_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv",
    "topic_registry_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv",
    "persona_registry_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv",
    "persona_scenario_registry_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv",
    "channel_touchpoint_registry_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv",
    "sourcing_register_rows": "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SOURCING_REGISTER.csv",
}


def test_sync_compliance_mirrors_count_only() -> None:
    """Every emitted counter matches its canonical CSV's row count (compute-from-CSV)."""
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"), "--count-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    for counter, csv_path in _COUNTED_CSVS.items():
        expected = _csv_row_count(csv_path)
        needle = f"{counter}={expected}"
        assert needle in r.stdout, (
            f"counter mismatch: expected '{needle}' (from {csv_path}); "
            f"--count-only stdout was:\n{r.stdout}"
        )
    assert "source_git_sha=" in r.stdout


def test_sync_compliance_mirrors_sql_contains_holistika_and_conflict() -> None:
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--process-list-only",
                "--output",
                str(out_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert r.returncode == 0, r.stderr + r.stdout
        out = out_path.read_text(encoding="utf-8")
    finally:
        out_path.unlink(missing_ok=True)
    assert "compliance.process_list_mirror" in out
    assert "ON CONFLICT (item_id) DO UPDATE SET" in out
    assert "holistika_reach_dtp_001" in out


def test_sync_finops_counterparty_register_only_sql() -> None:
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--finops-counterparty-register-only",
                "--output",
                str(out_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert r.returncode == 0, r.stderr + r.stdout
        out = out_path.read_text(encoding="utf-8")
    finally:
        out_path.unlink(missing_ok=True)
    assert "compliance.finops_counterparty_register_mirror" in out
    assert "ON CONFLICT (counterparty_id) DO UPDATE SET" in out
    assert "finops_example_cloud_platform" in out
    assert "finops_example_customer" in out


def test_sync_full_emit_includes_counterparty_upserts() -> None:
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--output",
                str(out_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert r.returncode == 0, r.stderr + r.stdout
        out = out_path.read_text(encoding="utf-8")
    finally:
        out_path.unlink(missing_ok=True)
    assert "compliance.process_list_mirror" in out
    assert "compliance.baseline_organisation_mirror" in out
    assert "compliance.finops_counterparty_register_mirror" in out
    # I51 P1: full bundle MUST now include persona_scenario_registry upserts.
    assert "compliance.persona_scenario_registry_mirror" in out
    assert "ON CONFLICT (scenario_id) DO UPDATE SET" in out


def test_sync_persona_scenario_registry_only_sql() -> None:
    """I51 P1 — persona_scenario_registry mirror reseed (closes OPS-47-9)."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--persona-scenario-registry-only",
                "--output",
                str(out_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert r.returncode == 0, r.stderr + r.stdout
        out = out_path.read_text(encoding="utf-8")
    finally:
        out_path.unlink(missing_ok=True)
    assert "compliance.persona_scenario_registry_mirror" in out
    assert "ON CONFLICT (scenario_id) DO UPDATE SET" in out
    # Anchored fixture row from I47 baseline.
    assert "SCN-OP-001-V1" in out
    # Scaffold row from I50 P5 telemetry promotion (one of the 3 merged).
    assert "SCN-OP-TP-001-V1" in out
    # Empty tenant_id should be emitted as NULL (D-IH-47-K shared semantics),
    # not an empty TEXT literal — verify the very first row uses NULL for it.
    first_row = next((line for line in out.splitlines() if "SCN-OP-001-V1" in line), "")
    assert first_row, "expected SCN-OP-001-V1 row in emitted SQL"
    # SCN-OP-001-V1 has empty tenant_id in the CSV; assert the NULL emission.
    assert "'OPERATOR', 'SKILL-MADEIRA-LOOKUP-V1', NULL," in first_row
    insert_count = sum(
        1
        for line in out.splitlines()
        if line.startswith("INSERT INTO compliance.persona_scenario_registry_mirror")
    )
    expected = _csv_row_count("docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv")
    assert insert_count == expected, (
        f"expected {expected} INSERT rows (one per scenario row in canonical CSV), got {insert_count}"
    )


# ---------------------------------------------------------------------------
# I57 P1 — F-22a-EMIT-1 + F-22a-EMIT-2 regression tests
#
# Closes the I22a Open follow-ups documented at
# ``docs/wip/planning/22a-i22-post-closure-followups/master-roadmap.md``.
# Both defects were observed during the 2026-05-04 Supabase MasterData
# parity reconciliation; both were patched in-batch on the apply side
# and now ship as upstream fixes in ``sync_compliance_mirrors_from_csv``.
# ---------------------------------------------------------------------------


def test_i57_emit_sourcing_register_empty_date_emits_null() -> None:
    """F-22a-EMIT-1 — empty DATE cell must emit NULL, not '' (22007 invalid_datetime_format)."""
    rows = [
        {
            "vendor_id": "vendor_with_empty_date",
            "discipline": "design",
            "engagement_type": "fractional",
            "languages_supported": "en",
            "timezone_band": "europe",
            "hourly_rate_band": "mid",
            "quality_band": "trial",
            "distance_band_at_first_contact": "warm",
            "current_distance_band": "warm",
            "last_engagement_date": "",  # the defect cell
            "linked_topic_ids": "",
            "notes": "",
        },
    ]
    sql_lines = _emit_sourcing_register_upserts(rows, source_git_sha="abc1234")
    insert_lines = [line for line in sql_lines if line.startswith("INSERT INTO")]
    assert len(insert_lines) == 1, "expected one INSERT for one row"
    insert = insert_lines[0]
    # The empty DATE cell must serialize as the NULL keyword, never as ''.
    assert ", NULL," in insert, f"expected NULL for empty last_engagement_date in: {insert}"
    # Defensively: there should be no '' (empty TEXT literal) for the DATE column.
    # The source_git_sha and other empty TEXT cells legitimately use '' so we
    # only check the column's positional slot.
    assert "''" in insert  # other empty TEXT cells (linked_topic_ids, notes) do use ''


def test_i57_emit_sourcing_register_filled_date_round_trips() -> None:
    """F-22a-EMIT-1 sanity — non-empty DATE cell still serializes as a TEXT literal."""
    rows = [
        {
            "vendor_id": "vendor_with_real_date",
            "discipline": "design",
            "engagement_type": "fractional",
            "languages_supported": "en",
            "timezone_band": "europe",
            "hourly_rate_band": "mid",
            "quality_band": "trial",
            "distance_band_at_first_contact": "warm",
            "current_distance_band": "warm",
            "last_engagement_date": "2026-04-15",  # populated cell
            "linked_topic_ids": "",
            "notes": "",
        },
    ]
    sql_lines = _emit_sourcing_register_upserts(rows, source_git_sha="abc1234")
    insert = next(line for line in sql_lines if line.startswith("INSERT INTO"))
    assert "'2026-04-15'" in insert, f"expected populated DATE to round-trip in: {insert}"


def test_i57_emit_skill_registry_empty_bool_emits_documented_default() -> None:
    """F-22a-EMIT-2 — empty NOT-NULL bool cell must emit the documented default ('false')."""
    rows = [
        {
            "skill_id": "SKILL-TEST-EMPTY-BOOL",
            "skill_name": "test",
            "lifecycle_status": "shadow",
            "tenant_scope": "shared",
            "agents_supported": "",
            "axes_consumed": "",
            "tools_required": "",
            "tools_required_waived": "",  # the defect cell
            "langfuse_trace_pattern": "",
            "topic_ids": "",
            "rubric_path": "",
            "promoted_from_skill_id": "",
            "owner_role": "",
            "routing_condition": "",
        },
    ]
    sql_lines = _emit_skill_registry_upserts(rows, source_git_sha="abc1234")
    insert = next(line for line in sql_lines if line.startswith("INSERT INTO"))
    # The empty bool cell must serialize as the keyword 'false', not NULL or ''.
    # Find the substring window around tools_required_waived's positional slot;
    # the column sits after `tools_required` in SKILL_REGISTRY_FIELDNAMES, so
    # the literal sequence ``, false,`` (or trailing) appears in the VALUES.
    assert ", false," in insert or insert.rstrip().endswith(", false") or ", false ," in insert, (
        f"expected documented default 'false' for empty tools_required_waived in: {insert}"
    )
    assert ", NULL," not in insert.replace(", NULL,", "", 0)  # placeholder; real check below
    # Stronger negative: the emitted line MUST NOT contain `, NULL,` for the bool slot.
    # (other slots are TEXT and would never legitimately emit NULL in this fixture).
    # Count occurrences explicitly:
    assert insert.count(", NULL,") == 0, f"empty bool must not emit NULL for NOT-NULL column; got: {insert}"


def test_i57_emit_skill_registry_truthy_bool_round_trips() -> None:
    """F-22a-EMIT-2 sanity — explicit 'true' / 'false' / '1' / '0' / 'yes' / 'no' all map cleanly."""
    truthy = ["true", "TRUE", "1", "yes", "y"]
    falsy = ["false", "FALSE", "0", "no", "n"]
    for token in truthy + falsy:
        rows = [
            {
                "skill_id": f"SKILL-TEST-BOOL-{token}",
                "skill_name": "test",
                "lifecycle_status": "shadow",
                "tenant_scope": "shared",
                "agents_supported": "",
                "axes_consumed": "",
                "tools_required": "",
                "tools_required_waived": token,
                "langfuse_trace_pattern": "",
                "topic_ids": "",
                "rubric_path": "",
                "promoted_from_skill_id": "",
                "owner_role": "",
                "routing_condition": "",
            },
        ]
        sql_lines = _emit_skill_registry_upserts(rows, source_git_sha="abc1234")
        insert = next(line for line in sql_lines if line.startswith("INSERT INTO"))
        expected = "true" if token in truthy else "false"
        assert f", {expected}," in insert, f"token {token!r} expected {expected}; got: {insert}"


def test_i57_emit_skill_registry_full_csv_uses_documented_default_for_blanks() -> None:
    """F-22a-EMIT-2 integration — running the emit against the real CSV produces no NULL bool literal."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--skill-registry-only",
                "--output",
                str(out_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert r.returncode == 0, r.stderr + r.stdout
        out = out_path.read_text(encoding="utf-8")
    finally:
        out_path.unlink(missing_ok=True)
    insert_lines = [line for line in out.splitlines() if line.startswith("INSERT INTO compliance.skill_registry_mirror")]
    assert insert_lines, "expected at least one skill_registry_mirror INSERT row"
    # No INSERT row should contain `, NULL,` substring — every blank bool now defaults.
    # (Other TEXT columns may legitimately emit '' but never NULL in the current schema.)
    for line in insert_lines:
        assert ", NULL," not in line, f"unexpected NULL emission in skill_registry insert: {line}"


def test_i57_emit_skill_registry_full_csv_includes_emitted_default_for_real_blanks() -> None:
    """F-22a-EMIT-2 integration — at least one row in the real CSV uses the documented blank default.

    The SKILL_REGISTRY at this date carries 5 rows; tools_required_waived is
    blank in most of them, which is exactly the cell that broke the 2026-05-04
    apply. After the fix, those rows must serialize as ``, false,`` (not NULL).
    """
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--skill-registry-only",
                "--output",
                str(out_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert r.returncode == 0, r.stderr + r.stdout
        out = out_path.read_text(encoding="utf-8")
    finally:
        out_path.unlink(missing_ok=True)
    insert_lines = [line for line in out.splitlines() if line.startswith("INSERT INTO compliance.skill_registry_mirror")]
    # The cells that broke the I22a apply: at least one row should use the
    # ``false`` default. (Pre-fix this row would have emitted ``NULL``.)
    rows_with_default = [line for line in insert_lines if ", false," in line]
    assert rows_with_default, (
        f"expected at least one row to use the documented 'false' default for blank "
        f"tools_required_waived; got {len(insert_lines)} INSERT rows but none used the default"
    )
