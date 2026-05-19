"""Madeira self-policing + voice-profile runbook per I76 P3.

Paired runbook for ``SOP-TECH_MADEIRA_PERSONALITY_001.md`` (Lane C of I76 P3,
post-operator-ratify 2026-05-19 21:00 per ``D-IH-76-G`` through ``D-IH-76-M``).

Three subcommands:

1. ``bbr-scan`` (default; Lane A original behavior) — pipe a draft via
   ``--text`` or stdin; scan for internal-register tokens per
   ``BRAND_BASELINE_REALITY_MATRIX.md`` §3 via
   :func:`akos.brand_baseline_reality.scan_text`. Exit 0 = clean; 1 = hits.
2. ``load --profile-id <id>`` — load a profile from
   :data:`akos.hlk_operator_voice.STANDARD_VOICE_PROFILES`; print trait list
   + audience constraint + corpus paths + cadence. Used by AICs at session
   start per ``D-IH-76-M`` per-AIC re-load.
3. ``voice-audit --transcript <path> [--profile-id <id>]`` — scan a
   transcript file for: (a) anti-sycophancy 3-consecutive-agreement
   threshold violations per ``D-IH-76-J``; (b) BBR-jargon leaks into
   ``J-OP``-marked surfaces via the BBR scanner; (c) audience-constraint
   mis-routing (when the transcript carries an explicit ``audience:`` tag
   that is NOT in the loaded profile's ``audience_constraint``). INFO-only
   by default; ``--strict`` promotes findings to FAIL.

Cross-references: ``akos-brand-baseline-reality.mdc`` (vocabulary axis),
``akos-external-render-discipline.mdc`` (render-format axis),
``akos-executable-process-catalog.mdc`` RULE 1 (SOP+runbook pairing).
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.brand_baseline_reality import BaselineHit, scan_text
from akos.hlk_operator_voice import (
    STANDARD_AUDIENCE_CONSTRAINTS,
    STANDARD_VOICE_PROFILES,
    OperatorVoiceProfile,
    get_profile,
)
from akos.log import setup_logging

LOG = logging.getLogger("madeira_personality_check")


_DEFAULT_PROFILE_ID = "voice_akos_founder_2026"
"""Per D-IH-76-M, the Founder voice is the default when no AIC-specific
profile is registered. Operator framing: Madeira is the 1 AIC at v1; the
founder voice is its primary register."""


_AGREEMENT_LEAD_PATTERN = re.compile(
    r"^\s*(?:[*-]?\s*)?(?:\*\*)?"  # optional bullet / bold marker
    r"(yes|sí|si|oui|correct|right|agreed|understood|absolutely|exactly|"
    r"sounds good|got it|will do|on it|copy|confirmed|ok|okay|sure)\b",
    re.IGNORECASE,
)
"""Heuristic for agreement-shaped turn opens per D-IH-76-J §6 friction-injection
contract. Tracks leading affirmation words (EN + ES + FR) at the start of a
Madeira turn. Anti-sycophancy fires when 3+ consecutive turns match this
pattern without an internal counter-option signal (see ``_COUNTER_OPTION_SIGNAL``)."""


_COUNTER_OPTION_SIGNAL = re.compile(
    r"\b(?:counter[-\s]?option|edge case|alternative|trade[-\s]?off|"
    r"risk\s+is|caveat|however|on the other hand|but if|"
    r"reversibility|forward[-\s]?charter)\b",
    re.IGNORECASE,
)
"""Signal that the agreement-shaped turn DID surface a counter-option /
edge case / risk / trade-off — exempts the turn from the sycophancy counter."""


_TURN_SEPARATOR_PATTERN = re.compile(
    r"^(?:---\s*$|##?\s*MADEIRA[:\s]|##?\s*AGENT[:\s]|##?\s*ASSISTANT[:\s])",
    re.IGNORECASE | re.MULTILINE,
)
"""Heuristic for transcript turn boundaries. Splits on horizontal rule (---)
or H1/H2 headings prefixed with MADEIRA/AGENT/ASSISTANT. Operator turns
(prefixed OPERATOR/USER/HUMAN) are NOT counted toward the sycophancy
counter — only Madeira turns are."""


_MADEIRA_TURN_PATTERN = re.compile(
    r"^##?\s*(?:MADEIRA|AGENT|ASSISTANT)[:\s]",
    re.IGNORECASE | re.MULTILINE,
)
"""Identifies Madeira-attributed turns within a transcript so the audit can
distinguish them from operator turns."""


_AUDIENCE_FRONTMATTER_PATTERN = re.compile(
    r"^audience\s*:\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
"""Optional ``audience: X`` frontmatter line for audience mis-routing detection."""


@dataclass
class VoiceAuditFindings:
    """Aggregated findings from a transcript voice-audit pass."""

    bbr_hits: list[BaselineHit] = field(default_factory=list)
    sycophancy_runs: list[tuple[int, int]] = field(default_factory=list)
    """List of (start_turn_index, run_length) tuples; one entry per
    consecutive-agreement run >= threshold."""
    audience_mismatches: list[tuple[str, list[str]]] = field(default_factory=list)
    """List of (declared_audience, allowed_audiences) tuples; one entry per
    mismatch detected."""

    @property
    def total_findings(self) -> int:
        return len(self.bbr_hits) + len(self.sycophancy_runs) + len(self.audience_mismatches)

    @property
    def is_clean(self) -> bool:
        return self.total_findings == 0


# ---------------------------------------------------------------------------
# bbr-scan subcommand (Lane A original behavior; retained as default)
# ---------------------------------------------------------------------------


def _read_input(text_arg: str | None) -> str:
    """Resolve the input text from --text or stdin."""
    if text_arg is not None:
        return text_arg
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read()


def _format_bbr_hits_human(hits: list[BaselineHit]) -> str:
    if not hits:
        return "CLEAN - no internal-register tokens detected."
    lines = [f"FINDINGS - {len(hits)} internal-register hit(s) before showing operator:"]
    for hit in hits:
        lines.append(
            f"  line {hit.line}: token {hit.token.token!r} -- {hit.snippet}"
        )
    lines.append(
        "Translate to external register OR confirm audience is operator-private "
        "before depending on this output."
    )
    return "\n".join(lines)


def _format_bbr_hits_json(hits: list[BaselineHit]) -> dict[str, object]:
    return {
        "verdict": "CLEAN" if not hits else "FINDINGS",
        "findings_count": len(hits),
        "findings": [
            {
                "line": h.line,
                "token": h.token.token,
                "snippet": h.snippet,
            }
            for h in hits
        ],
    }


def _run_bbr_scan(args: argparse.Namespace) -> int:
    text = _read_input(args.text)
    if not text.strip():
        if args.json:
            print(
                json.dumps(
                    {
                        "verdict": "EMPTY_INPUT",
                        "findings_count": 0,
                        "findings": [],
                        "hint": "Pass --text or pipe stdin.",
                    },
                    indent=2,
                )
            )
        else:
            LOG.error("No input. Pass --text 'draft' or pipe a draft via stdin.")
        return 1

    hits = scan_text(text, strip_frontmatter=args.strip_frontmatter)

    if args.json:
        print(json.dumps(_format_bbr_hits_json(hits), indent=2))
    else:
        print(_format_bbr_hits_human(hits))

    return 1 if hits else 0


# ---------------------------------------------------------------------------
# load subcommand (D-IH-76-M per-AIC re-load on session start)
# ---------------------------------------------------------------------------


def _format_profile_human(profile: OperatorVoiceProfile) -> str:
    lines = [
        f"PROFILE LOADED - {profile.profile_id} ({profile.profile_name})",
        f"  description: {profile.description}",
        f"  methodology_version: {profile.methodology_version}",
        f"  traits ({len(profile.traits)}):",
    ]
    for trait in profile.traits:
        lines.append(f"    - {trait}")
    lines.append(f"  audience_constraint ({len(profile.audience_constraint)}):")
    for aud in profile.audience_constraint:
        lines.append(f"    - {aud}")
    lines.append(f"  corpus_paths ({len(profile.corpus_paths)}; FK-only per D-IH-76-K):")
    for path in profile.corpus_paths:
        lines.append(f"    - {path}")
    lines.append(
        f"  anti_sycophancy_threshold: {profile.anti_sycophancy_threshold} consecutive "
        f"agreement turns (D-IH-76-J)"
    )
    lines.append(
        f"  knowledge_test_cadence_days: {profile.knowledge_test_cadence_days} "
        f"(D-IH-76-L; quarterly default)"
    )
    lines.append(
        f"  last_knowledge_test_at: {profile.last_knowledge_test_at or 'never (initial mint state)'}"
    )
    return "\n".join(lines)


def _format_profile_json(profile: OperatorVoiceProfile) -> dict[str, object]:
    return {
        "verdict": "LOADED",
        "profile_id": profile.profile_id,
        "profile_name": profile.profile_name,
        "description": profile.description,
        "methodology_version": profile.methodology_version,
        "traits": list(profile.traits),
        "audience_constraint": list(profile.audience_constraint),
        "corpus_paths": list(profile.corpus_paths),
        "anti_sycophancy_threshold": profile.anti_sycophancy_threshold,
        "knowledge_test_cadence_days": profile.knowledge_test_cadence_days,
        "last_knowledge_test_at": profile.last_knowledge_test_at,
    }


def _run_load(args: argparse.Namespace) -> int:
    profile_id = args.profile_id or _DEFAULT_PROFILE_ID
    try:
        profile = get_profile(profile_id)
    except KeyError as exc:
        if args.json:
            print(
                json.dumps(
                    {
                        "verdict": "UNKNOWN_PROFILE",
                        "profile_id": profile_id,
                        "known_profiles": sorted(STANDARD_VOICE_PROFILES.keys()),
                        "error": str(exc),
                    },
                    indent=2,
                )
            )
        else:
            LOG.error(
                "Unknown profile_id=%r; known: %s",
                profile_id,
                sorted(STANDARD_VOICE_PROFILES.keys()),
            )
        return 1

    if args.json:
        print(json.dumps(_format_profile_json(profile), indent=2))
    else:
        print(_format_profile_human(profile))
    return 0


# ---------------------------------------------------------------------------
# voice-audit subcommand (anti-sycophancy + BBR + audience mis-routing)
# ---------------------------------------------------------------------------


def _split_madeira_turns(text: str) -> list[str]:
    """Split a transcript into Madeira-attributed turns.

    Heuristic: locates lines matching ``_MADEIRA_TURN_PATTERN`` + carves the
    span until the next turn boundary (any header / horizontal rule). When the
    transcript carries no Madeira-turn markers, treats the entire text as one
    Madeira turn (single-turn audit shape).
    """
    turn_starts: list[int] = []
    for match in _MADEIRA_TURN_PATTERN.finditer(text):
        turn_starts.append(match.start())

    if not turn_starts:
        # Single-turn audit shape; treat entire text as one Madeira turn
        return [text.strip()] if text.strip() else []

    turns: list[str] = []
    for i, start in enumerate(turn_starts):
        # Find the body of this turn: everything after the header line, up to
        # the next turn boundary (or end of text).
        body_start = text.find("\n", start)
        if body_start < 0:
            continue
        body_start += 1
        body_end = turn_starts[i + 1] if i + 1 < len(turn_starts) else len(text)
        body = text[body_start:body_end].strip()
        if body:
            turns.append(body)
    return turns


def _detect_sycophancy_runs(turns: list[str], threshold: int) -> list[tuple[int, int]]:
    """Detect runs of >= threshold consecutive agreement-shaped turns
    without a counter-option signal.

    Returns list of (start_turn_index_0_based, run_length) tuples.
    """
    runs: list[tuple[int, int]] = []
    consecutive = 0
    run_start = 0

    def _is_sycophantic(turn: str) -> bool:
        if not _AGREEMENT_LEAD_PATTERN.search(turn):
            return False
        return not _COUNTER_OPTION_SIGNAL.search(turn)

    for idx, turn in enumerate(turns):
        if _is_sycophantic(turn):
            if consecutive == 0:
                run_start = idx
            consecutive += 1
        else:
            if consecutive >= threshold:
                runs.append((run_start, consecutive))
            consecutive = 0
    if consecutive >= threshold:
        runs.append((run_start, consecutive))
    return runs


def _detect_audience_mismatch(
    text: str, profile: OperatorVoiceProfile
) -> list[tuple[str, list[str]]]:
    """Detect audience-frontmatter mis-routing.

    Scans for ``audience: X`` lines. Each declared audience must be either
    (a) in the profile's ``audience_constraint`` OR (b) in the broader
    :data:`STANDARD_AUDIENCE_CONSTRAINTS` v1 set (the J-OP / J-AD-post-NDA /
    J-CO triad). Audiences outside the v1 set are external-register surfaces
    and constitute mis-routing per §4 audience-constraint matrix.
    """
    mismatches: list[tuple[str, list[str]]] = []
    allowed = list(profile.audience_constraint)
    for match in _AUDIENCE_FRONTMATTER_PATTERN.finditer(text):
        raw = match.group(1).strip()
        # audience may be a single value OR a semicolon-list
        declared_values = [v.strip() for v in raw.replace(",", ";").split(";") if v.strip()]
        for declared in declared_values:
            if declared in allowed:
                continue
            if declared in STANDARD_AUDIENCE_CONSTRAINTS:
                # In v1 set but not in this profile's constraint - WARN, not FAIL
                # (e.g., J-OP-only profile reading a J-CO surface)
                mismatches.append((declared, allowed))
            else:
                # Outside v1 set entirely - external audience mis-routing
                mismatches.append((declared, allowed))
    return mismatches


def _format_audit_human(
    findings: VoiceAuditFindings, profile: OperatorVoiceProfile, transcript_path: Path
) -> str:
    lines = [
        f"VOICE AUDIT - transcript: {transcript_path}",
        f"  profile: {profile.profile_id}",
        f"  total findings: {findings.total_findings}",
    ]
    if findings.is_clean:
        lines.append("  verdict: CLEAN - no anti-sycophancy / BBR / audience mismatches detected.")
        return "\n".join(lines)

    lines.append("  --- findings ---")
    if findings.bbr_hits:
        lines.append(
            f"  BBR jargon leaks ({len(findings.bbr_hits)}): internal-register tokens in J-OP-marked surface"
        )
        for hit in findings.bbr_hits[:10]:  # cap display
            lines.append(f"    line {hit.line}: token {hit.token.token!r} -- {hit.snippet}")
        if len(findings.bbr_hits) > 10:
            lines.append(f"    ... and {len(findings.bbr_hits) - 10} more")
    if findings.sycophancy_runs:
        lines.append(
            f"  Anti-sycophancy violations ({len(findings.sycophancy_runs)}; threshold = "
            f"{profile.anti_sycophancy_threshold} consecutive agreement turns per D-IH-76-J):"
        )
        for start, run_len in findings.sycophancy_runs:
            lines.append(
                f"    turn index {start} - run length {run_len} consecutive agreement turns "
                "without counter-option signal"
            )
    if findings.audience_mismatches:
        lines.append(
            f"  Audience-constraint mismatches ({len(findings.audience_mismatches)}; profile allows "
            f"{list(profile.audience_constraint)}):"
        )
        for declared, allowed in findings.audience_mismatches:
            lines.append(
                f"    declared audience: {declared!r}; profile allows: {allowed}"
            )
    return "\n".join(lines)


def _format_audit_json(
    findings: VoiceAuditFindings, profile: OperatorVoiceProfile, transcript_path: Path
) -> dict[str, object]:
    return {
        "verdict": "CLEAN" if findings.is_clean else "FINDINGS",
        "transcript": str(transcript_path),
        "profile_id": profile.profile_id,
        "total_findings": findings.total_findings,
        "bbr_hits": [
            {"line": h.line, "token": h.token.token, "snippet": h.snippet}
            for h in findings.bbr_hits
        ],
        "sycophancy_runs": [
            {"start_turn_index": s, "run_length": rl}
            for s, rl in findings.sycophancy_runs
        ],
        "audience_mismatches": [
            {"declared": d, "allowed": list(a)} for d, a in findings.audience_mismatches
        ],
    }


def _run_voice_audit(args: argparse.Namespace) -> int:
    profile_id = args.profile_id or _DEFAULT_PROFILE_ID
    try:
        profile = get_profile(profile_id)
    except KeyError:
        LOG.error(
            "Unknown profile_id=%r; known: %s",
            profile_id,
            sorted(STANDARD_VOICE_PROFILES.keys()),
        )
        return 1

    transcript_path = Path(args.transcript)
    if not transcript_path.exists():
        LOG.error("Transcript file not found: %s", transcript_path)
        return 1

    text = transcript_path.read_text(encoding="utf-8")

    bbr_hits = scan_text(text, strip_frontmatter=True, file=transcript_path)
    turns = _split_madeira_turns(text)
    sycophancy_runs = _detect_sycophancy_runs(turns, profile.anti_sycophancy_threshold)
    audience_mismatches = _detect_audience_mismatch(text, profile)

    findings = VoiceAuditFindings(
        bbr_hits=bbr_hits,
        sycophancy_runs=sycophancy_runs,
        audience_mismatches=audience_mismatches,
    )

    if args.json:
        print(json.dumps(_format_audit_json(findings, profile, transcript_path), indent=2))
    else:
        print(_format_audit_human(findings, profile, transcript_path))

    # Default = INFO advisory (exit 0 even with findings); --strict = FAIL
    if args.strict and not findings.is_clean:
        return 1
    return 0


# ---------------------------------------------------------------------------
# Argparse wiring
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Madeira voice + personality runbook per I76 P3 SOP-TECH_MADEIRA_PERSONALITY_001. "
            "Three subcommands: bbr-scan (default; per-output BBR self-policing), load "
            "(AIC session-start profile load per D-IH-76-M), voice-audit (transcript-level "
            "anti-sycophancy + BBR-jargon-leak + audience-mis-routing per D-IH-76-G..M)."
        )
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON to stdout (default: human-readable).",
    )
    # Root-level bbr-scan args (Lane A backward-compat: root invocation with
    # --text / stdin runs bbr-scan without an explicit subcommand).
    parser.add_argument(
        "--text",
        type=str,
        default=None,
        help="Text to BBR-scan (root-level shorthand for the bbr-scan subcommand).",
    )
    parser.add_argument(
        "--strip-frontmatter",
        action="store_true",
        help="Blank YAML frontmatter before scanning (per D-IH-89-H operator-metadata exemption).",
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    # bbr-scan subcommand (explicit invocation)
    p_scan = subparsers.add_parser(
        "bbr-scan",
        help=(
            "Per-output BBR self-policing scan (Lane A original behavior). "
            "Pipe a draft via --text or stdin; emits internal-register hits per "
            "BRAND_BASELINE_REALITY_MATRIX.md section 3."
        ),
    )
    p_scan.add_argument("--text", type=str, default=None, help="Text to scan.")
    p_scan.add_argument(
        "--strip-frontmatter",
        action="store_true",
        help="Blank YAML frontmatter before scanning (per D-IH-89-H operator-metadata exemption).",
    )
    p_scan.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON to stdout.",
    )

    # load subcommand
    p_load = subparsers.add_parser(
        "load",
        help=(
            "Load a voice profile (used by AICs at session start per D-IH-76-M). "
            "Prints trait list + audience constraint + corpus paths + cadence."
        ),
    )
    p_load.add_argument(
        "--profile-id",
        type=str,
        default=None,
        help=f"Profile ID to load (default: {_DEFAULT_PROFILE_ID}).",
    )
    p_load.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON to stdout.",
    )

    # voice-audit subcommand
    p_audit = subparsers.add_parser(
        "voice-audit",
        help=(
            "Audit a transcript for anti-sycophancy threshold violations + BBR jargon "
            "leaks + audience-constraint mis-routing per D-IH-76-G..M."
        ),
    )
    p_audit.add_argument(
        "--transcript",
        type=str,
        required=True,
        help="Path to the transcript file to audit.",
    )
    p_audit.add_argument(
        "--profile-id",
        type=str,
        default=None,
        help=f"Profile to audit against (default: {_DEFAULT_PROFILE_ID}).",
    )
    p_audit.add_argument(
        "--strict",
        action="store_true",
        help="Promote findings from INFO advisory to FAIL (exit 1 on any finding).",
    )
    p_audit.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON to stdout.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not args.json:
        setup_logging(level=logging.INFO)

    # Default subcommand = bbr-scan (Lane A backward-compat)
    if args.subcommand is None or args.subcommand == "bbr-scan":
        return _run_bbr_scan(args)
    if args.subcommand == "load":
        return _run_load(args)
    if args.subcommand == "voice-audit":
        return _run_voice_audit(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
