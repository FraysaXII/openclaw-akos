---
status: in_flight
classification: working
access_level: 5
language: en
register: internal
folder_id: substrate-audit-2026-Q2
target_initiatives: [INIT-OPENCLAW_AKOS-84]
target_strands:
  - I84 P1 Layer 1 — substrate landscape audit (4 threads: agent-SDK + competitive + regulatory + past-PoC)
  - I84 P4 batched ratification (D-IH-84-B/C/D/E) — uses this dossier as evidence input
recorded_at: 2026-05-17
---

# substrate-audit-2026-Q2 — Tier-1 WIP dossier (working space)

> **Purpose.** Tier-1 WIP per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §17 (intelligence-tier workspace). Cluster for the [I84](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) P1 substrate-landscape audit + supporting evidence. Each file under this folder is a self-contained audit thread; the synthesis output landing at [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) reads from these threads.

This folder is **internal working space** (`access_level: 5`). It is **not canonical** — it does not promote to `SUBSTRATE_REGISTRY.csv` / `SUBSTRATE_LANDSCAPE_DOCTRINE.md` directly. The promotion path is through I84 P3 canonical-mint phase (operator-gated) where audit rows are reviewed + filtered + ratified.

## Audit threads (4 threads; per master-roadmap §3 P1 Layer 1)

| Thread | File | Status | Notes |
|:---|:---|:---|:---|
| **Thread A — Agent-SDK comparison matrix** | (collapsed into P1 audit report) | Done | Lives at [`p1-substrate-landscape-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) §3 + §4 + §5. 17 substrates × 18 attributes. |
| **Thread B — Competitive layer positioning** | [`competitive-layer-positioning.md`](competitive-layer-positioning.md) | Done | Glean / Notion AI / Anthropic Projects / OpenAI Apps SDK / Microsoft Copilot Studio / Google Gemini for Workspace / Composio / Lindy — 8 competitors × structured rows. |
| **Thread C — Regulatory + ToS forecast** | [`regulatory-tos-forecast.md`](regulatory-tos-forecast.md) | Done | EU AI Act provider-vs-deployer 2026 + GDPR-as-SaaS DPA cascading + Cursor MSA evolution forecast + IP-indemnity carve-outs across SDKs. |
| **Thread D — Past-PoC translation matrix** | [`past-poc-translation-matrix.md`](past-poc-translation-matrix.md) | Done | I10 Madeira eval hardening (closed) + I11 Madeira ops copilot (active) + I12/I13 Madeira research lineage (superseded by I84) + KiRBe-still-on-LlamaIndex + R&L v2.7 framework references. |

## Existing evidence in this folder (pre-2026-05-17)

| File | Authored | Purpose |
|:---|:---|:---|
| [`openclaw-observed-symptoms-2026-05-16.md`](openclaw-observed-symptoms-2026-05-16.md) | 2026-05-16 | Real-world reliability evidence on OpenClaw observed during a 6-hour silent-fail window. Feeds I84 P1 Thread A OpenClaw row + I87 charter (5-strand operational hardening). |

## Cross-references

- [I84 master-roadmap](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) §3 P1 — the deliverable contract this folder serves.
- [I84 P1 audit report](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) — the operator-readable synthesis (Thread A scope).
- [I84 P2 scorecard](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md) — the 17×6 dimensional scoring grid (feeds P4 ratification).
- [I84 self-checkpoint](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/checkpoints/sc-i84-p1p2-complete-2026-05-17.md) — Tier-1 WIP scope expansion noted in §7 risk #2; this folder addresses that gap.
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md` §17](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — Tier-1 WIP folder convention.
- [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) — reference-only classification (Tier-1 WIP is not canonical).
