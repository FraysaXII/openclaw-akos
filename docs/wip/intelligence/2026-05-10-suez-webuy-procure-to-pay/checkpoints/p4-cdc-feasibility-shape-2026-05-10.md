---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P4
phase_name: CDC feasibility shape (FR centerpiece)
recorded_at: 2026-05-10
---

# P4 — CDC feasibility shape self-checkpoint

## Files authored

| File | Format | Lines |
|:---|:---|---:|
| `docs/references/hlk/v3.0/_assets/advops/shared/2026-suez-webuy/cdc-feasibility-shape.fr.md` | FR external register | ~250 |

## Structure

10 sections, 24 numbered functionalities, plus 3 reference tables:

* §0 — common preamble (constants across all categories).
* §1 — F-01 → F-04: workflow trigger + portal navigation.
* §2 — F-05 → F-11: procurement-side fields (label, profit centre, delivery, cost centre, D.I., comments).
* §3 — F-12 → F-22: supplier-side article detail (label, date, price, supplier, accounting, submit).
* §4 — F-23 → F-24: follow-up + monthly reporting (currently manual).
* §5 — twelve intervention codes (CAP / PMR / PMC / PMS / PMV / FSC / FSR / PMF / FST / PMT / PML / FSL).
* §6 — synthesis by eligibility flag (`actionnable` / `nécessite accès à l'application WeBuy` / `manuel uniquement (opérationnel)`).
* §7 — pre-conditions for detailed scoping.
* §8 — open hypotheses.
* §9 — three downstream deliverables (detailed CDC, feasibility study, lightweight prototype).
* §10 — cross-references.

## Eligibility-flag distribution

| Flag | Count | Headline |
|:---|---:|:---|
| `actionnable` | 19 | Generative / deterministic / lookup / extraction. |
| `nécessite accès à l'application WeBuy` | 9 | Effective portal interaction. |
| `manuel uniquement (opérationnel)` | 1 | F-09 — eOTP exchange with accounting. |

Reads commercially as per the plan: most of the process is generative / deterministic; an incompressible minority requires effective portal action; a single step stays manual. The variant comparison in `commercial-schedule.md` (Variants A / B / C) remains valid against this functional decomposition.

## FR external register adherence

* Vous register held throughout (no `tu`).
* Anglicisms scrubbed per `BRAND_FRENCH_PATTERNS.md` §5.1: `processus` not `process`; `livrable` not `deliverable`; `cadre` not `framework`; `cœur de métier` not `core business`. The single deliberate retention is `e-mail` (universally accepted).
* `manuel opérationnel` used for what English-internal would call `playbook`.
* Triadic structure used in §0 (workflow / detail / supplier) and §9 (three downstream deliverables) — consistent with the FR pattern reference in §3.2 of `BRAND_FRENCH_PATTERNS.md`.
* `[entité juridique du donneur d'ordre]` placeholder used wherever the formal name would otherwise appear (consistent with D-ENG-SUEZ-A still open).
* Specific examples retained as illustrative (`ENG5846`, `ENG6072`, `BRO00000759`) and explicitly framed as méthodologiques in §0 and the closing paragraph.

## Verification

* Manual review against `extracts/mode_ope_ratoire_-_process_de_passage_de_commande_webuy.txt` confirms every functionality block sources back to the document. F-01 → F-04 cover workflow init; F-05 → F-11 cover the « bloc orienté approvisionnement » verbatim; F-12 → F-22 cover the « bloc orienté fournisseur » verbatim; F-23 → F-24 reflect the follow-up + reporting gap explicitly raised in the EFA prospection brief.
* No collaborator name appears.
* No specific euro amount appears.
* Counterparty name placeholder `[entité juridique du donneur d'ordre]` used 7 times (header, §0 §1, §6, §7, §8, closing).

## Next

P5 — Discovery questionnaire (FR). 1–2 pages, Section A frame-setting (3 questions) + Section B direct elicitation (5 questions) translated from `elicitation-template-customer-sme.md` to FR external register, tailored to the WeBuy procure-to-pay context.
