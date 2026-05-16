---
initiative_id: I85
language: en
last_review: 2026-05-16
---

# I85 — Decision log

> Charter decisions ratified at P0 (2026-05-16) under I86 batch inline-ratify. All five carry `decision_source: agent_inline_default` because the operator skipped the explicit AskQuestion batch with directive *"continue with information you already have"*; defaults are reversible per [`akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) §"Time-box recovery".

## D-IH-85-A — `AUDIENCE_REGISTRY.csv` scope

**Question**: Should the canonical CSV carry the full per-audience matrix content (bridge frame + objection patterns + first-doubt trigger), or stay narrow (code + name + register-side + surface examples)?

**Options considered**:
- (A) **Narrow FK index** (~8 columns: `audience_code`, `audience_name`, `register_side` (internal|external), `dominant_register_tone`, `first_doubt_trigger_snippet`, `key_surfaces` semicolon-list, `created_at`, `last_review`). Matrix stays SSOT for prose content. **Verdict: chosen.**
- (B) **Full per-audience matrix** (~15 columns including the prose content). Single SSOT but doubles maintenance surface.

**Verdict**: **A — Narrow FK index**. Rationale: two-doc maintenance is not justified for prose content that already lives in the Matrix; the CSV is a FK-resolvability index, the Matrix is the writing-style reference. Mirrors the I77 P4.C precedent (RENDERING_PIPELINE_REGISTRY.csv is also a narrow FK index; the SOP carries the deep content).

**Closes**: C-85-1. **Activated**: 2026-05-16. **Reversible**: yes (CSV can absorb deep columns at P3 if review shows the matrix prose is drifting from the CSV).

## D-IH-85-B — Multi-audience frontmatter encoding

**Question**: When a surface is multi-audience, encode as `audience: J-IN+J-AD` (string with delimiter) or `audience: [J-IN, J-AD]` (YAML list)?

**Options considered**:
- (A) **YAML list** `audience: [J-IN, J-AD]`. Native YAML, FK-resolvable without string parsing, plays well with PyYAML default loader. **Verdict: chosen.**
- (B) **Delimited string** `audience: J-IN+J-AD`. Compact, single-line readable, but every consumer needs to parse the delimiter.

**Verdict**: **A — YAML list**. Rationale: native YAML parsing avoids ad-hoc string parsing in every downstream consumer (validator + drift gate + I81 evidence pack + Impeccable). One canonical encoding reduces ambiguity. Pydantic `List[str]` validator hard-fails malformed input.

**Closes**: C-85-2. **Activated**: 2026-05-16. **Reversible**: low cost — encoding migration could be batch-rewritten if a delimiter encoding became necessary later.

## D-IH-85-C — Tag-migration sweep posture

**Question**: Auto-apply audience tags per agent inference, OR interactive per surface, OR operator-batch-approve per file-class tranche?

**Options considered**:
- (A) **Operator-batch-approve per tranche** (advops/decks first; advops/dossiers next; touchpoint-kit/emails next). Each tranche surfaces a dry-run report; operator approves the batch. **Verdict: chosen.**
- (B) Auto-apply per agent inference. Fastest but audience is a judgement call; errors would silently propagate.
- (C) Interactive per surface. Highest fidelity but ~50-100 surfaces × per-surface decision = pause-fatigue.

**Verdict**: **A — Operator-batch-approve per tranche**. Rationale: balances throughput vs accuracy; aligns with `akos-agent-checkpoint-discipline.mdc` recommended pause-point density for migration-class work; tranches surface inferences in batch so operator can spot-correct in one review pass instead of 50-100 micro-decisions.

**Closes**: C-85-3. **Activated**: 2026-05-16. **Reversible**: yes (operator can demand interactive mode for a specific tranche during P2).

## D-IH-85-D — `BASELINE_REALITY.md` frontmatter

**Question**: Should `BASELINE_REALITY.md` itself gain `audience:` frontmatter (it's an internal bridge consumed by Impeccable and other agents)?

**Options considered**:
- (A) **Yes — `audience: [J-OP]`** for consistency. The bridge is itself an operator-internal surface. **Verdict: chosen.**
- (B) No — the bridge is meta-content; it describes the convention without claiming the convention.

**Verdict**: **A — Yes**. Rationale: "eat your own dog food" — the bridge cannot credibly describe a convention it doesn't follow. `[J-OP]` accurately reflects the readership (operator + agents). Addresses Impeccable audit finding #7 directly.

**Closes**: C-85-4. **Activated**: 2026-05-16. **Reversible**: yes (frontmatter line could be deleted in seconds if review shows it confuses readers).

## D-IH-85-E — I81 absorption posture

**Question**: Does I85 run as a sibling I-NN OR get absorbed as an I81 sub-strand?

**Options considered**:
- (A) **Sibling I-NN with concrete forward-link wire**: I85 P1 mints `AUDIENCE_REGISTRY.csv`; I81 P1 evidence pack adds `audience_tags_coverage` column consuming it. **Verdict: chosen.**
- (B) Absorb into I81. Reduces folder count but blurs governance axis: I81 = vault layout / SOP integrity; I85 = audience tagging / brand-FK-resolvability. Coupling charters that operate on different governance dimensions reduces clarity.

**Verdict**: **A — Sibling I-NN with explicit wire**. Rationale: different governance axes; less coupling = independent closure. The forward-link wire (audience_tags_coverage column) is the concrete "wired up with other jobs" pattern the operator demanded — beats a vague "absorbable by". Sequencing is hard: I85 P1 mints → I81 P1 evidence pack consumes; I86 D-IH-86-D verifies before I81 P1 closes.

**Closes**: C-85-5. **Activated**: 2026-05-16. **Reversible**: low — could re-fold I85 into I81 in a future tidy-up cycle if the two never diverge.

## Pre-existing decision references

- **I77 D-IH-77-I** (validator pinning pattern): I85 P1 mirrors `validate_brand_voice_register_pinning.py` wiring pattern verbatim for `validate_audience_registry.py`.
- **I86 D-IH-86-A** (cluster co-ownership): I85 is Wave 1 of the cluster.
- **I86 D-IH-86-C** (batched AskQuestion at wave boundaries): All five I85 P0 decisions were batched into the Wave 1 cluster ratification 2026-05-16; agent-default fallback fired when operator skipped.
- **I86 D-IH-86-D** (mechanical cross-check before closure): I85 P4 must satisfy the D-IH-86-D ordered list before `INIT-OPENCLAW_AKOS-85` flips to `closed`.
