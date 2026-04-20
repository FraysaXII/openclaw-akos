# Strategic GTM narrative — reference only (Initiative 14)

**Classification:** Reference / synthesis — **not** canonical HLK process law. Canonical SSOT remains [`process_list.csv`](../../../../references/hlk/compliance/process_list.csv), [`baseline_organisation.csv`](../../../../references/hlk/compliance/baseline_organisation.csv), and v3.0 SOPs under `docs/references/hlk/v3.0/`.

**Sources:** Themes from [`docs/references/hlk/business-intent/`](../../../../references/hlk/business-intent/) transcripts (onboarding, ENISA kickoff, etc.) and internal strategy discussions. Promote facts to CSV or SOPs only after operator review.

**Related:** [Initiative 04 — company formation](../../04-holistika-company-formation/) (legal / ENISA / incorporation narrative). **Regulatory claims** (EU AI Act, ENISA certification, CNAE/IAE) require **legal review** before public or investor-facing use; do not treat dates or obligations in this file as legal advice.

---

## 1. Positioning frame

- **Foresight:** Anticipate where the adoption curve moves (e.g. early adopters → early majority) rather than selling only “pure innovation” with unproven ROI.
- **Factor combination:** Combine existing platforms, partnerships, and differentiated delivery instead of competing head-on in saturated late-majority commodity markets.
- **Dual vector (“pincer”):** Executive-level narrative (governance, risk, compliance) plus practitioner-level utility (automation, workflows, time-to-value). Both vectors should connect to the same lead and delivery story—not parallel shadow GTM.

---

## 2. Segment lens (persona table — working)

Use for messaging and channel choice; **segment-specific playbooks** should map to existing `process_list` parents (e.g. [`thi_mkt_dtp_210`](../../../../references/hlk/compliance/process_list.csv)) rather than duplicate org entities.

| Segment | Narrative emphasis | Activation idea |
|---------|-------------------|-----------------|
| Agencies / partners | Embedded automation, revenue share, client lock-in via delivery | Partner intake: [`holistika_gtm_dtp_002`](../../../../references/hlk/compliance/process_list.csv) |
| SME executives / founders | Operational excellence, process before automation | Direct + thought leadership |
| Prosumers / creators | Reliable content and presence tooling | Organic + marketplaces (governed separately) |
| Large / regulated entities | Data governance, compliance, auditability | Enterprise motion + legal alignment |

---

## 3. Five-phase penetration (rhetoric overlay)

These labels are **sales/methodology language**, not new HLK phases. Map to existing flows:

| Label | Plain meaning | Map to (examples) |
|-------|---------------|-------------------|
| Engage | Show value fast; diagnose | Qualification + discovery ([`SOP-GTM_QUALIFICATION_001`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Growth/SOP-GTM_QUALIFICATION_001.md)) |
| Terraform | Stand up data + integrations | Tech Lab / DevOps (existing process rows) |
| Pacify | Trust, governance, “strict mode” | Compliance / data governance SOPs |
| Sell | Close scoped high-value work | BD handoff ([`SOP-GTM_BD_HANDOFF_001`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Growth/SOP-GTM_BD_HANDOFF_001.md)) |
| Normalize | Ongoing value, retention | PMO + customer success (candidate future rows) |

Do **not** add five new top-level `process_list` parents for these names unless a tranche explicitly approves them.

---

## 4. EU / ENISA / legal (disclaimer)

- **EU AI Act** and similar instruments: timelines and obligations change; **counsel** is the authority.
- **ENISA / startup certification** (Spain): business plan and mercantile narrative belong with **Initiative 04** and advisors; this document does not replace filings.

---

## 5. Site availability

Public property outages are **incident and reputation** issues. Handle with status/comms and backlog recovery—**not** as a strategic “blank canvas” excuse. Owner: Ops/CMO per charter.

---

## 6. Verification

This file does **not** require `validate_hlk.py` by itself. If `process_list.csv` or v3.0 links change in the same change set, run the governed matrix in [`docs/DEVELOPER_CHECKLIST.md`](../../../../DEVELOPER_CHECKLIST.md).
