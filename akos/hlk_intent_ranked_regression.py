"""Pydantic SSOT for the Intent-Ranked Regression (FINANCE/I88, D-IH-88-F candidate).

The mechanical inter-wave regression (``akos/hlk_inter_wave_regression.py``) asks
*"is everything wired correctly?"* across 13 equal-ish dimensions. This module adds
the layer the operator asked for on 2026-06-05: *"is the thing I actually care about
most still served?"* — a **value-weighted** regression that ranks **what to check**
by how load-bearing each surface is to the operator's intents (past / present /
future), so scarce attention (operator or agent) lands on the highest-stakes
surfaces first.

External grounding (see reports/intent-ranked-regression-2026-06-05.md §research):
- **FMEA / Risk Priority Number** (Severity x Occurrence x Detection; severity-first
  override / Action-Priority tables) — Jama Software, SixSigma.us, testRigor 2026.
- **WSJF** (Cost of Delay = Business-Value + Time-Criticality + Risk-Reduction) —
  SAFe / Reinertsen; the right altitude for an *initiative-portfolio* regression.
- **Test Impact Analysis + Predictive Test Selection** — Microsoft Learn, Meta
  Engineering, Fowler: bound the candidate set by what changed, rank by
  fault-likelihood, keep the full sweep as a periodic safety net.

The Intent Criticality Score (ICS) is a WSJF/FMEA fusion:

    ICS = 3*intent_value + 2*time_criticality + 2*risk_reduction + 1*detection_gap

where ``detection_gap`` is FMEA Detection *inverted* (5 = no automated gate would
catch a regression on this surface; 1 = a strong always-on gate already does).
``severity_first`` is the FMEA Action-Priority override: a surface serving the
existence-critical intents (legal/fiscal or governance-integrity) with a known live
gap escalates to the front of the queue regardless of composite ICS.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# --- ICS weights (numerator only; WSJF job-duration deliberately omitted because
# "checking" duration is ~uniform across surfaces and the operator wants a
# depth-ordering, not an effort-economy — documented deviation in the report). ---
ICS_WEIGHTS: dict[str, int] = {
    "intent_value": 3,
    "time_criticality": 2,
    "risk_reduction": 2,
    "detection_gap": 1,
}
ICS_MAX = (
    ICS_WEIGHTS["intent_value"] * 5
    + ICS_WEIGHTS["time_criticality"] * 5
    + ICS_WEIGHTS["risk_reduction"] * 5
    + ICS_WEIGHTS["detection_gap"] * 5
)  # 40

VALID_TIER_IDS: frozenset[str] = frozenset(
    {f"IT-{n}" for n in range(1, 8)}
)


class IntentTier(BaseModel):
    """One operator-intent dimension, weighted by evidenced priority (1-5)."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    tier_id: str = Field(pattern=r"^IT-[1-7]$")
    name: str = Field(min_length=1, max_length=120)
    value: int = Field(ge=1, le=5)
    horizon: Literal["past", "present", "future", "all"]
    evidence: str = Field(min_length=1, max_length=512)


class RegressionSurface(BaseModel):
    """A checkable surface, scored for intent-ranked sweep ordering."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    surface_id: str = Field(pattern=r"^S-\d{2}$")
    name: str = Field(min_length=1, max_length=160)
    served_tiers: tuple[str, ...] = Field(min_length=1)
    time_criticality: int = Field(ge=1, le=5)
    risk_reduction: int = Field(ge=1, le=5)
    detection_gap: int = Field(ge=1, le=5)
    severity_first: bool = False
    probe_cmd: str = Field(default="", max_length=512)
    notes: str = Field(default="", max_length=512)

    def intent_value(self, tiers: dict[str, IntentTier]) -> int:
        return max(tiers[t].value for t in self.served_tiers)

    def ics(self, tiers: dict[str, IntentTier]) -> int:
        return (
            ICS_WEIGHTS["intent_value"] * self.intent_value(tiers)
            + ICS_WEIGHTS["time_criticality"] * self.time_criticality
            + ICS_WEIGHTS["risk_reduction"] * self.risk_reduction
            + ICS_WEIGHTS["detection_gap"] * self.detection_gap
        )


# --- The intent corpus, distilled from the internal sweep 2026-06-05 ---
# (operator-scratchpad "full-protocol" sessions; RICE-ranked OPERATOR_INBOX;
# USE_CASE_ARCHIVE commercial aspirations; OPS_REGISTER open severities;
# INITIATIVE_REGISTRY portfolio). Weights are evidenced, not invented.
INTENT_TIERS: tuple[IntentTier, ...] = (
    IntentTier(
        tier_id="IT-1", name="Commercial path to first revenue", value=5, horizon="future",
        evidence="USE_CASE_ARCHIVE (KiRBe SaaS, Websitz/Rushly partner delivery); I67 RevOps RICE 1920; PRICING_MODEL; Finance F2a rev-rec/pricing.",
    ),
    IntentTier(
        tier_id="IT-2", name="Legal / fiscal existence", value=5, horizon="present",
        evidence="I04 incorporation; I81 FINOPS planes 3-5 (OPS-81-13 'single most consequential'); OPS-66-1 trademark; ENISA.",
    ),
    IntentTier(
        tier_id="IT-3", name="Governance integrity / SSOT trust (the AKOS thesis)", value=5, horizon="all",
        evidence="validate_hlk; area-completeness matrix; inter-wave regression; D-IH-88-E; drift gates — the product IS a governed knowledge base.",
    ),
    IntentTier(
        tier_id="IT-4", name="Operator leverage, interaction quality & VISIBILITY", value=4, horizon="all",
        evidence="I76 MADEIRA; I62/64/65 operator surfaces; scratchpad L68 'getting lost on visibility - I don't know where/how/what it gives'; L1376 'ERP must not be forgotten... my dashboard'; two-seat AIC.",
    ),
    IntentTier(
        tier_id="IT-5", name="Brand & external credibility", value=4, horizon="present",
        evidence="I66 Brand sweep (RICE 2040/840); I85 audience tags; external-render discipline; investor briefs; company deck.",
    ),
    IntentTier(
        tier_id="IT-6", name="Evidence & quality discipline", value=3, horizon="all",
        evidence="I45-52 eval harness + judge roster; I47 333 persona scenarios; I84 research grounding; UAT discipline.",
    ),
    IntentTier(
        tier_id="IT-7", name="Runtime & deploy health", value=3, horizon="present",
        evidence="I87 OpenClaw runtime; I68 CICD; akos-deploy-health; fleet-hygiene sweep; sibling repos.",
    ),
)

INTENT_TIERS_BY_ID: dict[str, IntentTier] = {t.tier_id: t for t in INTENT_TIERS}

# --- Regression surfaces, mapped to intents + the mechanical probe that checks them ---
REGRESSION_SURFACES: tuple[RegressionSurface, ...] = (
    RegressionSurface(
        surface_id="S-01", name="Governance SSOT integrity (canonical CSVs + FK + frontmatter)",
        served_tiers=("IT-3",), time_criticality=4, risk_reduction=5, detection_gap=1,
        probe_cmd="py scripts/validate_hlk.py",
        notes="Strong always-on gate; high blast radius but well-detected.",
    ),
    RegressionSurface(
        surface_id="S-02", name="Area-completeness (Finance/Data + 5 areas)",
        served_tiers=("IT-3", "IT-1"), time_criticality=3, risk_reduction=4, detection_gap=2,
        probe_cmd="py scripts/validate_area_completeness.py --matrix",
    ),
    RegressionSurface(
        surface_id="S-03", name="Structural regression (decision lineage, pairing, carryover)",
        served_tiers=("IT-3",), time_criticality=2, risk_reduction=4, detection_gap=2,
        probe_cmd="py scripts/inter_wave_regression_sweep.py --self-test",
        notes="13-dimension mechanical sweep; the safety net this layer ranks on top of.",
    ),
    RegressionSurface(
        surface_id="S-04", name="FINOPS commercial substrate (rev-rec, pricing, tax, counterparty spine)",
        served_tiers=("IT-1", "IT-2"), time_criticality=5, risk_reduction=4, detection_gap=2,
        severity_first=True,
        probe_cmd="py scripts/dataops_quality_check.py --data-fam FINOPS-SPINE --data-surface mirror_table; py scripts/finops_monthly_recon.py --self-test",
        notes="Serves first-revenue + fiscal-existence; severity-first (existence-critical).",
    ),
    RegressionSurface(
        surface_id="S-05", name="Release-gate composite (full test suite + validators)",
        served_tiers=("IT-3", "IT-6"), time_criticality=3, risk_reduction=5, detection_gap=1,
        probe_cmd="py scripts/release-gate.py",
        notes="Authoritative mechanical safety net; ~7min; periodic not per-commit.",
    ),
    RegressionSurface(
        surface_id="S-06", name="Legal/fiscal existence artifacts (instruments, tax calendar, trademark)",
        served_tiers=("IT-2",), time_criticality=5, risk_reduction=4, detection_gap=3,
        severity_first=True,
        probe_cmd="py scripts/validate_finops_tax_calendar.py; py scripts/validate_filed_instruments.py",
        notes="Counsel-encoded; weak automated detection (dates are external).",
    ),
    RegressionSurface(
        surface_id="S-07", name="Operator interaction surfaces (MADEIRA, dashboards, scratchpad continuity)",
        served_tiers=("IT-4",), time_criticality=3, risk_reduction=3, detection_gap=3,
        probe_cmd="py scripts/browser-smoke.py --playwright (operator/MADEIRA routes)",
    ),
    RegressionSurface(
        surface_id="S-08", name="Brand & external-render trail (deck, audience tags, baseline-reality)",
        served_tiers=("IT-5",), time_criticality=3, risk_reduction=3, detection_gap=2,
        probe_cmd="py scripts/validate_brand_baseline_reality_drift.py; py scripts/validate_external_render_trail.py --strict",
    ),
    RegressionSurface(
        surface_id="S-09", name="Eval / MADEIRA quality (adversarial cassettes, promotion, judge)",
        served_tiers=("IT-6", "IT-4"), time_criticality=2, risk_reduction=3, detection_gap=2,
        probe_cmd="py -m pytest tests/test_eval_adversarial.py tests/test_eval_promotion.py",
        notes="Known-deferred replay window OPS-90-9 (ETA 2026-06-11).",
    ),
    RegressionSurface(
        surface_id="S-10", name="Runtime / deploy health (OpenClaw probe, fleet hygiene, sibling repos)",
        served_tiers=("IT-7",), time_criticality=3, risk_reduction=3, detection_gap=3,
        probe_cmd="py scripts/check-drift.py; py scripts/workspace_fleet_hygiene_sweep.py --sweep",
    ),
    RegressionSurface(
        surface_id="S-11", name="Index integrity (planning README, PRECEDENCE, CHANGELOG, dashboards)",
        served_tiers=("IT-3", "IT-4"), time_criticality=2, risk_reduction=2, detection_gap=3,
        probe_cmd="py scripts/baseline_index_sweep.py (or validate_index_freshness.py)",
    ),
    RegressionSurface(
        surface_id="S-12", name="Schema drift (CSV header / Pydantic enum / mirror DDL three-surface sync)",
        served_tiers=("IT-3",), time_criticality=3, risk_reduction=4, detection_gap=3,
        probe_cmd="py scripts/check-drift.py + per-registry pytest enum-completeness",
        notes="The pattern_class enum-lag (I93 area_governance) lived here — weak detection until pytest.",
    ),
    RegressionSurface(
        surface_id="S-13", name="HCAM articulation + visibility gold layer (entity wiring, triple activation, DGO scorecard)",
        served_tiers=("IT-3", "IT-4"), time_criticality=3, risk_reduction=4, detection_gap=3,
        probe_cmd="py scripts/validate_canonical_articulation.py --matrix",
        notes="Area-completeness v3 gold layer (D-IH-95-E). Pre-I95-E this surface had NO metric/gate (the operator's 'no useful metrics / no gold layer / no UI for DGO' gap — detection_gap was 5); now --matrix scorecard + METRICS_REGISTRY MET-HOL-ARTICULATION-* give define-once metrics the ERP/BI consume.",
    ),
)

REGRESSION_SURFACES_BY_ID: dict[str, RegressionSurface] = {
    s.surface_id: s for s in REGRESSION_SURFACES
}


def rank_surfaces(
    surfaces: tuple[RegressionSurface, ...] = REGRESSION_SURFACES,
    tiers: dict[str, IntentTier] = INTENT_TIERS_BY_ID,
) -> list[tuple[RegressionSurface, int]]:
    """Return surfaces ordered by sweep priority: severity-first surfaces lead,
    then by descending ICS, then by surface_id for deterministic ties.
    """
    return sorted(
        ((s, s.ics(tiers)) for s in surfaces),
        key=lambda pair: (not pair[0].severity_first, -pair[1], pair[0].surface_id),
    )
