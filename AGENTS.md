# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

OpenCLAW-AKOS is a Python 3.10+ orchestration framework with a FastAPI control plane API. See `README.md` for full details.

### Key commands

- **Install deps:** `pip install -r requirements.txt`
- **Run tests:** `python3 -m pytest -v` (206 tests; 1 pre-existing failure on Linux due to `py` alias usage in `test_assemble_prompts_default`)
- **Run test groups:** `python3 scripts/test.py <group>` (use `--list` to see groups)
- **Start API server:** `python3 scripts/serve-api.py --port 8420` (Swagger UI at `/docs`)
- **Health check:** `curl http://127.0.0.1:8420/health`

### Non-obvious caveats

- Scripts installed by pip (pytest, uvicorn, playwright, etc.) land in `~/.local/bin`. Ensure `PATH` includes `$HOME/.local/bin` or invoke via `python3 -m <tool>`.
- The `py` command (Windows Python launcher alias) does not exist on Linux. One test (`test_assemble_prompts_default`) fails because it shells out to `py`. This is a pre-existing issue, not a setup problem.
- The bootstrap script (`scripts/bootstrap.py`) requires Ollama running locally and is not needed for running tests or the API server. Tests are fully offline (mocked dependencies).
- Live smoke tests behind `@pytest.mark.live` require `AKOS_LIVE_SMOKE=1` and a running API server; they are skipped by default.
- Optional services (Ollama, OpenCLAW gateway, RunPod, Langfuse) degrade gracefully when unavailable — the API and tests work without them.
- Node.js >= 22 is required by MCP server integrations (via `npx`) but not for running tests or the API server itself.
