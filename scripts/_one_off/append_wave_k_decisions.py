"""One-off script to append Wave K decision rows D-IH-86-AY through D-IH-86-BD.

Per akos-holistika-operations.mdc canonical-CSV gate discipline + operator
velocity-bless 2026-05-20 (Wave K opt-arch-plus-all-three direction includes
'wire whatever we left up'). Six decisions ratify the regression outcomes:
  - D-IH-86-AY: UAT 11-class promotion gate (G5)
  - D-IH-86-AZ: Fabric materialisation 5->8 specialties (G6)
  - D-IH-86-BA: compose() runbook gates charter->active (G7)
  - D-IH-86-BB: 4-layer output-architecture (operator G4 extension)
  - D-IH-86-BC: Forward-charter I-NN-OUTPUT-ARCHITECTURE
  - D-IH-86-BD: J-AIC AUDIENCE_REGISTRY mint (G1 fix-forward)

Schema (19 cols): decision_id,title,initiating_initiative_id,linked_initiative_ids,
linked_ops_action_ids,linked_policies,linked_topic_ids,decision_class,status,
reversibility,decided_at,decision_log_path,supersedes_decision_id,summary,notes,
last_review_at,last_review_by,last_review_decision_id,methodology_version_at_review
"""

from pathlib import Path
import csv

REGISTER = Path(__file__).resolve().parents[2] / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv"

ROWS = [
    [
        "D-IH-86-AY",
        "UAT_DISCIPLINE.md class taxonomy 7->11 promotion gate (Wave J G5 regression)",
        "INIT-OPENCLAW_AKOS-86",
        "",
        "",
        "",
        "",
        "governance",
        "active",
        "medium",
        "2026-05-20",
        "docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md",
        "",
        "Wave K ratify of Wave J regression G5 (operator opt-promote-11). UAT_DISCIPLINE.md class taxonomy promotes from 7 classes (closure / brand / send / render / regression / persona / deploy) to 11 classes adding 4: localisation (per-language UAT grounded in scripts/validate_locale_orthography.py + ES smart-quote / FR diacritics / EN word-list anti-patterns); accessibility (WCAG 2.2 AA verification; keyboard nav; screen reader; color contrast); performance (Core Web Vitals; bundle size; load time); privacy (GDPR cookie consent; data-retention claims; PII redaction). Promotion gates UAT_DISCIPLINE.md charter->active transition.",
        "Each new class carries internal precedent identification + external research grounding per akos-applied-research-discipline.mdc RULE 2 (WCAG 2.2 / Lighthouse / GDPR / locale-orthography validator). Aligns with Shadcn-class depth bar operator named in 2026-05-20 framing. Decision subclass: doctrine-extension. Wave J regression provenance: docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md L172-L177. ratify_source = inline_askquestion 2026-05-20 g5-uat-classes opt-promote-11.",
        "2026-05-20",
        "Founder",
        "D-IH-86-AY",
        "v3.1",
    ],
    [
        "D-IH-86-AZ",
        "HOLISTIKA_QUALITY_FABRIC.md materialisation table 5->8 specialty composes (G6 regression)",
        "INIT-OPENCLAW_AKOS-86",
        "",
        "",
        "",
        "",
        "governance",
        "active",
        "medium",
        "2026-05-20",
        "docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md",
        "",
        "Wave K ratify of Wave J regression G6 (operator opt-extend-8). HOLISTIKA_QUALITY_FABRIC.md section 6 materialisation table extends from 5 specialty composes (UAT / UX / brand-render / send / closure) to 8 specialties adding: MKTOPS_DISCIPLINE.md (campaigns / GTM funnel / landing-page conversion quality; addresses operator 2026-05-19 framing 'i don't know if from the MKT/Tech side of things our UAT holds'); TECHOPS_DISCIPLINE.md (system uptime / observability / Core Web Vitals beyond per-deploy); DATAOPS_DISCIPLINE.md (data quality / pipeline integrity / mirror sync correctness / FDW posture). Three new Operations-plane sister canonicals to People-plane UAT_DISCIPLINE / UX_DISCIPLINE.",
        "Forward-chartered as canonical-mint dependencies for fabric charter->active promotion. Each canonical owned by area Data Owner (MKTOPS = Marketing/Reach + Operations/RevOps; TECHOPS = Tech/System Owner + DevOPS; DATAOPS = Tech/Data + System Owner). Cross-area inheritance contract from UAT_DISCIPLINE.md section 5 inherits to all 8 specialties. Decision subclass: doctrine-extension. ratify_source = inline_askquestion 2026-05-20 g6-materialisation opt-extend-8.",
        "2026-05-20",
        "Founder",
        "D-IH-86-AZ",
        "v3.1",
    ],
    [
        "D-IH-86-BA",
        "Quality Fabric charter->active promotion gates on compose() runbook landing (G7 regression)",
        "INIT-OPENCLAW_AKOS-86",
        "",
        "",
        "",
        "",
        "governance",
        "active",
        "low",
        "2026-05-20",
        "docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md",
        "",
        "Wave K ratify of Wave J regression G7 (operator opt-gate-active). HOLISTIKA_QUALITY_FABRIC.md charter->active promotion is GATED on scripts/derive_quality_bar.py runbook landing + compose_UAT() + compose_UX() + compose_render() + compose_send() + compose_closure() functions delegating to it. The fabric is unfalsifiable in CI today (compose() is asserted in canonicals but not implemented as code); gating active-promotion on runbook implementation forces mechanical resolution before doctrine multiplies. Adds gate item 4 to HOLISTIKA_QUALITY_FABRIC.md section 10.",
        "Without compose() runbook agents resolve 5 axes by reading docs each time (slow + drift-prone). Runbook signature: derive_quality_bar(audience: str, channel: str, scenario: str, brand: str, governance: str, *, layer: Optional[str] = None) -> QualityBar (Pydantic model). Emits JSON for ERP panel + Markdown for human reading. Tests in tests/test_derive_quality_bar.py with paired audience/channel/scenario/brand/governance fixtures across 8 audience codes. Decision subclass: governance-gate. ratify_source = inline_askquestion 2026-05-20 g7-compose-runbook opt-gate-active.",
        "2026-05-20",
        "Founder",
        "D-IH-86-BA",
        "v3.1",
    ],
    [
        "D-IH-86-BB",
        "4-layer output architecture below 5-axis Quality Fabric (operator G4 extension)",
        "INIT-OPENCLAW_AKOS-86",
        "",
        "",
        "",
        "",
        "architecture",
        "active",
        "high",
        "2026-05-20",
        "docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md",
        "",
        "Wave K ratify of operator G4 extension (2026-05-20 verbatim: 'we are speaking of components in a UI and there could be more scenarios slides of pdf/pptx images voice for agents reading for different readers platforms scenarios excalidraw mermaids graphs gantts please try to think of a way to properly organize the output type'). Reframes Wave J G3 6th-axis-Component decision into a 4-layer hierarchy BELOW the 5-axis fabric. The 5-axis fabric stays at 5 axes; below it sit 4 layers: Layer 1 OUTPUT_TYPE (medium / shape: prose / slide / image / voice / mermaid / gantt / excalidraw / web / pdf / video; ~17 codes); Layer 2 ARTIFACT_CLASS (named purpose: dossier / cover_email / intro_message / deck / topic_graph / km_diagram / uat_report; ~20 codes); Layer 3 COMPONENT_PRIMITIVE (sub-units: greeting / hook / CTA / signature / evidence-block / slide-hero / slide-the-ask; ~25 codes); Layer 4 RENDER_SURFACE (already exists per akos-external-render-discipline.mdc RULE 1: PDF / Web / ERP / Mail / Slide / Broadcast). Each layer = registry CSV + canonical MD library doctrine. Quality Fabric compose() applies at every layer with derived bar varying by layer. Operator's Shadcn-bar achievable at Layer 3 (per-primitive doctrine pages with variants x accessibility x research x composition rules).",
        "Owned by Brand & Narrative Manager primary (Layer 2+3 per 2026-05-15 absorption D-IH-72-AO) + Front-End Developer co-owner (Layer 1 + web-rendered Layer 3 per implementation concerns). Touchpoint-kit's 15 existing files retro-tag cheaply. 11 render_*.py scripts retro-classify in ARTIFACT_CLASS_REGISTRY.render_script_path. Cross-axis: Quality Fabric stays at 5 axes; 4-layer hierarchy is parametrised BY the 5 axes (not a 6th axis). Mints OUTPUT_TYPE_REGISTRY.csv + OUTPUT_TYPE_LIBRARY.md + ARTIFACT_CLASS_REGISTRY.csv + ARTIFACT_CLASS_LIBRARY.md + COMPONENT_PRIMITIVE_REGISTRY.csv + COMPONENT_PRIMITIVE_LIBRARY.md (6 new canonicals). Decision subclass: meta-architecture. ratify_source = inline_askquestion 2026-05-20 output-arch-shape opt-4layer-full + wave-k-scope opt-arch-plus-all-three (with operator 'proper regression to wire whatever we left up' directive).",
        "2026-05-20",
        "Founder",
        "D-IH-86-BB",
        "v3.1",
    ],
    [
        "D-IH-86-BC",
        "Forward-charter I-NN-OUTPUT-ARCHITECTURE candidate-shape mint (4-layer hierarchy materialisation)",
        "INIT-OPENCLAW_AKOS-86",
        "",
        "",
        "",
        "",
        "scope",
        "active",
        "high",
        "2026-05-20",
        "docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md",
        "",
        "Forward-charters output-architecture initiative as candidate-shape file at docs/wip/planning/_candidates/i-nn-output-architecture.md per akos-conflict-surfacing-and-blocker-trackers.mdc Option 5 default posture. Subsumes previously-proposed I-NN-MESSAGE-COMPONENT-LIBRARY (D-IH-86-AU referenced 'Component as 6th axis'; now reframed per D-IH-86-BB as 3-layer hierarchy below fabric). Phase plan: P0 Charter + 4-layer architecture spec + retro-tag plan; P1 Layer 1 OUTPUT_TYPE_REGISTRY + LIBRARY (skeleton landed Wave K; full doctrine pages here); P2 Layer 2 ARTIFACT_CLASS_REGISTRY + LIBRARY + retro-tag 11 render scripts; P3 Layer 3 COMPONENT_PRIMITIVE_REGISTRY + LIBRARY (Shadcn-shape per-primitive doctrine pages); P4 Backfill touchpoint-kit's 15 files; P5 Mint scripts/derive_quality_bar.py compose() runbook; P6 Wire into ERP planning panel + dossier generation + UAT report; P7 UAT closure. Owner: Brand & Narrative Manager primary + Front-End Developer co-owner.",
        "Activation gates: Quality Fabric at active (gates on D-IH-86-BA compose() runbook landing); UAT_DISCIPLINE at active (gates on D-IH-86-AY 11-class promotion); >=1 channel doctrine POC. Operator 'continuous discovery research design determine test mint repeat' framing 2026-05-20 implies iterative depth: registries land at Wave K with codes + structure; doctrine pages mature in subsequent commits. Decision subclass: forward-charter-candidate. ratify_source = inline_askquestion 2026-05-20 wave-k-scope opt-arch-plus-all-three.",
        "2026-05-20",
        "Founder",
        "D-IH-86-BC",
        "v3.1",
    ],
    [
        "D-IH-86-BD",
        "AUDIENCE_REGISTRY.csv mint J-AIC row (G1 fix-forward; canonical-CSV gate via operator velocity-bless)",
        "INIT-OPENCLAW_AKOS-86",
        "",
        "",
        "",
        "",
        "governance",
        "active",
        "low",
        "2026-05-20",
        "docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md",
        "",
        "Wave K mechanical fix-forward of Wave J regression G1 dangling FK. AUDIENCE_REGISTRY.csv mints new row J-AIC (AI O5-1 / agent role-class internal) covering AICs (Madeira and successors) consuming canonicals as executable instructions and authoring artifacts on operator behalf. Distinct from J-OP because: (a) AICs consume SOPs as executable instructions not just operator narrative; (b) AICs AUTHOR artifacts (operator + cleared-agent superset). Wave I+J systematically established this distinction across 15+ sites (D-IH-86-AH/AJ/AO/AP/AU references) without registering; Wave K mints to close FK gap. J-OP notes column updated to remove 'AICs' (clearer separation). Replicates J-OP shape with AIC-specific notes citing HOLISTIKA_AGENTIC_DOCTRINE.md.",
        "Canonical-CSV gate per akos-holistika-operations.mdc 'New git-canonical compliance registers' satisfied via operator velocity-bless (Wave K opt-arch-plus-all-three direction explicitly includes 'proper regression to wire whatever we left up'). Alternative path was mass-rewrite J-AIC -> J-OP across 15+ sites; rejected because Wave I D-IH-86-AJ explicitly distinguished J-AIC as a 9th class and operator intent across waves treats AICs as semantically distinct. Future J-AIC populations beyond Madeira track via I76 MADEIRA elevation candidate. Decision subclass: csv-mint. ratify_source = operator velocity-bless 2026-05-20 wave-k-scope opt-arch-plus-all-three with 'wire whatever we left up' directive.",
        "2026-05-20",
        "Founder",
        "D-IH-86-BD",
        "v3.1",
    ],
]


def main() -> None:
    """Append the 6 Wave K decision rows to DECISION_REGISTER.csv."""
    import io

    if not REGISTER.exists():
        raise SystemExit(f"DECISION_REGISTER.csv not found at {REGISTER}")

    existing = REGISTER.read_text(encoding="utf-8")
    if not existing.endswith("\n"):
        existing += "\n"

    out_lines = []
    for row in ROWS:
        sio = io.StringIO()
        w = csv.writer(sio, lineterminator="", quoting=csv.QUOTE_MINIMAL)
        w.writerow(row)
        out_lines.append(sio.getvalue())

    REGISTER.write_text(existing + "\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Appended {len(ROWS)} rows; final size {REGISTER.stat().st_size} bytes")


if __name__ == "__main__":
    main()
