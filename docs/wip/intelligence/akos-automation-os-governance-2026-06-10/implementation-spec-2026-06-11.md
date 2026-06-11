---
intellectual_kind: implementation_spec
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: draft-pending-operator-ratification
language: en
control_confidence_level: Euclid
linked_decisions:
  - D-IH-94-A
gate_type: inline-ratify
blocks_downstream:
  - holistic-agentic R4-R12
  - TECH_AUTOMATION_REGISTRY.csv mint
---

# Automation OS — implementation spec (D4 draft for operator ratification)

> **Functional name:** The governed implementation plan that turns the Automation OS research
> (949-row ledger, R1–R12) into three shippable contracts: a multi-area script registry, a unified
> research-ledger engine, and verification-profile wiring.
>
> **Ratification gate:** Operator must approve this spec before holistic-agentic R4 resumes or
> `TECH_AUTOMATION_REGISTRY.csv` mints in vault. Status: **draft** — not yet binding.

---

## 1. Scope

### In scope (D4 ratification authorizes)

1. Mint `scripts/research_ledger.py` with subcommands in §3
2. Mint `tests/test_research_ledger.py` + `research_ledger_self_test` verification profile step
3. Draft `TECH_AUTOMATION_REGISTRY.csv` column spec → operator CSV tranche (separate commit)
4. Wire top-20 Load-bearing scripts into registry preview rows (WIP CSV under pack folder until vault gate)
5. Document D7 migration plan for named one-offs (no deletion in D4 commit)

### Out of scope (forward-charter)

- Holistic-agentic orchestration hooks / token attribution (holistic-agentic charter owns)
- INTELLIGENCEOPS_REGISTER CSV append (separate operator gate)
- Retiring one-off scripts (D7 post-implementation)
- Per-prong synthesis files `prong-p*.md` (D3 advisory)

---

## 2. Deliverable A — `TECH_AUTOMATION_REGISTRY.csv`

**Path (post-gate):** `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/TECH_AUTOMATION_REGISTRY.csv`

**Pydantic chassis:** `akos/hlk_tech_automation_registry_csv.py` (new module)

**Validator:** `scripts/validate_tech_automation_registry.py` → umbrella `validate_hlk.py`

### Column schema (binding preview)

| Column | Type | Purpose |
|:---|:---|:---|
| `script_id` | slug | Stable id (`runbook_research_ledger_validate`) |
| `script_path` | path | Repo-relative `scripts/…` |
| `paired_sop_path` | path | Human-readable twin (executable process catalog Rule 1) |
| `process_list_item_id` | FK | `process_list.csv` row when governed |
| `cadence` | enum | `on_demand` / `scheduled` / `event_triggered` / `gated_operator` |
| `adapter_status` | enum | `active` / `deprecated` / `one_off_retire` / `planned` |
| `verify_profile_step` | string | Step id in `verification-profiles.json` |
| `ics_tier` | enum | Load-bearing / High / Medium / Corroboration |
| `holistika_area` | enum | O5-1 area code |
| `replaces_one_off` | semicolon-list | Retired script paths (D7 traceability) |
| `linked_adapter_id` | FK | RPA/CRM/RevOps adapter when applicable |
| `role_owner` | string | From `baseline_organisation.csv` |
| `notes` | string | Impact / automation contract |

### Seed rows (Load-bearing — implement in D4 tranche)

| script_id | script_path | ics_tier | verify_profile_step |
|:---|:---|:---|:---|
| `runbook_research_ledger` | `scripts/research_ledger.py` | Load-bearing | `research_ledger_self_test` |
| `runbook_validate_research_action` | `scripts/validate_research_action.py` | Load-bearing | (release-gate always-on) |
| `runbook_verify` | `scripts/verify.py` | Load-bearing | `pre_commit_fast` |
| `runbook_release_gate` | `scripts/release-gate.py` | Load-bearing | `release_gate` |
| `runbook_validate_hlk` | `scripts/validate_hlk.py` | Load-bearing | `validate_hlk` |

Full inventory: harvest from R1 script census + R10 verify matrix (949-row ledger CORPINT paths).

**Operator gate:** CSV mint requires explicit approval per `akos-baseline-governance.mdc` — inline-ratify row count + area coverage before commit.

---

## 3. Deliverable B — `research_ledger.py` engine

**Path:** `scripts/research_ledger.py`

**Chassis:** `akos/hlk_research_action.py` (`ResearchSourceRow`, `SOURCE_LEDGER_FIELDNAMES`)

### Subcommand contract

```powershell
# Bootstrap a pack ledger from charter + prong headers
py scripts/research_ledger.py bootstrap --pack akos-automation-os-governance-2026-06-10

# Append tranche rows from manifest JSON (idempotent on source_id)
py scripts/research_ledger.py append --pack akos-automation-os-governance-2026-06-10 --tranche R7

# Validate (wrapper)
py scripts/research_ledger.py validate --pack akos-automation-os-governance-2026-06-10

# Migrate paths / retire one-offs (D7)
py scripts/research_ledger.py migrate --plan migration-plan-holistic-agentic-r1-r3-2026-06-11.md

# Radar staleness hook
py scripts/research_ledger.py radar-hook --pack akos-automation-os-governance-2026-06-10
```

### Behavioural requirements

1. **Idempotent append** — re-run on same manifest produces zero duplicate `source_id` rows
2. **Schema SSOT** — reads/writes via `ResearchSourceRow` Pydantic model only
3. **Validate delegation** — `validate` subcommand shells to `validate_research_action.py --source-ledger`
4. **Structured logging** — `akos.log.setup_logging`; no secret values in logs
5. **Cross-platform** — `pathlib.Path`; `akos.process.run` for subprocess

### Paired SOP (Rule 1)

**Path:** `docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_LEDGER_OPS_001.md`

Pairs with `process_list` row `hol_resea_dtp_research_ledger_001` (net-new — operator gate with CSV tranche).

### Tests

**Path:** `tests/test_research_ledger.py`

- Valid bootstrap produces header + seed rows
- Append R7 manifest twice → row count unchanged
- Invalid manifest → Pydantic validation error
- `@pytest.mark.research_action` group registration in `scripts/test.py`

---

## 4. Deliverable C — verify profile wiring

**Primary files:**

- `config/verification-profiles.json` — add `research_ledger_self_test` step
- `scripts/release-gate.py` — register step (INFO ramp → FAIL after 3 clean research actions)
- `scripts/verify.py` — expose in `--list`

### Profile step spec

```json
{
  "id": "research_ledger_self_test",
  "command": ["py", "scripts/research_ledger.py", "validate", "--pack", "akos-automation-os-governance-2026-06-10"],
  "profiles": ["pre_commit_fast", "pre_commit"],
  "timeout_seconds": 120
}
```

### Wiring rule (binding)

Every `TECH_AUTOMATION_REGISTRY` row with `ics_tier` ∈ {Load-bearing, High} MUST have non-empty
`verify_profile_step` OR explicit `notes` explaining release-gate always-on exemption.

---

## 5. Implementation phases (post-ratification)

| Phase | Deliverable | Verification |
|:---|:---|:---|
| D4-P1 | `research_ledger.py` + tests + SOP draft | `py -m pytest tests/test_research_ledger.py -v` |
| D4-P2 | Verify profile step + release-gate wire | `py scripts/verify.py pre_commit_fast` |
| D4-P3 | WIP registry preview CSV (pack folder) | `validate_tech_automation_registry.py` (new) |
| D4-P4 | Operator CSV gate → vault mint | `validate_hlk.py` PASS |
| D4-P5 | D7 migration execute | One-off scripts marked `one_off_retire` |

---

## 6. Inline-ratify options (operator)

| Option | Meaning |
|:---|:---|
| **A (recommended)** | Ratify full spec §1–§5; authorize D4-P1..P2 in next execution tranche; defer vault CSV to D4-P4 gate |
| **B** | Ratify engine only (§3); defer registry CSV to separate initiative |
| **C** | Ratify with reduced seed rows (top-10 Load-bearing only) |
| **D** | Reject — return to Opus for scope revision |

---

## 7. Verification matrix (D4 acceptance)

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/akos-automation-os-governance-2026-06-10/source-ledger.csv
py scripts/validate_research_action.py --self-test
py -m pytest tests/test_research_ledger.py -v
py scripts/verify.py pre_commit_fast
py scripts/validate_hlk.py
```

---

## 8. Cross-references

- Master synthesis: [`master-synthesis.md`](./master-synthesis.md)
- Charter D5–D8 index: [`RESEARCH_CHARTER_AND_EXECUTION_PLAN.md`](./RESEARCH_CHARTER_AND_EXECUTION_PLAN.md) §8
- Methodology wiring R7–R12: [`methodology-cross-area-wiring-2026-06-10.md`](./methodology-cross-area-wiring-2026-06-10.md)
- Executable process catalog: `.cursor/rules/akos-executable-process-catalog.mdc`
