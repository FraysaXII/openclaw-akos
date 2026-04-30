"""Initiative 30 P3 + P6 — drift detector for GOVERNANCE_MOAT.md.

The moat artifact at
``docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/GOVERNANCE_MOAT.md``
quotes four hero metrics that the deck slide 11 pillar 1 then re-quotes:

- Topics (count from ``TOPIC_REGISTRY.csv``)
- Processes (count from ``process_list.csv``)
- Roles (count from ``baseline_organisation.csv``)
- KM Output 1 manifests (count from ``validate_hlk_km_manifests.py``)

This test enforces parity between the artifact's quoted numbers and the live
``validate_hlk`` / ``sync_compliance_mirrors_from_csv --count-only`` output.

Tolerance per D-IH-30-F:
- Topics: +0 / -0 (exact match required; topic count growth is rare and meaningful)
- Roles: +0 / -0 (same — roles change deliberately)
- Processes: +/- 5 % (daily ops adds rows; a 5 % band absorbs growth without nuisance failures)
- KM manifests: +/- 1 (rare growth; tight band)

If any check fails, the operator updates GOVERNANCE_MOAT.md to match the live
counts (under five minutes of work) and re-runs the build pipeline.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
GOVERNANCE_MOAT_MD = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "Operations" / "PMO" / "business-strategy" / "GOVERNANCE_MOAT.md"
)


def _moat_text() -> str:
    if not GOVERNANCE_MOAT_MD.is_file():
        pytest.skip("GOVERNANCE_MOAT.md not present (Initiative 30 P3 not yet shipped)")
    return GOVERNANCE_MOAT_MD.read_text(encoding="utf-8")


def _live_topic_count() -> int:
    """Run validate_topic_registry.py and parse `Rows validated: <n>`."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_topic_registry.py")],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, (
        f"validate_topic_registry.py failed (rc={proc.returncode}): "
        f"stdout={proc.stdout}\nstderr={proc.stderr}"
    )
    m = re.search(r"Rows validated:\s*(\d+)", proc.stdout)
    assert m, f"could not parse 'Rows validated' from output:\n{proc.stdout}"
    return int(m.group(1))


def _live_count_only_dict() -> dict[str, int]:
    """Run sync_compliance_mirrors_from_csv.py --count-only and parse rows."""
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
            "--count-only",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, (
        f"sync_compliance_mirrors_from_csv --count-only failed (rc={proc.returncode}): "
        f"stdout={proc.stdout}\nstderr={proc.stderr}"
    )
    out: dict[str, int] = {}
    for line in proc.stdout.splitlines():
        m = re.match(r"^(\w+_rows)=(\d+)\s*$", line.strip())
        if m:
            out[m.group(1)] = int(m.group(2))
    return out


def _live_km_manifest_count() -> int:
    """Run validate_hlk_km_manifests.py and count PASS/FAIL lines."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk_km_manifests.py")],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, (
        f"validate_hlk_km_manifests.py failed (rc={proc.returncode}): "
        f"stdout={proc.stdout}\nstderr={proc.stderr}"
    )
    return sum(
        1 for line in proc.stdout.splitlines()
        if re.search(r"\.manifest\.md\s+(PASS|FAIL)", line)
    )


def _quoted_metric(text: str, pattern: str) -> int:
    """Find an integer captured by `pattern` (with one capture group) in text."""
    m = re.search(pattern, text)
    assert m, f"could not find metric matching {pattern!r} in GOVERNANCE_MOAT.md"
    raw = m.group(1).replace(".", "").replace(",", "")
    return int(raw)


def test_moat_topic_count_matches_live():
    """+0 / -0 tolerance per D-IH-30-F."""
    text = _moat_text()
    quoted = _quoted_metric(text, r"\*\*Temas gobernados\*\*\s*\|\s*\*\*(\d+)\*\*")
    live = _live_topic_count()
    assert quoted == live, (
        f"GOVERNANCE_MOAT.md quotes {quoted} topics; live validate_topic_registry "
        f"reports {live}. Update the artifact (and slide 11 pillar 1 in deck_slides.yaml)."
    )


def test_moat_role_count_matches_live():
    """+0 / -0 tolerance per D-IH-30-F."""
    text = _moat_text()
    quoted = _quoted_metric(text, r"\*\*Roles definidos\*\*\s*\|\s*\*\*(\d+)\*\*")
    live = _live_count_only_dict().get("baseline_organisation_rows")
    assert live is not None, "could not parse baseline_organisation_rows from sync output"
    assert quoted == live, (
        f"GOVERNANCE_MOAT.md quotes {quoted} roles; live count reports {live}. "
        f"Update the artifact (and slide 11 pillar 1 in deck_slides.yaml)."
    )


def test_moat_process_count_within_5pct_of_live():
    """+/- 5 % tolerance per D-IH-30-F (allows daily ops growth)."""
    text = _moat_text()
    quoted = _quoted_metric(text, r"\*\*Procesos gobernados\*\*\s*\|\s*\*\*([\d\.]+)\*\*")
    live = _live_count_only_dict().get("process_list_rows")
    assert live is not None, "could not parse process_list_rows from sync output"
    drift_pct = abs(quoted - live) / max(live, 1) * 100
    assert drift_pct <= 5.0, (
        f"GOVERNANCE_MOAT.md quotes {quoted} processes; live count reports {live}. "
        f"Drift is {drift_pct:.2f}% (limit: 5%). Refresh the artifact."
    )


def test_moat_km_manifest_count_within_1_of_live():
    """+/- 1 tolerance per D-IH-30-F."""
    text = _moat_text()
    quoted = _quoted_metric(text, r"\*\*Manifests Output 1 \(KM visuales\)\*\*\s*\|\s*\*\*(\d+)\*\*")
    live = _live_km_manifest_count()
    drift = abs(quoted - live)
    assert drift <= 1, (
        f"GOVERNANCE_MOAT.md quotes {quoted} KM manifests; live validator reports "
        f"{live}. Drift is {drift} (limit: 1). Refresh the artifact."
    )


def test_moat_artifact_declares_drift_test_in_body():
    """The artifact must point at this test in its body so a future operator
    knows where to look when a metric refreshes."""
    text = _moat_text()
    assert "tests/test_governance_moat_metrics.py" in text, (
        "GOVERNANCE_MOAT.md must reference the drift-detector test path so "
        "future operators understand the parity contract"
    )
