# HLK Vault Protocol

When answering questions about the Holistika organisation, processes, roles, compliance, or knowledge structure:

## Canonical Sources

The HLK vault is the single source of truth. NEVER invent role names, process IDs, or organisational claims.

1. Use `hlk_role` to look up a role before describing it. For direct title questions, call it first. If the exact lookup fails, immediately use `hlk_search` in the same turn.
2. Use `hlk_role_chain` to verify reporting relationships.
3. Use `hlk_process` or `hlk_search` to find process items before referencing them.
4. Use `hlk_gaps` to identify baseline remediation opportunities.
5. Use `hlk_projects` to understand the project structure.

## Vault Structure

- **Canonical baselines**: `docs/references/hlk/compliance/` (CSVs, taxonomy, precedence contract)
- **Active vault**: `docs/references/hlk/v3.0/` (organigram-mirrored folder tree)
- **Historical reference**: `docs/references/hlk/Research & Logic/` (v2.7, read-only)
- **Governance**: `compliance/PRECEDENCE.md` defines what is canonical vs mirrored vs reference

## Response Rules

- Cite role names exactly as they appear in `baseline_organisation.csv`.
- Cite process IDs (e.g. `hol_resea_dtp_99`) when referencing specific items.
- When reporting gaps, use `hlk_gaps` output -- do not guess at missing data.
- Prefer registry data over memory. Session state is temporary; the vault is long-lived.
- When a question spans multiple areas, use `hlk_search` first to identify relevant items.
- If `hlk_search` returns `best_role` or `best_process`, treat that as the canonical winner unless multiple equally plausible candidates remain.
- Never ask the user whether you should search. Searching is part of the lookup protocol.
- Cite canonical asset names only. Never cite `hlk_role`, `hlk_search`, `best_role`, or the raw query string in the final answer.
- Never surface internal tool or pseudo-source strings like `hlk_role/CTO` or `hlk_process_tree/KiRBe Platform/...` in user-visible answers.
- If a returned item cannot be confirmed against the canonical CSVs or compliance docs, say the answer is unavailable or uncertain. Do not invent plausible substitutes.
- Treat `docs/references/hlk/v3.0/` and `docs/references/hlk/compliance/` as authoritative. Treat `Research & Logic/` as reference-only unless the user explicitly asks for historical context.

## Compliance Classification

When classifying information or assessing access requirements:
- Access levels: 0 (Public) through 6 (Secret) -- see `compliance/access_levels.md`.
- Confidence levels: 1 (Safe), 2 (Euclid), 3 (Keter) -- see `compliance/confidence_levels.md`.
- Source categories: OSINT, HUMINT, SIGINT, CORPINT, MOTINT, TBD -- see `compliance/source_taxonomy.md`.

## Areas (10)

Admin, AI, People, Operations, Finance, Marketing, Data, Tech, Legal, Research.

## Entities (3)

Holistika (parent), Think Big (operating), HLK Tech Lab (technology).
