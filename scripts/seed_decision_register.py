#!/usr/bin/env python3
"""Initiative 59 P3 — seed DECISION_REGISTER.csv with closure + I59 decisions.

Closes the gap between the 104 historical ``D-IH-XX-Y`` decision headers in
``decision-log.md`` files and the empty ``DECISION_REGISTER.csv``. Seeds:

1. Every ``closure_decision_id`` referenced from ``INITIATIVE_REGISTRY.csv``
   (one row per closed / archived initiative).
2. The 14 I59 decisions ``D-IH-59-A`` … ``D-IH-59-N`` from the I59 P0 bootstrap.
3. Three I22a operational decisions ``D-IH-OPS-1`` / ``D-IH-OPS-2`` / ``D-IH-OPS-3``.
4. Two special closure-form decisions: I46 P3 NO-SHIP (graphrag) and I58 D-IH-58-I
   (judge wiring).

Usage::

    py scripts/seed_decision_register.py             # dry-run
    py scripts/seed_decision_register.py --write     # apply

Idempotent: re-running on an already-seeded CSV produces an identical file.

The advisory sync validator
(``scripts/validate_decision_register_decision_log_md_sync.py``) will continue
to flag remaining ``D-IH-XX-Y`` headers in MD that lack a CSV row — that is
expected and they can be backfilled incrementally.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_decision_register_csv import DECISION_REGISTER_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
DECISION_REGISTER_CSV = HLK_COMPLIANCE / "DECISION_REGISTER.csv"
INITIATIVE_REGISTRY_CSV = HLK_COMPLIANCE / "INITIATIVE_REGISTRY.csv"

# Snake-case audit-id ↔ canonical INIT-OPENCLAW_AKOS-NN id translation.
# Limited to the ids referenced from this seeder; extend if more are added.
_SNAKE_TO_INIT: dict[str, str] = {
    "i02_hlk_on_akos_madeira": "INIT-OPENCLAW_AKOS-02",
    "i07_hlk_neo4j_graph_projection": "INIT-OPENCLAW_AKOS-07",
    "i15_madeira_pivots": "INIT-OPENCLAW_AKOS-15",
    "i22a_post_closure_followups": "INIT-OPENCLAW_AKOS-22A",
    "i26_madeira_brand_deployment": "INIT-OPENCLAW_AKOS-26",
    "i46_neo4j_strategic_posture": "INIT-OPENCLAW_AKOS-46",
    "i58_cycle_2_multi_track_forward": "INIT-OPENCLAW_AKOS-58",
    "i59_hlk_governance_clean_slate": "INIT-OPENCLAW_AKOS-59",
}


def _to_init_id(snake: str) -> str:
    """Resolve a snake_case audit id to the canonical INIT- id when known."""
    return _SNAKE_TO_INIT.get(snake, snake)


def _row(
    decision_id: str,
    title: str,
    initiating: str,
    decision_class: str,
    decided_at: str,
    decision_log_path: str,
    summary: str,
    *,
    linked_initiative_ids: str = "",
    linked_ops_action_ids: str = "",
    linked_policies: str = "",
    linked_topic_ids: str = "",
    status: str = "active",
    reversibility: str = "low",
    supersedes: str = "",
    notes: str = "",
) -> dict[str, str]:
    return {
        "decision_id": decision_id,
        "title": title,
        "initiating_initiative_id": initiating,
        "linked_initiative_ids": linked_initiative_ids,
        "linked_ops_action_ids": linked_ops_action_ids,
        "linked_policies": linked_policies,
        "linked_topic_ids": linked_topic_ids,
        "decision_class": decision_class,
        "status": status,
        "reversibility": reversibility,
        "decided_at": decided_at,
        "decision_log_path": decision_log_path,
        "supersedes_decision_id": supersedes,
        "summary": summary,
        "notes": notes,
    }


def _i59_decisions() -> list[dict[str, str]]:
    """The 14 D-IH-59-A..N decisions from the I59 P0 bootstrap."""
    base = "docs/wip/planning/59-hlk-governance-clean-slate/decision-log.md"
    decided = "2026-05-06"
    out: list[dict[str, str]] = []
    seeds = [
        ("A", "Atomic dimension landing", "architecture",
         "Five new HLK governance dimensions land in a single P1 commit; no partial / sequential rollout."),
        ("B", "Two-layer SSOT (markdown for prose, CSV for metadata)", "architecture",
         "Markdown stays canonical for narrative; CSVs become canonical for queryable metadata. Sync gates enforce agreement."),
        ("C", "REPOSITORY_REGISTRY promotion path", "architecture",
         "REPOSITORIES_REGISTRY.md and REPOSITORY_REGISTRY.csv are joint canonicals (markdown for prose, CSV for FK target)."),
        ("D", "Status taxonomy ownership at akos.planning.status_taxonomy", "architecture",
         "Seven-value StrEnum (closed/archived/active/continuous/program_line/gated_external/gated_operator) + companion-field rules."),
        ("E", "DECISION_REGISTER inclusion in I59", "architecture",
         "Folded into I59 (vs I60 deferral) so initiative_registry's *_decision_id fields can be real FKs from day one."),
        ("F", "Nullable FKs (manifests_processes, coordinated_initiative_ids)", "execution",
         "Empty is explicit and fine; wrong is not. Validators FK-resolve when set, allow empty."),
        ("G", "manifests_processes column on INITIATIVE_REGISTRY (vs inverse)", "architecture",
         "FK lives on the initiative side as a semicolon-list to process_list.csv; reverse-lookup via mirror queries."),
        ("H", "Header-only seed for INITIATIVE/OPS/CYCLE/DECISION in P1; bulk seed in P3", "execution",
         "Avoids circular FK pressure during validator runs; P3 lockstep seed against fully-populated peer tables."),
        ("I", "Two new SOPs at status: review until G-59-D in P9", "governance",
         "SOP-INITIATIVE_GOVERNANCE_001 + SOP-INITIATIVE_PROCESS_HARMONISATION_001 ship at review state; ratified at P9."),
        ("J", "OPS-58-3 rubric calibration fix lands in I59 P6 (not deferred to I60)", "scope",
         "_heuristic_persona_fit gets persona context from scenario.persona_id so cross-persona alignment lifts above 80%."),
        ("K", "Telemetry promotion routine runs once in I59 P7 (in operator's stead)", "execution",
         "Auto-merge forbidden per I49 P11 / I50 P5; agent runs the proposal pass and operator merges at next sitting."),
        ("L", "Process_list mints deferred to I60 candidate", "scope",
         "I59 P8 ships the harmonisation proposal + new SOP; actual minting per-tranche is operator-approval-gated and out of scope here."),
        ("M", "process_list mint authority chain: SOP-META + role_owner + tranche operator approval", "governance",
         "No agent minting. Tranches authored under reports/process-list-mint-proposal-*.md and decision-log entries."),
        ("N", "I59 closure UAT requires zero advisory warnings under --strict on the 8 new validators", "execution",
         "P10 closure gate flips advisory→strict on validate_master_roadmap_frontmatter and the 3 sync gates."),
    ]
    for letter, title, klass, summary in seeds:
        out.append(_row(
            decision_id=f"D-IH-59-{letter}",
            title=title,
            initiating=_to_init_id("i59_hlk_governance_clean_slate"),
            decision_class=klass,
            decided_at=decided,
            decision_log_path=base,
            summary=summary,
            reversibility="medium" if klass != "architecture" else "low",
        ))
    return out


def _closure_rows_from_initiative_registry() -> list[dict[str, str]]:
    """Emit one closure-decision row per non-empty closure_decision_id in INITIATIVE_REGISTRY."""
    out: list[dict[str, str]] = []
    if not INITIATIVE_REGISTRY_CSV.is_file():
        return out
    with INITIATIVE_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = (row.get("closure_decision_id") or "").strip()
            if not cid or cid.startswith("D-IH-OPS"):
                continue
            initiative_id = row.get("initiative_id", "")
            folder_path = row.get("folder_path", "").rstrip("/")
            decided_at = row.get("closed_at", "") or row.get("last_review", "") or "2026-05-06"
            log_path = f"{folder_path}/decision-log.md" if folder_path else ""
            out.append(_row(
                decision_id=cid,
                title=f"Closure decision for {initiative_id}",
                initiating=initiative_id,
                decision_class="closure",
                decided_at=decided_at,
                decision_log_path=log_path,
                summary=f"Closes {initiative_id} (status: {row.get('status', '')}); seeded from INITIATIVE_REGISTRY.csv during I59 P3.",
                reversibility="low",
                notes="auto-seeded from initiative_registry; verify prose body in decision-log.md",
            ))
    return out


def _i22a_ops_decisions() -> list[dict[str, str]]:
    """D-IH-OPS-1/2/3 from I22a P7 supabase parity reconciliation."""
    base = "docs/wip/planning/22a-i22-post-closure-followups/decision-log.md"
    decided = "2026-05-04"
    init = _to_init_id("i22a_post_closure_followups")
    return [
        _row("D-IH-OPS-1", "Full-parity Supabase reconciliation approved", init,
             "execution", decided, base,
             "Reverse-import + apply migrations to bring MasterData Supabase to ledger parity (I49 + I51 + I14-phase-3).",
             reversibility="medium"),
        _row("D-IH-OPS-2", "Rename I14 Phase 3 migration to clean tail timestamp",
             init, "execution", decided, base,
             "Idempotent reapply at 20260503190000 to keep migration ledger linear.", reversibility="low"),
        _row("D-IH-OPS-3", "Reverse-import kirbe.monitoring_logs_retention to git",
             init, "execution", decided, base,
             "Pre-existing remote body imported to git so git remains SSOT.", reversibility="low"),
    ]


def _special_closure_decisions() -> list[dict[str, str]]:
    """I46 P3 NO-SHIP and I58 D-IH-58-I."""
    return [
        _row(
            "D-IH-46-Decision-P3-NO-SHIP-2026-05-03",
            "GraphRAG PoC NO-SHIP verdict (D-IH-46-E non-additive bar)",
            _to_init_id("i46_neo4j_strategic_posture"),
            "closure", "2026-05-03",
            "docs/wip/planning/46-neo4j-strategic-posture/decision-log.md",
            "Non-additive bar (≥3pp / ≥30% / ≥40%) not cleared; ship deferred under conditional gate.",
            reversibility="high",
            linked_ops_action_ids="OPS-53-1",
        ),
        _row(
            "D-IH-58-I",
            "Judge live-API wiring + roster pivot under operator go-all-out",
            _to_init_id("i58_cycle_2_multi_track_forward"),
            "execution", "2026-05-06",
            "docs/wip/planning/58-cycle-2-multi-track-forward/decision-log.md",
            "Wired _call_member_via_api for live Anthropic + OpenAI dispatch; pivoted to all-Anthropic roster after key probe.",
            reversibility="medium",
            linked_ops_action_ids="OPS-58-1;OPS-58-2",
        ),
        _row(
            "D-IH-58-J",
            "OPS-58-3 forwarded as engineering follow-up",
            _to_init_id("i58_cycle_2_multi_track_forward"),
            "scope", "2026-05-06",
            "docs/wip/planning/58-cycle-2-multi-track-forward/decision-log.md",
            "Persona-aware offline _heuristic_persona_fit fix (RICE 149) closes the persona=None rubric gap.",
            reversibility="high",
            linked_ops_action_ids="OPS-58-3",
        ),
        _row(
            "D-IH-58-K",
            "OpenAI key rotation forwarded as operator action",
            _to_init_id("i58_cycle_2_multi_track_forward"),
            "execution", "2026-05-06",
            "docs/wip/planning/58-cycle-2-multi-track-forward/decision-log.md",
            "Existing key returns 401; operator rotates and updates ~/.openclaw/.env (RICE 144).",
            reversibility="high",
            linked_ops_action_ids="OPS-58-2",
        ),
    ]


def _all_rows() -> list[dict[str, str]]:
    rows = []
    rows.extend(_i59_decisions())
    rows.extend(_closure_rows_from_initiative_registry())
    rows.extend(_i22a_ops_decisions())
    rows.extend(_special_closure_decisions())
    seen: set[str] = set()
    deduped: list[dict[str, str]] = []
    for r in rows:
        if r["decision_id"] in seen:
            continue
        seen.add(r["decision_id"])
        deduped.append(r)
    return deduped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write the seeded CSV (otherwise dry-run summary)")
    args = parser.parse_args()

    rows = _all_rows()
    print()
    print("  seed_decision_register")
    print("  ========================================")
    print(f"  Rows to write: {len(rows)}")
    if not args.write:
        print()
        print("  DRY-RUN: pass --write to apply.")
        return 0
    with DECISION_REGISTER_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(DECISION_REGISTER_FIELDNAMES), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({fn: r.get(fn, "") for fn in DECISION_REGISTER_FIELDNAMES})
    print(f"  WROTE {DECISION_REGISTER_CSV.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
