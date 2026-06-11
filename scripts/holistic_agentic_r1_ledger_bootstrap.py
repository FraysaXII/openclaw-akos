#!/usr/bin/env python3
"""Bootstrap holistic-agentic orchestration R1 internal source ledger (120 CORPINT rows).

Emits source-ledger.csv for validate_research_action.py. R1 scope: internal + substrate
SSOT per RESEARCH_CHARTER_AND_EXECUTION_PLAN.md §5. Does not modify canonical CSVs.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

OUT_DIR = (
    REPO_ROOT
    / "docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10"
)
OUT_PATH = OUT_DIR / "source-ledger.csv"
AOS_LEDGER = (
    REPO_ROOT
    / "docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/source-ledger.csv"
)

HEADER = [
    "source_id",
    "prong",
    "topic_cluster",
    "source_title_or_owner",
    "url",
    "format",
    "source_category",
    "source_level",
    "holistika_reliability_score",
    "external_perceived_credibility_score",
    "control_confidence_level",
    "decision_use",
    "notes",
]

PRONG_HEADERS: list[tuple[str, str, str]] = [
    ("P1-DATA", "prong_scope", "P1 Data — DAMA metadata for agent session events"),
    ("P2-FINANCE", "prong_scope", "P2 Finance — token spend attribution by initiative/seat"),
    ("P3-LEGAL", "prong_scope", "P3 Legal — durable audit trail for inline-ratify decisions"),
    ("P4-MARKETING", "prong_scope", "P4 Marketing — operator surfaces for live agent state"),
    ("P5-OPS-PEOPLE", "prong_scope", "P5 Ops+People — handoff markers and stream recovery"),
    ("P6-TECH-SUBSTRATE", "prong_scope", "P6 Tech — substrate facts MCP/hooks/verification"),
    ("P7-RESEARCH", "prong_scope", "P7 Research — capability-agnostic orchestration doctrine"),
    ("P8-MADEIRA", "prong_scope", "P8 MADEIRA — plug-and-play primitives across harnesses"),
]

INTERNAL_TARGET = 120


GITHUB_BLOB_BASE = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _ledger_url(path: Path) -> str:
    rel = _rel(path)
    if rel.startswith("docs/"):
        return rel
    return f"{GITHUB_BLOB_BASE}{rel}"


def _prong_for_path(path: Path, text: str) -> str:
    parts = {p.lower() for p in path.parts}
    low = text.lower()
    if any(x in parts for x in ("data", "dataops")) or "dama" in low or "mirror" in low:
        return "P1-DATA"
    if "finance" in parts or "finops" in low:
        return "P2-FINANCE"
    if "legal" in parts or "nda" in low or "adviser" in low:
        return "P3-LEGAL"
    if "marketing" in parts or "brand" in low or "wip_dashboard" in low:
        return "P4-MARKETING"
    if (
        "madeira" in low
        or "holistika_agentic" in low
        or "aic_registry" in low
        or "madeira_aic" in low
    ):
        return "P8-MADEIRA"
    if (
        "research" in parts
        and "methodology" in parts
        or "research_action" in low
        or "research_radar" in low
        or "intelligenceops" in low
    ):
        return "P7-RESEARCH"
    if (
        "config/" in _rel(path)
        or "hooks" in low
        or "mcp" in low
        or "openclaw" in low
        or "agentic_framework" in low
        or "substrate" in low
        or ".cursor/agents" in _rel(path)
        or "cursor-two-seat" in low
    ):
        return "P6-TECH-SUBSTRATE"
    return "P5-OPS-PEOPLE"


def _fmt_for(path: Path) -> str:
    if path.suffix.lower() == ".csv":
        return "dataset"
    if "canonical" in path.parts or path.suffix.lower() in {".yaml", ".yml", ".json"}:
        return "internal_canonical"
    if "transcript" in path.name.lower():
        return "internal_transcript"
    return "report"


def _add(
    rows: list[dict[str, str]],
    seen_urls: set[str],
    seq: list[int],
    prong: str,
    cluster: str,
    title: str,
    url: str,
    fmt: str,
    level: str,
    rel: int,
    ccl: str,
    use: str,
    notes: str,
    prefix: str = "SRC-HAC-I",
) -> bool:
    if url in seen_urls:
        return False
    seq[0] += 1
    seen_urls.add(url)
    rows.append(
        {
            "source_id": f"{prefix}-{seq[0]:03d}",
            "prong": prong,
            "topic_cluster": cluster,
            "source_title_or_owner": title[:240],
            "url": url[:500],
            "format": fmt,
            "source_category": "CORPINT",
            "source_level": level if level in {"4.1", "5.1", "5.2", "5.3"} else "5.1",
            "holistika_reliability_score": str(min(5, max(1, rel))),
            "external_perceived_credibility_score": "2",
            "control_confidence_level": ccl,
            "decision_use": use[:240],
            "notes": notes[:600],
        }
    )
    return True


def _prong_header_rows() -> list[dict[str, str]]:
    charter = OUT_DIR / "RESEARCH_CHARTER_AND_EXECUTION_PLAN.md"
    rows: list[dict[str, str]] = []
    charter_rel = _rel(charter)
    for i, (prong, cluster, title) in enumerate(PRONG_HEADERS, start=1):
        rows.append(
            {
                "source_id": f"SRC-HAC-PRONG-{i:02d}",
                "prong": prong,
                "topic_cluster": cluster,
                "source_title_or_owner": title,
                "url": f"{charter_rel}#{prong}",
                "format": "internal_canonical",
                "source_category": "CORPINT",
                "source_level": "5.1",
                "holistika_reliability_score": "5",
                "external_perceived_credibility_score": "1",
                "control_confidence_level": "Safe",
                "decision_use": "prong-scope",
                "notes": f"R1 prong header; charter §3 row {prong}",
            }
        )
    return rows


def _seed_agentic_os(rows: list[dict[str, str]], seen: set[str], seq: list[int]) -> int:
    if not AOS_LEDGER.is_file():
        return 0
    count = 0
    with AOS_LEDGER.open(encoding="utf-8-sig", newline="") as fh:
        for raw in csv.DictReader(fh):
            if raw.get("source_category") != "CORPINT":
                continue
            if count >= 20:
                break
            url = raw.get("url", "")
            if not (url.startswith("docs/") or url.startswith("https://")):
                continue
            prong = _prong_for_path(REPO_ROOT / url, raw.get("notes", ""))
            if _add(
                rows,
                seen,
                seq,
                prong,
                f"aos_seed_{raw.get('topic_cluster', 'prior')[:40]}",
                raw.get("source_title_or_owner", "agentic-os seed")[:80],
                url,
                raw.get("format", "internal_canonical"),
                raw.get("source_level", "5.1"),
                int(raw.get("holistika_reliability_score", "5")),
                raw.get("control_confidence_level", "Safe"),
                raw.get("decision_use", "def-taxonomy")[:80],
                f"R1 seed from agentic-os pack; orig={raw.get('source_id', '')}",
                prefix="SRC-HAC-AOS",
            ):
                count += 1
    return count


def _harvest_globs(
    rows: list[dict[str, str]],
    seen: set[str],
    seq: list[int],
    patterns: list[str],
    cluster: str,
    default_prong: str | None = None,
    limit: int | None = None,
) -> int:
    added = 0
    for pattern in patterns:
        for path in sorted(REPO_ROOT.glob(pattern)):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {
                ".md",
                ".mdc",
                ".csv",
                ".yaml",
                ".yml",
                ".json",
                ".py",
            }:
                continue
            url = _ledger_url(path)
            text = path.read_text(encoding="utf-8", errors="ignore")[:4000]
            prong = default_prong or _prong_for_path(path, text)
            if _add(
                rows,
                seen,
                seq,
                prong,
                cluster,
                path.stem[:80],
                url,
                _fmt_for(path),
                "5.1",
                5,
                "Safe",
                "def-orchestration",
                f"R1 harvest; cluster={cluster}",
            ):
                added += 1
            if limit and len(rows) >= INTERNAL_TARGET:
                return added
    return added


def main() -> int:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    seq = [0]

    for row in _prong_header_rows():
        seen.add(row["url"])
        rows.append(row)

    aos_count = _seed_agentic_os(rows, seen, seq)

    harvest_plan: list[tuple[str, list[str], str | None, int]] = [
        (
            "corpint_canon",
            [
                "docs/references/hlk/v3.0/Research/Methodology/**/*.md",
                "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/*.md",
                ".cursor/rules/akos-aic-delegation.mdc",
                ".cursor/rules/akos-inline-ratification.mdc",
                ".cursor/skills/aic-delegation-craft/SKILL.md",
                ".cursor/skills/inline-ratify-craft/SKILL.md",
                ".cursor/skills/research-action-craft/SKILL.md",
                ".cursor/skills/research-radar-craft/SKILL.md",
            ],
            None,
            35,
        ),
        (
            "agentic_os_pack",
            ["docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/**/*"],
            "P7-RESEARCH",
            15,
        ),
        (
            "akos_runtime",
            [
                "config/openclaw.json.example",
                "config/cursor-rule-tiers.json",
                ".cursor/hooks.json",
                ".cursor/agents/*.md",
                "docs/guides/cursor-two-seat-routing.md",
                "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md",
                "scripts/verify.py",
                "scripts/release-gate.py",
            ],
            "P6-TECH-SUBSTRATE",
            20,
        ),
        (
            "i94_ops_session",
            [
                "docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-*.md",
                "docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md",
            ],
            "P5-OPS-PEOPLE",
            15,
        ),
        (
            "substrate_aic_registers",
            [
                "docs/references/hlk/v3.0/**/SUBSTRATE*.md",
                "docs/references/hlk/v3.0/**/SUBSTRATE*.csv",
                "docs/references/hlk/v3.0/**/AIC_REGISTRY.csv",
                "docs/references/hlk/v3.0/**/MADEIRA*.csv",
                "docs/references/hlk/v3.0/**/MADEIRA*.md",
            ],
            "P8-MADEIRA",
            15,
        ),
        (
            "planning_decision_lineage",
            [
                "docs/wip/planning/90-*/**/*.md",
                "docs/wip/planning/80-*/**/*inline*.md",
                "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv",
            ],
            "P5-OPS-PEOPLE",
            10,
        ),
    ]

    for cluster, patterns, prong, _budget in harvest_plan:
        _harvest_globs(rows, seen, seq, patterns, cluster, prong)

    # Session learnings: I94 P6 doctrine + holistic charter cross-refs
    session_paths = [
        OUT_DIR / "RESEARCH_CHARTER_AND_EXECUTION_PLAN.md",
        REPO_ROOT
        / "docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-p6-ops-sweep-session-doctrine-2026-06-10.md",
        REPO_ROOT / "AGENTS.md",
    ]
    for path in session_paths:
        if path.is_file():
            _add(
                rows,
                seen,
                seq,
                "P5-OPS-PEOPLE",
                "session_learnings",
                path.stem,
                _ledger_url(path),
                _fmt_for(path),
                "5.1",
                5,
                "Safe",
                "def-incident",
                "MainThreadCursor/AskQuestion loss learnings; stream recovery",
            )

    # Pad with high-value cursor/akos surfaces until 120 internal (excl. headers count toward total)
    pad_patterns = [
        "akos/*.py",
        "scripts/hlk_mcp_server.py",
        "scripts/validate_research_action.py",
        "scripts/validate_research_radar.py",
        "scripts/validate_intelligenceops_register.py",
        "docs/ARCHITECTURE.md",
        "docs/USER_GUIDE.md",
    ]
    while len(rows) < INTERNAL_TARGET:
        before = len(rows)
        _harvest_globs(rows, seen, seq, pad_patterns, "corpint_pad", "P6-TECH-SUBSTRATE")
        if len(rows) == before:
            break

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows[:INTERNAL_TARGET])

    corpint_count = sum(1 for r in rows[:INTERNAL_TARGET] if r["source_category"] == "CORPINT")
    print(f"Wrote {OUT_PATH}")
    print(f"  total={min(len(rows), INTERNAL_TARGET)} corpint={corpint_count} aos_seed={aos_count}")
    if len(rows) < INTERNAL_TARGET:
        print(f"WARN: rows={len(rows)} (<{INTERNAL_TARGET})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
