---
language: en
status: active
canonical: true
role_owner: Research Director + Research Analyst
classification: way_of_working
intellectual_kind: discipline_charter
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
---

# DIAGNOSIS_DISCIPLINE_CHARTER — Research/Diagnosis

> Authored I70 P4.7 per `RESEARCH_AREA_CHARTER.md` §2 + D-IH-70-S + Conundrum 11. **NEW discipline** (no pre-existing folder migration). Formalizes the engagement-as-org-diagnostic pattern (F-51) that has been implicit in P13's I12 SUEZ engagement work.

## 1. Mission

The discipline of *what's wrong* — at the counterparty (engagement) level, the system level, or the methodology level. Diagnosis runs ON intelligence (collected by Research/Intelligence), produces verdict + recommendation outputs, and feeds Validation gates.

## 2. Three diagnosis surfaces

| Surface | Object diagnosed | Output | Worked example |
|:---|:---|:---|:---|
| **Engagement diagnostic** | Counterparty's current operational state | Per-engagement diagnostic report (counterparty-baseline-reality + key gaps + recommended posture) | SUEZ engagement: WeBuy procure-to-pay diagnostic surfaced the litige-prevention gap that became deck slide F·05 |
| **System diagnostic** | Holistika's own systems (AKOS canonicals + render pipeline + Supabase mirrors + ERP panels) | System-health diagnostic report | I70 P2.5 v3.0 vault audit is the first full system diagnostic; ~120 directory verdicts |
| **Methodology diagnostic** | Holistika's own methodology (per-pillar effectiveness; per-discipline coverage) | Methodology gap analysis | I70 P2 synthesis (the 7 gaps mapped to phases) is a methodology diagnostic |

## 3. Roles

- **Research Director** (primary) — owns diagnostic verdict authoring + cross-area implications.
- **Research Analyst** (primary) — runs the diagnostic data-gathering pass + drafts findings.

## 4. Engagement-as-org-diagnostic pattern (F-51 codified)

Per founder principle 2.3 (anticipatory preparation) + the operating story §"Why one master initiative not four" framing:

> Every customer engagement is a stress-test of Holistika's own governance discipline. Every gap in the engagement's deliverable surfaces a gap in the governance that fed the deliverable.

Concrete loop:

1. **Engagement begins** — operator + Research Analyst gather intelligence (HUMINT + OSINT + counterparty-supplied artifacts).
2. **Counterparty diagnostic** — Research Analyst authors counterparty-baseline-reality assessment.
3. **Methodology diagnostic** — as deliverable authoring proceeds, gaps in Holistika's own canonical doctrine surface. Document them in `docs/wip/intelligence/<engagement-slug>/checkpoints/` (Tier 1 WIP).
4. **System diagnostic** — at engagement-completion or quarterly, aggregate methodology-diagnostic findings into a system-level audit.
5. **Promotion** — diagnostic findings promote (via blueprint §13 4-step ladder) to canonical extensions or initiative charters.

I70 itself is a worked example: SUEZ engagement (I12 P12) revealed deck-discipline + multilingual + brand-sub-discipline + Gantt-discipline + copywriting-discipline gaps → I70 master initiative landed those gaps as Phases 5/6/7.

## 5. Diagnostic templates (reserved)

- Counterparty-baseline-reality template (per-engagement; cross-link to Intelligence's `SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001`).
- System-health audit template (cross-link to P2.5 v3.0 vault audit as worked example).
- Methodology-gap audit template (cross-link to P2 synthesis as worked example).

Templates author at I71+ as the discipline matures.

## 6. Cross-references

- Parent: [`RESEARCH_AREA_CHARTER.md`](../../canonicals/RESEARCH_AREA_CHARTER.md)
- Sister disciplines: Intelligence (input source), Methodology (how-to), Validation (gate on diagnostic verdicts).
- Founder principle F-51: engagement-as-org-diagnostic.
- Worked example (engagement-level): SUEZ I12 P12 deck-discipline gap surfacing → I70 P5/P6/P7.
- Worked example (methodology-level): I70 P2 7-gap synthesis at [`docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/checkpoints/p13.0-canonical-dig-synthesis.md`](../../../../../wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/checkpoints/p13.0-canonical-dig-synthesis.md).
- Worked example (system-level): I70 P2.5 vault audit at [`docs/wip/planning/70-holistika-os-self-governance/reports/p2-5-v3-0-vault-audit-2026-05-12.md`](../../../../../wip/planning/70-holistika-os-self-governance/reports/p2-5-v3-0-vault-audit-2026-05-12.md).
