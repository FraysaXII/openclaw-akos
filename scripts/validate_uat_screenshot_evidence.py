"""Experiential UAT screenshot evidence validator (L3.0 mechanical gate).

Pairs with:
- research-center-experiential-uat-ladder L3.0 (agent visual review)
- SOP-EXPERIENTIAL_UAT_AGENT_VISUAL_REVIEW_001 (I96 mint; promote to v3.0 when ratified)

Checks a capture session folder BEFORE a UAT verdict may cite journey PNGs:
- Unique sha256 per journey file (no duplicate captures)
- Minimum file size (sidebar-crop / favicon failures)
- Required journey filename tokens (Operator + Director × discover/triage/drawer/audit)
- agent_visual_review.json present with VALID row per journey file

CLI:
    py scripts/validate_uat_screenshot_evidence.py --self-test
    py scripts/validate_uat_screenshot_evidence.py --session-dir artifacts/uat-screenshots/<slug>/
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

JOURNEY_TOKENS: tuple[tuple[str, str], ...] = (
    ("operator", "discover"),
    ("operator", "triage"),
    ("operator", "drawer"),
    ("operator", "audit"),
    ("director", "discover"),
    ("director", "triage"),
    ("director", "drawer"),
    ("director", "audit"),
)

DEFAULT_MIN_BYTES = 29_000
REVIEW_FILENAME = "agent_visual_review.json"


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def journey_files(session_dir: Path) -> list[Path]:
    pngs = sorted(session_dir.glob("*.png"))
    journey: list[Path] = []
    for path in pngs:
        name = path.name.lower()
        if name.startswith("00-"):
            continue
        if any(token in name for token in ("operator", "director")):
            journey.append(path)
    return journey


def token_hit(name: str, lens: str, stage: str) -> bool:
    n = name.lower()
    return lens in n and stage in n.replace("drawer-open", "drawer")


def validate_session(session_dir: Path, *, min_bytes: int) -> list[Finding]:
    findings: list[Finding] = []
    if not session_dir.is_dir():
        return [
            Finding("UAT-SS-00-SESSION-MISSING", "fail", f"Session dir not found: {session_dir}")
        ]

    files = journey_files(session_dir)
    if len(files) < len(JOURNEY_TOKENS):
        findings.append(
            Finding(
                "UAT-SS-03-MISSING-JOURNEY",
                "fail",
                f"Expected ≥{len(JOURNEY_TOKENS)} journey PNGs; found {len(files)}",
            )
        )

    canonical: dict[tuple[str, str], Path] = {}
    for lens, stage in JOURNEY_TOKENS:
        matches = [p for p in files if token_hit(p.name, lens, stage)]
        if not matches:
            findings.append(
                Finding(
                    "UAT-SS-03-MISSING-JOURNEY",
                    "fail",
                    f"No PNG for {lens}/{stage}",
                )
            )
            continue
        best = max(matches, key=lambda p: p.stat().st_size)
        canonical[(lens, stage)] = best
        if best.stat().st_size < min_bytes:
            findings.append(
                Finding(
                    "UAT-SS-02-UNDERSIZE",
                    "fail",
                    f"{best.name} is {best.stat().st_size} bytes (< {min_bytes}) — likely sidebar crop or favicon",
                )
            )

    hashes: dict[str, list[str]] = {}
    for path in canonical.values():
        digest = sha256_file(path)
        hashes.setdefault(digest, []).append(path.name)
    for digest, names in hashes.items():
        if len(names) > 1:
            findings.append(
                Finding(
                    "UAT-SS-01-DUP-HASH",
                    "fail",
                    f"Duplicate capture sha256 {digest[:16]}… in {names}",
                )
            )

    review_path = session_dir / REVIEW_FILENAME
    if not review_path.is_file():
        findings.append(
            Finding(
                "UAT-SS-04-NO-VISUAL-REVIEW",
                "fail",
                f"Missing {REVIEW_FILENAME} — parent agent must read every PNG and record VALID/INVALID",
            )
        )
        return findings

    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(
            Finding(
                "UAT-SS-04-NO-VISUAL-REVIEW",
                "fail",
                f"{REVIEW_FILENAME} invalid JSON: {exc}",
            )
        )
        return findings

    rows = review.get("captures") or []
    if review.get("delegation_allowed") is True:
        findings.append(
            Finding(
                "UAT-SS-05-SUBAGENT-ONLY",
                "fail",
                "delegation_allowed=true — L3.0 forbids subagent-only visual review",
            )
        )

    by_file = {str(r.get("file", "")): r for r in rows if isinstance(r, dict)}
    for (lens, stage), path in canonical.items():
        row = by_file.get(path.name)
        if not row:
            findings.append(
                Finding(
                    "UAT-SS-04-NO-VISUAL-REVIEW",
                    "fail",
                    f"No visual-review row for {path.name}",
                )
            )
        elif str(row.get("verdict", "")).upper() != "VALID":
            findings.append(
                Finding(
                    "UAT-SS-06-INVALID-VISUAL",
                    "fail",
                    f"{path.name} visual verdict={row.get('verdict')!r} (must be VALID for journey PASS)",
                )
            )
        elif not str(row.get("observations", "")).strip():
            findings.append(
                Finding(
                    "UAT-SS-07-EMPTY-OBSERVATIONS",
                    "warn",
                    f"{path.name} missing observations text",
                )
            )

    return findings


def run_self_test() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        session = Path(tmp)
        good = session / "01-operator-discover-1280.png"
        good.write_bytes(b"x" * DEFAULT_MIN_BYTES)
        review = {
            "delegation_allowed": False,
            "captures": [
                {
                    "file": good.name,
                    "verdict": "VALID",
                    "observations": "Research Center heading visible",
                }
            ],
        }
        (session / REVIEW_FILENAME).write_text(json.dumps(review), encoding="utf-8")
        findings = validate_session(session, min_bytes=DEFAULT_MIN_BYTES)
        assert any(f.code == "UAT-SS-03-MISSING-JOURNEY" for f in findings)
        print("  self-test: incomplete journey detected OK")

        dup = session / "06-director-triage-1280.png"
        dup.write_bytes(good.read_bytes())
        findings = validate_session(session, min_bytes=DEFAULT_MIN_BYTES)
        assert any(f.code == "UAT-SS-01-DUP-HASH" for f in findings)
        print("  self-test: duplicate hash detected OK")

    print("validate_uat_screenshot_evidence.py self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate experiential UAT screenshot evidence")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--session-dir", type=Path, help="Capture session folder")
    parser.add_argument("--min-bytes", type=int, default=DEFAULT_MIN_BYTES)
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return 0

    if not args.session_dir:
        parser.error("--session-dir required unless --self-test")
        return 2

    session_dir = args.session_dir
    if not session_dir.is_absolute():
        session_dir = REPO_ROOT / session_dir

    findings = validate_session(session_dir, min_bytes=args.min_bytes)
    fails = [f for f in findings if f.severity == "fail"]
    warns = [f for f in findings if f.severity == "warn"]

    for f in findings:
        print(f"[{f.severity.upper()}] {f.code}: {f.message}")

    if fails:
        print(f"\nFAIL count={len(fails)} WARN count={len(warns)}")
        return 1
    print(f"\nPASS — screenshot evidence clean (WARN={len(warns)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
