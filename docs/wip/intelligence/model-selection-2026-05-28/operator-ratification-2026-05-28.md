---
title: Operator ratification — model-selection decision questions (2026-05-28)
language: en
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP
authored: 2026-05-28
last_review: 2026-05-28
status: ratified
linked_research_sources:
  - docs/wip/intelligence/model-selection-2026-05-28/source-ledger.csv
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
---

# Operator ratification — DQ-MS-01..06

> Verbatim operator input distilled into durable routing posture for the
> model-selection knowledge base. Ratified 2026-05-28 in-session.

## Summary table

| ID | Question (short) | Verdict |
|:---|:---|:---|
| **DQ-MS-01** | Data residency — API vs self-host for client work | **Engagement-scoped hybrid** (see below) |
| **DQ-MS-02** | Composer / Kimi lineage + EU posture | **Law-bound neutrality**; internal OSS preference; managed external register |
| **DQ-MS-03** | Mint SUBSTRATE_REGISTRY rows for V4 + K2.6 | **Yes — candidate rows now** (same tranche as this KB) |
| **DQ-MS-04** | Multimodal GPU posture | **Hybrid:** local Ollama/small + RunPod for FLUX/video |
| **DQ-MS-05** | Brand gate on AI images | **Yes** for external; draft WIP internal-only exempt |
| **DQ-MS-06** | SUEZ demo visuals | **Internal-only**; Mermaid/wireframes base + upgrade to polished professional (AI or not) |

---

## DQ-MS-01 — Data residency (DeepSeek / Kimi / Qwen APIs)

**Operator stance:** wants **flexibility** and **best practice** — not a single binary.

**Ratified posture (engagement-scoped hybrid):**

| Context | Default | Override path |
|:---|:---|:---|
| **SUEZ-class / customer code / engagement payloads** | **Self-host or Holistika-controlled inference** (RunPod vLLM, EU-region contract, or air-gapped Ollama). Third-party OSS vendor APIs **off by default**. | Engagement addendum + inline ratify if API is explicitly accepted (document residency + retention in engagement folder). |
| **Holistika-internal** (CORPINT, AKOS dev, WIP intelligence, non-customer repos) | **API allowed** for DeepSeek / Kimi / Qwen tiers when cost/latency wins. | Prefer self-host when volume justifies RunPod economics. |
| **Production MADEIRA routes touching CRM/ERP/customer mirrors** | Treat as **client-class** until proven otherwise. | Same as SUEZ-class. |

**Best-practice anchor:** default to the stricter lane; relax only with named engagement scope + audit trail — not repo-wide config drift.

---

## DQ-MS-02 — Composer 2.5 / Kimi K2.5 lineage and compliance posture

**Operator stance (meta-political neutrality):**

- Holistika is **Spanish**, **research-led**, **not politically aligned** with any state or bloc.
- Bound by **law and ethics**, not by popular sentiment or economic boycotts of the past.
- **Researchers, not politicians** — geopolitics is a research topic category, not a brand identity.
- **Will not endorse unethical instances**; will **not perform blanket exclusion** of capable open-source stacks for origin alone.
- **Internal preference:** DeepSeek and Kimi (and comparable open-weight stacks) for **democratic token economy** and open-source posture — silent operational bias, not public slogan.

**Does Kimi lineage block defaulting to Composer?**

**No** for internal Cursor default — Composer remains the execution default per field test.

**Valid reasons to *not* use Kimi** (when they apply — not moral blanket):

| Reason | When it fires |
|:---|:---|
| **Modified MIT / license class** at enterprise self-host scale | Compliance review for redistribution or multi-tenant product |
| **Customer engagement API ban** | DQ-MS-01 SUEZ-class path |
| **EU data residency contract** | Customer DPA requires EU-only inference; Kimi API region may not qualify |
| **Benchmark skepticism** | Procure on Holistika eval, not leaderboard (SRC-MS-16/17) |
| **Disclosure request** | Counterparty asks model lineage — answer factually; offer self-host alternate |

**External messaging discipline (binding):**

- **Internal register (CORPINT):** may name DeepSeek, Kimi, Moonshot, origin, license, token economics.
- **External register:** lead with **capability, cost, license, eval results, residency controls** — not origin narrative or geopolitics.
- If asked directly: factual, neutral, law-framed answer; pivot to **Holistika eval + engagement controls**.
- See dual-register pattern in `BRAND_BASELINE_REALITY_MATRIX.md` §3.

---

## DQ-MS-03 — SUBSTRATE_REGISTRY candidate rows

**Verdict:** Mint **now** in the same initiative as this KB commit.

| substrate_id | status | Notes |
|:---|:---|:---|
| `SUBS-DEEPSEEK-DEEPSEEK-V4` | `candidate` | Flash + Pro tiers; pending Holistika eval before `active` |
| `SUBS-MOONSHOT-KIMI-K26` | `candidate` | K2.6 agentic tier; Modified MIT flag; pending eval |

Rows land in `SUBSTRATE_REGISTRY.csv` with `akos_integration_state=candidate`.

---

## DQ-MS-04 — Multimodal GPU posture

**Verdict:** **Hybrid**

- **Local:** Ollama + small multimodal smoke; operator laptop / future RTX workstation for ComfyUI experiments when hardware lands.
- **Cloud:** RunPod for **FLUX** image pipelines and **Wan**/video when VRAM or time-box demands it.
- Do not block R&D on “cloud-only” or “local-only” — route by **VRAM need + engagement deadline**.

---

## DQ-MS-05 — Brand gate on AI-generated images

**Verdict:** **Yes** — any **external audience** (investor, customer, partner, regulator, etc.) requires Brand Manager review (or delegated brand-token check) before send.

**Exempt:** draft WIP under `docs/wip/` and internal-only CORPINT — matches **external-render discipline** (markdown/AI draft ≠ delivery surface).

---

## DQ-MS-06 — SUEZ deep demos (visuals)

**Verdict:** **Internal-only delivery posture** (Option B — not customer-facing AI mockups as SSOT).

- **Primary:** Mermaid diagrams + Power Apps / wireframe-class artifacts (current posture holds).
- **Upgrade intent:** same information architecture, but **more beautiful, trendy, professional** presentation — **AI-generated or not**, as long as it stays **internal or niche** surfaces until brand + render trail clear external bar.
- Do **not** ship raw AI UI mockups to SUEZ as deliverable SSOT without Figma/render path.

---

## Field-test note cross-link

Composer Iteration 1 interpretive pass: operator may fill verdict in
`field-test-note.md` §"Operator verdict" separately from these governance
decisions.

## Implement checklist (post-ratification)

- [x] `operator-ratification-2026-05-28.md` (this file)
- [x] `SUBSTRATE_REGISTRY.csv` candidate rows (DQ-MS-03)
- [ ] `config/model-tiers.json` OSS slot mapping — forward I84 / Tech after eval
- [ ] Engagement template addendum stub for DQ-MS-01 API-vs-self-host — forward charter
- [ ] Operator scratchpad drain entry at commit time
