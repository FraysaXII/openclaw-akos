#!/usr/bin/env python3
"""Validator/runbook for MKTOps 7-dimension campaign quality bar.

Default mode (``--self-test``) validates the Pydantic SSOT at
``akos/hlk_mktops.py`` and the dimension constants. The full per-campaign
sweep (``--check-campaign <manifest.yaml>``) runs the 7 dimensions against
a campaign manifest authored alongside the campaign artifacts.

Per ``MKTOPS_DISCIPLINE.md`` §4 cadence:

- ``--self-test`` fires at every ``pre_commit`` and ``release-gate.py`` run.
- ``--check-campaign`` fires at campaign-brief authoring + each lifecycle
  gate.

This runbook is the AC-AUTOMATION half of the SOP+runbook pair per
``akos-executable-process-catalog.mdc`` Rule 1; the operator-facing SOP
walks the same checks manually.

Status promotion from ``charter`` to ``active`` lands at Wave R+4 C3a
per ``D-IH-86-EY``.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_mktops import (  # noqa: E402
    DIMENSION_DESCRIPTIONS,
    VALID_FUNNEL_STAGES,
    VALID_LIFECYCLE_STATES,
    VALID_MKTOPS_DIMENSIONS,
    MKTOpsCampaignManifest,
    MKTOpsCampaignReport,
    MKTOpsFindingRow,
    fixture_campaign_manifest,
    fixture_finding_pass,
)

PERSONA_REGISTRY_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "dimensions"
    / "PERSONA_REGISTRY.csv"
)
CHANNEL_REGISTRY_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "dimensions"
    / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
)


def _load_csv_column(path: Path, column: str) -> set[str]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return {
            (row.get(column) or "").strip()
            for row in csv.DictReader(fh)
            if (row.get(column) or "").strip()
        }


def _load_manifest(path: Path) -> MKTOpsCampaignManifest:
    raw_text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data: Any = json.loads(raw_text)
    else:
        try:
            import yaml

            data = yaml.safe_load(raw_text)
        except Exception as exc:  # pragma: no cover - import error path
            raise SystemExit(
                f"Cannot parse manifest at {path}; install PyYAML or provide .json"
            ) from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Manifest at {path} is not a YAML/JSON mapping")
    return MKTOpsCampaignManifest.model_validate(data)


def _check_lifecycle_quality(manifest: MKTOpsCampaignManifest) -> MKTOpsFindingRow:
    if manifest.lifecycle_state in VALID_LIFECYCLE_STATES:
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-01-CAMPAIGN-LIFECYCLE-QUALITY",
            status="PASS",
            finding_text=(
                f"lifecycle_state={manifest.lifecycle_state} is a recognised gate."
            ),
        )
    return MKTOpsFindingRow(
        campaign_id=manifest.campaign_id,
        dimension_code="MKT-01-CAMPAIGN-LIFECYCLE-QUALITY",
        status="FAIL",
        finding_text=(
            f"lifecycle_state={manifest.lifecycle_state!r} not in known gates."
        ),
        recommended_action="Use one of: brief / creative / review / launch / measure / closed.",
    )


def _check_funnel_stage_ux(manifest: MKTOpsCampaignManifest) -> MKTOpsFindingRow:
    if manifest.funnel_stage not in VALID_FUNNEL_STAGES:
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-02-FUNNEL-STAGE-UX",
            status="FAIL",
            finding_text=f"funnel_stage={manifest.funnel_stage!r} not in enum.",
            recommended_action="Set funnel_stage to one of awareness / consideration / decision / retention / advocacy.",
        )
    return MKTOpsFindingRow(
        campaign_id=manifest.campaign_id,
        dimension_code="MKT-02-FUNNEL-STAGE-UX",
        status="INFO",
        finding_text=(
            f"funnel_stage={manifest.funnel_stage} accepted; deep UX bar from "
            "UX_DISCIPLINE.md applies at creative review."
        ),
    )


def _check_landing_page_conversion(manifest: MKTOpsCampaignManifest) -> MKTOpsFindingRow:
    if not manifest.landing_page_path and not manifest.measurement_event:
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-03-LANDING-PAGE-CONVERSION",
            status="WARN",
            finding_text=(
                "No landing_page_path and no measurement_event named; conversion bar "
                "cannot be tested at lifecycle later."
            ),
            recommended_action="Add measurement_event (and landing_page_path when applicable).",
        )
    return MKTOpsFindingRow(
        campaign_id=manifest.campaign_id,
        dimension_code="MKT-03-LANDING-PAGE-CONVERSION",
        status="PASS",
        finding_text=(
            f"measurement_event={manifest.measurement_event or 'unset'}; "
            f"landing_page_path={manifest.landing_page_path or 'unset'}."
        ),
    )


def _check_attribution_trail(manifest: MKTOpsCampaignManifest) -> MKTOpsFindingRow:
    missing = [
        name
        for name, value in (
            ("utm_source", manifest.utm_source),
            ("utm_medium", manifest.utm_medium),
            ("utm_campaign", manifest.utm_campaign),
        )
        if not value
    ]
    if missing:
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-04-ATTRIBUTION-TRAIL",
            status="WARN",
            finding_text=f"Missing UTM tag(s): {', '.join(missing)}.",
            recommended_action="Populate utm_source / utm_medium / utm_campaign before launch.",
        )
    return MKTOpsFindingRow(
        campaign_id=manifest.campaign_id,
        dimension_code="MKT-04-ATTRIBUTION-TRAIL",
        status="PASS",
        finding_text="UTM tags present (source + medium + campaign).",
    )


def _check_channel_coverage(
    manifest: MKTOpsCampaignManifest, valid_channels: set[str]
) -> MKTOpsFindingRow:
    if not manifest.channel_ids:
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-05-CHANNEL-COVERAGE",
            status="FAIL",
            finding_text="No channel_ids declared.",
            recommended_action="Name at least one CHANNEL_TOUCHPOINT_REGISTRY channel.",
        )
    unresolved = sorted(set(manifest.channel_ids) - valid_channels) if valid_channels else []
    if unresolved:
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-05-CHANNEL-COVERAGE",
            status="FAIL",
            finding_text=f"channel_ids do not resolve: {unresolved}.",
            recommended_action="Use channel_id values present in CHANNEL_TOUCHPOINT_REGISTRY.csv.",
        )
    return MKTOpsFindingRow(
        campaign_id=manifest.campaign_id,
        dimension_code="MKT-05-CHANNEL-COVERAGE",
        status="PASS",
        finding_text=f"channel_ids resolve: {manifest.channel_ids}.",
    )


def _check_persona_fit(
    manifest: MKTOpsCampaignManifest, valid_personas: set[str]
) -> MKTOpsFindingRow:
    if not manifest.target_persona_ids:
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-06-PERSONA-FIT",
            status="FAIL",
            finding_text="No target_persona_ids declared.",
            recommended_action="Name at least one PERSONA_REGISTRY persona.",
        )
    unresolved = (
        sorted(set(manifest.target_persona_ids) - valid_personas) if valid_personas else []
    )
    if unresolved:
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-06-PERSONA-FIT",
            status="FAIL",
            finding_text=f"target_persona_ids do not resolve: {unresolved}.",
            recommended_action="Use persona_id values present in PERSONA_REGISTRY.csv.",
        )
    return MKTOpsFindingRow(
        campaign_id=manifest.campaign_id,
        dimension_code="MKT-06-PERSONA-FIT",
        status="PASS",
        finding_text=f"target_persona_ids resolve: {manifest.target_persona_ids}.",
    )


def _check_brand_voice(manifest: MKTOpsCampaignManifest) -> MKTOpsFindingRow:
    if manifest.brand_register == "external-translated":
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-07-BRAND-VOICE-INTEGRITY",
            status="INFO",
            finding_text=(
                "brand_register=external-translated; defer to validate_brand_baseline_reality_drift.py "
                "for full external-prose scan."
            ),
        )
    if manifest.brand_register == "internal-corpint" or manifest.brand_register == "internal-only":
        return MKTOpsFindingRow(
            campaign_id=manifest.campaign_id,
            dimension_code="MKT-07-BRAND-VOICE-INTEGRITY",
            status="INFO",
            finding_text=(
                f"brand_register={manifest.brand_register}; CORPINT register acceptable for J-OP."
            ),
        )
    return MKTOpsFindingRow(
        campaign_id=manifest.campaign_id,
        dimension_code="MKT-07-BRAND-VOICE-INTEGRITY",
        status="WARN",
        finding_text=(
            f"brand_register={manifest.brand_register} is mixed; ensure dual-register "
            "translation is explicit per surface."
        ),
        recommended_action="Split mixed-register surfaces or name each surface's register explicitly.",
    )


def run_campaign_check(manifest: MKTOpsCampaignManifest) -> MKTOpsCampaignReport:
    """Execute the 7-dimension check on a campaign manifest."""

    valid_personas = _load_csv_column(PERSONA_REGISTRY_PATH, "persona_id")
    valid_channels = _load_csv_column(CHANNEL_REGISTRY_PATH, "channel_id")
    findings: list[MKTOpsFindingRow] = [
        _check_lifecycle_quality(manifest),
        _check_funnel_stage_ux(manifest),
        _check_landing_page_conversion(manifest),
        _check_attribution_trail(manifest),
        _check_channel_coverage(manifest, valid_channels),
        _check_persona_fit(manifest, valid_personas),
        _check_brand_voice(manifest),
    ]
    counts = Counter(f.status for f in findings)
    return MKTOpsCampaignReport(
        campaign_id=manifest.campaign_id,
        funnel_stage=manifest.funnel_stage,
        dimensions_fired=[f.dimension_code for f in findings],
        pass_count=counts.get("PASS", 0),
        warn_count=counts.get("WARN", 0),
        fail_count=counts.get("FAIL", 0),
        info_count=counts.get("INFO", 0),
        skip_count=counts.get("SKIP", 0),
        findings=findings,
    )


def self_test() -> int:
    """Self-test the Pydantic chassis and dimension enums."""

    if len(VALID_MKTOPS_DIMENSIONS) != 7:
        print(f"FAIL: expected 7 MKTOps dimensions, got {len(VALID_MKTOPS_DIMENSIONS)}")
        return 1
    missing_desc = sorted(VALID_MKTOPS_DIMENSIONS - set(DIMENSION_DESCRIPTIONS))
    if missing_desc:
        print(f"FAIL: missing DIMENSION_DESCRIPTIONS for {missing_desc}")
        return 1
    try:
        manifest = fixture_campaign_manifest()
        finding = fixture_finding_pass()
    except Exception as exc:
        print(f"FAIL: fixture construction error {exc!r}")
        return 1
    if not manifest.campaign_id.startswith("CAMP-"):
        print("FAIL: fixture manifest campaign_id missing CAMP- prefix")
        return 1
    if finding.dimension_code not in VALID_MKTOPS_DIMENSIONS:
        print("FAIL: fixture finding dimension not in enum")
        return 1
    print("PASS: mktops campaign self-test")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--check-campaign",
        help="Path to a campaign manifest (YAML or JSON).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat WARN findings as exit code 1.",
    )
    args = parser.parse_args(argv)

    if args.self_test or not args.check_campaign:
        return self_test()

    manifest_path = Path(args.check_campaign)
    if not manifest_path.is_absolute():
        manifest_path = REPO_ROOT / manifest_path
    if not manifest_path.is_file():
        print(f"FAIL: manifest not found at {manifest_path}")
        return 1

    manifest = _load_manifest(manifest_path)
    report = run_campaign_check(manifest)
    print(
        f"MKTOps campaign {report.campaign_id} ({report.funnel_stage}): "
        f"PASS={report.pass_count} WARN={report.warn_count} FAIL={report.fail_count} "
        f"INFO={report.info_count}"
    )
    for finding in report.findings:
        print(f"  [{finding.status}] {finding.dimension_code}: {finding.finding_text}")
        if finding.recommended_action:
            print(f"        -> {finding.recommended_action}")

    if report.fail_count > 0:
        return 1
    if args.strict and report.warn_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
