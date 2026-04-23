# Initiative 19 — Decision log

## D-19-1 — Phase 1 table shape

**Decision:** Introduce **`finops.registered_fact`** as a single flexible fact row keyed by **`counterparty_id`** (text slug aligned with `FINOPS_COUNTERPARTY_REGISTER.csv`) plus optional Stripe identifiers and **`fact_type`** text discriminator.

**Rationale:** Avoids premature normalization (many narrow tables) while giving a first-class home for ledger-shaped data; Phase 2 can split by `fact_type` if volume warrants.

## D-19-2 — No FK to compliance mirror

**Decision:** **`counterparty_id`** is **not** a foreign key to `compliance.finops_counterparty_register_mirror`.

**Rationale:** Matches Initiative 18 bridge pattern — git CSV is authoritative; mirror is a projection; ledger facts remain valid even if mirror sync lags.

## D-19-3 — RLS posture

**Decision:** Same deny-all for `anon` / `authenticated` as compliance mirrors; **`service_role`** owns DML.

**Rationale:** Financial facts are not browser-key surfaces; keeps PostgREST exposure safe by default.

## D-19-4 — Supersede Initiative 18 Phase C deferral

**Decision:** Initiative 18 **D-18-4** (“no Phase C monetary DDL”) is **superseded** for execution purposes by this initiative; the CFO/Legal gate (`thi_finan_dtp_306`) still governs **what** may be loaded into `registered_fact`, not whether the **schema** may exist.

**Rationale:** Schema-first removes the governance gap between metadata mirror and ad-hoc tables; content remains policy-gated.
