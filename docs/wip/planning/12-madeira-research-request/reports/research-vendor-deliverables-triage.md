# Vendor research deliverables — triage and evidence contract

**Initiative:** [12 — MADEIRA external research request](../master-roadmap.md)  
**Date:** 2026-04-17  
**SOC:** This report does not contain API keys, bearer tokens, full system prompts, or raw CSV rows.

## 1. Purpose

External research documents in this folder synthesize AKOS/MADEIRA architecture with industry narrative. This file tells **commissioning and product** how to use those deliverables without treating **unverified** or **illustrative** content as repository fact.

**Reference-only vendor files (not SSOT):**

- [`Researching Madeira AI Assistant.md`](../Researching%20Madeira%20AI%20Assistant.md)
- [`Researching MADEIRA Assistant in AKOS.md`](../Researching%20MADEIRA%20Assistant%20in%20AKOS.md)

**SSOT for product behaviour** remains: `docs/USER_GUIDE.md`, `docs/ARCHITECTURE.md`, `config/agent-capabilities.json`, `prompts/MADEIRA_PROMPT.md`, [`research-request-madeira.md`](../research-request-madeira.md), and HLK governance per [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../../../docs/references/hlk/compliance/PRECEDENCE.md).

## 2. Evidence classification rubric

When reviewing claims in the vendor documents, tag each major assertion:

| Tag | Meaning | Action |
|:----|:--------|:-------|
| **Repo-sourced** | Traceable to a named file/section in openclaw-akos | Safe for engineering backlog citations |
| **Stakeholder research** | Interviews, sessions, n noted | Valid for UX; cite methodology |
| **Literature / analogy** | External frameworks, case studies, market claims | Use for context; do not treat as shipped features |
| **Unverified** | Numbers, customer names, infra stacks, or UAT metrics without a path to repo or dated evidence | Do not prioritize without verification |

**Rule:** Only **Repo-sourced** and **Stakeholder research** (with method) should drive hard commitments. **Literature** and **Unverified** items become hypotheses or spikes.

## 3. Naming disambiguation — two different “four paths”

The commissioning brief [`research-request-madeira.md`](../research-request-madeira.md) defines **operator paths** for AKOS (how a user moves between modes):

| Path | Meaning (Initiative 12 brief) |
|:-----|:--------------------------------|
| Path 1 | Simple inquiry in Madeira (lookup ladder, citations) |
| Path 2 | Deeper vault work — **human** git/CSV/markdown workflow (not Madeira writes) |
| Path 3 | High-level coordination — escalation → Orchestrator → Architect → Executor → Verifier |
| Path 4 | Optional ops prose (standard/full Madeira; non-canonical drafts) |

The vendor document *Researching MADEIRA Assistant in AKOS* maps **four pillars** to Holistika **methodology** language (e.g. process engineering, business engineering, factor combination, foresight), tied to `process_list` / business framing.

**These are not the same model.** Product and research discussions must use explicit labels:

- **AKOS operator paths** — use “Path 1–4” as in `research-request-madeira.md`, or say “inquiry / vault / swarm / ops overlay.”
- **Holistika methodology pillars** — say “methodology pillars” or “process_list methodology workstream,” not “Path 2” unless you redefine it.

Mixing the two causes incorrect requirements (e.g. mapping “foresight” to swarm escalation without qualification).

## 4. UAT cross-check (vendor narrative vs in-repo evidence)

### 4.1 Initiative 11 — Madeira ops copilot (authoritative)

Canonical UAT for ops overlay behaviour is:

- [`docs/wip/planning/11-madeira-ops-copilot/reports/uat-madeira-ops-copilot-20260415.md`](../../11-madeira-ops-copilot/reports/uat-madeira-ops-copilot-20260415.md)

That report defines **S1–S4** (standup/cadence, handoff pack, negative admin escalation, intent exemplars) with **PASS (spec)** or **PASS (automated)** as stated. It does **not** include logistics/SAP warehouse scenarios, lithium-battery regulatory rows, or percentage accuracy figures.

**Conclusion:** Tables in vendor documents that resemble enterprise logistics UAT with quantitative outcomes are **not** evidenced by Initiative 11 repo files unless the vendor supplies separate, dated raw notes and you file them under `reports/` with SOC hygiene. Treat those tables as **illustrative or external** unless provenance is added.

### 4.2 Related automated / qualitative baselines

- Madeira Path B+C browser UAT: [`docs/wip/planning/10-madeira-eval-hardening/reports/uat-madeira-path-bc-browser-20260416.md`](../../10-madeira-eval-hardening/reports/uat-madeira-path-bc-browser-20260416.md)
- WebChat / HLK smoke dimensions: [`docs/uat/hlk_admin_smoke.md`](../../../../../docs/uat/hlk_admin_smoke.md)

Use these for **parity** with what the repo actually tested, not as automatic validation of vendor prose.

## 5. Testable UX hypotheses (from vendor themes, not as facts)

The following are **candidates for product research or evals**, not validated measurements:

1. **Acronym / label density** — Internal abbreviations cause wrong `hlk_*` resolution; mitigations might include disambiguation prompts or UI context (hypothesis; test with task studies).
2. **Escalation comprehension** — Users do not understand when to switch from Madeira to Orchestrator; test copy, handoff template visibility, and dashboard affordances.
3. **Verbose / tool visibility** — `verboseDefault` and `/verbose` affect trust and perceived freezes; align with `docs/USER_GUIDE.md` / `docs/ARCHITECTURE.md` guidance.
4. **Multi-agent latency** — Escalation paths may feel slow; measure perceived vs actual latency in controlled tests (no claim without instrumentation design).

## 6. Governance pointers (no new security decisions)

- **Initiative 11** ops overlay and **D-OPS** decisions: [`docs/wip/planning/11-madeira-ops-copilot/master-roadmap.md`](../../11-madeira-ops-copilot/master-roadmap.md)
- **`memory_store` deferral / scratch memory:** [`SECURITY.md`](../../../../../SECURITY.md) section 8a (Madeira ops copilot and scratch memory)
- **HLK asset class and canonical precedence:** [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../../../docs/references/hlk/compliance/PRECEDENCE.md)

Do not reinterpret SECURITY or D-OPS in this triage document; link only.

## 7. Suggested next steps for commissioning

1. **Maintain** the classified addendum in **section 8** when vendor or internal research updates; keep tags aligned with section 2 (see **section 8.1**).
2. File any future **raw** research artefacts under `reports/` with SOC review; avoid pasting secrets or full transcripts into git.
3. Prioritise backlog items only from **Repo-sourced** + verified **Stakeholder research** rows; park **Unverified** until evidence exists.

### Commissioning handoff (backlog prioritisation)

Use **section 8** finding IDs when talking to product:

| Priority | IDs | Basis |
|:---------|:----|:------|
| **Engineering-safe citations** | **F5–F8** | **Repo-sourced** — backlog items can cite paths in footnotes 2–4. |
| **UX / programme (with artefact refs)** | **F1–F3** | **Stakeholder research** — promote only with **artefact class + date** (footnote 1); F1 mechanism remains **hypothesis** until task studies. |
| **Park / spike** | **F4** (quantitative or third-party enterprise claims) | **Unverified** until SOC-safe raw notes or repo evidence; same bar as **section 4.1**. |
| **Strategy context only** | **F9–F10** | **Literature / analogy** + governance pointers — not shipped features or legal sign-off. |

## 8. Addendum — top findings and evidence classification

This addendum applies the rubric in **section 2** and separates **observed** (sessions / internal programme data) from **desk** (repo + industry literature). Tags on each finding are the primary classification; sub-bullets note **hypothesis** where the mechanism is not yet measured.

### 8.1 Maintenance contract (section 8)

When vendor or internal research changes:

- **Re-tag** each new or revised finding using **section 2** (do not invent informal labels).
- **Edit** the Part 1 / Part 2 tables and **footnotes** in place, or add a **dated** subsection (e.g. `### Addendum update — YYYY-MM-DD`) so history stays traceable without orphan claims.
- Keep **footnote 1** as commissioning-held only; keep repo paths in footnotes 2–6 accurate if files move.

### Part 1 — Observed findings (stakeholder sessions and field data)

| ID | Finding | Tag | Notes |
|:---|:--------|:----|:------|
| **F1** | **Friction in intent expression** — users often rely on dense internal terminology and acronyms that overlap across departments. | **Stakeholder research** | **Hypothesis (testable):** overlap may contribute to missed or ambiguous `hlk_*` resolution — see section 5. Does not claim logged failure rates without session artefacts. |
| **F2** | **Manual workarounds** — operations rely on manual steps (e.g. lead assignment workflows where automation is not yet available). | **Stakeholder research** | Sourced from internal workstream / programme documentation; see footnote 1. |
| **F3** | **Corporate incorporation ambiguity** — open decisions on legal-entity framing can delay formalisation of baseline processes and compliance evidence packs. | **Stakeholder research** | Programme-level; see footnote 1. Not a claim about current repo CSV state without a separate compliance audit. |
| **F4** | **Crisis / dependency mapping** — prospection discussions (e.g. multi-stakeholder operational crises) surface a need for structured, multi-hop views of document dependencies. | **Stakeholder research** | **Unverified** for any quantitative enterprise UAT or named third-party outcomes until SOC-safe raw notes exist (same bar as section 4.1). |

### Part 2 — Desk findings (repo-sourced architecture and industry context)

| ID | Finding | Tag | Notes |
|:---|:--------|:----|:------|
| **F5** | **MADEIRA read-only at gateway; escalation for mutations** — mutative tools are denied for Madeira in [`config/agent-capabilities.json`](../../../../../config/agent-capabilities.json); escalation uses routing / swarm path (operator **Path 3** per [`research-request-madeira.md`](../research-request-madeira.md)). | **Repo-sourced** | See footnote 2. |
| **F6** | **Initiative 11 ops overlay** — `OVERLAY_MADEIRA_OPS.md` applies to Madeira **standard/full** ([`config/model-tiers.json`](../../../../../config/model-tiers.json)); operator **Path 4** (ops prose). UAT **S1–S3** are **PASS (spec)**; **S4** is **PASS (automated)** per dated report — not “all automated.” | **Repo-sourced** | See footnotes 2–3. |
| **F7** | **Precedence contract** — canonical compliance assets override mirrored projections per [`PRECEDENCE.md`](../../../../../docs/references/hlk/compliance/PRECEDENCE.md). | **Repo-sourced** | Retrieval behaviour for HLK tools follows governance in repo docs; see footnote 2. |
| **F8** | **Local Ollama context default** — Ollama defaults to a **4096-token** `num_ctx` unless overridden; large session bootstrap (SOUL, prompts) can be truncated. **Mitigation in repo:** committed Modelfiles under [`config/ollama/`](../../../../../config/ollama/) and guidance in [`docs/ARCHITECTURE.md`](../../../../../docs/ARCHITECTURE.md) / [`docs/USER_GUIDE.md`](../../../../../docs/USER_GUIDE.md). | **Repo-sourced** | See footnote 4. |
| **F9** | **Enterprise AI ROI framing** — sector narrative shifting from simple “time saved” to outcome velocity and compound workflow effects. | **Literature / analogy** | Not a shipped KPI; see footnote 5. |
| **F10** | **Regulatory and governance context** — EU AI Act and similar regimes emphasise traceability and oversight. **Repo alignment (high level):** [`SECURITY.md`](../../../../../SECURITY.md) (section 7, EU AI Act 2026 Compliance), [`config/compliance/eu-ai-act-checklist.json`](../../../../../config/compliance/eu-ai-act-checklist.json), Verifier role in [`docs/ARCHITECTURE.md`](../../../../../docs/ARCHITECTURE.md) — not a substitute for legal sign-off. | **Literature / analogy** + **pointers** | See footnote 6. |

### Disambiguation for product backlog

Same contract as **section 3**: do **not** conflate **AKOS operator paths** (Path 1 inquiry → Path 2 vault/human → Path 3 swarm escalation → Path 4 ops overlay) with **Holistika methodology pillars** (process engineering, business engineering, factor combination, foresight).

### Footnotes

1. **Internal programme / workstream material** — Holistika commissioning-held notes or internal docs (e.g. prospection, operations). Not reproduced here (SOC). When citing externally, use artefact class + date, not raw tables.
2. **Repo SSOT** — [`config/agent-capabilities.json`](../../../../../config/agent-capabilities.json), [`prompts/MADEIRA_PROMPT.md`](../../../../../prompts/MADEIRA_PROMPT.md), [`research-request-madeira.md`](../research-request-madeira.md), [`docs/ARCHITECTURE.md`](../../../../../docs/ARCHITECTURE.md).
3. **Initiative 11 UAT** — [`docs/wip/planning/11-madeira-ops-copilot/reports/uat-madeira-ops-copilot-20260415.md`](../../11-madeira-ops-copilot/reports/uat-madeira-ops-copilot-20260415.md) (scenario matrix: S1–S3 PASS (spec), S4 PASS (automated)); [`docs/wip/planning/11-madeira-ops-copilot/master-roadmap.md`](../../11-madeira-ops-copilot/master-roadmap.md).
4. **Ollama `num_ctx`** — [`docs/ARCHITECTURE.md`](../../../../../docs/ARCHITECTURE.md) (Ollama context / Modelfile guidance), [`docs/USER_GUIDE.md`](../../../../../docs/USER_GUIDE.md) (troubleshooting), [`config/ollama/`](../../../../../config/ollama/) (committed Modelfiles).
5. **Industry / market framing** — desk sources outside this repo; use for context only.
6. **Governance pointers** — [`SECURITY.md`](../../../../../SECURITY.md) section 7 (EU AI Act 2026 Compliance); [`config/compliance/eu-ai-act-checklist.json`](../../../../../config/compliance/eu-ai-act-checklist.json); [`docs/ARCHITECTURE.md`](../../../../../docs/ARCHITECTURE.md) (multi-agent stack, compliance table). Compare to sector literature under F9–F10, not as equivalence.

---

*This report satisfies Initiative 12 post-research triage traceability; it does not close Initiative 12 unless the master roadmap is updated separately.*
