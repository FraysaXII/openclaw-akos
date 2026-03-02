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

| Operation Type | Approval Required |
|:---------------|:------------------|
| Read-only (file read, web search) | Autonomous |
| File writes, shell execution | Manual confirmation |
| Network downloads | Manual confirmation |
| System configuration changes | Manual confirmation |

### 4. Network Egress Filtering

The gateway daemon binds exclusively to `127.0.0.1:18789`. Remote access is permitted **only** via SSH tunnels or zero-trust mesh networks (e.g., Tailscale). Direct internet exposure is prohibited.

Docker sandboxes restrict outbound traffic to the host loopback interface:

```bash
docker sandbox network proxy openclaw --allow-host localhost
```

### 5. SOC Monitoring

All gateway logs are emitted in structured JSON and can be monitored through two complementary channels:

**Live Alert Engine (`akos/alerts.py` + `scripts/log-watcher.py`):**

The log watcher tails the OpenCLAW gateway log in real-time and evaluates each entry against the conditions defined in `config/eval/alerts.json`. Triggered alerts are logged at `CRITICAL` level and can be forwarded to Langfuse for tracing. Start with: `python scripts/log-watcher.py`

**Splunk SIEM (for enterprise deployments):**

Structured JSON logs can also be forwarded to Splunk via `config/splunk/inputs.conf` for SOC-level anomaly detection dashboards.

**High-priority alert triggers** (defined in `config/eval/alerts.json`):
- Execution of `chmod` commands (real-time, critical)
- Access to `/etc/` or `~/.ssh/` directories (real-time, critical)
- Invocation of `canvas_eval` JavaScript primitive (real-time, high)
- Prompt injection detection (continuous, critical)
- Completion rate drops below baseline (7d window, high)

### 6. EU AI Act 2026 Compliance

- **Automated Record-Keeping:** Full trace logging of prompts, tool calls, and outputs
- **Human Oversight:** HITL gates for all state-mutating operations
- **Risk Management:** Continuous `skillvet` auditing and prompt-injection vulnerability monitoring

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainer directly or use GitHub's private vulnerability reporting feature
3. Include a clear description, reproduction steps, and potential impact assessment

We aim to acknowledge reports within 48 hours and provide a fix or mitigation within 7 days.

## Supported Versions

| Version | Supported |
|:--------|:----------|
| 2.0.x   | Yes       |
| < 2.0   | No        |
