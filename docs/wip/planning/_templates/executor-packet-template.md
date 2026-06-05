---
template_kind: executor_packet
version: 1.0
authored: 2026-06-05
worked_example: docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-executor-packet-f1-2026-06-05.md
pairs_with:
  - docs/guides/cursor-two-seat-routing.md
  - .cursor/agents/executor.md
  - akos-synthesis-before-tranche.mdc
---

# Executor packet template — Composer execution seat

> **When to use.** Any initiative phase where the **thinking seat** has finished
> judgment and the **execution seat** (Composer 2.5) must land a bounded tranche
> without re-deriving scope. Copy this file to
> `docs/wip/planning/<NN-initiative>/reports/<phase>-executor-packet-<YYYY-MM-DD>.md`
> and fill every section. Pair with a one-page **tranche charter** for
> `synthesis_before_tranche_check.py`.

## Packet header (YAML frontmatter)

```yaml
packet_id: <INIT>-<PHASE>-<YYYY-MM-DD>
initiative_id: INIT-OPENCLAW_AKOS-NN
phase: <P# or F#>
seat: execution
model_pin: composer-2.5
tranche_class: internal_governance | canonical_csv_mint | specialty_mint
operator_gates: [<csv files requiring approval>]
prerequisites: [<prior packets / decisions>]
supersedes: [<stale reports>]
```

## 0. F0 / ratification assumptions (if thinking seat deferred AskQuestion)

| Decision | Locked value | Escalate if |
|:---|:---|:---|
| … | … | Composer sees conflict with vault |

## 1. Mission (one paragraph)

What this packet accomplishes in plain language + what it explicitly does **not** do.

## 2. In scope / out of scope

| In | Out |
|:---|:---|
| … | … |

## 3. Files to create / edit (ordered)

| # | Action | Path | Spec pointer |
|:---:|:---|:---|:---|
| 1 | CREATE | … | §4.x |

## 4. Canonical specs (copy-paste quality bar)

### 4.1 …

Section-by-section requirements, frontmatter keys, cross-refs, evidence base minimums.

## 5. Canonical CSV rows (exact)

Paste-ready CSV lines or column-by-column table. **Stop** if operator gate not cleared.

## 6. Verification matrix (must all PASS)

```powershell
# ordered commands + expected outcome
```

## 7. Acceptance criteria (falsifiable)

- [ ] …
- [ ] Matrix row: `<Area>` ≥ N% with gaps AREA-XX cleared

## 8. Stop conditions → `=== COMPOSER BLOCKED -> SWITCH TO OPUS ===`

| Condition | Action |
|:---|:---|
| Validator FAIL after one fix attempt | Stop + paste finding codes |
| Ambiguous doctrine / missing gate | Stop + list options |
| Scope creep (file not in §3) | Stop |

## 9. Commit discipline

- **One commit** per packet: `feat(<initiative>-<phase>): <plain-language summary>`
- Attach matrix excerpt to `reports/<phase>-execution-evidence-<date>.md` (optional, 20 lines max)

## 10. Handoff markers

```text
=== OPUS DONE -> SWITCH TO COMPOSER ===
(paste §0–§10 of this packet into Composer thread)

=== COMPOSER BLOCKED -> SWITCH TO OPUS ===
(executor emits when stopping)

=== COMPOSER DONE — operator review ===
(executor emits after commit + validators)
```

## 11. Next packet pointer

Link to F(n+1) executor packet path (stub OK until authored).
