---
language: en
status: active
initiative: 55-brand-ops-continuous-loop
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 55 — Decision log

Six decisions seeded; operator-ratified at I50-I56 master-roadmap session 2026-05-03 ("we operate independently from the advisor … keep improving brand and ops while doing regressions").

## D-IH-55-A — Pre-flight checklist authoritative location

**Decision:** Per-fire pre-flight checklist lives in I55 `reports/uat-adviser-send-N-YYYY-MM-DD.md` (N increments). Cumulative log in `reports/loop-history.md` records every regression cycle (proposal or no-proposal) so the loop shows both signal and silence.

**Rationale:** The I24 P6 pre-flight template exists; rather than fork it, I55 reuses the per-fire pattern with N-incrementing reports — each fire is its own UAT closure. The cumulative `loop-history.md` is what makes the loop's *velocity* visible (D-IH-55-E + R-55-7).

---

## D-IH-55-B — SMTP send path: off-repo identity store

**Decision:** Recipient email address **never enters git**. Pre-commit grep guard for SMTP-recipient pattern. Off-repo identity store (operator's personal email client / address book).

**Rationale:** R-55-2 mitigation. PII in git is a hard incident; the cost of preventing it is one regex. SOP cite per `SOP-HLK_TRANSCRIPT_REDACTION_001`.

---

## D-IH-55-C — I24 vs I55 folder split

**Decision:** I24 stays Closed at capability landing (P8). I55 stays **Open as continuous loop** (D-IH-55-F). Both linked via cross-references.

**Rationale:** I24's deliverables are *capabilities* (composer, brand foundation, GOI/POI ALTER, register schema). Once those exist, I24's mission is complete. The *operating loop* (regression → review → improve → maybe-send) is a different shape — it's a continuously running process, not a project. Splitting them keeps the planning README readable and the open-vs-closed signal honest.

---

## D-IH-55-D — Material-change threshold default values

**Decision (default values):**
- `min_changed_scenarios ≥ 3` (at least 3 PERSONA_SCENARIO rows must move).
- `min_judge_axis_movement_pp ≥ 2` (at least one judge axis must shift ≥2 percentage points up).
- `min_register_rows_added ≥ 1` (at least one canonical-register row added or materially edited since last send).

**Rationale:** Conservative defaults trade off R-55-5 (too tight: never triggers; advisor never updated) vs R-55-6 (too loose: spam). The bias is toward "tight" because G-24-3 is IRREVERSIBLE per fire; the operator can always force a proposal via `propose_advisor_update.py --force-proposal`. Field values can be tuned per-advisor or per-tier (POLICY-row edit, not code edit).

**Reversibility:** High — POLICY row edit + decision-log update.

---

## D-IH-55-E — Loop telemetry

**Decision:** Every G-24-3 fire writes a `reports/uat-adviser-send-N-YYYY-MM-DD.md`. Every regression cycle that **does not** trigger a proposal also logs to `reports/loop-history.md` (one-line entry: timestamp + diff summary + reason for no-proposal). The operator sees both signal and silence.

**Rationale:** R-55-7 mitigation. If the loop runs 12 times in 90 days with 0 sends, that's a visible metric ("N regressions, 0 sends since YYYY-MM-DD") that surfaces "operator independence is working" or "advisor relationship cooling" depending on the operator's read. Without telemetry of the silence, the operator only sees fires.

---

## D-IH-55-F — Closure of I55 itself

**Decision:** **No fixed end date.** Revisit closure trigger only if doctrine changes (e.g., advisor relationship ends; communication methodology rewritten; operator decides loop is no longer worth running).

**Rationale:** This is the heart of the operator's reframing — the loop is the deliverable, not a one-time send. I55 stays Open as a tracked initiative with a continuous-loop status; it never auto-closes.

---

## Decisions made during execution

(Will be appended as P0-P8 phases execute.)
