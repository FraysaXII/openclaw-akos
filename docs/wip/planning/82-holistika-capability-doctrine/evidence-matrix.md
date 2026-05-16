# I82 — Evidence matrix

What evidence each phase produces and what verifier validates it.

| Phase | Evidence artefact | Validator | Manual review? |
|:---|:---|:---|:---|
| **P0 — Charter** | `master-roadmap.md` + 5 sibling planning files + INIT/DEC/OPS canonical rows | `py scripts/validate_hlk.py` | Inline-ratify (operator skip 2026-05-16 → `agent_inline_default`) |
| **P0 followup — Doctrine mint** | `HOLISTIKA_CAPABILITY_DOCTRINE.md` paired body + `.addendum.md` at `People/canonicals/` | `py scripts/validate_hlk.py`; `py scripts/validate_knowledge_pairing_registry.py`; `KNOWLEDGE_PAIRING_REGISTRY.csv` row | Operator approval (doctrine prose review) |
| **P1 — Talent activation** | `baseline_organisation.csv` row append; optional `process_list.csv` Talent upkeep rows | `py scripts/validate_hlk.py` (includes `validate_baseline_organisation.py` + `validate_process_list.py`) | **Operator approval** (canonical-CSV gate per `akos-governance-remediation.mdc`) |
| **P2 — Capability registry** | `CAPABILITY_REGISTRY.csv` seed rows + Pydantic + validator + tests + `CANONICAL_REGISTRY.csv` row + `PRECEDENCE.md` row; seed rows reference audited `process_list.csv` paths via I81 P1 integrity matrix | New validator GREEN; `py scripts/validate_hlk.py`; `py scripts/test.py governance` | **Operator approval** (canonical-CSV gate; D-IH-82-PREREQ closes here if no I81 P1 evidence yet) |
| **P3 — Confidence rating** | `CAPABILITY_CONFIDENCE_REGISTRY.csv` paired body+addendum; SCP-cameo + numbers + plain registers in addendum | New validator GREEN; Marketing/Brand co-sign signature in `reports/p3-confidence-naming-cosign-<date>.md` | Operator approval (D-IH-82-C close) |
| **P4 — Use case archive** | `USE_CASE_ARCHIVE.csv` with 5 POC seed rows (GDF + Hosteleria + RCD + documentation-team + Shopify); redaction policy documented | New validator GREEN; FK resolution to `CAPABILITY_REGISTRY.csv` + `redaction_class` enum check | Operator approval (D-IH-82-E close) + Compliance Officer redaction sign-off per row |
| **P5 — Eloquence extension** | `BRAND_BASELINE_REALITY_MATRIX.md` §N "Capability messaging extension" with per-audience translation tables (consumes I85 `AUDIENCE_REGISTRY.csv`) | `py scripts/validate_brand_baseline_reality_drift.py`; `validate_audience_tags.py` (I85 P2 deliverable) | Inline-ratify |
| **P6 — Mirrors + ERP alignment** | `compliance.*_mirror` row appends + `hlk-erp` capability-panel route specs | `py scripts/verify.py compliance_mirror_emit`; sibling repo CI | Inline-ratify (coordinated with I81 P2 layout waves if interleaving) |
| **P7 — Live UAT + closure** | `reports/p7-live-capability-surfacing-uat-<date>.md` — one live external-stakeholder request rehearsed AND served via the doctrine flow (or waiver narrative); closure UAT report | `py scripts/verify.py pre_commit`; `py scripts/release-gate.py` | Operator approval (closure gate) |

## Acceptance threshold

- **P2 PASS bar**: every `CAPABILITY_REGISTRY.csv` seed row resolves cleanly via FK to a `process_list.csv` `item_id` that has been audited PASS in I81 P1 integrity matrix (OR operator waiver via D-IH-82-PREREQ logged in row's `notes` column).
- **P4 PASS bar**: every `USE_CASE_ARCHIVE.csv` row has `redaction_class` set + Compliance Officer sign-off in `notes` before any external surfacing.
- **P7 PASS bar**: one live capability-surfacing rehearsal executes end-to-end (counterparty request → capability rows + confidence + proofs + eloquence-translated reply); transcript captured (redacted per redaction policy) in P7 UAT report. Waiver acceptable with explicit narrative.

## Out-of-band evidence (operator-side)

- Marketing/Brand naming co-sign for D-IH-82-F (filename decision) at P0 followup.
- Compliance Officer redaction sign-off per `USE_CASE_ARCHIVE` row at P4.
- Operator live-UAT scheduling row tracked as `OPS-82-1`.
