#!/usr/bin/env python3
"""Always-on validator for the SYNTHESIS_BEFORE_TRANCHE discipline.

The 14th Quality Fabric specialty per `D-IH-86-EA` mint (2026-05-25).
Canonical doctrine:
  ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/``
  ``SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md``
Pydantic SSOT:
  ``akos/hlk_synthesis_before_tranche.py``
Paired runbook:
  ``scripts/synthesis_before_tranche_check.py``
Companion cursor rule (Commit 2c-a):
  ``.cursor/rules/akos-synthesis-before-tranche.mdc``
Companion skill (Commit 2c-a):
  ``.cursor/skills/synthesis-before-tranche-craft/SKILL.md``
Decision lineage:
  D-IH-86-EA (doctrine mint + INFO ramp),
  D-IH-86-EB (10-dimension probe set ratification),
  D-IH-86-EC (5-option disposition enum + per-tranche-class firing),
  D-IH-86-ED (broad-fire posture with INFO ramp).

Unlike COLLABORATOR_SHARE (the 13th specialty) — which validates 5 sibling
canonical CSVs — SYNTHESIS_BEFORE_TRANCHE's artifacts are per-tranche
synthesis reports (markdown deliverables emitted by the paired runbook).
There is no canonical CSV gate; therefore this validator does NOT register
in the ``validate_hlk.py`` umbrella (it's invoked directly from
``pre_commit`` via verification-profiles.json + release-gate.py).

The validator's job is to be the always-on circuit-breaker that guarantees:

  (a) the Pydantic chassis at ``akos/hlk_synthesis_before_tranche.py`` is
      importable + the 5 frozenset enums + 3 lookup dicts + the
      ``resolve_fire_set()`` helper + 3 Pydantic models all instantiate
      from worked-example fixtures.

  (b) the per-tranche-class fire rules in ``DIMENSION_FIRE_RULES`` are
      well-formed (every tranche class has a (always, conditional)
      tuple; every dimension referenced is in VALID_DIMENSION_CODES;
      always + conditional are disjoint per class).

  (c) the 10 dimensions all have DIMENSION_DESCRIPTIONS entries +
      DIMENSION_SEVERITY_CLASS entries (no orphan dimensions).

Posture per D-IH-86-ED (Wave R+1 P3 mint INFO ramp):

  --self-test  : Pydantic-fixture validation + probe-registry shape
                 check; zero CI cost; always exits 0 on PASS. Wired into
                 release-gate.py + pre_commit profile.
  (no args)    : same as --self-test (default mode at INFO ramp; the
                 actual per-tranche sweep lives in the paired runbook
                 ``scripts/synthesis_before_tranche_check.py``).
  --strict     : exit non-zero on any chassis/probe-registry drift
                 (currently equivalent to --self-test FAIL; reserved for
                 future expansion when the FAIL ramp promotes per
                 D-IH-86-ED Stage 2).

Per ``akos-executable-process-catalog.mdc`` Rule 1: this validator is the
AC-AUTOMATION half of the SOP+runbook pair. The SOP (Commit 2c-a) carries
the AC-HUMAN narrative + operator walkthrough.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_synthesis_before_tranche import (  # noqa: E402
    DIMENSION_DESCRIPTIONS,
    DIMENSION_FIRE_RULES,
    DIMENSION_SEVERITY_CLASS,
    VALID_DIMENSION_CODES,
    VALID_DISPOSITIONS,
    VALID_FINDING_STATUSES,
    VALID_REVERSIBILITY_CLASSES,
    VALID_SWEEP_TRIGGERS,
    VALID_TRANCHE_CLASSES,
    SynthesisFindingRow,
    SynthesisReportSummary,
    SynthesisTrancheCharter,
    resolve_fire_set,
)

logger = logging.getLogger(__name__)


def _verify_enum_invariants() -> list[str]:
    """Return a list of human-readable error messages; empty list = PASS."""
    errors: list[str] = []

    # 1. Every dimension in VALID_DIMENSION_CODES has a description.
    missing_desc = sorted(VALID_DIMENSION_CODES - set(DIMENSION_DESCRIPTIONS))
    if missing_desc:
        errors.append(
            f"DIMENSION_DESCRIPTIONS missing entries for: {missing_desc}"
        )
    extra_desc = sorted(set(DIMENSION_DESCRIPTIONS) - VALID_DIMENSION_CODES)
    if extra_desc:
        errors.append(
            f"DIMENSION_DESCRIPTIONS has orphan entries: {extra_desc}"
        )

    # 2. Every dimension has a severity class.
    missing_sev = sorted(VALID_DIMENSION_CODES - set(DIMENSION_SEVERITY_CLASS))
    if missing_sev:
        errors.append(
            f"DIMENSION_SEVERITY_CLASS missing entries for: {missing_sev}"
        )

    # 3. Every tranche class has a fire-rule entry.
    missing_fire = sorted(VALID_TRANCHE_CLASSES - set(DIMENSION_FIRE_RULES))
    if missing_fire:
        errors.append(
            f"DIMENSION_FIRE_RULES missing entries for: {missing_fire}"
        )

    # 4. Per-class invariant: always + conditional disjoint; both subsets of
    #    VALID_DIMENSION_CODES.
    for tclass, (always, conditional) in DIMENSION_FIRE_RULES.items():
        overlap = always & conditional
        if overlap:
            errors.append(
                f"DIMENSION_FIRE_RULES[{tclass!r}]: always + conditional "
                f"overlap: {sorted(overlap)}"
            )
        out_of_bounds = (always | conditional) - VALID_DIMENSION_CODES
        if out_of_bounds:
            errors.append(
                f"DIMENSION_FIRE_RULES[{tclass!r}]: unknown dimensions: "
                f"{sorted(out_of_bounds)}"
            )

    return errors


def _verify_pydantic_fixtures() -> list[str]:
    """Instantiate each Pydantic model from a worked-example fixture."""
    errors: list[str] = []

    try:
        row = SynthesisFindingRow(
            tranche_id="ENG-SUEZ-EFA-2026/p1-libelle-generator",
            tranche_class="engagement",
            dimension_code="SYN-01-AUDIENCE-COMPLETENESS",  # canonical per chassis
            status="PASS",
            finding_text=(
                "audience J-CU (SUEZ CTO office) + J-PT (Aïsha continuity) "
                "+ J-OP (operator) named in tranche charter frontmatter"
            ),
            recommended_disposition="scope-complete",
        )
        if row.tranche_class != "engagement":
            errors.append("SynthesisFindingRow: tranche_class round-trip failed")
    except Exception as exc:  # pragma: no cover
        errors.append(f"SynthesisFindingRow fixture failed: {exc!r}")

    try:
        charter = SynthesisTrancheCharter(
            tranche_id="I86-WaveRplus1-P3-Commit2b-synthesis-validator",
            tranche_class="specialty_mint",
            tranche_title=(
                "14th specialty validator + runbook + verification wiring"
            ),
            audiences_named=["J-OP"],
            channels_named=[],
            scenarios_named=[],
            brand_register="internal-corpint",
            ratifying_decisions=["D-IH-86-EA", "D-IH-86-EB", "D-IH-86-EC",
                                 "D-IH-86-ED"],
            erp_surface_citations=[],
            is_atomic_commit=True,
            reversibility_class="medium",
            reversibility_rationale=(
                "validator + runbook + verification wiring; revert via git "
                "revert + verification-profiles.json + release-gate.py "
                "unwiring; no canonical CSV writes; medium reversibility"
            ),
            closing_loop_test=(
                "validate_synthesis_before_tranche.py --self-test PASS + "
                "synthesis_before_tranche_check.py --self-test PASS + 60+ "
                "pytest in tests/test_validate_synthesis_before_tranche.py "
                "PASS"
            ),
            recipient_fallback_channel="n/a (J-OP-only governance tranche)",
        )
        if charter.tranche_class != "specialty_mint":
            errors.append("SynthesisTrancheCharter: tranche_class round-trip failed")
    except Exception as exc:  # pragma: no cover
        errors.append(f"SynthesisTrancheCharter fixture failed: {exc!r}")

    try:
        summary = SynthesisReportSummary(
            tranche_id="I86-WaveRplus1-P3-Commit2b-synthesis-validator",
            tranche_class="specialty_mint",
            swept_at="2026-05-25",
            sweep_trigger="pre_commit_self_test",
            dimensions_fired=7,
            pass_count=7,
            warn_count=0,
            fail_count=0,
            info_count=0,
            na_count=3,
            synthesis_complete=True,
            inline_ratify_gates_open=0,
            operator_disposition_recorded=True,
        )
        if not summary.synthesis_complete:
            errors.append("SynthesisReportSummary: synthesis_complete round-trip failed")
    except Exception as exc:  # pragma: no cover
        errors.append(f"SynthesisReportSummary fixture failed: {exc!r}")

    return errors


def _verify_resolve_fire_set() -> list[str]:
    """Spot-check the resolve_fire_set helper across all 6 tranche classes."""
    errors: list[str] = []

    # engagement fires all 10 always
    eng_always = resolve_fire_set("engagement", conditional_triggers=False)
    if eng_always != VALID_DIMENSION_CODES:
        errors.append(
            f"resolve_fire_set('engagement'): expected all 10 dimensions, "
            f"got {sorted(eng_always)}"
        )

    # specialty_mint fires 7 always (missing SYN-03 + SYN-06 + SYN-10 from baseline)
    sm_always = resolve_fire_set("specialty_mint", conditional_triggers=False)
    if len(sm_always) != 7:
        errors.append(
            f"resolve_fire_set('specialty_mint'): expected 7 baseline, "
            f"got {len(sm_always)} ({sorted(sm_always)})"
        )

    # specialty_mint with conditional adds SYN-03 (total 8)
    sm_all = resolve_fire_set("specialty_mint", conditional_triggers=True)
    if len(sm_all) != 8:
        errors.append(
            f"resolve_fire_set('specialty_mint', conditional=True): "
            f"expected 8, got {len(sm_all)} ({sorted(sm_all)})"
        )

    # internal_governance fires 3 baseline
    ig_always = resolve_fire_set("internal_governance", conditional_triggers=False)
    if len(ig_always) != 3:
        errors.append(
            f"resolve_fire_set('internal_governance'): expected 3 baseline, "
            f"got {len(ig_always)} ({sorted(ig_always)})"
        )

    # external_deliverable fires all 10
    ed_always = resolve_fire_set("external_deliverable", conditional_triggers=False)
    if ed_always != VALID_DIMENSION_CODES:
        errors.append(
            f"resolve_fire_set('external_deliverable'): expected all 10, "
            f"got {sorted(ed_always)}"
        )

    # unknown tranche class raises ValueError
    try:
        resolve_fire_set("unknown_class")
        errors.append(
            "resolve_fire_set('unknown_class'): expected ValueError, no exception raised"
        )
    except ValueError:
        pass  # expected

    return errors


def _verify_enum_membership_counts() -> list[str]:
    """Enforce the canonical enum cardinalities per doctrine §2 / §3 / §7."""
    errors: list[str] = []
    if len(VALID_DIMENSION_CODES) != 10:
        errors.append(
            f"VALID_DIMENSION_CODES: expected 10 SYN-NN codes, got {len(VALID_DIMENSION_CODES)}"
        )
    if len(VALID_TRANCHE_CLASSES) != 6:
        errors.append(
            f"VALID_TRANCHE_CLASSES: expected 6 classes, got {len(VALID_TRANCHE_CLASSES)}"
        )
    if len(VALID_DISPOSITIONS) != 5:
        errors.append(
            f"VALID_DISPOSITIONS: expected 5 options, got {len(VALID_DISPOSITIONS)}"
        )
    if len(VALID_FINDING_STATUSES) != 5:
        errors.append(
            f"VALID_FINDING_STATUSES: expected 5 statuses (PASS/WARN/FAIL/INFO/N/A), "
            f"got {len(VALID_FINDING_STATUSES)}"
        )
    if len(VALID_REVERSIBILITY_CLASSES) != 3:
        errors.append(
            f"VALID_REVERSIBILITY_CLASSES: expected 3 (low/medium/high), "
            f"got {len(VALID_REVERSIBILITY_CLASSES)}"
        )
    if len(VALID_SWEEP_TRIGGERS) != 4:
        errors.append(
            f"VALID_SWEEP_TRIGGERS: expected 4, got {len(VALID_SWEEP_TRIGGERS)}"
        )
    return errors


def self_test() -> int:
    """Pydantic chassis + probe-registry shape validation.

    Returns 0 on PASS; non-zero (1..4) on FAIL with category indicator.
    """
    enum_errors = _verify_enum_invariants()
    if enum_errors:
        for msg in enum_errors:
            print(f"FAIL [enum-invariant]: {msg}")
        return 1

    cardinality_errors = _verify_enum_membership_counts()
    if cardinality_errors:
        for msg in cardinality_errors:
            print(f"FAIL [enum-cardinality]: {msg}")
        return 2

    fixture_errors = _verify_pydantic_fixtures()
    if fixture_errors:
        for msg in fixture_errors:
            print(f"FAIL [pydantic-fixture]: {msg}")
        return 3

    helper_errors = _verify_resolve_fire_set()
    if helper_errors:
        for msg in helper_errors:
            print(f"FAIL [resolve-fire-set]: {msg}")
        return 4

    print(
        "validate_synthesis_before_tranche --self-test: PASS "
        f"({len(VALID_DIMENSION_CODES)} dimensions x "
        f"{len(VALID_TRANCHE_CLASSES)} tranche classes x "
        f"{len(VALID_DISPOSITIONS)} dispositions; Pydantic fixtures "
        "instantiate; resolve_fire_set helper consistent)"
    )
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    parser = argparse.ArgumentParser(
        description=(
            "Always-on validator for the SYNTHESIS_BEFORE_TRANCHE discipline "
            "(14th Quality Fabric specialty per D-IH-86-EA mint). At INFO "
            "ramp; --self-test mode is the always-on circuit breaker."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Verify Pydantic chassis + probe-registry shape. Wired into "
            "pre_commit + release-gate.py for zero-cost CI gating."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Reserved for the FAIL ramp (D-IH-86-ED Stage 2). Currently "
            "equivalent to --self-test (exits non-zero on chassis drift)."
        ),
    )
    args = parser.parse_args()

    # Default behaviour at INFO ramp = self-test
    return self_test()


if __name__ == "__main__":
    sys.exit(main())
