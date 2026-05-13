---
sop_id: SOP-LEGAL_IP_REGISTER_MAINTENANCE_001
title: IP Register Maintenance
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: internal
process_id: hol_lgl_prc_ip_register_mtnce_001
role_owner: Legal Counsel
role_parent_1: CPO
area: Legal
entity: Holistika
governance:
  - D-IH-66-C (per-jurisdiction filing matrix)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-LEGAL_TRADEMARK_MONITORING_001
---

# SOP-LEGAL_IP_REGISTER_MAINTENANCE_001 — IP Register Maintenance

> Legal-Counsel-owned **quarterly process** that maintains the canonical IP register: registered marks, applications-in-progress, oppositions, and renewals due. Companion to `SOP-LEGAL_TRADEMARK_MONITORING_001` (which produces the per-quarter monitoring report).

## 1. Purpose

The IP register is the operator-facing source-of-truth for "what marks does Holistika own / pending / lost / sold". Where `SOP-LEGAL_TRADEMARK_MONITORING_001` produces a per-quarter snapshot, this SOP maintains the **standing register** that the snapshot updates.

The register is a small CSV under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/` (created in P3 Half 2 follow-up tranche, or as part of the I66 P4 trademark-filing strategy phase). Until the CSV exists, the register lives as a canonical Markdown table inside `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`.

## 2. Cadence

**Quarterly** (4 cycles per year). Synchronised with the Trademark Monitoring quarterly cycle (Step 5 of that SOP feeds Step 1 of this SOP).

Out-of-cycle on:

- Registration grant from EUIPO / OEPM.
- Application filed (new mark filed; immediately added with `status: applied`).
- Opposition received from third party (`status: opposed`).
- Refusal received (`status: refused`).
- Renewal completed (`renewed_at: <date>`).
- Mark sold / abandoned / cancelled.

## 3. Inputs

- Latest trademark monitoring report (per `SOP-LEGAL_TRADEMARK_MONITORING_001`).
- Counsel correspondence + filing receipts since last cycle.
- EUIPO + OEPM portal status checks.

## 4. Process steps

### Step 1 — Reconcile against monitoring report (15 min)

For each mark in the monitoring report, confirm the IP register entry matches. Discrepancies indicate either a missed status update on the register or an outdated monitoring report.

### Step 2 — Apply per-mark status updates (10-30 min)

For each mark with status change since last cycle: update the register's `status:` field, `last_status_change_at:`, and any related fields (filing number assigned, opposition number assigned, renewal date scheduled).

### Step 3 — Renewal calendar refresh (10 min)

For all `status: registered` marks, recompute days-to-next-renewal. Flag entries crossing the 12 / 6 / 3 month thresholds for `SOP-LEGAL_TRADEMARK_MONITORING_001` Step 3 (renewal calendar review).

### Step 4 — File register snapshot (5 min)

Snapshot the current register state to `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/IP_REGISTER_SNAPSHOT_<YYYY-Q[1-4]>.md` for institutional-memory purposes. The standing register is mutable; the snapshot is immutable.

### Step 5 — File quarterly review report (10 min)

Under `docs/wip/planning/<active-legal-ops-initiative>/reports/`:

```
ip-register-quarterly-review-<YYYY-Q[1-4]>.md
```

Containing: per-mark status delta table, renewal calendar updates, action items dispatched to operator + counsel.

## 5. Outputs

- Quarterly review report (Step 5 file).
- Snapshot file (Step 4 file).
- Updated standing IP register.
- Action items dispatched.

## 6. Anti-patterns

- **Stale-status drift.** Marks in `status: applied` for > 18 months without a status check usually indicate a filing complication; do not let them sit silently.
- **Snapshot collapse.** Skipping the snapshot step means the institutional memory disappears with each register edit.

## 7. Cross-references

- Sister SOP: [`SOP-LEGAL_TRADEMARK_MONITORING_001.md`](SOP-LEGAL_TRADEMARK_MONITORING_001.md).
- [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) — current home of the register table until a dedicated CSV is shipped.
- D-IH-66-C (per-jurisdiction filing matrix).
