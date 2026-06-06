---
initiative_id: INIT-OPENCLAW_AKOS-79
status: active
authored: 2026-05-15
last_review: 2026-05-15
owner_role: People Operations Manager
---

# I79 Risk Register

| ID | Risk | Likelihood | Impact | Owner | Mitigation | Close-out phase |
|:---|:---|:---:|:---:|:---|:---|:---:|
| **R-IH-79-1** | Manifesto drifts from operator's CPO frame (becomes generic / loses voice) | Med | High | People Operations Manager | Verbatim operator-quote capture in §"Operating story" of master-roadmap; manifesto draft cites operator's exact CPO language; P1 PAUSE allows operator AL5 review before commit | P1 |
| **R-IH-79-2** | Pattern library row content disagrees on which I59..I77 patterns count as "consulting design patterns" | Med | Med | People Operations Manager | P2 inline-ratify gate previews row list (8-12 candidates); operator selects + edits; charter-time decision deferred to per-phase ratification (`C-79-2`) | P2 |
| **R-IH-79-3** | Anti-jargon drift gate too strict — blocks legitimate token use in People canonicals | Med | Med | System Owner | Two-tier token list (forbidden + allowed) with allowed list explicitly enumerated in cursor rule + validator; Tech Lab canonicals exempt by file-path glob; INFO-level fallback at first deploy then promote to FAIL once tuned | P2-P3a |
| **R-IH-79-4** | Anti-jargon drift gate too lax — misses jargon variants (e.g. "embeddings" vs "embedder") | Med | Med | System Owner | Validator uses regex case-insensitive + word-boundary matching; tests cover plural / verb / noun variants; periodic operator review of drift-gate hits | P2-P7 |
| **R-IH-79-5** | Strand C three-part split fragments AI governance — readers can't find the right canonical | Med | High | People Operations Manager | Each canonical opens with "Where to look first" navigation block; Cursor rule §3 carries the routing table; Ethics canonical cross-references both People doctrine + Tech Lab landscape on first page | P3a-P3b |
| **R-IH-79-6** | Pattern library + process_list FK creates accidental adoption claim (process declares parent pattern it doesn't actually inherit from) | Med | Low | People Operations Manager | P6 PAUSE for operator review of seeded FKs (canonical CSV gate); validator FK-resolution check on every commit; inline-ratify per process row (`C-79-7`) | P6 |
| **R-IH-79-7** | Madeira role-class footnote phrasing assumed forward-compatibility but ages poorly when role-class population grows | Low | Med | PMO | Footnote points at I76 candidate + Tech Lab MADEIRA-AKOS STATUS.md; future I76 mint updates the footnote target without breaking semantics | I76 lifetime |
| **R-IH-79-8** | Cross-area breakthrough propagation SOP becomes ceremony — areas don't actually adopt patterns when minted | Med | Med | People Operations Manager | Paired runbook drafts the announcement; owner-area stub-acknowledges or rejects in comment thread; operator quarterly review of adoption surface (`SELECT COUNT(*) ... WHERE inherited_pattern_id`) | P4 + recurring |
| **R-IH-79-9** | Orphan inventory sweep misses doc trees (e.g., new tree spawned mid-initiative) | Low | Low | PMO | P5 covers explicit 7-tree list; future trees added via housekeeping cadence (D-IH-79-J case-by-case); periodic orphan re-scan in next People-area initiative | P5 + recurring |
| **R-IH-79-10** | Tech Lab canonical mint at P3b lacks System Owner review (no dedicated System Owner active currently) | High | Med | PMO + Founder | P3b runs as "PMO + Founder co-sign" until System Owner role activates; landscape canonical drafted as living-document with explicit `status: active_v1` + planned v2 review; not blocking | P3b + future System Owner promotion |
| **R-IH-79-11** | P5 orphan housekeeping accumulates large delete diff that destabilizes git history / unrelated initiative refs | Med | High | PMO | Per-cluster commits (one cluster = one atomic commit); deletes captured in `files-modified.csv` with `change_kind: deleted`; PR-style review window before each delete commit per D-IH-79-J case-by-case | P5 |
| **R-IH-79-12** | `process_list.csv` 8th col extension breaks downstream consumers (Pydantic SSOT, validator, Supabase mirror) | Med | High | PMO | Atomic schema-extension commit at P6 (column + Pydantic + validator + mirror DDL together); column nullable so existing rows pass; PAUSE for operator review of full diff before commit | P6 |
| **R-IH-79-13** | I79 closure backlog leaks into I76 / I75 / I77 / I78 (operator promised follow-ups but never executes) | Med | Med | PMO | Closure record at P8 enumerates carry-forward items with explicit owner_initiative target; INITIATIVE_DEPENDENCIES.md updated with cross-references; quarterly housekeeping review in next People-area initiative | P8 + recurring |
| **R-IH-79-14** | Pattern library Markdown narrative drifts from CSV (different content, contradictory descriptions) | Med | Med | People Operations Manager | Validator extension at P2 enforces `pattern_id` parity between CSV rows and MD section anchors; periodic re-review during I79 lifetime | P2 + recurring |
| **R-IH-79-15** | New Cursor rule conflicts with existing rules (e.g., disagreements on owner-area for AI governance) | Low | Med | PMO | Rule §"Cross-references" lists peer rules; explicit non-conflict statement: this rule extends, never overrides, the executable-process-catalog rule + brand-baseline-reality rule + Holistika operations rule | P0 |

## Mitigation cadence

- **Per-phase**: Each PAUSE-phase fires inline-ratify reviews that re-evaluate any open risks at that gate (P1 reviews R-1; P3a reviews R-5; P5 reviews R-9 + R-11; P6 reviews R-6 + R-12).
- **Closure (P8)**: Closure pause record per `akos-agent-checkpoint-discipline.mdc` reviews every risk row. Closed risks marked; unclosed risks moved to follow-on initiative or registered as recurring.
- **Recurring**: R-7, R-8, R-9, R-13 are explicitly recurring beyond I79 lifetime; tracked at next People-area initiative or quarterly operator review cadence.
