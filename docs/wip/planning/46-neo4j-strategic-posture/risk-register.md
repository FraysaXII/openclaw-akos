---
language: en
status: active
initiative: 46-neo4j-strategic-posture
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 46 — Risk Register

## Active risks

### R-46-1 — GraphRAG PoC indexing cost overruns the operator's budget (H / M)
**Trigger:** P3 indexes ~1000 process rows + ~65 roles + ~30 dimensions via LLM-driven entity extraction. Even at LightRAG's $0.50 / 500-page corpus, our scale could land $1-5 per re-index. Multiple re-indexes during PoC tuning could compound.

**Mitigation:**
- P0 sets a hard cost ceiling (`GRAPHRAG_POC_USD_CEILING`, default $20) enforced by `scripts/graphrag_poc.py --max-spend`.
- PoC uses Ollama-local embeddings where possible (zero marginal cost) for the embedding side; LLM is only used for entity extraction (the 58%-of-tokens slice per Microsoft cost piece).
- Single re-index per PoC iteration; tuning happens on cached extracted entities.
- Operator must explicitly opt in (`AKOS_GRAPHRAG_POC_LIVE=1`) before live LLM calls.

**Rollback:** N/A (cost is unrecoverable; the ceiling prevents catastrophe).

### R-46-2 — GraphRAG hallucinations leak into MADEIRA answers (H / M)
**Trigger:** GraphRAG retrieves an unrelated subgraph; LLM hallucinates a connection between entities; MADEIRA presents it as a grounded fact.

**Mitigation:**
- Hybrid retrieval (graph + vector) cross-checks; D-IH-46-A defaults to LightRAG-style hybrid for this reason.
- Golden query regression in P3 covers the 20 highest-impact MADEIRA query shapes.
- Grounded-citation requirement in MADEIRA_BASE.md (already enforced) — every claim must cite a vault path.
- I45 P5 adversarial cassette (PII / brand-jargon / prompt-injection) extended in I46 P6 with "graph-escape probe": queries that should resolve via direct CSV must NOT escape into GraphRAG.

**Rollback:** Set SKILL_REGISTRY row's `retrieval_mode=vector_only`; GraphRAG path is bypassed.

### R-46-3 — Vendor lock-in to Neo4j Aura at Holistika scale (M / L)
**Trigger:** As Holistika grows, Aura pricing tiers don't scale economically; we want to migrate to self-hosted Neo4j or even a different graph DB.

**Mitigation:**
- P1 doctrine explicitly addresses portability: HLK CSV vault remains SSOT; Neo4j is rebuildable projection.
- `neo4j-graphrag-python` is provider-agnostic on the LLM side (D-IH-46-A); the Neo4j side is locked but the library abstracts query construction (Cypher) which is portable to other graph stores with similar Cypher dialects.
- Doctrine documents the "scale trigger" for Aura → self-hosted migration (~10× current data volume).

**Rollback:** Re-run sync against new Neo4j endpoint; CSVs unchanged.

### R-46-4 — Agent memory built half-way then abandoned (H / L)
**Trigger:** A future operator interpretation of the I46 P4 ADR triggers building Zep-like temporal layer; mid-build the trigger fades; we ship a half-built memory system that costs maintenance.

**Mitigation:**
- D-IH-46-B is "defer until trigger" — codified, not vibes. P4 ADR explicitly names 3 candidate triggers; operator picks ONE in P4.
- Trigger fires → opens a new initiative (I47+); does NOT in-line into I46.
- ADR has a "trigger-not-fired sunset" clause: if trigger doesn't fire within 12 months, ADR is reviewed (not auto-revived).

**Rollback:** N/A (defer is reversible by definition).

### R-46-5 — Use-case A (governance KG) drifts between CSV and Neo4j between syncs (M / H)
**Trigger:** Operator edits `SKILL_REGISTRY.csv` → commits → does not run `sync_hlk_neo4j.py` → MADEIRA queries Neo4j and sees stale skill catalog.

**Mitigation:**
- P2 nightly drift canary: `scripts/graphrag_drift_canary.py` compares Neo4j node counts to CSV row counts; fails CI / WIP_DASHBOARD on >1 row deviation.
- Pre-commit hook addition: warn (not block) on CSV edit without sync.
- P2 also adds idempotency proof to `release-gate.py` (per release, must show 2 consecutive identical sync outputs).

**Rollback:** Operator runs sync; canary clears.

### R-46-6 — Doctrine page drifts from reality as new initiatives extend Neo4j (M / M)
**Trigger:** Future initiatives (I47+) add new MCP tools, new edge types, new use-cases → `NEO4J_STRATEGY.md` becomes stale prose.

**Mitigation:**
- Doctrine page has `last_review` frontmatter + 90-day staleness alarm in `validate_localisation_frontmatter` (extend in P1).
- Each new Neo4j-touching initiative is required by `akos-planning-traceability.mdc` to update the doctrine if the use-case classification (A/B/C) changes; cross-cutting test enforces this.

**Rollback:** N/A (review-and-update is the discipline).

### R-46-7 — `hlk_graph_skill_neighbourhood` MCP tool surfaces sensitive policy data (L / M)
**Trigger:** P2 tool returns the full skill subgraph including `POLICY_REGISTER` neighbours; if a policy_id encodes sensitive routing logic (e.g., a tenant-specific RLS exception), exposing it via MADEIRA leaks intent.

**Mitigation:**
- Allowlist-style query: tool returns `(skill, agents_supported, axes_consumed, tools_required, topic_ids)` only; does NOT expand into POLICY_REGISTER unless an explicit `--include-policies` flag is set.
- POLICY_REGISTER stays gated by `policy_class` (the existing `pii_scope` / `redaction` / `service_role_rotation` / `rls` enum); a future `tenant_specific` class would not be expanded by default.

**Rollback:** Remove the tool from `agent-capabilities.json` for the `madeira` role.

### R-46-8 — `retrieval_mode` column on SKILL_REGISTRY (P5) is added but no skill uses it (L / L)
**Trigger:** P3 PoC fails to meet the bar; P5 conditional ship is no-op; column is added for futures-only.

**Mitigation:** Column is intentional even if unused (placeholder for I46 P5 conditional ship + future GraphRAG additions). P5 closure documents whether the column is "live for SKILL-X" or "reserved for future use".

**Rollback:** Drop column (Supabase + CSV migration).

### R-46-9 — Cross-repo doctrine alignment (KiRBe / hlk-erp) ignores `NEO4J_STRATEGY.md` (M / M)
**Trigger:** P1 cites the doctrine in `EXTERNAL_REPO_CONTRACT_TEMPLATE.md` and `kirbe-sync-contract.md` §11. KiRBe / hlk-erp teams may not adopt the citation in their next contract review.

**Mitigation:**
- P1 cross-references are passive (markdown links), not enforced. Adoption is handled by the I32 P7 cross-repo bilingual cover-email pattern: ship a forwarded note when the doctrine lands.
- Future I32 P7-style snapshots will pick up doctrine adoption via `REPO_HEALTH_SNAPSHOT.csv` extension (operator-side, not in I46 scope).

**Rollback:** N/A.

### R-46-10 — P3 PoC succeeds but P5 conditional ship is delayed by I45 P3 dependency (M / L)
**Trigger:** I45 P3 (router refactor) hasn't shipped when I46 P3 PoC succeeds; we want to ship GraphRAG retrieval but the router can't honour `retrieval_mode` yet.

**Mitigation:**
- Phase plan calls out the dependency explicitly (I46 P5 depends on I45 P3).
- If timing slips, P5 ships the column + POLICY_REGISTER row but does NOT wire intent.py; documents "wired in I45 P3" as a forward-reference.

**Rollback:** N/A (the column is harmless even unwired).

### R-46-11 — `neo4j-graphrag-python` package adds runtime dependency (M / L)
**Trigger:** P3 PoC introduces `neo4j-graphrag-python` to `requirements.txt`; future initiatives may pin or unpin awkwardly; library may have its own Neo4j driver version constraint that conflicts with `akos/hlk_neo4j.py`.

**Mitigation:**
- P3 ships with `neo4j-graphrag-python` as an OPTIONAL extra (`pip install -e ".[graphrag]"`); not required for default workflows.
- PoC script imports lazily; absence of the library does NOT break `validate_hlk.py` or main runtime.
- Pin version in P3; revisit at I47 if conflicts surface.

**Rollback:** Remove from optional extras; PoC script becomes inactive.

### R-46-12 — Operator decision fatigue — P4 ADR trigger choice is left undecided (L / M)
**Trigger:** Operator is asked in P4 to pick 1 of 3 candidate triggers for agent memory; defers indefinitely.

**Mitigation:**
- P4 default trigger is "multi-tenant load (when I34 closes)" — most concrete signal, longest deferral horizon. ADR ships with default and operator can flip later via decision-log update.
- If 3 weeks pass post-P4 close without explicit operator pick, default holds.

**Rollback:** N/A (default is itself reversible).

## Cross-references

- I32 P7 cross-repo cover-email pattern → R-46-9 mitigation.
- I32 P9 canary 3 (Langfuse trace shape) → I46 P6 promotes to semantic when GraphRAG ships.
- I22 operator-pasted SOP pattern → R-46-1 cost ceiling enforcement.
- I26 quarterly service_role rotation → R-46-3 portability doctrine pattern.
