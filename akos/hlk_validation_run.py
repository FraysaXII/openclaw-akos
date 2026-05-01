"""Field contract for compliance.validation_runs (Initiative 32 P1).

Operational mirror — NOT git-canonical SSOT. Each row records the outcome of one
validator invocation (e.g., one run of ``scripts/validate_topic_registry.py``)
with its structured result. Same governance pattern as ``finops.registered_fact``
(Initiative 19): server-only writes (``service_role``), deny ``anon`` and
``authenticated``, no FK to canonical CSVs.

Use case: audit history. Answers "what was the validator state on date X?",
"how often did validator Y fail in the last quarter?", "which validator caught
the last drift incident?". Without it, validator runs are ephemeral CI events.

Per D-IH-32-F: writes happen via ``scripts/validate_hlk.py --json`` when invoked
with the ``--emit-validation-run-rows`` flag (default off); the structured JSON
report itself is always emitted to stdout. The Postgres write is operator-driven
or CI-driven, not part of every developer-local validator invocation.
"""

from __future__ import annotations

# Keep in sync with supabase/migrations/<ts>_i32_validation_runs.sql.
VALIDATION_RUN_FIELDNAMES: tuple[str, ...] = (
    "run_id",            # UUID v4, generated per dispatcher invocation
    "validator_name",    # e.g., 'validate_topic_registry'
    "started_at",        # ISO 8601 UTC timestamp
    "duration_ms",       # int milliseconds
    "status",            # 'pass' | 'fail' | 'error' | 'skipped'
    "exit_code",         # int (0 = pass)
    "row_count",         # int rows validated (when applicable; 0 otherwise)
    "error_count",       # int errors surfaced (0 when pass)
    "drift_detected",    # bool — true when a drift incident was recorded
    "git_sha",           # commit SHA at run time (string; 'dirty' if uncommitted)
    "host",              # short hostname (truncated; for cross-machine attribution)
    "notes",             # short free-text (e.g., 'invoked via CI', 'baseline regression')
)

VALID_STATUSES: tuple[str, ...] = ("pass", "fail", "error", "skipped")
