---
title: Derived Recall Discipline (RECALL lifecycle stage)
language: en
status: charter
canonical: true
role_owner: KM Officer
co_owner_role: System Owner
classification: way_of_working
intellectual_kind: discipline_charter
access_level: 4
authored: 2026-05-29
last_review: 2026-05-29
last_review_by: Founder
last_review_decision_id: D-IH-75-G
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-75-G
linked_canonicals:
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
---

# Derived Recall Discipline (charter)

> **Status: `charter`.** Low-priority Methodology craft per backlog item A4. The load-bearing
> retrieval infrastructure (Neo4j, MCP, search) remains **Tech-owned**; this canonical names
> Research/Methodology's *discipline* side of the RECALL join.

## 1. Purpose

**Derived recall** is the practice of retrieving knowledge by **deriving the question** from the
decision context — not by remembering file paths or folder names. The IntelligenceOps register,
Topic registry, and substrate landscape are **indexes**; the recall discipline teaches *how* to
compose a query that lands on the right fact for the moment of need.

## 2. The derived-recall principle (three rules)

1. **Start from the decision**, not the document. Name the audience, scenario, and confidence bar
   before opening the vault.
2. **Traverse registers, not directories.** FK-resolve `topic_id`, `register_id`, `source_id` from
   canonical CSVs; use graph/search surfaces as projections of those registers.
3. **Carry provenance on the way out.** Every recalled fact travels with source + confidence +
   access level — RECALL is not SHARE; do not skip PROTECT gates.

## 3. Split ownership (Research vs Tech)

| Layer | Owner | Examples |
|:---|:---|:---|
| **Discipline** (this charter) | Research / Methodology | Question derivation; register literacy; recall SOPs |
| **Infrastructure** | Tech Lab / System Owner | Neo4j projection; MCP servers; embedders; ERP/KB search |

Cross-area pointer: [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md).

## 4. Forward work (not blocking charter)

- Paired SOP when recall workflows multiply beyond ad-hoc operator practice.
- Validator only if recall artefacts become machine-auditable (e.g. mandatory `recall_brief` frontmatter).

## 5. Cross-references

- Lifecycle: [`RESEARCH_LIFECYCLE_DOCTRINE.md`](../../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md) §6.2
- Backlog A4: `research-rollout-backlog-2026-05-29.md`
