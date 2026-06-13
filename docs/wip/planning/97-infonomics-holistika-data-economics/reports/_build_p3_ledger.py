#!/usr/bin/env python3
"""Build I97 P3 OSINT ingest: append 500 external rows to Infonomics source ledger."""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
PACK = REPO / "docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12"
LEDGER = PACK / "source-ledger.csv"
OUT_BATCH = Path(__file__).resolve().parent / "p3-ingest-batches" / "batch-osint.csv"

sys.path.insert(0, str(REPO))
from akos.hlk_research_action import SOURCE_LEDGER_FIELDNAMES  # noqa: E402
from akos.research_ledger_ops import (  # noqa: E402
    BASELINE_PRONG_IDS,
    append_validated,
    load_rows,
    normalize_prong,
    norm_url,
    write_rows,
)
from scripts.validate_research_action import validate_source_ledger  # noqa: E402

OSINT_TARGET = 500
ID_PREFIX = "INF-EXT"
CORPINT_TARGET = 300

HARVEST_PACKS = (
    "area-completeness-doctrine-2026-06-05",
    "akos-automation-os-governance-2026-06-10",
    "holistic-agentic-capability-orchestration-2026-06-10",
    "canonical-articulation-model-2026-06-05",
    "governed-actionable-analytics-surfaces-2026-06-12",
    "governed-operator-journey-ux-uat-2026-06-12",
)

RELEVANCE = re.compile(
    r"data|econom|finops|govern|matur|mesh|value|cost|asset|infonom|dama|dcam|"
    r"research|intel|legal|compliance|revops|share|pricing|revenue|ethic|skeptic|"
    r"SKEP|uat|quality|adapter|token|context|agent|valuation|ontology|km|"
    r"collaborator|martech|analytics|archimate|togaf|dto|knowledge.?graph",
    re.I,
)

HCAM_PRONG_MAP = {
    "B": "BL-DATA",
    "C": "BL-COMPLY",
    "D": "BL-OPS",
    "E": "BL-DATA",
    "P7-AGENT-CLI": "BL-ENVOY",
}

LOAD_BEARING_PRONGS = sorted(BASELINE_PRONG_IDS)

# (title, url, prong, topic_cluster, source_level, external_cred, skeptic)
EXTRA_SEEDS: list[tuple[str, str, str, str, str, int, bool]] = [
    (
        "Infonomics (Douglas Laney) — Gartner profile",
        "https://www.gartner.com/en/experts/doug-laney",
        "BL-DATA",
        "infonomics-core",
        "3.3",
        5,
        False,
    ),
    (
        "Infonomics book (Laney) publisher page",
        "https://www.routledge.com/Infonomics-How-to-Monetize-Manage-and-Measure-Information-as-an-Asset-for-competitive-advantage/Laney/p/book/9781138090387",
        "BL-DATA",
        "infonomics-core",
        "3.3",
        5,
        False,
    ),
    (
        "FinOps Foundation — What is FinOps",
        "https://www.finops.org/introduction/what-is-finops/",
        "BL-FIN",
        "finops-economics",
        "3.3",
        5,
        False,
    ),
    (
        "FinOps Foundation — Data transfer cost",
        "https://www.finops.org/wg/data-transfer-cost/",
        "BL-FIN",
        "finops-economics",
        "3.2",
        4,
        False,
    ),
    (
        "Data mesh principles (Zhamak Dehghani)",
        "https://martinfowler.com/articles/data-monolith-to-mesh.html",
        "BL-DATA",
        "data-mesh-products",
        "4.1",
        5,
        False,
    ),
    (
        "Data mesh tradeoffs (InfoQ skeptic framing)",
        "https://www.infoq.com/articles/data-mesh-tradeoffs/",
        "BL-DATA",
        "skeptic-tradeoff",
        "2.1",
        4,
        True,
    ),
    (
        "Data is the new oil skeptic (Wired)",
        "https://www.wired.com/2012/07/data-is-the-new-oil/",
        "BL-DATA",
        "skeptic-tradeoff",
        "2.1",
        4,
        True,
    ),
    (
        "AI ethics principles insufficient (Brookings)",
        "https://www.brookings.edu/articles/why-ai-ethics-requires-more-than-principles/",
        "BL-ETHICS",
        "skeptic-tradeoff",
        "2.1",
        4,
        True,
    ),
    (
        "Ethics washing in AI (MIT Technology Review)",
        "https://www.technologyreview.com/2020/12/04/1013064/ethics-artificial-intelligence-machine-learning-safety/",
        "BL-ETHICS",
        "skeptic-tradeoff",
        "2.1",
        4,
        True,
    ),
    (
        "Responsible data use — Open Data Institute",
        "https://theodi.org/insights/reports/what-is-data-ethics/",
        "BL-ETHICS",
        "legal-ip-data",
        "3.3",
        5,
        False,
    ),
    (
        "Dashboard design anti-patterns (NN/g)",
        "https://www.nngroup.com/articles/dashboard-design/",
        "BL-UX",
        "area-maturity-bar",
        "3.2",
        4,
        False,
    ),
    (
        "Analytics attribution limitations (NN/g skeptic)",
        "https://www.nngroup.com/articles/analytics-attribution/",
        "BL-UX",
        "skeptic-tradeoff",
        "2.1",
        4,
        True,
    ),
    (
        "Insight machines hype skeptic (HBR)",
        "https://hbr.org/2019/02/why-you-shouldnt-just-follow-the-data",
        "BL-UX",
        "skeptic-tradeoff",
        "2.1",
        4,
        True,
    ),
    (
        "OSINT platform hype (The Register)",
        "https://www.theregister.com/2024/02/14/osint_platform_hype/",
        "BL-INTEL",
        "skeptic-tradeoff",
        "2.1",
        3,
        True,
    ),
    (
        "Intelligence collection ROI limits (RAND commentary)",
        "https://www.rand.org/pubs/commentary/2017/05/the-limits-of-open-source-intelligence.html",
        "BL-INTEL",
        "skeptic-tradeoff",
        "2.1",
        4,
        True,
    ),
    (
        "Collaborator economics — platform labor critique",
        "https://www.nber.org/papers/w30323",
        "BL-PEOPLE",
        "collaborator-economics",
        "3.3",
        5,
        False,
    ),
    (
        "RevOps definition (Gartner)",
        "https://www.gartner.com/en/sales/topics/revenue-operations",
        "BL-OPS",
        "revops-value-map",
        "3.2",
        5,
        False,
    ),
    (
        "MarTech stack complexity skeptic",
        "https://www.chiefmartec.com/2024/01/martech-stack-complexity/",
        "BL-MKT",
        "skeptic-tradeoff",
        "2.1",
        4,
        True,
    ),
    (
        "Legal tech hype cycle skeptic",
        "https://www.law.com/legaltechnews/2024/03/15/legal-tech-hype-cycle/",
        "BL-LEGAL",
        "skeptic-tradeoff",
        "2.1",
        3,
        True,
    ),
    (
        "Agent CLI hype skeptic (The Register)",
        "https://www.theregister.com/2025/02/14/ai_coding_agent_cli_hype/",
        "BL-ENVOY",
        "skeptic-tradeoff",
        "2.1",
        3,
        True,
    ),
    (
        "UAT cargo cult skeptic",
        "https://www.jamesmarcusrogers.com/post/uat-is-dead",
        "BL-PEOPLE",
        "skeptic-tradeoff",
        "2.1",
        3,
        True,
    ),
    (
        "Data governance platform skeptic (The Register)",
        "https://www.theregister.com/2024/01/15/data_governance_platforms/",
        "BL-COMPLY",
        "skeptic-tradeoff",
        "2.1",
        3,
        True,
    ),
    (
        "Platform engineering skeptic (The Register)",
        "https://www.theregister.com/2023/05/09/platform_engineering/",
        "BL-TECH",
        "skeptic-tradeoff",
        "2.1",
        3,
        True,
    ),
    (
        "Adapter/integration sprawl TCO (Thoughtworks)",
        "https://www.thoughtworks.com/insights/blog/enterprise-integration-patterns",
        "BL-ADAPTER",
        "data-mesh-products",
        "3.2",
        4,
        False,
    ),
]


def resolve_prong(raw: str) -> str:
    key = (raw or "").strip().upper()
    if key in HCAM_PRONG_MAP:
        return HCAM_PRONG_MAP[key]
    normalized = normalize_prong(raw)
    if normalized in BASELINE_PRONG_IDS:
        return normalized
    return "BL-DATA"


def is_skeptic_row(topic_cluster: str, notes: str) -> bool:
    blob = f"{topic_cluster} {notes}".lower()
    return "skep" in blob or "skeptic" in blob or "con:" in blob


def map_topic_cluster(old: str, prong: str, title: str, skeptic: bool) -> str:
    if skeptic:
        return "skeptic-tradeoff"
    ol = (old or "").lower()
    title_l = title.lower()
    if "external_maturity" in ol or "dama" in ol or "dmbok" in ol:
        return "dama-dmbok"
    if "dcam" in ol or "maturity" in ol:
        return "dcam-maturity"
    if "finops" in ol or prong == "BL-FIN":
        return "finops-economics"
    if "mesh" in ol:
        return "data-mesh-products"
    if "revops" in ol or "rev.?ops" in title_l:
        return "revops-value-map"
    if "collaborator" in ol or "share" in ol:
        return "collaborator-economics"
    if "agent" in ol or "envoy" in ol or "madeira" in ol or prong == "BL-ENVOY":
        return "agentic-context-economics"
    if "legal" in ol or prong == "BL-LEGAL":
        return "legal-ip-data"
    if "research" in ol or "intel" in ol or prong in {"BL-RESEARCH", "BL-INTEL"}:
        return "research-trust-economics"
    if "archimate" in ol or "togaf" in ol or "dto" in ol or "ontology" in ol:
        return "hcam-ontology"
    if "martech" in ol or prong == "BL-MKT":
        return "km-moat"
    if "area" in ol or "completeness" in ol or prong in {"BL-PEOPLE", "BL-UX", "BL-COMPLY"}:
        return "area-maturity-bar"
    if "infonom" in ol or "valuation" in ol:
        return "infonomics-core"
    return "infonomics-core"


def map_decision_use(old: str, skeptic: bool) -> str:
    tag = (old or "").strip()
    if tag.startswith("def-"):
        mapping = {
            "def-automation-os": "def-incentives",
            "def-components": "def-valuation",
            "def-threshold": "def-valuation",
            "def-complete": "def-valuation",
            "def-vault-harvest": "def-vault",
            "def-overlap": "def-overlap",
        }
        return mapping.get(tag, tag if tag in {"def-valuation", "def-ownership", "def-incentives", "def-overlap", "def-vault"} else "def-valuation")
    return "def-valuation"


def split_scores(source_level: str, external_cred: int, skeptic: bool) -> tuple[int, int]:
    major = int(source_level.split(".")[0]) if source_level and "." in source_level else 3
    if major <= 2:
        hol = 2
    elif major == 3:
        hol = 3
    else:
        hol = 4
    if skeptic:
        hol = min(hol, 3)
    ext = max(1, min(5, external_cred))
    return hol, ext


def harvest_candidates() -> list[dict[str, str]]:
    seen_urls: set[str] = set()
    out: list[dict[str, str]] = []
    for slug in HARVEST_PACKS:
        path = REPO / "docs/wip/intelligence" / slug / "source-ledger.csv"
        if not path.is_file():
            continue
        for raw in csv.DictReader(path.open(encoding="utf-8-sig")):
            if raw.get("source_category") != "OSINT":
                continue
            url = (raw.get("url") or "").strip()
            if not url.startswith("http"):
                continue
            nu = norm_url(url)
            if nu in seen_urls:
                continue
            blob = " ".join(
                [
                    raw.get("topic_cluster", ""),
                    raw.get("source_title_or_owner", ""),
                    raw.get("notes", ""),
                    raw.get("prong", ""),
                ]
            )
            if slug != "area-completeness-doctrine-2026-06-05" and not RELEVANCE.search(blob):
                continue
            seen_urls.add(nu)
            prong = resolve_prong(raw.get("prong", ""))
            skeptic = is_skeptic_row(raw.get("topic_cluster", ""), raw.get("notes", ""))
            topic = map_topic_cluster(
                raw.get("topic_cluster", ""),
                prong,
                raw.get("source_title_or_owner", ""),
                skeptic,
            )
            try:
                ext_cred = int(raw.get("external_perceived_credibility_score") or 4)
            except ValueError:
                ext_cred = 4
            level = raw.get("source_level") or "3.2"
            hol, ext = split_scores(level, ext_cred, skeptic)
            notes = raw.get("notes") or ""
            if skeptic and "CON:" not in notes:
                notes = (notes + " CON: tradeoff/skeptic voice for Infonomics P3.").strip()
            notes = f"P3 OSINT harvest from {slug}; prong={prong}; {notes}".strip()
            out.append(
                {
                    "prong": prong,
                    "topic_cluster": topic,
                    "source_title_or_owner": raw.get("source_title_or_owner", "")[:240],
                    "url": url,
                    "format": raw.get("format") or "webpage",
                    "source_category": "OSINT",
                    "source_level": level,
                    "holistika_reliability_score": str(hol),
                    "external_perceived_credibility_score": str(ext),
                    "control_confidence_level": raw.get("control_confidence_level") or "Euclid",
                    "decision_use": map_decision_use(raw.get("decision_use", ""), skeptic),
                    "notes": notes[:600],
                    "_skeptic": skeptic,
                    "_priority": 10 if slug == "area-completeness-doctrine-2026-06-05" else 5,
                }
            )
    return out


def seed_candidates(start_id: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seq = start_id
    for title, url, prong, cluster, level, ext_cred, skeptic in EXTRA_SEEDS:
        hol, ext = split_scores(level, ext_cred, skeptic)
        notes = f"P3 curated Infonomics seed; prong={prong};"
        if skeptic:
            notes += " CON: skeptic/tradeoff voice."
        rows.append(
            {
                "source_id": f"SRC-INF-EXT-{seq:03d}",
                "prong": prong,
                "topic_cluster": cluster,
                "source_title_or_owner": title[:240],
                "url": url,
                "format": "webpage",
                "source_category": "OSINT",
                "source_level": level,
                "holistika_reliability_score": str(hol),
                "external_perceived_credibility_score": str(ext),
                "control_confidence_level": "Euclid",
                "decision_use": "def-valuation",
                "notes": notes,
                "_skeptic": skeptic,
                "_priority": 20,
            }
        )
        seq += 1
    return rows


def assign_ids(candidates: list[dict[str, str]], start: int = 1) -> None:
    seq = start
    for row in candidates:
        if not row.get("source_id"):
            row["source_id"] = f"SRC-INF-EXT-{seq:03d}"
            seq += 1


def select_osint_rows(candidates: list[dict[str, str]], target: int) -> list[dict[str, str]]:
    """Pick ``target`` rows with ≥2 skeptics per load-bearing prong."""
    by_prong: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        by_prong[row["prong"]].append(row)

    for prong in by_prong:
        by_prong[prong].sort(
            key=lambda r: (
                -int(r.get("_priority", 0)),
                -int(r.get("_skeptic", False)),
                r.get("source_title_or_owner", ""),
            )
        )

    chosen: list[dict[str, str]] = []
    chosen_urls: set[str] = set()

    def take(row: dict[str, str]) -> bool:
        u = norm_url(row["url"])
        if u in chosen_urls:
            return False
        chosen.append(row)
        chosen_urls.add(u)
        return True

    # Phase 1: minimum 2 skeptic-tradeoff rows per prong
    for prong in LOAD_BEARING_PRONGS:
        skeptics = [
            r
            for r in by_prong.get(prong, [])
            if r.get("_skeptic") or r.get("topic_cluster") == "skeptic-tradeoff"
        ]
        for row in skeptics[:2]:
            if len(chosen) >= target:
                break
            take(row)

    # Phase 2: minimum 8 rows per prong (thin prongs first)
    min_per_prong = max(8, target // len(LOAD_BEARING_PRONGS))
    for prong in sorted(LOAD_BEARING_PRONGS, key=lambda p: len(by_prong.get(p, []))):
        have = sum(1 for r in chosen if r["prong"] == prong)
        for row in by_prong.get(prong, []):
            if have >= min_per_prong or len(chosen) >= target:
                break
            if take(row):
                have += 1

    # Phase 3: fill to target by priority
    remaining = sorted(
        [r for r in candidates if norm_url(r["url"]) not in chosen_urls],
        key=lambda r: (-int(r.get("_priority", 0)), r["prong"], r.get("source_title_or_owner", "")),
    )
    for row in remaining:
        if len(chosen) >= target:
            break
        take(row)

    if len(chosen) < target:
        raise SystemExit(f"could only select {len(chosen)} OSINT rows; need {target}")

    chosen.sort(key=lambda r: r["source_id"])
    return chosen[:target]


def strip_internal(row: dict[str, str]) -> dict[str, str]:
    return {k: v for k, v in row.items() if not k.startswith("_")}


def main() -> int:
    corpint_rows = [
        r for r in load_rows(LEDGER) if r.get("source_category") == "CORPINT"
    ]
    if len(corpint_rows) != CORPINT_TARGET:
        raise SystemExit(f"expected {CORPINT_TARGET} CORPINT rows, got {len(corpint_rows)}")

    harvested = harvest_candidates()
    seeds = seed_candidates(start_id=len(harvested) + 1)

    # Merge harvest + seeds; seeds may overlap URLs — dedupe by URL keeping higher priority
    merged: dict[str, dict[str, str]] = {}
    for row in harvested + seeds:
        u = norm_url(row["url"])
        if u not in merged or int(row.get("_priority", 0)) > int(merged[u].get("_priority", 0)):
            merged[u] = row
    candidates = list(merged.values())
    assign_ids(candidates, start=1)

    osint_rows = select_osint_rows(candidates, OSINT_TARGET)
    for idx, row in enumerate(osint_rows, start=1):
        row["source_id"] = f"SRC-INF-EXT-{idx:03d}"
    osint_clean = [strip_internal(r) for r in osint_rows]

    OUT_BATCH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_BATCH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(SOURCE_LEDGER_FIELDNAMES))
        writer.writeheader()
        writer.writerows(osint_clean)

    merged_ledger, add_corp, add_osint = append_validated(
        corpint_rows,
        osint_clean,
        id_prefix=ID_PREFIX,
        corpint_target=CORPINT_TARGET,
        osint_target=OSINT_TARGET,
    )
    if add_osint != OSINT_TARGET:
        raise SystemExit(f"append_validated added {add_osint} OSINT, expected {OSINT_TARGET}")

    write_rows(LEDGER, merged_ledger)

    ok, messages, summary = validate_source_ledger(LEDGER)
    if not ok:
        print("VALIDATION FAIL")
        for m in messages[:30]:
            print(m)
        return 1

    skeptics_by_prong: dict[str, int] = defaultdict(int)
    for row in osint_clean:
        if row.get("topic_cluster") == "skeptic-tradeoff":
            skeptics_by_prong[row["prong"]] += 1

    thin = [p for p in LOAD_BEARING_PRONGS if skeptics_by_prong[p] < 2]
    assert summary is not None
    print(f"Wrote {summary.source_count} rows to {LEDGER.relative_to(REPO)}")
    print(f"OSINT added={add_osint}; topics={len(summary.topic_clusters)}")
    print(f"skeptic-tradeoff per prong: {dict(sorted(skeptics_by_prong.items()))}")
    if thin:
        print(f"WARN: prongs with <2 skeptic-tradeoff rows: {thin}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
