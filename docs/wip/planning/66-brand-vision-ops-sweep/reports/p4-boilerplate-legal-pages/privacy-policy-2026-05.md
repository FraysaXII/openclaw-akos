---
draft_for: boilerplate/app/privacy/page.tsx
status: P5_input_draft
language: en (canonical; ES + FR translations follow at P5)
register: external
governance: D-IH-66-W (legal templates), GDPR + LSSI-CE
linked_initiative: I66
created: 2026-05-09
last_review: 2026-05-09
---

# Privacy Policy — Holistika Research SL (P5 input draft)

> **Draft for boilerplate `/privacy` route**. P5 (boilerplate rewrite) consumes this draft, translates to ES + FR, and renders into `boilerplate/app/privacy/page.tsx`. Counsel review before publication is mandatory; this is a starting draft, not a final-form policy.

> Replace `[BRACKETED]` placeholders with operator-supplied values before publication.

---

## Privacy Policy

**Last updated**: `[YYYY-MM-DD]`
**Effective date**: `[YYYY-MM-DD]`

This Privacy Policy describes how **Holistika Research SL** ("**Holistika**", "**we**", "**us**") collects, uses, and protects personal data in connection with our website (`https://holistikaresearch.com` and its subdomains) and our services. We act as **Data Controller** in respect of the personal data described in this policy.

If you have questions, contact us at `privacy@holistikaresearch.com` or by post at `[REGISTERED_ADDRESS]`.

### 1. Data we collect

We collect personal data in three categories:

**1.1. Information you provide directly**
- Contact information (name, email, organisation, role) when you fill in our contact forms or request a discovery conversation.
- Communication content (the messages you send us by email, contact form, or scheduled call).
- Information you provide during a discovery, advisory, or engagement conversation, including documents you share with us.

**1.2. Information we collect automatically**
- Technical information about your visit (IP address, browser, device type, referring URL).
- Aggregate, anonymised analytics about page views and engagement.

**1.3. Information from third parties**
- Information from public business registers (e.g., Companies House, Registro Mercantil) when we conduct preparatory research on a counterparty before an engagement (per our research methodology).
- Information from professional networks (e.g., LinkedIn) where you have made it publicly available.

### 2. Why we collect it (legal bases)

We process personal data on the following legal bases under GDPR Article 6:

| Purpose | Legal basis |
|:---|:---|
| Responding to your inquiries; managing the discovery + proposal cycle | Contract performance + pre-contractual measures (GDPR Art. 6(1)(b)) |
| Performing services under an executed engagement | Contract performance (GDPR Art. 6(1)(b)) |
| Sending operational emails (engagement updates, deliverable notifications) | Contract performance (GDPR Art. 6(1)(b)) |
| Marketing emails (only with your prior consent) | Consent (GDPR Art. 6(1)(a)) |
| Compliance with legal obligations (tax, accounting, regulatory) | Legal obligation (GDPR Art. 6(1)(c)) |
| Establishing, exercising, or defending legal claims | Legitimate interest (GDPR Art. 6(1)(f)) — defending business interests |
| Aggregate analytics + service improvement | Legitimate interest (GDPR Art. 6(1)(f)) — improving our services |

We do **not** process special-category data (health, political opinions, etc.) without your explicit consent under GDPR Article 9.

### 3. How long we keep it (retention)

We retain personal data only as long as necessary for the purposes for which it was collected:

- **Inquiry data (no engagement materialises)**: 24 months from last contact.
- **Engagement data (active engagement)**: duration of engagement + 6 years post-engagement (Spanish accounting / tax retention requirement).
- **Aggregate analytics**: indefinitely in anonymised form.
- **Marketing-consent data**: until you withdraw consent or until 36 months of inactivity, whichever first.

### 4. Who we share it with

We share personal data only with:

- **Service providers** who help us operate the business (cloud hosting, email infrastructure, accounting software). These are bound by Data Processing Agreements per GDPR Article 28.
- **Professional advisors** (lawyers, accountants, auditors) as needed for their professional services.
- **Authorities** when required by law or court order.
- **Successors in interest** in the event of a merger, acquisition, or sale of substantially all assets (subject to equivalent privacy protection).

We do **not** sell personal data and we do not share it with marketing data brokers.

### 5. International transfers

Our primary data infrastructure is in the EEA. Where personal data is transferred outside the EEA (e.g., to certain service providers), we rely on:

- European Commission **adequacy decisions** (e.g., for transfers to countries with adequate protection); or
- **Standard Contractual Clauses** (Commission Decision 2021/914); or
- Other lawful transfer mechanisms documented at the time of transfer.

A list of our current sub-processors and their locations is available on request.

### 6. Your rights (GDPR Chapter III)

You have the following rights regarding your personal data:

- **Access** — request a copy of personal data we hold about you.
- **Rectification** — request correction of inaccurate or incomplete data.
- **Erasure** — request deletion ("right to be forgotten"), subject to retention obligations.
- **Restriction** — request that we restrict processing.
- **Portability** — request transfer of data to another controller in a structured machine-readable format.
- **Objection** — object to processing based on legitimate interest, including direct marketing.
- **Withdrawal of consent** — withdraw consent at any time where processing is based on consent.
- **Complaint** — lodge a complaint with the Spanish Data Protection Agency (AEPD: <https://www.aepd.es>) or the supervisory authority of your habitual residence.

To exercise these rights, contact us at `privacy@holistikaresearch.com`. We respond within 30 days.

### 7. Security

We implement appropriate technical and organisational measures to protect personal data, including: encrypted data transmission (TLS 1.2+); access controls based on role and need-to-know; regular review of security practices; incident response procedures; and Data Processing Agreements with all sub-processors.

In the event of a personal data breach affecting your data, we notify you and the supervisory authority as required by GDPR Article 33-34.

### 8. Cookies and tracking

For information about cookies and similar technologies on our website, see our separate [Cookie Policy](/cookies).

### 9. Children's privacy

Our services are intended for business and professional contexts. We do not knowingly collect personal data from children under 14 (the age threshold under Spanish data protection law). If you believe we have done so inadvertently, contact us and we will delete the data.

### 10. Changes to this policy

We may update this policy from time to time. The "Last updated" date at the top reflects the most recent change. Material changes are communicated to active engagement counterparties by email; non-material changes (e.g., editorial improvements) are not actively communicated.

### 11. Contact

**Data Controller**: Holistika Research SL
**Address**: `[REGISTERED_ADDRESS]`
**Email**: `privacy@holistikaresearch.com`
**Data Protection Officer**: `[Not appointed (small entity below GDPR Art. 37 threshold) | DPO contact if appointed]`

---

## Notes for P5 implementation

- Translate to ES + FR per `BRAND_SPANISH_PATTERNS.md` / `BRAND_FRENCH_PATTERNS.md` voice rules.
- Replace bracketed placeholders with operator-supplied values.
- Page voice tier: Tier-1 academic-formal (legal text always Tier-1).
- Counsel review **before** publication is mandatory — privacy policies have legal weight.
- Cross-link to `/cookies` and `/terms` from this page (existing boilerplate footer already does this; P5 confirms link integrity).
