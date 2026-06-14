# I99 — Risk Register

| ID | Risk | L | I | Mitigation |
|:---|:---|:---|:---|:---|
| R-IH-99-1 | Dashboard module ON without registry row | H | H | EG-5 tranche; module registry SSOT |
| R-IH-99-2 | MCP mistaken for mutation authority | M | H | Two-plane doctrine in master-roadmap; operator SQL gate |
| R-IH-99-3 | I96 auth UAT friction continues if Auth deferred | M | M | I96 named first consumer; P2 priority |
| R-IH-99-4 | CSV tranche without SOP-META ordering | L | H | P5 AskQuestion; process rows before SOP promotion |
| R-IH-99-5 | Prod schema/mirror lag before new modules | M | H | P1 reconcile; `supabase/migrations/README.md` prod catch-up |
