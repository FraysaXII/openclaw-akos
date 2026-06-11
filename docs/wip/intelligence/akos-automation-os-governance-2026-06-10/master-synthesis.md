---
intellectual_kind: research_master_synthesis
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: draft
language: en
control_confidence_level: Euclid
source_ledger: ./source-ledger.csv
source_count: 949
note: D4 draft — operator ratification pending before holistic-agentic R4 resumes
---

# AKOS Automation OS — master synthesis (draft)

> **Purpose:** Close the twelve-tranche research action (`IO-CAP-AKOS-AUTOMATION-OS-2026-001`)
> with a governed answer to the charter question: *what Automation OS contracts must AKOS adopt
> so every runbook is discoverable, paired-SOP compliant, intent-ranked, and CI-gated — eliminating
> one-off tranche scripts without losing ledger integrity during GTM research pile-up and ops peaks?*
>
> **Evidence base:** **949 sources** in [`source-ledger.csv`](./source-ledger.csv) (399 CORPINT /
> 550 OSINT across R1–R12; `validate_research_action.py` PASS). Implementation detail lives in
> [`implementation-spec-2026-06-11.md`](./implementation-spec-2026-06-11.md) — **operator ratification
> required** before vault CSV mint or holistic-agentic R4.

---

## 1. Diagnosis — the one-off script failure class is fleet-scale

Twelve tranches confirm the same failure modes named in the charter §1:

| Failure mode | What the ledger proved | ICS |
|:---|:---|:---|
| One-off ledger scripts | Every tranche minted `gen_r*_manifest.py` / `holistic_agentic_r*_ledger_*` instead of one engine | **Load-bearing** |
| Schema SSOT without engine | `akos/hlk_research_action.py` frozen; no unified `research_ledger.py` owner | **Load-bearing** |
| Registry gap | No `TECH_AUTOMATION_REGISTRY.csv` — scripts invisible to area owners | **Load-bearing** |
| Verify-profile drift | New scripts land without `verification-profiles.json` step | **Load-bearing** |
| Paired-SOP violation | Tranche append scripts lack human-readable twins | **High** |
| Adapter silos | CRM/RPA/RevOps registries exist but no automation crosswalk | **High** |

Holistic-agentic owns **orchestration** (handoffs, substrates, MADEIRA primitives). This pack owns
**automation plumbing** beneath it. Q12 Option A binding: holistic-agentic stays **PAUSED at R3**
until D4 ratifies.

---

## 2. Answer — three contracts (registry + engine + verify wiring)

### 2.1 `TECH_AUTOMATION_REGISTRY.csv` (D5)

A vault canonical inventory of every governed `scripts/*.py` runbook across O5-1 areas:

- Stable `script_id`, repo path, paired SOP, `process_list` FK, cadence, adapter status, ICS tier
- `verify_profile_step` FK into `verification-profiles.json`
- `replaces_one_off` semicolon-list for D7 migration traceability
- `linked_adapter_id` FK when script touches CRM/RPA/RevOps surface

Column spec preview: charter §8 D5. Full mint requires **operator CSV gate**.

### 2.2 `research_ledger.py` unified engine (D6)

Single runbook replacing `*_ledger_bootstrap.py` / `*_ledger_append.py`:

| Subcommand | Replaces |
|:---|:---|
| `bootstrap` | Per-pack seed (`holistic_agentic_r1_*`, `i94_p4_*`, …) |
| `append` | Per-tranche manifest append (`gen_r*_manifest.py` one-offs) |
| `validate` | Wrapper → `validate_research_action.py --source-ledger` |
| `migrate` | D7 one-off retirement |
| `radar-hook` | INTELLIGENCEOPS staleness hints for pack folder |

Chassis: extend `akos/hlk_research_action.py`; tests: `tests/test_research_ledger.py`; profile:
`research_ledger_self_test` in `pre_commit`.

### 2.3 Verify-profile wiring (D8)

Every Load-bearing / High ICS script gets a named step in `verification-profiles.json` and
release-gate registration. R10 harvest mapped the existing golden path (`verify.py pre_commit_fast`
/ `pre_commit`); D8 extends that contract to ledger ops + area validators discovered in R1–R11.

---

## 3. Prong synthesis rollup (R1–R12)

| Prong | Area | Key finding |
|:---|:---|:---|
| P1-TECH | System Owner | CICD baseline + verify profiles are the worked Automation OS for CI |
| P2-VERIFY | Tech | Profile step id is the FK `TECH_AUTOMATION_REGISTRY` needs |
| P3-ENVOY | Envoy Tech Lab | MCP topology + MADEIRA tool catalog = agent-side adapter layer |
| P4-RESEARCH | Research | Prong lattice + radar discipline govern ingest, not append scripts |
| P5-PEOPLE | People | QF specialties + regression runbooks already paired — registry rows missing |
| P6-COMPLIANCE | Compliance | PRECEDENCE + process_list are the mint gate for any registry CSV |
| P7-FINOPS | Finance | FINOPS registers + mirror spine = finance automation crosswalk |
| P8-LEGAL | Legal | Trademark/naming SOP gates public automation surfaces |
| P9-MARKETING | Marketing | Brand dual-register + CRM adapters = GTM automation boundary |
| P10-INTEL-OPS | Intelligence | INTELLIGENCEOPS row still draft — operator gate |
| P11-AGENT-CLI | Envoy | Agent CLI / monorepo patterns = execution seat plumbing |
| P12-RPA-ADAPTERS | Data/Ops | Adapter registries need FK from automation registry |

Per-prong detail: forward-charter as `prong-p*.md` tranche (D3) — not blocking D4 ratification.

---

## 4. Migration posture (D7 preview)

| One-off class | Count (approx) | Action |
|:---|---:|:---|
| `holistic_agentic_r*_ledger_*` | 3 | Fold to `research_ledger.py bootstrap/append` |
| `i94_*` / `i93_*` ops sweep | 4+ | Registry row + deprecate or merge |
| `gen_r*_manifest.py` (this pack) | 12 | Retire post-D4; manifests become engine input |
| Area validators (`validate_*`) | 40+ | Registry row; already in release-gate |

305-row holistic-agentic ledger may commit independently; R4+ must use engine only.

---

## 5. What unblocks on D4 ratification

| Blocked work | Unblocks when |
|:---|:---|
| Holistic-agentic R4–R12 | Operator ratifies `implementation-spec-2026-06-11.md` |
| `TECH_AUTOMATION_REGISTRY.csv` vault mint | D4 + operator CSV gate |
| One-off script retirement | D7 executed post-D4 |
| INTELLIGENCEOPS_REGISTER append | Separate operator gate (appendix §A) |

---

## 6. Cross-references

- Charter: [`RESEARCH_CHARTER_AND_EXECUTION_PLAN.md`](./RESEARCH_CHARTER_AND_EXECUTION_PLAN.md)
- Implementation spec (D4): [`implementation-spec-2026-06-11.md`](./implementation-spec-2026-06-11.md)
- Methodology wiring: [`methodology-cross-area-wiring-2026-06-10.md`](./methodology-cross-area-wiring-2026-06-10.md)
- Holistic-agentic (PAUSED): [`../holistic-agentic-capability-orchestration-2026-06-10/`](../holistic-agentic-capability-orchestration-2026-06-10/)
- Executable process catalog rule: `.cursor/rules/akos-executable-process-catalog.mdc`
