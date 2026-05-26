# AGENTS.md

## Cursor Cloud specific instructions

### Runtime environment

- **Python**: Use `python3.13` (installed from deadsnakes PPA). The system default `python3` is 3.12 which cannot satisfy `scipy>=2.4.4`. Always invoke as `python3.13` or set PATH appropriately.
- **PATH**: Add `/home/ubuntu/.local/bin` to PATH before running any pip-installed CLI tools (pytest, fastapi, streamlit, etc.).
- **Node.js**: v22 is available system-wide. `npm install` in repo root provides the Supabase CLI (`npx supabase`).

### Running the application

- **API server**: `python3.13 scripts/serve-api.py --port 8420` starts the FastAPI control plane. Health: `GET /health`. Agents: `GET /agents`. HLK queries: `GET /hlk/roles`, `GET /hlk/processes`.
- The OpenClaw gateway, Ollama, Neo4j, and Langfuse are **optional** for development. The API server, tests, and validators all run without them.
- The `check-drift.py` script will report `missing_workspace` and `missing_openclaw_config` drift in Cloud Agent VMs — this is expected and non-blocking for development.

### Testing

- **Full suite**: `python3.13 -m pytest tests/ -q` (~2400 tests, ~36s)
- **Targeted groups**: `python3.13 scripts/test.py <group>` (run `--list` for options)
- **HLK validator**: `python3.13 scripts/validate_hlk.py` (must PASS before commits touching compliance CSVs)
- **Release gate**: `python3.13 scripts/release-gate.py` (runs all validators; one pre-existing FAIL on BRAND vision drift is known)
- See `README.md` §"Running Tests" and `docs/DEVELOPER_CHECKLIST.md` for the full verification matrix.

### Gotchas

- `scipy>=2.4.4` in `requirements.txt` requires Python 3.13+. The latest available scipy on 3.12 is 1.17.x. Installing all other deps first then `pip install scipy` (without version pin) works as a fallback — the graph explorer layout features degrade gracefully.
- Some test failures (~18 of 2460) are pre-existing and relate to optional features (PDF rendering via WeasyPrint, Docker probes, eval cassette replays). These are not caused by the dev environment setup.
- The `release-gate.py` single FAIL (`BRAND vision drift`) is a pre-existing repo issue, not an environment problem.
