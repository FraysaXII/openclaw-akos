#!/usr/bin/env python3
"""G-58-1 pre-flight check for the Initiative 58 Phase A live cycle (OPS-58-1).

Asserts that the 11 operator-funded prerequisites are loaded into the calling
process environment before any of A.1 (judge calibration burn) / A.2 (persona
cassette dispatch) / A.3 (GraphRAG A/B) / A.4 (live MADEIRA dossier) fires.

The 11 checks mirror the I57 P4 forward checklist in
``docs/wip/planning/57-cycle-closeout-live-validation/reports/p4-live-cycle-forward-2026-05-04.md``
and ``ops-57-1-env-recheck-2026-05-04.md``, but resolve the I58 alias seam
(D-IH-58-G): each RunPod / Kalavai endpoint accepts either the canonical
``VLLM_*`` name or the I57-era ``*_ENDPOINT_URL`` alias.

This script is read-only: no live API calls, no Supabase writes, no model
calls. It loads the long-lived ``~/.openclaw/.env`` block (per D-IH-58-F) into
the process environment so operator-pasted values resolve, then evaluates each
check and prints a deterministic table.

Exit codes:
    0 — all 11 prerequisites met (G-58-1 GREEN; A.* may fire under the
        ``MAX_DOSSIER_USD`` envelope and the abort threshold wired into
        ``scripts/endpoint_envelope_alarm.py``).
    1 — one or more prerequisites missing (G-58-1 NO-FIRE; reschedule the
        window per R-58-1 + R-58-cycle2-A documented response).
    2 — script-internal failure (env file unreadable, etc.).

Usage (repo root):
    py scripts/preflight_g58_1.py

The script never authors secret values (D-IH-58-F / D-IH-17 invariance); it
only reads ``os.environ``. Operator pastes values into the empty placeholders
in ``~/.openclaw/.env`` (P0 wrote the structure).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.io import bootstrap_openclaw_process_env  # noqa: E402

ALARM_SCRIPT = REPO_ROOT / "scripts" / "endpoint_envelope_alarm.py"

MAX_DOSSIER_USD_CEILING = 50
"""Hard ceiling per D-IH-57-G inheritance (D-IH-58-B). Operators may set a
lower value (more conservative); they may not exceed this without a new
decision-log entry in the I58 decision-log."""

REQUIRED_JUDGE_PROVIDERS = ("anthropic", "openai")
"""Cross-family roster shape: `anthropic+openai` is the canonical pair for
`D-IH-52-B` cost-aware tiered escalation evidence. The preflight prefers this
pair but accepts an in-family pair (`anthropic+anthropic` flagship+cheap) per
the `D-IH-58-I` roster pivot, which is the documented fallback while OPS-58-2
(OpenAI key rotation) remains open. See [I52 P2 dispatcher
contract](../docs/wip/planning/52-multi-model-judge-and-cost-discipline/master-roadmap.md)
and [`docs/wip/planning/58-cycle-2-multi-track-forward/decision-log.md#d-ih-58-i`](../docs/wip/planning/58-cycle-2-multi-track-forward/decision-log.md)."""

MIN_ROSTER_MEMBERS = 2
"""``AKOS_JUDGE_ROSTER`` must list at least this many ``provider:model`` members
so the multi-judge dispatcher can run consensus mode."""


class CheckResult(NamedTuple):
    """Outcome of one of the 11 G-58-1 checks.

    NamedTuple (not ``@dataclass``) so module loading is robust under
    ``importlib.util.spec_from_file_location`` in tests — Python 3.14
    dataclass introspection requires the module to be in ``sys.modules``
    at decoration time, which is not guaranteed when the loader spec is
    used directly.
    """

    name: str
    required: str
    available: bool
    detail: str


def _is_truthy_one(value: str | None) -> bool:
    """``1``/``true``/``yes`` (case-insensitive) count as truthy; anything else does not.

    Empty string and ``None`` are falsy. Used by AKOS_RECORD_LIVE +
    AKOS_GRAPHRAG_POC_LIVE checks so the operator can't accidentally fire the
    cycle by typing ``AKOS_RECORD_LIVE=0``.
    """
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes"}


def _nonempty(value: str | None) -> bool:
    """Treat ``None`` / empty / whitespace-only as missing."""
    return bool(value and value.strip())


def _alias_resolved(canonical: str, alias: str) -> tuple[bool, str]:
    """Return ``(ok, detail)`` where ok is True if either env var is set.

    Per D-IH-58-G the canonical ``VLLM_*`` name wins precedence at runtime,
    but for the pre-flight check either name satisfies the prerequisite.
    """
    canonical_value = os.environ.get(canonical)
    alias_value = os.environ.get(alias)
    if _nonempty(canonical_value):
        return True, f"{canonical} set"
    if _nonempty(alias_value):
        return True, f"{alias} set (alias; {canonical} unset)"
    return False, f"both {canonical} and {alias} unset"


def _max_dossier_usd_check() -> CheckResult:
    """Verify ``MAX_DOSSIER_USD`` is set, integer-castable, and ``<=50``."""
    raw = os.environ.get("MAX_DOSSIER_USD")
    if not _nonempty(raw):
        return CheckResult(
            name="MAX_DOSSIER_USD",
            required=f"set; <={MAX_DOSSIER_USD_CEILING} (D-IH-57-G inheritance)",
            available=False,
            detail="unset",
        )
    try:
        envelope = int(str(raw).strip())
    except ValueError:
        return CheckResult(
            name="MAX_DOSSIER_USD",
            required=f"set; integer; <={MAX_DOSSIER_USD_CEILING}",
            available=False,
            detail=f"set but not integer: {raw!r}",
        )
    if envelope <= 0:
        return CheckResult(
            name="MAX_DOSSIER_USD",
            required=f"set; positive integer; <={MAX_DOSSIER_USD_CEILING}",
            available=False,
            detail=f"set but non-positive: {envelope}",
        )
    if envelope > MAX_DOSSIER_USD_CEILING:
        return CheckResult(
            name="MAX_DOSSIER_USD",
            required=f"<={MAX_DOSSIER_USD_CEILING}",
            available=False,
            detail=f"{envelope} exceeds D-IH-57-G ceiling of {MAX_DOSSIER_USD_CEILING}",
        )
    return CheckResult(
        name="MAX_DOSSIER_USD",
        required=f"set; <={MAX_DOSSIER_USD_CEILING}",
        available=True,
        detail=f"{envelope} (within ceiling)",
    )


def _judge_roster_check() -> CheckResult:
    """Verify ``AKOS_JUDGE_ROSTER`` is a >=2-member multi-judge roster.

    Accepts either:
    - **Cross-family (preferred):** at least one ``anthropic:`` member AND at
      least one ``openai:`` member -- canonical for ``D-IH-52-B`` evidence.
    - **In-family fallback (per ``D-IH-58-I``):** >=2 members from a single
      provider family (e.g. ``anthropic:claude-sonnet-4-5,anthropic:claude-haiku-4-5``)
      -- valid while ``OPS-58-2`` (OpenAI key rotation) remains open.
    """
    expected = "set; >=2 members; cross-family preferred (anthropic+openai)"
    roster = os.environ.get("AKOS_JUDGE_ROSTER")
    if not _nonempty(roster):
        return CheckResult(
            name="AKOS_JUDGE_ROSTER",
            required=expected,
            available=False,
            detail="unset",
        )
    members = [m.strip() for m in (roster or "").split(",") if m.strip()]
    if len(members) < MIN_ROSTER_MEMBERS:
        return CheckResult(
            name="AKOS_JUDGE_ROSTER",
            required=expected,
            available=False,
            detail=f"only {len(members)} member(s); need >= {MIN_ROSTER_MEMBERS}",
        )
    lower = (roster or "").lower()
    has_anthropic = "anthropic:" in lower
    has_openai = "openai:" in lower
    if has_anthropic and has_openai:
        return CheckResult(
            name="AKOS_JUDGE_ROSTER",
            required=expected,
            available=True,
            detail="cross-family: anthropic + openai present",
        )
    if has_anthropic or has_openai:
        family = "anthropic" if has_anthropic else "openai"
        return CheckResult(
            name="AKOS_JUDGE_ROSTER",
            required=expected,
            available=True,
            detail=f"in-family fallback ({family}-only; >= 2 members; D-IH-58-I)",
        )
    return CheckResult(
        name="AKOS_JUDGE_ROSTER",
        required=expected,
        available=False,
        detail="no recognized provider prefix (expected anthropic: or openai:)",
    )


def _alarm_script_check() -> CheckResult:
    """Verify ``scripts/endpoint_envelope_alarm.py`` is present in the repo."""
    if ALARM_SCRIPT.is_file():
        return CheckResult(
            name="endpoint_envelope_alarm.py",
            required="present (abort at $40 wired at invocation time)",
            available=True,
            detail=f"present: {ALARM_SCRIPT.relative_to(REPO_ROOT).as_posix()}",
        )
    return CheckResult(
        name="endpoint_envelope_alarm.py",
        required="present (abort at $40 wired at invocation time)",
        available=False,
        detail=f"missing: {ALARM_SCRIPT}",
    )


def evaluate_checks() -> list[CheckResult]:
    """Run all 11 pre-flight checks against the current ``os.environ``.

    Caller is expected to have invoked ``bootstrap_openclaw_process_env()``
    before this so the long-lived ``~/.openclaw/.env`` block is loaded.
    """
    results: list[CheckResult] = []

    results.append(
        CheckResult(
            name="AKOS_RECORD_LIVE",
            required="=1 (truthy)",
            available=_is_truthy_one(os.environ.get("AKOS_RECORD_LIVE")),
            detail=f"value={os.environ.get('AKOS_RECORD_LIVE')!r}",
        )
    )

    for var_name in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
        is_set = _nonempty(os.environ.get(var_name))
        results.append(
            CheckResult(
                name=var_name,
                required="set; non-empty (operator-pasted per D-IH-58-F)",
                available=is_set,
                detail="set" if is_set else "unset / empty",
            )
        )

    results.append(_max_dossier_usd_check())

    runpod_ok, runpod_detail = _alias_resolved("VLLM_RUNPOD_URL", "RUNPOD_ENDPOINT_URL")
    results.append(
        CheckResult(
            name="VLLM_RUNPOD_URL or RUNPOD_ENDPOINT_URL",
            required="at least one set (D-IH-58-G alias seam; VLLM_* wins precedence)",
            available=runpod_ok,
            detail=runpod_detail,
        )
    )

    kalavai_ok, kalavai_detail = _alias_resolved("VLLM_SHADOW_URL", "KALAVAI_ENDPOINT_URL")
    results.append(
        CheckResult(
            name="VLLM_SHADOW_URL or KALAVAI_ENDPOINT_URL",
            required="at least one set (D-IH-58-G alias seam; VLLM_* wins precedence)",
            available=kalavai_ok,
            detail=kalavai_detail,
        )
    )

    results.append(_judge_roster_check())

    results.append(
        CheckResult(
            name="AKOS_GRAPHRAG_POC_LIVE",
            required="=1 (truthy; A.3 only)",
            available=_is_truthy_one(os.environ.get("AKOS_GRAPHRAG_POC_LIVE")),
            detail=f"value={os.environ.get('AKOS_GRAPHRAG_POC_LIVE')!r}",
        )
    )

    results.append(_alarm_script_check())

    return results


def render_table(results: list[CheckResult]) -> str:
    """Format the check results as a human-readable table.

    Stable shape across runs so the regression test can lock the columns.
    """
    name_w = max(len(r.name) for r in results)
    name_w = max(name_w, len("Prerequisite"))
    lines: list[str] = []
    lines.append(f"  {'Prerequisite'.ljust(name_w)}  Status   Detail")
    lines.append(f"  {'-' * name_w}  -------  ------")
    for r in results:
        status = "OK" if r.available else "MISS"
        lines.append(f"  {r.name.ljust(name_w)}  {status.ljust(7)}  {r.detail}")
    return "\n".join(lines)


def summarize(results: list[CheckResult]) -> tuple[int, int]:
    """Return ``(met_count, total_count)`` across the check list."""
    met = sum(1 for r in results if r.available)
    return met, len(results)


def main(argv: list[str] | None = None) -> int:
    """Bootstrap the OpenClaw env file, run the 11 checks, render the table.

    Returns 0 on G-58-1 GREEN, 1 on NO-FIRE, 2 on script-internal failure.
    The argv parameter is reserved for future ``--json`` / ``--fail-soft``
    flags; currently it is accepted but unused so callers (CI, tests) can
    pass through arguments without crashing.
    """
    del argv
    try:
        bootstrap_openclaw_process_env()
    except Exception as exc:  # pragma: no cover - defensive: env file malformed
        print(f"preflight_g58_1: failed to bootstrap ~/.openclaw/.env: {exc}", file=sys.stderr)
        return 2

    results = evaluate_checks()
    met, total = summarize(results)

    print()
    print(f"  G-58-1 pre-flight check (Initiative 58 Phase A / OPS-58-1)")
    print(f"  D-IH-58-B + D-IH-58-F + D-IH-58-G inherit D-IH-57-G envelope")
    print()
    print(render_table(results))
    print()
    print(f"  Result: {met} / {total} prerequisites met")
    if met == total:
        print(f"  G-58-1 GREEN — A.* may fire under MAX_DOSSIER_USD={os.environ.get('MAX_DOSSIER_USD')} envelope.")
        print(f"  Wire endpoint_envelope_alarm.py at invocation time with --abort-at $40.")
        return 0
    print(f"  G-58-1 NO-FIRE — reschedule the window per R-58-1 + R-58-cycle2-A.")
    print(f"  Operator runbook: docs/wip/planning/57-cycle-closeout-live-validation/reports/p4-live-cycle-forward-2026-05-04.md")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
