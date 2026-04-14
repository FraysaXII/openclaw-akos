# AKOS / MADEIRA Method Adoption Memo

**Document owner**: Operator (Admin / O5-1)
**Version**: 0.1
**Date**: 2026-04-02
**Status**: Draft
**Classification**: Level 6 -- Restricted Internal Research Synthesis
**Program mapping**: Support memo for `madeira_ultimate_agent_e97ddcd9.plan.md`
**Canonical plan**: `C:\Users\Shadow\.cursor\plans\madeira_ultimate_agent_e97ddcd9.plan.md`

---

## 1. Executive Summary

This memo translates redacted external harness-engineering research into practical AKOS and MADEIRA method improvements. The goal is not to copy foreign systems or prompts verbatim, but to extract what materially improves planning quality, runtime safety, answer grounding, and verification discipline in this repo.

The key conclusion is:

- **Adopt** parity auditing, anti-fabrication discipline, stronger tool-contract translation, and evidence-first UAT.
- **Adapt** coordinator-mode, memory consolidation, and task-orchestration ideas so they fit AKOS SSOT / MCP / HLK governance.
- **Reject** second orchestration frameworks, authorship-obfuscation patterns, and delight-only features that do not improve governed operator value.

---

## 2. Research Basis (Redacted)

This memo is derived from:

- internal workspace research and code-reading
- redacted external harness/prompt studies
- redacted transcript-based research notes
- repo-native AKOS / HLK governance materials

All explicit external source names are intentionally withheld from this document. This memo should be treated as an internal synthesis of research outcomes, not a source catalog.

---

## 3. Practical Adoption Matrix

| Research stream | High-signal idea | Practical value for AKOS / MADEIRA | Decision |
|-----------------|------------------|------------------------------------|----------|
| External runtime/tooling research [REDACTED-L6] | Explicit tool contracts (`isReadOnly()`, `checkPermissions()`, `isConcurrencySafe()`) | Improves how AKOS models tool semantics and bootstrap translation | **Adopt** |
| External runtime/tooling research [REDACTED-L6] | MCP discovery + task tools + subsystem separation | Helps keep AKOS runtime and tool translation explicit and testable | **Adopt** |
| External parity research [REDACTED-L6] | Parity audits between target runtime and source architecture | Directly useful for bootstrap/runtime/dashboard/doc parity in AKOS | **Adopt** |
| External orchestration workflow research [REDACTED-L6] | Parallel review and persistent verification loops | Useful as method inspiration for parallel review + persistent verification loops | **Adapt** |
| External prompt-corpus research [REDACTED-L6] | Search ladder, anti-fabrication, todo/status cadence, completion discipline | Directly useful for MADEIRA prompt behavior and AKOS planning norms | **Adopt** |
| IDE workflow documentation research [REDACTED-L6] | Rules as long-term memory, context-first planning, docs-from-conversations | Directly useful for workspace rules, planning skill, and report generation | **Adopt** |
| Transcript-based harness analysis [REDACTED-L6] | Offline memory consolidation | Potentially useful later for session-memory hygiene, not for canonical HLK facts | **Adapt later** |
| Transcript-based harness analysis [REDACTED-L6] | Coordinator mode | AKOS already has orchestrator/architect/executor/verifier; adapt only for handoff rigor | **Adapt** |
| Transcript-based harness analysis [REDACTED-L6] | Authorship-obfuscation patterns | Conflicts with provenance/transparency goals in this repo | **Reject** |
| Transcript-based harness analysis [REDACTED-L6] | Companion / delight-only entity patterns | Delight feature, not governed operator value | **Reject** |
| Broad framework evaluation | Framework-level orchestration + retrieval | Overkill; would compete with AKOS orchestration and weaken SSOT clarity | **Reject** |

---

## 4. Adopt Now

### 4.1 Runtime Parity Audit

Derived from the external parity research stream [REDACTED-L6]:

- treat runtime consistency as a **parity problem**, not just a broken config
- compare the following surfaces explicitly:
  - `config/agent-capabilities.json`
  - `config/openclaw.json.example`
  - `scripts/bootstrap.py`
  - live `~/.openclaw/openclaw.json`
  - `/agents` dashboard view
  - `docs/ARCHITECTURE.md`, `docs/USER_GUIDE.md`, `docs/uat/hlk_admin_smoke.md`

**Practical next step**:
- add a named parity-audit subsection to the remediation report
- add targeted tests for translation parity, not only broad regressions

### 4.2 Explicit Tool Contract Modeling

Derived from the external runtime/tooling research stream [REDACTED-L6]:

- separate **policy name**, **gateway core ID**, and **MCP registered tool name**
- make bootstrap translation explicit, not heuristic

**Practical next step**:
- refine AKOS built-ins to clearly distinguish:
  - AKOS logical tool semantics
  - gateway-enforced core tool IDs
  - MCP plugin names exposed via `alsoAllow`

### 4.3 Anti-Fabrication by Default

Borrow from SOTA prompt corpora and confirmed by live Madeira failure:

- never fill missing facts with plausible-looking prose
- if a tool result is missing, malformed, or uncertain, say so explicitly
- never leak internal tool names in end-user answers

**Practical next step**:
- encode this in `MADEIRA_BASE.md`
- enforce it in the UAT acceptance matrix
- add a regression guard where possible

### 4.4 Evidence-Backed UAT

Derived from IDE workflow research [REDACTED-L6] and transcript-based analysis [REDACTED-L6]:

- real browser UAT is a first-class sign-off surface
- test what the user actually sees, not only API responses

**Practical next step**:
- keep browser MCP UAT as a developer workflow
- require canonical cross-checks against `baseline_organisation.csv` and `process_list.csv` for acceptance

---

## 5. Adapt Carefully

### 5.1 Coordinator-Mode Handoff Rigor

The coordinator-mode pattern from redacted harness research is useful, but AKOS already has its own 5-agent split.

What to adapt:

- Orchestrator handoffs should be more explicit
- verification should remain independent from implementation
- write/admin work requested through MADEIRA should hand off with visible scope and constraints

What not to copy:

- no new coordination framework
- no second orchestration layer

### 5.2 Memory Consolidation

The transcript-derived offline memory consolidation pattern is interesting.

What to adapt later:

- summarize volatile session memory or telemetry into durable, derived operator notes
- never treat these summaries as canonical HLK facts

Where it could fit:

- telemetry and answer-quality review
- operator notes / session digests
- runtime UX report aggregation

What must never happen:

- no automated rewrite of canonical HLK compliance CSVs
- no vector index treated as source of truth

### 5.3 Swarm / Harness Workflow Patterns

The `$team` and `$ralph` ideas are useful as **method**, not product.

Translate them into AKOS as:

- `$team` -> parallel exploration/review passes when gathering evidence
- `$ralph` -> persistent verification discipline until the issue is genuinely closed

This already aligns with:

- our governance planning skill
- browser UAT + verification gates
- phase-scoped commits and reports

---

## 6. Reject for This Repo

### 6.1 Second Orchestration Frameworks

Reject for AKOS / MADEIRA:

- a broad framework-style orchestration or runtime layer
- any sidecar agent framework that duplicates OpenClaw + MCP + AKOS policy

Why:

- AKOS already owns the orchestration stack
- deterministic typed lookup beats RAG for canonical HLK data
- a second control plane weakens SSOT and DI

### 6.2 Authorship / Transparency Obfuscation

Reject:

- \"undercover mode\" style authorship concealment

Why:

- conflicts with provenance, trust, and governed operator flows

### 6.3 Delight-Only Features

Reject for now:

- buddy/companion features
- cosmetic agent flourishes that do not improve governed answer quality

Why:

- operator trust, determinism, and correctness are more urgent

---

## 7. Implications for AKOS Built-ins

These objects should absorb the method improvements directly:

| Object | Practical implication |
|--------|-----------------------|
| `CapabilityMatrix` (`akos/policy.py`) | Tool intent must stay SSOT; avoid leaking gateway naming complexity into policy authoring |
| `ToolRegistry` (`akos/tools.py`) | Needs clearer mapping between logical names, gateway core IDs, and MCP plugin names |
| `_sync_tool_profiles_from_capability_matrix()` (`scripts/bootstrap.py`) | Should behave like a strict translator, not a best-effort mutator |
| `check_gateway_tool_config()` (`scripts/doctor.py`) | Should detect unknown or mismatched runtime tool IDs and surface parity drift |
| `AGENT_WORKSPACES` (`akos/io.py`) | Already 5-agent aware; continue treating workspaces as durable operator scaffolds |
| `HlkRegistry` (`akos/hlk.py`) | Remains deterministic and typed; no probabilistic replacement |

---

## 8. Implications for HLK Assets

### `docs/references/hlk/v3.0/`

- stays the active vault tree
- becomes more operationally important as MADEIRA improves
- new SOPs under role folders should be authored here, then registered via canonical compliance assets

### `docs/references/hlk/compliance/`

- becomes even more important because it is the canonical query truth
- any hallucination against these files is now a direct product failure
- future UAT must cross-check answers against these files explicitly

### `Research & Logic/` and `previous-project-for-product-owner-example-only/`

- remain reference-only
- useful for:
  - structure
  - tone
  - PO artifact patterns
  - historical input for future `hlk_doc_search`

but:

- they must not silently influence canonical operator answers unless surfaced through an explicit derived/search tool

---

## 9. Planned Future Enrichment Map (No Canonical Edits In This Phase)

This section maps **where** future enrichment should land once the runtime contract is fixed. It does **not** authorize canonical edits in this planning phase.

### 9.1 `docs/references/hlk/compliance/`

These are candidate future enrichment tracks for canonical governance assets:

- **`process_list.csv`**
  - Add or normalize process entries for:
    - runtime parity audit
    - browser/dashboard UAT
    - hallucination / trust-defect remediation
    - startup/session hygiene review
    - read-only escalation and handoff workflow
    - MCP tool exposure governance
  - From a broader Holistika perspective, these likely belong across:
    - **Tech / AI Engineer**
    - **Operations / PMO**
    - **People / Compliance**
    - **Data / Governance**
    - **Research** where provenance or source-evaluation loops are formalized

- **`PRECEDENCE.md`**
  - Clarify where new SOPs for runtime/operator behavior should live:
    - `v3.0/` as authored operational truth
    - mirrors/DB/indices as derived artifacts
  - Classify future derived search/index artifacts (for example a document-search index) explicitly as **mirrored / derived**, never canonical
  - Record how incident and remediation reports relate to canonical governance assets

- **`source_taxonomy.md`**
  - Potential future addendum if MADEIRA evolves into multi-source synthesis over documents:
    - how public/private/internal material should be classified when surfaced in answers
    - how reference-only research material can inform operator answers only through governed, provenance-aware flows

- **`baseline_organisation.csv`**
  - Only if role ownership needs formalization later for:
    - AI Engineer runtime stewardship
    - DevOPS runtime operations
    - PMO rollout/reporting ownership
    - Compliance ownership of answer-quality or provenance review

### 9.2 `docs/references/hlk/v3.0/`

These are candidate future enrichment tracks for the active vault tree:

- **`Envoy Tech Lab/MADEIRA/`**
  - operator-facing MADEIRA concept docs
  - runtime governance notes
  - GTM / positioning artifacts that are still useful internally
  - UAT and rollout references that should live with the product-facing surface

- **`Admin/O5-1/Tech/AI Engineer/`**
  - SOPs for agent orchestration, prompt contract maintenance, runtime capability stewardship, and answer-grounding policy

- **`Admin/O5-1/Operations/PMO/`**
  - SOPs for remediation tracking, phase reports, rollout decisions, and acceptance sign-off

- **`Admin/O5-1/People/Compliance/`** and/or **`Data/Governance/`**
  - SOPs for provenance review, policy enforcement, and canonical/mirrored conflict handling

- **`Admin/O5-1/Research/`**
  - research-to-answer methodology, evidence discipline, contradiction handling, and source-quality review for future document-search work

### 9.3 Use of Reference-Only Material

The reference-only trees remain valuable, but only as **input to future governed enrichment**, not as direct authoring surfaces:

- **`Research & Logic/`**
  - methodology and historical reasoning patterns
  - source material for future SOP drafting
  - useful for deriving operator procedures or search/index requirements

- **`previous-project-for-product-owner-example-only/`**
  - PRD / GTM / timeline / UX review formats
  - useful for structuring future MADEIRA product or rollout docs in `v3.0/`

### 9.4 Recommended Sequencing

1. Fix runtime contract and anti-fabrication first.
2. Capture the final operator workflow in `docs/uat` and reports.
3. Only then decide which operator/runtime behaviors deserve canonical expression in:
   - `process_list.csv`
   - `v3.0/` SOPs and role folders
   - `PRECEDENCE.md` clarifications

This keeps canonical truth downstream of proven runtime behavior, not speculative planning.

---

## 10. Immediate Practical Changes to the Madeira Remediation

The following should be considered mandatory in the Madeira remediation track:

1. **Contract freeze first**
   - resolve the read-only vs direct-write contradiction before touching runtime again

2. **Parity audit language**
   - add explicit parity framing to the runtime/report sections

3. **Anti-fabrication acceptance**
   - no fake names, fake UUIDs, fake workstreams, or tool-path leakage

4. **Startup hygiene**
   - fresh sessions must not expose startup-control text or `NO_REPLY`

5. **Canonical cross-check UAT**
   - dashboard answers must be verified against compliance CSVs, not just judged by tone

---

## 11. Deferred Follow-Ups

- Add `hlk_doc_search` as a lightweight MCP tool for markdown/SOP discovery
- Add runtime parity checks to `doctor.py`
- Add answer-quality telemetry and hallucination incident reporting
- Clarify SOP location precedence in `PRECEDENCE.md`

---

## 12. Final Practical Verdict

We should **improve our methods** with these sources, but selectively:

- **adopt** tool-contract explicitness, parity auditing, anti-fabrication, browser UAT, and planning governance
- **adapt** coordinator rigor, memory consolidation, and swarm-style review into AKOS-native patterns
- **reject** second orchestration layers, transparency-weakening behaviors, and non-essential delight features

That is the practical path that strengthens AKOS and MADEIRA without diluting the repo’s SSOT, DI, and HLK governance model.
