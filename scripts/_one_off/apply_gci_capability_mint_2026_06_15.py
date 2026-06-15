#!/usr/bin/env python3
"""One-off: apply GCI capability mint tranche T1-cap (D-IH-76-CAP-GCI)."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAP_PATH = ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv"
ACIM_PATH = ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv"
XW_WIP = ROOT / "docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/wip/CAPABILITY_ALPHA_CROSSWALK.csv"
XW_VAULT = ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_ALPHA_CROSSWALK.csv"
DECISION_PATH = ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv"

SUBSTRATE_BACKFILL = {
    "CAP-CONVERSATIONAL-AI-ENGINE": "SUBS-HOLISTIKA-OPENCLAW-WINDOWS",
    "CAP-AGENTIC-OPERATIONS": "SUBS-ANYSPHERE-CURSOR-SDK",
    "CAP-AI-PERSONA-PERSONALITY": "SUBS-HOLISTIKA-OPENCLAW",
    "CAP-KNOWLEDGE-RETRIEVAL-RAG": "SUBS-HOLISTIKA-LLAMAINDEX-WORKER",
    "CAP-AI-EVALUATION-BENCHMARKING": "SUBS-HOLISTIKA-OPENCLAW",
    "CAP-AI-AGENT-ORCHESTRATION": "SUBS-HOLISTIKA-OPENCLAW",
    "CAP-MADEIRA-SCENARIO-LIFECYCLE": "SUBS-ANYSPHERE-CURSOR-SDK",
    "CAP-AGENTIC-INFRA-OPS": "SUBS-HOLISTIKA-OPENCLAW-WINDOWS",
    "CAP-RES-DEEP-METHODOLOGY": "SUBS-HOLISTIKA-OPENCLAW",
    "CAP-RES-KB-PIPELINE-RADAR": "SUBS-HOLISTIKA-KIRBE",
    "CAP-CANONICAL-GOVERNANCE": "SUBS-ANYSPHERE-CURSOR-SDK",
    "CAP-CLOSURE-ASSURANCE-GOVERNANCE": "SUBS-ANYSPHERE-CURSOR-SDK",
    "CAP-PRECOMMIT-SYNTHESIS-DISCIPLINE": "SUBS-ANYSPHERE-CURSOR-SDK",
    "CAP-TECHOPS-RELIABILITY-OBSERVABILITY": "SUBS-HOLISTIKA-OPENCLAW",
    "CAP-API-LIFECYCLE-GOVERNANCE": "SUBS-HOLISTIKA-OPENCLAW",
    "CAP-MULTIPLATFORM-DEPLOYMENT": "SUBS-VERCEL-VERCEL-AI-SDK",
}

NEW_ROWS = [
    {
        "capability_id": "CAP-MADEIRA-INTERACTION-MODE-PARITY",
        "capability_name": "MADEIRA Interaction Mode Parity",
        "area": "Tech",
        "role_owner": "AI Engineer",
        "originating_process_ids": "env_tech_dtp_madeira_lifecycle;gtm_madeira_dtp_51",
        "substrate_id": "SUBS-ANYSPHERE-CURSOR-SDK",
        "skill_ids": "",
        "lifecycle_status": "active",
        "i81_verdict": "",
        "i81_gap_summary": "",
        "external_register_summary": "",
        "last_review_at": "2026-06-15",
        "last_review_by": "Data Governance Office",
        "last_review_decision_id": "D-IH-76-CAP-GCI",
        "methodology_version_at_review": "v3.2",
        "notes": "Five MADEIRA modes Ask/Plan/Agent/Debug/Methodology per MADEIRA_MODE_PARITY.md; alpha CAP-M02.",
        "capability_tier": "differentiating",
        "l1_domain": "Applied AI & MADEIRA",
        "definition": "Deliver and enforce five governed interaction modes with per-mode RBAC posture and transition rules.",
        "alpha_inventory_refs": "CAP-M02",
    },
    {
        "capability_id": "CAP-MADEIRA-TOOL-CATEGORY-RBAC",
        "capability_name": "MADEIRA Tool Category RBAC",
        "area": "Tech",
        "role_owner": "System Owner",
        "originating_process_ids": "SOP-MCP_SERVER_DEFINITION;env_tech_dtp_openclaw_runtime_health_triage_001",
        "substrate_id": "SUBS-HOLISTIKA-OPENCLAW",
        "skill_ids": "",
        "lifecycle_status": "active",
        "i81_verdict": "",
        "i81_gap_summary": "",
        "external_register_summary": "",
        "last_review_at": "2026-06-15",
        "last_review_by": "Data Governance Office",
        "last_review_decision_id": "D-IH-76-CAP-GCI",
        "methodology_version_at_review": "v3.2",
        "notes": "16 tool-category RBAC per MADEIRA_TOOL_RBAC.csv; alpha CAP-M03.",
        "capability_tier": "differentiating",
        "l1_domain": "Applied AI & MADEIRA",
        "definition": "Block wrong-mode tool calls deterministically via governed tool-category permission matrix.",
        "alpha_inventory_refs": "CAP-M03",
    },
    {
        "capability_id": "CAP-MADEIRA-RESEARCH-CENTER-SURFACE",
        "capability_name": "MADEIRA Research Center Surface",
        "area": "Tech",
        "role_owner": "AI Engineer",
        "originating_process_ids": "hol_peopl_dtp_uat_visual_evidence_001;env_tech_dtp_256",
        "substrate_id": "SUBS-HOLISTIKA-LLAMAINDEX-WORKER",
        "skill_ids": "",
        "lifecycle_status": "active",
        "i81_verdict": "",
        "i81_gap_summary": "",
        "external_register_summary": "",
        "last_review_at": "2026-06-15",
        "last_review_by": "Data Governance Office",
        "last_review_decision_id": "D-IH-76-CAP-GCI",
        "methodology_version_at_review": "v3.2",
        "notes": "Research Center UI (I96 Scenario B); alpha CAP-M07.",
        "capability_tier": "differentiating",
        "l1_domain": "Applied AI & MADEIRA",
        "definition": "Render governed Research Center panels for operator and director POVs with live or stubbed BFF data.",
        "alpha_inventory_refs": "CAP-M07",
    },
    {
        "capability_id": "CAP-MADEIRA-CONTEXT-ECONOMICS",
        "capability_name": "MADEIRA Context Economics & Metered Context",
        "area": "Tech",
        "role_owner": "System Owner",
        "originating_process_ids": "hol_peopl_talent_a_aic_dispatcher_001;env_tech_dtp_agentic_infra_ops_001",
        "substrate_id": "SUBS-HOLISTIKA-OPENCLAW",
        "skill_ids": "",
        "lifecycle_status": "planned",
        "i81_verdict": "",
        "i81_gap_summary": "",
        "external_register_summary": "",
        "last_review_at": "2026-06-15",
        "last_review_by": "Data Governance Office",
        "last_review_decision_id": "D-IH-76-CAP-GCI",
        "methodology_version_at_review": "v3.2",
        "notes": "Cache/compaction/postprocess per context-economics-wip-spec; alpha CAP-M16..M18; T2 code scheduled.",
        "capability_tier": "differentiating",
        "l1_domain": "Applied AI & MADEIRA",
        "definition": "Govern prompt cache boundaries, session compaction, and output postprocessing so context spend is metered and trustworthy.",
        "alpha_inventory_refs": "CAP-M16;CAP-M17;CAP-M18",
    },
]

ACIM_NEW = [
    ("ACIM-0013", "CAP-CONVERSATIONAL-AI-ENGINE", "AIC-MADEIRA-ON-CURSOR", "implemented", "Governed IDE chat via OpenClaw gateway + Cursor rules", ".cursor/rules/akos-operator-communication.mdc; scripts/openclaw_gateway_repair.py", "", "confirmed", "Alpha CAP-M01 primary."),
    ("ACIM-0014", "CAP-AGENTIC-OPERATIONS", "AIC-MADEIRA-ON-CURSOR", "implemented", "Two-seat routing + AIC lifecycle per OPERATOR_STEERING", "docs/wip/planning/OPERATOR_STEERING_AND_CARRYOVER.md; .cursor/rules/akos-aic-delegation.mdc", "", "confirmed", "Alpha CAP-M01 supplement + CAP-M13."),
    ("ACIM-0015", "CAP-MADEIRA-INTERACTION-MODE-PARITY", "AIC-MADEIRA-ON-CURSOR", "implemented", "Five-mode parity SOP + coverage matrix", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_MODE_PARITY.md", "", "confirmed", "Alpha CAP-M02."),
    ("ACIM-0016", "CAP-MADEIRA-TOOL-CATEGORY-RBAC", "AIC-MADEIRA-ON-CURSOR", "implemented", "16-category tool RBAC validator", "scripts/validate_madeira_tool_rbac.py; MADEIRA_TOOL_RBAC.csv", "", "confirmed", "Alpha CAP-M03."),
    ("ACIM-0017", "CAP-CANONICAL-GOVERNANCE", "AIC-MADEIRA-ON-CURSOR", "implemented", "Inline ratify on CSV/canonical gates", ".cursor/rules/akos-inline-ratification.mdc; .cursor/skills/inline-ratify-craft/SKILL.md", "", "confirmed", "Alpha CAP-M04."),
    ("ACIM-0018", "CAP-RES-DEEP-METHODOLOGY", "AIC-MADEIRA-ON-CURSOR", "implemented", "Research action 8-stage loop", "scripts/validate_research_action.py; RESEARCH_ACTION_DISCIPLINE.md", "", "confirmed", "Alpha CAP-M05."),
    ("ACIM-0019", "CAP-RES-KB-PIPELINE-RADAR", "AIC-MADEIRA-ON-CURSOR", "partial", "Research radar freshness sweep", "scripts/validate_research_radar.py; scripts/research_radar_sweep.py", "", "confirmed", "Alpha CAP-M06."),
    ("ACIM-0020", "CAP-MADEIRA-RESEARCH-CENTER-SURFACE", "AIC-MADEIRA-ON-CURSOR", "partial", "Research Center experiential UAT manifests", "artifacts/uat-screenshots/i96-research-center-v32-alpha-t0-2026-06-14/", "", "confirmed", "Alpha CAP-M07."),
    ("ACIM-0021", "CAP-KNOWLEDGE-RETRIEVAL-RAG", "AIC-MADEIRA-ON-CURSOR", "partial", "KiRBe retrieval worker substrate", "docs/wip/planning/83-ai-archivist-and-kirbe-ingestor/master-roadmap.md", "", "confirmed", "Alpha CAP-M08."),
    ("ACIM-0022", "CAP-KNOWLEDGE-REGISTER-STEWARDSHIP", "AIC-MADEIRA-ON-CURSOR", "partial", "Source register + ledger promote path", "docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/source-ledger.csv", "", "confirmed", "Alpha CAP-M09 supplement."),
    ("ACIM-0023", "CAP-AI-EVALUATION-BENCHMARKING", "AIC-MADEIRA-ON-CURSOR", "implemented", "Langfuse traces + release-gate eval", "scripts/release-gate.py", "", "confirmed", "Alpha CAP-M10."),
    ("ACIM-0024", "CAP-AGENTIC-INFRA-OPS", "AIC-MADEIRA-ON-CURSOR", "implemented", "Gateway repair + check-only proof", "scripts/openclaw_gateway_repair.py; artifacts/gateway-repair-post-reboot-2026-06-15.json", "", "confirmed", "Alpha CAP-M12."),
    ("ACIM-0025", "CAP-FIN-COUNTERPARTY-MDM", "AIC-CURSOR-BORROWED", "implemented", "Finops counterparty register", "scripts/validate_finops_counterparty_register.py", "", "confirmed", "Alpha CAP-M14 primary."),
    ("ACIM-0026", "CAP-FIN-REVENUE-OPS-BILLING", "AIC-CURSOR-BORROWED", "implemented", "RevOps billing sibling", "scripts/validate_finops_ledger.py", "", "confirmed", "Alpha CAP-M14 supplement."),
    ("ACIM-0027", "CAP-DATA-PLATFORM-PRODUCTS", "AIC-CURSOR-BORROWED", "partial", "Infonomics join via data-product planes", "docs/wip/planning/97-infonomics-data-economics-p0/charter.md", "", "pre-ratified", "Alpha CAP-M15; I97 scheduled."),
    ("ACIM-0028", "CAP-MADEIRA-CONTEXT-ECONOMICS", "AIC-MADEIRA-ON-CURSOR", "planned", "Context economics spec ratified; T2 code", "docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/context-economics-wip-spec-2026-06-15.md", "", "pre-ratified", "Alpha CAP-M16..M18."),
    ("ACIM-0029", "CAP-AI-AGENT-ORCHESTRATION", "AIC-MADEIRA-ON-CURSOR", "implemented", "OpenClaw normalize + MCP orchestration", "scripts/legacy/verify_openclaw_inventory.py; AGENTIC_FRAMEWORK_LANDSCAPE.md", "", "confirmed", "Alpha CAP-M19/M20/M21."),
    ("ACIM-0030", "CAP-API-LIFECYCLE-GOVERNANCE", "AIC-MADEIRA-ON-CURSOR", "implemented", "MCP server definition governance", "SOP-MCP_SERVER_DEFINITION", "", "confirmed", "Alpha CAP-M21 supplement."),
    ("ACIM-0031", "CAP-MULTIPLATFORM-DEPLOYMENT", "AIC-CURSOR-BORROWED", "partial", "Hosted SDK/API path I74", "docs/wip/planning/74-madeira-hosted-sdk-api/master-roadmap.md", "", "pre-ratified", "Alpha CAP-M22."),
    ("ACIM-0032", "CAP-CLOSURE-ASSURANCE-GOVERNANCE", "AIC-MADEIRA-ON-CURSOR", "implemented", "Experiential UAT + browser evidence", "scripts/validate_uat_screenshot_evidence.py; scripts/validate_uat_report.py", "", "confirmed", "Alpha CAP-M24/M28."),
    ("ACIM-0033", "CAP-EXPERIENCE-UX-QUALITY", "AIC-MADEIRA-ON-CURSOR", "implemented", "Quality Fabric 5-axis composition", ".cursor/rules/akos-quality-fabric.mdc", "", "confirmed", "Alpha CAP-M25."),
    ("ACIM-0034", "CAP-ENGAGEMENT-MODEL-GOVERNANCE", "AIC-CURSOR-BORROWED", "implemented", "Persona/scenario library", "PERSONA_SCENARIO_REGISTRY.csv", "", "confirmed", "Alpha CAP-M26."),
    ("ACIM-0035", "CAP-PRECOMMIT-SYNTHESIS-DISCIPLINE", "AIC-MADEIRA-ON-CURSOR", "implemented", "Synthesis-before-tranche gate", "scripts/validate_synthesis_before_tranche.py", "", "confirmed", "Alpha CAP-M29."),
    ("ACIM-0036", "CAP-OPS-PROGRAM-PORTFOLIO-MGMT", "AIC-CURSOR-BORROWED", "implemented", "Carryover posture index under PMO portfolio", "docs/wip/planning/_trackers/carryover-posture-index.md", "", "confirmed", "Alpha CAP-M30."),
]


def _build_alpha_refs() -> dict[str, list[str]]:
    refs: dict[str, list[str]] = defaultdict(list)
    with XW_WIP.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            vault = (row.get("vault_capability_id") or "").strip()
            alpha = (row.get("alpha_capability_id") or "").strip()
            if vault and alpha and alpha not in refs[vault]:
                refs[vault].append(alpha)
    return refs


def apply_capability_registry() -> None:
    from akos.hlk_capability_registry_csv import CAPABILITY_REGISTRY_FIELDNAMES

    refs = _build_alpha_refs()
    with CAP_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    existing_ids = {r["capability_id"] for r in rows}
    for row in rows:
        cid = row["capability_id"]
        if cid in SUBSTRATE_BACKFILL:
            row["substrate_id"] = SUBSTRATE_BACKFILL[cid]
        if cid in refs:
            row["alpha_inventory_refs"] = ";".join(sorted(refs[cid]))
        else:
            row.setdefault("alpha_inventory_refs", "")
        if cid in SUBSTRATE_BACKFILL or cid in refs:
            row["methodology_version_at_review"] = "v3.2"
            row["last_review_at"] = "2026-06-15"
            row["last_review_decision_id"] = "D-IH-76-CAP-GCI"

    for new_row in NEW_ROWS:
        if new_row["capability_id"] not in existing_ids:
            rows.append(new_row)

    with CAP_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CAPABILITY_REGISTRY_FIELDNAMES), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            out = {k: row.get(k, "") for k in CAPABILITY_REGISTRY_FIELDNAMES}
            writer.writerow(out)


def apply_crosswalk() -> None:
    with XW_WIP.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    XW_VAULT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "crosswalk_id", "alpha_capability_id", "vault_capability_id",
        "relationship", "substrate_id_proposed", "notes",
    ]
    with XW_VAULT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def apply_acim() -> None:
    from akos.hlk_aic_capability_implementation_matrix_csv import (
        AIC_CAPABILITY_IMPLEMENTATION_MATRIX_FIELDNAMES,
    )

    with ACIM_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    existing = {(r["capability_id"], r["aic_id"]) for r in rows}

    for tpl in ACIM_NEW:
        key = (tpl[1], tpl[2])
        if key in existing:
            continue
        rows.append({
            "matrix_id": tpl[0],
            "capability_id": tpl[1],
            "aic_id": tpl[2],
            "implementation_status": tpl[3],
            "approach_summary": tpl[4],
            "tool_catalog_ref": tpl[5],
            "realisation_refs": "",
            "paired_madeira_task_id": tpl[6],
            "confidence_class": tpl[7],
            "notes": tpl[8] + " | D-IH-76-CAP-GCI mint 2026-06-15.",
            "last_review_at": "2026-06-15",
            "last_review_by": "Data Governance Office",
            "last_review_decision_id": "D-IH-76-CAP-GCI",
            "methodology_version_at_review": "v3.2",
        })

    with ACIM_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(AIC_CAPABILITY_IMPLEMENTATION_MATRIX_FIELDNAMES), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            out = {k: row.get(k, "") for k in AIC_CAPABILITY_IMPLEMENTATION_MATRIX_FIELDNAMES}
            writer.writerow(out)


def apply_decision() -> None:
    with DECISION_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if any(r.get("decision_id") == "D-IH-76-CAP-GCI" for r in rows):
        return
    rows.append({
        "decision_id": "D-IH-76-CAP-GCI",
        "title": "MADEIRA v3.2 capability governance mint tranche T1-cap-GCI",
        "initiating_initiative_id": "INIT-OPENCLAW_AKOS-76",
        "linked_initiative_ids": "",
        "linked_ops_action_ids": "",
        "linked_policies": "",
        "linked_topic_ids": "",
        "decision_class": "governance",
        "status": "active",
        "reversibility": "low",
        "decided_at": "2026-06-15",
        "decision_log_path": "docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/mint-gate-packet-gci-capability-tranche-2026-06-15.md",
        "supersedes_decision_id": "",
        "summary": "Operator ratifies GCI bundle: +4 CAP rows; 16 substrate backfills; alpha_inventory_refs column; CAPABILITY_ALPHA_CROSSWALK 36 edges; +24 ACIM rows; validator FAIL on empty substrate for active Applied AI & MADEIRA.",
        "notes": "decision_source: operator AskQuestion mint_full + hybrid_both 2026-06-15.",
        "last_review_at": "2026-06-15",
        "last_review_by": "Operator",
        "last_review_decision_id": "D-IH-76-CAP-GCI",
        "methodology_version_at_review": "v3.2",
    })
    with DECISION_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    apply_capability_registry()
    apply_crosswalk()
    apply_acim()
    apply_decision()
    print("GCI mint applied.")


if __name__ == "__main__":
    main()
