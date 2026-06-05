---
intellectual_kind: research_prong
prong: B
topic_cluster: external_maturity_models
authored: 2026-06-05
status: active
language: en
---

# Prong B — How industry ranks governance / data maturity

> External research-sweep (`SRC-AREA-EXT-01..23`). The question: when the field scores
> "is this domain governed well enough", what *shape* does the model take — and what does
> ours lack?

## B.1 Every mature model is multi-dimensional AND leveled — not a flat checklist

The dominant industry pattern is a **2-D grid**: *dimensions/components* × *maturity levels*.

- **DCAM** (`SRC-AREA-EXT-04`, `SRC-AREA-EXT-05`): 8 components → 34 capabilities → 101
  sub-capabilities, scored on a **6-level matrix against auditable evidence**.
- **CMMI** (`SRC-AREA-EXT-07`, `SRC-AREA-EXT-09`): 5 maturity levels (Initial → Managed →
  Defined → Quantitatively-Managed → Optimizing) or capability levels 0–5 (Incomplete →
  Optimizing). Crucially **continuous representation** lets you target *specific* process
  areas at *different* levels — exactly the per-area-tier idea.
- **IBM DG model** (`SRC-AREA-EXT-12`): 11 domains, each **scored individually** at its own
  level — "very few orgs reach L4/L5 at enterprise level; more common for specific domains."
- **Stanford** (`SRC-AREA-EXT-13`): 6 components × **3 dimensions** (people / policies /
  capabilities) → a component×dimension **matrix**, averaged.
- **DAMA-DMBOK** (`SRC-AREA-EXT-01`, `SRC-AREA-EXT-02`): 11 knowledge areas, governance at
  the hub — areas "implemented at different times depending on requirements" (i.e. **not all
  areas need the same depth at the same time**).

**Delta vs us:** our bar is **1-D and binary-ish** (present/partial/absent), no maturity
ladder. CMMI's "Incomplete" (L0) ≈ our `gap`; "Defined" (L3) ≈ our `pass`; but we have no
"Quantitatively-Managed/Optimizing" headroom — a `pass` is terminal. We collapse a 5-rung
ladder into a 1-rung gate.

## B.2 Maturity-model *design theory* gives us a quality bar for our own bar

Academic procedure models (Becker/Knackstedt/Pöppelbuß `SRC-AREA-EXT-14`; Pöppelbuß/Röglinger
`SRC-AREA-EXT-15`; Mettler `SRC-AREA-EXT-17`) converge on requirements our bar can be graded
against:

- **Intersubjective verifiability** (DP 2.1/2.2): criteria + assessment method must be
  precise enough that two assessors get the same verdict. *Our heuristic probe is
  deterministic — we pass this, and it is a genuine strength worth keeping.*
- **Multi-dimensional, possibly hierarchical** structure (R2): dimensions → sub-criteria.
  *Our 14 flat components are single-level; DCAM-style component→capability→sub nesting is
  the maturity path.*
- **Descriptive vs prescriptive** purpose: a good model not only *scores* (descriptive) but
  *tells you what to do to improve* (prescriptive). *Our gap tracker is prescriptive-ish;
  the bar itself is purely descriptive.*

## B.3 Governance standards: separate "governance" from "management"; principles over checklists

- **COBIT 2019** (`SRC-AREA-EXT-18`, `SRC-AREA-EXT-19`): 40 objectives across **5 domains**,
  one of which (EDM = Evaluate/Direct/Monitor) is *governance* and four are *management*.
  Plus **11 design factors** that **tailor** which objectives apply — explicit support for
  "not every area scores every component."
- **ISO/IEC 38500** (`SRC-AREA-EXT-21`, `SRC-AREA-EXT-22`): governance of IT = 6 principles +
  the **Evaluate-Direct-Monitor** cycle; applies "regardless of org size." Reinforces that a
  governance bar should be **principle-anchored**, and that governance ≠ management activity.

**Delta vs us:** our 14 components mix governance artifacts (charter, PRECEDENCE) with
management artifacts (process pairing, mirrors) on one flat list, with no
governance-vs-management separation and no tailoring factors.

## B.4 What Prong B establishes for the decision

- `def-components`: industry models are **2-D (component × level)** and often
  **hierarchical**; ours is 1-D flat. Strongest case for adding a **maturity-level** axis
  and/or **weights**.
- `def-threshold`: CMMI/IBM **score each area/domain at its own level** and expect different
  levels for different domains — direct support for **per-area or per-tier thresholds**
  rather than one global 88%.
- `def-area`: DMBOK/COBIT **tailor** which components apply — support for **conditional
  components** (Prong A already does this in sibling disciplines).
- **Keep:** our deterministic heuristic = "intersubjective verifiability," a property these
  academic models prize and many real assessments lack.
