---
initiative_id: I87
language: en
last_review: 2026-05-16
---

# I87 — Decision log

> Charter decisions ratified at P0 (2026-05-16) under I86 batch inline-ratify. All three carry `decision_source: agent_inline_default` because the operator skipped the explicit AskQuestion batch with the directive *"continue with information you already have"*; defaults are reversible per [`akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) §"Time-box recovery".

## D-IH-87-A — Escalation sink for health-monitor failure loops

**Question**: When the OpenClaw health monitor records N (default 3) consecutive 30-min failure cycles for the same root cause, where does the operator-visible signal go?

**Options considered**:
- (A) Append a row to `OPS_REGISTER.csv` + render via `scripts/render_operator_inbox.py` into `OPERATOR_INBOX.md`. **Verdict: chosen.**
- (B) Post to a Slack webhook (requires `AKOS_OPS_SLACK_WEBHOOK` secret in env).
- (C) Render a toast in the MADEIRA control-plane HTML at `static/madeira_control.html`.
- (D) All three behind feature flags.

**Verdict**: **A — OPERATOR_INBOX.md row**. Rationale: lowest coupling (the surface already exists; renderer is shipped; the row obeys the canonical CSV gate the rest of the cluster respects); aligns with [`akos-governance-remediation.mdc`](../../../.cursor/rules/akos-governance-remediation.mdc) §"Runtime contract" — the inbox is the SSOT for operator-visible obligations. B + C are deferred follow-ups conditional on signal-to-noise at P6 review.

**Closes**: C-87-1. **Activated**: 2026-05-16. **Reversible**: yes (P6 review can promote to B+C without breaking A).

## D-IH-87-B — `plugins.allow` validator scope

**Question**: Ship a `scripts/validate_openclaw_plugin_pinning.py` validator at P2, or defer to a future hygiene pass?

**Options considered**:
- (A) Ship in P2 mirroring I77 P4.C `validate_brand_voice_register_pinning.py` wiring pattern in miniature. **Verdict: chosen.**
- (B) Defer; allow operators to edit `plugins.allow` manually without validation rails.

**Verdict**: **A — ship miniature validator now**. Rationale: precedent is fresh (I77 P4.C 2026-05-14); shipping in P2 closes the loop while the pattern is in working memory; the validator surface is ~30 lines (per-environment allow-list + Pydantic check + integration with `release-gate.py` as INFO). Deferring creates two-phase tech debt — pin without validation today, validator next quarter — that the inline-ratify-craft skill flags as a known anti-pattern.

**Closes**: C-87-2. **Activated**: 2026-05-16. **Reversible**: yes (validator can be deleted if it produces zero signal at P6 review).

## D-IH-87-C — modelsConfig posture for `ollama/qwen3:8b`

**Question**: Bump the context window for `ollama/qwen3:8b` in modelsConfig (raise to 32K+ to clear the warn threshold), or remove the entry entirely?

**Options considered**:
- (A) Remove the entry. Gateway log evidence shows requests already fall back to vLLM after bonjour self-heal fires; the row is observability drift, not functional. **Verdict: chosen.**
- (B) Bump ctx and keep the entry as a "Ollama is registered but rarely used" signal.
- (C) Investigate whether Ollama serves the row at all on operator host; defer the decision.

**Verdict**: **A — remove the unused row**. Rationale: keeping an entry that warns every cycle but never serves traffic creates a learned-blindness pattern (operator dismisses the warn because it's known-bad). Removing the row makes the next warn a real signal worth investigating. Bonjour self-heal already routes around the missing model; this is documented as the fallback path in P3.

**Closes**: C-87-3. **Activated**: 2026-05-16. **Reversible**: yes (P3 ships with a one-liner rollback to re-add the row if bonjour self-heal misbehaves under load).

## Pre-existing decision references

- **I86 D-IH-86-A** (cluster coordinator co-ownership): I87 is the operational sibling to I84 in the wave cluster.
- **I86 D-IH-86-C** (batched AskQuestion at wave boundaries): I87's three decisions were batched into the Wave 1 cluster ratification at 2026-05-16; agent-default fallback fired when operator skipped.
- **I77 D-IH-77-I** (validator pinning pattern): I87 D-IH-87-B inherits this validator wiring pattern in miniature for `plugins.allow`.
