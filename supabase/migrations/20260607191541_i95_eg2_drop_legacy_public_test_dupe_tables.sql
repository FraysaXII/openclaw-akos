-- I95 EG-2 (D-IH-95-G / DB-02): drop verified-dead KiRBe-era test + duplicate tables.
-- Applied to remote MasterData (swrmqpelgoblaquequzb) via MCP apply_migration on 2026-06-07.
-- Pre-checked: no FK references, no view dependencies. service_role/AKOS backend unaffected.
-- Part of the Supabase ecosystem-governance closure (SUPABASE_ECOSYSTEM_GOVERNANCE.md, SUPA-MOD-09).
DROP TABLE IF EXISTS public."Process list";
DROP TABLE IF EXISTS public."Test access";
DROP TABLE IF EXISTS public.test_aapl;
DROP TABLE IF EXISTS public.test_clients;
DROP TABLE IF EXISTS public.test_contract;
DROP TABLE IF EXISTS public.test_process;
DROP TABLE IF EXISTS public.test_product;
DROP TABLE IF EXISTS public.example_csv;
DROP TABLE IF EXISTS public.document_vectors;
DROP TABLE IF EXISTS public.users2;
