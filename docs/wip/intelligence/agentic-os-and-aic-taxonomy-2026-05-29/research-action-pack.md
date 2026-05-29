---
language: en
status: draft
intellectual_kind: research_action_pack
sharing_label: internal_only
audience: J-OP;J-AIC
role_owner: Research Director + KM Officer
authored: 2026-05-29
last_review: 2026-05-29
linked_sources:
  - source-ledger.csv
  - master-synthesis.md
  - aos-branding-forward-charter.md
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_ACTION_001.md
  - docs/wip/intelligence/README.md
---

# Agentic-OS + AIC taxonomy — research action pack

## 1. Why this pack exists

The operator asked, while routing models between a thinking seat and an execution
seat, for the **clear lines** between: the MADEIRA manifesto, the MADEIRA product,
a specific AIC instance, the substrate it runs on, an agentic operating system
(AOS), AKOS itself, and the wider field of non-AIC agentic workers (RPA, serverless
workers, Agent-as-a-Service, harness-as-a-service, text-only). This pack is the
**first ingest** of the standalone taxonomy research action the operator approved,
built under the research-to-decision discipline (the rulebook requiring a scored,
cross-checked source log before synthesis drives any governance edit).

It also answers a live operator question — *is AOS a category and AKOS a
subcategory?* — and explicitly **defers** the branding question (*should we claim
the AOS label*) to a dedicated reusable research, because this sweep was scoped to
taxonomy, not positioning.

## 2. Artifact inventory

| Artifact | Purpose | Status |
|:---|:---|:---|
| `source-ledger.csv` | 32 scored, cross-checked sources (7 prongs) | draft (validator PASS) |
| `master-synthesis.md` | Taxonomy + AOS category read + AKOS earned-label verdict + 8-lens analysis | draft |
| `aos-branding-forward-charter.md` | Deferred reusable branding research (the "own the AOS label?" question) | charter |
| `README.md` | Folder index | draft |

## 3. Operating-loop status (8 stages)

| Stage | Evidence |
|:---|:---|
| **Ingest** | 32 sources across 7 prongs (AOS-DEF, AOS-KERNEL, LINEAGE, MOAT, ENTITY-TAX, SKEPTIC, CORPINT) |
| **Rate** | Holistika reliability + external credibility + Safe/Euclid/Keter on every row; vendor sources scored down + paired with skeptics |
| **Rank** | Confidence mix 9 Safe / 16 Euclid / 7 Keter — honestly reflects a young, hyped field |
| **Synthesize** | `master-synthesis.md` — taxonomy + cross-checked category claims + earned-label test + 8 lenses |
| **Govern** | This pack + the AskQuestion gates that led here; no canonical-CSV edits yet (gated) |
| **Implement** | Deferred — taxonomy must be operator-ratified before AIC-registry expansion or any routing-directive mint |
| **Test** | `py scripts/validate_research_action.py --source-ledger ...` → PASS |
| **Iterate** | Next cycle: independent measured KB-compounding evidence; model the wider non-AIC entity classes; branding research |

## 4. The v3.1 lens (operator's request)

Read through Holistika's current methodology version (v3.1, the version the AIC
registry rows are reviewed at): the models/AOS field is evaluated not by vendor
benchmark but by **does it make the knowledge base compound, and is every action
governed + attributed?** Under that lens AKOS is a *KB-first operating system with
OS-grade governance* — passing the governance test the field is weakest on, not
claiming the kernel test it would fail. Full treatment in `master-synthesis.md` §3–§4.

## 5. Validator command

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/source-ledger.csv
```

## 6. Anti-patterns avoided

- **Research-as-ornament:** every prong ends in an operator-decidable line (taxonomy ratification, AIC-class expansion, branding research, routing-directive home).
- **Vendor hype laundering:** every vendor source paired with a skeptic; reliability scored down; the 3-test earned-label bar applied to our own claim.
- **Premature governance:** no canonical-CSV edits; AIC-registry expansion + routing-directive mint stay gated behind operator ratification of the taxonomy.
- **Folder ambiguity:** README + this pack name every artifact; reusable shape for the next "is X a category" question.

## 7. Reusability (the strength to lock in)

This research action is a **reusable engine**, not a one-off. The same shape —
KiRBe-style scored source ledger + multi-lens synthesis + earned-label test +
deferred-sub-question charter — can be re-pointed at any role / process / dimension
question Holistika faces. The operator's framing: *"a research can then be reused
or extended to answer questions from any role or process or any other dimension we
have — that's the strength."* This pack is the worked template for that.
