"""Area-completeness validator + sweep runbook (I93 P0).

Canonical doctrine:
``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md``
Paired SOP: ``SOP-PEOPLE_AREA_GOVERNANCE_001.md``
Pydantic SSOT: ``akos/hlk_area_completeness.py``

CLI:
    py scripts/validate_area_completeness.py --self-test
    py scripts/validate_area_completeness.py --matrix
    py scripts/validate_area_completeness.py [--strict]
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import sys
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_area_completeness import (  # noqa: E402
    AREA_KIND_ENTITY,
    CRITICAL_COMPONENT_CODES,
    VALID_AREA_COMPONENT_CODES,
    VALID_SCORED_AREAS,
    VERDICT_TO_LEVEL,
    AreaCompletenessFindingRow,
    AreaCompletenessReport,
    level_ge,
)

O5_ROOT = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1"
COMPLIANCE_DIR = O5_ROOT / "People/Compliance/canonicals"
DIMENSIONS_DIR = COMPLIANCE_DIR / "dimensions"
PEOPLE_CANONICALS = O5_ROOT / "People/canonicals"
QUALITY_FABRIC_PATH = PEOPLE_CANONICALS / "HOLISTIKA_QUALITY_FABRIC.md"
CURSOR_RULES_DIR = REPO_ROOT / ".cursor/rules"
CURSOR_SKILLS_DIR = REPO_ROOT / ".cursor/skills"

PROCESS_LIST_PATH = COMPLIANCE_DIR / "process_list.csv"
BASELINE_ORG_PATH = COMPLIANCE_DIR / "baseline_organisation.csv"
CANONICAL_REGISTRY_PATH = COMPLIANCE_DIR / "CANONICAL_REGISTRY.csv"
PRECEDENCE_PATH = COMPLIANCE_DIR / "PRECEDENCE.md"
CAPABILITY_PATH = DIMENSIONS_DIR / "CAPABILITY_REGISTRY.csv"
CONFIDENCE_PATH = DIMENSIONS_DIR / "CAPABILITY_CONFIDENCE_REGISTRY.csv"

AREA_CONFIG: dict[str, dict[str, object]] = {
    "Data": {"process_area": "Data", "folders": ("Data",)},
    "Tech": {"process_area": "Tech", "folders": ("Tech", "Envoy Tech Lab")},
    "Finance": {"process_area": "Finance", "folders": ("Finance",)},
    "Marketing": {"process_area": "MKT", "folders": ("Marketing",)},
    "Operations": {"process_area": "Operations", "folders": ("Operations",)},
    "People": {"process_area": "People", "folders": ("People",)},
    "Research": {"process_area": "Research", "folders": ("Research",)},
    "Legal": {"process_area": "Legal", "folders": ("People/Legal",)},
}

COMPONENT_ORDER: tuple[str, ...] = tuple(sorted(VALID_AREA_COMPONENT_CODES))


def _today() -> str:
    return _dt.date.today().isoformat()


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _area_roots(area: str) -> list[Path]:
    folders = AREA_CONFIG[area]["folders"]  # type: ignore[index]
    return [O5_ROOT / str(name) for name in folders]  # type: ignore[arg-type]


def _walk_md(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for root in paths:
        if not root.exists():
            continue
        found.extend(root.rglob("*.md"))
    return found


def _row(
    component: str,
    area: str,
    verdict: str,
    evidence: str,
    *,
    action: str = "",
    severity: str = "low",
    notes: str = "",
    level: str | None = None,
    next_action: str = "",
) -> AreaCompletenessFindingRow:
    """Build a v2 finding. criticality / maturity_level / target_level / owner_role
    are auto-derived so v1 probes (01-13) keep their original call signature."""
    crit = "critical" if component in CRITICAL_COMPONENT_CODES else "enhancing"
    lvl = level or VERDICT_TO_LEVEL.get(verdict, "L0")
    target = "L3" if crit == "critical" else "L2"
    owner = str(AREA_KIND_ENTITY.get(area, {}).get("owner_role", ""))
    return AreaCompletenessFindingRow(
        component_code=component,  # type: ignore[arg-type]
        area=area,  # type: ignore[arg-type]
        verdict=verdict,  # type: ignore[arg-type]
        maturity_level=lvl,  # type: ignore[arg-type]
        target_level=target,  # type: ignore[arg-type]
        criticality=crit,  # type: ignore[arg-type]
        evidence_summary=evidence,
        proposed_action=action,
        next_action=next_action or action,
        owner_role=owner,
        severity=severity,  # type: ignore[arg-type]
        notes=notes,
    )


def _probe_area_01(area: str) -> AreaCompletenessFindingRow:
    roots = _area_roots(area)
    if not any(r.exists() for r in roots):
        return _row(
            "AREA-01-PARENT-REDESIGN", area, "gap",
            "O5-1 area folder missing under Admin/O5-1",
            action="Create area folder tree per pattern_area_buildout",
            severity="high",
        )
    subdirs = 0
    for root in roots:
        if root.exists():
            subdirs += sum(1 for c in root.iterdir() if c.is_dir())
    if subdirs >= 1:
        return _row(
            "AREA-01-PARENT-REDESIGN", area, "pass",
            f"area tree present; subdirs={subdirs}",
        )
    return _row(
        "AREA-01-PARENT-REDESIGN", area, "partial",
        "area folder exists but has no role/sub-area subdirectories yet",
        action="Add role-owned subfolders per area charter",
        severity="medium",
    )


def _probe_area_02(area: str) -> AreaCompletenessFindingRow:
    for path in _walk_md(_area_roots(area)):
        name = path.name.upper()
        if "CHARTER" in name and "AREA" in name:
            return _row(
                "AREA-02-AREA-CHARTER", area, "pass",
                f"area charter candidate: {path.relative_to(REPO_ROOT)}",
            )
    if area == "Data":
        return _row(
            "AREA-02-AREA-CHARTER", area, "gap",
            "no *AREA*CHARTER*.md under Data/ (P1 forward-charter)",
            action="Mint DATA_AREA_CHARTER at I93 P1",
            severity="high",
            notes="I93 P0 does not mint Data charter per packet boundary",
        )
    return _row(
        "AREA-02-AREA-CHARTER", area, "gap",
        "no area charter markdown found in area tree",
        action="Mint <AREA>_AREA_CHARTER.md per SOP-PEOPLE_AREA_GOVERNANCE_001",
        severity="high",
    )


def _probe_area_03(area: str) -> AreaCompletenessFindingRow:
    disciplines = [
        p for p in _walk_md(_area_roots(area))
        if p.name.endswith("_DISCIPLINE.md")
    ]
    if disciplines:
        return _row(
            "AREA-03-DISCIPLINE-CHARTERS", area, "pass",
            f"discipline charters={len(disciplines)}",
        )
    governance = [
        p for p in _walk_md(_area_roots(area))
        if "Governance" in str(p) and p.name.endswith(".md")
    ]
    if governance:
        return _row(
            "AREA-03-DISCIPLINE-CHARTERS", area, "partial",
            f"governance markdown={len(governance)}; no *_DISCIPLINE.md",
            severity="medium",
        )
    return _row(
        "AREA-03-DISCIPLINE-CHARTERS", area, "gap",
        "no discipline or governance canonicals detected",
        severity="medium",
    )


def _probe_area_04(area: str) -> AreaCompletenessFindingRow:
    proc_area = str(AREA_CONFIG[area]["process_area"])
    rows = [
        r for r in _read_csv(PROCESS_LIST_PATH)
        if (r.get("area") or "").strip() == proc_area
        and (r.get("item_granularity") or "").strip() == "process"
    ]
    if rows:
        return _row(
            "AREA-04-PROCESS-LIST", area, "pass",
            f"process_list rows (process granularity)={len(rows)}",
        )
    return _row(
        "AREA-04-PROCESS-LIST", area, "gap",
        f"no process_list rows for area column {proc_area!r}",
        severity="high",
    )


def _probe_area_05(area: str) -> AreaCompletenessFindingRow:
    proc_area = str(AREA_CONFIG[area]["process_area"])
    if proc_area == "MKT":
        proc_area = "Marketing"
    rows = [
        r for r in _read_csv(BASELINE_ORG_PATH)
        if (r.get("area") or "").strip() in {proc_area, str(AREA_CONFIG[area]["process_area"])}
    ]
    if rows:
        return _row(
            "AREA-05-BASELINE-ROLES", area, "pass",
            f"baseline_organisation rows={len(rows)}",
        )
    return _row(
        "AREA-05-BASELINE-ROLES", area, "gap",
        "no baseline_organisation roles for area",
        severity="medium",
    )


def _probe_area_06(area: str) -> AreaCompletenessFindingRow:
    proc_area = str(AREA_CONFIG[area]["process_area"])
    cap_rows = [r for r in _read_csv(CAPABILITY_PATH) if (r.get("area") or "").strip() == proc_area]
    cap_ids = {(r.get("capability_id") or "").strip() for r in cap_rows}
    conf_rows = [
        r for r in _read_csv(CONFIDENCE_PATH)
        if (r.get("capability_id") or "").strip() in cap_ids
    ]
    if cap_rows and conf_rows:
        return _row(
            "AREA-06-CAPABILITY-CONFIDENCE", area, "pass",
            f"CAPABILITY={len(cap_rows)} CONFIDENCE={len(conf_rows)}",
        )
    if cap_rows or conf_rows:
        return _row(
            "AREA-06-CAPABILITY-CONFIDENCE", area, "partial",
            f"CAPABILITY={len(cap_rows)} CONFIDENCE={len(conf_rows)}",
            severity="medium",
        )
    return _row(
        "AREA-06-CAPABILITY-CONFIDENCE", area, "gap",
        "no CAPABILITY_REGISTRY rows for area",
        severity="medium",
    )


def _probe_area_07(area: str) -> AreaCompletenessFindingRow:
    proc_area = str(AREA_CONFIG[area]["process_area"])
    needles = list(AREA_CONFIG[area]["folders"]) + [proc_area]  # type: ignore[list-item]
    reg_hits = 0
    for row in _read_csv(CANONICAL_REGISTRY_PATH):
        path = (row.get("file_path") or "").lower()
        owning = (row.get("owning_area") or "")
        if any(n.lower() in path for n in needles) or owning == area:
            reg_hits += 1
    prec_text = ""
    if PRECEDENCE_PATH.exists():
        prec_text = PRECEDENCE_PATH.read_text(encoding="utf-8", errors="replace").lower()
    prec_hits = sum(1 for n in needles if str(n).lower() in prec_text)
    if reg_hits >= 2 and prec_hits >= 1:
        return _row(
            "AREA-07-CANONICAL-PRECEDENCE", area, "pass",
            f"CANONICAL_REGISTRY hits={reg_hits}; PRECEDENCE mentions={prec_hits}",
        )
    if reg_hits >= 1 or prec_hits >= 1:
        return _row(
            "AREA-07-CANONICAL-PRECEDENCE", area, "partial",
            f"CANONICAL_REGISTRY hits={reg_hits}; PRECEDENCE mentions={prec_hits}",
            severity="medium",
        )
    return _row(
        "AREA-07-CANONICAL-PRECEDENCE", area, "gap",
        "sparse CANONICAL_REGISTRY / PRECEDENCE coverage for area",
        severity="medium",
    )


def _probe_area_08(area: str) -> AreaCompletenessFindingRow:
    reg_csvs = 0
    for root in _area_roots(area):
        if not root.exists():
            continue
        reg_csvs += len(list(root.rglob("dimensions/*.csv")))
        reg_csvs += len(list((root / "canonicals").glob("*.csv"))) if (root / "canonicals").exists() else 0
    if reg_csvs >= 2:
        return _row(
            "AREA-08-DIMENSION-REGISTRIES", area, "pass",
            f"dimension/canonical CSV files={reg_csvs}",
        )
    if reg_csvs == 1:
        return _row(
            "AREA-08-DIMENSION-REGISTRIES", area, "partial",
            f"dimension/canonical CSV files={reg_csvs}",
            severity="low",
        )
    return _row(
        "AREA-08-DIMENSION-REGISTRIES", area, "gap",
        "no area-local dimension CSV registries found",
        severity="medium",
    )


def _probe_area_09(area: str) -> AreaCompletenessFindingRow:
    proc_area = str(AREA_CONFIG[area]["process_area"])
    paired = 0
    total = 0
    for row in _read_csv(PROCESS_LIST_PATH):
        if (row.get("area") or "").strip() != proc_area:
            continue
        if (row.get("item_granularity") or "").strip() != "process":
            continue
        total += 1
        sop = (row.get("sop_path") or "").strip()
        runbook = (row.get("runbook_path") or "").strip()
        if sop and runbook:
            paired += 1
    if total == 0:
        return _row(
            "AREA-09-PAIRED-SOP-RUNBOOK", area, "skip",
            "no processes to evaluate (AREA-04 gap)",
            notes="depends on process_list rows",
        )
    if paired == total:
        return _row(
            "AREA-09-PAIRED-SOP-RUNBOOK", area, "pass",
            f"paired processes={paired}/{total}",
        )
    return _row(
        "AREA-09-PAIRED-SOP-RUNBOOK", area, "partial",
        f"paired processes={paired}/{total}",
        action="Fill sop_path + runbook_path per akos-executable-process-catalog Rule 1",
        severity="medium",
    )


def _finops_mirror_repo_gaps() -> list[str]:
    from akos.hlk_dataops_quality import FINOPS_MIRROR_TARGETS, I18_FINOPS_MIRROR_MIGRATION_BASENAME

    migration = REPO_ROOT / "supabase/migrations" / I18_FINOPS_MIRROR_MIGRATION_BASENAME
    sync_script = REPO_ROOT / "scripts/sync_compliance_mirrors_from_csv.py"
    sync_text = sync_script.read_text(encoding="utf-8") if sync_script.is_file() else ""
    gaps: list[str] = []
    if not migration.is_file():
        gaps.append(f"missing {I18_FINOPS_MIRROR_MIGRATION_BASENAME}")
    else:
        mig = migration.read_text(encoding="utf-8")
        for _csv, table, emit_sym in FINOPS_MIRROR_TARGETS:
            if table not in mig:
                gaps.append(f"DDL missing compliance.{table}")
            if emit_sym not in sync_text:
                gaps.append(f"sync missing {emit_sym}")
    return gaps


def _probe_area_10(area: str) -> AreaCompletenessFindingRow:
    if area == "Finance":
        from akos.hlk_dataops_quality import FINOPS_F3_MIRROR_EVIDENCE_REL

        gaps = _finops_mirror_repo_gaps()
        evidence = REPO_ROOT / FINOPS_F3_MIRROR_EVIDENCE_REL
        if gaps:
            return _row(
                "AREA-10-SUPABASE-MIRRORS", area, "gap",
                f"FINOPS mirror spine gaps={len(gaps)}",
                action="Restore I18 migration + finops sync emit",
                severity="medium",
                notes="; ".join(gaps[:3]),
            )
        if evidence.is_file():
            return _row(
                "AREA-10-SUPABASE-MIRRORS", area, "partial",
                "repo-native FINOPS mirror DDL+emit; F3 evidence on disk",
                notes="live row-count parity requires operator SQL apply per holistika-ops",
            )
        return _row(
            "AREA-10-SUPABASE-MIRRORS", area, "partial",
            "repo-native FINOPS mirror DDL+emit verified",
            notes="file F3 execution evidence after tranche close",
        )
    return _row(
        "AREA-10-SUPABASE-MIRRORS", area, "skip",
        "mirror parity requires live Supabase MCP/SQL evidence",
        notes="conservative skip per I93 P0; probe at area-buildout close",
    )


def _probe_area_11(area: str) -> AreaCompletenessFindingRow:
    slug = area.lower().replace(" ", "-")
    if area == "Tech":
        rule_candidates = list(CURSOR_RULES_DIR.glob("akos-*tech*.mdc"))
        skill_candidates = list(CURSOR_SKILLS_DIR.glob("*tech*"))
    else:
        rule_candidates = list(CURSOR_RULES_DIR.glob(f"akos-{slug}*.mdc"))
        skill_candidates = list(CURSOR_SKILLS_DIR.glob(f"{slug}*"))
    if area == "People":
        rule_candidates = list(CURSOR_RULES_DIR.glob("akos-people*.mdc")) + list(
            CURSOR_RULES_DIR.glob("akos-area-governance.mdc")
        )
        skill_candidates = list(CURSOR_SKILLS_DIR.glob("area-governance-craft")) + list(
            CURSOR_SKILLS_DIR.glob("*people*")
        )
    if rule_candidates and skill_candidates:
        return _row(
            "AREA-11-CURSOR-RULE-SKILL", area, "pass",
            f"rules={len(rule_candidates)} skills={len(skill_candidates)}",
        )
    if rule_candidates or skill_candidates:
        return _row(
            "AREA-11-CURSOR-RULE-SKILL", area, "partial",
            f"rules={len(rule_candidates)} skills={len(skill_candidates)}",
            severity="low",
        )
    return _row(
        "AREA-11-CURSOR-RULE-SKILL", area, "gap",
        "no matched cursor rule + skill pair for area",
        severity="low",
    )


def _probe_area_12(area: str) -> AreaCompletenessFindingRow:
    text = ""
    if QUALITY_FABRIC_PATH.exists():
        text = QUALITY_FABRIC_PATH.read_text(encoding="utf-8", errors="replace")
    if not text:
        return _row(
            "AREA-12-QUALITY-FABRIC", area, "blocked",
            "HOLISTIKA_QUALITY_FABRIC.md unreadable",
            severity="high",
        )
    if area == "People" and "compose_AREA" in text:
        return _row(
            "AREA-12-QUALITY-FABRIC", area, "pass",
            "compose_AREA specialty row present (meta-process owner)",
        )
    discipline_hits = [
        p.name for p in _walk_md(_area_roots(area))
        if p.name.endswith("_DISCIPLINE.md")
    ]
    if discipline_hits:
        mentioned = sum(1 for d in discipline_hits if d.replace("_DISCIPLINE.md", "") in text)
        if mentioned >= 1:
            return _row(
                "AREA-12-QUALITY-FABRIC", area, "pass",
                f"Quality Fabric mentions area disciplines ({mentioned})",
            )
        return _row(
            "AREA-12-QUALITY-FABRIC", area, "partial",
            f"area disciplines={len(discipline_hits)} not all cited in §6 table",
            severity="low",
        )
    return _row(
        "AREA-12-QUALITY-FABRIC", area, "partial",
        "no area discipline canonical to cross-check against §6",
        severity="low",
    )


def _probe_area_13(area: str) -> AreaCompletenessFindingRow:
    readmes = []
    for root in _area_roots(area):
        if (root / "README.md").exists():
            readmes.append(root / "README.md")
    if readmes:
        return _row(
            "AREA-13-AREA-README", area, "pass",
            f"README.md present ({len(readmes)} root(s))",
        )
    return _row(
        "AREA-13-AREA-README", area, "gap",
        "missing area README.md index",
        action="Add README.md at area root per pattern_area_buildout",
        severity="medium",
    )


# Known discipline-name prefixes that belong to a specific area (drift detector for AREA-15).
DRIFT_PREFIX_TO_AREA: dict[str, str] = {
    "MKTOPS": "Marketing",
    "TECHOPS": "Tech",
    "DATAOPS": "Data",
    "UX": "Marketing",
}
# Structural / non-role subfolders allowed by the file-plan (AREA-16) without a role FK.
FILE_PLAN_STRUCTURAL_DIRS: frozenset[str] = frozenset({
    "canonicals", "dimensions", "programs", "_templates", "_assets", "_validators",
    "imports", "sourcing-briefs", "business-strategy", "people-files", "MADEIRA-AKOS",
    "External Repos", "historical-AIC", "wip",
    # Area-specific structural folders (governance canonicals home; not a role sub-area)
    "Governance",
})
DATA_CONTRACT_PATH = O5_ROOT / "Data/Governance/canonicals/dimensions/DATA_CONTRACT_REGISTRY.csv"


def _probe_area_14(area: str) -> AreaCompletenessFindingRow:
    """AREA-14 (v2): kind + entity declared (+ inherited_pattern adoption preserved from v1)."""
    profile = AREA_KIND_ENTITY.get(area, {})
    proc_area = str(AREA_CONFIG[area]["process_area"])
    inherited = [
        r for r in _read_csv(PROCESS_LIST_PATH)
        if (r.get("area") or "").strip() == proc_area
        and (r.get("inherited_pattern_id") or "").strip()
    ]
    if not profile:
        return _row(
            "AREA-14-KIND-ENTITY", area, "gap",
            "no kind/entity declared for area in AREA_KIND_ENTITY",
            action="Declare area kind + entity per AREA_GOVERNANCE_DISCIPLINE v2 §2",
            severity="high", level="L0",
            next_action="Add area to AREA_KIND_ENTITY map (kind + entity + owner_role)",
        )
    kind = profile.get("kind", "?")
    entity = profile.get("entity", "?")
    if inherited:
        return _row(
            "AREA-14-KIND-ENTITY", area, "pass",
            f"kind={kind}; entity={entity}; inherited_pattern rows={len(inherited)}",
            level="L3",
        )
    return _row(
        "AREA-14-KIND-ENTITY", area, "partial",
        f"kind={kind}; entity={entity}; no inherited_pattern_id rows yet",
        severity="medium", level="L2",
        next_action="Set inherited_pattern_id=pattern_area_buildout on area process rows",
    )


def _probe_area_15(area: str) -> AreaCompletenessFindingRow:
    """AREA-15 (v2 NEW): placement integrity — no drifted disciplines + ships a contract."""
    drift: list[str] = []
    for path in _walk_md(_area_roots(area)):
        if not path.name.endswith("_DISCIPLINE.md"):
            continue
        prefix = path.name.replace("_DISCIPLINE.md", "").upper()
        mapped = DRIFT_PREFIX_TO_AREA.get(prefix)
        if mapped and mapped != area:
            # Skip deprecation-alias stubs (migration scaffolding per the D-IH-93-C
            # one-cycle relocation pattern) — they are not live drift.
            head = path.read_text(encoding="utf-8", errors="replace")[:400].lower()
            if "status: deprecated" in head or "deprecation_alias" in head:
                continue
            drift.append(f"{path.name}->{mapped}")
    # Area-name aliases so the contract detector recognises domain-coded contracts
    # (e.g. Finance ships DC-HOL-FINOPS-* rows; Data ships DC-HOL-* producer rows).
    contract_aliases: dict[str, tuple[str, ...]] = {
        "Finance": ("finance", "finops"),
        "Data": ("data", "dataops", "dc-hol"),
        "Marketing": ("marketing", "mkt", "mktops", "brand"),
        "Tech": ("tech", "techops", "envoy"),
        "Operations": ("operations", "revops", "smo", "pmo"),
        "People": ("people", "compliance"),
        "Research": ("research", "intelligenceops", "osint", "humint"),
        "Legal": ("legal", "legalops", "advops"),
    }
    aliases = contract_aliases.get(area, (area.lower(),))
    contract_rows = 0
    for row in _read_csv(DATA_CONTRACT_PATH):
        blob = " ".join(str(v) for v in row.values()).lower()
        if any(a in blob for a in aliases):
            contract_rows += 1
    if drift:
        return _row(
            "AREA-15-PLACEMENT-INTEGRITY", area, "gap",
            f"misplaced disciplines={len(drift)} ({'; '.join(drift[:3])})",
            action="Migrate drifted disciplines to their owning area",
            severity="high", level="L0",
            next_action=f"git mv the {len(drift)} drifted *_DISCIPLINE.md out of {area} to their area",
        )
    if contract_rows >= 1:
        return _row(
            "AREA-15-PLACEMENT-INTEGRITY", area, "pass",
            f"no placement drift; cross-area contract rows={contract_rows}",
            level="L3",
        )
    return _row(
        "AREA-15-PLACEMENT-INTEGRITY", area, "partial",
        "no placement drift, but no consumed cross-area contract yet",
        severity="medium", level="L2",
        next_action="Mint >=1 DATA_CONTRACT_REGISTRY row with this area as producer/consumer",
    )


def _probe_area_16(area: str) -> AreaCompletenessFindingRow:
    """AREA-16 (v2 NEW): file-plan — area sub-folders FK to baseline_organisation role/sub_area.

    Resolution order: sub_area column (exact) > role_name (exact) > role_name keyword
    (strips common prefixes/suffixes: Lead/Data/Senior/Manager/Specialist/Analyst to get
    the functional form). This handles the 'Data Governance Lead' -> folder 'Governance'
    case without requiring a roster rename (forward-charter: deprecate 'Lead' naming).
    """
    proc_area = str(AREA_CONFIG[area]["process_area"])
    match_areas = {proc_area, area}
    if proc_area == "MKT":
        match_areas.add("Marketing")
    # Build the set of valid folder names from roster: sub_area values + role_name + keywords
    names: set[str] = set()
    STRIP_TOKENS = {"lead", "senior", "data", "manager", "specialist", "analyst", "holistik"}
    for r in _read_csv(BASELINE_ORG_PATH):
        if (r.get("area") or "").strip() in match_areas:
            # sub_area (primary FK source)
            sub = (r.get("sub_area") or "").strip().lower()
            if sub:
                names.add(sub)
            # role_name (exact)
            role = (r.get("role_name") or "").strip().lower()
            if role:
                names.add(role)
            # role_name keyword extraction (functional form)
            tokens = [t for t in role.split() if t not in STRIP_TOKENS and t != area.lower()]
            if tokens:
                names.add(" ".join(tokens))
    subdirs: list[str] = []
    for root in _area_roots(area):
        if root.exists():
            subdirs.extend(
                c.name for c in root.iterdir()
                if c.is_dir() and c.name not in FILE_PLAN_STRUCTURAL_DIRS
            )
    if not subdirs:
        return _row(
            "AREA-16-FILE-PLAN", area, "partial",
            "no role-named sub-folders to evaluate (flat area tree)",
            severity="low", level="L1",
            next_action="Create role-named sub-folders per baseline_organisation (RACI)",
        )
    matched = [d for d in subdirs if d.strip().lower() in names]
    if len(matched) == len(subdirs):
        return _row(
            "AREA-16-FILE-PLAN", area, "pass",
            f"all {len(subdirs)} sub-folders FK to role/sub_area",
            level="L3",
        )
    orphan = [d for d in subdirs if d.strip().lower() not in names]
    return _row(
        "AREA-16-FILE-PLAN", area, "partial",
        f"sub-folder=role match {len(matched)}/{len(subdirs)}; orphans={orphan[:3]}",
        severity="medium", level="L1",
        next_action=f"Rename/relocate orphan sub-folders to role names: {orphan[:3]}",
    )


PROBE_BY_COMPONENT: dict[str, Callable[[str], AreaCompletenessFindingRow]] = {
    "AREA-01-PARENT-REDESIGN": _probe_area_01,
    "AREA-02-AREA-CHARTER": _probe_area_02,
    "AREA-03-DISCIPLINE-CHARTERS": _probe_area_03,
    "AREA-04-PROCESS-LIST": _probe_area_04,
    "AREA-05-BASELINE-ROLES": _probe_area_05,
    "AREA-06-CAPABILITY-CONFIDENCE": _probe_area_06,
    "AREA-07-CANONICAL-PRECEDENCE": _probe_area_07,
    "AREA-08-DIMENSION-REGISTRIES": _probe_area_08,
    "AREA-09-PAIRED-SOP-RUNBOOK": _probe_area_09,
    "AREA-10-SUPABASE-MIRRORS": _probe_area_10,
    "AREA-11-CURSOR-RULE-SKILL": _probe_area_11,
    "AREA-12-QUALITY-FABRIC": _probe_area_12,
    "AREA-13-AREA-README": _probe_area_13,
    "AREA-14-KIND-ENTITY": _probe_area_14,
    "AREA-15-PLACEMENT-INTEGRITY": _probe_area_15,
    "AREA-16-FILE-PLAN": _probe_area_16,
}


def run_sweep(
    *,
    sweep_trigger: str = "on_demand",
    swept_by: str = "agent:validate_area_completeness",
    areas: tuple[str, ...] | None = None,
) -> AreaCompletenessReport:
    """Score each area against the 14-component bar."""
    target_areas = areas or tuple(sorted(VALID_SCORED_AREAS))
    findings: list[AreaCompletenessFindingRow] = []
    for area in target_areas:
        for code in COMPONENT_ORDER:
            findings.append(PROBE_BY_COMPONENT[code](area))

    pass_count = sum(1 for f in findings if f.verdict == "pass")
    partial_count = sum(1 for f in findings if f.verdict == "partial")
    gap_count = sum(1 for f in findings if f.verdict == "gap")
    blocked_count = sum(1 for f in findings if f.verdict == "blocked")
    skip_count = sum(1 for f in findings if f.verdict == "skip")

    return AreaCompletenessReport(
        report_id=f"area-completeness-{_today()}",
        sweep_trigger=sweep_trigger,  # type: ignore[arg-type]
        swept_at=_today(),
        swept_by=swept_by,
        findings=findings,
        pass_count=pass_count,
        partial_count=partial_count,
        gap_count=gap_count,
        blocked_count=blocked_count,
        skip_count=skip_count,
        total_findings=len(findings),
    )


def _score_label(pass_n: int, partial_n: int, gap_n: int, total: int) -> str:
    if total == 0:
        return "n/a"
    weighted = pass_n + 0.5 * partial_n
    pct = int(round(100 * weighted / total))
    return f"{pct}%"


def print_matrix(report: AreaCompletenessReport) -> None:
    """Emit area × component score table to stdout."""
    by_area: dict[str, list[AreaCompletenessFindingRow]] = {
        a: [] for a in VALID_SCORED_AREAS
    }
    for f in report.findings:
        by_area[f.area].append(f)

    print("Area completeness matrix (v2 — 16-component x L0-L5 maturity grid; D-IH-94-A)")
    print(f"sweep: {report.report_id} trigger={report.sweep_trigger} at={report.swept_at}")
    print("")
    header = ["area", "kind", "pass", "partial", "gap", "skip", "score", "crit@L3", "tier"]
    print("| " + " | ".join(header) + " |")
    print("| " + " | ".join(["---"] * len(header)) + " |")
    for area in sorted(VALID_SCORED_AREAS):
        rows = by_area[area]
        pass_n = sum(1 for r in rows if r.verdict == "pass")
        partial_n = sum(1 for r in rows if r.verdict == "partial")
        gap_n = sum(1 for r in rows if r.verdict == "gap")
        skip_n = sum(1 for r in rows if r.verdict == "skip")
        blocked_n = sum(1 for r in rows if r.verdict == "blocked")
        scored = [r for r in rows if r.verdict not in ("skip", "blocked")]
        score = _score_label(pass_n, partial_n, gap_n, len(scored))
        crit_rows = [r for r in rows if r.criticality == "critical"]
        crit_ok = sum(1 for r in crit_rows if level_ge(r.maturity_level, "L3"))
        tier = "COMPLETE" if crit_ok == len(crit_rows) and crit_rows else "INCOMPLETE"
        kind = str(AREA_KIND_ENTITY.get(area, {}).get("kind", "?"))
        print(
            f"| {area} | {kind} | {pass_n} | {partial_n} | {gap_n} | {skip_n} | "
            f"{score} | {crit_ok}/{len(crit_rows)} | {tier} |"
        )
    print("")
    print("Component detail (non-pass only):")
    for f in report.findings:
        if f.verdict in ("pass", "skip"):
            continue
        print(
            f"  {f.area} {f.component_code} {f.verdict} ({f.severity}): "
            f"{f.evidence_summary}"
        )


def print_worklist(report: AreaCompletenessReport, *, area_filter: str | None = None) -> None:
    """Action-emitting output: ranked next-actions (critical-first) to raise areas to tier.

    This is the activation lever — the tool emits the worklist, not just the diagnosis,
    so a human OR an AIC can execute it directly (AC-HUMAN / AC-AUTOMATION).
    """
    items = [
        f for f in report.findings
        if f.verdict not in ("skip",)
        and not level_ge(f.maturity_level, f.target_level)
        and (area_filter is None or f.area == area_filter)
    ]
    # critical first, then by area, then component
    items.sort(key=lambda f: (f.criticality != "critical", f.area, f.component_code))
    print("Area-governance worklist (v2 — ranked next-actions; critical-first)")
    print(f"sweep: {report.report_id}; items={len(items)}"
          + (f"; area={area_filter}" if area_filter else ""))
    print("")
    header = ["area", "component", "crit", "now", "->", "tgt", "owner", "next_action"]
    print("| " + " | ".join(header) + " |")
    print("| " + " | ".join(["---"] * len(header)) + " |")
    for f in items:
        crit = "CRIT" if f.criticality == "critical" else "enh"
        nxt = (f.next_action or f.proposed_action or f.evidence_summary).replace("|", "/")
        print(
            f"| {f.area} | {f.component_code} | {crit} | {f.maturity_level} | -> | "
            f"{f.target_level} | {f.owner_role} | {nxt} |"
        )


def self_test() -> int:
    """Pydantic fixture + probe registry validation."""
    fixture = AreaCompletenessFindingRow(
        component_code="AREA-02-AREA-CHARTER",
        area="People",
        verdict="pass",
        evidence_summary="self-test fixture",
        severity="low",
    )
    rep = AreaCompletenessReport(
        report_id="area-completeness-2026-06-04-selftest",
        sweep_trigger="pre_commit_self_test",
        swept_at="2026-06-04",
        swept_by="self_test",
        findings=[fixture],
        pass_count=1,
        partial_count=0,
        gap_count=0,
        blocked_count=0,
        skip_count=0,
        total_findings=1,
    )
    if rep.total_findings != 1:
        return 1
    if set(PROBE_BY_COMPONENT) != VALID_AREA_COMPONENT_CODES:
        return 2
    if len(AREA_CONFIG) != len(VALID_SCORED_AREAS):
        return 3
    live = run_sweep(sweep_trigger="pre_commit_self_test", swept_by="self_test")
    expected = len(VALID_SCORED_AREAS) * len(VALID_AREA_COMPONENT_CODES)
    if live.total_findings != expected:
        return 4
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--matrix", action="store_true", help="print area score table")
    parser.add_argument("--next", action="store_true", help="print ranked next-action worklist")
    parser.add_argument("--area", type=str, default=None, help="limit to one area (e.g. Finance)")
    parser.add_argument("--strict", action="store_true", help="exit 1 on gap/blocked findings")
    args = parser.parse_args()

    if args.self_test:
        code = self_test()
        if code == 0:
            print("validate_area_completeness: self-test PASS")
        else:
            print(f"validate_area_completeness: self-test FAIL (code={code})", file=sys.stderr)
        return code

    sweep_areas = (args.area,) if args.area and args.area in VALID_SCORED_AREAS else None
    report = run_sweep(areas=sweep_areas)
    if args.next:
        print_worklist(report, area_filter=args.area if sweep_areas is None else None)
    elif args.matrix:
        print_matrix(report)
    else:
        print(
            f"validate_area_completeness: total={report.total_findings} "
            f"pass={report.pass_count} partial={report.partial_count} "
            f"gap={report.gap_count} blocked={report.blocked_count} "
            f"skip={report.skip_count}"
        )

    if args.strict and (report.gap_count or report.blocked_count):
        print(
            "STRICT MODE FAIL: gap or blocked findings surfaced. "
            "Re-run with --matrix for the area table.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
