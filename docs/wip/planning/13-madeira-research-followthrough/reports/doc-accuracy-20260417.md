# Doc accuracy — claim vs config (Initiative 13)

**Date:** 2026-04-17  
**Purpose:** Before/after checklist for verbose defaults and Ollama `num_ctx` guidance.

| Claim (USER_GUIDE / ARCHITECTURE) | Source of truth | After (pass) |
|:----------------------------------|:----------------|:-------------|
| `verboseDefault: "on"` recommended when tool visibility is needed | `docs/ARCHITECTURE.md` Config: `verboseDefault`; `config/openclaw.json.example` pattern | pass — aligned |
| Ollama defaults to `num_ctx=4096` unless Modelfile overrides | Ollama upstream behavior; `docs/ARCHITECTURE.md` § Ollama `num_ctx` | pass — aligned |
| Committed Modelfiles set `num_ctx` to match tier budgets | `config/ollama/` Modelfiles; `config/model-tiers.json` `contextBudget` | pass — aligned |
| `/verbose` overrides session tool visibility | `docs/ARCHITECTURE.md` § Config: verboseDefault | pass — aligned |

**Note:** No prose change required for the above in this initiative — documentation already matched SSOT. USER_GUIDE §5.2 and troubleshooting §Ollama remain the operator entrypoints.
