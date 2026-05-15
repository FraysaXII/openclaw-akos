---
language: en
status: active
authored: 2026-05-15
last_review: 2026-05-15
role_owner: PMO
classification: fact
ssot: true
---

# Universal kickstart — paste this into a fresh Cursor chat

> **What this is.** The "literally paste this into a fresh agent chat" artefact for any Holistika initiative — discovery, plan-author, mid-execution, or trigger-watch.
>
> **What it does.** Routes the agent into the right mode + tells it which files to read before touching anything else.

---

## Step 1 — Mandatory read-pass (before any tool call)

Read these three files end-to-end. Do not skip:

1. [`docs/wip/planning/_templates/PLANNING_COMPENDIUM.md`](PLANNING_COMPENDIUM.md) — the SSOT for initiative discipline. ~1500 lines. Cover §1 through §10 fully; §11 (per-initiative appendix) only the relevant sub-section.
2. [`docs/wip/planning/_templates/INITIATIVE_DEPENDENCIES.md`](INITIATIVE_DEPENDENCIES.md) — mermaid dep map + per-initiative blocker table + cross-strand linkages.
3. The mode-routing block below (Step 2).

If any of (1–3) doesn't load, STOP and surface the gap via `AskQuestion`.

---

## Step 2 — Mode routing

Pick one mode. If unsure, ask the operator via `AskQuestion`.

| Mode | Trigger | Entry checklist |
|:---|:---|:---|
| **fresh** | Operator says "let's plan a new initiative" with a loose idea; no candidate scaffold OR candidate exists but operator wants to re-discover. | (a) Run compendium §3 Discovery pipeline. (b) Capture 5-7 operator-context fields via `AskQuestion`. (c) Read candidate scaffold if exists. (d) Sketch architecture mermaid during discovery (§3.3). (e) Surface conundrums inline (§3.4 + §3.5). (f) Author discovery report (§3.6) + self-critique gate (§3.7). |
| **gated_operator** | Candidate exists in `INITIATIVE_REGISTRY.csv` with `status: gated_operator`; operator says "activate I7N". | (a) Read `INITIATIVE_REGISTRY.csv` row to confirm `gated_on:` clearance. (b) Read candidate scaffold under `docs/wip/planning/_candidates/`. (c) Read related initiatives' `master-roadmap.md` per `INITIATIVE_DEPENDENCIES.md` blocker rows. (d) Skip operator-context capture (use candidate's operating story); jump to compendium §3.2 read-pass → §3.4 conundrums → §4 plan-author. |
| **mid-execution** | Operator says "continue I7N P3" or `git log` shows initiative in flight. | (a) Read initiative's `master-roadmap.md`. (b) Read the Cursor plan body for the in-flight phase. (c) Self-checkpoint (compendium §8.2) before starting. (d) Execute phase → ONE atomic commit per phase. (e) Inline-ratify gate before next phase (compendium §6). |
| **TRIGGER-watch** | Candidate is `gated_external` or TRIGGER-watch (e.g. I74 ≥2 external requests; I78 ≥2 regex-pushback signals). | (a) Read candidate scaffold §"Spin-out trigger conditions" or §"TRIGGER conditions". (b) Confirm trigger has NOT fired. (c) If operator asks to plan anyway, surface `AskQuestion` confirming operator override. (d) Otherwise: no-op; close chat with summary. |

If operator does not specify the mode, infer from:

- `git log --oneline -5` (shows in-flight work → mid-execution),
- presence of `INITIATIVE_REGISTRY.csv` row with `status: active` (mid-execution) vs `status: gated_operator` (gated_operator),
- absence of any registry row (fresh).

---

## Step 3 — Self-critique gate hand-off

Before declaring any plan / discovery report / phase commit "ready for operator ratification", run the **12-row self-critique gate** from compendium §2.2 verbatim. Report per-row PASS / FAIL with evidence. Revise on FAIL; re-run.

The gate is non-negotiable. Operators may waive specific rows in writing (logged as D-IH-7N-* row); agents may not waive unilaterally.

---

## Step 4 — Inline-ratify discipline

Per compendium §6 + [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc):

- **Use `AskQuestion`** for: evidence-dependent decisions, spot-check / approval gates, architectural forks surfaced during discovery.
- **Do NOT use** the phrase `OPERATOR PAUSE POINT` in plan bodies, commit messages, or chat. Use `(inline-ratify gate at §X.Y)` instead.
- **Use `opt-stop-report`** (a 5-line blocker report) ONLY for: validator failures, broken builds, missing files, security incidents. NOT for decisions.
- **Option labels carry**: rationale snippet + cited evidence (internal file path or external URL) + `(recommended …)` suffix when one option is the agent's default.
- **Batch up to 6 questions** per `AskQuestion` call. Don't fire sequential single-question calls when batched.

---

## Step 5 — Phase + commit discipline

Per compendium §4 + [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc):

- ONE atomic commit per phase. P0 charter = ONE commit (outputs A-I per compendium §4.3). P1 = ONE commit. P2 = ONE commit. Etc.
- Commit message format: `i[7N] p<N> <one-line summary>`.
- Update `docs/wip/planning/<NN-slug>/files-modified.csv` with every commit (18-column schema per `akos-planning-traceability.mdc` §"Per-initiative file-changes CSV").

---

## Step 6 — Final pre-commit gate

Per compendium §5:

Run validators in this order; STOP at first FAIL:

1. `py scripts/verify.py pre_commit` (composes most validators per `config/verification-profiles.json`),
2. OR the discrete sequence in compendium §5.1.

On FAIL: write `docs/wip/planning/<NN-slug>/reports/p<N>-blocker-<YYYY-MM-DD>.md` (opt-stop-report posture) and stop.

---

## Closing line

**Do not skip the self-critique gate. Do not skip the dep-map read. Use `AskQuestion` for every architectural fork surfaced during discovery. NEVER write `OPERATOR PAUSE POINT`. ONE atomic commit per phase.**

If you find yourself about to violate any of the above, STOP and surface the conflict inline.
