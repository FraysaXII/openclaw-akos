# Intent benchmark — after (Initiative 13)

**Date:** 2026-04-17  
**Command:** `py scripts/intent_benchmark.py` (repo root)  
**Environment:** Windows; Ollama embeddings available (`method` = `embedding` where shown).

SOC: no secrets; queries are test phrases only.

| id | regex_route | full_route | method |
|:---|:------------|:-------------|:-------|
| hlk_acronym_pmo | hlk_lookup | hlk_lookup | embedding |
| hlk_acronym_dri | hlk_lookup | hlk_lookup | embedding |
| hlk_search_acronym | hlk_search | hlk_search | embedding |
| hlk_lookup_disambiguate_role | hlk_lookup | hlk_lookup | embedding |
| other_clarify_no_hlk_token | other | other | embedding |
| standup_still_other | other | other | embedding |
| admin_still_escalates | admin_escalate | admin_escalate | embedding+escalation_regex |
| exec_still_escalates | execution_escalate | execution_escalate | embedding+escalation_regex |

**Baseline:** Capture a sibling `intent-benchmark-<date>-baseline.md` before exemplar changes on the parent commit when comparing tuning iterations.
