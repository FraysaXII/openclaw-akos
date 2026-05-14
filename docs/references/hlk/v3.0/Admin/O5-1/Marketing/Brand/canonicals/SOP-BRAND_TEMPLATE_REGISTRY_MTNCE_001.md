---
sop_id: SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001
title: Brand Template Registry Maintenance
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: internal
process_id: tbi_mkt_prc_template_registry_mtnce_001
role_owner: Brand & Narrative Manager
role_parent_1: CMO
area: MKT
entity: Holistika
governance:
  - D-IH-66-J (drift gates wired into release-gate)
  - D-IH-66-T (P6 governance.brand_template_registry view)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-BRAND_CANON_MAINTENANCE_001
  - SOP-BRAND_DRIFT_GATE_OPS_001
---

# SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001 — Brand Template Registry Maintenance

> Brand-Manager-owned **quarterly process** that maintains the canonical registry of brand templates (decks, dossiers, email signatures, press kit, recruiter copy, partner pitch, founder bio). Operationalises the `governance.brand_template_registry` view (P6 deliverable).

## 1. Purpose

Holistika's brand templates are scattered across surfaces (boilerplate's `_assets/advops/`, deck YAML sources, email-signature HTML, press-kit Markdown, etc.). Without a registry, three failure modes recur:

- **Stale templates ship.** A deck template that hasn't been updated since the brand canon shifted gets sent to a counterparty.
- **Variant drift.** The investor deck and the partner deck diverge on shared brand elements (founder bio, logo placement, voice tier) without intent.
- **Discovery cost.** Every new collaborator spends time finding the canonical version of each template.

The registry tracks every brand template's location, last-update date, last-canon-sync date, and `governed-by` SOP link.

## 2. Cadence

**Quarterly** (4 cycles per year). Out-of-cycle on:

- New template introduced (immediate registration).
- Material brand canon shift (registry sweep to identify which templates need a re-sync pass).
- Drift-gate signal cluster pointing at template content.

## 3. Inputs

- Current `governance.brand_template_registry` view contents (P6 deliverable; until P6 lands, the registry lives as a Markdown table at `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_TEMPLATE_REGISTRY.md`).
- Last-quarter canon-update history (per `SOP-BRAND_CANON_MAINTENANCE_001` quarterly review reports).
- Validator outputs across the 4 brand drift gates.

## 4. Process steps

### Step 1 — Inventory sweep (15 min)

Walk the canonical template locations (decks under `_assets/advops/`, email-signature HTML, press-kit Markdown, etc.) and confirm every template has a registry row. Add rows for missing templates.

### Step 2 — Per-template currency check (30-45 min)

For each registered template:

- Last-update date (from git log).
- Last-canon-sync date (from registry; manually updated by maintainers when they intentionally pass through a template after a canon update).
- Currency status: **current** (synced after most recent canon update) / **stale** (canon update happened after last sync, no review).

### Step 3 — Triage stale templates (15-30 min)

For each stale template:

- **Re-sync this quarter** (high-traffic templates: investor deck, founder bio, email signatures).
- **Re-sync next quarter** (medium-traffic: advisor deck, partner deck).
- **Defer** with sunset date (low-traffic: legacy templates approaching deprecation).

### Step 4 — Per-template canon-cross-reference verify (15 min)

For each template, confirm the declared `references:` block in template frontmatter matches the actual canonical files cited. Drift indicates the template references a canonical that has been moved or renamed.

### Step 5 — File quarterly review report (10 min)

Under `docs/wip/planning/<active-brand-ops-initiative>/reports/`:

```
brand-template-registry-review-<YYYY-Q[1-4]>.md
```

Containing: per-template currency table, triage decisions, applied re-syncs, deferred-with-sunset rows.

## 5. Outputs

- Quarterly review report (Step 5 file).
- Updated registry (currency markers + new rows).
- Re-synced templates (cascaded to consumer surfaces).

## 6. Anti-patterns

- **Add-only drift.** Adding rows to the registry but never marking them `current` after a sync means the registry stops being trusted.
- **Single-template spot-check.** Reviewing only the most-prominent template each quarter (e.g., investor deck) and ignoring the others. Registry coverage is non-negotiable.
- **Canon-cross-reference rot.** Templates citing renamed canonicals stop being parseable by tooling; Step 4 catches this.

## 7. Cross-references

- Sister SOPs: [`SOP-BRAND_CANON_MAINTENANCE_001.md`](SOP-BRAND_CANON_MAINTENANCE_001.md), [`SOP-BRAND_DRIFT_GATE_OPS_001.md`](SOP-BRAND_DRIFT_GATE_OPS_001.md).
- P6 deliverable: `governance.brand_template_registry` view.
- D-IH-66-T (P6 view definition).
