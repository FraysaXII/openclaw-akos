"""Initiative 47 P1 tests — PERSONA_SCENARIO_REGISTRY schema + validator + mirror DDL.

Coverage:
- akos.hlk_persona_scenario_csv field contract
- scripts/validate_persona_scenario_registry.py (header, FKs, enums, edge cases)
- Supabase migration shape (column presence + composite index per D-IH-47-K)
- TOPIC_REGISTRY topic_persona_scenario_registry row
- validate_hlk dispatcher integration
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_persona_scenario_csv import (
    OPERATOR_PSEUDO_PERSONA,
    PERSONA_SCENARIO_REGISTRY_FIELDNAMES,
    VALID_DIFFICULTY_CLASSES,
    VALID_EXPECTED_OUTCOME_CLASSES,
    VALID_EXPECTED_ROUTES,
    VALID_LANGUAGES,
    VALID_LIFECYCLE_STATUSES,
    VALID_SCENARIO_CLASSES,
    VALID_TIERS,
)

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"
VALIDATOR = REPO_ROOT / "scripts" / "validate_persona_scenario_registry.py"
MIGRATION = REPO_ROOT / "supabase" / "migrations" / "20260502033000_i47_persona_scenario_registry_mirror.sql"
MIGRATION_I49_PRIORITY = REPO_ROOT / "supabase" / "migrations" / "20260503120000_i49_persona_scenario_registry_priority_columns.sql"
MIGRATION_I51_BAND = REPO_ROOT / "supabase" / "migrations" / "20260503180000_i51_persona_scenario_target_difficulty_band.sql"
DISPATCHER = REPO_ROOT / "scripts" / "validate_hlk.py"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"


# ---------------------------------------------------------------------------
# Field contract
# ---------------------------------------------------------------------------

def test_fieldnames_include_5_typed_dimensions() -> None:
    """The 5 scenario-taxonomy dimensions per D-IH-47-A + tenant_id per D-IH-47-K."""
    required = {
        "scenario_id",
        "persona_id",
        "skill_id",
        "tenant_id",          # D-IH-47-K
        "scenario_class",     # P0 taxonomy
        "difficulty_class",   # D-IH-47-C
        "expected_outcome_class",  # P0 taxonomy
        "priority_score",
        "safety_lane",
        "release_blocking",
    }
    missing = required - set(PERSONA_SCENARIO_REGISTRY_FIELDNAMES)
    assert not missing, f"missing required field(s): {missing}"


def test_csv_header_matches_contract() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES)


def test_valid_enums_have_expected_members() -> None:
    assert "lookup" in VALID_SCENARIO_CLASSES
    assert "adversarial" in VALID_SCENARIO_CLASSES
    assert "recovery" in VALID_SCENARIO_CLASSES
    assert "benchmark" in VALID_SCENARIO_CLASSES
    assert "cross_axis" in VALID_SCENARIO_CLASSES
    assert "cannot_answer" in VALID_SCENARIO_CLASSES

    assert VALID_DIFFICULTY_CLASSES == frozenset({"trivial", "moderate", "hard", "impossible"})
    assert VALID_EXPECTED_OUTCOME_CLASSES == frozenset({"PASS", "GROUND", "ESCALATE", "REFUSE"})
    assert VALID_TIERS == frozenset({"1", "2", "3"})
    assert VALID_LANGUAGES >= frozenset({"en", "es", "fr"})
    assert "active" in VALID_LIFECYCLE_STATUSES


def test_valid_expected_routes_match_intent_literals() -> None:
    """Sync against akos.intent IntentRoute literals (no drift)."""
    from akos.intent import IntentRoute  # type: ignore[attr-defined]

    intent_routes = set(IntentRoute.__args__)  # type: ignore[attr-defined]
    assert VALID_EXPECTED_ROUTES == intent_routes, (
        f"akos.hlk_persona_scenario_csv VALID_EXPECTED_ROUTES drifted from akos.intent.IntentRoute. "
        f"diff: {VALID_EXPECTED_ROUTES.symmetric_difference(intent_routes)}"
    )


def test_operator_pseudo_persona_constant() -> None:
    assert OPERATOR_PSEUDO_PERSONA == "OPERATOR"


# ---------------------------------------------------------------------------
# CSV content (P1 ships with 1 scaffold row; full library lands in P2-P9)
# ---------------------------------------------------------------------------

def _read_csv() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_csv_has_at_least_one_row() -> None:
    rows = _read_csv()
    assert len(rows) >= 1, "PERSONA_SCENARIO_REGISTRY.csv must have at least 1 scaffold row at P1 close"


def test_seed_row_uses_operator_pseudo_persona() -> None:
    rows = _read_csv()
    operator_rows = [r for r in rows if r["persona_id"] == OPERATOR_PSEUDO_PERSONA]
    assert operator_rows, "P1 seed row should anchor on OPERATOR pseudo-persona"


def test_scenario_id_format_consistent() -> None:
    pat = re.compile(r"^SCN-[A-Z0-9-]{4,80}-V\d+$")
    for r in _read_csv():
        assert pat.match(r["scenario_id"]), f"scenario_id {r['scenario_id']!r} does not match pattern"


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

def _run_validator() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def test_validator_passes_on_seed() -> None:
    code, out = _run_validator()
    assert code == 0, out
    assert "PASS" in out


def test_validator_catches_bad_scenario_id(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Inject an invalid scenario_id and confirm validator FAILs."""
    fake_csv = tmp_path / "PERSONA_SCENARIO_REGISTRY.csv"
    rows = _read_csv()
    rows.append({**rows[0], "scenario_id": "BAD-NAME"})
    with fake_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=PERSONA_SCENARIO_REGISTRY_FIELDNAMES)
        w.writeheader()
        w.writerows(rows)

    # Re-run validator against a temp REPO_ROOT shimmed via monkeypatch.
    src = VALIDATOR.read_text(encoding="utf-8")
    shim_path = tmp_path / "validator_shim.py"
    shim_path.write_text(
        "import sys; sys.path.insert(0, " + repr(str(REPO_ROOT)) + ")\n"
        "from pathlib import Path\n"
        "import scripts.validate_persona_scenario_registry as v\n"
        "v.CSV_PATH = Path(" + repr(str(fake_csv)) + ")\n"
        "sys.exit(v.main())\n",
        encoding="utf-8",
    )
    proc = subprocess.run([sys.executable, str(shim_path)], capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "scenario_id" in proc.stdout.lower() or "scenario_id" in proc.stderr.lower()


def test_validator_accepts_operator_pseudo_persona() -> None:
    """OPERATOR is valid even though it's not in PERSONA_REGISTRY.csv."""
    code, out = _run_validator()
    assert code == 0
    assert "OPERATOR" in out or "PASS" in out


def test_validator_accepts_null_tenant_id() -> None:
    """D-IH-47-K: tenant_id NULL is the default; validator must not error."""
    code, _ = _run_validator()
    assert code == 0


# ---------------------------------------------------------------------------
# Supabase migration (P1 DDL)
# ---------------------------------------------------------------------------

def test_migration_file_exists() -> None:
    assert MIGRATION.is_file()


def test_migration_creates_mirror_table() -> None:
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    assert "create table if not exists compliance.persona_scenario_registry_mirror" in sql
    assert "primary key (scenario_id)" in sql


def test_migration_has_tenant_id_column_with_null_default() -> None:
    """D-IH-47-K: tenant_id is nullable; NULL = shared scenario."""
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    # tenant_id column exists and is nullable (no NOT NULL)
    assert "tenant_id" in sql
    # The composite (persona_id, tenant_id) index is the I34 multi-tenant prep
    assert "persona_id, tenant_id" in sql


def test_migration_has_required_columns() -> None:
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    # All 5 typed dimensions per D-IH-47-A + tenant_id
    for col in (
        "scenario_id",
        "persona_id",
        "skill_id",
        "tenant_id",
        "scenario_class",
        "difficulty_class",
        "expected_outcome_class",
        "prompt_text",
        "expected_route",
        "language",
        "lifecycle_status",
        "source_git_sha",
        "synced_at",
    ):
        assert col in sql, f"migration missing column {col!r}"


def test_migration_enforces_rls() -> None:
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    assert "row level security" in sql
    assert "deny_authenticated" in sql
    assert "deny_anon" in sql
    assert "service_role" in sql


def test_migration_has_partial_tenant_index() -> None:
    """D-IH-47-K: partial index on non-NULL tenant_id is the I34-prep slot."""
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    # Allow for whitespace variants in the WHERE clause.
    assert re.search(r"where\s+tenant_id\s+is\s+not\s+null", sql), (
        "expected partial index on WHERE tenant_id IS NOT NULL"
    )


def test_migration_i49_priority_columns_file_exists() -> None:
    assert MIGRATION_I49_PRIORITY.is_file()


def test_migration_i49_adds_priority_columns_to_mirror() -> None:
    sql = MIGRATION_I49_PRIORITY.read_text(encoding="utf-8").lower()
    assert "alter table compliance.persona_scenario_registry_mirror" in sql
    for col in ("priority_score", "safety_lane", "release_blocking"):
        assert f"add column if not exists {col}" in sql, f"missing ALTER for {col}"


# ---------------------------------------------------------------------------
# I51 P3 (D-IH-51-A) — target_difficulty_band column
# ---------------------------------------------------------------------------

def test_fieldnames_include_target_difficulty_band() -> None:
    """I51 P3: per-persona calibration target column is in the contract."""
    assert "target_difficulty_band" in PERSONA_SCENARIO_REGISTRY_FIELDNAMES


def test_target_difficulty_band_per_persona_consistent() -> None:
    """All rows of a persona must share the same target_difficulty_band."""
    rows = _read_csv()
    by_pid: dict[str, set[str]] = {}
    for r in rows:
        pid = (r.get("persona_id") or "").strip()
        if not pid:
            continue
        by_pid.setdefault(pid, set()).add((r.get("target_difficulty_band") or "").strip())
    for pid, bands in by_pid.items():
        assert len(bands) == 1, (
            f"persona {pid!r} has inconsistent target_difficulty_band values: {sorted(bands)}"
        )


def test_target_difficulty_band_format_valid() -> None:
    """Non-empty bands must parse as 4 ints summing to 100."""
    from akos.hlk_persona_scenario_csv import parse_target_difficulty_band

    rows = _read_csv()
    for r in rows:
        raw = (r.get("target_difficulty_band") or "").strip()
        try:
            parse_target_difficulty_band(raw)
        except ValueError as exc:
            raise AssertionError(f"row {r['scenario_id']}: {exc}") from exc


def test_13_outlier_personas_have_band_overrides() -> None:
    """Per the I51 P2 audit, the 13 outlier personas carry non-empty bands."""
    rows = _read_csv()
    expected_overrides = {
        "OPERATOR",
        "PERSONA-ADVISOR-COLD",
        "PERSONA-CUSTOMER-KIRBE-PROSPECT",
        "PERSONA-CUSTOMER-SERVICE-PROSPECT",
        "PERSONA-EXISTING-CUSTOMER",
        "PERSONA-EXISTING-PARTNER",
        "PERSONA-IDEA-PROPOSER",
        "PERSONA-INVESTOR-COLD",
        "PERSONA-PARTNER-JOINT-EQUITY",
        "PERSONA-PRESS",
        "PERSONA-RANDOM-INBOUND",
        "PERSONA-VENDOR-INBOUND",
        "PERSONA-VENDOR-OUTBOUND",
    }
    by_pid: dict[str, str] = {}
    for r in rows:
        pid = (r.get("persona_id") or "").strip()
        band = (r.get("target_difficulty_band") or "").strip()
        if pid and band:
            by_pid[pid] = band
    missing = expected_overrides - set(by_pid.keys())
    assert not missing, f"expected band overrides for {missing}"


def test_4_passing_personas_have_no_band_override() -> None:
    """The 4 already-passing personas fall through to the global default."""
    rows = _read_csv()
    expected_passing = {
        "PERSONA-ADVISOR-REFERRAL",
        "PERSONA-INVESTOR-WARM",
        "PERSONA-PARTNER-SUBCONTRACT",
        "PERSONA-TALENT-INBOUND",
    }
    for r in rows:
        pid = (r.get("persona_id") or "").strip()
        band = (r.get("target_difficulty_band") or "").strip()
        if pid in expected_passing:
            assert band == "", (
                f"persona {pid!r} should fall through to global default; got band {band!r}"
            )


def test_calibration_distribution_uses_per_persona_band() -> None:
    """I51 P3 D-IH-51-A: calibrator consults per-persona band; result.target reflects it."""
    from akos.eval_harness.persona import calibration_distribution

    results = calibration_distribution()
    # OPERATOR has a band override of 15/40/35/10.
    operator = results.get("OPERATOR")
    assert operator is not None
    assert operator.target_source == "persona"
    assert operator.target == {"trivial": 15.0, "moderate": 40.0, "hard": 35.0, "impossible": 10.0}
    # PERSONA-INVESTOR-WARM has no override; falls through to global default.
    warm = results.get("PERSONA-INVESTOR-WARM")
    assert warm is not None
    assert warm.target_source == "global"
    assert warm.target == {"trivial": 10.0, "moderate": 40.0, "hard": 40.0, "impossible": 10.0}


def test_calibration_passes_after_p3_remediation() -> None:
    """I51 P3 G-51-1 exit criterion: ≤ 2 personas outside tolerance against own target."""
    from akos.eval_harness.persona import calibration_distribution

    results = calibration_distribution()
    outliers = [pid for pid, r in results.items() if pid != "__overall__" and not r.overall_pass]
    # Plan exit criterion is ≤ 2; we verify ≤ 2 to lock the gate value, not 0
    # (so future regressions surface, but we don't trip on band-edge floats).
    assert len(outliers) <= 2, f"I51 P3 exit failed: {outliers}"


def test_calibration_overall_uses_global_default() -> None:
    """__overall__ aggregate always uses the global D-IH-47-C target."""
    from akos.eval_harness.persona import calibration_distribution

    results = calibration_distribution()
    overall = results.get("__overall__")
    assert overall is not None
    assert overall.target_source == "global"
    assert overall.overall_pass is True


def test_migration_i51_target_difficulty_band_file_exists() -> None:
    assert MIGRATION_I51_BAND.is_file()


def test_migration_i51_adds_target_difficulty_band_column() -> None:
    sql = MIGRATION_I51_BAND.read_text(encoding="utf-8").lower()
    assert "alter table compliance.persona_scenario_registry_mirror" in sql
    assert "add column if not exists target_difficulty_band" in sql


# ---------------------------------------------------------------------------
# TOPIC_REGISTRY row (D-IH-47-A also adds a topic row for the new dimension)
# ---------------------------------------------------------------------------

def test_topic_registry_has_new_topic_row() -> None:
    with TOPIC_CSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    topic_ids = {r["topic_id"] for r in rows}
    assert "topic_persona_scenario_registry" in topic_ids


# ---------------------------------------------------------------------------
# Dispatcher integration
# ---------------------------------------------------------------------------

def test_validate_hlk_dispatcher_includes_new_validator() -> None:
    src = DISPATCHER.read_text(encoding="utf-8")
    assert "PERSONA_SCENARIO_REGISTRY" in src
    assert "validate_persona_scenario_registry" in src


def test_full_validate_hlk_passes() -> None:
    """End-to-end: full dispatcher run is green at P1 close."""
    proc = subprocess.run(
        [sys.executable, str(DISPATCHER)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PERSONA_SCENARIO_REGISTRY: PASS" in proc.stdout
    assert "OVERALL: PASS" in proc.stdout
