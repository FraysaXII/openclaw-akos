# Stripe and billing — two planes

| Plane | Schema | Purpose |
|-------|--------|---------|
| **KiRBe SaaS** | `kirbe.*` (`subscriptions`, `invoice_items`, …) | Tentative **KiRBe product** SaaS |
| **Holistika company** | `holistika_ops` (or chosen name) | **Company** CRM/ERP revenue, partners, internal commercial ops |

**Process anchor:** [`thi_finan_dtp_261`](../../../references/hlk/compliance/process_list.csv).

**Rule:** Do not mix Holistika company billing rows into `kirbe.*` unless the record is explicitly a KiRBe customer subscription.

**Webhook routing (Wave B3):** [`supabase/functions/stripe-webhook-handler/README.md`](../../../../../supabase/functions/stripe-webhook-handler/README.md) — `metadata.hlk_billing_plane` distinguishes planes (legacy `akos_billing_plane` still honored).
