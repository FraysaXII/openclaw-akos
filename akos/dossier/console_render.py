"""Initiative 48 — Operator Console (qualitative companion to dossier.html).

The standard ``dossier.html`` is metric-rich but qualitatively thin: it shows
counts and statuses but not WHAT was asked, WHAT the choices were, or WHERE
the testing actually lives. The Operator Console answers those questions in
a single standalone HTML page using the same brand SSOT and the same "no JS,
no CDN, no external fonts" invariant (D-IH-48-I; R-48-3).

Output: ``dossier-console.html`` written next to ``dossier.html`` whenever the
dossier renderer is asked for ``--format html`` or ``--format all``.

Panels (each is a self-contained brand card):

- A. Cover + run header + quick links to sibling dossier artifacts
- B. System status at-a-glance (12 section pills colored by status + counters)
- C. Trend small-multiples (4 sparklines drawn from artifacts/uat-dossier/index.json)
- D. Persona x difficulty scenario heatmap (PERSONA_SCENARIO_REGISTRY.csv)
- E. Scenario sample cards (8 representative scenarios: prompt, expected, skill, topic)
- F. Decisions taken across the last 3 initiatives (D-IH-46/47/48 decision-logs)
- G. Skill registry x retrieval mode x eval baseline (SKILL_REGISTRY.csv)
- H. Recent dossier runs timeline (last 10 entries from index.json with mini-bars)
- I. Cassette transcript samples (one per skill from tests/evals/cassettes/)

All chart primitives (donut, heatmap, pill, bar, card) are pure SVG/HTML/CSS.
Brand tokens reused from ``akos.hlk_pdf_render.BRAND_TOKENS_LIGHT`` (E9 SSOT;
drift caught by ``tests/test_render_dossier.py::test_brand_tokens_light_match_pattern_doc``).
"""

from __future__ import annotations

import csv
import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from akos.dossier.html_render import BRAND_CSS_VARS, _html_escape

logger = logging.getLogger("akos.dossier.console_render")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DIMENSIONS_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions"
PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"
CASSETTES_DIR = REPO_ROOT / "tests" / "evals" / "cassettes"
INDEX_JSON = REPO_ROOT / "artifacts" / "uat-dossier" / "index.json"

PERSONA_SCENARIO_CSV = DIMENSIONS_DIR / "PERSONA_SCENARIO_REGISTRY.csv"
SKILL_REGISTRY_CSV = DIMENSIONS_DIR / "SKILL_REGISTRY.csv"
PERSONA_REGISTRY_CSV = DIMENSIONS_DIR / "PERSONA_REGISTRY.csv"

# Difficulty + outcome ordering (visual axes) per I47 P1 contract.
DIFFICULTY_ORDER = ("trivial", "moderate", "hard", "impossible")
OUTCOME_BADGES = {
    "GROUND": ("hsl(168 55% 38%)", "GROUND"),
    "REFUSE": ("hsl(0 60% 45%)", "REFUSE"),
    "ESCALATE": ("hsl(35 90% 45%)", "ESCALATE"),
    "PARTIAL": ("hsl(220 8% 42%)", "PARTIAL"),
    "FALLBACK": ("hsl(220 8% 42%)", "FALLBACK"),
}
STATUS_BADGES = {
    "PASS": "hsl(168 55% 38%)",
    "FAIL": "hsl(0 65% 45%)",
    "WARN": "hsl(35 90% 45%)",
    "SKIP": "hsl(220 8% 60%)",
    "INFO": "hsl(220 35% 50%)",
}
REVERSIBILITY_BADGES = {
    "Trivial": "hsl(168 55% 38%)",
    "trivial": "hsl(168 55% 38%)",
    "Med": "hsl(35 90% 45%)",
    "med": "hsl(35 90% 45%)",
    "Medium": "hsl(35 90% 45%)",
    "High": "hsl(0 60% 45%)",
    "high": "hsl(0 60% 45%)",
    "Hard": "hsl(0 60% 45%)",
}


@dataclass
class _ScenarioRow:
    scenario_id: str
    persona_id: str
    skill_id: str
    tier: str
    scenario_class: str
    difficulty_class: str
    prompt_text: str
    expected_route: str
    expected_keywords: str
    forbidden_keywords: str
    expected_outcome_class: str
    language: str
    topic_ids: str
    notes: str


@dataclass
class _DecisionRow:
    initiative: str
    decision_id: str
    question: str
    decision: str
    reversibility: str


@dataclass
class _CassetteSample:
    skill_id: str
    probe_id: str
    probe_kind: str
    prompt: str
    final_route: str
    confidence: float
    status: str
    latency_ms: int


def render_console_html(
    run: Any,
    *,
    repo_root: Path | None = None,
    dossier_run_index_path: Path | None = None,
) -> str:
    """Render the Operator Console as a standalone HTML document.

    Args:
        run: a ``DossierRun`` with ``section_results`` populated.
        repo_root: optional override (default = repo root inferred from this file).
        dossier_run_index_path: optional override for the trend index JSON.

    Returns the full HTML document as a string. Standalone-file invariant per
    D-IH-48-I: no <script>, no remote URLs, no external fonts. The CSP meta
    matches dossier.html (default-src 'self' 'unsafe-inline').
    """
    rr = repo_root or REPO_ROOT
    idx_path = dossier_run_index_path or (rr / "artifacts" / "uat-dossier" / "index.json")

    panels: list[str] = []
    panels.append(_panel_a_cover(run))
    panels.append(_panel_b_status_at_a_glance(run))
    panels.append(_panel_c_trend_small_multiples(idx_path, run))
    panels.append(_panel_d_persona_heatmap(rr))
    panels.append(_panel_e_scenario_samples(rr, run))
    panels.append(_panel_f_decisions_taken(rr))
    panels.append(_panel_g_skill_registry(rr))
    panels.append(_panel_h_recent_runs(idx_path))
    panels.append(_panel_i_cassette_samples(rr))

    body = "\n".join(panels)
    css = _CONSOLE_CSS
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline'">
<title>AKOS Operator Console &mdash; {_html_escape(run.run_id)}</title>
<style>{css}</style>
</head>
<body>
<main class="console">
{body}
</main>
<footer>
Operator Console &middot; AKOS Initiative 48 &middot; Standalone (no JS / no CDN / no remote fonts)
&middot; companion to <code>dossier.html</code>
</footer>
</body>
</html>
"""


# -------------------------------------------------------------------------
# Panel A — cover + quick links
# -------------------------------------------------------------------------


def _panel_a_cover(run: Any) -> str:
    overall_color = STATUS_BADGES.get(run.overall_status, STATUS_BADGES["INFO"])
    filt_chips = []
    if getattr(run.filter, "initiative", None):
        filt_chips.append(_chip(f"initiative {run.filter.initiative}", "hsl(220 35% 50%)"))
    if getattr(run.filter, "persona_id", None):
        filt_chips.append(_chip(run.filter.persona_id, "hsl(168 55% 38%)"))
    if getattr(run.filter, "since", None):
        filt_chips.append(_chip(f"since {run.filter.since}", "hsl(220 8% 60%)"))
    filt_html = " ".join(filt_chips) if filt_chips else "<span class=\"muted\">no filter (full snapshot)</span>"
    return f"""
<section class="panel cover" id="panel-a">
  <div class="cover-band">
    <h1>AKOS Operator Console</h1>
    <p class="cover-sub">A visual companion to the UAT dossier. What ran, what was asked, what was decided.</p>
  </div>
  <dl class="cover-meta">
    <dt>run_id</dt><dd><code>{_html_escape(run.run_id)}</code></dd>
    <dt>started_at</dt><dd>{_html_escape(run.started_at)}</dd>
    <dt>git_sha</dt><dd><code>{_html_escape(run.git_sha)}</code></dd>
    <dt>mode</dt><dd><strong>{_html_escape(run.mode)}</strong></dd>
    <dt>overall</dt><dd><span class="badge" style="background:{overall_color}">{_html_escape(run.overall_status)}</span></dd>
    <dt>elapsed</dt><dd>{run.elapsed_ms} ms</dd>
    <dt>filter</dt><dd>{filt_html}</dd>
  </dl>
  <p class="quicklinks">
    Sibling artifacts:
    <a href="dossier.html">dossier.html</a> &middot;
    <a href="dossier.pdf">dossier.pdf</a> &middot;
    <a href="dossier.md">dossier.md</a> &middot;
    <a href="manifest.json">manifest.json</a>
  </p>
</section>
"""


# -------------------------------------------------------------------------
# Panel B — system status at-a-glance
# -------------------------------------------------------------------------


def _panel_b_status_at_a_glance(run: Any) -> str:
    pills = []
    counts: dict[str, int] = {}
    for r in sorted(run.section_results, key=lambda x: x.section_id):
        color = STATUS_BADGES.get(r.status, STATUS_BADGES["INFO"])
        age = ""
        if r.data_age_seconds is not None:
            hrs = r.data_age_seconds / 3600.0
            age = f"<span class=\"age\">{hrs:.1f}h</span>"
        counts[r.status] = counts.get(r.status, 0) + 1
        pills.append(
            f'<a class="status-pill" href="dossier.html#section-{r.section_id:02d}" '
            f'style="border-left-color:{color}">'
            f'<span class="num">{r.section_id:02d}</span>'
            f'<span class="name">{_html_escape(r.name)}</span>'
            f'<span class="badge" style="background:{color}">{_html_escape(r.status)}</span>'
            f'{age}'
            f"</a>"
        )
    counter_chips = " ".join(
        f'<span class="counter" style="border-color:{STATUS_BADGES.get(k, STATUS_BADGES["INFO"])}">'
        f'<strong>{v}</strong> {_html_escape(k)}</span>'
        for k, v in counts.items()
    )
    return f"""
<section class="panel" id="panel-b">
  <h2>B &middot; System status at-a-glance</h2>
  <p class="lead">12 sections, one tile each. Click a tile to jump into the full dossier section.</p>
  <div class="counters">{counter_chips}</div>
  <div class="status-grid">
{chr(10).join(pills)}
  </div>
</section>
"""


# -------------------------------------------------------------------------
# Panel C — trend small-multiples
# -------------------------------------------------------------------------


def _panel_c_trend_small_multiples(idx_path: Path, run: Any) -> str:
    runs = _load_index_runs(idx_path)
    if len(runs) < 2:
        return f"""
<section class="panel" id="panel-c">
  <h2>C &middot; Trend small-multiples</h2>
  <p class="muted">INSUFFICIENT-DATA: need &ge;2 dossier runs in <code>artifacts/uat-dossier/index.json</code>;
  currently {len(runs)}. Each new dossier run appends a row; sparklines appear automatically once two are present.</p>
</section>
"""
    series = _extract_trend_series(runs, last_n=20)
    cards = []
    for label, data, fmt in series:
        cards.append(
            f'<div class="mini-card">'
            f'<div class="mini-title">{_html_escape(label)}</div>'
            f"{_full_sparkline_svg(data, label=label, value_fmt=fmt)}"
            f'<div class="mini-foot">first <strong>{fmt(data[0])}</strong> &middot; '
            f'last <strong>{fmt(data[-1])}</strong> &middot; '
            f'n=<strong>{len(data)}</strong></div>'
            f'</div>'
        )
    return f"""
<section class="panel" id="panel-c">
  <h2>C &middot; Trend small-multiples (last {len(runs)} dossier runs)</h2>
  <p class="lead">Each card draws from <code>artifacts/uat-dossier/index.json</code>: an offline trend cache
  appended on every dossier render.</p>
  <div class="mini-grid">
{chr(10).join(cards)}
  </div>
</section>
"""


# -------------------------------------------------------------------------
# Panel D — persona x difficulty heatmap
# -------------------------------------------------------------------------


def _panel_d_persona_heatmap(rr: Path) -> str:
    csv_path = rr / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"
    rows = _read_scenario_csv(csv_path)
    if not rows:
        return f"""
<section class="panel" id="panel-d">
  <h2>D &middot; Persona &times; difficulty heatmap</h2>
  <p class="muted">PERSONA_SCENARIO_REGISTRY.csv unavailable.</p>
</section>
"""
    matrix: dict[str, dict[str, int]] = {}
    persona_totals: dict[str, int] = {}
    diff_totals: dict[str, int] = {d: 0 for d in DIFFICULTY_ORDER}
    grand_total = 0
    for r in rows:
        matrix.setdefault(r.persona_id, {d: 0 for d in DIFFICULTY_ORDER})
        d = r.difficulty_class if r.difficulty_class in DIFFICULTY_ORDER else "moderate"
        matrix[r.persona_id][d] = matrix[r.persona_id].get(d, 0) + 1
        persona_totals[r.persona_id] = persona_totals.get(r.persona_id, 0) + 1
        diff_totals[d] = diff_totals.get(d, 0) + 1
        grand_total += 1
    personas_sorted = sorted(matrix.keys(), key=lambda p: (-persona_totals.get(p, 0), p))
    max_cell = max((matrix[p][d] for p in personas_sorted for d in DIFFICULTY_ORDER), default=1)
    rows_html: list[str] = []
    for p in personas_sorted:
        cells_html = []
        for d in DIFFICULTY_ORDER:
            v = matrix[p].get(d, 0)
            bg = _heatmap_color(v, max_cell)
            txt = "&nbsp;" if v == 0 else str(v)
            cells_html.append(
                f'<td class="cell" style="background:{bg}" title="{_html_escape(p)} / {d} / {v} scenarios">{txt}</td>'
            )
        rows_html.append(
            f'<tr><th class="rowhead">{_html_escape(p)}</th>{"".join(cells_html)}'
            f'<td class="rowtotal"><strong>{persona_totals.get(p, 0)}</strong></td></tr>'
        )
    cols_total_html = "".join(f"<td class=\"coltotal\"><strong>{diff_totals[d]}</strong></td>" for d in DIFFICULTY_ORDER)
    head_html = "".join(f'<th class="colhead">{_html_escape(d)}</th>' for d in DIFFICULTY_ORDER)
    return f"""
<section class="panel" id="panel-d">
  <h2>D &middot; Persona &times; difficulty heatmap</h2>
  <p class="lead">Where the <strong>{grand_total}</strong> governed scenarios live.
  Darker = more scenarios. Cells are linked to the persona &times; difficulty axis from PERSONA_SCENARIO_REGISTRY.csv.</p>
  <table class="heatmap">
    <thead><tr><th>persona</th>{head_html}<th>total</th></tr></thead>
    <tbody>
{chr(10).join(rows_html)}
      <tr><th class="rowhead">total</th>{cols_total_html}<td class="rowtotal"><strong>{grand_total}</strong></td></tr>
    </tbody>
  </table>
</section>
"""


# -------------------------------------------------------------------------
# Panel E — scenario sample cards
# -------------------------------------------------------------------------


def _panel_e_scenario_samples(rr: Path, run: Any) -> str:
    csv_path = rr / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"
    rows = _read_scenario_csv(csv_path)
    if not rows:
        return ""
    persona_filter = getattr(run.filter, "persona_id", None) or ""
    if persona_filter:
        rows = [r for r in rows if r.persona_id == persona_filter] or rows
    samples = _pick_diverse_samples(rows, n=8)
    cards = [_scenario_card_html(s) for s in samples]
    title = "E &middot; Scenario samples"
    if persona_filter:
        title += f" &middot; filtered to <code>{_html_escape(persona_filter)}</code>"
    return f"""
<section class="panel" id="panel-e">
  <h2>{title}</h2>
  <p class="lead">A diversified sample (across tiers, skills, outcome classes) drawn from PERSONA_SCENARIO_REGISTRY.csv.
  Each card shows the prompt the system saw, what it should have done, and where the evidence lives.</p>
  <div class="card-grid">
{chr(10).join(cards)}
  </div>
</section>
"""


# -------------------------------------------------------------------------
# Panel F — decisions taken (last 3 initiatives)
# -------------------------------------------------------------------------


def _panel_f_decisions_taken(rr: Path) -> str:
    initiatives = ["48-operator-dossier", "47-user-centric-uat", "46-neo4j-strategic-posture"]
    decisions: list[_DecisionRow] = []
    for slug in initiatives:
        path = rr / "docs" / "wip" / "planning" / slug / "decision-log.md"
        decisions.extend(_parse_decision_log(path, slug))
    decisions = decisions[:24]
    if not decisions:
        return f"""
<section class="panel" id="panel-f">
  <h2>F &middot; Decisions taken</h2>
  <p class="muted">No parseable decision-logs found.</p>
</section>
"""
    rows_html = []
    for d in decisions:
        rev_color = REVERSIBILITY_BADGES.get(d.reversibility, "hsl(220 8% 60%)")
        rows_html.append(
            f'<tr>'
            f'<td><code>{_html_escape(d.decision_id)}</code></td>'
            f'<td>{_html_escape(d.question)}</td>'
            f'<td><strong>{_html_escape(d.decision)}</strong></td>'
            f'<td><span class="badge" style="background:{rev_color}">{_html_escape(d.reversibility)}</span></td>'
            f'<td><a href="https://github.com/FraysaXII/openclaw-akos/blob/main/docs/wip/planning/{_html_escape(d.initiative)}/decision-log.md">i{_html_escape(d.initiative.split("-")[0])}</a></td>'
            f'</tr>'
        )
    return f"""
<section class="panel" id="panel-f">
  <h2>F &middot; Decisions taken (last 3 initiatives)</h2>
  <p class="lead">What choices were made and how reversible they are.
  Trivial = flip a flag &middot; Med = needs migration &middot; High = touches contracts.</p>
  <table class="decisions">
    <thead><tr><th>id</th><th>question</th><th>decision</th><th>reversibility</th><th>initiative</th></tr></thead>
    <tbody>
{chr(10).join(rows_html)}
    </tbody>
  </table>
</section>
"""


# -------------------------------------------------------------------------
# Panel G — skill registry visual
# -------------------------------------------------------------------------


def _panel_g_skill_registry(rr: Path) -> str:
    csv_path = rr / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
    if not csv_path.is_file():
        return ""
    try:
        with csv_path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            skills = list(reader)
    except OSError:
        return ""
    if not skills:
        return ""
    rows_html = []
    for s in skills:
        skill_id = s.get("skill_id", "")
        owner = s.get("owner_role", "") or s.get("agent_id", "")
        rmode = (s.get("retrieval_mode") or "(empty)").strip() or "(empty)"
        baseline = (s.get("eval_baseline_pct") or "").strip()
        try:
            pct = float(baseline) if baseline else 0.0
        except ValueError:
            pct = 0.0
        bar = _hbar_html(pct, max_value=100.0, color="hsl(168 55% 38%)")
        rmode_color = "hsl(220 8% 88%)" if rmode == "(empty)" else "hsl(168 30% 80%)"
        rows_html.append(
            f'<tr>'
            f'<td><code>{_html_escape(skill_id)}</code></td>'
            f'<td>{_html_escape(owner)}</td>'
            f'<td><span class="chip" style="background:{rmode_color}">{_html_escape(rmode)}</span></td>'
            f'<td class="bar-cell">{bar}<span class="bar-label">{_html_escape(baseline) or "&mdash;"}</span></td>'
            f'</tr>'
        )
    return f"""
<section class="panel" id="panel-g">
  <h2>G &middot; Skill registry</h2>
  <p class="lead">{len(skills)} governed skills. <code>retrieval_mode</code> stays empty for skills that don&apos;t need
  vector or graph search; the column was added in I46 P5 to gate GraphRAG eligibility.</p>
  <table class="skills">
    <thead><tr><th>skill</th><th>owner role</th><th>retrieval mode</th><th>eval baseline pct</th></tr></thead>
    <tbody>
{chr(10).join(rows_html)}
    </tbody>
  </table>
</section>
"""


# -------------------------------------------------------------------------
# Panel H — recent dossier runs
# -------------------------------------------------------------------------


def _panel_h_recent_runs(idx_path: Path) -> str:
    runs = _load_index_runs(idx_path)
    if not runs:
        return f"""
<section class="panel" id="panel-h">
  <h2>H &middot; Recent dossier runs</h2>
  <p class="muted">No runs in <code>artifacts/uat-dossier/index.json</code> yet.</p>
</section>
"""
    last_n = runs[-10:]
    eval_max = max((r.get("rollup", {}).get("eval_pass_rate", 0.0) or 0.0) for r in last_n) or 1.0
    rows_html = []
    for r in last_n:
        ts = r.get("started_at", "")
        mode = r.get("mode", "")
        ru = r.get("rollup", {}) or {}
        eval_pct = float(ru.get("eval_pass_rate") or 0.0) * 100.0
        cost = float(ru.get("cost_total_usd") or 0.0)
        drift = int(ru.get("drift_canary_total") or 0)
        bar = _hbar_html(eval_pct, max_value=max(eval_max * 100.0, 1.0), color="hsl(168 55% 38%)")
        mode_color = "hsl(220 35% 50%)" if mode == "snapshot" else ("hsl(35 90% 45%)" if mode == "live" else "hsl(0 60% 45%)")
        rows_html.append(
            f'<tr>'
            f'<td>{_html_escape(_human_ago(ts))}</td>'
            f'<td><span class="badge" style="background:{mode_color}">{_html_escape(mode)}</span></td>'
            f'<td class="bar-cell">{bar}<span class="bar-label">{eval_pct:.1f}%</span></td>'
            f'<td>{drift}</td>'
            f'<td>${cost:.4f}</td>'
            f'<td><code>{_html_escape((r.get("git_sha") or "")[:8])}</code></td>'
            f'</tr>'
        )
    return f"""
<section class="panel" id="panel-h">
  <h2>H &middot; Recent dossier runs</h2>
  <p class="lead">Last {len(last_n)} runs from the local trend cache. Eval pass rate bars are scaled to the local max.</p>
  <table class="runs">
    <thead><tr><th>when</th><th>mode</th><th>eval pass</th><th>drift</th><th>cost</th><th>git_sha</th></tr></thead>
    <tbody>
{chr(10).join(rows_html)}
    </tbody>
  </table>
</section>
"""


# -------------------------------------------------------------------------
# Panel I — cassette transcript samples
# -------------------------------------------------------------------------


def _panel_i_cassette_samples(rr: Path) -> str:
    cassettes_dir = rr / "tests" / "evals" / "cassettes"
    if not cassettes_dir.is_dir():
        return ""
    samples: list[_CassetteSample] = []
    for skill_dir in sorted(p for p in cassettes_dir.iterdir() if p.is_dir() and p.name.startswith("SKILL-")):
        for jsonl in sorted(skill_dir.glob("*.jsonl")):
            sample = _parse_cassette(jsonl)
            if sample:
                samples.append(sample)
                break
    samples = samples[:6]
    if not samples:
        return ""
    cards = []
    for s in samples:
        confidence_pct = max(0.0, min(1.0, s.confidence)) * 100.0
        bar = _hbar_html(confidence_pct, max_value=100.0, color="hsl(168 55% 38%)")
        status_color = STATUS_BADGES.get(s.status, STATUS_BADGES["INFO"])
        cards.append(f"""
<div class="cassette">
  <div class="cassette-head">
    <code>{_html_escape(s.skill_id)}</code>
    <span class="muted">/{_html_escape(s.probe_id)}</span>
    <span class="chip">{_html_escape(s.probe_kind)}</span>
    <span class="badge" style="background:{status_color}">{_html_escape(s.status)}</span>
    <span class="muted">{s.latency_ms} ms</span>
  </div>
  <div class="cassette-prompt"><strong>prompt</strong> &middot; {_html_escape(s.prompt)}</div>
  <div class="cassette-final">
    <strong>final route</strong> &middot; <code>{_html_escape(s.final_route)}</code>
    <span class="bar-inline" style="margin-left:0.6em">{bar}<span class="bar-label">{confidence_pct:.0f}%</span></span>
  </div>
</div>""")
    return f"""
<section class="panel" id="panel-i">
  <h2>I &middot; Cassette transcript samples</h2>
  <p class="lead">One recorded probe per skill. The full set lives at
  <code>tests/evals/cassettes/&lt;skill_id&gt;/*.jsonl</code> and is replayed on every <code>--mode live</code> eval run.</p>
  <div class="cassettes">
{chr(10).join(cards)}
  </div>
</section>
"""


# -------------------------------------------------------------------------
# Helpers — chart primitives + parsers
# -------------------------------------------------------------------------


def _heatmap_color(v: int, max_v: int) -> str:
    if max_v <= 0 or v <= 0:
        return "hsl(220 8% 96%)"
    ratio = v / max_v
    lightness = max(35, 90 - int(ratio * 55))
    return f"hsl(168 55% {lightness}%)"


def _hbar_html(value: float, *, max_value: float = 100.0, color: str = "hsl(168 55% 38%)", width_px: int = 80) -> str:
    if max_value <= 0:
        max_value = 1.0
    pct = max(0.0, min(1.0, value / max_value))
    return (
        f'<span class="hbar" style="display:inline-block;width:{width_px}px;height:8px;'
        f'background:hsl(220 8% 92%);border-radius:4px;vertical-align:middle">'
        f'<span style="display:inline-block;height:100%;width:{pct * 100.0:.1f}%;'
        f'background:{color};border-radius:4px"></span></span>'
    )


def _chip(text: str, color: str) -> str:
    return f'<span class="chip" style="background:{color};color:white">{_html_escape(text)}</span>'


def _full_sparkline_svg(values: Sequence[float], *, label: str, value_fmt) -> str:
    width = 280
    height = 80
    pad_x = 8
    pad_y = 12
    inner_w = width - 2 * pad_x
    inner_h = height - 2 * pad_y
    floats = [float(v) for v in values]
    n = len(floats)
    if n < 2:
        return ""
    vmin = min(floats)
    vmax = max(floats)
    span = vmax - vmin
    if span == 0:
        norm = [0.5] * n
    else:
        norm = [(v - vmin) / span for v in floats]
    points = []
    for i, nv in enumerate(norm):
        x = pad_x + (i / (n - 1)) * inner_w
        y = pad_y + (1.0 - nv) * inner_h
        points.append((round(x, 2), round(y, 2)))
    polyline = " ".join(f"{x},{y}" for x, y in points)
    area_pts = f"{points[0][0]},{height - pad_y} " + " ".join(f"{x},{y}" for x, y in points) + f" {points[-1][0]},{height - pad_y}"
    end_x, end_y = points[-1]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{_html_escape(label)}">'
        f'<polygon points="{area_pts}" fill="hsl(168 55% 92%)" opacity="0.6"/>'
        f'<line x1="{pad_x}" y1="{height - pad_y}" x2="{width - pad_x}" y2="{height - pad_y}" stroke="hsl(220 8% 88%)" stroke-width="0.5"/>'
        f'<polyline points="{polyline}" fill="none" stroke="hsl(168 55% 38%)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{end_x}" cy="{end_y}" r="3" fill="hsl(168 55% 38%)"/>'
        f"</svg>"
    )


def _read_scenario_csv(csv_path: Path) -> list[_ScenarioRow]:
    if not csv_path.is_file():
        return []
    out: list[_ScenarioRow] = []
    try:
        with csv_path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                out.append(_ScenarioRow(
                    scenario_id=row.get("scenario_id", "").strip(),
                    persona_id=row.get("persona_id", "").strip(),
                    skill_id=row.get("skill_id", "").strip(),
                    tier=row.get("tier", "").strip(),
                    scenario_class=row.get("scenario_class", "").strip(),
                    difficulty_class=row.get("difficulty_class", "").strip(),
                    prompt_text=row.get("prompt_text", "").strip(),
                    expected_route=row.get("expected_route", "").strip(),
                    expected_keywords=row.get("expected_keywords", "").strip(),
                    forbidden_keywords=row.get("forbidden_keywords", "").strip(),
                    expected_outcome_class=row.get("expected_outcome_class", "").strip(),
                    language=row.get("language", "").strip(),
                    topic_ids=row.get("topic_ids", "").strip(),
                    notes=row.get("notes", "").strip(),
                ))
    except OSError as exc:
        logger.warning("scenario csv unreadable: %s", exc)
    return out


def _pick_diverse_samples(rows: list[_ScenarioRow], *, n: int = 8) -> list[_ScenarioRow]:
    """Pick scenarios across (tier, outcome_class) to maximise diversity.

    Deterministic: scenarios are sorted by scenario_id ascending; first match
    in each (tier, outcome) bucket wins until ``n`` is reached.
    """
    seen: set[tuple[str, str]] = set()
    picked: list[_ScenarioRow] = []
    for r in sorted(rows, key=lambda x: x.scenario_id):
        key = (r.tier or "?", r.expected_outcome_class or "?")
        if key in seen:
            continue
        seen.add(key)
        picked.append(r)
        if len(picked) >= n:
            return picked
    if len(picked) < n:
        for r in sorted(rows, key=lambda x: x.scenario_id):
            if r in picked:
                continue
            picked.append(r)
            if len(picked) >= n:
                break
    return picked


def _scenario_card_html(s: _ScenarioRow) -> str:
    outcome_color, outcome_label = OUTCOME_BADGES.get(s.expected_outcome_class, ("hsl(220 8% 60%)", s.expected_outcome_class or "?"))
    topics_html = " ".join(
        f'<span class="topic-chip">{_html_escape(t.strip())}</span>'
        for t in (s.topic_ids or "").split(";") if t.strip()
    )
    forbidden_html = ""
    if s.forbidden_keywords:
        forbidden_html = (
            f'<div class="kw kw-forbidden"><strong>forbidden</strong> &middot; '
            f'{_html_escape(s.forbidden_keywords)}</div>'
        )
    expected_html = ""
    if s.expected_keywords:
        expected_html = (
            f'<div class="kw"><strong>expected keywords</strong> &middot; '
            f'{_html_escape(s.expected_keywords)}</div>'
        )
    notes_html = ""
    if s.notes:
        notes_html = f'<div class="notes">{_html_escape(s.notes)}</div>'
    return f"""
<article class="scenario">
  <header>
    <code class="scn-id">{_html_escape(s.scenario_id)}</code>
    <span class="chip persona">{_html_escape(s.persona_id)}</span>
    <span class="chip diff">tier {_html_escape(s.tier)} &middot; {_html_escape(s.difficulty_class)}</span>
    <span class="badge" style="background:{outcome_color}">{_html_escape(outcome_label)}</span>
  </header>
  <div class="prompt">{_html_escape(s.prompt_text)}</div>
  <div class="meta">
    <span class="chip skill">{_html_escape(s.skill_id)}</span>
    <span class="chip route">route &rarr; <code>{_html_escape(s.expected_route)}</code></span>
    <span class="chip lang">{_html_escape(s.language)}</span>
  </div>
  {expected_html}
  {forbidden_html}
  <div class="topics">{topics_html}</div>
  {notes_html}
</article>
"""


_DECISION_HEADER_RE = re.compile(r"^##\s+(D-IH-\d+-[A-Z][A-Z0-9]*)\s+(?:[-—]\s+)?(.*)$")
_DECISION_FIELD_RE = re.compile(r"^\*\*(?P<key>Decision|Reversibility)[:\s]\*\*\s*(?P<val>.*)$", re.IGNORECASE)


def _parse_decision_log(path: Path, slug: str) -> list[_DecisionRow]:
    if not path.is_file():
        return []
    out: list[_DecisionRow] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    blocks = re.split(r"\n(?=##\s+D-IH-)", text)
    for block in blocks:
        first_line, _, rest = block.partition("\n")
        m = _DECISION_HEADER_RE.match(first_line.strip())
        if not m:
            continue
        decision_id = m.group(1).strip()
        question = m.group(2).strip()
        decision_text = ""
        reversibility = ""
        for line in rest.splitlines():
            f = _DECISION_FIELD_RE.match(line.strip())
            if f:
                key = f.group("key").lower()
                val = f.group("val").strip().rstrip(".")
                if key == "decision" and not decision_text:
                    decision_text = re.sub(r"\s+", " ", val)[:160]
                elif key == "reversibility" and not reversibility:
                    reversibility = val.split()[0] if val else ""
        out.append(_DecisionRow(
            initiative=slug,
            decision_id=decision_id,
            question=question[:200],
            decision=decision_text or "(see decision-log)",
            reversibility=reversibility or "?",
        ))
    return out


def _parse_cassette(jsonl_path: Path) -> _CassetteSample | None:
    if not jsonl_path.is_file():
        return None
    try:
        lines = [json.loads(l) for l in jsonl_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    except (OSError, json.JSONDecodeError):
        return None
    if not lines:
        return None
    header = next((e for e in lines if e.get("event") == "header"), {})
    prompt = next((e.get("text", "") for e in lines if e.get("event") == "prompt"), "")
    final = next((e for e in lines if e.get("event") == "final"), {})
    summary = next((e for e in lines if e.get("event") == "summary"), {})
    return _CassetteSample(
        skill_id=header.get("skill_id", ""),
        probe_id=header.get("probe_id", ""),
        probe_kind=header.get("probe_kind", ""),
        prompt=prompt[:240],
        final_route=str(final.get("route") or final.get("decision") or "?"),
        confidence=float(final.get("confidence") or 0.0),
        status=summary.get("status", ""),
        latency_ms=int(summary.get("latency_ms") or 0),
    )


def _load_index_runs(idx_path: Path) -> list[dict[str, Any]]:
    if not idx_path.is_file():
        return []
    try:
        data = json.loads(idx_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    runs = data.get("runs") if isinstance(data, dict) else None
    return runs or []


def _extract_trend_series(runs: list[dict[str, Any]], *, last_n: int = 20):
    pick = runs[-last_n:]

    def fmt_pct(v):
        return f"{float(v) * 100.0:.1f}%"

    def fmt_int(v):
        return str(int(v))

    def fmt_usd(v):
        return f"${float(v):.4f}"

    return [
        ("eval pass rate", [r.get("rollup", {}).get("eval_pass_rate", 0.0) or 0.0 for r in pick], fmt_pct),
        ("calibration ok", [r.get("rollup", {}).get("calibration_ok", 0.0) or 0.0 for r in pick], fmt_pct),
        ("drift canary total", [r.get("rollup", {}).get("drift_canary_total", 0) or 0 for r in pick], fmt_int),
        ("eval cost (USD)", [r.get("rollup", {}).get("cost_total_usd", 0.0) or 0.0 for r in pick], fmt_usd),
    ]


def _human_ago(ts: str) -> str:
    if not ts:
        return "?"
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return ts
    now = datetime.now(timezone.utc)
    delta = now - dt
    secs = int(delta.total_seconds())
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


# -------------------------------------------------------------------------
# CSS — single block, brand SSOT, no JS
# -------------------------------------------------------------------------


_CONSOLE_CSS = f"""
{BRAND_CSS_VARS}

* {{ box-sizing: border-box; }}
html {{ font-size: 15px; }}
body {{
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--c-background);
  color: var(--c-foreground);
  margin: 0;
  padding: 0 1.25rem 3rem;
  line-height: 1.55;
}}
main.console {{
  max-width: 1180px;
  margin: 1.5rem auto;
  display: grid;
  gap: 1.25rem;
}}
.panel {{
  background: var(--c-card);
  border: 1px solid var(--c-border);
  border-radius: 0.6rem;
  padding: 1.25rem 1.5rem;
}}
.panel h2 {{
  margin: 0 0 0.4rem 0;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--c-accent-primary);
}}
.panel p.lead {{
  margin: 0 0 1rem 0;
  color: var(--c-muted-foreground);
  font-size: 0.92rem;
}}
.panel p.muted, .muted {{ color: var(--c-muted-foreground); font-style: italic; }}

/* Cover */
.cover {{ padding: 0; overflow: hidden; }}
.cover .cover-band {{
  background: linear-gradient(135deg, var(--c-accent-primary) 0%, hsl(168 55% 30%) 100%);
  color: white;
  padding: 1.6rem 1.75rem;
}}
.cover .cover-band h1 {{ margin: 0; font-size: 1.7rem; font-weight: 700; }}
.cover .cover-sub {{ margin: 0.3rem 0 0 0; opacity: 0.92; font-size: 0.95rem; }}
.cover dl.cover-meta {{
  display: grid; grid-template-columns: max-content 1fr max-content 1fr; gap: 0.4rem 1.25rem;
  padding: 1.1rem 1.75rem 0;
}}
.cover dl.cover-meta dt {{ color: var(--c-muted-foreground); font-weight: 500; }}
.cover dl.cover-meta dd {{ margin: 0; }}
.cover .quicklinks {{
  padding: 0.75rem 1.75rem 1.2rem;
  margin: 0;
  color: var(--c-muted-foreground);
  font-size: 0.9rem;
}}
.cover .quicklinks a {{ color: var(--c-accent-primary); text-decoration: none; font-weight: 500; }}
.cover .quicklinks a:hover {{ text-decoration: underline; }}

/* Status pills */
.counters {{ margin: 0 0 0.8rem 0; display: flex; flex-wrap: wrap; gap: 0.4rem; }}
.counter {{
  display: inline-block; padding: 0.15rem 0.5rem;
  border: 1px solid hsl(220 8% 80%); border-left-width: 4px;
  border-radius: 0.25rem; font-size: 0.85rem; background: white;
}}
.status-grid {{ display: grid; gap: 0.5rem; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }}
.status-pill {{
  display: flex; align-items: center; gap: 0.5rem; padding: 0.45rem 0.75rem;
  background: white; border: 1px solid var(--c-border); border-left: 4px solid var(--c-accent-primary);
  border-radius: 0.4rem; text-decoration: none; color: var(--c-foreground); font-size: 0.88rem;
  transition: transform 0.06s;
}}
.status-pill:hover {{ transform: translateX(2px); border-color: var(--c-accent-primary); }}
.status-pill .num {{ font-family: 'Fira Code', Consolas, monospace; color: var(--c-muted-foreground); font-size: 0.82rem; }}
.status-pill .name {{ flex: 1; }}
.status-pill .age {{ color: var(--c-muted-foreground); font-size: 0.78rem; }}

.badge {{
  display: inline-block; padding: 0.1rem 0.45rem;
  border-radius: 0.25rem; color: white; font-size: 0.75rem;
  font-weight: 600; letter-spacing: 0.02em;
}}
.chip {{
  display: inline-block; padding: 0.08rem 0.4rem;
  background: hsl(220 8% 92%); border-radius: 0.25rem;
  font-size: 0.78rem; font-family: 'Fira Code', Consolas, monospace;
  color: var(--c-foreground);
}}

/* Mini cards (trend) */
.mini-grid {{ display: grid; gap: 0.9rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
.mini-card {{ background: white; border: 1px solid var(--c-border); border-radius: 0.4rem; padding: 0.75rem; }}
.mini-title {{ font-weight: 600; margin-bottom: 0.3rem; color: var(--c-foreground); }}
.mini-foot {{ font-size: 0.78rem; color: var(--c-muted-foreground); margin-top: 0.2rem; }}

/* Heatmap */
table.heatmap {{ border-collapse: collapse; font-size: 0.85rem; width: 100%; max-width: 720px; }}
table.heatmap th, table.heatmap td {{ padding: 0.3rem 0.45rem; text-align: center; border: 1px solid var(--c-border); }}
table.heatmap th.colhead, table.heatmap th.rowhead {{ background: hsl(220 8% 95%); text-transform: uppercase; letter-spacing: 0.04em; font-size: 0.7rem; }}
table.heatmap th.rowhead {{ text-align: left; font-family: 'Fira Code', Consolas, monospace; font-weight: 500; }}
table.heatmap td.cell {{ font-weight: 600; min-width: 56px; }}
table.heatmap td.rowtotal, table.heatmap td.coltotal {{ background: hsl(220 8% 95%); }}

/* Scenario cards */
.card-grid {{ display: grid; gap: 0.85rem; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); }}
article.scenario {{
  background: white; border: 1px solid var(--c-border); border-radius: 0.5rem;
  padding: 0.85rem 1rem; display: flex; flex-direction: column; gap: 0.45rem;
}}
article.scenario header {{ display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; }}
article.scenario .scn-id {{ font-size: 0.78rem; color: var(--c-muted-foreground); margin-right: 0.4rem; }}
article.scenario .prompt {{
  background: hsl(220 8% 96%); border-left: 3px solid var(--c-accent-primary);
  padding: 0.5rem 0.7rem; border-radius: 0 0.3rem 0.3rem 0; font-style: italic;
  color: var(--c-foreground);
}}
article.scenario .meta {{ display: flex; flex-wrap: wrap; gap: 0.35rem; font-size: 0.8rem; }}
article.scenario .kw {{ font-size: 0.78rem; color: var(--c-muted-foreground); }}
article.scenario .kw-forbidden strong {{ color: hsl(0 60% 45%); }}
article.scenario .topics {{ display: flex; flex-wrap: wrap; gap: 0.25rem; }}
article.scenario .topic-chip {{
  background: hsl(168 55% 92%); color: hsl(168 55% 25%);
  font-size: 0.72rem; padding: 0.05rem 0.4rem; border-radius: 0.2rem;
  font-family: 'Fira Code', Consolas, monospace;
}}
article.scenario .notes {{ font-size: 0.78rem; color: var(--c-muted-foreground); font-style: italic; }}

/* Decisions table */
table.decisions, table.skills, table.runs {{
  border-collapse: collapse; width: 100%; font-size: 0.88rem;
}}
table.decisions th, table.decisions td,
table.skills th, table.skills td,
table.runs th, table.runs td {{
  padding: 0.45rem 0.6rem; text-align: left; border-bottom: 1px solid var(--c-border);
  vertical-align: middle;
}}
table.decisions th, table.skills th, table.runs th {{ background: hsl(220 8% 95%); font-weight: 600; }}
table.decisions tr:hover, table.skills tr:hover, table.runs tr:hover {{ background: hsl(168 55% 98%); }}

.bar-cell {{ white-space: nowrap; }}
.bar-label {{ margin-left: 0.4rem; font-size: 0.8rem; color: var(--c-muted-foreground); }}
.bar-inline {{ display: inline-block; vertical-align: middle; }}

/* Cassettes */
.cassettes {{ display: grid; gap: 0.7rem; }}
.cassette {{ background: white; border: 1px solid var(--c-border); border-radius: 0.4rem; padding: 0.7rem 0.95rem; }}
.cassette-head {{ display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; font-size: 0.85rem; margin-bottom: 0.3rem; }}
.cassette-prompt {{ background: hsl(220 8% 96%); padding: 0.4rem 0.6rem; border-radius: 0.3rem; font-size: 0.88rem; margin-bottom: 0.25rem; }}
.cassette-final {{ font-size: 0.85rem; }}

footer {{
  max-width: 1180px;
  margin: 1.5rem auto 0;
  padding: 1rem;
  text-align: center;
  color: var(--c-muted-foreground);
  font-size: 0.8rem;
  border-top: 1px solid var(--c-border);
}}

@media (prefers-color-scheme: dark) {{
  :root {{
    --c-background: hsl(220 16% 7%);
    --c-foreground: hsl(210 15% 90%);
    --c-card: hsl(220 14% 10%);
    --c-secondary: hsl(220 8% 15%);
    --c-border: hsl(220 8% 22%);
    --c-muted-foreground: hsl(220 8% 60%);
  }}
  .status-pill, .mini-card, article.scenario, .cassette, .counter {{ background: hsl(220 14% 12%); }}
  table.decisions th, table.skills th, table.runs th,
  table.heatmap th.colhead, table.heatmap th.rowhead, table.heatmap td.rowtotal, table.heatmap td.coltotal {{ background: hsl(220 8% 17%); }}
  article.scenario .prompt, .cassette-prompt {{ background: hsl(220 8% 16%); }}
  article.scenario .topic-chip {{ background: hsl(168 55% 22%); color: hsl(168 55% 88%); }}
}}
"""

__all__ = ["render_console_html"]
