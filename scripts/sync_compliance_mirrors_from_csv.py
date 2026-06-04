#!/usr/bin/env python3
"""Emit PostgreSQL upsert statements for compliance mirror tables from git CSVs.

Maps canonical ``process_list.csv``, ``baseline_organisation.csv``, and optionally
``FINOPS_COUNTERPARTY_REGISTER.csv`` to compliance mirror shapes in
``docs/wip/planning/14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md``
(Initiative 18 FINOPS counterparty mirror DDL under ``scripts/sql/i18_phase1_staging/``).
Does **not** connect to Supabase by default: outputs SQL for operator review / staging
``apply_migration`` after DDL exists.

Usage (repo root):

    py scripts/sync_compliance_mirrors_from_csv.py --count-only
    py scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only --output /tmp/finops-upsert.sql
    py scripts/sync_compliance_mirrors_from_csv.py --ops8615-gap-mirrors-only
        # default: docs/wip/planning/93-.../artifacts/ops8615-mirror-upsert.sql (repo-local)
    py scripts/sync_compliance_mirrors_from_csv.py --output /tmp/mirror-upsert.sql
    py scripts/sync_compliance_mirrors_from_csv.py --git-sha abc123def

Parent IDs: process rows are normalized and ``resolve_all_parent_ids`` is applied so
mirror content matches the same resolution as other HLK tooling.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_adviser_disciplines_csv import ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES  # noqa: E402
from akos.hlk_adviser_questions_csv import ADVISER_OPEN_QUESTIONS_FIELDNAMES  # noqa: E402
from akos.hlk_baseline_org_csv import BASELINE_ORGANISATION_FIELDNAMES  # noqa: E402  # release-gate hygiene 2026-05-11
from akos.hlk_finops_counterparty_csv import FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_filed_instruments_csv import FILED_INSTRUMENTS_FIELDNAMES  # noqa: E402  # I81 P2 T3 (D-IH-81-S, 2026-05-23) renamed from hlk_founder_filed_instruments_csv
from akos.hlk_dataops_quality import I93_P6_OPS8615_UPSERT_ARTIFACT  # noqa: E402  # I93 P6 default emit path
from akos.hlk_aic_registry_csv import AIC_REGISTRY_FIELDNAMES  # noqa: E402  # I93 P6 OPS-86-15
from akos.hlk_audience_csv import AUDIENCE_REGISTRY_FIELDNAMES  # noqa: E402  # I93 P6 OPS-86-15
from akos.hlk_capability_confidence_csv import CAPABILITY_CONFIDENCE_FIELDNAMES  # noqa: E402  # I93 P6
from akos.hlk_capability_registry_csv import CAPABILITY_REGISTRY_FIELDNAMES  # noqa: E402  # I93 P6
from akos.hlk_channel_touchpoint_registry_csv import CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_cycle_register_csv import CYCLE_REGISTER_FIELDNAMES  # noqa: E402  # I59 P1.4
from akos.hlk_decision_register_csv import DECISION_REGISTER_FIELDNAMES  # noqa: E402  # I59 P1.5
from akos.hlk_engagement_model_csv import ENGAGEMENT_MODEL_FIELDNAMES  # noqa: E402  # I73 P1 (D-IH-73-C sibling-dimension; D-IH-73-D 7-class taxonomy)
from akos.hlk_design_pattern_csv import DESIGN_PATTERN_FIELDNAMES  # noqa: E402  # I79 P2 (D-IH-79-C/D People design pattern library)
from akos.hlk_substrate_registry_csv import SUBSTRATE_REGISTRY_FIELDNAMES  # noqa: E402  # I84 P3 (D-IH-84-F substrate doctrine registry)
from akos.hlk_intelligenceops_register_csv import INTELLIGENCEOPS_REGISTER_FIELDNAMES  # noqa: E402  # I72 P6 + I75 (D-IH-72-H sibling canonical; D-IH-86-FH radar freshness cols)
from akos.hlk_collaborator_share import (  # noqa: E402  # I86 Wave R+1 P2c-a (D-IH-86-DA/DB/DC/DD/DE collaborator share doctrine)
    COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
    HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
    PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES,
    COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES,
    COLLABORATOR_RATE_OVERRIDES_FIELDNAMES,
    CSV_PATH_RELATIVE_SHARE_REGISTRY,
    CSV_PATH_RELATIVE_VENDOR_BILLED,
    CSV_PATH_RELATIVE_OVERLAP_CLAUSES,
    CSV_PATH_RELATIVE_MARKET_RATE,
    CSV_PATH_RELATIVE_RATE_OVERRIDES,
)
from akos.hlk_output_type_registry_csv import OUTPUT_TYPE_REGISTRY_FIELDNAMES  # noqa: E402  # I86 Wave L (D-IH-86-BG output architecture Layer 1)
from akos.hlk_artifact_class_registry_csv import ARTIFACT_CLASS_REGISTRY_FIELDNAMES  # noqa: E402  # I86 Wave L (D-IH-86-BG output architecture Layer 2)
from akos.hlk_component_primitive_registry_csv import COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES  # noqa: E402  # I86 Wave L (D-IH-86-BG output architecture Layer 3)
from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_initiative_registry_csv import INITIATIVE_REGISTRY_FIELDNAMES  # noqa: E402  # I59 P1.2
from akos.hlk_ops_register_csv import OPS_REGISTER_FIELDNAMES  # noqa: E402  # I59 P1.3
from akos.hlk_persona_registry_csv import PERSONA_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_persona_scenario_csv import PERSONA_SCENARIO_REGISTRY_FIELDNAMES  # noqa: E402  # I47 P1 + I49 (closes OPS-47-9 in I51 P1)
from akos.hlk_policy_register_csv import POLICY_REGISTER_FIELDNAMES  # noqa: E402  # I32 P4
from akos.hlk_program_registry_csv import PROGRAM_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_repo_health_csv import REPO_HEALTH_SNAPSHOT_FIELDNAMES  # noqa: E402  # I32 P7
from akos.hlk_repository_registry_csv import REPOSITORY_REGISTRY_FIELDNAMES  # noqa: E402  # I59 P1.1
from akos.hlk_skill_registry_csv import SKILL_REGISTRY_FIELDNAMES  # noqa: E402  # I32 P2
from akos.hlk_sourcing_register_csv import SOURCING_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_topic_registry_csv import TOPIC_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_touchpoint_kit_cell_csv import TOUCHPOINT_KIT_CELL_FIELDNAMES  # noqa: E402  # I32 P3
from akos.hlk_process_csv import (  # noqa: E402
    PROCESS_LIST_FIELDNAMES,
    normalize_process_row,
    read_process_csv,
    resolve_all_parent_ids,
)

PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "process_list.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
# I81 P2 T1 (D-IH-81-Q under D-IH-81-G umbrella, 2026-05-23): FINOPS_COUNTERPARTY_REGISTER
# moved to finops/ per Initiative 22 forward layout. Deprecation alias for one cycle.
_FINOPS_CSV_NEW = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "finops" / "FINOPS_COUNTERPARTY_REGISTER.csv"
_FINOPS_CSV_LEGACY = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "FINOPS_COUNTERPARTY_REGISTER.csv"
FINOPS_CSV = _FINOPS_CSV_NEW if _FINOPS_CSV_NEW.is_file() else _FINOPS_CSV_LEGACY
_GOIPOI_CSV_NEW = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "GOI_POI_REGISTER.csv"
_GOIPOI_CSV_LEGACY = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "GOI_POI_REGISTER.csv"
# I32 P7 (D-IH-32-D): GOI/POI relocated to dimensions/. Deprecation alias for one cycle.
GOIPOI_CSV = _GOIPOI_CSV_NEW if _GOIPOI_CSV_NEW.is_file() else _GOIPOI_CSV_LEGACY
# I81 P2 T2 (D-IH-81-R under D-IH-81-G umbrella, 2026-05-23): ADVISER_ENGAGEMENT_DISCIPLINES
# and ADVISER_OPEN_QUESTIONS moved to advops/ per Initiative 22 forward layout. Deprecation
# aliases for one initiative cycle (removal scheduled at I81 P9 closure).
_ADVISER_DISCIPLINES_NEW = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "advops" / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
_ADVISER_DISCIPLINES_LEGACY = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
ADVISER_DISCIPLINES_CSV = _ADVISER_DISCIPLINES_NEW if _ADVISER_DISCIPLINES_NEW.is_file() else _ADVISER_DISCIPLINES_LEGACY
_ADVISER_QUESTIONS_NEW = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "advops" / "ADVISER_OPEN_QUESTIONS.csv"
_ADVISER_QUESTIONS_LEGACY = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "ADVISER_OPEN_QUESTIONS.csv"
ADVISER_QUESTIONS_CSV = _ADVISER_QUESTIONS_NEW if _ADVISER_QUESTIONS_NEW.is_file() else _ADVISER_QUESTIONS_LEGACY
# I81 P2 T3 (D-IH-81-S under D-IH-81-G umbrella, 2026-05-23): moved + renamed to advops/FILED_INSTRUMENTS.csv.
_FILED_INSTRUMENTS_NEW = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "advops" / "FILED_INSTRUMENTS.csv"
_FILED_INSTRUMENTS_LEGACY = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "FOUNDER_FILED_INSTRUMENTS.csv"
FILED_INSTRUMENTS_CSV = _FILED_INSTRUMENTS_NEW if _FILED_INSTRUMENTS_NEW.is_file() else _FILED_INSTRUMENTS_LEGACY
PROGRAM_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PROGRAM_REGISTRY.csv"
TOPIC_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"
PERSONA_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PERSONA_REGISTRY.csv"
PERSONA_SCENARIO_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"
CHANNEL_TOUCHPOINT_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
SOURCING_REGISTER_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SOURCING_REGISTER.csv"
# I32 P2/P3/P4/P7: 4 new mirrors
SKILL_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SKILL_REGISTRY.csv"
TOUCHPOINT_KIT_CELL_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOUCHPOINT_KIT_CELL_REGISTRY.csv"
POLICY_REGISTER_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "POLICY_REGISTER.csv"
REPO_HEALTH_SNAPSHOT_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPO_HEALTH_SNAPSHOT.csv"
# I59 P1: 5 new HLK governance mirrors (planning workspace dimensions)
REPOSITORY_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
INITIATIVE_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "INITIATIVE_REGISTRY.csv"
OPS_REGISTER_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "OPS_REGISTER.csv"
CYCLE_REGISTER_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "CYCLE_REGISTER.csv"
DECISION_REGISTER_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
# I73 P1 — Engagement Model Registry (sibling dimension at People Operations per D-IH-73-C).
ENGAGEMENT_MODEL_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "People Operations" / "canonicals" / "dimensions" / "ENGAGEMENT_MODEL_REGISTRY.csv"
# I79 P2 — People Design Pattern Registry (cross-area design pattern library SSOT per D-IH-79-C/D).
DESIGN_PATTERN_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PEOPLE_DESIGN_PATTERN_REGISTRY.csv"
# I84 P3 — Substrate Registry (substrate doctrine SSOT per D-IH-84-A/F/G).
SUBSTRATE_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SUBSTRATE_REGISTRY.csv"
INTELLIGENCEOPS_REGISTER_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Research" / "Intelligence" / "canonicals" / "dimensions" / "INTELLIGENCEOPS_REGISTER.csv"
# I86 Wave L — 4-layer output architecture (Layer 1/2/3) per D-IH-86-BG.
OUTPUT_TYPE_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "OUTPUT_TYPE_REGISTRY.csv"
ARTIFACT_CLASS_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "ARTIFACT_CLASS_REGISTRY.csv"
COMPONENT_PRIMITIVE_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "COMPONENT_PRIMITIVE_REGISTRY.csv"
# I86 Wave R+1 P2c-a — 5 Collaborator Share CSVs (D-IH-86-DA/DB/DC/DD/DE). Paths are
# canonical SSOT in akos/hlk_collaborator_share.py; we just resolve them under REPO_ROOT.
COLLABORATOR_SHARE_REGISTRY_CSV = REPO_ROOT / CSV_PATH_RELATIVE_SHARE_REGISTRY
HOLISTIKA_VENDOR_SERVICES_BILLED_CSV = REPO_ROOT / CSV_PATH_RELATIVE_VENDOR_BILLED
PARTNER_OVERLAP_EXCLUSION_CLAUSES_CSV = REPO_ROOT / CSV_PATH_RELATIVE_OVERLAP_CLAUSES
COLLABORATOR_MARKET_RATE_REFERENCE_CSV = REPO_ROOT / CSV_PATH_RELATIVE_MARKET_RATE
COLLABORATOR_RATE_OVERRIDES_CSV = REPO_ROOT / CSV_PATH_RELATIVE_RATE_OVERRIDES
# I93 P6 — OPS-86-15 mirror gap (MIRROR-2)
_I93_DIM = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions"
AIC_REGISTRY_CSV = _I93_DIM / "AIC_REGISTRY.csv"
AUDIENCE_REGISTRY_CSV = _I93_DIM / "AUDIENCE_REGISTRY.csv"
CAPABILITY_REGISTRY_CSV = _I93_DIM / "CAPABILITY_REGISTRY.csv"
CAPABILITY_CONFIDENCE_REGISTRY_CSV = _I93_DIM / "CAPABILITY_CONFIDENCE_REGISTRY.csv"
COUNTRY_WORK_CALENDAR_CSV = _I93_DIM / "COUNTRY_WORK_CALENDAR.csv"
COUNTRY_WORK_CALENDAR_FIELDNAMES: tuple[str, ...] = (
    "country_code",
    "country_name",
    "legal_hours_per_day",
    "public_holidays_per_year_avg",
    "locale_uplift_pct",
    "notes",
)

# SSOT for the baseline_organisation column contract is akos.hlk_baseline_org_csv.
# This local alias preserves the existing in-module name without re-declaring the
# tuple body (release-gate hygiene 2026-05-11: closes a 3-column drift between
# the prior 12-column hardcode and the 15-column CSV header that has carried the
# role_hourly_*_eur rate trio since at least the I12 P12 commit 8296512).
# Per akos-governance-remediation.mdc DI principle: extend SSOT instead of
# duplicating; the canonical fieldnames live in akos/, scripts import.
BASELINE_FIELDNAMES = BASELINE_ORGANISATION_FIELDNAMES


def _git_head_sha() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except OSError:
        pass
    return "unknown"


def _sql_text_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _sql_column_value(
    column: str,
    raw: str,
    *,
    date_columns: frozenset[str] = frozenset(),
    numeric_columns: frozenset[str] = frozenset(),
) -> str:
    """Emit SQL for a mirror column; empty DATE/NUMERIC fields become NULL (I57 P1 pattern)."""
    if column in date_columns and not raw:
        return "NULL"
    if column in date_columns:
        return f"DATE {_sql_text_literal(raw)}"
    if column in numeric_columns and not raw:
        return "NULL"
    if column in numeric_columns:
        return raw
    return _sql_text_literal(raw)


def _sql_bool_or_null(raw: str) -> str:
    """Emit TRUE/FALSE for non-empty bool strings; NULL when CSV cell is empty."""
    if not raw:
        return "NULL"
    return "TRUE" if raw.lower() == "true" else "FALSE"


_DECISION_REGISTER_DATE_COLUMNS = frozenset({"decided_at", "last_review_at"})
_PROCESS_LIST_DATE_COLUMNS = frozenset({"last_review_at"})
_PROCESS_LIST_NUMERIC_COLUMNS = frozenset(
    {"min_rev_value_eur", "par_rev_value_eur", "max_rev_value_eur"}
)
_INITIATIVE_REGISTRY_DATE_COLUMNS = frozenset(
    {"inception_date", "last_review", "closed_at", "archived_at", "last_review_at"}
)
_OPS_REGISTER_DATE_COLUMNS = frozenset({"opened_at", "closed_at", "last_review_at"})
_OPS_REGISTER_NUMERIC_COLUMNS = frozenset(
    {
        "rice_reach",
        "rice_impact",
        "rice_confidence_pct",
        "rice_effort_person_weeks",
        "rice_score",
    }
)
_INTELLIGENCEOPS_REGISTER_DATE_COLUMNS = frozenset({"last_review_at", "next_verify_by"})
_INTELLIGENCEOPS_REGISTER_NUMERIC_COLUMNS = frozenset({"staleness_days"})
_CYCLE_REGISTER_DATE_COLUMNS = frozenset({"started_at", "closed_at"})
_BASELINE_ORG_DATE_COLUMNS = frozenset({"last_review_at"})
_REPO_HEALTH_DATE_COLUMNS = frozenset({"snapshot_date", "last_review_at"})
_REPO_HEALTH_BOOL_COLUMNS = frozenset({
    "has_external_repo_contract",
    "has_akos_mirror_rule",
    "embedded_obsidian_snapshot_present",
    "ci_workflow_present",
    "dependabot_present",
    "codeowners_present",
    "license_present",
    "akos_mirror_sha256_match",
})
_REPO_HEALTH_INT_COLUMNS = frozenset({
    "cursor_rule_count",
    "brand_jargon_violations",
    "secret_rotation_oldest_age_days",
})
_REPOSITORY_REGISTRY_DATE_COLUMNS = frozenset({
    "last_review_at",
    "created_at",
    "pushed_at",
    "last_inventory_at",
})
_REPOSITORY_REGISTRY_BOOL_COLUMNS = frozenset({
    "codeowners_present",
    "branch_protection_enabled",
})
_REPOSITORY_REGISTRY_NULLABLE_ENUM_COLUMNS = frozenset({
    "app_class",
    "github_visibility",
    "governance_status",
})


def _emit_process_list_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(PROCESS_LIST_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in PROCESS_LIST_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.process_list_mirror upserts (one row per statement)")
    for r in rows:
        nr = normalize_process_row(r)
        vals = ", ".join(
            _sql_column_value(
                k,
                (nr.get(k) or "").strip(),
                date_columns=_PROCESS_LIST_DATE_COLUMNS,
                numeric_columns=_PROCESS_LIST_NUMERIC_COLUMNS,
            )
            for k in PROCESS_LIST_FIELDNAMES
        )
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        iid = nr["item_id"].strip()
        if not iid:
            continue
        out.append(
            f"INSERT INTO compliance.process_list_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (item_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_baseline_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(BASELINE_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in BASELINE_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.baseline_organisation_mirror upserts")
    for r in rows:
        vals = ", ".join(
            _sql_column_value(
                c,
                (r.get(c) or "").strip(),
                date_columns=_BASELINE_ORG_DATE_COLUMNS,
            )
            for c in BASELINE_FIELDNAMES
        )
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        oid = (r.get("org_uuid") or "").strip()
        if not oid:
            continue
        out.append(
            f"INSERT INTO compliance.baseline_organisation_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (org_uuid) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_finops_counterparty_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.finops_counterparty_register_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        cid = (r.get("counterparty_id") or "").strip()
        if not cid:
            continue
        out.append(
            f"INSERT INTO compliance.finops_counterparty_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (counterparty_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_goipoi_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(GOIPOI_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in GOIPOI_REGISTER_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.goipoi_register_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in GOIPOI_REGISTER_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        ref = (r.get("ref_id") or "").strip()
        if not ref:
            continue
        out.append(
            f"INSERT INTO compliance.goipoi_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (ref_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_adviser_disciplines_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.adviser_engagement_disciplines_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        did = (r.get("discipline_id") or "").strip()
        if not did:
            continue
        out.append(
            f"INSERT INTO compliance.adviser_engagement_disciplines_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (discipline_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_adviser_questions_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(ADVISER_OPEN_QUESTIONS_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in ADVISER_OPEN_QUESTIONS_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.adviser_open_questions_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in ADVISER_OPEN_QUESTIONS_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        qid = (r.get("question_id") or "").strip()
        if not qid:
            continue
        out.append(
            f"INSERT INTO compliance.adviser_open_questions_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (question_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_founder_filed_instruments_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    # I81 P2 T3 (D-IH-81-S, 2026-05-23): table renamed to compliance.filed_instruments_mirror.
    # Function name retained for one initiative cycle (call-site stability); removal at I81 P9 closure.
    cols_csv = ", ".join(FILED_INSTRUMENTS_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in FILED_INSTRUMENTS_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.filed_instruments_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in FILED_INSTRUMENTS_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        iid = (r.get("instrument_id") or "").strip()
        if not iid:
            continue
        out.append(
            f"INSERT INTO compliance.filed_instruments_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (instrument_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_topic_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 25 P2 mirror upsert emitter for compliance.topic_registry_mirror."""
    cols_csv = ", ".join(TOPIC_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in TOPIC_REGISTRY_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.topic_registry_mirror upserts (Initiative 25)")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in TOPIC_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        tid = (r.get("topic_id") or "").strip()
        if not tid:
            continue
        out.append(
            f"INSERT INTO compliance.topic_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (topic_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_persona_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 31 P2.1 mirror upsert emitter for compliance.persona_registry_mirror."""
    cols_csv = ", ".join(PERSONA_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in PERSONA_REGISTRY_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.persona_registry_mirror upserts (Initiative 31)")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in PERSONA_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        pid = (r.get("persona_id") or "").strip()
        if not pid:
            continue
        out.append(
            f"INSERT INTO compliance.persona_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (persona_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_persona_scenario_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 51 P1 (closes OPS-47-9) — compliance.persona_scenario_registry_mirror upserts.

    Mirror DDL was created at I47 P1 (`20260502033000_i47_persona_scenario_registry_mirror.sql`)
    and extended at I49 with `priority_score` / `safety_lane` / `release_blocking`
    columns (`20260503120000_i49_persona_scenario_registry_priority_columns.sql`),
    but the CSV-to-mirror reseeder was never wired up. This emitter closes that
    carrier. Same shape as `_emit_persona_registry_upserts`: DAMA-pure projection
    of CSV; semicolon-list columns (`expected_keywords`, `forbidden_keywords`,
    `topic_ids`) stored verbatim as TEXT.

    `tenant_id` is emitted as `NULL` when blank to honor the D-IH-47-K shared-
    scenario default (the DDL allows NULL but PostgreSQL would reject the empty
    string for a TEXT column with a DEFAULT NULL only on INSERT-without-column;
    explicit '' is a valid TEXT value but breaks the "NULL = shared" semantics).
    All other columns retain the existing _sql_text_literal handling.
    """
    cols_csv = ", ".join(PERSONA_SCENARIO_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in PERSONA_SCENARIO_REGISTRY_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.persona_scenario_registry_mirror upserts (I47 P1 + I49; closes OPS-47-9 in I51 P1)"]
    nullable_when_blank = {"tenant_id"}  # D-IH-47-K shared-scenario semantics
    for r in rows:
        sid = (r.get("scenario_id") or "").strip()
        if not sid:
            continue
        row_vals: list[str] = []
        for c in PERSONA_SCENARIO_REGISTRY_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c in nullable_when_blank and not raw:
                row_vals.append("NULL")
            else:
                row_vals.append(_sql_text_literal(raw))
        vals_full = ", ".join(row_vals) + f", {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.persona_scenario_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (scenario_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_channel_touchpoint_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 31 P3 mirror upsert emitter for compliance.channel_touchpoint_registry_mirror."""
    cols_csv = ", ".join(CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.channel_touchpoint_registry_mirror upserts (Initiative 31)")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        cid = (r.get("channel_id") or "").strip()
        if not cid:
            continue
        out.append(
            f"INSERT INTO compliance.channel_touchpoint_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (channel_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_sourcing_register_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 31 P5.2 mirror upsert emitter for compliance.sourcing_register_mirror.

    I57 P1 (closes I22a F-22a-EMIT-1): empty CSV cells for DATE columns are
    emitted as ``NULL`` instead of ``''``. PostgreSQL rejects the empty-string
    literal for DATE/TIMESTAMP types (22007 invalid_datetime_format); the
    ``last_engagement_date`` column is the canonical occurrence and was the
    real-world cell that broke during the 2026-05-04 mirror reseed (see
    ``docs/wip/planning/22a-i22-post-closure-followups/master-roadmap.md``
    Open follow-ups). Same idiom as ``_emit_persona_scenario_registry_upserts``
    ``nullable_when_blank``. If more DATE/TIMESTAMP columns are added to
    SOURCING_REGISTER in future initiatives, extend ``DATE_COLUMNS``.
    """
    cols_csv = ", ".join(SOURCING_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in SOURCING_REGISTER_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    DATE_COLUMNS = {"last_engagement_date"}  # I57 P1 — F-22a-EMIT-1 fix
    out: list[str] = []
    out.append("-- compliance.sourcing_register_mirror upserts (Initiative 31 + I57 P1 DATE-NULL fix)")
    for r in rows:
        vid = (r.get("vendor_id") or "").strip()
        if not vid:
            continue
        row_vals: list[str] = []
        for c in SOURCING_REGISTER_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c in DATE_COLUMNS and not raw:
                row_vals.append("NULL")
            else:
                row_vals.append(_sql_text_literal(raw))
        vals_full = ", ".join(row_vals) + f", {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.sourcing_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (vendor_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_program_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 23 P2 mirror upsert emitter for compliance.program_registry_mirror.

    Same shape as the other Wave-2 mirrors (DAMA-pure projection of CSV; semicolon-list
    columns stored verbatim as TEXT; Neo4j projection extends from CSV separately).
    """
    cols_csv = ", ".join(PROGRAM_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in PROGRAM_REGISTRY_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.program_registry_mirror upserts (Initiative 23)")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in PROGRAM_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        pid = (r.get("program_id") or "").strip()
        if not pid:
            continue
        out.append(
            f"INSERT INTO compliance.program_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (program_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_skill_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 32 P2 — compliance.skill_registry_mirror upserts.

    I47 P13 item 2 (D-IH-47-G): boolean column emit fix per the I46 P7 lesson.
    Boolean columns receive 'true' / 'false' keywords (not the empty string '').

    I57 P1 (closes I22a F-22a-EMIT-2): the empty-or-unknown branch for known
    NOT-NULL bool columns now emits the documented column default instead of
    ``NULL``. ``tools_required_waived`` defaults to ``false`` (the
    SKILL_REGISTRY contract documented in this function: blank = "not waived").
    Emitting ``NULL`` for a NOT-NULL column was rejected at apply time during
    the 2026-05-04 mirror reseed (see ``docs/wip/planning/22a-i22-post-closure-followups/master-roadmap.md``
    Open follow-ups). For NOT-NULL bool columns added to SKILL_REGISTRY in
    future initiatives, extend ``BOOL_COLUMN_DEFAULTS`` with the documented
    blank-cell default. Adding the column to ``BOOL_COLUMN_DEFAULTS`` without
    a default value (i.e. mapping to ``None``) routes through the explicit
    fail-loud branch so the defect surfaces at emit time, not at apply time.
    """
    cols_csv = ", ".join(SKILL_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in SKILL_REGISTRY_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    # I57 P1 — F-22a-EMIT-2 fix. Map column -> documented blank-cell default
    # (string literal that the emitter writes as-is into the SQL VALUES list).
    # ``None`` value means "no documented default; fail loudly if encountered".
    BOOL_COLUMN_DEFAULTS: dict[str, str | None] = {
        "tools_required_waived": "false",  # SKILL_REGISTRY contract: blank = not waived
    }
    out: list[str] = ["-- compliance.skill_registry_mirror upserts (Initiative 32 P2 + I47 P13 + I57 P1 NOT-NULL-bool default fix)"]
    for r in rows:
        sid = (r.get("skill_id") or "").strip()
        if not sid:
            continue
        row_vals: list[str] = []
        for c in SKILL_REGISTRY_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c in BOOL_COLUMN_DEFAULTS:
                low = raw.lower()
                if low in ("true", "1", "yes", "y"):
                    row_vals.append("true")
                elif low in ("false", "0", "no", "n"):
                    row_vals.append("false")
                else:  # empty / unknown
                    default = BOOL_COLUMN_DEFAULTS[c]
                    if default is None:
                        raise ValueError(
                            f"SKILL_REGISTRY row {sid!r} column {c!r} is empty/unknown and no "
                            f"documented blank-cell default exists. Either fill the CSV cell "
                            f"with 'true'/'false' or extend BOOL_COLUMN_DEFAULTS in "
                            f"_emit_skill_registry_upserts with the column's documented default."
                        )
                    row_vals.append(default)
            else:
                row_vals.append(_sql_text_literal(raw))
        vals_full = ", ".join(row_vals) + f", {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.skill_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (skill_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_touchpoint_kit_cell_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 32 P3 — compliance.touchpoint_kit_cell_mirror upserts."""
    cols_csv = ", ".join(TOUCHPOINT_KIT_CELL_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in TOUCHPOINT_KIT_CELL_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.touchpoint_kit_cell_mirror upserts (Initiative 32 P3)"]
    for r in rows:
        cid = (r.get("cell_id") or "").strip()
        if not cid:
            continue
        # last_review is DATE in DDL; pass NULL when empty so PG doesn't reject ''
        row_vals: list[str] = []
        for c in TOUCHPOINT_KIT_CELL_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c == "last_review" and not raw:
                row_vals.append("NULL")
            elif c == "last_review" and raw:
                row_vals.append(f"DATE {_sql_text_literal(raw)}")
            else:
                row_vals.append(_sql_text_literal(raw))
        vals_full = ", ".join(row_vals) + f", {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.touchpoint_kit_cell_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (cell_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_policy_register_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 32 P4 — compliance.policy_register_mirror upserts."""
    cols_csv = ", ".join(POLICY_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in POLICY_REGISTER_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.policy_register_mirror upserts (Initiative 32 P4)"]
    date_columns = {"last_review", "next_review"}
    for r in rows:
        pid = (r.get("policy_id") or "").strip()
        if not pid:
            continue
        row_vals: list[str] = []
        for c in POLICY_REGISTER_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c in date_columns and not raw:
                row_vals.append("NULL")
            elif c in date_columns and raw:
                row_vals.append(f"DATE {_sql_text_literal(raw)}")
            else:
                row_vals.append(_sql_text_literal(raw))
        vals_full = ", ".join(row_vals) + f", {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.policy_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (policy_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_repo_health_snapshot_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 32 P7 — compliance.repo_health_snapshot_mirror upserts.

    Append-only history; PK is (repo_slug, snapshot_date). UPDATE on conflict refreshes
    the metrics (operator may rerun the snapshot script same-day; CSV always
    reflects latest weekly snapshot).
    """
    cols_csv = ", ".join(REPO_HEALTH_SNAPSHOT_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in REPO_HEALTH_SNAPSHOT_FIELDNAMES if c not in ("repo_slug", "snapshot_date")]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.repo_health_snapshot_mirror upserts (Initiative 32 P7)"]
    for r in rows:
        slug = (r.get("repo_slug") or "").strip()
        sd = (r.get("snapshot_date") or "").strip()
        if not slug or not sd:
            continue
        row_vals: list[str] = []
        for c in REPO_HEALTH_SNAPSHOT_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c in _REPO_HEALTH_DATE_COLUMNS:
                row_vals.append(
                    _sql_column_value(c, raw, date_columns=_REPO_HEALTH_DATE_COLUMNS)
                )
            elif c in _REPO_HEALTH_BOOL_COLUMNS:
                row_vals.append(_sql_bool_or_null(raw))
            elif c == "language_frontmatter_compliance_pct":
                row_vals.append(raw if raw else "0.0")
            elif c in _REPO_HEALTH_INT_COLUMNS:
                if c == "secret_rotation_oldest_age_days":
                    row_vals.append(raw if raw else "NULL")
                else:
                    row_vals.append(raw if raw else "0")
            else:
                row_vals.append(_sql_text_literal(raw))
        vals_full = ", ".join(row_vals) + f", {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.repo_health_snapshot_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (repo_slug, snapshot_date) DO UPDATE SET {update_sets};"
        )
    return out


# ---- I59 P1 — five HLK governance dimensions ---------------------------------


def _emit_repository_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I59 P1.1 — compliance.repository_registry_mirror upserts.

    PK = repo_slug. CSV is canonical (machine-readable); REPOSITORIES_REGISTRY.md is
    canonical for prose. Sync validator enforces slug-set consistency between the two.
    """
    cols_csv = ", ".join(REPOSITORY_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in REPOSITORY_REGISTRY_FIELDNAMES if c != "repo_slug"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.repository_registry_mirror upserts (Initiative 59 P1.1)"]
    for r in rows:
        slug = (r.get("repo_slug") or "").strip()
        if not slug:
            continue
        row_vals: list[str] = []
        for c in REPOSITORY_REGISTRY_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c in _REPOSITORY_REGISTRY_DATE_COLUMNS:
                row_vals.append(
                    _sql_column_value(c, raw, date_columns=_REPOSITORY_REGISTRY_DATE_COLUMNS)
                )
            elif c in _REPOSITORY_REGISTRY_BOOL_COLUMNS:
                row_vals.append(_sql_bool_or_null(raw))
            elif c in _REPOSITORY_REGISTRY_NULLABLE_ENUM_COLUMNS and not raw:
                row_vals.append("NULL")
            else:
                row_vals.append(_sql_text_literal(raw))
        vals = ", ".join(row_vals)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.repository_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (repo_slug) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_initiative_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I59 P1.2 — compliance.initiative_registry_mirror upserts.

    PK = initiative_id (e.g. ``i59_hlk_governance``). CSV is canonical for metadata
    (status, last_review, ...); master-roadmap.md frontmatter is canonical for prose.
    Sync validator enforces frontmatter ↔ CSV agreement on (status, last_review).
    """
    cols_csv = ", ".join(INITIATIVE_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in INITIATIVE_REGISTRY_FIELDNAMES if c != "initiative_id"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.initiative_registry_mirror upserts (Initiative 59 P1.2)"]
    for r in rows:
        iid = (r.get("initiative_id") or "").strip()
        if not iid:
            continue
        vals = ", ".join(
            _sql_column_value(
                c, (r.get(c) or "").strip(), date_columns=_INITIATIVE_REGISTRY_DATE_COLUMNS
            )
            for c in INITIATIVE_REGISTRY_FIELDNAMES
        )
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.initiative_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (initiative_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_ops_register_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I59 P1.3 — compliance.ops_register_mirror upserts.

    PK = ops_action_id (e.g. ``OPS-58-1``). Operator/mixed-owned rows feed
    docs/wip/planning/OPERATOR_INBOX.md (auto-rendered).
    """
    cols_csv = ", ".join(OPS_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in OPS_REGISTER_FIELDNAMES if c != "ops_action_id"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.ops_register_mirror upserts (Initiative 59 P1.3)"]
    for r in rows:
        oid = (r.get("ops_action_id") or "").strip()
        if not oid:
            continue
        vals = ", ".join(
            _sql_column_value(
                c,
                (r.get(c) or "").strip(),
                date_columns=_OPS_REGISTER_DATE_COLUMNS,
                numeric_columns=_OPS_REGISTER_NUMERIC_COLUMNS,
            )
            for c in OPS_REGISTER_FIELDNAMES
        )
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.ops_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (ops_action_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_cycle_register_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I59 P1.4 — compliance.cycle_register_mirror upserts.

    PK = cycle_id (e.g. ``cycle_2_multi_track_forward``). One row per coordinating
    cycle; coordinated_initiative_ids is a comma-separated FK list.
    """
    cols_csv = ", ".join(CYCLE_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in CYCLE_REGISTER_FIELDNAMES if c != "cycle_id"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.cycle_register_mirror upserts (Initiative 59 P1.4)"]
    for r in rows:
        cid = (r.get("cycle_id") or "").strip()
        if not cid:
            continue
        vals = ", ".join(
            _sql_column_value(c, (r.get(c) or "").strip(), date_columns=_CYCLE_REGISTER_DATE_COLUMNS)
            for c in CYCLE_REGISTER_FIELDNAMES
        )
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.cycle_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (cycle_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_engagement_model_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I73 P1 — compliance.engagement_model_registry_mirror upserts.

    PK = engagement_model_id (e.g. ``eng_model_hourly_consultant``). Sibling
    dimension to the engagement_registry_mirror per D-IH-73-C. ``access_level_default``
    is SMALLINT (CHECK 0..6); emitted as a bare integer literal (not text-quoted)
    when present, NULL when blank. All other columns are TEXT with verbatim
    quoting.
    """
    cols_csv = ", ".join(ENGAGEMENT_MODEL_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in ENGAGEMENT_MODEL_FIELDNAMES if c != "engagement_model_id"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.engagement_model_registry_mirror upserts (Initiative 73 P1)"]
    for r in rows:
        eid = (r.get("engagement_model_id") or "").strip()
        if not eid:
            continue
        row_vals: list[str] = []
        for c in ENGAGEMENT_MODEL_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c == "access_level_default":
                # SMALLINT column; emit bare int literal or NULL.
                if not raw:
                    row_vals.append("NULL")
                else:
                    row_vals.append(raw)  # int literal; CHECK constraint validates 0..6
            else:
                row_vals.append(_sql_text_literal(raw))
        vals_full = ", ".join(row_vals) + f", {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.engagement_model_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (engagement_model_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_design_pattern_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I79 P2 - compliance.people_design_pattern_registry_mirror upserts.

    PK = pattern_id (e.g. ``pattern_register_csv_pydantic_validator_mirror``). All
    columns are TEXT except ``last_review`` which is DATE in the mirror. The
    DATE column is emitted as a quoted ISO literal (PostgreSQL coerces to date).
    Per D-IH-79-C/D pattern library shape; D-IH-79-N anti-jargon drift gate
    pairing covers the canonical CSV.
    """
    cols_csv = ", ".join(DESIGN_PATTERN_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in DESIGN_PATTERN_FIELDNAMES if c != "pattern_id"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.people_design_pattern_registry_mirror upserts (Initiative 79 P2)"]
    for r in rows:
        pid = (r.get("pattern_id") or "").strip()
        if not pid:
            continue
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in DESIGN_PATTERN_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.people_design_pattern_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (pattern_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_substrate_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I84 P3 - compliance.substrate_registry_mirror upserts.

    PK = substrate_id (matches ``^SUBS-[A-Z0-9-]+$``; e.g. ``SUBS-HOLISTIKA-OPENCLAW``).
    All columns are TEXT except ``last_audit_date`` which is DATE in the mirror;
    DATE column is emitted as a quoted ISO literal (PostgreSQL coerces date).
    Per D-IH-84-A/F/G substrate doctrine.
    """
    cols_csv = ", ".join(SUBSTRATE_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in SUBSTRATE_REGISTRY_FIELDNAMES if c != "substrate_id"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.substrate_registry_mirror upserts (Initiative 84 P3)"]
    for r in rows:
        sid = (r.get("substrate_id") or "").strip()
        if not sid:
            continue
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in SUBSTRATE_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.substrate_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (substrate_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_intelligenceops_register_upserts(rows: list[dict[str, str]], _source_git_sha: str) -> list[str]:
    """I72 P6 + I75 (D-IH-86-FH) - compliance.intelligenceops_register_mirror upserts.

    PK = ``register_id``. DATE columns (``last_review_at``, ``next_verify_by``) +
    INTEGER column (``staleness_days``) emit as NULL when the CSV cell is empty
    (per the I57 P1 ``_sql_column_value`` pattern); non-empty DATE cells emit as
    ``DATE 'YYYY-MM-DD'`` literals so PostgreSQL never coerces an empty string.

    Unlike the I59 + I86-Wave-L mirror fleet, this mirror table carries NO
    ``source_git_sha`` / ``synced_at`` audit columns (see the I72 P6 DDL at
    ``supabase/migrations/20260514240000_i72_intelligenceops_register_mirror.sql``),
    so they are NOT appended. The ``_source_git_sha`` arg is accepted only for
    dispatch-signature parity with the other emitters and is intentionally unused.
    """
    cols_full = ", ".join(INTELLIGENCEOPS_REGISTER_FIELDNAMES)
    update_sets = ", ".join(
        f"{c} = EXCLUDED.{c}"
        for c in INTELLIGENCEOPS_REGISTER_FIELDNAMES
        if c != "register_id"
    )
    out: list[str] = ["-- compliance.intelligenceops_register_mirror upserts (I72 P6 + I75 D-IH-86-FH)"]
    for r in rows:
        rid = (r.get("register_id") or "").strip()
        if not rid:
            continue
        vals = ", ".join(
            _sql_column_value(
                c,
                (r.get(c) or "").strip(),
                date_columns=_INTELLIGENCEOPS_REGISTER_DATE_COLUMNS,
                numeric_columns=_INTELLIGENCEOPS_REGISTER_NUMERIC_COLUMNS,
            )
            for c in INTELLIGENCEOPS_REGISTER_FIELDNAMES
        )
        out.append(
            f"INSERT INTO compliance.intelligenceops_register_mirror ({cols_full}) VALUES ({vals}) "
            f"ON CONFLICT (register_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_output_type_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I86 Wave L (D-IH-86-BG) - compliance.output_type_registry_mirror upserts.

    PK = output_type_code (matches ``^OT-[A-Z0-9][A-Z0-9-]+$``; e.g. ``OT-PROSE-MARKDOWN``).
    All columns are TEXT except ``added_at`` and ``last_review_at`` which are DATE in
    the mirror; DATE columns are emitted as quoted ISO literals (PostgreSQL coerces).
    """
    cols_csv = ", ".join(OUTPUT_TYPE_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in OUTPUT_TYPE_REGISTRY_FIELDNAMES if c != "output_type_code"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.output_type_registry_mirror upserts (I86 Wave L)"]
    for r in rows:
        code = (r.get("output_type_code") or "").strip()
        if not code:
            continue
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in OUTPUT_TYPE_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.output_type_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (output_type_code) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_artifact_class_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I86 Wave L (D-IH-86-BG) - compliance.artifact_class_registry_mirror upserts.

    PK = artifact_class_code (matches ``^AC-[A-Z0-9][A-Z0-9-]+$``; e.g. ``AC-DOSSIER``).
    """
    cols_csv = ", ".join(ARTIFACT_CLASS_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in ARTIFACT_CLASS_REGISTRY_FIELDNAMES if c != "artifact_class_code"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.artifact_class_registry_mirror upserts (I86 Wave L)"]
    for r in rows:
        code = (r.get("artifact_class_code") or "").strip()
        if not code:
            continue
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in ARTIFACT_CLASS_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.artifact_class_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (artifact_class_code) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_component_primitive_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I86 Wave L (D-IH-86-BG) - compliance.component_primitive_registry_mirror upserts.

    PK = component_primitive_code (matches ``^CP-[A-Z0-9][A-Z0-9-]+$``; e.g. ``CP-CTA``).
    """
    cols_csv = ", ".join(COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES if c != "component_primitive_code"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.component_primitive_registry_mirror upserts (I86 Wave L)"]
    for r in rows:
        code = (r.get("component_primitive_code") or "").strip()
        if not code:
            continue
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.component_primitive_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (component_primitive_code) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_generic_pk_upserts(
    *,
    rows: list[dict[str, str]],
    fieldnames: tuple[str, ...],
    mirror_table: str,
    pk_column: str,
    source_git_sha: str,
    initiative_label: str,
) -> list[str]:
    """Generic single-PK UPSERT emitter used by I86 Wave R+1 collaborator-share mirrors.

    Mirrors the shape of the I59 + I86 Wave L per-mirror emit functions but factored
    so the 5 collaborator-share mirrors (sharing the same single-PK pattern) reuse
    one body. Skips rows where the PK column is empty.
    """
    cols_csv = ", ".join(fieldnames)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in fieldnames if c != pk_column]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = [f"-- {mirror_table} upserts ({initiative_label})"]
    for r in rows:
        pk = (r.get(pk_column) or "").strip()
        if not pk:
            continue
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in fieldnames)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO {mirror_table} ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT ({pk_column}) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_aic_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    return _emit_generic_pk_upserts(
        rows=rows,
        fieldnames=AIC_REGISTRY_FIELDNAMES,
        mirror_table="compliance.aic_registry_mirror",
        pk_column="aic_id",
        source_git_sha=source_git_sha,
        initiative_label="I93 P6 OPS-86-15",
    )


def _emit_audience_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    return _emit_generic_pk_upserts(
        rows=rows,
        fieldnames=AUDIENCE_REGISTRY_FIELDNAMES,
        mirror_table="compliance.audience_registry_mirror",
        pk_column="audience_code",
        source_git_sha=source_git_sha,
        initiative_label="I93 P6 OPS-86-15",
    )


def _emit_capability_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    return _emit_generic_pk_upserts(
        rows=rows,
        fieldnames=CAPABILITY_REGISTRY_FIELDNAMES,
        mirror_table="compliance.capability_registry_mirror",
        pk_column="capability_id",
        source_git_sha=source_git_sha,
        initiative_label="I93 P6 OPS-86-15",
    )


def _emit_capability_confidence_registry_upserts(
    rows: list[dict[str, str]], source_git_sha: str
) -> list[str]:
    return _emit_generic_pk_upserts(
        rows=rows,
        fieldnames=CAPABILITY_CONFIDENCE_FIELDNAMES,
        mirror_table="compliance.capability_confidence_registry_mirror",
        pk_column="confidence_id",
        source_git_sha=source_git_sha,
        initiative_label="I93 P6 OPS-86-15",
    )


def _emit_country_work_calendar_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    return _emit_generic_pk_upserts(
        rows=rows,
        fieldnames=COUNTRY_WORK_CALENDAR_FIELDNAMES,
        mirror_table="compliance.country_work_calendar_mirror",
        pk_column="country_code",
        source_git_sha=source_git_sha,
        initiative_label="I93 P6 OPS-86-15",
    )


# I86 Wave R+1 P2c-a — 5 Collaborator Share mirrors. Dispatched together via a
# single --collaborator-share-only flag because the doctrine treats them as ONE
# atomic kit (per akos-collaborator-share.mdc RULE 2 + the COLLABORATOR_SHARE
# doctrine §2). Order matters: reference rows (clauses + market rates) emit
# before engagement-scoped rows (share_registry + rate_overrides + vendor_billed)
# so any FK references resolve cleanly when applied in sequence.
COLLABORATOR_SHARE_MIRROR_SPECS: tuple[tuple[str, Path, tuple[str, ...], str], ...] = (
    (
        "compliance.partner_overlap_exclusion_clauses_mirror",
        PARTNER_OVERLAP_EXCLUSION_CLAUSES_CSV,
        PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES,
        "clause_id",
    ),
    (
        "compliance.collaborator_market_rate_reference_mirror",
        COLLABORATOR_MARKET_RATE_REFERENCE_CSV,
        COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES,
        "rate_id",
    ),
    (
        "compliance.collaborator_share_registry_mirror",
        COLLABORATOR_SHARE_REGISTRY_CSV,
        COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
        "share_id",
    ),
    (
        "compliance.collaborator_rate_overrides_mirror",
        COLLABORATOR_RATE_OVERRIDES_CSV,
        COLLABORATOR_RATE_OVERRIDES_FIELDNAMES,
        "override_id",
    ),
    (
        "compliance.holistika_vendor_services_billed_mirror",
        HOLISTIKA_VENDOR_SERVICES_BILLED_CSV,
        HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
        "vendor_billing_id",
    ),
)


def _emit_decision_register_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """I59 P1.5 — compliance.decision_register_mirror upserts.

    PK = decision_id (e.g. ``D-IH-58-I``). Markdown decision-log files remain prose
    canonical; CSV is metadata canonical (status, reversibility, FK linkages).
    """
    cols_csv = ", ".join(DECISION_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in DECISION_REGISTER_FIELDNAMES if c != "decision_id"]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = ["-- compliance.decision_register_mirror upserts (Initiative 59 P1.5)"]
    for r in rows:
        did = (r.get("decision_id") or "").strip()
        if not did:
            continue
        vals = ", ".join(
            _sql_column_value(c, (r.get(c) or "").strip(), date_columns=_DECISION_REGISTER_DATE_COLUMNS)
            for c in DECISION_REGISTER_FIELDNAMES
        )
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        out.append(
            f"INSERT INTO compliance.decision_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (decision_id) DO UPDATE SET {update_sets};"
        )
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--git-sha",
        type=str,
        default=None,
        help="Provenance SHA (default: git rev-parse HEAD, or 'unknown')",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Write SQL to this file (default: stdout; with --ops8615-gap-mirrors-only "
            f"defaults to {I93_P6_OPS8615_UPSERT_ARTIFACT})"
        ),
    )
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="Print row counts only; no SQL",
    )
    parser.add_argument(
        "--process-list-only",
        action="store_true",
        help="Only emit process_list_mirror statements",
    )
    parser.add_argument(
        "--baseline-only",
        action="store_true",
        help="Only emit baseline_organisation_mirror statements",
    )
    parser.add_argument(
        "--finops-counterparty-register-only",
        action="store_true",
        help="Only emit finops_counterparty_register_mirror statements (requires FINOPS_COUNTERPARTY_REGISTER.csv)",
    )
    parser.add_argument(
        "--goipoi-register-only",
        action="store_true",
        help="Only emit goipoi_register_mirror statements (requires GOI_POI_REGISTER.csv)",
    )
    parser.add_argument(
        "--adviser-disciplines-only",
        action="store_true",
        help="Only emit adviser_engagement_disciplines_mirror statements (requires ADVISER_ENGAGEMENT_DISCIPLINES.csv)",
    )
    parser.add_argument(
        "--adviser-questions-only",
        action="store_true",
        help="Only emit adviser_open_questions_mirror statements (requires ADVISER_OPEN_QUESTIONS.csv)",
    )
    parser.add_argument(
        "--founder-filed-instruments-only",
        action="store_true",
        # I81 P2 T3 (D-IH-81-S, 2026-05-23): table renamed to compliance.filed_instruments_mirror; flag name retained for one initiative cycle.
        help="Only emit filed_instruments_mirror statements (requires advops/FILED_INSTRUMENTS.csv or legacy FOUNDER_FILED_INSTRUMENTS.csv)",
    )
    parser.add_argument(
        "--program-registry-only",
        action="store_true",
        help="Only emit program_registry_mirror statements (requires dimensions/PROGRAM_REGISTRY.csv) [Initiative 23]",
    )
    parser.add_argument(
        "--topic-registry-only",
        action="store_true",
        help="Only emit topic_registry_mirror statements (requires dimensions/TOPIC_REGISTRY.csv) [Initiative 25]",
    )
    parser.add_argument(
        "--persona-registry-only",
        action="store_true",
        help="Only emit persona_registry_mirror statements (requires dimensions/PERSONA_REGISTRY.csv) [Initiative 31]",
    )
    parser.add_argument(
        "--persona-scenario-registry-only",
        action="store_true",
        help="Only emit persona_scenario_registry_mirror statements (requires dimensions/PERSONA_SCENARIO_REGISTRY.csv) [Initiative 47 P1 + I49; closes OPS-47-9 in I51 P1]",
    )
    parser.add_argument(
        "--ops8615-gap-mirrors-only",
        action="store_true",
        help="Emit all five OPS-86-15 gap mirrors (AIC AUDIENCE CAPABILITY CAPABILITY_CONFIDENCE COUNTRY_WORK_CALENDAR) [I93 P6]",
    )
    parser.add_argument(
        "--ops8615-split",
        action="store_true",
        help=(
            "With --ops8615-gap-mirrors-only, write one BEGIN/COMMIT-wrapped .sql per mirror table "
            "(under artifacts/ops8615-batches/ or next to --output). Use for Supabase SQL Editor limits; "
            "large capability tables still need psql."
        ),
    )
    parser.add_argument(
        "--channel-touchpoint-registry-only",
        action="store_true",
        help="Only emit channel_touchpoint_registry_mirror statements (requires dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv) [Initiative 31]",
    )
    parser.add_argument(
        "--sourcing-register-only",
        action="store_true",
        help="Only emit sourcing_register_mirror statements (requires dimensions/SOURCING_REGISTER.csv) [Initiative 31]",
    )
    # I32 P2/P3/P4/P7 — 4 new flags
    parser.add_argument(
        "--skill-registry-only",
        action="store_true",
        help="Only emit skill_registry_mirror statements (requires dimensions/SKILL_REGISTRY.csv) [Initiative 32 P2]",
    )
    parser.add_argument(
        "--touchpoint-kit-cell-only",
        action="store_true",
        help="Only emit touchpoint_kit_cell_mirror statements (requires dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv) [Initiative 32 P3]",
    )
    parser.add_argument(
        "--policy-register-only",
        action="store_true",
        help="Only emit policy_register_mirror statements (requires dimensions/POLICY_REGISTER.csv) [Initiative 32 P4]",
    )
    parser.add_argument(
        "--repo-health-snapshot-only",
        action="store_true",
        help="Only emit repo_health_snapshot_mirror statements (requires REPO_HEALTH_SNAPSHOT.csv) [Initiative 32 P7]",
    )
    # I59 P1 — five HLK governance dimensions (planning workspace SSOT)
    parser.add_argument(
        "--repository-registry-only",
        action="store_true",
        help="Only emit repository_registry_mirror statements (requires REPOSITORY_REGISTRY.csv) [Initiative 59 P1.1]",
    )
    parser.add_argument(
        "--initiative-registry-only",
        action="store_true",
        help="Only emit initiative_registry_mirror statements (requires INITIATIVE_REGISTRY.csv) [Initiative 59 P1.2]",
    )
    parser.add_argument(
        "--ops-register-only",
        action="store_true",
        help="Only emit ops_register_mirror statements (requires OPS_REGISTER.csv) [Initiative 59 P1.3]",
    )
    parser.add_argument(
        "--cycle-register-only",
        action="store_true",
        help="Only emit cycle_register_mirror statements (requires CYCLE_REGISTER.csv) [Initiative 59 P1.4]",
    )
    parser.add_argument(
        "--decision-register-only",
        action="store_true",
        help="Only emit decision_register_mirror statements (requires DECISION_REGISTER.csv) [Initiative 59 P1.5]",
    )
    parser.add_argument(
        "--engagement-model-only",
        action="store_true",
        help="Only emit engagement_model_registry_mirror statements (requires ENGAGEMENT_MODEL_REGISTRY.csv) [Initiative 73 P1]",
    )
    parser.add_argument(
        "--design-pattern-registry-only",
        action="store_true",
        help="Only emit people_design_pattern_registry_mirror statements (requires PEOPLE_DESIGN_PATTERN_REGISTRY.csv) [Initiative 79 P2]",
    )
    parser.add_argument(
        "--substrate-registry-only",
        action="store_true",
        help="Only emit substrate_registry_mirror statements (requires SUBSTRATE_REGISTRY.csv) [Initiative 84 P3]",
    )
    parser.add_argument(
        "--intelligenceops-only",
        action="store_true",
        help="Only emit intelligenceops_register_mirror statements (requires INTELLIGENCEOPS_REGISTER.csv) [I72 P6 + I75 D-IH-86-FH]",
    )
    parser.add_argument(
        "--collaborator-share-only",
        action="store_true",
        help=(
            "Only emit the 5 Collaborator Share mirrors as ONE atomic kit "
            "(clauses + market_rate + share_registry + rate_overrides + vendor_billed). "
            "Requires the 5 sibling CSVs under People Operations/canonicals/dimensions/. "
            "[I86 Wave R+1 P2c-a; D-IH-86-DA/DB/DC/DD/DE]"
        ),
    )
    parser.add_argument(
        "--output-type-registry-only",
        action="store_true",
        help="Only emit output_type_registry_mirror statements (requires OUTPUT_TYPE_REGISTRY.csv) [I86 Wave L D-IH-86-BG]",
    )
    parser.add_argument(
        "--artifact-class-registry-only",
        action="store_true",
        help="Only emit artifact_class_registry_mirror statements (requires ARTIFACT_CLASS_REGISTRY.csv) [I86 Wave L D-IH-86-BG]",
    )
    parser.add_argument(
        "--component-primitive-registry-only",
        action="store_true",
        help="Only emit component_primitive_registry_mirror statements (requires COMPONENT_PRIMITIVE_REGISTRY.csv) [I86 Wave L D-IH-86-BG]",
    )
    parser.add_argument(
        "--no-begin-commit",
        action="store_true",
        help="Omit BEGIN/COMMIT wrapper",
    )
    args = parser.parse_args()
    if args.ops8615_gap_mirrors_only and args.output is None and not args.ops8615_split:
        args.output = REPO_ROOT / I93_P6_OPS8615_UPSERT_ARTIFACT
        args.output.parent.mkdir(parents=True, exist_ok=True)
    mode_flags = sum(
        1
        for x in (
            args.process_list_only,
            args.baseline_only,
            args.finops_counterparty_register_only,
            args.goipoi_register_only,
            args.adviser_disciplines_only,
            args.adviser_questions_only,
            args.founder_filed_instruments_only,
            args.program_registry_only,
            args.topic_registry_only,
            args.persona_registry_only,
            args.persona_scenario_registry_only,
            args.channel_touchpoint_registry_only,
            args.sourcing_register_only,
            args.skill_registry_only,
            args.touchpoint_kit_cell_only,
            args.policy_register_only,
            args.repo_health_snapshot_only,
            args.repository_registry_only,
            args.initiative_registry_only,
            args.ops_register_only,
            args.cycle_register_only,
            args.decision_register_only,
            args.engagement_model_only,
            args.design_pattern_registry_only,
            args.substrate_registry_only,
            args.intelligenceops_only,
            args.collaborator_share_only,
            args.output_type_registry_only,
            args.artifact_class_registry_only,
            args.component_primitive_registry_only,
        )
        if x
    )
    if mode_flags > 1:
        print(
            "error: at most one of --process-list-only, --baseline-only, "
            "--finops-counterparty-register-only, --goipoi-register-only, "
            "--adviser-disciplines-only, --adviser-questions-only, "
            "--founder-filed-instruments-only, --program-registry-only, "
            "--topic-registry-only, --persona-registry-only, "
            "--persona-scenario-registry-only, "
            "--channel-touchpoint-registry-only, "
            "--repository-registry-only, --initiative-registry-only, "
            "--ops-register-only, --cycle-register-only, "
            "--decision-register-only, --collaborator-share-only",
            file=sys.stderr,
        )
        return 1

    sha = (args.git_sha or "").strip() or _git_head_sha()

    if args.finops_counterparty_register_only:
        if not FINOPS_CSV.is_file():
            print("error: missing", FINOPS_CSV, file=sys.stderr)
            return 1
        with FINOPS_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES):
                print(
                    "error: FINOPS_COUNTERPARTY_REGISTER.csv header drift vs FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            finops_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"finops_counterparty_register_rows={len(finops_rows)}")
            return 0
        blocks = _emit_finops_counterparty_upserts(finops_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.finops_counterparty_register_mirror exists (Initiative 18 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.goipoi_register_only:
        if not GOIPOI_CSV.is_file():
            print("error: missing", GOIPOI_CSV, file=sys.stderr)
            return 1
        with GOIPOI_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(GOIPOI_REGISTER_FIELDNAMES):
                print(
                    "error: GOI_POI_REGISTER.csv header drift vs GOIPOI_REGISTER_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(GOIPOI_REGISTER_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            goipoi_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"goipoi_register_rows={len(goipoi_rows)}")
            return 0
        blocks = _emit_goipoi_upserts(goipoi_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.goipoi_register_mirror exists (Initiative 21 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.adviser_disciplines_only:
        if not ADVISER_DISCIPLINES_CSV.is_file():
            print("error: missing", ADVISER_DISCIPLINES_CSV, file=sys.stderr)
            return 1
        with ADVISER_DISCIPLINES_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES):
                print(
                    "error: ADVISER_ENGAGEMENT_DISCIPLINES.csv header drift vs ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            ad_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"adviser_engagement_disciplines_rows={len(ad_rows)}")
            return 0
        blocks = _emit_adviser_disciplines_upserts(ad_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.adviser_engagement_disciplines_mirror exists (Initiative 21 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.adviser_questions_only:
        if not ADVISER_QUESTIONS_CSV.is_file():
            print("error: missing", ADVISER_QUESTIONS_CSV, file=sys.stderr)
            return 1
        with ADVISER_QUESTIONS_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(ADVISER_OPEN_QUESTIONS_FIELDNAMES):
                print(
                    "error: ADVISER_OPEN_QUESTIONS.csv header drift vs ADVISER_OPEN_QUESTIONS_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(ADVISER_OPEN_QUESTIONS_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            aq_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"adviser_open_questions_rows={len(aq_rows)}")
            return 0
        blocks = _emit_adviser_questions_upserts(aq_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.adviser_open_questions_mirror exists (Initiative 21 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.founder_filed_instruments_only:
        if not FILED_INSTRUMENTS_CSV.is_file():
            print("error: missing", FILED_INSTRUMENTS_CSV, file=sys.stderr)
            return 1
        with FILED_INSTRUMENTS_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(FILED_INSTRUMENTS_FIELDNAMES):
                print(
                    "error: FILED_INSTRUMENTS.csv header drift vs FILED_INSTRUMENTS_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(FILED_INSTRUMENTS_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            fi_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"founder_filed_instruments_rows={len(fi_rows)}")
            return 0
        blocks = _emit_founder_filed_instruments_upserts(fi_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.filed_instruments_mirror exists (I21 DDL + I81 P2 T3 rename migration).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.program_registry_only:
        if not PROGRAM_REGISTRY_CSV.is_file():
            print("error: missing", PROGRAM_REGISTRY_CSV, file=sys.stderr)
            return 1
        with PROGRAM_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(PROGRAM_REGISTRY_FIELDNAMES):
                print(
                    "error: PROGRAM_REGISTRY.csv header drift vs PROGRAM_REGISTRY_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(PROGRAM_REGISTRY_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            pr_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"program_registry_rows={len(pr_rows)}")
            return 0
        blocks = _emit_program_registry_upserts(pr_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.program_registry_mirror exists (Initiative 23 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.topic_registry_only:
        if not TOPIC_REGISTRY_CSV.is_file():
            print("error: missing", TOPIC_REGISTRY_CSV, file=sys.stderr)
            return 1
        with TOPIC_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(TOPIC_REGISTRY_FIELDNAMES):
                print(
                    "error: TOPIC_REGISTRY.csv header drift vs TOPIC_REGISTRY_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(TOPIC_REGISTRY_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            tr_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"topic_registry_rows={len(tr_rows)}")
            return 0
        blocks = _emit_topic_registry_upserts(tr_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.topic_registry_mirror exists (Initiative 25 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.persona_registry_only:
        if not PERSONA_REGISTRY_CSV.is_file():
            print("error: missing", PERSONA_REGISTRY_CSV, file=sys.stderr)
            return 1
        with PERSONA_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(PERSONA_REGISTRY_FIELDNAMES):
                print(
                    "error: PERSONA_REGISTRY.csv header drift vs PERSONA_REGISTRY_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(PERSONA_REGISTRY_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            pr_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"persona_registry_rows={len(pr_rows)}")
            return 0
        blocks = _emit_persona_registry_upserts(pr_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.persona_registry_mirror exists (Initiative 31 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.persona_scenario_registry_only:
        if not PERSONA_SCENARIO_REGISTRY_CSV.is_file():
            print("error: missing", PERSONA_SCENARIO_REGISTRY_CSV, file=sys.stderr)
            return 1
        with PERSONA_SCENARIO_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES):
                print(
                    "error: PERSONA_SCENARIO_REGISTRY.csv header drift vs PERSONA_SCENARIO_REGISTRY_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            psr_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"persona_scenario_registry_rows={len(psr_rows)}")
            return 0
        blocks = _emit_persona_scenario_registry_upserts(psr_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.persona_scenario_registry_mirror exists (Initiative 47 P1 DDL + I49 priority columns).",
            "-- I51 P1 closes OPS-47-9 (mirror reseed): emitter wired up.",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.sourcing_register_only:
        if not SOURCING_REGISTER_CSV.is_file():
            print("error: missing", SOURCING_REGISTER_CSV, file=sys.stderr)
            return 1
        with SOURCING_REGISTER_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(SOURCING_REGISTER_FIELDNAMES):
                print(
                    "error: SOURCING_REGISTER.csv header drift vs SOURCING_REGISTER_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(SOURCING_REGISTER_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            sr_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"sourcing_register_rows={len(sr_rows)}")
            return 0
        blocks = _emit_sourcing_register_upserts(sr_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.sourcing_register_mirror exists (Initiative 31 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    _i93_ops8615_specs: list[tuple[Path, tuple[str, ...], str, str, callable]] = [
        (AIC_REGISTRY_CSV, AIC_REGISTRY_FIELDNAMES, "compliance.aic_registry_mirror", "aic_registry_rows", _emit_aic_registry_upserts),
        (AUDIENCE_REGISTRY_CSV, AUDIENCE_REGISTRY_FIELDNAMES, "compliance.audience_registry_mirror", "audience_registry_rows", _emit_audience_registry_upserts),
        (CAPABILITY_REGISTRY_CSV, CAPABILITY_REGISTRY_FIELDNAMES, "compliance.capability_registry_mirror", "capability_registry_rows", _emit_capability_registry_upserts),
        (
            CAPABILITY_CONFIDENCE_REGISTRY_CSV,
            CAPABILITY_CONFIDENCE_FIELDNAMES,
            "compliance.capability_confidence_registry_mirror",
            "capability_confidence_registry_rows",
            _emit_capability_confidence_registry_upserts,
        ),
        (
            COUNTRY_WORK_CALENDAR_CSV,
            COUNTRY_WORK_CALENDAR_FIELDNAMES,
            "compliance.country_work_calendar_mirror",
            "country_work_calendar_rows",
            _emit_country_work_calendar_upserts,
        ),
    ]
    if args.ops8615_gap_mirrors_only:
        loaded: list[tuple[str, str, list[dict[str, str]], callable]] = []
        for csv_path, fieldnames, mirror_table, count_key, emit_fn in _i93_ops8615_specs:
            if not csv_path.is_file():
                print("error: missing", csv_path, file=sys.stderr)
                return 1
            with csv_path.open(encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                fn = list(reader.fieldnames or [])
                if fn != list(fieldnames):
                    print(f"error: {csv_path.name} header drift", file=sys.stderr)
                    return 1
                rows = [dict(r) for r in reader]
            loaded.append((count_key, mirror_table, rows, emit_fn))
        if args.count_only:
            print(f"source_git_sha={sha}")
            for count_key, _mirror_table, rows, _emit_fn in loaded:
                print(f"{count_key}={len(rows)}")
            return 0

        def _ops8615_preamble() -> list[str]:
            lines = [
                "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
                f"-- source_git_sha: {sha}",
                "-- Apply after supabase/migrations/20260604120000_i93_p6_ops8615_mirror_gap_closure.sql",
                "",
            ]
            if not args.no_begin_commit:
                lines.extend(["BEGIN;", ""])
            return lines

        def _ops8615_ending() -> list[str]:
            return ["", "COMMIT;", ""] if not args.no_begin_commit else []

        if args.ops8615_split:
            if args.output is not None and args.output.suffix != ".sql":
                batch_dir = args.output
            elif args.output is not None:
                batch_dir = args.output.parent / "ops8615-batches"
            else:
                batch_dir = REPO_ROOT / Path(I93_P6_OPS8615_UPSERT_ARTIFACT).parent / "ops8615-batches"
            batch_dir.mkdir(parents=True, exist_ok=True)
            manifest: list[str] = [
                "# OPS-86-15 mirror batches (auto-generated manifest)",
                "",
                f"source_git_sha: {sha}",
                "",
                "Apply in numeric order. Prefer **psql** for all files; SQL Editor is OK for 01–02 and 05 only.",
                "",
                "| order | file | mirror | expected rows |",
                "| --- | --- | --- | ---: |",
            ]
            for idx, (count_key, mirror_table, rows, emit_fn) in enumerate(loaded, start=1):
                slug = mirror_table.removeprefix("compliance.").removesuffix("_mirror")
                path = batch_dir / f"{idx:02d}-{slug}.sql"
                blocks = emit_fn(rows, sha)
                text = "\n".join(_ops8615_preamble() + blocks + _ops8615_ending())
                path.write_text(text, encoding="utf-8")
                print("Wrote", path, "bytes=", len(text.encode("utf-8")), f"rows={len(rows)}")
                manifest.append(f"| {idx:02d} | `{path.name}` | `{mirror_table}` | {len(rows)} |")
            (batch_dir / "MANIFEST.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
            print("Wrote", batch_dir / "MANIFEST.md")
            return 0

        all_blocks: list[str] = []
        for _count_key, _mirror_table, rows, emit_fn in loaded:
            all_blocks.extend(emit_fn(rows, sha))
        text = "\n".join(_ops8615_preamble() + all_blocks + _ops8615_ending())
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.channel_touchpoint_registry_only:
        if not CHANNEL_TOUCHPOINT_REGISTRY_CSV.is_file():
            print("error: missing", CHANNEL_TOUCHPOINT_REGISTRY_CSV, file=sys.stderr)
            return 1
        with CHANNEL_TOUCHPOINT_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES):
                print(
                    "error: CHANNEL_TOUCHPOINT_REGISTRY.csv header drift vs CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            ct_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"channel_touchpoint_registry_rows={len(ct_rows)}")
            return 0
        blocks = _emit_channel_touchpoint_registry_upserts(ct_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.channel_touchpoint_registry_mirror exists (Initiative 31 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    # I32 P2/P3/P4/P7 — 4 new mirror branches use a compact factory pattern.
    _i32_mirror_specs: list[tuple[bool, Path, tuple[str, ...], str, str]] = [
        (
            args.skill_registry_only, SKILL_REGISTRY_CSV, SKILL_REGISTRY_FIELDNAMES,
            "compliance.skill_registry_mirror", "Initiative 32 P2",
        ),
        (
            args.touchpoint_kit_cell_only, TOUCHPOINT_KIT_CELL_CSV, TOUCHPOINT_KIT_CELL_FIELDNAMES,
            "compliance.touchpoint_kit_cell_mirror", "Initiative 32 P3",
        ),
        (
            args.policy_register_only, POLICY_REGISTER_CSV, POLICY_REGISTER_FIELDNAMES,
            "compliance.policy_register_mirror", "Initiative 32 P4",
        ),
        (
            args.repo_health_snapshot_only, REPO_HEALTH_SNAPSHOT_CSV, REPO_HEALTH_SNAPSHOT_FIELDNAMES,
            "compliance.repo_health_snapshot_mirror", "Initiative 32 P7",
        ),
    ]
    _i32_emit_fns = {
        "compliance.skill_registry_mirror": _emit_skill_registry_upserts,
        "compliance.touchpoint_kit_cell_mirror": _emit_touchpoint_kit_cell_upserts,
        "compliance.policy_register_mirror": _emit_policy_register_upserts,
        "compliance.repo_health_snapshot_mirror": _emit_repo_health_snapshot_upserts,
    }
    _i32_count_keys = {
        "compliance.skill_registry_mirror": "skill_registry_rows",
        "compliance.touchpoint_kit_cell_mirror": "touchpoint_kit_cell_rows",
        "compliance.policy_register_mirror": "policy_register_rows",
        "compliance.repo_health_snapshot_mirror": "repo_health_snapshot_rows",
    }
    for flag, csv_path, fieldnames, mirror_table, initiative in _i32_mirror_specs:
        if not flag:
            continue
        if not csv_path.is_file():
            print("error: missing", csv_path, file=sys.stderr)
            return 1
        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(fieldnames):
                print(f"error: {csv_path.name} header drift vs contract", file=sys.stderr)
                print("  expected:", list(fieldnames), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            i32_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"{_i32_count_keys[mirror_table]}={len(i32_rows)}")
            return 0
        blocks = _i32_emit_fns[mirror_table](i32_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            f"-- Apply only after {mirror_table} exists ({initiative} DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    # I86 Wave R+1 P2c-a — Collaborator Share 5-mirror kit. Dispatched together
    # because the doctrine treats them as ONE atomic set (per
    # .cursor/rules/akos-collaborator-share.mdc RULE 2). One flag → one combined
    # SQL output covering all 5 mirrors in FK-safe dependency order.
    if args.collaborator_share_only:
        # Per-mirror header drift check + row load.
        cs_loaded: list[tuple[str, tuple[str, ...], str, list[dict[str, str]]]] = []
        for mirror_table, csv_path, fieldnames, pk_column in COLLABORATOR_SHARE_MIRROR_SPECS:
            if not csv_path.is_file():
                print("error: missing", csv_path, file=sys.stderr)
                return 1
            with csv_path.open(encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                fn = list(reader.fieldnames or [])
                if fn != list(fieldnames):
                    print(f"error: {csv_path.name} header drift vs contract", file=sys.stderr)
                    print("  expected:", list(fieldnames), file=sys.stderr)
                    print("  got:     ", fn, file=sys.stderr)
                    return 1
                cs_loaded.append((mirror_table, fieldnames, pk_column, [dict(r) for r in reader]))
        if args.count_only:
            print(f"source_git_sha={sha}")
            for mirror_table, _fn, _pk, rows in cs_loaded:
                # Slug ends with `_mirror`; the count key drops it for symmetry
                # with the `_i59_count_keys` style (e.g. `collaborator_share_registry_rows`).
                key = mirror_table.split(".", 1)[1].removesuffix("_mirror") + "_rows"
                print(f"{key}={len(rows)}")
            return 0
        blocks: list[str] = []
        for mirror_table, fieldnames, pk_column, rows in cs_loaded:
            blocks.extend(
                _emit_generic_pk_upserts(
                    rows=rows,
                    fieldnames=fieldnames,
                    mirror_table=mirror_table,
                    pk_column=pk_column,
                    source_git_sha=sha,
                    initiative_label="I86 Wave R+1 P2c-a",
                )
            )
            blocks.append("")  # blank line between per-mirror blocks for readability
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Collaborator Share kit (I86 Wave R+1 P2c-a; D-IH-86-DA/DB/DC/DD/DE).",
            "-- Apply only after the 5 mirror tables exist (see Supabase migration",
            "-- supabase/migrations/20260524000000_i86_wr1_collaborator_share_mirrors.sql).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    # I59 P1 — 5 new HLK governance dimensions reuse the same compact factory pattern.
    _i59_mirror_specs: list[tuple[bool, Path, tuple[str, ...], str, str]] = [
        (
            args.repository_registry_only, REPOSITORY_REGISTRY_CSV, REPOSITORY_REGISTRY_FIELDNAMES,
            "compliance.repository_registry_mirror", "Initiative 59 P1.1",
        ),
        (
            args.initiative_registry_only, INITIATIVE_REGISTRY_CSV, INITIATIVE_REGISTRY_FIELDNAMES,
            "compliance.initiative_registry_mirror", "Initiative 59 P1.2",
        ),
        (
            args.ops_register_only, OPS_REGISTER_CSV, OPS_REGISTER_FIELDNAMES,
            "compliance.ops_register_mirror", "Initiative 59 P1.3",
        ),
        (
            args.cycle_register_only, CYCLE_REGISTER_CSV, CYCLE_REGISTER_FIELDNAMES,
            "compliance.cycle_register_mirror", "Initiative 59 P1.4",
        ),
        (
            args.decision_register_only, DECISION_REGISTER_CSV, DECISION_REGISTER_FIELDNAMES,
            "compliance.decision_register_mirror", "Initiative 59 P1.5",
        ),
        # I73 P1 — engagement-model registry (sibling dimension; D-IH-73-C).
        (
            args.engagement_model_only, ENGAGEMENT_MODEL_REGISTRY_CSV, ENGAGEMENT_MODEL_FIELDNAMES,
            "compliance.engagement_model_registry_mirror", "Initiative 73 P1",
        ),
        # I79 P2 — People Design Pattern Registry (cross-area design pattern library; D-IH-79-C/D).
        (
            args.design_pattern_registry_only, DESIGN_PATTERN_REGISTRY_CSV, DESIGN_PATTERN_FIELDNAMES,
            "compliance.people_design_pattern_registry_mirror", "Initiative 79 P2",
        ),
        # I84 P3 — Substrate Registry (substrate doctrine SSOT; D-IH-84-A/F/G).
        (
            args.substrate_registry_only, SUBSTRATE_REGISTRY_CSV, SUBSTRATE_REGISTRY_FIELDNAMES,
            "compliance.substrate_registry_mirror", "Initiative 84 P3",
        ),
        # I72 P6 + I75 — IntelligenceOps register (radar freshness cols; D-IH-86-FH).
        (
            args.intelligenceops_only, INTELLIGENCEOPS_REGISTER_CSV, INTELLIGENCEOPS_REGISTER_FIELDNAMES,
            "compliance.intelligenceops_register_mirror", "Initiative 72 P6 + I75",
        ),
        # I86 Wave L — Output architecture mirrors (D-IH-86-BG; 4-layer architecture
        # beneath the 5-axis Quality Fabric). Layer 1 + Layer 2 + Layer 3 in dispatch order
        # so cross-FKs resolve cleanly when emitted in sequence.
        (
            args.output_type_registry_only, OUTPUT_TYPE_REGISTRY_CSV, OUTPUT_TYPE_REGISTRY_FIELDNAMES,
            "compliance.output_type_registry_mirror", "I86 Wave L (Layer 1)",
        ),
        (
            args.artifact_class_registry_only, ARTIFACT_CLASS_REGISTRY_CSV, ARTIFACT_CLASS_REGISTRY_FIELDNAMES,
            "compliance.artifact_class_registry_mirror", "I86 Wave L (Layer 2)",
        ),
        (
            args.component_primitive_registry_only, COMPONENT_PRIMITIVE_REGISTRY_CSV, COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES,
            "compliance.component_primitive_registry_mirror", "I86 Wave L (Layer 3)",
        ),
    ]
    _i59_emit_fns = {
        "compliance.output_type_registry_mirror": _emit_output_type_registry_upserts,
        "compliance.artifact_class_registry_mirror": _emit_artifact_class_registry_upserts,
        "compliance.component_primitive_registry_mirror": _emit_component_primitive_registry_upserts,
        "compliance.repository_registry_mirror": _emit_repository_registry_upserts,
        "compliance.initiative_registry_mirror": _emit_initiative_registry_upserts,
        "compliance.ops_register_mirror": _emit_ops_register_upserts,
        "compliance.cycle_register_mirror": _emit_cycle_register_upserts,
        "compliance.decision_register_mirror": _emit_decision_register_upserts,
        "compliance.engagement_model_registry_mirror": _emit_engagement_model_upserts,
        "compliance.people_design_pattern_registry_mirror": _emit_design_pattern_upserts,
        "compliance.substrate_registry_mirror": _emit_substrate_registry_upserts,
        "compliance.intelligenceops_register_mirror": _emit_intelligenceops_register_upserts,
    }
    _i59_count_keys = {
        "compliance.repository_registry_mirror": "repository_registry_rows",
        "compliance.initiative_registry_mirror": "initiative_registry_rows",
        "compliance.ops_register_mirror": "ops_register_rows",
        "compliance.cycle_register_mirror": "cycle_register_rows",
        "compliance.decision_register_mirror": "decision_register_rows",
        "compliance.engagement_model_registry_mirror": "engagement_model_registry_rows",
        "compliance.people_design_pattern_registry_mirror": "people_design_pattern_registry_rows",
        "compliance.substrate_registry_mirror": "substrate_registry_rows",
        "compliance.intelligenceops_register_mirror": "intelligenceops_register_rows",
    }
    for flag, csv_path, fieldnames, mirror_table, initiative in _i59_mirror_specs:
        if not flag:
            continue
        if not csv_path.is_file():
            print("error: missing", csv_path, file=sys.stderr)
            return 1
        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(fieldnames):
                print(f"error: {csv_path.name} header drift vs contract", file=sys.stderr)
                print("  expected:", list(fieldnames), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            i59_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"{_i59_count_keys[mirror_table]}={len(i59_rows)}")
            return 0
        blocks = _i59_emit_fns[mirror_table](i59_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            f"-- Apply only after {mirror_table} exists ({initiative} DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if not PROC_CSV.is_file():
        print("error: missing", PROC_CSV, file=sys.stderr)
        return 1
    if not ORG_CSV.is_file():
        print("error: missing", ORG_CSV, file=sys.stderr)
        return 1

    header, raw_proc = read_process_csv(PROC_CSV)
    if list(header) != PROCESS_LIST_FIELDNAMES:
        print("error: process_list.csv header drift vs PROCESS_LIST_FIELDNAMES", file=sys.stderr)
        return 1
    proc_rows = resolve_all_parent_ids([normalize_process_row(r) for r in raw_proc])

    with ORG_CSV.open(encoding="utf-8", newline="") as f:
        org_reader = csv.DictReader(f)
        org_fn = list(org_reader.fieldnames or [])
        if org_fn != list(BASELINE_FIELDNAMES):
            print("error: baseline_organisation.csv header drift vs script BASELINE_FIELDNAMES", file=sys.stderr)
            print("  expected:", list(BASELINE_FIELDNAMES), file=sys.stderr)
            print("  got:     ", org_fn, file=sys.stderr)
            return 1
        org_rows = [dict(r) for r in org_reader]

    finops_n = 0
    finops_rows: list[dict[str, str]] = []
    if FINOPS_CSV.is_file():
        with FINOPS_CSV.open(encoding="utf-8", newline="") as f:
            fr = csv.DictReader(f)
            if list(fr.fieldnames or []) == list(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES):
                finops_rows = [dict(r) for r in fr]
                finops_n = len(finops_rows)

    goipoi_n = 0
    goipoi_rows: list[dict[str, str]] = []
    if GOIPOI_CSV.is_file():
        with GOIPOI_CSV.open(encoding="utf-8", newline="") as f:
            gr = csv.DictReader(f)
            if list(gr.fieldnames or []) == list(GOIPOI_REGISTER_FIELDNAMES):
                goipoi_rows = [dict(r) for r in gr]
                goipoi_n = len(goipoi_rows)

    ad_n = 0
    ad_rows: list[dict[str, str]] = []
    if ADVISER_DISCIPLINES_CSV.is_file():
        with ADVISER_DISCIPLINES_CSV.open(encoding="utf-8", newline="") as f:
            ar = csv.DictReader(f)
            if list(ar.fieldnames or []) == list(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES):
                ad_rows = [dict(r) for r in ar]
                ad_n = len(ad_rows)

    aq_n = 0
    aq_rows: list[dict[str, str]] = []
    if ADVISER_QUESTIONS_CSV.is_file():
        with ADVISER_QUESTIONS_CSV.open(encoding="utf-8", newline="") as f:
            qr = csv.DictReader(f)
            if list(qr.fieldnames or []) == list(ADVISER_OPEN_QUESTIONS_FIELDNAMES):
                aq_rows = [dict(r) for r in qr]
                aq_n = len(aq_rows)

    fi_n = 0
    fi_rows: list[dict[str, str]] = []
    if FILED_INSTRUMENTS_CSV.is_file():
        with FILED_INSTRUMENTS_CSV.open(encoding="utf-8", newline="") as f:
            ir = csv.DictReader(f)
            if list(ir.fieldnames or []) == list(FILED_INSTRUMENTS_FIELDNAMES):
                fi_rows = [dict(r) for r in ir]
                fi_n = len(fi_rows)

    pr_n = 0
    pr_rows: list[dict[str, str]] = []
    if PROGRAM_REGISTRY_CSV.is_file():
        with PROGRAM_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            pr_reader = csv.DictReader(f)
            if list(pr_reader.fieldnames or []) == list(PROGRAM_REGISTRY_FIELDNAMES):
                pr_rows = [dict(r) for r in pr_reader]
                pr_n = len(pr_rows)

    tr_n = 0
    tr_rows: list[dict[str, str]] = []
    if TOPIC_REGISTRY_CSV.is_file():
        with TOPIC_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            tr_reader = csv.DictReader(f)
            if list(tr_reader.fieldnames or []) == list(TOPIC_REGISTRY_FIELDNAMES):
                tr_rows = [dict(r) for r in tr_reader]
                tr_n = len(tr_rows)

    persona_n = 0
    persona_rows: list[dict[str, str]] = []
    if PERSONA_REGISTRY_CSV.is_file():
        with PERSONA_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            persona_reader = csv.DictReader(f)
            if list(persona_reader.fieldnames or []) == list(PERSONA_REGISTRY_FIELDNAMES):
                persona_rows = [dict(r) for r in persona_reader]
                persona_n = len(persona_rows)

    psr_n = 0
    psr_rows: list[dict[str, str]] = []
    if PERSONA_SCENARIO_REGISTRY_CSV.is_file():
        with PERSONA_SCENARIO_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            psr_reader = csv.DictReader(f)
            if list(psr_reader.fieldnames or []) == list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES):
                psr_rows = [dict(r) for r in psr_reader]
                psr_n = len(psr_rows)

    ct_n = 0
    ct_rows: list[dict[str, str]] = []
    if CHANNEL_TOUCHPOINT_REGISTRY_CSV.is_file():
        with CHANNEL_TOUCHPOINT_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            ct_reader = csv.DictReader(f)
            if list(ct_reader.fieldnames or []) == list(CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES):
                ct_rows = [dict(r) for r in ct_reader]
                ct_n = len(ct_rows)

    sr_n = 0
    sr_rows: list[dict[str, str]] = []
    if SOURCING_REGISTER_CSV.is_file():
        with SOURCING_REGISTER_CSV.open(encoding="utf-8", newline="") as f:
            sr_reader = csv.DictReader(f)
            if list(sr_reader.fieldnames or []) == list(SOURCING_REGISTER_FIELDNAMES):
                sr_rows = [dict(r) for r in sr_reader]
                sr_n = len(sr_rows)

    # I32 P2/P3/P4/P7 — 4 new mirrors
    skill_n = 0
    skill_rows: list[dict[str, str]] = []
    if SKILL_REGISTRY_CSV.is_file():
        with SKILL_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            skr = csv.DictReader(f)
            if list(skr.fieldnames or []) == list(SKILL_REGISTRY_FIELDNAMES):
                skill_rows = [dict(r) for r in skr]
                skill_n = len(skill_rows)

    tkc_n = 0
    tkc_rows: list[dict[str, str]] = []
    if TOUCHPOINT_KIT_CELL_CSV.is_file():
        with TOUCHPOINT_KIT_CELL_CSV.open(encoding="utf-8", newline="") as f:
            tkr = csv.DictReader(f)
            if list(tkr.fieldnames or []) == list(TOUCHPOINT_KIT_CELL_FIELDNAMES):
                tkc_rows = [dict(r) for r in tkr]
                tkc_n = len(tkc_rows)

    pol_n = 0
    pol_rows: list[dict[str, str]] = []
    if POLICY_REGISTER_CSV.is_file():
        with POLICY_REGISTER_CSV.open(encoding="utf-8", newline="") as f:
            por = csv.DictReader(f)
            if list(por.fieldnames or []) == list(POLICY_REGISTER_FIELDNAMES):
                pol_rows = [dict(r) for r in por]
                pol_n = len(pol_rows)

    rhs_n = 0
    rhs_rows: list[dict[str, str]] = []
    if REPO_HEALTH_SNAPSHOT_CSV.is_file():
        with REPO_HEALTH_SNAPSHOT_CSV.open(encoding="utf-8", newline="") as f:
            rhsr = csv.DictReader(f)
            if list(rhsr.fieldnames or []) == list(REPO_HEALTH_SNAPSHOT_FIELDNAMES):
                rhs_rows = [dict(r) for r in rhsr]
                rhs_n = len(rhs_rows)

    # I59 P1 — 5 new HLK governance dimensions
    repo_reg_n = 0
    repo_reg_rows: list[dict[str, str]] = []
    if REPOSITORY_REGISTRY_CSV.is_file():
        with REPOSITORY_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            rrr = csv.DictReader(f)
            if list(rrr.fieldnames or []) == list(REPOSITORY_REGISTRY_FIELDNAMES):
                repo_reg_rows = [dict(r) for r in rrr]
                repo_reg_n = len(repo_reg_rows)

    init_reg_n = 0
    init_reg_rows: list[dict[str, str]] = []
    if INITIATIVE_REGISTRY_CSV.is_file():
        with INITIATIVE_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            irr = csv.DictReader(f)
            if list(irr.fieldnames or []) == list(INITIATIVE_REGISTRY_FIELDNAMES):
                init_reg_rows = [dict(r) for r in irr]
                init_reg_n = len(init_reg_rows)

    ops_reg_n = 0
    ops_reg_rows: list[dict[str, str]] = []
    if OPS_REGISTER_CSV.is_file():
        with OPS_REGISTER_CSV.open(encoding="utf-8", newline="") as f:
            orr = csv.DictReader(f)
            if list(orr.fieldnames or []) == list(OPS_REGISTER_FIELDNAMES):
                ops_reg_rows = [dict(r) for r in orr]
                ops_reg_n = len(ops_reg_rows)

    cycle_reg_n = 0
    cycle_reg_rows: list[dict[str, str]] = []
    if CYCLE_REGISTER_CSV.is_file():
        with CYCLE_REGISTER_CSV.open(encoding="utf-8", newline="") as f:
            crr = csv.DictReader(f)
            if list(crr.fieldnames or []) == list(CYCLE_REGISTER_FIELDNAMES):
                cycle_reg_rows = [dict(r) for r in crr]
                cycle_reg_n = len(cycle_reg_rows)

    dec_reg_n = 0
    dec_reg_rows: list[dict[str, str]] = []
    if DECISION_REGISTER_CSV.is_file():
        with DECISION_REGISTER_CSV.open(encoding="utf-8", newline="") as f:
            drr = csv.DictReader(f)
            if list(drr.fieldnames or []) == list(DECISION_REGISTER_FIELDNAMES):
                dec_reg_rows = [dict(r) for r in drr]
                dec_reg_n = len(dec_reg_rows)

    # I73 P1 — engagement-model registry (sibling dimension; D-IH-73-C).
    eng_model_n = 0
    eng_model_rows: list[dict[str, str]] = []
    if ENGAGEMENT_MODEL_REGISTRY_CSV.is_file():
        with ENGAGEMENT_MODEL_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            emr = csv.DictReader(f)
            if list(emr.fieldnames or []) == list(ENGAGEMENT_MODEL_FIELDNAMES):
                eng_model_rows = [dict(r) for r in emr]
                eng_model_n = len(eng_model_rows)

    # I79 P2 — People Design Pattern Registry (cross-area design pattern library; D-IH-79-C/D).
    design_pattern_n = 0
    design_pattern_rows: list[dict[str, str]] = []
    if DESIGN_PATTERN_REGISTRY_CSV.is_file():
        with DESIGN_PATTERN_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            dpr = csv.DictReader(f)
            if list(dpr.fieldnames or []) == list(DESIGN_PATTERN_FIELDNAMES):
                design_pattern_rows = [dict(r) for r in dpr]
                design_pattern_n = len(design_pattern_rows)

    # I84 P3 — Substrate Registry (substrate doctrine SSOT; D-IH-84-A/F/G).
    substrate_reg_n = 0
    substrate_reg_rows: list[dict[str, str]] = []
    if SUBSTRATE_REGISTRY_CSV.is_file():
        with SUBSTRATE_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            srr = csv.DictReader(f)
            if list(srr.fieldnames or []) == list(SUBSTRATE_REGISTRY_FIELDNAMES):
                substrate_reg_rows = [dict(r) for r in srr]
                substrate_reg_n = len(substrate_reg_rows)

    # I72 P6 + I75 — IntelligenceOps register (radar freshness cols; D-IH-86-FH).
    intelligenceops_n = 0
    intelligenceops_rows: list[dict[str, str]] = []
    if INTELLIGENCEOPS_REGISTER_CSV.is_file():
        with INTELLIGENCEOPS_REGISTER_CSV.open(encoding="utf-8", newline="") as f:
            ior = csv.DictReader(f)
            if list(ior.fieldnames or []) == list(INTELLIGENCEOPS_REGISTER_FIELDNAMES):
                intelligenceops_rows = [dict(r) for r in ior]
                intelligenceops_n = len(intelligenceops_rows)

    if args.count_only:
        print(f"source_git_sha={sha}")
        print(f"process_list_rows={len(proc_rows)}")
        print(f"baseline_organisation_rows={len(org_rows)}")
        print(f"finops_counterparty_register_rows={finops_n}")
        print(f"goipoi_register_rows={goipoi_n}")
        print(f"adviser_engagement_disciplines_rows={ad_n}")
        print(f"adviser_open_questions_rows={aq_n}")
        print(f"founder_filed_instruments_rows={fi_n}")
        print(f"program_registry_rows={pr_n}")
        print(f"topic_registry_rows={tr_n}")
        print(f"persona_registry_rows={persona_n}")
        print(f"persona_scenario_registry_rows={psr_n}")
        print(f"channel_touchpoint_registry_rows={ct_n}")
        print(f"sourcing_register_rows={sr_n}")
        # I32 P2/P3/P4/P7 additions
        print(f"skill_registry_rows={skill_n}")
        print(f"touchpoint_kit_cell_rows={tkc_n}")
        print(f"policy_register_rows={pol_n}")
        print(f"repo_health_snapshot_rows={rhs_n}")
        # I59 P1 additions
        print(f"repository_registry_rows={repo_reg_n}")
        print(f"initiative_registry_rows={init_reg_n}")
        print(f"ops_register_rows={ops_reg_n}")
        print(f"cycle_register_rows={cycle_reg_n}")
        print(f"decision_register_rows={dec_reg_n}")
        # I73 P1 addition
        print(f"engagement_model_registry_rows={eng_model_n}")
        # I79 P2 addition
        print(f"people_design_pattern_registry_rows={design_pattern_n}")
        # I84 P3 addition
        print(f"substrate_registry_rows={substrate_reg_n}")
        # I72 P6 + I75 addition
        print(f"intelligenceops_register_rows={intelligenceops_n}")
        return 0

    blocks: list[str] = []
    if not args.baseline_only:
        blocks.extend(_emit_process_list_upserts(proc_rows, sha))
    if not args.process_list_only:
        blocks.extend(_emit_baseline_upserts(org_rows, sha))
    if not args.process_list_only and not args.baseline_only and finops_rows:
        blocks.extend(_emit_finops_counterparty_upserts(finops_rows, sha))
    if not args.process_list_only and not args.baseline_only and goipoi_rows:
        blocks.extend(_emit_goipoi_upserts(goipoi_rows, sha))
    if not args.process_list_only and not args.baseline_only and ad_rows:
        blocks.extend(_emit_adviser_disciplines_upserts(ad_rows, sha))
    if not args.process_list_only and not args.baseline_only and aq_rows:
        blocks.extend(_emit_adviser_questions_upserts(aq_rows, sha))
    if not args.process_list_only and not args.baseline_only and fi_rows:
        blocks.extend(_emit_founder_filed_instruments_upserts(fi_rows, sha))
    if not args.process_list_only and not args.baseline_only and pr_rows:
        blocks.extend(_emit_program_registry_upserts(pr_rows, sha))
    if not args.process_list_only and not args.baseline_only and tr_rows:
        blocks.extend(_emit_topic_registry_upserts(tr_rows, sha))
    if not args.process_list_only and not args.baseline_only and persona_rows:
        blocks.extend(_emit_persona_registry_upserts(persona_rows, sha))
    if not args.process_list_only and not args.baseline_only and psr_rows:
        blocks.extend(_emit_persona_scenario_registry_upserts(psr_rows, sha))
    if not args.process_list_only and not args.baseline_only and ct_rows:
        blocks.extend(_emit_channel_touchpoint_registry_upserts(ct_rows, sha))
    if not args.process_list_only and not args.baseline_only and sr_rows:
        blocks.extend(_emit_sourcing_register_upserts(sr_rows, sha))
    # I32 P2/P3/P4/P7 — append the 4 new mirror upsert blocks to the full bundle.
    if not args.process_list_only and not args.baseline_only and skill_rows:
        blocks.extend(_emit_skill_registry_upserts(skill_rows, sha))
    if not args.process_list_only and not args.baseline_only and tkc_rows:
        blocks.extend(_emit_touchpoint_kit_cell_upserts(tkc_rows, sha))
    if not args.process_list_only and not args.baseline_only and pol_rows:
        blocks.extend(_emit_policy_register_upserts(pol_rows, sha))
    if not args.process_list_only and not args.baseline_only and rhs_rows:
        blocks.extend(_emit_repo_health_snapshot_upserts(rhs_rows, sha))
    # I59 P1 — append the 5 new HLK governance mirror upsert blocks to the full bundle.
    if not args.process_list_only and not args.baseline_only and repo_reg_rows:
        blocks.extend(_emit_repository_registry_upserts(repo_reg_rows, sha))
    if not args.process_list_only and not args.baseline_only and init_reg_rows:
        blocks.extend(_emit_initiative_registry_upserts(init_reg_rows, sha))
    if not args.process_list_only and not args.baseline_only and ops_reg_rows:
        blocks.extend(_emit_ops_register_upserts(ops_reg_rows, sha))
    if not args.process_list_only and not args.baseline_only and cycle_reg_rows:
        blocks.extend(_emit_cycle_register_upserts(cycle_reg_rows, sha))
    if not args.process_list_only and not args.baseline_only and dec_reg_rows:
        blocks.extend(_emit_decision_register_upserts(dec_reg_rows, sha))
    # I73 P1 — append engagement-model upserts to the full bundle.
    if not args.process_list_only and not args.baseline_only and eng_model_rows:
        blocks.extend(_emit_engagement_model_upserts(eng_model_rows, sha))
    # I79 P2 — append design pattern registry upserts to the full bundle.
    if not args.process_list_only and not args.baseline_only and design_pattern_rows:
        blocks.extend(_emit_design_pattern_upserts(design_pattern_rows, sha))
    # I84 P3 — substrate registry (substrate doctrine; D-IH-84-A/F/G).
    if not args.process_list_only and not args.baseline_only and substrate_reg_rows:
        blocks.extend(_emit_substrate_registry_upserts(substrate_reg_rows, sha))
    # I72 P6 + I75 — IntelligenceOps register (radar freshness cols; D-IH-86-FH).
    if not args.process_list_only and not args.baseline_only and intelligenceops_rows:
        blocks.extend(_emit_intelligenceops_register_upserts(intelligenceops_rows, sha))

    preamble = [
        "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
        f"-- source_git_sha: {sha}",
        "-- Apply only after compliance.process_list_mirror / baseline_organisation_mirror / finops_counterparty_register_mirror exist.",
        "",
    ]
    if not args.no_begin_commit:
        preamble.extend(["BEGIN;", ""])

    body = "\n".join(blocks) + "\n"

    ending: list[str] = []
    if not args.no_begin_commit:
        ending = ["", "COMMIT;", ""]

    text = "\n".join(preamble) + body + "\n".join(ending)

    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
