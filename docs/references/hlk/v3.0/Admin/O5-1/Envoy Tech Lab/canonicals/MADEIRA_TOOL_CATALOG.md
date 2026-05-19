---
intellectual_kind: canonical
sharing_label: internal_only
authored: 2026-05-19
last_review: 2026-05-19
owner_role: System Owner
co_owner_role: Founder
co_owner_role_2: PMO
authority: Founder + System Owner + PMO
status: active
language: en
linked_decisions:
  - D-IH-76-A         # I76 charter inception
  - D-IH-86-O         # Option 5 default posture
  - D-IH-76-B         # I17 per-deliverable triage (Option E)
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_MODE_PARITY.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_METHODOLOGY_MODE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md
linked_initiatives:
  - INIT-OPENCLAW_AKOS-76
paired_runbook:
  - scripts/validate_madeira_tool_rbac.py
paired_csv:
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_TOOL_RBAC.csv
---

# MADEIRA — Tool catalog and per-mode RBAC

> The human-readable companion to [`dimensions/MADEIRA_TOOL_RBAC.csv`](./dimensions/MADEIRA_TOOL_RBAC.csv). Defines the **tool categories** Madeira (current AI O5-1) can call, classifies each category against the [`MADEIRA_MODE_PARITY.md`](./MADEIRA_MODE_PARITY.md) §6 RBAC posture taxonomy, and operationalises the per-mode RBAC matrix as a canonical CSV that the runtime enforces and the operator can review at every commit.

## 1. Purpose + scope

The 5-mode taxonomy in `MADEIRA_MODE_PARITY.md` declares **postures** (read / read+plan-write / full / read+observability / methodology-checkpoint). This canonical takes each posture and binds it to a **concrete tool category list** so the per-mode runtime can evaluate "is this tool call allowed in this mode?" deterministically.

**In scope:** the tool category enum + per-mode permission matrix + provenance + lifecycle status. **Out of scope:** per-tool detailed RBAC (the categories are the granularity); MCP-server-level access lists (forward — I76 P4 AICs dispatcher uses categories, not server lists); operator personal preferences (forward — I76 P3 personality SOP).

The CSV is the SSOT for the matrix; this markdown is the narrative companion (per the paired-file pattern — `pattern_register_dimension` from [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../../People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv)).

## 2. The 16-category seed

The initial seed registers 16 tool categories that cover the Madeira tool surface as of 2026-05-19. Categories are grouped by **posture family** below; full per-row detail lives in the CSV.

### 2.1 Universal read categories (allowed in all 5 modes)

- `tool_read_codebase` — Read, Glob, Grep, SemanticSearch, ReadLints.
- `tool_read_external` — WebFetch, WebSearch.
- `tool_mcp_observability_readonly` — Sentry / Cloudflare Observability / Render monitoring / browser snapshot read paths.
- `tool_mcp_external_world_read` — Figma read / Stripe read / docs MCPs / GitHub read.

These are the universal substrate. Every mode (including the most-restrictive Ask) can call them because none of them mutate any state — repo, world, or remote.

### 2.2 Planning-scoped categories (Plan + Agent + conditional in Methodology)

- `tool_write_planning` — Write/StrReplace/EditNotebook scoped to `docs/wip/planning/**` only.

Plan mode owns this category by design (the plan markdown is the persistence vehicle). Agent mode inherits it as part of the `full` posture. Methodology mode is `conditional` — it may write only to methodology-tracking files (LOGIC_CHANGE_LOG drafts, operator-scratchpad, decision-row drafts, principle log) per the `conditional_constraint`.

### 2.3 Operator-dialog category (Plan + Agent + Methodology)

- `tool_operator_dialog` — AskQuestion (structured inline-ratify per [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc)).

Three modes need AskQuestion: Plan (plan-ratify gates), Agent (inline-ratify per-phase), Methodology (methodology-candidate ratify). Ask mode is read-only research and does not need to surface ratify gates. Debug mode escalates by **mode transition** (Debug → Agent for fixes), not by AskQuestion.

### 2.4 Agent-mode-only categories (full posture)

- `tool_write_canonical_code` — writes to `akos/**` / `scripts/**` / `tests/**` / `config/**` / `supabase/**` / `docs/references/**`. **Canonical-CSV sub-gate** applies per [`akos-governance-remediation.mdc`](../../../../../../.cursor/rules/akos-governance-remediation.mdc).
- `tool_delete_files` — Delete. Reversible via git checkout.
- `tool_shell_full` — git commit/push, npm install, build, deploy commands.
- `tool_subagent_delegation` — Task tool subagent spawning.
- `tool_image_generation` — GenerateImage (user-explicit-request-only).
- `tool_mcp_data_mutation` — Supabase apply_migration / mutating execute_sql. Data-plane gate per [`akos-holistika-operations.mdc`](../../../../../../.cursor/rules/akos-holistika-operations.mdc) operator SQL gate.

These six categories are gated to Agent mode because they mutate persistent state. Plan / Ask / Debug / Methodology cannot invoke them. Operator approvals stack on top via the canonical-CSV gate and the holistika-operations SQL gate.

### 2.5 Debug-mode additions (read+observability posture)

- `tool_shell_read_only` — git log/diff/status/blame, `py scripts/validate_*.py`, pytest, ls-equivalent.

Allowed in Agent and Debug modes. Debug mode's *primary* execution surface (Debug-mode shells are intentionally read-only; fixing requires Debug → Agent transition).

### 2.6 Methodology-mode primary surfaces

- `tool_write_methodology` — Write to LOGIC_CHANGE_LOG / DECISION_REGISTER drafts / operator-scratchpad / principle log. Methodology mode's persistent-across-sessions vehicle.
- `tool_brand_voice_check` — `scripts/validate_brand_voice_register.py` + `scripts/validate_brand_baseline_reality_drift.py` + manual BBR matrix lookup. **Mandatory** in Methodology mode (per [`MADEIRA_METHODOLOGY_MODE.md`](./MADEIRA_METHODOLOGY_MODE.md) §2.3). Conditional in Plan and Agent modes when authoring external-audience prose.

### 2.7 External-world mutation (Agent-mode + conditional)

- `tool_mcp_external_world_mutation` — Slack send / Resend email / Stripe write / Figma write. **Conditional** in Agent mode (the only mode that can call it at all). Conditional constraint requires: (a) operator-ratified send list, (b) BBR external-register check per [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc), (c) render-trail per [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc) when audience is external.

This is the highest-risk category. The triple-gate (operator + brand + render) protects against silent external-world side effects.

## 3. Per-mode summary matrix

| Mode | Read | Plan-write | Canonical-code-write | Methodology-write | Shell read-only | Shell full | Subagent | Operator dialog | Image gen | Data mutate | Ext-world mutate | BBR check |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Ask** | yes | no | no | no | no | no | no | no | no | no | no | no |
| **Plan** | yes | yes | no | no | no | no | no | yes | no | no | no | conditional |
| **Agent** | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | conditional | conditional |
| **Debug** | yes | no | no | conditional | yes | no | no | no | no | no | no | no |
| **Methodology** | yes | conditional | no | yes | no | no | no | yes | no | no | no | **yes (mandatory)** |

(Simplified view; full per-category detail with conditional_constraint text lives in the CSV.)

## 4. Conditional constraint examples (worked)

The `conditional` permission value is the discriminating semantic — it says "allowed, but only under these named conditions." The CSV's `conditional_constraint` column carries the constraint text; the validator enforces the constraint must be non-empty when any per-mode cell is `conditional` AND must be empty when no cell is.

Three worked examples from the seed:

- **`tool_write_planning` in Methodology mode = conditional.** Constraint: "Methodology mode may write only to methodology-tracking files (LOGIC_CHANGE_LOG drafts; operator-scratchpad; decision-row drafts; principle log)." This prevents Methodology mode from authoring full plan documents (that's Plan-mode work) while preserving Methodology's ability to capture methodology candidates persistently.
- **`tool_mcp_external_world_mutation` in Agent mode = conditional.** Constraint: triple-gate listed in §2.7 above. The conditional value is intentionally narrow — the operator must opt in per invocation, not blanket-allow at session start.
- **`tool_brand_voice_check` in Plan/Agent = conditional.** Constraint: "Plan and Agent modes must invoke when authoring external-audience prose (any audience tag in J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO); skip when audience is J-OP only." This pairs the per-mode RBAC matrix with the [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc) audience taxonomy without duplicating the audience enum here.

## 5. Provenance taxonomy

Each row's `provenance` column traces where the tool surface comes from:

- **`cursor-native`** — built into Cursor IDE (Read, Write, StrReplace, Glob, Grep, SemanticSearch, AskQuestion, Task, GenerateImage, Delete).
- **`shell`** — OS shell exec (Shell tool with `git`, `py`, `npm`, `pytest`, etc.).
- **`mcp-server`** — MCP protocol server (cursor-ide-browser, plugin-supabase, plugin-cloudflare-*, plugin-vercel, etc.).
- **`agent-skill`** — `.cursor/skills/<name>/SKILL.md` invocation.
- **`scripts-runbook`** — `scripts/<name>.py` invocation per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1.

The seed has 13 `cursor-native` + 2 `mcp-server` + 1 `shell` + 1 `scripts-runbook` + 0 `agent-skill` rows. Agent-skill rows will mint when I76 P3 personality SOPs land + a per-skill RBAC posture is needed.

## 6. Cadence + maintenance

- **Cadence:** `event_triggered` — review when a new tool surface appears (new MCP server installed; new Cursor tool released; new skill authored) OR when an existing tool's RBAC posture needs to shift (e.g., a previously-mutating tool is wrapped in a safer read-only adapter).
- **Owner:** System Owner. Co-owners: Founder + PMO.
- **Review default:** quarterly baseline + ad-hoc per event.
- **Maintenance procedure:** edit the CSV directly (canonical-CSV gate applies — operator approval required); update this markdown's §2 narrative to reflect new categories or removed ones; commit both files in the same operator-gated commit.
- **Drift gate:** `py scripts/validate_madeira_tool_rbac.py` (paired runbook). Wires into [`config/verification-profiles.json`](../../../../../../config/verification-profiles.json) `pre_commit` profile + [`scripts/release-gate.py`](../../../../../../scripts/release-gate.py) per CONTRIBUTING.md.

## 7. RBAC posture taxonomy (cross-reference)

Per [`MADEIRA_MODE_PARITY.md`](./MADEIRA_MODE_PARITY.md) §6, the 5 postures map to specific tool category sets per the table in §3 above. The validator does not re-encode the posture-to-category mapping (the SOP is the SSOT for that); it enforces the per-row schema + uniqueness + FK-resolution + conditional-constraint semantics.

## 8. Cursor-rules adherence

This canonical operationalises:

- [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1 (paired SOP + executable runbook) — this canonical pairs with [`scripts/validate_madeira_tool_rbac.py`](../../../../../../scripts/validate_madeira_tool_rbac.py).
- [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 2 (adapter-status enum) — tool-category `status` column uses the same lifecycle enum (`active` / `experimental` / `deprecated` / `planned`).
- [`akos-holistika-operations.mdc`](../../../../../../.cursor/rules/akos-holistika-operations.mdc) "New git-canonical compliance registers (pattern)" — the CSV lives under a `dimensions/` subfolder; Pydantic SSOT; dedicated validator; PRECEDENCE.md entry; CI wiring.
- [`akos-governance-remediation.mdc`](../../../../../../.cursor/rules/akos-governance-remediation.mdc) "HLK compliance governance" — canonical-CSV gate (operator approval required for every mint + every revision).
- [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc) "CONTRIBUTING.md adherence callouts for new validators" — Pydantic in `akos/`, type hints, structured logging, `pathlib.Path`, tests, release-gate wiring.

## 9. Cross-references

- Parent initiative: [I76 MADEIRA elevation](../../../../wip/planning/76-madeira-elevation/master-roadmap.md)
- Mode taxonomy: [`MADEIRA_MODE_PARITY.md`](./MADEIRA_MODE_PARITY.md)
- Methodology deep spec: [`MADEIRA_METHODOLOGY_MODE.md`](./MADEIRA_METHODOLOGY_MODE.md)
- Paired runbook: [`scripts/validate_madeira_tool_rbac.py`](../../../../../../scripts/validate_madeira_tool_rbac.py)
- Pydantic SSOT: [`akos/hlk_madeira_tool_rbac.py`](../../../../../../akos/hlk_madeira_tool_rbac.py)
- Tech Lab framework landscape: [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](./AGENTIC_FRAMEWORK_LANDSCAPE.md)
- People agentic doctrine: [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md)
- BBR dual-register: [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc)
- External-render discipline: [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc)
- Forward — persistence SOP: [`SOP-TECH_MADEIRA_PERSISTENCE_001.md`](./SOP-TECH_MADEIRA_PERSISTENCE_001.md) (I76 P3 forward)
- Forward — personality SOP: [`SOP-TECH_MADEIRA_PERSONALITY_001.md`](./SOP-TECH_MADEIRA_PERSONALITY_001.md) (I76 P3 forward)
- Forward — AICs F5 dispatcher: [`MADEIRA_AIC_PER_TASK_REGISTRY.csv`](./dimensions/MADEIRA_AIC_PER_TASK_REGISTRY.csv) (I76 P4 forward; consumes this catalog)
