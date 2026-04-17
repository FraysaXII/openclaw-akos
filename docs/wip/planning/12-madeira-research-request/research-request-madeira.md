# Research request — MADEIRA

**To:** Research team  
**Subject:** Independent discovery of use cases, technology fit, frameworks, and user journeys for the MADEIRA assistant in AKOS.

---

## Background you need (as-built)

Behaviour and limits are defined in the **openclaw-akos** repository. The **standalone summaries** in the table below are enough to orient interviews and reports; repository paths are for engineers who need to verify line-level detail.

- **Five agents:** Madeira (user-facing), Orchestrator, Architect, Executor, Verifier.
- **Madeira** is the user-facing assistant for Holistika (HLK)–related questions via registry tools; **read-only at the gateway** for work that belongs to execution or admin paths; escalation to the multi-agent **swarm** is the designed path for writes and execution (see summaries below).

**System-of-record artefacts (what each is, without opening the repo)**

| Topic | What it is (self-contained) | Path in repo (verification) |
|:------|:----------------------------|:----------------------------|
| Operator guide | End-user documentation: how to run AKOS, select agents in WebChat, GPU/RunPod, MCP servers, Langfuse/telemetry, HLK Registry MCP, dashboard URLs, prompt tiering tables, and **§24 HLK Operator Model** (how to operate the vault through MADEIRA). | `docs/USER_GUIDE.md` |
| Architecture | System design: five-agent model, Madeira’s role and **minimal** tool profile, model **tiers** (small/medium/large/sota) and **prompt variants** (compact/standard/full), SOUL/workspace loading, Langfuse wiring, multi-provider config, HLK registry scale notes. | `docs/ARCHITECTURE.md` |
| Madeira prompt (shipped behaviour) | The full instruction set for Madeira: mandatory session startup reads (`IDENTITY.md`, `USER.md`, etc.), **lookup ladder** for HLK tools (`hlk_role` → `hlk_search` on miss, etc.), finance mode, **escalation** when the user asks for code/shell/browser writes or admin mutations, allowed tools list, guardrails (no fabrication, citation rules, memory vs vault). | `prompts/MADEIRA_PROMPT.md` |
| Base prompt + assembly | `MADEIRA_BASE.md` is the base fragment; `assemble-prompts.py` merges base + overlays into `prompts/assembled/MADEIRA_PROMPT.{compact,standard,full}.md` per tier. | `prompts/base/MADEIRA_BASE.md`, `scripts/assemble-prompts.py` |
| Tier → overlay mapping | JSON **SSOT**: which overlay files attach to **compact** vs **standard** vs **full** for each agent. For Madeira, **compact** adds HLK+startup compact only; **standard/full** add HLK graph + (for Madeira) `OVERLAY_MADEIRA_OPS`. | `config/model-tiers.json` → key `variantOverlays` |
| Tool matrix (hard permissions) | **Authoritative** allow/deny lists per agent role. `madeira` includes HLK + finance + routing + read-only browser observation tools; **denies** writes, shell, interactive browser, `memory_store`, git push/commit, etc. Prompts cannot override this file. | `config/agent-capabilities.json` → `roles.madeira` |
| Intent / routing exemplars | JSON used with `akos_route_request` and related routing; supports exemplar-based classification (not the research brief). | `config/intent-exemplars.json` |
| Ops overlay (Madeira, standard/full only) | Extra prompt text for non-canonical **drafts**, standup-style outlines, meeting-prep scaffolding, and a structured **Orchestrator handoff pack**—still read-only for registry mutations. **This is current product wording**, not a research mandate. | `prompts/overlays/OVERLAY_MADEIRA_OPS.md` |
| Initiative 11 (ops copilot) | Internal roadmap: goal to strengthen day-to-day support **without** widening write tools; decisions D-OPS-1…4 (overlay tiering, `memory_store` deferred, intent exemplars). | `docs/wip/planning/11-madeira-ops-copilot/master-roadmap.md` |
| Security (Madeira ops) | Threat-model note: Initiative 11 is prompt-only; **persistent scratch** via `memory_store` deferred until reviewed. | `SECURITY.md` (section on Madeira ops / scratch) |
| HLK precedence contract | Defines **canonical** CSVs/MD vs **mirrored** (KiRBe, Neo4j, Drive) vs **reference-only**; conflict resolution (**canonical wins**); vault v3.0 vs Research & Logic. | `docs/references/hlk/compliance/PRECEDENCE.md` |
| HLK Operator Model | **How operators move from inquiry → vault work → swarm coordination** — see **subsection below** (this row is not redundant; it points to the same content summarized here). Operator manual with task tables, promotion ladder, and CSV maintenance lives in USER_GUIDE §24. | `docs/USER_GUIDE.md` §24 |
| Active vault index | Map of **v3.0** vault folder structure (organigram-aligned), entity placement, navigation—**active** vault; v2.7 under Research & Logic is historical. | `docs/references/hlk/v3.0/index.md` |

### HLK Operator Model — inquiry to coordination (self-contained)

The **HLK Operator Model** is documented at length in USER_GUIDE §24. This subsection gives the **granular transitions** researchers asked for, so the briefing is not “truncated” at a section reference.

**Three layers of state (always distinguish these):**

| Layer | Meaning | Lifetime |
|:------|:--------|:---------|
| **Session** | One chat thread with an agent | Ends when the chat closes or resets |
| **Workspace** | Per-agent folder (`~/.openclaw/workspace-{agent}/`) with identity, memory, rules | Persists across sessions; **not** the business SSOT |
| **Vault** | Canonical HLK knowledge (CSVs + v3.0 markdown), versioned in git | **Source of truth** for org and process facts |

**Operating rule:** Business facts come from the **vault** (via tools), not from chat memory.

---

**Path 1 — Simple inquiry (stays in Madeira)**

1. User opens WebChat, selects **Madeira** (or follows deep link in USER_GUIDE).
2. User asks a factual question (role, process, area, gap, search).
3. Madeira runs the **lookup ladder** (`hlk_role` / `hlk_process` / … → `hlk_search` when needed), batches reads where appropriate.
4. User receives an answer with **citations to canonical asset names** (e.g. `baseline_organisation.csv`, `process_list.csv`), not raw file paths.
5. No registry mutation occurs; session may store context only.

This path supports “simple inquiry” end-to-end without leaving Madeira.

---

**Path 2 — “Deeper vault” work (human operator; not Madeira writes)**

Changing the vault (new SOP, new `process_list.csv` row, org baseline edit) is a **human-led git workflow** in the repository, not a button inside chat. Documented steps (abbreviated from §24) are:

1. **Identify the owning role** (from the organigram / `baseline_organisation.csv`).
2. **Open the correct v3.0 folder** under `docs/references/hlk/v3.0/Admin/O5-1/{area}/{role}/` (or compliance CSVs for baseline rows).
3. **Author or edit markdown** (and follow Topic–Fact–Source / manifest rules for governed KM artefacts where applicable).
4. **Register new processes** in `process_list.csv` when the item must appear in the runtime registry (parent names/ids, granularity, owner).
5. **Validate** (e.g. `py scripts/validate_hlk.py`; manifests: `validate_hlk_km_manifests.py` where relevant).
6. **Commit / review** through normal engineering governance.

Madeira **reads** the result via tools after deployment; it does **not** perform these writes. Interviews should treat “operator adds knowledge” as **this path**, distinct from chatting with Madeira.

---

**Path 3 — High-level coordination (execution / code / multi-step automation)**

When the user needs work that **mutates repos, runs shell or browser automation, or applies multi-step MCP actions**, the product design routes away from Madeira:

1. **Classification** — `akos_route_request` (and related intent handling) can label the turn as lookup, finance, **admin escalation**, or **execution escalation**.
2. **Madeira’s first response** — States the limitation and provides a **handoff** (goal, grounding so far, suggested swarm: Orchestrator → Architect → Executor → Verifier). Optional **standard/full** prompt adds an “ops” handoff-pack block; still no writes.
3. **User switches context** — Operator opens **Orchestrator** in the dashboard (or continues in a workflow scoped to the swarm).
4. **Orchestrator** — Produces a **delegation plan** (tasks, agents, dependencies, HITL gates).
5. **Architect** — Read-only planning; may use browser/research tools per policy; outputs a **Plan Document**.
6. **Executor** — Performs writes, shell, MCP, git per plan and **HITL** (auto vs requires approval).
7. **Verifier** — Validates (tests, lint, browser checks); loop back to Executor on failure (bounded retries), then back to Orchestrator/user.

So “transition from simple inquiry to high-level coordination” in production is: **successful lookups in Madeira** until intent crosses the read/write boundary → **explicit escalation language** → **different agent(s)** carrying out plans with human approval where configured—not a hidden deepening of the same chat mode into registry edits.

---

**Path 4 — Day-to-day prose help (optional, standard/full Madeira only)**

On **medium+** prompt variants, Madeira may help with **non-canonical drafts** (labeled), checklists, or meeting-prep **text** grounded with `hlk_*` when facts matter. That does **not** replace Path 2 or Path 3.

---

## Holistika, processes, compliance, and governance (context)

This block is **background for researchers** so interviews and artefacts align with how Holistika defines truth and change. It summarises `docs/references/hlk/compliance/PRECEDENCE.md` and the HLK Operator Model in `docs/USER_GUIDE.md` (§24); the **canonical text** remains in those files. **Path 1–4 above** are the missing “operator journey” bridge.

### Holistika and the HLK knowledge vault

**Holistika** operates a structured **Holistika Knowledge (HLK)** vault: organisational roles and areas, a **process baseline** (projects, workstreams, processes, tasks, and related metadata), and **role-owned** procedures and documents. **MADEIRA** is described in-repo as the user-facing assistant for questions about that vault, using **read-only registry tools** so answers can be grounded in the same sources operators maintain.

**Vault versions:** The **active** canonical knowledge tree is **`docs/references/hlk/v3.0/`** (folder structure aligned with the organigram). Older material under `docs/references/hlk/Research & Logic/` (e.g. v2.7) is **reference-only**; v3.0 wins when both cover the same topic. Navigation: `docs/references/hlk/v3.0/index.md`.

### Canonical vs mirrored vs reference-only (precedence)

Per **PRECEDENCE**, assets fall into three classes:

- **Canonical (author here first):** e.g. `baseline_organisation.csv`, `process_list.csv`, compliance taxonomies (`access_levels.md`, `confidence_levels.md`, `source_taxonomy.md`), meta-SOP `SOP-META_PROCESS_MGMT_001.md`, KM contract `HLK_KM_TOPIC_FACT_SOURCE.md`, role-owned SOPs under `v3.0/`, and `PRECEDENCE.md` itself.
- **Mirrored (derived; resync from canonical):** e.g. KiRBe/Supabase mirrors, Drive hierarchy, Neo4j graph index (read-optimized; not an authoring surface for baselines), repository typings where noted.
- **Reference-only:** historical exports, SQL dumps, superseded CSVs under Research & Logic, example-only project trees — **not** edited as current truth.

**Conflict rule:** If canonical and a mirror disagree, **canonical wins**; fix drift at the mirror and document incidents per PRECEDENCE.

### Processes and the process baseline

The **process baseline** is `process_list.csv`: registered items (including projects, workstreams, processes, tasks), ownership, granularity, and parent relationships (including optional program-style groupings per in-repo conventions). **Operator-approved changes** to this file are gated (validation, approval, documentation sync) as described in governance rules and `docs/USER_GUIDE.md` (HLK Operator Model). MADEIRA is **not** the write path for those edits; it **reads** via tools so users get consistent answers without treating chat as registry mutation.

### Compliance and taxonomy

Shared **compliance** definitions (access levels, confidence levels, source taxonomy) and the **Topic–Fact–Source** knowledge-management contract live under `docs/references/hlk/compliance/`. They constrain how facts are classified and cited across vault, KiRBe, and tooling. Full detail: `HLK_KM_TOPIC_FACT_SOURCE.md` and related files listed in PRECEDENCE.

### Repositories, PMO, and “where code lives”

Holistika tracks many **GitHub** repositories; the **vault registry** (`docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` and policy README there) is the Holistika-facing record for governance and linking — **not** a replacement for each repo’s source tree. PMO/client-delivery topic indexes and portfolio tables are described in USER_GUIDE §24 and `v3.0/index.md`.

### AKOS-specific governance notes (product)

- **Tooling SSOT:** Agent tool access is declared in `config/agent-capabilities.json`; prompts do not override deny lists.
- **EU AI Act / evidence:** The repo tracks compliance evidence (e.g. checklist under `config/compliance/`); Langfuse/telemetry usage follows SOC rules in `docs/USER_GUIDE.md` and `docs/ARCHITECTURE.md` — relevant if research touches observability or risk narratives.
- **Research stance:** Understanding **Holistika’s precedence and change model** helps researchers interpret user expectations (e.g. “change the org chart” vs “tell me who reports to whom”) without directing **what** the product should build.

---

## What we are asking you to research

Design your own methods. We want **evidence-backed** outputs on:

1. **Use cases** — What people try to do with MADEIRA (or would), in their own words; what belongs to a read-only, HLK-grounded assistant vs other agents or systems.
2. **Technology and surfaces** — What channels, tools, and constraints matter in practice (not limited to what ships today).
3. **Frameworks** — Governance, trust, org models, or other concepts that should shape UX (you identify which apply).
4. **User journeys** — Real paths: success, failure, workaround, abandonment; gaps vs documented intent where relevant.
5. **Gaps and recommendations** — What is missing vs needs; features are **not** predetermined. Do not treat text inside `OVERLAY_MADEIRA_OPS.md` or other prompts as the research brief — it is current product wording only.

---

## Deliverables

1. Findings report (methods, evidence, limitations; SOC-safe handling of secrets and prompts).
2. Use-case and journey artefacts as you judge appropriate.
3. Prioritised recommendations with traceability to evidence.

---

## Out of scope for this engagement

- Code or config changes in this repository (unless separately contracted).
- Edits to canonical HLK compliance CSVs or vault-of-record content.

---

*Commissioning party uses your feedback for product planning; this document is the sole briefing for scope and context. For how to read vendor follow-up documents without treating unverified claims as repo truth, see [`reports/research-vendor-deliverables-triage.md`](reports/research-vendor-deliverables-triage.md).*
