---
report_type: hygiene-research
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L5-hygiene
authored: 2026-06-09
authored_by: Thinking seat (Opus) → execution seat mint
ratifying_decisions:
  - D-IH-95-J
verdict: B-complete_C-research
---

# I95 Hygiene — B→C research (2026-06-09)

**Operator intent:** B then C — re-scan vault for 74th CSV, then charter amend + CS strict audit/fix. **Research + brainstorm first** for Hygiene C.

---

## Hygiene B — Re-scan verdict (73 vs 74)

| Source | Count | Notes |
|:---|:---:|:---|
| Charter prose ([`universal-canonical-governance-charter-2026-06-09.md`](universal-canonical-governance-charter-2026-06-09.md)) | **74** | Planning estimate |
| GOV-1 filesystem inventory ([`synthesis-p95-gov-1-2026-06-09.md`](synthesis-p95-gov-1-2026-06-09.md)) | **73** | SSOT at mint |
| [`CANONICAL_GOVERNANCE_REGISTRY.csv`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CANONICAL_GOVERNANCE_REGISTRY.csv) rows | **73** | 1:1 with inventory |
| Glob `v3.0/**/canonicals/**/*.csv` | **77 paths** | ~4 are duplicate path representations (Windows `\` vs `/`); **not** 4 extra assets |

### Verdict

**73 is SSOT.** There is **no mysterious 74th data CSV** to hunt. The charter's "74" is stale prose (likely counted `CANONICAL_GOVERNANCE_REGISTRY.csv` as the extra asset, but that meta-registry is **not self-indexed** in its own registry).

### Hygiene B action

Amend charter §1/§2 from 74 → **73** + footnote (GOV-1 inventory @ 2026-06-09). Optional: add self-row for governance registry as **74th governance row**, not a new vault CSV.

---

## Hygiene C — `validate_collaborator_share.py --strict`

Per GOV-6 synthesis + GOV-8 UAT: **`validate_hlk.py` OVERALL PASS** with `--strict` armed at **2026-06-09 closure** — **no active CS-04/CS-06 failures** at that snapshot.

| Finding code | Meaning |
|:---|:---|
| **CS-04** | Default-split audit (65/35 composition vs pattern) |
| **CS-06** | Billed rate within market band |

**Mechanical gate is armed** (D-IH-95-J); **commercial accuracy debt** (operator scratchpad / intent-ranked IT-3) is a **separate Hygiene C research** track — settlement tranche refreshing all 5 share CSVs, not a revert of `--strict`.

### Fresh evidence command (execution time)

```powershell
py scripts/validate_collaborator_share.py --strict
py scripts/validate_hlk.py
```

---

## Hygiene C — Research / brainstorm outline

**Scope options (AskQuestion Q4):**

| Option | Scope | Risk |
|:---|:---|:---|
| **A (recommended)** | Research + brainstorm only — accuracy audit charter + OPS rows; no share CSV edits this round | Low |
| **B** | Strict re-run + fix any CS-04/06 findings row-by-row in canonical CSVs | Medium — canonical-CSV gate |
| **C** | Full settlement tranche — refresh all 5 share registers to match live engagements | High — pairs with I86 CS discipline |

### Research tracks (brainstorm inputs)

1. **Engagement coverage map** — which live engagements lack matching share-register rows?
2. **Pattern vs reality drift** — 65/35 composition vs actual bill modes per engagement.
3. **Market-rate band audit** — CS-06 posture when engagements use non-standard rates.
4. **Settlement tranche charter** — if operator picks option C, scope all 5 registers + operator gate per row class.

### Deferred-work posture (option A)

- Keep `--strict` armed in `validate_hlk.py` umbrella.
- Track commercial accuracy as **OPS/deferred-work** until settlement tranche.
- Do **not** revert D-IH-95-J INFO→FAIL ramp.

---

## Cross-references

- Universal governance charter: [`universal-canonical-governance-charter-2026-06-09.md`](universal-canonical-governance-charter-2026-06-09.md)
- GOV-1 synthesis: [`synthesis-p95-gov-1-2026-06-09.md`](synthesis-p95-gov-1-2026-06-09.md)
- Operator ratification: [`i95-round2-operator-ratification-2026-06-09.md`](i95-round2-operator-ratification-2026-06-09.md)
- Collaborator-share discipline: `.cursor/rules/akos-collaborator-share.mdc`
