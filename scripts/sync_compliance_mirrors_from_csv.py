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
from akos.hlk_founder_filed_instruments_csv import FOUNDER_FILED_INSTRUMENTS_FIELDNAMES  # noqa: E402
from akos.hlk_channel_touchpoint_registry_csv import CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_cycle_register_csv import CYCLE_REGISTER_FIELDNAMES  # noqa: E402  # I59 P1.4
from akos.hlk_decision_register_csv import DECISION_REGISTER_FIELDNAMES  # noqa: E402  # I59 P1.5
from akos.hlk_engagement_model_csv import ENGAGEMENT_MODEL_FIELDNAMES  # noqa: E402  # I73 P1 (D-IH-73-C sibling-dimension; D-IH-73-D 7-class taxonomy)
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
FINOPS_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "FINOPS_COUNTERPARTY_REGISTER.csv"
_GOIPOI_CSV_NEW = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "GOI_POI_REGISTER.csv"
_GOIPOI_CSV_LEGACY = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "GOI_POI_REGISTER.csv"
# I32 P7 (D-IH-32-D): GOI/POI relocated to dimensions/. Deprecation alias for one cycle.
GOIPOI_CSV = _GOIPOI_CSV_NEW if _GOIPOI_CSV_NEW.is_file() else _GOIPOI_CSV_LEGACY
ADVISER_DISCIPLINES_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
ADVISER_QUESTIONS_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "ADVISER_OPEN_QUESTIONS.csv"
FILED_INSTRUMENTS_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "FOUNDER_FILED_INSTRUMENTS.csv"
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
        vals = ", ".join(_sql_text_literal(nr[k]) for k in PROCESS_LIST_FIELDNAMES)
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
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in BASELINE_FIELDNAMES)
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
    cols_csv = ", ".join(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in FOUNDER_FILED_INSTRUMENTS_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.founder_filed_instruments_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in FOUNDER_FILED_INSTRUMENTS_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        iid = (r.get("instrument_id") or "").strip()
        if not iid:
            continue
        out.append(
            f"INSERT INTO compliance.founder_filed_instruments_mirror ({cols_full}) VALUES ({vals_full}) "
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
    int_columns = {"cursor_rule_count", "brand_jargon_violations"}
    bool_columns = {
        "has_external_repo_contract",
        "has_akos_mirror_rule",
        "embedded_obsidian_snapshot_present",
    }
    for r in rows:
        slug = (r.get("repo_slug") or "").strip()
        sd = (r.get("snapshot_date") or "").strip()
        if not slug or not sd:
            continue
        row_vals: list[str] = []
        for c in REPO_HEALTH_SNAPSHOT_FIELDNAMES:
            raw = (r.get(c) or "").strip()
            if c == "snapshot_date":
                row_vals.append(f"DATE {_sql_text_literal(raw)}")
            elif c == "cursor_rule_count" or c == "brand_jargon_violations":
                row_vals.append(raw if raw else "0")
            elif c == "language_frontmatter_compliance_pct":
                row_vals.append(raw if raw else "0.0")
            elif c in bool_columns:
                row_vals.append("TRUE" if raw.lower() == "true" else "FALSE")
            else:
                row_vals.append(_sql_text_literal(raw))
        _ = int_columns  # silence unused (reserved for future strict casting)
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
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in REPOSITORY_REGISTRY_FIELDNAMES)
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
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in INITIATIVE_REGISTRY_FIELDNAMES)
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
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in OPS_REGISTER_FIELDNAMES)
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
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in CYCLE_REGISTER_FIELDNAMES)
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
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in DECISION_REGISTER_FIELDNAMES)
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
        help="Write SQL to this file (default: stdout)",
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
        help="Only emit founder_filed_instruments_mirror statements (requires FOUNDER_FILED_INSTRUMENTS.csv)",
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
        "--no-begin-commit",
        action="store_true",
        help="Omit BEGIN/COMMIT wrapper",
    )
    args = parser.parse_args()
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
            "--decision-register-only",
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
            if fn != list(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES):
                print(
                    "error: FOUNDER_FILED_INSTRUMENTS.csv header drift vs FOUNDER_FILED_INSTRUMENTS_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES), file=sys.stderr)
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
            "-- Apply only after compliance.founder_filed_instruments_mirror exists (Initiative 21 DDL).",
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
    ]
    _i59_emit_fns = {
        "compliance.repository_registry_mirror": _emit_repository_registry_upserts,
        "compliance.initiative_registry_mirror": _emit_initiative_registry_upserts,
        "compliance.ops_register_mirror": _emit_ops_register_upserts,
        "compliance.cycle_register_mirror": _emit_cycle_register_upserts,
        "compliance.decision_register_mirror": _emit_decision_register_upserts,
        "compliance.engagement_model_registry_mirror": _emit_engagement_model_upserts,
    }
    _i59_count_keys = {
        "compliance.repository_registry_mirror": "repository_registry_rows",
        "compliance.initiative_registry_mirror": "initiative_registry_rows",
        "compliance.ops_register_mirror": "ops_register_rows",
        "compliance.cycle_register_mirror": "cycle_register_rows",
        "compliance.decision_register_mirror": "decision_register_rows",
        "compliance.engagement_model_registry_mirror": "engagement_model_registry_rows",
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
            if list(ir.fieldnames or []) == list(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES):
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
