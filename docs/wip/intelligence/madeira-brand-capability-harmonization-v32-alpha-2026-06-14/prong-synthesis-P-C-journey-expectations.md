---
intellectual_kind: research_synthesis_prong
prong_id: P-C
prong_topic: User journeys and functionality expectation inventory
authored: 2026-06-14
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
control_confidence: Euclid
---

# Prong P-C — User journeys and functionality expectations

## Load-bearing finding

You need help **assessing what each functionality is for, who it serves, and what "good" looks like** because the surface changes every wave. The repo already has **pieces of an expectation system** but they are **not unified into one operator-facing inventory**:

- **5 MADEIRA modes** + 16 tool categories (`MADEIRA_MODE_PARITY`, `MADEIRA_TOOL_CATALOG`)
- **I17 coverage matrix** — Cursor Ask/Plan/Agent gaps
- **PERSONA_SCENARIO_REGISTRY** — alpha cohort scenarios
- **Governed operator journey UX** (Discover → Triage → Act → Audit) for Research Center
- **Experiential UAT charter** — separates validator PASS from operator PASS

What's missing: a **single capability ↔ journey ↔ expectation ↔ evidence** matrix the operator can read without hunting initiatives.

## Four alpha products under one MADEIRA brand

| Scenario | Product shape | Primary journey | Expectation anchor |
|:---|:---|:---|:---|
| **A — Cursor-local** | Agent in IDE + gateway | Mode parity (Ask…Methodology) | I17 matrix + three-lights conversational |
| **B — Sibling vault workspace** | HLK-ERP Research Center | Operator/director POV journeys | I96 experiential UAT + journey component matrix |
| **C — Hosted/SDK** | I74 madeira-agent | API/session SDK consumers | Deploy-health + auth tenancy spec |
| **D — Multi-org voice** (later) | Brand register per org | Quality Fabric 5-axis | AUDIENCE_REGISTRY + tenancy (not alpha-blocking) |

## External alpha discipline (SRC-MBH-EXT-013..015, 022)

Closed alpha readiness is **reliability judgment**, not feature checklist:

- 50–100 hand-picked users (B2B); retention gate ~40% week-4
- Track **verification behavior** (do users re-check AI output?) — signals trust
- Task **completion success** > engagement metrics
- Daily output review + weekly feedback synthesis during beta

Maps to Holistika: MADEIRA dossier three-lights + experiential UAT manifest pattern already encode this — **need explicit exit criteria doc for v3.2 alpha**.

## Functionality categories (seed for inventory matrix)

| Category | Example capabilities | Expectation question |
|:---|:---|:---|
| **Converse** | WebChat, Cursor chat, voice (future) | Does it stay in RBAC posture for mode? |
| **Govern** | Inline ratify, research action, carryover | Does operator retain decisions? |
| **Research** | Radar, ledger, synthesis, Research Center | Is ingest→govern→consume e2e proven? |
| **Build** | Planning tranches, code edit, deploy | Does synthesis-before-tranche fire? |
| **Observe** | Langfuse, dossier, gateway health | Can operator see cost/latency/errors? |
| **Economize** | Finops, infonomics, token attribution | Can we explain bill per cohort? |

## Gaps

| Gap | Closure |
|:---|:---|
| No unified functionality inventory | `capability-functionality-inventory-matrix.md` (this pack) → promote to I76 |
| Mode × tool × journey not cross-walked | CSV join: TOOL_RBAC × PERSONA_SCENARIO × CAPABILITY_REGISTRY |
| Expectations drift each wave | Tie each row to evidence class + last UAT path |
| Alpha exit criteria not written for v3.2 | Prong H + inline-ratify |

## Ranked insights

1. **Four scenarios = four products; one brand; shared governance spine** — RANK 1
2. **Experiential UAT is the expectation enforcement layer** (INT-010) — RANK 1
3. **External beta playbooks confirm dossier/three-lights direction** — RANK 2
