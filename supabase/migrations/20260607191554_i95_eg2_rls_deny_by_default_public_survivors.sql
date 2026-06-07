-- I95 EG-2 (D-IH-95-G / DB-03): enable RLS deny-by-default on surviving KiRBe-era public tables.
-- Applied to remote MasterData (swrmqpelgoblaquequzb) via MCP apply_migration on 2026-06-07.
-- RLS-enabled with no policy = anon/authenticated denied; service_role (AKOS backend) bypasses RLS.
-- Closes the critical 'rls_disabled' advisory (16 -> 0). Reversible (ALTER TABLE ... DISABLE ROW LEVEL SECURITY).
ALTER TABLE public.agent_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.components ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.data_document_vectors ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.data_madeira_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.function_calls ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.madeira_document_store ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.madeira_index_store ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.monitoring_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.special_processes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rag_2 ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workstreams ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.data_kirbe_document_vectors_1536 ENABLE ROW LEVEL SECURITY;
