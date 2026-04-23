# Initiative 19 — SQL proposal Phase 1 (2026-04-23)

## Scope

- **Schema:** `finops`
- **Table:** `finops.registered_fact` (UUID PK, `counterparty_id`, optional Stripe ids, `fact_type`, `currency`, optional `amount_minor`, `effective_date`, `metadata` JSONB, `source_reference`, `created_at`)
- **Indexes:** `counterparty_id`, partial on `stripe_customer_id`, `fact_type`
- **RLS:** deny `anon` / `authenticated`; grant `service_role` ALL on table

## Rollback

- `DROP TABLE finops.registered_fact`; `DROP SCHEMA finops` (Phase 1 only — revise if later objects added)

## PII / SOC

- No raw card data; amounts are optional minor units; Stripe ids are identifiers — treat as sensitive in application logs.

## Approval

- Recorded in [decision-log.md](../decision-log.md) (D-19-1–D-19-3).
