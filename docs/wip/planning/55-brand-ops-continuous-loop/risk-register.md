---
language: en
status: active
initiative: 55-brand-ops-continuous-loop
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 55 — Risk register

## R-55-1 — Operator changes mind mid-pre-flight or after send

**Severity:** Medium-High.

**Mitigation:** Pre-flight is reversible (drafts hold composer); G-24-3 is IRREVERSIBLE by definition per fire; **no retry/recall policy**. The pre-flight checklist (D-IH-55-A) explicitly asks the operator to confirm intent at every box.

**Status:** Active.

---

## R-55-2 — Recipient email address leaks into git

**Severity:** High.

**Mitigation:** Pre-commit grep for SMTP recipient pattern (D-IH-55-B); off-repo identity store; SOP cite per `SOP-HLK_TRANSCRIPT_REDACTION_001`.

**Status:** Active.

---

## R-55-3 — Brand voice authoring slips into invention

**Severity:** High (doctrinal).

**Mitigation:** D-IH-17 "we cite operator's lived protocols, not invent". P1 + P2 explicitly run Wave-2 backfill, not free-form. **In this cycle: P1-P2 deferred to operator wave-2 fill (OPS-55-1).** No agent-authored brand voice content lands until the operator fills Wave-2 Section 2 + 3.

**Status:** Active and **realized as anticipated** in this cycle (P1-P2 deferred to OPS-55-1).

---

## R-55-4 — `compose_adviser_message` adds language jargon that fails brand lint at runtime

**Severity:** Medium.

**Mitigation:** I49 `lint_brand_voice_offline.py` runs in `pre_commit`; composer tests assert linter green on rendered fixtures (I55 P5).

**Status:** Active.

---

## R-55-5 — Material-change threshold too tight: real improvements never trigger a proposal

**Severity:** Medium.

**Mitigation:** Per-axis thresholds tunable in `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` POLICY (P7). Operator can manually trigger via `propose_advisor_update.py --force-proposal`.

**Status:** Active.

---

## R-55-6 — Material-change threshold too loose: advisor gets spammed with non-improvements

**Severity:** Medium.

**Mitigation:** G-24-3 is per-fire operator-gated (no auto-send); threshold defaults err on the conservative side (D-IH-55-D); operator review before any send.

**Status:** Active.

---

## R-55-7 — Operator improves brand/ops indefinitely without ever sending; advisor relationship cools

**Severity:** Low (this is a feature, not a bug — operator independence is the point).

**Mitigation:** `loop-history.md` (D-IH-55-E) surfaces "N regressions, 0 sends since YYYY-MM-DD" so the silence is visible and the operator can decide. No automated escalation.

**Status:** Active.

---

## R-55-8 — Loop-tooling diff produces false positives on cosmetic dossier reformat

**Severity:** Low-Medium.

**Mitigation:** `regression_artifact_diff.py` compares **structural** signals (cite-counts, scenario IDs that flipped, judge-axis movement, register row counts) — NOT raw text bytes. Cosmetic reformat (whitespace, section reordering, sparkline pixel drift) does not move structural signals.

**Status:** Active.

---

## R-55-9 — `loop-history.md` accumulates indefinitely

**Severity:** Low (admin hygiene).

**Mitigation:** One-line entry per regression cycle (~120 chars); even at daily cadence, 10-year accumulation is ~440 KB. Single-file growth bounded; archive to per-year files only if file size exceeds 5 MB.

**Status:** Active.
