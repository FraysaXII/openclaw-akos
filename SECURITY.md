# Security Policy

## Threat Model

OpenCLAW-AKOS deploys an autonomous agent with filesystem access, authenticated API credentials, and shell execution capabilities. This introduces **insider threat dynamics** equivalent to granting a new employee full workstation access on day one.

### Known Active Threats

- **ClawHavoc Campaign** — Distributed Atomic Stealer (AMOS) malware via 341+ malicious ClawHub skills masquerading as legitimate tools ([ESecurity Planet](https://www.esecurityplanet.com/threats/hundreds-of-malicious-skills-found-in-openclaws-clawhub/), [The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html))
- **CVE-2026-24763** — Command injection vulnerability in OpenCLAW gateway ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-24763))
- **ClickFix Social Engineering** — Prompt-injection payloads disguised as community skills

## Mandatory Security Controls

### 1. Execution Isolation

The agent **must never** run on bare metal. All deployments require:

- **Windows:** WSL2 with a dedicated `openclaw` service account (non-root)
- **macOS / Linux:** Docker Sandbox with network proxy restricted to `localhost`

API keys are injected via the Docker sandbox proxy — the agent process never has direct read access to raw cryptographic material.

### 2. Pre-Execution Skill Auditing

**Never** install community skills directly from ClawHub without prior verification.

```bash
# Always use the safe-install wrapper (repo-level convenience script)
bash scripts/vet-install.sh <skill-slug>

# Or call the underlying skillvet scanner directly
bash skills/skillvet/scripts/safe-install.sh <skill-slug>
```

The `skillvet` scanner performs 48 vulnerability checks:
- Obfuscated base64 payloads
- Unauthorized `curl`/`wget` commands
- Credential harvesting patterns
- ClawHavoc and ClickFix campaign signatures
- Prompt-injection vectors

### 3. Human-in-the-Loop (HITL) Enforcement

The full tool classification is maintained in `config/permissions.json` (36 autonomous, 33 approval-gated tool IDs in the current branch, spanning gateway core IDs, MCP plugin IDs, and AKOS logical aliases).

| Operation Type | Approval Required |
|:---------------|:------------------|
| Read-only (file read, web search, memory retrieval) | Autonomous |
| File writes, shell execution | Manual confirmation |
| Network downloads, HTTP POST | Manual confirmation |
| Memory writes, filesystem writes | Manual confirmation |
| System configuration changes | Manual confirmation |
| Browser JS eval (`browser_console_exec`) | Manual confirmation |

The Orchestrator assigns HITL gates per task in the Delegation Plan. The Executor enforces them before every action. The Verifier operates independently as a quality gate with a 3-attempt error recovery limit.

### 4. Network Egress Filtering

The gateway daemon binds exclusively to `127.0.0.1:18789`. Remote access is permitted **only** via SSH tunnels or zero-trust mesh networks (e.g., Tailscale). Direct internet exposure is prohibited.

Docker sandboxes restrict outbound traffic to the host loopback interface:

```bash
docker sandbox network proxy openclaw --allow-host localhost
```

### 4a. Optional Neo4j HLK graph mirror

When enabled, `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD` must live in **`~/.openclaw/.env`** (or process env) alongside other operator secrets—never commit them. The graph database is a **read-optimized mirror** of canonical CSVs and validated vault markdown; treat compromise of Neo4j credentials as exposure of **internal organisational structure** metadata, not as a substitute for vault write controls. AKOS graph endpoints use **allowlisted** Cypher only; do not expose arbitrary open Cypher to untrusted clients. The operator HTML page `GET /hlk/graph/explorer` loads **vis-network** from a public CDN (jsDelivr); air-gapped or strict CSP deployments should use REST/MCP only or self-host that script. When `scripts/serve-api.py` auto-starts **Streamlit** (`scripts/hlk_graph_explorer.py`), it binds **127.0.0.1** by default—do not use `--open` on shared jump hosts; never pass secrets on the child command line (SOC).

**TLS:** Prefer Aura’s `neo4j+s://` URI with normal system CA trust. Optional `NEO4J_TRUST=all` causes the client to use **`neo4j+ssc` / `bolt+ssc`** semantics (encrypted transport with relaxed server certificate verification). Use only when you understand the MITM risk; fixing corporate CA trust is the safer fix for inspection proxies.

### 5. SOC Monitoring

All gateway logs are emitted in structured JSON and can be monitored through two complementary channels:

**Live Alert Engine (`akos/alerts.py` + `scripts/log-watcher.py`):**

The log watcher tails the OpenCLAW gateway log in real-time, reviews Madeira session transcripts for flagship answer-quality events, and evaluates each entry against the conditions defined in `config/eval/alerts.json`. Triggered alerts are logged at `CRITICAL` level and can be forwarded to Langfuse for tracing. Secrets for this path must live in process env or `~/.openclaw/.env`, never in repo-local `config/eval/*.env` files. Start with: `python scripts/log-watcher.py`

**Splunk SIEM (for enterprise deployments):**

Structured JSON logs can also be forwarded to Splunk via `config/splunk/inputs.conf` for SOC-level anomaly detection dashboards.

**High-priority alert triggers** (defined in `config/eval/alerts.json`):
- Execution of `chmod` commands (real-time, critical)
- Access to `/etc/` or `~/.ssh/` directories (real-time, critical)
- Invocation of `canvas_eval` JavaScript primitive (real-time, high)
- Prompt injection detection (continuous, critical)
- Completion rate drops below baseline (7d window, high)
- Madeira answer-quality grounding signals (real-time, high): `madeira_internal_tool_leak`, `madeira_pseudo_hlk_path_leak`, `madeira_suspect_uuid_hallucination` — emitted when log-watcher scoring detects leaked tool ids, pseudo HLK paths in user-visible text, or UUID-shaped tokens without `hlk_*` tool use on HLK-classified turns

**OpenClaw security audit:** After gateway or tool-surface changes, operators should run `openclaw security audit` (and `openclaw security audit --deep` when investigating exposure). Full cadence, `--fix`, and incident-style review live in [docs/USER_GUIDE.md](docs/USER_GUIDE.md) — **§14.3 OpenClaw gateway security audit**.

### 5a. Playwright and Browser Smoke (v0.5.0)

The `browser-smoke.py` script and Playwright MCP run in a **sandboxed browser**:

- **browser-smoke.py:** Uses Chromium via `playwright install chromium`. No network egress except to localhost (gateway 18789, API 8420). Optional dependency; CI and developers without Playwright still pass.
- **Playwright MCP (agent runtime):** Same sandbox; agent uses it for Verifier screenshots and DOM interaction. Distinct from `browser-smoke.py` (operator UAT).
- **MCP surface area:** Custom AKOS MCP (`akos_health`, `akos_agents`, `akos_status`), Finance MCP (`finance_quote`, `finance_search`, `finance_sentiment`), and GitHub MCP extend the tool surface. Ensure `GITHUB_TOKEN`, `AKOS_API_URL`, `ALPHA_VANTAGE_KEY`, and `FINNHUB_API_KEY` are not exposed in logs.
- **Finance MCP:** Read-only; no trading, order routing, or account access. `yfinance` is a community scraping library (personal/research use). `ALPHA_VANTAGE_KEY` is optional and stored in `.env` (gitignored). `FINNHUB_API_KEY` is optional and improves symbol search. Quotes are delayed ~15 minutes; the tool surface carries no privileged financial data.

### 5b. Sensitive-Key Schema Signals

AKOS emits path-only schema signals for potentially sensitive config keys through `scripts/doctor.py`.

- **Informational signal:** `[config/schema] info` means the key-path is env-backed (`${VAR}` or `{source: "env", id: ...}`) and no action is required.
- **Actionable signal:** `[config/schema] action` means a sensitive key-path appears non-env-backed and should be migrated to an env reference or secret manager.
- **Redaction rule:** Logs show key-paths only. Secret values must never be printed or persisted in diagnostic output.

Run `py scripts/doctor.py` after config changes and treat actionable signals as remediation tasks before release.

### 6. RunPod Infrastructure Security (v0.3.0)

When using the `gpu-runpod` environment:

- `RUNPOD_API_KEY` is stored in a `.env` file (gitignored), never committed.
- The RunPod provider (`akos/runpod_provider.py`) degrades to a no-op when the API key is absent.
- Endpoint health is monitored every 60 seconds by `log-watcher.py` and traced to Langfuse.
- The FastAPI control plane binds to `127.0.0.1` by default. Do not expose to the public internet without a reverse proxy and authentication.

### 6a. Dedicated Pod Security (gpu-runpod-pod)

When using dedicated RunPod pods (`gpu-runpod-pod` profile), the vLLM process runs on a persistent machine with different security characteristics than serverless endpoints:

- **Exposed ports:** The pod exposes port 8000 (vLLM) and optionally port 22 (SSH) via RunPod's HTTPS proxy (`{pod_id}-{port}.proxy.runpod.net`). Access is authenticated by RunPod's proxy layer, but operators should treat pod URLs as sensitive — do not embed them in client-side code or public configs.
- **SSH access:** Pods with SSH enabled allow direct shell access. Restrict SSH key distribution to infrastructure operators. Never store SSH keys in this repo or in `.env` files that may be shared.
- **SSRF considerations:** Direct pod URLs bypass RunPod's serverless request validation. If `VLLM_RUNPOD_URL` is user-controllable or logged in full, it could be leveraged for SSRF against RunPod's internal network. Always validate and sanitize the URL. The `/openai/v1` suffix is enforced at config time.
- **Pod lifecycle:** Unlike serverless endpoints, dedicated pods do not auto-scale to zero. Unattended pods continue billing and remain reachable. Use `setup-runpod-pod.py` for provisioning and ensure pods are stopped when not in use.
- **Health probe surface:** `probe_vllm_health()` issues HTTP GETs to the pod URL. Ensure the probe target is always an operator-configured value from `.env`, never derived from untrusted input.

### 7. EU AI Act 2026 Compliance

- **Automated Record-Keeping:** Full trace logging of prompts, tool calls, and outputs; RunPod health traces; workspace checkpoints for reversibility
- **Human Oversight:** HITL gates for all state-mutating operations; Orchestrator delegation with per-task HITL gates; Verifier independent quality validation
- **Risk Management:** Continuous `skillvet` auditing, prompt-injection vulnerability monitoring, Verifier quality gate with 3-attempt error recovery limit

### 8. Gateway-Level Capability Enforcement (v0.5.0)

AKOS v0.5.0 adds **gateway-level capability enforcement** as defense-in-depth on top of prompt-level controls.

- **Per-agent tool profiles** — The OpenClaw gateway enforces `tools.profile` plus curated `alsoAllow` / `deny` lists per agent. Madeira uses `minimal` with curated `read`, memory, HLK/finance lookups, **read-only** browser observation tools (`browser_snapshot`, `browser_screenshot` in `alsoAllow`), explicit `deny` for write/edit/apply_patch/exec, and **no** coarse `browser` token (navigate/click/type remain off-template). Orchestrator and Architect use `minimal` with curated read-only extras; Executor and Verifier use `coding` and expose the coarse `browser` class for full validation flows (Verifier still denies write/edit/apply_patch). Even if an agent is prompt-injected, the gateway blocks unauthorized tool calls.
- **Exec security mode** — `tools.exec.security` restricts shell execution (deny/allowlist/full). Orchestrator and Architect must not have `full` exec; bootstrap and drift detection enforce this.
- **Browser SSRF policy** — `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork: false` prevents browser automation from accessing private/internal networks. Reduces SSRF risk from malicious web content.

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainer directly or use GitHub's private vulnerability reporting feature
3. Include a clear description, reproduction steps, and potential impact assessment

We aim to acknowledge reports within 48 hours and provide a fix or mitigation within 7 days.

## Supported Versions

| Version | Supported |
|:--------|:----------|
| 0.5.x   | Yes       |
| 0.4.x   | Yes       |
| 0.3.x   | Yes       |
| 0.2.x   | Yes       |
| < 0.2   | No        |
