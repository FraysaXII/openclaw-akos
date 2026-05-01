"""Initiative 45 P1 — Unified eval harness v2.

Collapses three drifting eval surfaces into one runner:
  - `--mode rubric`  — manifest-based suite scoring (was scripts/run-evals.py)
  - `--mode canary`  — per-skill scorecard + canary trips (was scripts/eval_per_skill.py)
  - `--mode smoke`   — in-process probes (was %TEMP%/madeira_uat_inproc.py)
  - `--mode replay`  — cassette replay (P2 fills in)
  - `--mode all`     — runs all four (defaults to rubric+canary+smoke; replay is opt-in)

Single Scorecard schema covers all modes. Output: JSON (machine) or markdown table (human).

Usage::

    py scripts/eval.py --mode canary --json
    py scripts/eval.py --mode rubric --suite pathc-research-spine
    py scripts/eval.py --mode all --json | jq '.modes.canary.canary_2_trips'

Per the I45 master-roadmap, this module is intentionally additive: existing
``akos/eval_harness/__init__.py`` re-exports the I10 API unchanged.
"""

from __future__ import annotations

import csv
import json
import logging
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("akos.eval.v2")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
)
BASELINES_DIR = REPO_ROOT / "config" / "eval-baselines"
CASSETTE_ROOT = REPO_ROOT / "tests" / "evals" / "cassettes"

VALID_MODES = ("rubric", "canary", "replay", "smoke", "adversarial", "all")


@dataclass
class ScoreRow:
    """One row in the unified Scorecard. Always carries skill_id (or '__suite__' for rubric mode)."""

    mode: str  # rubric|canary|replay|smoke
    skill_id: str
    name: str = ""
    status: str = "PASS"  # PASS|FAIL|SKIP
    baseline_pct: float | None = None
    current_pct: float | None = None
    delta_pp: float | None = None
    canary_2_tripped: bool = False
    cost_usd: float | None = None  # P4 fills in
    latency_ms_p50: float | None = None  # P4 fills in
    latency_ms_p95: float | None = None  # P4 fills in
    failures: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class Scorecard:
    """Unified scorecard shared by all modes."""

    schema_version: str = "1.0"
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    modes_run: list[str] = field(default_factory=list)
    rows: list[ScoreRow] = field(default_factory=list)
    overall_status: str = "pass"  # pass|fail
    elapsed_ms: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def add(self, row: ScoreRow) -> None:
        self.rows.append(row)
        if row.status == "FAIL":
            self.overall_status = "fail"

    def to_json(self) -> str:
        d = asdict(self)
        return json.dumps(d, indent=2, sort_keys=True, default=str)

    def to_markdown(self) -> str:
        lines = [
            "# AKOS Eval Scorecard (v2)",
            "",
            f"- generated_at: {self.generated_at}",
            f"- modes_run: {', '.join(self.modes_run)}",
            f"- overall_status: **{self.overall_status.upper()}**",
            f"- elapsed_ms: {self.elapsed_ms}",
            f"- rows: {len(self.rows)}",
            "",
            "| mode | skill_id | status | baseline | current | delta_pp | failures |",
            "|:-----|:---------|:-------|:---------|:--------|:---------|:---------|",
        ]
        for r in self.rows:
            bl = f"{r.baseline_pct:.1f}" if r.baseline_pct is not None else "-"
            cu = f"{r.current_pct:.1f}" if r.current_pct is not None else "-"
            dp = f"{r.delta_pp:+.1f}" if r.delta_pp is not None else "-"
            fl = "; ".join(r.failures[:3]) if r.failures else ""
            lines.append(
                f"| {r.mode} | {r.skill_id} | {r.status} | {bl} | {cu} | {dp} | {fl} |"
            )
        return "\n".join(lines) + "\n"


# ── Helpers ───────────────────────────────────────────────────────────────────


def _load_skill_registry() -> dict[str, dict[str, str]]:
    if not SKILL_CSV.is_file():
        return {}
    with SKILL_CSV.open(encoding="utf-8", newline="") as fh:
        return {r["skill_id"]: r for r in csv.DictReader(fh)}


def _load_baselines() -> dict[str, float]:
    out: dict[str, float] = {}
    if not BASELINES_DIR.is_dir():
        return out
    for p in BASELINES_DIR.glob("skill_*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            sid = data.get("skill_id")
            ebp = data.get("eval_baseline_pct")
            if sid and isinstance(ebp, (int, float)):
                out[sid] = float(ebp)
        except Exception as exc:
            logger.warning("baseline load skipped: %s (%s)", p.name, exc)
    return out


# ── Mode runners ──────────────────────────────────────────────────────────────


def run_canary(
    sc: Scorecard,
    *,
    threshold_pp: float = 2.0,
    overrides: dict[str, float] | None = None,
    enforce_cost: bool = False,
) -> None:
    """Per-skill scorecard + canary 2 (regression > threshold) + (P4) per-skill
    cost+latency from cassette aggregation + optional cost ceiling enforcement.
    """
    overrides = overrides or {}
    registry = _load_skill_registry()
    baselines = _load_baselines()

    # I45 P4: load cost ceilings + per-skill metrics (best-effort; soft-fail on import error)
    cost_ceilings: dict = {}
    aggregate_skill_cost = None
    evaluate_cost_ceiling = None
    try:
        from akos.eval_harness.cost_obs import (
            aggregate_skill_cost as _agg,
            evaluate_cost_ceiling as _eval,
            load_cost_ceilings,
        )
        cost_ceilings = load_cost_ceilings()
        aggregate_skill_cost = _agg
        evaluate_cost_ceiling = _eval
    except Exception as exc:
        logger.debug("cost_obs unavailable: %s", exc)

    for sid in sorted(registry.keys()):
        row = registry[sid]
        baseline = baselines.get(sid)
        if baseline is None:
            try:
                baseline = float(row.get("eval_baseline_pct", "0") or "0")
            except ValueError:
                baseline = 0.0
        current = overrides.get(sid, baseline)
        delta = current - baseline
        tripped = delta < -threshold_pp

        cost_usd: float | None = None
        latency_p50: float | None = None
        latency_p95: float | None = None
        cost_failures: list[str] = []
        cost_status: str = "SKIP"
        cost_notes = ""

        if aggregate_skill_cost is not None:
            metrics = aggregate_skill_cost(sid)
            if metrics is not None:
                cost_usd = round(metrics.cost_usd_avg, 6)
                latency_p50 = round(metrics.latency_ms_p50, 1)
                latency_p95 = round(metrics.latency_ms_p95, 1)
                ceiling = cost_ceilings.get(sid)
                cost_eval = evaluate_cost_ceiling(sid, metrics, ceiling) if evaluate_cost_ceiling else None
                if cost_eval is not None:
                    cost_status = cost_eval.get("status", "SKIP")
                    cost_failures = list(cost_eval.get("failures", []) or [])
                    cost_notes = cost_eval.get("reason", "")

        # Status: canary-2 still drives; cost_ceiling is additive when --enforce
        status = "FAIL" if tripped else "PASS"
        failures = [f"canary_2_regression:{abs(delta):.1f}pp"] if tripped else []
        if enforce_cost and cost_status == "FAIL":
            status = "FAIL"
            failures.extend(cost_failures)
        elif enforce_cost and cost_status == "WARN":
            failures.extend(cost_failures)
            # WARN does not fail the row; just surfaces

        notes_parts = [row.get("lifecycle_status", "")]
        if cost_notes:
            notes_parts.append(f"cost:{cost_notes}")
        sc.add(
            ScoreRow(
                mode="canary",
                skill_id=sid,
                name=row.get("name", ""),
                status=status,
                baseline_pct=baseline,
                current_pct=current,
                delta_pp=round(delta, 2),
                canary_2_tripped=tripped,
                cost_usd=cost_usd,
                latency_ms_p50=latency_p50,
                latency_ms_p95=latency_p95,
                failures=failures,
                notes="; ".join(p for p in notes_parts if p),
            )
        )


def run_rubric(
    sc: Scorecard,
    *,
    suite_ids: list[str] | None = None,
    governance_only: bool = False,
) -> None:
    """Manifest-based suite scoring. Replaces scripts/run-evals.py rubric path."""
    from akos.eval_harness import list_suite_ids, load_suite, score_rubric_task

    if governance_only:
        try:
            from akos.verification_profiles import governance_rubric_suites

            suite_ids = governance_rubric_suites()
        except Exception as exc:
            logger.warning("governance_rubric_suites unavailable: %s", exc)
            suite_ids = []
    if suite_ids is None:
        suite_ids = list_suite_ids()

    for sid in suite_ids:
        try:
            manifest, tasks = load_suite(sid)
        except FileNotFoundError:
            sc.add(ScoreRow(mode="rubric", skill_id=sid, status="SKIP", notes="suite not found"))
            continue

        suite_failures: list[str] = []
        for task in tasks:
            golden = task.get("golden_answer", "")
            status, failures = score_rubric_task(task, golden)
            if status == "FAIL":
                suite_failures.extend(f"task:{task.get('id', '?')}:{f}" for f in failures)

        status = "PASS" if not suite_failures else "FAIL"
        sc.add(
            ScoreRow(
                mode="rubric",
                skill_id=f"suite:{sid}",
                name=manifest.get("description", sid),
                status=status,
                failures=suite_failures[:5],
                notes=f"version={manifest.get('version', '?')}; reviewed={manifest.get('last_reviewed', '?')}",
            )
        )


def run_smoke(sc: Scorecard) -> None:
    """In-process probes — promoted from %TEMP%/madeira_uat_inproc.py.

    Verifies: env bootstrap, all 4 I32 mirror loads, classify_request, validator dispatcher.
    Pure-Python; no LLM call. ~5s on a warm machine.
    """
    try:
        from akos.io import bootstrap_openclaw_process_env

        bootstrap_openclaw_process_env()
        sc.add(ScoreRow(mode="smoke", skill_id="env_bootstrap", status="PASS"))
    except Exception as e:
        sc.add(
            ScoreRow(
                mode="smoke", skill_id="env_bootstrap", status="FAIL", failures=[f"{type(e).__name__}: {e}"]
            )
        )

    csv_checks = [
        ("SKILL_REGISTRY.csv", "akos.hlk_skill_registry_csv", "SKILL_REGISTRY_FIELDNAMES", 5),
        (
            "TOUCHPOINT_KIT_CELL_REGISTRY.csv",
            "akos.hlk_touchpoint_kit_cell_csv",
            "TOUCHPOINT_KIT_CELL_FIELDNAMES",
            15,
        ),
        ("POLICY_REGISTER.csv", "akos.hlk_policy_register_csv", "POLICY_REGISTER_FIELDNAMES", 14),
        (
            "REPO_HEALTH_SNAPSHOT.csv",
            "akos.hlk_repo_health_csv",
            "REPO_HEALTH_SNAPSHOT_FIELDNAMES",
            3,
        ),
    ]
    for fname, mod_name, const_name, min_rows in csv_checks:
        try:
            mod = __import__(mod_name, fromlist=[const_name])
            fields = getattr(mod, const_name)
            if fname == "REPO_HEALTH_SNAPSHOT.csv":
                path = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / fname
            else:
                path = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / fname
            rows = list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))
            assert len(rows) >= min_rows, f"expected >={min_rows}, got {len(rows)}"
            missing = set(fields) - (set(rows[0].keys()) if rows else set())
            assert not missing, f"missing fields: {missing}"
            sc.add(
                ScoreRow(
                    mode="smoke",
                    skill_id=f"csv_load:{fname}",
                    status="PASS",
                    notes=f"{len(rows)} rows; {len(fields)} fields",
                )
            )
        except Exception as e:
            sc.add(
                ScoreRow(
                    mode="smoke",
                    skill_id=f"csv_load:{fname}",
                    status="FAIL",
                    failures=[f"{type(e).__name__}: {e}"],
                )
            )

    try:
        from akos.intent import classify_request

        out = classify_request("Need a quick lookup on Madeira's lore")
        ok = isinstance(out, dict) and ("route" in out or "agent_id" in out or "agent" in out)
        sc.add(
            ScoreRow(
                mode="smoke",
                skill_id="classify_request_smoke",
                status="PASS" if ok else "FAIL",
                notes=f"keys={list(out.keys())[:5]}" if isinstance(out, dict) else "",
            )
        )
    except Exception as e:
        sc.add(
            ScoreRow(
                mode="smoke",
                skill_id="classify_request_smoke",
                status="FAIL",
                failures=[f"{type(e).__name__}: {e}"],
            )
        )

    probes = [
        "Need a quick lookup on Madeira's lore",
        "Plan a 5-phase rollout for the new persona",
        "Run the test suite and report failures",
        "Verify the patch matches the spec",
        "Detect the language of this French paragraph",
    ]
    fallback = 0
    try:
        from akos.intent import classify_request

        for q in probes:
            r = classify_request(q)
            agent = r.get("agent_id") or r.get("agent") or r.get("route") or ""
            if "orchestrator" in str(agent).lower() and "fallback" in str(r).lower():
                fallback += 1
        sc.add(
            ScoreRow(
                mode="smoke",
                skill_id="intent_5_probes",
                status="PASS" if fallback == 0 else "FAIL",
                notes=f"orchestrator-fallback={fallback}/5 (canary 5)",
                failures=[f"orchestrator_fallback={fallback}"] if fallback else [],
            )
        )
    except Exception as e:
        sc.add(
            ScoreRow(
                mode="smoke",
                skill_id="intent_5_probes",
                status="FAIL",
                failures=[f"{type(e).__name__}: {e}"],
            )
        )


def run_adversarial(sc: Scorecard, *, skill_id: str | None = None) -> None:
    """Adversarial cassette replay (I45 P5). Walks
    tests/evals/cassettes/adversarial/<skill_id>/*.jsonl and runs each.
    """
    from akos.eval_harness.cassette import adversarial_cassettes, replay_cassette

    targets = adversarial_cassettes(skill_id=skill_id)
    if not targets:
        sc.add(
            ScoreRow(
                mode="adversarial",
                skill_id=skill_id or "__no_adversarial_cassettes__",
                status="SKIP",
                notes="no adversarial cassettes recorded yet",
            )
        )
        return

    for p in targets:
        sid = p.parent.name
        try:
            outcome = replay_cassette(p)
        except Exception as e:
            sc.add(
                ScoreRow(
                    mode="adversarial",
                    skill_id=sid,
                    status="FAIL",
                    failures=[f"{type(e).__name__}: {e}"],
                    notes=f"cassette={p.relative_to(REPO_ROOT)}",
                )
            )
            continue

        status = outcome.get("status", "FAIL")
        sc.add(
            ScoreRow(
                mode="adversarial",
                skill_id=sid,
                status=status if status in ("PASS", "FAIL", "SKIP", "WARN") else "FAIL",
                failures=list(outcome.get("failures", []) or []),
                notes=f"probe={p.stem}; route={outcome.get('actual_route', '?')}",
            )
        )


def run_replay(
    sc: Scorecard,
    *,
    skill_id: str | None = None,
    include_adversarial: bool = False,
) -> None:
    """Cassette replay (P2). Walks tests/evals/cassettes/<skill_id>/*.jsonl and
    asserts each cassette's recorded behavior still matches via the cassette
    module's classify_request or live_llm replay path.
    """
    from akos.eval_harness.cassette import (
        adversarial_cassettes,
        list_cassettes,
        replay_cassette,
    )

    targets = list_cassettes(skill_id=skill_id)
    if include_adversarial:
        targets += adversarial_cassettes(skill_id=skill_id)

    if not targets:
        sc.add(
            ScoreRow(
                mode="replay",
                skill_id=skill_id or "__no_cassettes__",
                status="SKIP",
                notes=f"no cassettes recorded yet for {skill_id or '<any skill>'}",
            )
        )
        return

    for p in targets:
        sid = p.parent.name
        try:
            outcome = replay_cassette(p)
        except Exception as e:
            sc.add(
                ScoreRow(
                    mode="replay",
                    skill_id=sid,
                    status="FAIL",
                    failures=[f"{type(e).__name__}: {e}"],
                    notes=f"cassette={p.relative_to(REPO_ROOT)}",
                )
            )
            continue

        status = outcome.get("status", "FAIL")
        sc.add(
            ScoreRow(
                mode="replay",
                skill_id=sid,
                status=status if status in ("PASS", "FAIL", "SKIP", "WARN") else "FAIL",
                failures=list(outcome.get("failures", []) or []),
                notes=(
                    f"probe={p.stem}; age={outcome.get('age_days', '?')}d; "
                    f"{outcome.get('stale', '?')}"
                ),
            )
        )


# ── Top-level dispatcher ──────────────────────────────────────────────────────


def run_modes(
    modes: list[str],
    *,
    suite_ids: list[str] | None = None,
    governance_only: bool = False,
    threshold_pp: float = 2.0,
    overrides: dict[str, float] | None = None,
    replay_skill: str | None = None,
    enforce_cost: bool = False,
) -> Scorecard:
    """Run one or more modes; return unified Scorecard."""
    sc = Scorecard()
    if "all" in modes:
        modes = ["smoke", "canary", "rubric"]  # replay is opt-in; not in default 'all'
    sc.modes_run = list(modes)

    t0 = time.perf_counter()
    if "smoke" in modes:
        run_smoke(sc)
    if "canary" in modes:
        run_canary(sc, threshold_pp=threshold_pp, overrides=overrides, enforce_cost=enforce_cost)
    if "rubric" in modes:
        run_rubric(sc, suite_ids=suite_ids, governance_only=governance_only)
    if "replay" in modes:
        run_replay(sc, skill_id=replay_skill)
    if "adversarial" in modes:
        run_adversarial(sc, skill_id=replay_skill)
    sc.elapsed_ms = int((time.perf_counter() - t0) * 1000)

    return sc
