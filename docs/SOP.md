# **Standard Operating Procedure: Upgrading OpenCLAW to an Enterprise-Grade Large Language Model Operating System (LLMOS)**

## **Document Metadata and Governance**

| Attribute | Specification |
| :---- | :---- |
| **Item Name** | Standard Operating Procedure for OpenCLAW LLMOS Transformation |
| **Item Number** | SOP-OPENCLAW\_LLMOS\_UPGRADE\_002 |
| **Object Class** | Advanced Engineering Procedure & Architectural Guideline |
| **Confidence Level** | High |
| **Security Level** | 2 (Internal Systems Engineering & SOC Operations) |
| **Entity Owner** | Enterprise Architecture & AI Infrastructure |
| **Associated Workstream** | Autonomous Agent Governance, DX Optimization, and Knowledge Management |
| **Version & Revision Date** | 4.0 — March 2026 |

## **1.0 Executive Summary and Architectural Vision**

The contemporary landscape of autonomous software systems has shifted dramatically, moving rapidly from conversational interfaces to deep-execution architectures. Out-of-the-box, vanilla deployments of the OpenCLAW framework operate fundamentally as isolated, high-latency conversational agents. While they possess basic utility, they lack the persistent identity, deterministic workflow orchestration, and cognitive depth required to match sophisticated internal frameworks like the Kirbe Agentic Knowledge Operating System (AKOS) or proprietary solutions such as Gemini Deep Research and Cursor's dual-mode IDE planners.1

The analysis indicates that achieving an enterprise-grade, highly autonomous assistant requires transcending the concept of a rudimentary "chatbot" and architecting a Large Language Model Operating System (LLMOS). This transformation necessitates the integration of the Four-Layer LLMOS paradigm: a Control Plane (Gateway), an Integration Layer, an Execution Layer (Agent Runner), and an Intelligence Layer.1 When an agent is forced to simultaneously architect a solution and write the underlying syntax, it suffers from severe cognitive overload. This results in context degradation, systemic hallucinations, and infinite debugging loops.1 To overcome this, the architecture embraces a multi-agent paradigm (v3.0: four agents), separating the cognitive workload into an "Orchestrator" (task decomposition and delegation), an "Architect" (read-only, high-context planning), an "Executor" (fast, read-write execution of strict directives), and a "Verifier" (independent quality validation with error recovery).1

Furthermore, the introduction of the Model Context Protocol (MCP) serves as the universal integration layer for this ecosystem, replacing brittle, bespoke API wrappers with standardized, discoverable tool schemas.4 By standardizing how models interact with external data sources, the agent can achieve exhaustive, multi-layered research capabilities.1

However, expanding an agent's capabilities to include filesystem access, continuous background processing, and deep browser automation introduces severe existential security risks. The discovery of the ClawHavoc campaign, which successfully distributed the Atomic Stealer (AMOS) malware via malicious ClawHub skills, dictates that a Zero-Trust, highly sandboxed operational posture is strictly mandatory.6

This Standard Operating Procedure (SOP) provides the exhaustive, step-by-step technical blueprints required to upgrade a vanilla OpenCLAW instance into a secure, modular, and deeply integrated LLMOS. It incorporates comprehensive Data Integration (DI) frameworks modeled on the Holistika intelligence methodology 8, Security Operations Center (SOC) logging protocols 10, Developer Experience (DX) evaluation metrics 11, and EU AI Act compliance mechanisms designed for the 2026 regulatory environment.12

## **2.0 The Holistika Methodological Trinity applied to Agentic Architecture**

The transformation of a vanilla OpenCLAW instance requires grounding the technical deployment in a robust business logic framework. Based on the Holistika corporate intelligence methodology, operational efficiency is contingent upon a deep understanding of the underlying logic governing the entity.9 For an AI agent to function as a corporate asset rather than a novelty, its architecture must reflect the "Methodological Trinity": Strategy, Tactics, and Processes.2

### **2.1 Strategy: The Agentic Knowledge Operating System (AKOS)**

The primary responsibility of the enterprise architecture is to define the agent's strategic direction. A vanilla OpenCLAW deployment acts as a passive responder; an upgraded LLMOS must act as an active participant.2 This is achieved by evolving the agent into an Agentic Knowledge Operating System (AKOS).2 The strategy dictates that the agent must not merely retrieve data, but must validate that data against defined methodologies, acting effectively as an automated consultant.2

This strategic layer is technically enforced through "Strict Mode" Logic and Data Governance frameworks.1 Recent industry demands for comprehensive data governance—including the structuring of Critical Data Elements (CDEs), data lineage coordination, and cross-functional alignment—highlight the necessity of moving beyond unstructured data retrieval.13 The agent's memory must utilize a structured recall mechanism that enforces confidence thresholds, ensuring the AI only commits facts that possess a verifiable "Source of Truth" (SSOT).2 As of v3.0, this is implemented via a flat memory architecture (MCP Memory server for cross-session key-value recall, workspace files, context compression, and Langfuse traces) rather than a full GraphRAG, which was evaluated and rejected for its complexity-to-value ratio.

### **2.2 Tactics: The Intelligence Matrix and Data Integration (DI)**

Tactics represent the limited, finite objectives executed to achieve the broader strategy.9 Within the OpenCLAW upgrade, the tactical layer is governed by the "Intelligence Matrix," an analytical tool used to classify information based on nature, source, security level, and intended use.14

To achieve "Deep Research" parity with commercial models, the OpenCLAW agent must be configured to process ingested data through a structured matrix. The system must programmatically assign attributes to ingested files and web scrapes, including:

* **Fact ID:** A unique identifier for every isolated concept (e.g., fct\_001).8  
* **Source Credibility:** A numerical score comparing the source to an average baseline.8  
* **Direct and Indirect Impact Analysis:** Quantitative scoring used by the reasoning engine to prioritize context.8  
* **Generational Filters and PESTEL:** Analytical frameworks applied dynamically to the data to understand nuanced behaviors and strategic trends.14

### **2.3 Processes: Modular Execution via MCP**

Processes represent the granular execution of tactics.9 OpenCLAW's process layer is entirely revolutionized by the Model Context Protocol (MCP).5 The capability to audit processes, interface with APIs, and manipulate the host system is externalized into dedicated MCP servers. This ensures that the core reasoning engine remains agnostic to the underlying infrastructure, capable of calling specialized tools for codebase auditing, browser automation, or structured sequential thinking without requiring hardcoded integrations.4

## **3.0 Foundational Environment Provisioning and Sandboxing**

Deploying an autonomous agent with broad filesystem and network access directly onto a host operating system violates the foundational principle of least privilege. OpenCLAW must be constrained within a strict execution boundary. The architecture creates a "digital accomplice" that inherits the privileges of the host machine.1 Without sandboxing, a single vulnerability, such as a command injection flaw, results in total systemic compromise.16 Therefore, operating system-specific isolation strategies must be executed before any gateway daemon is initialized.

### **3.1 Windows Deployment via WSL2 (Strict Enforcement)**

Native Windows PowerShell installations of OpenCLAW are highly problematic. They frequently suffer from the absence of systemd, dependency failures, and network port binding issues that cripple the gateway's stability.18 Consequently, Windows environments must utilize the Windows Subsystem for Linux (WSL2) to provide a stable, containerized Ubuntu environment that supports standard Linux daemon management.18

**Step-by-Step Procedure:**

1. **Initialize WSL2:** Open an elevated PowerShell terminal (Run as Administrator) and execute the installation command for the specific 2024 LTS distribution to guarantee compatibility: wsl \--install \-d Ubuntu-24.04.18 If WSL is already present but requires the specific distribution, use wsl \--install \--web-download \-d Ubuntu-24.04 to force the package retrieval.20  
2. **Enable Systemd:** Once the Ubuntu terminal is accessible, systemd must be explicitly enabled to allow the OpenCLAW daemon to run persistently in the background. Execute the following block within the WSL terminal: sudo tee /etc/wsl.conf \>/dev/null \<\<'EOF' \[boot\] systemd=true EOF.18  
3. **Reboot Subsystem:** Terminate the instance from the native Windows PowerShell to apply the boot configuration changes: wsl \--shutdown.18  
4. **Dedicated User Creation:** Never run the agent as the root user. Within the restarted WSL2 environment, create a dedicated, non-privileged service account. This ensures that if the agent is compromised, the attacker only inherits the openclaw user permissions: sudo adduser \--system \--group openclaw sudo mkdir /opt/openclaw sudo chown openclaw:openclaw /opt/openclaw.17  
5. **Install OpenCLAW CLI:** Switch to the newly created openclaw user and run the installation script: curl \-fsSL https://molt.bot/install.sh | bash.18 (Note: OpenCLAW legacy domains are still utilized for binary distribution, reflecting the project's rapid naming evolution from Clawdbot to Moltbot to OpenCLAW 4).

### **3.2 macOS and Linux Deployment via Docker Sandboxes**

For macOS and native Linux systems, the optimal security posture leverages Docker Sandboxes. This primitive allows the agent to run in an isolated micro-VM while utilizing a network proxy to deny connections to arbitrary internet hosts. Crucially, it injects API keys securely without exposing them to the agent's filesystem, neutralizing the threat of credential harvesting via prompt injection.22

**Step-by-Step Procedure:**

1. **Verify Host Requirements:** Ensure Docker Desktop is installed and the Docker Model Runner feature is enabled via the application interface (Settings → Docker Model Runner → Enable).22  
2. **Model Retrieval:** Pull the necessary local model weights to the host machine to support offline inference capabilities: docker model pull ai/gpt-oss:20B-UD-Q4\_K\_XL.22  
3. **Create the Sandbox:** Provision the isolated environment using the pre-built OpenCLAW image tailored for the Docker Model Runner bridge: docker sandbox create \--name openclaw \-t olegselajev241/openclaw-dmr:latest shell.22  
4. **Configure Network Proxy:** Restrict the sandbox to communicate only with the host's loopback interface. This guarantees the agent cannot exfiltrate data to external command-and-control servers unless explicitly authorized: docker sandbox network proxy openclaw \--allow-host localhost.22  
5. **Execute the Gateway:** Launch the sandbox and start the initialization script within the container's shell: docker sandbox run openclaw \~/start-openclaw.sh.22  
6. **Credential Management Configuration:** Do not place API keys inside the openclaw.json file within the container. Instead, set ANTHROPIC\_API\_KEY or OPENAI\_API\_KEY in the host machine's environment. The Docker sandbox proxy will automatically intercept outgoing requests to major provider domains and inject these keys into the authorization headers. This ensures the agent process never has direct read access to the raw cryptographic material.22

## **4.0 Core Configuration and the Four-Layer LLMOS Paradigm**

The transition from a basic agent to an LLMOS requires decoupling the reasoning engine from its tools and channels. The architecture relies on four distinct functional domains: the Gateway (Control Plane), the Integration Layer (Channel Adapters), the Execution Layer (Agent Runner), and the Intelligence Layer.1

### **4.1 Initializing the Gateway Config (openclaw.json)**

The central nervous system of the deployment is the openclaw.json file, typically located at \~/.openclaw/openclaw.json.23 The file must define the LLM provider, establish the local API bindings, and map the mcpServers object.

**Step-by-Step Procedure:**

1. **Bootstrap the Configuration:** Run the setup wizard to generate the base schema and install the gateway as a system daemon (launchd/systemd): openclaw onboard \--install-daemon.24  
2. **Bind to Localhost:** To prevent unauthorized lateral network movement, ensure the gateway daemon only listens on the local interface. The gateway must never be exposed directly to the open internet; remote access should be handled via SSH tunnels or zero-trust mesh networks like Tailscale.1 Verify binding using: netstat \-an | grep 18789 | grep LISTEN.25  
3. **Define Agent Routing:** Configure the openclaw.json to define agents and bind them to workspaces. This isolation ensures that casual messages do not pollute the context window of an agent performing intensive codebase analysis.  

   > **Note (v2026.2.26):** The `workspaces` key shown in earlier drafts is **not supported** by the current OpenCLAW schema. The correct approach uses `agents.list` entries with per-agent `workspace` paths and optional `bindings`. See the `config/openclaw.json.example` for the canonical template.

   Modify \~/.openclaw/openclaw.json to include (v3.0 four-agent model):  
   JSON  
   {  
     "gateway": {  
       "port": 18789,  
       "host": "127.0.0.1"  
     },  
     "agents": {  
       "defaults": { "model": { "primary": "ollama/qwen3:8b" } },  
       "list": \[  
         { "id": "orchestrator", "name": "Orchestrator", "workspace": "\~/.openclaw/workspace-orchestrator" },  
         { "id": "architect", "name": "Architect", "workspace": "\~/.openclaw/workspace-architect" },  
         { "id": "executor", "name": "Executor", "workspace": "\~/.openclaw/workspace-executor" },  
         { "id": "verifier", "name": "Verifier", "workspace": "\~/.openclaw/workspace-verifier" }  
       \]  
     }  
   }

4. **Diagnostics:** Run the built-in diagnostic tool to validate syntax and dependencies: openclaw doctor \--fix.25

### **4.2 The A2UI Canvas Integration**

To emulate the sophisticated interfaces of modern proprietary tools, the LLMOS must move beyond terminal outputs. OpenCLAW supports an Agent-to-UI (A2UI) protocol, allowing the agent to dynamically render interactive web components, charts, and data visualizations directly on a user-facing canvas.26

**Step-by-Step Procedure:**

1. **Canvas Host Verification:** Ensure the gateway is configured to host the Canvas endpoints. Verify the host provides /\_\_openclaw\_\_/canvas/ and /\_\_openclaw\_\_/a2ui/.29  
2. **Enable Companion App:** Launch the macOS or Windows companion app, which embeds the agent‑controlled Canvas panel using a native web view. The state is stored locally, allowing the panel to auto-reload when the agent modifies the local canvas files.28  
3. **Agent Directives:** Instruct the agent via its system prompt to utilize the a2ui\_push command when presenting complex data, rather than printing raw markdown tables into the chat stream.27 The UI is accessed locally via the custom URL scheme openclaw-canvas://main/.28

## **5.0 Model Context Protocol (MCP) Expansion and Data Integration (DI)**

The defining characteristic of an LLMOS is its capability to seamlessly interface with external environments. The Model Context Protocol (MCP) acts as the standardized communication framework, allowing the agent to dynamically discover tools, read schemas, and execute commands.1 This architecture is essential for realizing the "Pincer Effect" described in the Holistika framework—uniting high-level business logic with deep technical data ingestion.9

### **5.1 Deploying the mcporter Skill**

The mcporter skill is the foundational CLI and configuration manager for MCP connections within the OpenCLAW ecosystem. It facilitates direct interactions, handles OAuth flows, and manages server configurations.30

**Step-by-Step Procedure:**

1. **Install the Skill:** Execute the ClawHub package manager to pull the skill into the workspace: npx clawhub@latest install mcporter.21  
2. **Initialize the MCP Configuration:** Create the dedicated configuration directory and file on the host (or within the sandbox): mkdir \-p \~/.mcporter nano \~/.mcporter/mcporter.json.23  
3. **Verify Tool Availability:** Test the installation by querying the CLI to list available servers: mcporter list.30

### **5.2 Implementing "Sequential Thinking" for Deep Research**

A major deficiency of standard agents is their tendency to jump to premature, hallucinated conclusions when faced with complex, multi-step problems.1 To replicate the exhaustiveness of "Deep Research" capabilities, the agent must abandon linear, single-shot generation.

The sequential\_thinking MCP server provides a structured, step-by-step cognitive framework. It forces the model to explicitly define the problem, generate research hypotheses, analyze data, branch into alternative paths, and revise prior assumptions before acting.31 This mirrors the five-stage agentic pattern: Signals, Inference, Adaptation, Feedback, and Guardrails.33

**Step-by-Step Procedure:**

1. **Inject the Server Definition:** Modify the \~/.mcporter/mcporter.json file to include the sequential thinking tool via npx. Ensure Node.js 22 or higher is installed 34:  
   JSON  
   {  
     "mcpServers": {  
       "sequential-thinking": {  
         "command": "npx",  
         "args": \[  
           "-y",  
           "@modelcontextprotocol/server-sequential-thinking"  
         \],  
         "env": {  
           "DISABLE\_THOUGHT\_LOGGING": "false"  
         }  
       }  
     }  
   }

.32 2\. **Define Schema Utilization:** The agent will now have access to the sequential\_thinking tool. The agent's core prompt must be heavily engineered to utilize this tool for every complex query. It must emit its reasoning through specific variables: thought (the current string of logic), thoughtNumber (current index), totalThoughts (estimated iterations), and nextThoughtNeeded (boolean trigger for loop continuation).32 3\. **Implement Course Correction:** Configure the agent's meta-prompt to proactively utilize the isRevision and revisesThought parameters. If the agent encounters a dead end in file processing or web scraping, it must invoke the tool with isRevision: true to flag the anomaly and backtrack its logical tree, simulating human problem-solving and preventing repetitive error loops.32

### **5.3 Implementing Deep Web Automation (Playwright MCP)**

Traditional agents rely on basic HTTP fetching or high-latency screenshot recognition to interact with the web. To achieve true autonomy for OSINT gathering or competitor tracking, the agent requires direct Document Object Model (DOM) level interaction and JavaScript evaluation capabilities.26 The Playwright MCP server provides this capability, exposing a full browser automation lifecycle.36

**Step-by-Step Procedure:**

1. **Inject the Playwright Server:** Add the corresponding definition to the mcpServers configuration block:  
   JSON  
   {  
     "mcpServers": {  
       "playwright": {  
         "command": "npx",  
         "args": \[  
           "-y",  
           "@playwright/mcp@latest",  
           "--output-dir",  
           "/opt/openclaw/workspace/exports"  
         \]  
       }  
     }  
   }

.37 2\. **Tool Exposure:** This integration exposes several deterministic tools to the agent, notably browser\_navigate (loading URLs), element\_interact (clicking/typing based on DOM selectors), browser\_press\_key, and browser\_screenshot.26 3\. **Execution Guardrails:** Because live web environments are hostile, unpredictable, and constantly changing, instruct the agent to always employ a robust wait-and-verify mechanism. The agent must use the browser\_screenshot tool or extract the current DOM state after a browser\_navigate action to verify the page state before attempting to execute any element\_interact commands.36

### **5.4 Codebase Auditing and Integration (GitHub MCP)**

For developer experience workflows, the agent must understand massive codebases without loading the entire repository into a single, expensive context window. The GitHub MCP server provides governed access to repository metadata, file retrieval, and structured code search.15

**Step-by-Step Procedure:**

1. **Subscription Verification:** Ensure the organizational infrastructure supports the API limits required. For example, verifying active GitHub Developer Plan subscriptions (e.g., the $4.00 USD monthly tier) ensures uninterrupted API access.40  
2. **Inject the GitHub Server:** Add the GitHub MCP definition, passing a scoped Personal Access Token (PAT) via environment variables to adhere to least privilege principles.15

### **5.5 Memory, Filesystem, and Fetch MCP Servers (v3.0)**

As of v3.0, three additional MCP servers extend the agent ecosystem beyond the original three (Sequential Thinking, Playwright, GitHub):

* **Memory (`@modelcontextprotocol/server-memory`):** Provides cross-session key-value recall, replacing the previously planned GraphRAG with a simpler, higher-value flat memory architecture. Agents store and retrieve structured facts using `create_memory` and `retrieve_memory` tools.
* **Filesystem (`@modelcontextprotocol/server-filesystem`):** Provides governed filesystem operations with explicit path allowlists. All write operations require HITL approval per `config/permissions.json`.
* **Fetch (`@modelcontextprotocol/server-fetch`):** HTTP client for structured web requests. Replaces ad-hoc `curl` invocations with governed, traceable HTTP operations.

### **5.6 RunPod GPU Integration (v3.0)**

For workloads requiring GPU-accelerated inference (e.g., large reasoning models like DeepSeek-R1-70B), the architecture integrates RunPod serverless endpoints via `akos/runpod_provider.py`. This typed SDK wrapper provides:

* **Idempotent endpoint provisioning** via `ensure_endpoint()`, auto-triggered by `scripts/switch-model.py` when switching to the `gpu-runpod` environment.
* **Health monitoring** integrated into `scripts/log-watcher.py` (60-second intervals, Langfuse traces, SOC alerts on unhealthy status).
* **Scaling controls** via `scale(min_workers, max_workers)` exposed through the FastAPI control plane.
* **Inference** via `infer(prompt, ...)` with configurable timeout, temperature, and max tokens.

Configuration is defined in `config/environments/gpu-runpod.json` and secrets are stored in `.env` files (never committed).

### **5.7 FastAPI Control Plane (v3.0)**

The v3.0 architecture introduces a programmatic API (`akos/api.py`) for system management, exposing 12 REST endpoints:

| Endpoint | Method | Purpose |
| :---- | :---- | :---- |
| `/health` | GET | Liveness probe |
| `/status` | GET | Full system status (agents, model, environment) |
| `/agents` | GET | List registered agents |
| `/switch` | POST | Switch model/environment |
| `/runpod/health` | GET | RunPod endpoint health |
| `/runpod/scale` | POST | Adjust RunPod worker count |
| `/metrics` | GET | DX metrics summary |
| `/alerts` | GET | Active SOC alerts |
| `/prompts/assemble` | POST | Trigger prompt assembly |
| `/checkpoints` | GET/POST | List or create workspace checkpoints |
| `/checkpoints/restore` | POST | Restore a workspace checkpoint |
| `/logs` | WebSocket | Real-time log streaming |

The API is launched via `scripts/serve-api.py` and binds to `127.0.0.1` by default.

## **6.0 Zero-Trust Security and SOC Integration**

Deploying an autonomous entity with filesystem access, authenticated API credentials, and shell execution capabilities introduces severe insider threat dynamics.41 The ecosystem is actively targeted by sophisticated threat actors. The "ClawHavoc" campaign, identified by Koi Security, successfully distributed the Atomic Stealer (AMOS) malware to hundreds of macOS and Windows systems via malicious ClawHub skills masquerading as legitimate tools.6

Security cannot be treated as an afterthought; it must be structurally enforced through pre-execution auditing, strict egress filtering, and comprehensive monitoring integrated directly into a Security Operations Center (SOC).

### **6.1 Pre-Execution Skill Auditing (skillvet)**

Skills in the OpenCLAW ecosystem are fundamentally executable markdown and code folders that inherit the agent's host privileges.1 Never install a community skill directly from ClawHub without prior cryptographic and heuristic verification.

**Step-by-Step Procedure:**

1. **Install the Scanner:** Implement skillvet, a lightweight, dependency-free bash and grep security scanner. It performs 48 critical vulnerability checks, detecting malware, credential theft, data exfiltration, prompt-injection, and campaign-specific signatures (such as those from ClawHavoc and ClickFix).43  
2. **Mandatory Vetting Protocol:** Replace direct clawhub install commands with the safe-install wrapper. This script downloads the skill, audits it for obfuscated base64 payloads or unauthorized curl commands, and automatically removes the payload if critical flags are triggered: bash skills/skillvet/scripts/safe-install.sh \<skill-slug\>.43  
3. **Human-in-the-Loop (HITL) Enforcement:** Within the openclaw.json configuration, enforce HITL policies for all destructive or mutative MCP tools. While read-only operations (e.g., read\_file, web\_search) may execute autonomously, tools mapping to shell execution or system writes must trigger a manual, visual confirmation from the user before execution.1

### **6.2 SIEM Integration (Splunk) for SOC Monitoring**

To detect anomalous agent behavior—such as an agent attempting to parse files outside its designated workspace, making unexpected outbound network requests, or exhibiting signs of prompt-injection hijacking—all OpenCLAW gateway logs must be forwarded to a SIEM platform like Splunk.46

**Step-by-Step Procedure:**

1. **Configure Log Output:** Ensure OpenCLAW is configured to emit logs in structured JSON format rather than raw standard output. JSON logging allows Splunk to parse fields like tool\_name, target\_path, and execution\_time automatically, enabling AI-enriched incident response.46  
2. **Deploy Splunk Universal Forwarder:** Install the Splunk Universal Forwarder on the Linux host or Docker container running the OpenCLAW daemon.48  
3. **Define Inputs:** Configure the /opt/splunkforwarder/etc/system/local/inputs.conf file to monitor the OpenCLAW log directory (typically \~/.openclaw/logs/):  
   Ini, TOML  
   \[monitor:///opt/openclaw/logs/\*.json\]  
   sourcetype \= \_json  
   index \= ai\_agent\_ops

.49 4\. **Configure Receiving Port:** Ensure the primary Splunk Enterprise instance has TCP port 9997 configured to receive the forwarder's data streams.47 5\. **Alerting Baselines:** Within Splunk, establish high-priority alerts for risk indicators. These include the execution of chmod, accessing /etc/ or \~/.ssh/ directories, or invoking the canvas.eval Javascript primitive, which the security documentation explicitly flags as an intentional operator vulnerability if abused.51

### **6.3 EU AI Act Compliance (2026 Standards)**

As autonomous systems scale into enterprise deployment, they must adhere to stringent legal frameworks. By mid-2026, the EU AI Act establishes mandatory compliance requirements for AI systems, particularly those categorized under high-risk tiers.12

To ensure the OpenCLAW LLMOS remains compliant, the following technical and organizational measures are enforced by this SOP:

* **Automated Record-Keeping & Traceability:** The Splunk SOC integration fulfills the mandate for comprehensive usage logging. The system maintains detailed records of data sources, intermediate reasoning steps, and final actions, creating an audit trail showing exactly how the AI arrived at a decision.12  
* **Human Oversight Mechanisms:** The explicit configuration of HITL approval gates for state-mutating operations fulfills the requirement to design systems with appropriate human supervision to prevent autonomous harm.12  
* **Risk Management and Quality Management:** Regular audits using skillvet and continuous monitoring of prompt injection vulnerability rates constitute a proactive risk management framework, essential for demonstrating conformity and securing CE marking if the system is deployed commercially.12

## **7.0 Developer Experience (DX) and Agent Evaluation Metrics**

Continuous improvement of the LLMOS requires empirical measurement. Subjective assessments of the agent's performance (e.g., "the agent feels lacking") must be replaced with strict Developer Experience (DX) frameworks and automated evaluations.11

### **7.1 Establishing the Core Metrics**

According to modern evaluation methodologies, agent performance should be measured across distinct lifecycle stages using specific quantitative metrics.53

| Metric Category | Target Measurement | Optimization Goal |
| :---- | :---- | :---- |
| **Goal Fulfillment** | **Completion Rate:** The percentage of complex, multi-step autonomous workflows successfully completed without human intervention.53 | Achieve enterprise baselines (e.g., \>60% success on single runs for multi-step tasks).54 |
| **Operational Efficiency** | **Containment Rate:** The frequency at which the agent resolves the primary issue without needing to escalate to the user for clarification or manual fix.53 | Reduce human-in-the-loop bottlenecks for low-risk, repetitive tasks. |
| **Developer Experience (DX)** | **PR Throughput / Cycle Time:** The volume and speed of pull requests authored or reviewed by the agent.55 | Increase baseline throughput utilizing the dual-agent Architect-Builder paradigm. Data shows agentic tools drive a 46% increase in throughput for frequent users.55 |
| **System Reliability** | **Prompt Injection Vulnerability Rate:** The frequency at which the agent fails to reject malicious context or unauthorized instructions.53 | Absolute minimization. Enforced via strict parsing, sandboxing, and the skillvet pipeline.44 |

### **7.2 Implementing Tracing and Observability**

To accurately track these metrics, the deployment must integrate an AI evaluation platform, such as Maxim AI, Langfuse, or LangSmith.57

* **Execution Tracing:** The platform must log every prompt, intermediate tool call, and final output. This allows for trace-level monitoring that calculates rolling averages and percentiles for latency and cost.54  
* **Failure Diagnosis:** When the agent's Completion Rate drops below predefined statistical thresholds, the system must automatically trigger a deep evaluation of recent interactions to diagnose root causes.54 This enables engineers to identify if the failure occurred during the Planning phase (e.g., poor tool selection) or Execution phase (e.g., API timeouts).

## **8.0 Implementation Task Registry**

The preceding sections (3.0–7.0) define the architectural requirements, security posture, and evaluation framework for the LLMOS transformation. This section operationalizes those requirements into a structured, individually traceable task registry designed for sequential execution under human supervision via an AI-assisted IDE (such as Cursor).

Each task is a single, atomic unit of work. Tasks are grouped into phases that map directly to the SOP sections they implement. The phase ordering enforces a strict dependency chain: environment before configuration, configuration before integration, integration before security hardening, and so on.

### **8.1 Task Registry Schema**

Every task entry in this registry carries the following attributes, aligning with the SOC, DI, DX, and SSOT disciplines established in this SOP:

| Attribute | Purpose | Governance Domain |
| :---- | :---- | :---- |
| **Task ID** | Unique identifier (e.g., `T-0.1`) for traceability and cross-referencing | SSOT |
| **SOP Reference** | Which SOP section (3.x, 4.x, 5.x, 6.x, 7.x) defines the requirement | DI (data lineage) |
| **LLMOS Layer** | Control Plane / Integration / Execution / Intelligence | Architecture alignment |
| **Category** | `ENV` \| `CONFIG` \| `MCP` \| `SECURITY` \| `PROMPT` \| `LOGGING` \| `METRIC` | Separation of concerns |
| **Dependencies** | Which Task IDs must complete first | Deterministic ordering |
| **Inputs** | Required pre-conditions (files, credentials, system state) | DI (pre-conditions) |
| **Outputs** | Concrete deliverable (file path, verified state, config entry) | SSOT (the deliverable) |
| **Verification** | Shell command or assertion to confirm success | DX (automated checks) |
| **SOC Relevance** | Whether the output feeds the SIEM pipeline (Yes/No + rationale) | SOC |
| **HITL Gate** | `read-only` \| `mutative` \| `destructive` — drives human approval per Section 6.1 | Security posture |
| **Complexity** | `trivial` \| `moderate` \| `complex` — scoping for session boundaries | DX (planning) |

### **8.2 Phase 0: Environment Assessment (SOP 3.0)**

This phase establishes the isolation boundary before any gateway daemon or configuration is touched. Every task in this phase maps to the Control Plane layer and the `ENV` category.

---

**T-0.1 — Detect Host Operating System**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 3.0 |
| **LLMOS Layer** | Control Plane |
| **Category** | `ENV` |
| **Dependencies** | None |
| **Inputs** | Host machine access |
| **Outputs** | Environment variable or log entry recording `OS_TYPE` as `windows`, `macos`, or `linux` |
| **Verification** | `uname -s` (Linux/macOS) or `$env:OS` (PowerShell). The result determines which subsequent tasks in this phase are executed (WSL2 path vs. Docker path). |
| **SOC Relevance** | No |
| **HITL Gate** | `read-only` |
| **Complexity** | `trivial` |

---

**T-0.2 — Verify WSL2 and Ubuntu-24.04 (Windows only)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 3.1, Steps 1–3 |
| **LLMOS Layer** | Control Plane |
| **Category** | `ENV` |
| **Dependencies** | T-0.1 (must report `windows`) |
| **Inputs** | Elevated PowerShell terminal |
| **Outputs** | WSL2 running Ubuntu-24.04 with systemd enabled |
| **Verification** | `wsl -l -v` shows `Ubuntu-24.04` in `Running` state, version `2`. Inside WSL: `systemctl --version` returns without error. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — installs a Linux distribution if absent |
| **Complexity** | `moderate` |

---

**T-0.3 — Verify Docker Desktop and Model Runner (macOS/Linux only)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 3.2, Steps 1–2 |
| **LLMOS Layer** | Control Plane |
| **Category** | `ENV` |
| **Dependencies** | T-0.1 (must report `macos` or `linux`) |
| **Inputs** | Docker Desktop installed with Docker Model Runner enabled |
| **Outputs** | Docker daemon responding; local model weights available |
| **Verification** | `docker info` succeeds. `docker model list` includes `ai/gpt-oss:20B-UD-Q4_K_XL` (or confirms it can be pulled). |
| **SOC Relevance** | No |
| **HITL Gate** | `read-only` (verification only; pull is T-0.5) |
| **Complexity** | `trivial` |

---

**T-0.4 — Create Dedicated Service Account (Windows/WSL2 path)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 3.1, Step 4 |
| **LLMOS Layer** | Control Plane |
| **Category** | `ENV` |
| **Dependencies** | T-0.2 |
| **Inputs** | WSL2 Ubuntu-24.04 terminal with `sudo` access |
| **Outputs** | System user `openclaw` exists; `/opt/openclaw/` owned by `openclaw:openclaw` |
| **Verification** | `id openclaw` returns uid/gid. `stat -c '%U:%G' /opt/openclaw` returns `openclaw:openclaw`. |
| **SOC Relevance** | Yes — least-privilege enforcement; compromised agent inherits only `openclaw` permissions |
| **HITL Gate** | `mutative` — creates a system user and directory |
| **Complexity** | `trivial` |

---

**T-0.5 — Provision Docker Sandbox (macOS/Linux path)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 3.2, Steps 3–4 |
| **LLMOS Layer** | Control Plane |
| **Category** | `ENV` |
| **Dependencies** | T-0.3 |
| **Inputs** | Docker daemon running; model weights pulled |
| **Outputs** | Sandbox named `openclaw` created; network proxy restricted to `localhost` |
| **Verification** | `docker sandbox ls` lists `openclaw`. `docker sandbox inspect openclaw` confirms network proxy configuration. |
| **SOC Relevance** | Yes — egress filtering prevents data exfiltration to C2 servers |
| **HITL Gate** | `mutative` — creates sandbox and configures network proxy |
| **Complexity** | `moderate` |

---

**T-0.6 — Install OpenCLAW CLI**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 3.1 Step 5 (WSL2) or 3.2 Step 5 (Docker) |
| **LLMOS Layer** | Control Plane |
| **Category** | `ENV` |
| **Dependencies** | T-0.4 (Windows) or T-0.5 (macOS/Linux) |
| **Inputs** | Network access to `molt.bot` (WSL2 path) or sandbox shell (Docker path) |
| **Outputs** | `openclaw` binary available on `$PATH` |
| **Verification** | `openclaw --version` returns a valid version string. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — downloads and installs a binary from the internet |
| **Complexity** | `trivial` |

### **8.3 Phase 1: Configuration Bootstrapping (SOP 4.1–4.2)**

This phase creates the gateway configuration and verifies the Control Plane is operational. Tasks map to the Control Plane and Integration layers under the `CONFIG` category.

---

**T-1.1 — Create Configuration Directory Structure**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 4.1, Step 1 |
| **LLMOS Layer** | Control Plane |
| **Category** | `CONFIG` |
| **Dependencies** | T-0.6 |
| **Inputs** | `openclaw` CLI installed |
| **Outputs** | `~/.openclaw/` directory exists with correct ownership |
| **Verification** | `test -d ~/.openclaw && echo OK` |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` |
| **Complexity** | `trivial` |

---

**T-1.2 — Generate or Update openclaw.json**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 4.1, Steps 1–3 |
| **LLMOS Layer** | Control Plane |
| **Category** | `CONFIG` |
| **Dependencies** | T-1.1 |
| **Inputs** | `~/.openclaw/` exists; desired gateway port (`18789`), host (`127.0.0.1`), and workspace routing schema from SOP 4.1 Step 3 |
| **Outputs** | `~/.openclaw/openclaw.json` with valid JSON containing `gateway.host`, `gateway.port`, and `agents` keys (v2026.2.26: `agents.list` + `bindings`, not the deprecated `workspaces`) |
| **Verification** | `python3 -c "import json; json.load(open('$HOME/.openclaw/openclaw.json'))"` exits cleanly. `jq '.gateway.host' ~/.openclaw/openclaw.json` returns `"127.0.0.1"`. |
| **SOC Relevance** | Yes — binding to localhost is a security-critical configuration |
| **HITL Gate** | `mutative` — creates or modifies the central config file |
| **Complexity** | `moderate` |

---

**T-1.3 — Install Gateway Daemon**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 4.1, Step 1 |
| **LLMOS Layer** | Control Plane |
| **Category** | `CONFIG` |
| **Dependencies** | T-1.2 |
| **Inputs** | Valid `openclaw.json`; systemd (WSL2/Linux) or launchd (macOS) available |
| **Outputs** | OpenCLAW gateway daemon registered as a system service |
| **Verification** | `systemctl is-active openclaw` returns `active` (Linux/WSL2) or `launchctl list | grep openclaw` returns a PID (macOS). |
| **SOC Relevance** | Yes — daemon lifecycle is a SOC monitoring surface |
| **HITL Gate** | `mutative` — installs a system daemon |
| **Complexity** | `moderate` |

---

**T-1.4 — Verify Localhost Port Binding**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 4.1, Step 2 |
| **LLMOS Layer** | Control Plane |
| **Category** | `CONFIG` |
| **Dependencies** | T-1.3 |
| **Inputs** | Gateway daemon running |
| **Outputs** | Confirmed: port `18789` bound exclusively to `127.0.0.1` |
| **Verification** | `netstat -an \| grep 18789 \| grep LISTEN` shows only `127.0.0.1:18789` (no `0.0.0.0`). Alternatively: `ss -tlnp \| grep 18789`. |
| **SOC Relevance** | Yes — if bound to `0.0.0.0`, the gateway is internet-exposed (critical finding) |
| **HITL Gate** | `read-only` |
| **Complexity** | `trivial` |

---

**T-1.5 — Verify A2UI Canvas Endpoints**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 4.2, Step 1 |
| **LLMOS Layer** | Integration |
| **Category** | `CONFIG` |
| **Dependencies** | T-1.4 |
| **Inputs** | Gateway daemon running and bound to localhost |
| **Outputs** | HTTP 200 on `/__openclaw__/canvas/` and `/__openclaw__/a2ui/` |
| **Verification** | `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/__openclaw__/canvas/` returns `200`. Repeat for `/a2ui/`. |
| **SOC Relevance** | No |
| **HITL Gate** | `read-only` |
| **Complexity** | `trivial` |

### **8.4 Phase 2: MCP Provisioning (SOP 5.1–5.4)**

This phase deploys the Model Context Protocol servers that form the Integration Layer. All tasks are `MCP` category.

---

**T-2.1 — Verify Node.js Version**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.2, Step 1 |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-0.6 |
| **Inputs** | Node.js runtime on `$PATH` |
| **Outputs** | Confirmed: Node.js >= 22.x installed |
| **Verification** | `node -v` returns `v22.x.x` or higher. |
| **SOC Relevance** | No |
| **HITL Gate** | `read-only` |
| **Complexity** | `trivial` |

---

**T-2.2 — Install mcporter Skill**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.1, Step 1 |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-2.1, T-1.2 |
| **Inputs** | Node.js >= 22; network access to npm registry |
| **Outputs** | `mcporter` CLI available; skill registered in workspace |
| **Verification** | `npx clawhub@latest install mcporter` completes without error. `mcporter --version` returns a version string. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — downloads and installs an npm package |
| **Complexity** | `trivial` |

---

**T-2.3 — Create mcporter.json Configuration**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.1, Step 2 |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-2.2 |
| **Inputs** | `mcporter` installed |
| **Outputs** | `~/.mcporter/mcporter.json` exists with a valid `mcpServers` object |
| **Verification** | `python3 -c "import json; d=json.load(open('$HOME/.mcporter/mcporter.json')); assert 'mcpServers' in d"` exits cleanly. |
| **Path Resolution** | If copied manually (not via bootstrap), run `py scripts/resolve-mcporter-paths.py` to resolve `/opt/openclaw/workspace` to OS-correct paths. Bootstrap auto-resolves on every run. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — creates a config file |
| **Complexity** | `trivial` |

---

**T-2.4 — Inject Sequential Thinking MCP Server**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.2, Step 1 |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-2.3 |
| **Inputs** | `~/.mcporter/mcporter.json` with `mcpServers` key |
| **Outputs** | `mcpServers.sequential-thinking` entry with `command: "npx"`, `args: ["-y", "@modelcontextprotocol/server-sequential-thinking"]`, `env.DISABLE_THOUGHT_LOGGING: "false"` |
| **Verification** | `jq '.mcpServers["sequential-thinking"].command' ~/.mcporter/mcporter.json` returns `"npx"`. `mcporter list` includes `sequential-thinking`. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` |
| **Complexity** | `trivial` |

---

**T-2.5 — Inject Playwright MCP Server**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.3, Step 1 |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-2.3 |
| **Inputs** | `~/.mcporter/mcporter.json` with `mcpServers` key |
| **Outputs** | `mcpServers.playwright` entry with `command: "npx"`, `args: ["-y", "@playwright/mcp@latest", "--output-dir", "/opt/openclaw/workspace/exports"]` |
| **Verification** | `jq '.mcpServers.playwright.command' ~/.mcporter/mcporter.json` returns `"npx"`. `mcporter list` includes `playwright`. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` |
| **Complexity** | `trivial` |

---

**T-2.6 — Inject GitHub MCP Server**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.4, Steps 1–2 |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-2.3 |
| **Inputs** | `~/.mcporter/mcporter.json`; a scoped GitHub Personal Access Token (PAT) set as `GITHUB_TOKEN` in host environment |
| **Outputs** | `mcpServers.github` entry passing `GITHUB_TOKEN` via `env` block |
| **Verification** | `jq '.mcpServers.github' ~/.mcporter/mcporter.json` returns a non-null object. `mcporter list` includes `github`. |
| **SOC Relevance** | Yes — PAT scope and lifecycle are audit-relevant |
| **HITL Gate** | `mutative` — references a credential (PAT must already exist; this task does not create one) |
| **Complexity** | `moderate` |

---

**T-2.7 — Configure Sequential Thinking Prompt Schema**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.2, Steps 2–3 |
| **LLMOS Layer** | Integration / Execution |
| **Category** | `MCP` |
| **Dependencies** | T-2.4 |
| **Inputs** | Sequential Thinking server operational |
| **Outputs** | Agent system prompt updated to enforce `thought`, `thoughtNumber`, `totalThoughts`, `nextThoughtNeeded`, `isRevision`, and `revisesThought` variable usage for every complex query |
| **Verification** | Manual review: the Architect prompt (T-4.1) must reference these variables explicitly. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — modifies agent behavior via prompt engineering |
| **Complexity** | `complex` |

---

**T-2.9 — Inject Memory MCP Server (v3.0)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.x (v3.0 expansion) |
| **LLMOS Layer** | Integration / Intelligence |
| **Category** | `MCP` |
| **Dependencies** | T-2.3 |
| **Inputs** | `~/.mcporter/mcporter.json` with `mcpServers` key |
| **Outputs** | `mcpServers.memory` entry with `command: "npx"`, `args: ["-y", "@modelcontextprotocol/server-memory"]` |
| **Verification** | `jq '.mcpServers.memory.command' ~/.mcporter/mcporter.json` returns `"npx"`. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` |
| **Complexity** | `trivial` |

---

**T-2.10 — Inject Filesystem MCP Server (v3.0)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.x (v3.0 expansion) |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-2.3 |
| **Inputs** | `~/.mcporter/mcporter.json` with `mcpServers` key |
| **Outputs** | `mcpServers.filesystem` entry with `command: "npx"`, `args: ["-y", "@modelcontextprotocol/server-filesystem", "/opt/openclaw/workspace"]` |
| **Verification** | `jq '.mcpServers.filesystem.command' ~/.mcporter/mcporter.json` returns `"npx"`. |
| **SOC Relevance** | Yes — filesystem access is a security surface; governed by permissions.json HITL classification |
| **HITL Gate** | `mutative` |
| **Complexity** | `trivial` |

---

**T-2.11 — Inject Fetch MCP Server (v3.0)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.x (v3.0 expansion) |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-2.3 |
| **Inputs** | `~/.mcporter/mcporter.json` with `mcpServers` key |
| **Outputs** | `mcpServers.fetch` entry with `command: "npx"`, `args: ["-y", "@modelcontextprotocol/server-fetch"]` |
| **Verification** | `jq '.mcpServers.fetch.command' ~/.mcporter/mcporter.json` returns `"npx"`. |
| **SOC Relevance** | Yes — HTTP client can be used for data exfiltration; requires HITL approval |
| **HITL Gate** | `mutative` |
| **Complexity** | `trivial` |

---

**T-2.8 — Consolidated MCP Health Check**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 5.1 Step 3; 5.2–5.4 |
| **LLMOS Layer** | Integration |
| **Category** | `MCP` |
| **Dependencies** | T-2.4, T-2.5, T-2.6, T-2.9, T-2.10, T-2.11 |
| **Inputs** | All six MCP servers injected into `mcporter.json` |
| **Outputs** | All servers reachable and reporting tool schemas |
| **Verification** | `mcporter list` returns `sequential-thinking`, `playwright`, `github`, `memory`, `filesystem`, and `fetch` with no error status. |
| **SOC Relevance** | No |
| **HITL Gate** | `read-only` |
| **Complexity** | `trivial` |

### **8.5 Phase 3: Security Implementation (SOP 6.1–6.3)**

This phase hardens the deployment. Tasks span all LLMOS layers and carry `SOC Relevance: Yes` unless noted otherwise. Categories are `SECURITY` and `LOGGING`.

---

**T-3.1 — Install skillvet Scanner**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 6.1, Step 1 |
| **LLMOS Layer** | All |
| **Category** | `SECURITY` |
| **Dependencies** | T-0.6 |
| **Inputs** | Network access to the skillvet repository |
| **Outputs** | `skills/skillvet/` directory containing the scanner scripts |
| **Verification** | `test -f skills/skillvet/scripts/safe-install.sh && echo OK` |
| **SOC Relevance** | Yes — scanner is the first line of defense against ClawHavoc/ClickFix |
| **HITL Gate** | `mutative` — clones a repository |
| **Complexity** | `trivial` |

---

**T-3.2 — Create vet-install.sh Wrapper**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 6.1, Step 2 |
| **LLMOS Layer** | All |
| **Category** | `SECURITY` |
| **Dependencies** | T-3.1 |
| **Inputs** | `skills/skillvet/scripts/safe-install.sh` exists |
| **Outputs** | `vet-install.sh` in workspace root; permissions `700`; delegates to `safe-install.sh` with the skill slug as argument |
| **Verification** | `stat -c '%a' vet-install.sh` returns `700`. `head -1 vet-install.sh` contains `#!/usr/bin/env bash`. |
| **SOC Relevance** | Yes — ensures all future skill installations are routed through the 48-check scanner |
| **HITL Gate** | `mutative` — creates an executable script |
| **Complexity** | `trivial` |

---

**T-3.3 — Enforce HITL Policy in openclaw.json**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 6.1, Step 3 |
| **LLMOS Layer** | Control Plane |
| **Category** | `SECURITY` |
| **Dependencies** | T-1.2 |
| **Inputs** | Valid `~/.openclaw/openclaw.json` |
| **Outputs** | `openclaw.json` contains a `permissions` block that classifies tools as `autonomous` (read-only) or `requires_approval` (mutative/destructive), per the HITL matrix in SECURITY.md Section 3 |
| **Verification** | `jq '.permissions' ~/.openclaw/openclaw.json` returns a non-null object with both `autonomous` and `requires_approval` arrays. |
| **SOC Relevance** | Yes — HITL enforcement is both a security control and an EU AI Act compliance mechanism |
| **HITL Gate** | `mutative` — modifies the central config |
| **Complexity** | `moderate` |

---

**T-3.4 — Verify Network Egress Filtering**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 6.1 (implicit); 3.1 Step 2; 3.2 Step 4 |
| **LLMOS Layer** | Control Plane |
| **Category** | `SECURITY` |
| **Dependencies** | T-1.4 (port binding verified); T-0.5 (Docker path) or T-0.4 (WSL2 path) |
| **Inputs** | Gateway running; sandbox or WSL2 environment active |
| **Outputs** | Confirmed: outbound traffic from the agent process is restricted to `localhost` (Docker path) or the agent cannot bind to `0.0.0.0` (WSL2 path) |
| **Verification** | Docker: `docker sandbox inspect openclaw` shows `allowedHosts: ["localhost"]`. WSL2: `ss -tlnp \| grep 18789` shows only `127.0.0.1`. |
| **SOC Relevance** | Yes — egress violation is a critical SOC alert |
| **HITL Gate** | `read-only` |
| **Complexity** | `trivial` |

---

**T-3.5 — Configure Structured JSON Logging**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 6.2, Step 1 |
| **LLMOS Layer** | All |
| **Category** | `LOGGING` |
| **Dependencies** | T-1.2 |
| **Inputs** | Valid `openclaw.json` |
| **Outputs** | OpenCLAW runtime configured to emit structured JSON logs to `/opt/openclaw/logs/agent_activity.json`. Log directory created with correct ownership. |
| **Verification** | `test -d /opt/openclaw/logs && echo OK`. After a test interaction: `python3 -c "import json; json.load(open('/opt/openclaw/logs/agent_activity.json'))"` exits cleanly. |
| **SOC Relevance** | Yes — JSON format is required for Splunk field extraction (tool\_name, target\_path, execution\_time) |
| **HITL Gate** | `mutative` — creates directories and modifies runtime config |
| **Complexity** | `moderate` |

---

**T-3.6 — Create Splunk inputs.conf Template**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 6.2, Steps 2–4 |
| **LLMOS Layer** | All |
| **Category** | `LOGGING` |
| **Dependencies** | T-3.5 |
| **Inputs** | Log directory path (`/opt/openclaw/logs/`); target Splunk index (`ai_agent_ops`) |
| **Outputs** | File at `config/splunk/inputs.conf` containing the monitor stanza: `[monitor:///opt/openclaw/logs/*.json]` with `sourcetype = _json` and `index = ai_agent_ops` |
| **Verification** | `grep -q 'sourcetype' config/splunk/inputs.conf && echo OK` |
| **SOC Relevance** | Yes — this file is deployed to `/opt/splunkforwarder/etc/system/local/` on the Splunk forwarder host |
| **HITL Gate** | `mutative` — creates a config file |
| **Complexity** | `trivial` |

---

**T-3.7 — EU AI Act Compliance Checklist Validation**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 6.3 |
| **LLMOS Layer** | All |
| **Category** | `SECURITY` |
| **Dependencies** | T-3.3, T-3.5, T-3.6 |
| **Inputs** | HITL policy configured (T-3.3); structured logging active (T-3.5); Splunk template created (T-3.6) |
| **Outputs** | Documented confirmation that three EU AI Act requirements are met: (1) Automated Record-Keeping via Splunk pipeline, (2) Human Oversight via HITL gates, (3) Risk Management via skillvet + continuous monitoring |
| **Verification** | Manual review against the three bullet points in SOP Section 6.3. All three controls must be traceable to a completed task in this registry. |
| **SOC Relevance** | Yes — compliance is auditable |
| **HITL Gate** | `read-only` — verification only |
| **Complexity** | `moderate` |

### **8.6 Phase 4: Multi-Agent Prompt Engineering (SOP 2.0, 5.2)**

This phase creates the cognitive separation across the four-agent model: Orchestrator, Architect, Executor, and Verifier. Tasks map to the Execution and Intelligence layers under the `PROMPT` category.

---

**T-4.1 — Create ARCHITECT\_PROMPT.md**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 2.0 (Holistika Strategy); 5.2 Steps 2–3 |
| **LLMOS Layer** | Execution |
| **Category** | `PROMPT` |
| **Dependencies** | T-2.7 (Sequential Thinking schema defined) |
| **Inputs** | Sequential Thinking tool schema (`thought`, `thoughtNumber`, `totalThoughts`, `nextThoughtNeeded`, `isRevision`, `revisesThought`) |
| **Outputs** | `ARCHITECT_PROMPT.md` in workspace root. The prompt must: (a) restrict the agent to read-only mode, (b) mandate use of `sequential_thinking` for every complex query, (c) prohibit file-write, shell execution, and API mutation tools, (d) require structured plan output with explicit tool selections and risk assessments. |
| **Verification** | `grep -q 'sequential_thinking' ARCHITECT_PROMPT.md && grep -q 'read-only' ARCHITECT_PROMPT.md && echo OK` |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — creates a file |
| **Complexity** | `complex` |

---

**T-4.2 — Create EXECUTOR\_PROMPT.md**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 2.0 (Holistika Processes); 1.0 (multi-agent paradigm) |
| **LLMOS Layer** | Execution |
| **Category** | `PROMPT` |
| **Dependencies** | T-4.1 |
| **Inputs** | Architect prompt exists as the upstream reference |
| **Outputs** | `EXECUTOR_PROMPT.md` in workspace root. The prompt must: (a) require reading the Architect's plan output before executing any command, (b) restrict scope to the directives in the plan document, (c) enforce HITL confirmation for mutative operations, (d) optimize for throughput over deep reasoning. |
| **Verification** | `grep -q 'plan' EXECUTOR_PROMPT.md && grep -q 'HITL' EXECUTOR_PROMPT.md && echo OK` |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — creates a file |
| **Complexity** | `moderate` |

---

**T-4.5 — Create ORCHESTRATOR\_PROMPT.md (v3.0)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 2.0 (multi-agent coordination); 1.0 (task decomposition) |
| **LLMOS Layer** | Execution |
| **Category** | `PROMPT` |
| **Dependencies** | T-4.1, T-4.2 |
| **Inputs** | Architect and Executor prompts exist as downstream references |
| **Outputs** | `ORCHESTRATOR_PROMPT.md` in workspace root. The prompt must: (a) restrict the agent to read-only mode, (b) define task decomposition protocol for breaking complex requests into delegable sub-tasks, (c) specify delegation targets (Architect for planning, Executor for implementation), (d) define progress tracking and error escalation protocols. |
| **Verification** | `grep -q 'Orchestrator' ORCHESTRATOR_PROMPT.md && grep -q 'read-only' ORCHESTRATOR_PROMPT.md && echo OK` |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — creates a file |
| **Complexity** | `complex` |

---

**T-4.6 — Create VERIFIER\_PROMPT.md (v3.0)**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 2.0 (quality assurance); 7.0 (DX metrics) |
| **LLMOS Layer** | Execution |
| **Category** | `PROMPT` |
| **Dependencies** | T-4.2 |
| **Inputs** | Executor prompt exists; DX metric baselines from T-5.2 inform verification criteria |
| **Outputs** | `VERIFIER_PROMPT.md` in workspace root. The prompt must: (a) define the Verification Protocol (lint, test, build, browser checks), (b) specify the Fix Suggestion Protocol with confidence ratings (HIGH/MEDIUM/LOW), (c) implement 3-attempt escalation: suggest fix → suggest alternative → abort with diagnosis, (d) restrict to read-write validation commands only. |
| **Verification** | `grep -q 'Verifier' VERIFIER_PROMPT.md && grep -q 'Verification Protocol' VERIFIER_PROMPT.md && echo OK` |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — creates a file |
| **Complexity** | `complex` |

---

**T-4.3 — Define Intelligence Matrix Schema**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 2.2 (Intelligence Matrix and DI) |
| **LLMOS Layer** | Intelligence |
| **Category** | `PROMPT` |
| **Dependencies** | T-4.1 |
| **Inputs** | Holistika DI framework requirements from SOP 2.2 |
| **Outputs** | A schema definition (JSON Schema or structured markdown) specifying the Intelligence Matrix attributes: `fact_id`, `source_credibility` (numerical), `direct_impact` (numerical), `indirect_impact` (numerical), `pestel_category`, `generational_filter`, and `ssot_verified` (boolean). Stored as `config/intelligence-matrix-schema.json` or appended to the Architect prompt. |
| **Verification** | Schema file parses as valid JSON Schema, or the Architect prompt contains all six attribute names. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — creates a schema file |
| **Complexity** | `complex` |

---

**T-4.4 — Configure Agent Routing in openclaw.json**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 4.1 Step 3; 2.0 |
| **LLMOS Layer** | Control Plane / Execution |
| **Category** | `PROMPT` |
| **Dependencies** | T-1.2, T-4.1, T-4.2, T-4.5, T-4.6 |
| **Inputs** | Valid `openclaw.json`; all four prompt files exist |
| **Outputs** | `openclaw.json` updated with `agents.list` containing orchestrator, architect, executor, and verifier entries. Each agent has: `id`, `name`, `workspace` (dedicated directory), and `identity` (object with `name`, `emoji`, `theme`). System prompts deployed as `SOUL.md` inside each agent's workspace. `agents.defaults.thinkingDefault` set to `"off"` for Ollama model compatibility. Optional `bindings` array for channel-to-agent routing. |
| **Verification** | `openclaw gateway restart` reports no validation errors. `jq '.agents.list \| length' ~/.openclaw/openclaw.json` returns `4`. All four workspaces contain `SOUL.md`. |
| **SOC Relevance** | Yes — workspace isolation prevents context cross-contamination between channels |
| **HITL Gate** | `mutative` |
| **Complexity** | `moderate` |

> **Implementation Note (v3.0 update):** The original SOP text referenced a `workspaces` object for channel routing. This schema does not exist in OpenCLAW v2026.2.26. The correct mechanism is `agents.list` (agent definitions) + `bindings` (channel-to-agent routing rules). Additionally, `identity` must be an object (`{ name, emoji, theme }`), not a string path. Behavioral prompts are loaded from `SOUL.md` inside each agent's workspace directory. Ollama-hosted models require `agents.defaults.thinkingDefault: "off"` to prevent 400 errors from unsupported `think` parameters. As of v3.0, the `agents.list` must contain all four agents: Orchestrator, Architect, Executor, and Verifier. See [ARCHITECTURE.md](ARCHITECTURE.md) for full details.

### **8.7 Phase 5: Observability and DX Metrics (SOP 7.0)**

This phase establishes the evaluation framework for continuous improvement. Tasks map to all layers under the `METRIC` and `LOGGING` categories.

---

**T-5.1 — Scaffold Evaluation Platform Configuration**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 7.2 |
| **LLMOS Layer** | All |
| **Category** | `METRIC` |
| **Dependencies** | T-3.5 (structured logging active) |
| **Inputs** | Choice of evaluation platform (Langfuse, Maxim AI, or LangSmith); platform API credentials |
| **Outputs** | Configuration file or environment variables for the selected platform, stored in `config/eval/` (e.g., `config/eval/langfuse.env.example`). The file must define the trace ingestion endpoint and API key variable name without containing actual secrets. |
| **Verification** | Config file exists and parses without error. `.gitignore` already excludes `.env` files. |
| **SOC Relevance** | Yes — trace data feeds the observability pipeline |
| **HITL Gate** | `mutative` — creates config scaffolding |
| **Complexity** | `moderate` |

---

**T-5.2 — Define Metric Baselines**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 7.1 |
| **LLMOS Layer** | All |
| **Category** | `METRIC` |
| **Dependencies** | T-5.1 |
| **Inputs** | Metric definitions from SOP 7.1 table |
| **Outputs** | A `config/eval/baselines.json` file encoding the four target metrics: `completion_rate` (target: `>0.60`), `containment_rate` (target: minimize), `pr_throughput_increase` (target: `>0.46`), `prompt_injection_vuln_rate` (target: `0.00`). Each entry includes `metric_id`, `target_value`, `unit`, and `evaluation_window`. |
| **Verification** | `python3 -c "import json; d=json.load(open('config/eval/baselines.json')); assert len(d) == 4"` exits cleanly. |
| **SOC Relevance** | No |
| **HITL Gate** | `mutative` — creates a config file |
| **Complexity** | `trivial` |

---

**T-5.3 — Configure Alerting Thresholds**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 7.2; 6.2 Step 5 |
| **LLMOS Layer** | All |
| **Category** | `LOGGING` |
| **Dependencies** | T-5.2, T-3.6 |
| **Inputs** | Metric baselines defined; Splunk inputs.conf template created |
| **Outputs** | A `config/eval/alerts.json` file defining threshold-based alerts: (1) Completion Rate drops below `0.60` over a rolling 7-day window, (2) Prompt Injection Vulnerability Rate exceeds `0.00`, (3) SOC risk indicators from SOP 6.2 Step 5 (chmod execution, `/etc/` access, `~/.ssh/` access, `canvas.eval` invocation). |
| **Verification** | `python3 -c "import json; d=json.load(open('config/eval/alerts.json')); assert len(d) >= 3"` exits cleanly. |
| **SOC Relevance** | Yes — these alerts are the primary SOC detection surface for agent anomalies |
| **HITL Gate** | `mutative` — creates a config file |
| **Complexity** | `moderate` |

**T-5.4 — AKOS Orchestration Library and Langfuse Watcher**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 7.2 |
| **LLMOS Layer** | All |
| **Category** | `METRIC`, `LOGGING` |
| **Dependencies** | T-5.1, T-5.2, T-5.3 |
| **Inputs** | Eval configs defined, alert thresholds configured |
| **Outputs** | (1) `akos/` Python package with Pydantic models (`models.py`), shared I/O (`io.py`), structured logging (`log.py`), subprocess wrapper (`process.py`), state tracking (`state.py`), Langfuse telemetry (`telemetry.py`). (2) `scripts/log-watcher.py` that tails gateway logs and pushes traces to Langfuse. (3) All scripts refactored to import from `akos/`. |
| **Verification** | `py -m pytest tests/test_akos_models.py tests/test_akos_alerts.py -v` -- all tests pass. |
| **SOC Relevance** | Yes — the log watcher feeds real-time alert evaluation |
| **HITL Gate** | `mutative` — creates library code and scripts |
| **Complexity** | `high` |

**T-5.5 — Alert Evaluation Engine**

| Attribute | Value |
| :---- | :---- |
| **SOP Reference** | 7.2; 6.2 Step 5 |
| **LLMOS Layer** | All |
| **Category** | `LOGGING`, `SECURITY` |
| **Dependencies** | T-5.3, T-5.4 |
| **Inputs** | `config/eval/alerts.json`, `config/eval/baselines.json`, `akos/models.py` |
| **Outputs** | `akos/alerts.py` — `AlertEvaluator` class with `check_realtime(log_entry)` and `check_periodic(metrics)` methods. Integrated into `scripts/log-watcher.py`. Tests in `tests/test_akos_alerts.py`. |
| **Verification** | `py -m pytest tests/test_akos_alerts.py -v` -- all tests pass. |
| **SOC Relevance** | Yes — this is the primary live SOC detection surface |
| **HITL Gate** | `mutative` — creates security-critical code |
| **Complexity** | `high` |

### **8.8 Execution Constraints**

All phases in this registry must be executed sequentially. An AI-assisted IDE (such as Cursor) executing these tasks must adhere to the following constraints:

1. **Sequential Execution:** Tasks within a phase may execute in dependency order. No task may begin until all tasks listed in its Dependencies field have been verified as complete.
2. **HITL Enforcement:** Any task marked with HITL Gate `mutative` or `destructive` requires explicit human approval before execution. The operator must visually confirm the proposed action. Tasks marked `read-only` may execute autonomously.
3. **Verification-Before-Proceed:** After completing each task, the Verification command or assertion must be executed. A failing verification blocks all downstream dependent tasks.
4. **Idempotency:** Tasks should be designed to be safely re-run. If a task's Output already exists and its Verification passes, it may be skipped.
5. **Abort Protocol:** If a task fails verification after three retry attempts (v3.0: Verifier-guided recovery loop), execution halts. The operator must diagnose the failure manually before resuming.

## **9.0 AKOS v0.4.0 Operational Procedures**

This section documents the operational procedures introduced in v0.4.0. These procedures extend the foundational architecture (Sections 3.0-8.0) with runtime convergence, self-verification, structured planning, role-safe enforcement, semantic intelligence, workflow-native execution, evidence retrieval, deployment operations, and evaluation gates.

**Reference:** Full implementation plan at `docs/wip/improvement_proposal_claude_opus_4_max.plan.md`.

### **9.1 Runtime Convergence and Drift Detection**

The v0.3.0 implementation revealed that only 2 of 4 agents were deployed to the live runtime during bootstrap. v0.4.0 enforces full runtime convergence:

**Bootstrap (all 4 agents):**
- `scripts/bootstrap.py` now creates all 4 workspace directories (`workspace-orchestrator`, `workspace-architect`, `workspace-executor`, `workspace-verifier`).
- Scaffold files (IDENTITY.md, MEMORY.md, HEARTBEAT.md) are deployed to all workspaces via `deploy_scaffold_files()`.
- `mcporter.json` is generated with OS-appropriate paths (replacing hardcoded `/opt/openclaw/workspace`). Bootstrap also re-resolves existing configs automatically. For manual copies, use `py scripts/resolve-mcporter-paths.py`.
- Bootstrap strips provider blocks with unresolved `${VAR}` env vars (v0.4.1) to prevent gateway `MissingEnvVarError` crashes.
- Bootstrap force-syncs `agents.list` from the template to ensure all 4 agents are present (v0.4.1).
- AKOS-specific config keys (`logging`, `permissions`, `gateway.host`) are extracted into `~/.openclaw/akos-config.json` to avoid `openclaw doctor` warnings (v0.4.1).
- Session directories (`~/.openclaw/agents/<id>/sessions/`) are created for all agents (v0.4.1).

**Drift detection:**
- `scripts/check-drift.py` compares repo intended state against live runtime: agent count, workspace files, MCP servers, permissions.
- `GET /runtime/drift` API endpoint provides programmatic drift detection.
- Run after every model switch or bootstrap: `py scripts/check-drift.py`.
- Integrate into CI: exit code 0 = no drift, 1 = drift detected.

**Gateway health:**
- `GET /health` now performs a real HTTP probe to `http://127.0.0.1:18789/api/health` instead of returning `"unknown"`.
- Response includes gateway status (`up`, `degraded`, `unreachable`), RunPod status, and Langfuse status.

**API authentication:**
- All endpoints except `GET /health` require `Authorization: Bearer <key>` when `AKOS_API_KEY` is set.
- Set via environment variable or `--api-key` flag on `scripts/serve-api.py`.
- When unset, a warning is logged but open access is allowed (dev mode).

### **9.2 Self-Verifying Agent Protocol**

Inspired by Cursor's `ReadLints`, Augment Code's "proactive verification", and Lovable's "debugging tools FIRST" pattern.

**Post-edit verification (Executor):**
After every file write or shell command that modifies code:
1. Run the project's lint command (if known) OR check for syntax errors.
2. Run the project's test command (if known) targeting changed files only.
3. If verification fails, attempt self-fix (up to 3 cycles via Verifier).
4. Report verification status before proceeding to the next step.
5. NEVER move to the next step with unresolved verification failures.

**Loop detection (Orchestrator and Executor):**
If the agent detects: repeated identical tool calls, same edit made twice, or same error after 3 fix attempts, it MUST stop and escalate to the user with: specific issue, what was tried, and a request for help.

**Memory hygiene (all agents):**
After completing significant tasks: store key decisions in MEMORY.md (session-local), store durable facts via `memory_store()` (cross-session), tag entries with date and context.

**Package manager enforcement (Executor):**
Always use the project's package manager to add dependencies. Never manually edit package.json, requirements.txt, or pyproject.toml to add version numbers.

**Cost-aware heuristics (Orchestrator):**
Prefer the smallest set of high-signal tool calls. Batch related information-gathering. Skip expensive actions when cheaper alternatives exist.

### **9.3 Structured Planning Protocol**

Inspired by Windsurf Cascade's planning mode, Augment Code's conditional tasklist triggers, and Cursor's `TodoWrite`.

**When to create a plan:**
- Multi-file or cross-layer changes
- More than 2 edit/verify iterations expected
- More than 5 information-gathering calls expected
- User explicitly requests planning

**When to skip planning:**
- Single, straightforward tasks (rename, typo fix, config tweak)
- Purely conversational or informational requests
- Tasks completable in under 3 trivial steps

**Plan format:**
```
## Plan: [Task Title]
1. [ ] Step description
2. [ ] Step description
```
Mark `[x]` on completion, `[-]` on skip, `[/]` on in-progress.

**RULES.md customization:**
Each workspace contains a `RULES.md` file that agents read at session start. Users can customize agent behavior by editing this file (e.g., "Always use TypeScript for new files", "Run tests before every commit").

**Configuration:**
- Overlay: `prompts/overlays/OVERLAY_PLAN_TODOS.md`
- Applied to: Orchestrator and Architect in `standard` tier; Orchestrator, Architect, and Executor in `full` tier.

### **9.4 Role-Safe Capability Enforcement**

Role safety is enforced at the configuration layer via `config/agent-capabilities.json`, not just by prompt instructions.

**Capability matrix (SSOT):**

| Role | Read | Write | Shell | Browser | Memory Write |
|:-----|:-----|:------|:------|:--------|:-------------|
| Orchestrator | Yes | No | No | No | Yes |
| Architect | Yes | No | No | Limited (snapshot/screenshot) | No |
| Executor | Yes | Yes | Yes | Yes | Yes |
| Verifier | Yes | No | Limited | Yes | No |

**Policy engine:**
- `akos/policy.py` loads the capability matrix and generates per-agent tool profiles.
- `GET /agents/{id}/policy` returns the effective tool list for any agent.
- `GET /agents/{id}/capability-drift` reports mismatches between policy and runtime.

**Audit procedure:**
After any change to agent tools or permissions:
1. Update `config/agent-capabilities.json`.
2. Verify via `GET /agents/{id}/policy`.
3. Confirm no drift via `GET /agents/{id}/capability-drift`.

### **9.5 Semantic Code Intelligence**

v0.4.0 adds LSP and code-search MCP servers for type-aware code navigation (Phase 4).

**MCP servers added:**
- `lsp` (`@akos/mcp-lsp-server`) -- `get_diagnostics(file)`, `go_to_definition(symbol)`, `find_references(symbol)`, `get_type_signature(symbol)`.
- `code-search` (`@akos/mcp-code-search`) -- `search_code(query, scope)` via ripgrep + tree-sitter.

**Agent usage:**
- Architect: use LSP tools to trace dependencies before drafting plans.
- Executor: run `get_diagnostics()` after edits, before handing off to Verifier.
- Verifier: check `get_diagnostics()` as part of verification.

**Research protocol:**
`prompts/overlays/OVERLAY_RESEARCH.md` defines citation requirements: cite source origin and freshness, distinguish `[FACT]` from `[INFERENCE]`, state uncertainty when confidence < 80%.

### **9.6 Workflow Definitions and Dashboard UX**

Reusable workflow specs in `config/workflows/` structure common tasks with explicit agent sequences, tool requirements, approval points, and completion criteria.

**Available workflows:**

| Workflow | Agents | Purpose |
|:---------|:-------|:--------|
| `analyze_repo` | Architect, Orchestrator | Full codebase analysis |
| `implement_feature` | Architect, Executor, Verifier | Plan + implement + verify |
| `verify_changes` | Verifier | Lint, test, build, screenshot |
| `browser_smoke` | Verifier | Dashboard browser validation |
| `deploy_check` | Architect, Verifier | Deployment readiness |
| `incident_review` | Architect, Orchestrator | Root cause + remediation |

**Creating new workflows:**
Add a `.md` file to `config/workflows/` with: Agent Sequence, Required Tools, Steps (checkboxes), Approval Points, Completion Criteria.

### **9.7 Memory Packs and Evidence Retrieval**

v0.4.0 extends the flat memory architecture (no GraphRAG) with structured memory domains and citation requirements.

**Memory domains:**
- `memory/decisions/` -- architecture and design decisions
- `memory/policies/` -- governance and operational policies
- `memory/incidents/` -- incident reports and lessons learned
- `memory/sources/` -- curated reference materials

**Citation requirements:**
For planning, research, and compliance outputs: cite source origin, cite freshness, distinguish facts from inferences, retain confidence markers.

**Context pinning:**
Operators and workflows can pin critical context (repo files, docs, memory items, policies, current goal) to keep agent focus.

### **9.8 Deployment Pipeline and Operational Tooling**

**Operator scripts:**

| Script | Purpose | Usage |
|:-------|:--------|:------|
| `scripts/doctor.py` | One-command system health check | `py scripts/doctor.py` |
| `scripts/sync-runtime.py` | Hydrate runtime from repo SSOT | `py scripts/sync-runtime.py` |
| `scripts/release-gate.py` | Unified release gate (tests + drift) | `py scripts/release-gate.py` |
| `scripts/check-drift.py` | Detect repo-to-runtime drift | `py scripts/check-drift.py` |

**Infrastructure auto-failover:**
If RunPod health check fails 3 consecutive times, auto-switch to cloud API fallback. If cloud fails, fall back to local Ollama. Emit `INFRA_FAILOVER_TRIGGERED` SOC alert. Periodically re-check failed provider; restore when healthy.

**Environment promotion:**
Formal deployment lanes: `dev-local` -> `gpu-runpod` -> `prod-cloud`. Each promotion requires: all tests pass, drift check clean, browser smoke pass.

### **9.9 Evaluation Release Gates**

v0.4.0 formalizes three testing lanes as a hard release gate.

**Lane 1 -- Offline regression:**
```
py scripts/test.py all
```
193+ tests covering: config validation, Pydantic models, alert evaluation, RunPod provider, FastAPI endpoints, checkpoints, prompt structure, E2E wiring, scaffolding integrity.

**Lane 2 -- Browser/gateway smoke:**
Canonical scenarios defined in `docs/uat/dashboard_smoke.md`:
- `dashboard_health` -- page loads, no errors
- `agent_visibility` -- all 4 agents visible
- `architect_read_only` -- Architect produces plans, no file writes
- `executor_approval_flow` -- mutative actions require HITL approval
- `workflow_launch` -- at least one workflow invocable
- `prompt_injection_refusal` -- harmful prompts refused

**Lane 3 -- Live provider smoke (opt-in):**
```
AKOS_LIVE_SMOKE=1 py scripts/test.py live
```
Tests: health endpoint live, agents endpoint returns 4 agents.

**Release gate procedure:**
```
py scripts/release-gate.py
```
Runs Lane 1 + drift check. Reports PASS/FAIL. If `AKOS_LIVE_SMOKE=1`, notes live tests should also pass.

**Governance packs (Phase 8):**
- Policy packs in `config/policies/` define named governance profiles (engineering-safe, compliance-review, incident-response).
- Workflow packs in `config/workflow-packs/` provide team-distributable workflow collections.

### **9.10 Version History**

See `CHANGELOG.md` for the full version history from v0.0.1 to v0.5.0.

### **9.11 Gateway Runtime Wiring (v0.5.0)**

Bootstrap acts as the **translation layer** between AKOS's design-time SSOT and OpenClaw's runtime enforcement. Policy is defined once in AKOS files, bootstrap pushes it to OpenClaw's config schema, and the dashboard shows the live state. The operator never manually edits the OpenClaw Config page.

- **Per-agent tool profiles** — Each agent's `tools.profile` (minimal/coding) and allow/deny lists are translated from `config/agent-capabilities.json` by bootstrap. Orchestrator and Architect use `minimal`; Executor and Verifier use `coding` (Verifier with explicit deny for write_file, delete_file, git_push, git_commit).
- **Exec security** — `tools.exec.security` is set per AKOS policy (allowlist for Executor, deny for Architect). Orchestrator/Architect must never have `full` exec access.
- **Loop detection** — Gateway-level repetition circuit breaker (`tools.loopDetection`) provides defense-in-depth with AKOS prompt-level loop detection.
- **Agent-to-agent** — `tools.agentToAgent` enables Orchestrator delegation at runtime level. `tools.agentToAgent.allow` restricts which agents can be invoked.
- **Session policy** — `session.reset` (idle timeout 60 min), `session.typingMode` (thinking mode), and `session.agentToAgent.maxPingPongTurns` are configured by bootstrap.
- **Browser SSRF policy** — `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork: false` restricts private network access during browser automation.

See [ARCHITECTURE.md](ARCHITECTURE.md#bootstrap-translation-layer-v050) for the full translation layer design.

### **9.12 Browser UAT with Playwright**

Automated browser smoke tests validate the dashboard and control plane without manual interaction.

**Prerequisites:** `pip install playwright && playwright install chromium`

**Commands:**
- `py scripts/browser-smoke.py` — HTTP-only checks (gateway, Swagger) when gateway is reachable
- `py scripts/browser-smoke.py --playwright` — Full DOM-based checks (dashboard health, agent visibility, Swagger health, Architect tools UI, Executor approval hint, workflow launch)
- `py scripts/browser-smoke.py --playwright --headed` — Same as above, with visible browser window

**Test groups:** Run via `py scripts/test.py browser`. The release gate invokes browser smoke when Playwright is installed.

**Phase 2 (Architect/Executor):** The architect_tools_ui and executor_approval_hint checks navigate to `/agents`, wait for agent cards to load, then click the Architect and Executor cards to verify tools and approval hints.

**Platform separation:** AKOS uses **Playwright MCP** (in agent runtime) for Verifier screenshots and browser automation. The **browser-smoke.py** script is operator tooling for UAT and release gates. **cursor-ide-browser** is a Cursor IDE built-in (optional) for in-IDE WebChat testing — AKOS does not depend on it. See [USER_GUIDE §9.6](docs/USER_GUIDE.md#96-cursor-ide-browser-cursor-ide-only-optional) and [ARCHITECTURE.md](docs/ARCHITECTURE.md).

### **9.13 Governance-Hardened Remediation Execution Ledger (March 2026)**

This ledger is the immutable execution record for the governance-hardened runtime/inventory remediation.

**Locked constraints (scope lock):**
- Inventory mode is **full-only** and must match the exact AKOS contract (no active/relaxed/profile mode).
- Git policy is **one commit per phase**.
- Reuse/extension only: existing scripts, models, and validators are extended; no parallel sidecar frameworks.

**Baseline command set (reproducible):**
- `openclaw gateway status`
- `openclaw status`
- `py -3 scripts/legacy/verify_openclaw_inventory.py`
- `py -3 scripts/check-drift.py`
- `py -3 scripts/test.py all`
- `py -3 scripts/release-gate.py`

**Baseline snapshot (Phase 0 capture):**
- `openclaw gateway status`: `RPC probe: ok`, `Listening: 127.0.0.1:18789`, and `Runtime: unknown`.
- `openclaw status`: gateway reachable, service listed as scheduled task with `unknown` service state.
- `verify_openclaw_inventory.py`: `OVERALL: FAIL` due to provider set mismatch and missing `tools.agentToAgent.allow`.
- `check-drift.py`: PASS (`No drift detected. Runtime matches repo state.`).
- `test.py all`: PASS (195 passed, 2 skipped).
- `release-gate.py`: FAIL due to browser smoke crash (`scripts/browser-smoke.py --playwright` exit 3221225477 on Windows).

**Frozen acceptance criteria by phase:**
- Phase 1: Runtime status contract no longer reports ambiguous unknown state when probe/listener are healthy.
- Phase 2: strict inventory verification returns `OVERALL: PASS` with exact full AKOS provider/model/allowlist contract.
- Phase 3: sensitive-key signals have explicit severity and action text; logs never expose secret values.
- Phase 4: full matrix (`strict inventory`, `drift`, `test.py all`, `browser smoke`, `release gate`) passes.
- Phase 5: required docs are synchronized and consistent with verified behavior.
- Phase 6: exactly one commit per phase (plus optional final audit commit only if needed), then push.

**Phase 1 execution note (runtime contract hardening):**
- Runtime interpretation is normalized via AKOS diagnostics: when `RPC probe: ok` and a listener is present, runtime is classified as `healthy` even if raw OpenClaw service metadata reports `unknown`.
- Determinism gate: runtime normalization is validated across 3 repeated probes in `py scripts/doctor.py`.

---

#### **Works cited**

1. Enhancing OpenCLAW Agentic Capabilities, [https://drive.google.com/open?id=1v3FXuWFzAqXVFh9dgCUTFK-xUfWypR9lRgliuy9fsmU](https://drive.google.com/open?id=1v3FXuWFzAqXVFh9dgCUTFK-xUfWypR9lRgliuy9fsmU)  
2. Kirbe Strategy: Holistika Ecosystem Integration  
3. OpenClaw x AWS EC2 x AnChain.AI Data MCP: Build Your 24x7 AML Compliance Officer AI Agent (For Free), accessed March 1, 2026, [https://www.anchain.ai/blog/openclaw](https://www.anchain.ai/blog/openclaw)  
4. How OpenClaw Works: Understanding AI Agents Through a Real ..., accessed March 1, 2026, [https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764](https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764)  
5. punkpeye/awesome-mcp-servers \- GitHub, accessed March 1, 2026, [https://github.com/punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)  
6. Hundreds of Malicious Skills Found in OpenClaw's ClawHub | eSecurity Planet, accessed March 1, 2026, [https://www.esecurityplanet.com/threats/hundreds-of-malicious-skills-found-in-openclaws-clawhub/](https://www.esecurityplanet.com/threats/hundreds-of-malicious-skills-found-in-openclaws-clawhub/)  
7. Researchers Find 341 Malicious ClawHub Skills Stealing Data from OpenClaw Users \- The Hacker News, accessed March 1, 2026, [https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)  
8. Matriz de Inteligencia \- Copia de Facts.csv  
9. Holistika: A Framework for Business Logic and Growth  
10. Optimizing Splunk Enterprise Security for your SOC, accessed March 1, 2026, [https://lantern.splunk.com/Security\_Use\_Cases/Automation\_and\_Orchestration/Optimizing\_Splunk\_Enterprise\_Security\_for\_your\_SOC](https://lantern.splunk.com/Security_Use_Cases/Automation_and_Orchestration/Optimizing_Splunk_Enterprise_Security_for_your_SOC)  
11. Developer Experience (DevEx) in 2026 \- DEV Community, accessed March 1, 2026, [https://dev.to/austinwdigital/developer-experience-devex-in-2026-the-real-competitive-advantage-2996](https://dev.to/austinwdigital/developer-experience-devex-in-2026-the-real-competitive-advantage-2996)  
12. AI Act Compliance Checklist: Your 2026 Survival Guide (With Free Template) \- Medium, accessed March 1, 2026, [https://medium.com/@vicki-larson/ai-act-compliance-checklist-your-2026-survival-guide-with-free-template-44cdcd8fbf8e](https://medium.com/@vicki-larson/ai-act-compliance-checklist-your-2026-survival-guide-with-free-template-44cdcd8fbf8e)  
13. PIXIE \- Proyecto Data Governance \- Larga Duración, [https://mail.google.com/mail/u/0/\#all/FMfcgzQfBsnWcqmjtFtbZKbNFJTQlgrV](https://mail.google.com/mail/u/0/#all/FMfcgzQfBsnWcqmjtFtbZKbNFJTQlgrV)  
14. process\_list\_1 \- process\_list\_1 (2).csv  
15. Top 10 MCP Servers for Cybersecurity in 2026 \- Levo.ai, accessed March 1, 2026, [https://www.levo.ai/resources/blogs/top-mcp-servers-for-cybersecurity-2026](https://www.levo.ai/resources/blogs/top-mcp-servers-for-cybersecurity-2026)  
16. CVE-2026-24763 \- NVD, accessed March 1, 2026, [https://nvd.nist.gov/vuln/detail/CVE-2026-24763](https://nvd.nist.gov/vuln/detail/CVE-2026-24763)  
17. OpenClaw Security Guide 2026 | Contabo Blog, accessed March 1, 2026, [https://contabo.com/blog/openclaw-security-guide-2026/](https://contabo.com/blog/openclaw-security-guide-2026/)  
18. Install openclaw on windows the right way \- Friends of the Crustacean, accessed March 1, 2026, [https://www.answeroverflow.com/m/1466683796874330337](https://www.answeroverflow.com/m/1466683796874330337)  
19. Windows 11: WSL2 vs Native — real-world experience, gotchas, and recommended approach for running OpenClaw \#7462 \- GitHub, accessed March 1, 2026, [https://github.com/openclaw/openclaw/discussions/7462](https://github.com/openclaw/openclaw/discussions/7462)  
20. Install WSL | Microsoft Learn, accessed March 1, 2026, [https://learn.microsoft.com/en-us/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install)  
21. GitHub \- VoltAgent/awesome-openclaw-skills, accessed March 1, 2026, [https://github.com/VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)  
22. Run OpenClaw Securely in Docker Sandboxes, accessed March 1, 2026, [https://www.docker.com/blog/run-openclaw-securely-in-docker-sandboxes/](https://www.docker.com/blog/run-openclaw-securely-in-docker-sandboxes/)  
23. How do i get openclaw to connect to my custom mcp? \- Friends of the Crustacean, accessed March 1, 2026, [https://www.answeroverflow.com/m/1473249738492088450](https://www.answeroverflow.com/m/1473249738492088450)  
24. openclaw/openclaw: Your own personal AI assistant. Any OS. Any Platform. The lobster way. \- GitHub, accessed March 1, 2026, [https://github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)  
25. OpenClaw Config Example (Sanitized) \- GitHub Gist, accessed March 1, 2026, [https://gist.github.com/digitalknk/4169b59d01658e20002a093d544eb391](https://gist.github.com/digitalknk/4169b59d01658e20002a093d544eb391)  
26. OpenClaw Capabilities Matrix: Complete Guide to 7 Core Modules ..., accessed March 1, 2026, [https://eastondev.com/blog/en/posts/ai/20260204-openclaw-capabilities-matrix/](https://eastondev.com/blog/en/posts/ai/20260204-openclaw-capabilities-matrix/)  
27. 02/08/2026 \- OpenClaw Architecture Deep Dive \- HackMD, accessed March 1, 2026, [https://hackmd.io/Z39YLHZoTxa7YLu\_PmEkiA](https://hackmd.io/Z39YLHZoTxa7YLu_PmEkiA)  
28. Canvas \- OpenClaw, accessed March 1, 2026, [https://beaverslab.mintlify.app/en/platforms/mac/canvas](https://beaverslab.mintlify.app/en/platforms/mac/canvas)  
29. How to Run OpenClaw Safely Across Platforms (Windows, macOS, Linux) \- Knolli.ai, accessed March 1, 2026, [https://www.knolli.ai/post/how-to-run-openclaw-safely](https://www.knolli.ai/post/how-to-run-openclaw-safely)  
30. mcporter | Skills Marketplace \- LobeHub, accessed March 1, 2026, [https://lobehub.com/skills/openclaw-openclaw-mcporter](https://lobehub.com/skills/openclaw-openclaw-mcporter)  
31. Sequential Thinking \- Awesome MCP Servers, accessed March 1, 2026, [https://mcpservers.org/servers/arben-adm/mcp-sequential-thinking](https://mcpservers.org/servers/arben-adm/mcp-sequential-thinking)  
32. @modelcontextprotocol/server-sequential-thinking | MCP Package Details & Installation Guide, accessed March 1, 2026, [https://mcp-get.com/packages/%40modelcontextprotocol%2Fserver-sequential-thinking](https://mcp-get.com/packages/%40modelcontextprotocol%2Fserver-sequential-thinking)  
33. Top 10 Agentic AI Design Patterns | Enterprise Guide \- Aufait UX, accessed March 1, 2026, [https://www.aufaitux.com/blog/agentic-ai-design-patterns-enterprise-guide/](https://www.aufaitux.com/blog/agentic-ai-design-patterns-enterprise-guide/)  
34. Sequential Thinking MCP Server \- modelcontextprotocol/servers/sequentialthinking, accessed March 1, 2026, [https://playbooks.com/mcp/modelcontextprotocol/servers/sequentialthinking](https://playbooks.com/mcp/modelcontextprotocol/servers/sequentialthinking)  
35. README.md \- Sequential Thinking MCP Server \- GitHub, accessed March 1, 2026, [https://github.com/modelcontextprotocol/servers/blob/main/src/sequentialthinking/README.md](https://github.com/modelcontextprotocol/servers/blob/main/src/sequentialthinking/README.md)  
36. MCP server with 300+ local tools (Playwright browser automation, DB, notifications, docs parsing) — works with Continue/Cline/LM Studio : r/LocalLLaMA \- Reddit, accessed March 1, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1r31op2/mcp\_server\_with\_300\_local\_tools\_playwright/](https://www.reddit.com/r/LocalLLaMA/comments/1r31op2/mcp_server_with_300_local_tools_playwright/)  
37. Playwright MCP Server Is Here: Let's Integrate It\! | HackerNoon, accessed March 1, 2026, [https://hackernoon.com/playwright-mcp-server-is-here-lets-integrate-it](https://hackernoon.com/playwright-mcp-server-is-here-lets-integrate-it)  
38. playwright-mcp | Skills Marketplace \- LobeHub, accessed March 1, 2026, [https://lobehub.com/de/skills/darraghh1-my-claude-setup-playwright-mcp](https://lobehub.com/de/skills/darraghh1-my-claude-setup-playwright-mcp)  
39. A2A MCP Server Playwright For Web Automation | by Vishal Mysore \- Medium, accessed March 1, 2026, [https://medium.com/@visrow/a2a-mcp-server-playwright-for-web-automation-700ff657f8da](https://medium.com/@visrow/a2a-mcp-server-playwright-for-web-automation-700ff657f8da)  
40. \[GitHub\] Payment Receipt for FraysaXII, [https://mail.google.com/mail/u/0/\#all/FMfcgzQfCDQjNCfkGlFFFqpJzHgNqRxK](https://mail.google.com/mail/u/0/#all/FMfcgzQfCDQjNCfkGlFFFqpJzHgNqRxK)  
41. OpenClaw AI Agent Vulnerabilities: Detection and Removal for Mac \- Jamf, accessed March 1, 2026, [https://www.jamf.com/blog/openclaw-ai-agent-insider-threat-analysis/](https://www.jamf.com/blog/openclaw-ai-agent-insider-threat-analysis/)  
42. Malicious OpenClaw 'skill' targets crypto users on ClawHub — 14 malicious skills were uploaded to ClawHub last month | Tom's Hardware, accessed March 1, 2026, [https://www.tomshardware.com/tech-industry/cyber-security/malicious-moltbot-skill-targets-crypto-users-on-clawhub](https://www.tomshardware.com/tech-industry/cyber-security/malicious-moltbot-skill-targets-crypto-users-on-clawhub)  
43. skillvet | Skills Marketplace \- LobeHub, accessed March 1, 2026, [https://lobehub.com/skills/openclaw-skills-skillvet](https://lobehub.com/skills/openclaw-skills-skillvet)  
44. skillvet \- Github \- LobeHub, accessed March 1, 2026, [https://lobehub.com/zh/skills/openclaw-skills-skillvet](https://lobehub.com/zh/skills/openclaw-skills-skillvet)  
45. Unleashing OpenClaw: The Ultimate Guide to Local AI Agents for Developers in 2026 \- DEV Community, accessed March 1, 2026, [https://dev.to/mechcloud\_academy/unleashing-openclaw-the-ultimate-guide-to-local-ai-agents-for-developers-in-2026-3k0h](https://dev.to/mechcloud_academy/unleashing-openclaw-the-ultimate-guide-to-local-ai-agents-for-developers-in-2026-3k0h)  
46. Is it possible to integrate router logs into ELK or Splunk? Is the log format JSON?, accessed March 1, 2026, [https://www.tencentcloud.com/techpedia/137958](https://www.tencentcloud.com/techpedia/137958)  
47. SOC Automation Project — Using Splunk, n8n, OpenAI, and Slack | by Annie Wong, accessed March 1, 2026, [https://medium.com/@anniehswong/soc-automation-project-automated-detection-ai-enriched-incident-response-with-splunk-n8n-e6368bb0955f](https://medium.com/@anniehswong/soc-automation-project-automated-detection-ai-enriched-incident-response-with-splunk-n8n-e6368bb0955f)  
48. TryHackme | Splunk: Setting up a SOC Lab WriteUp | by DefenderFela \- Medium, accessed March 1, 2026, [https://medium.com/@abhishek.rk96/tryhackme-splunk-setting-up-a-soc-lab-1fba3ab043de](https://medium.com/@abhishek.rk96/tryhackme-splunk-setting-up-a-soc-lab-1fba3ab043de)  
49. Openclaw Setup: From Zero to First Chat in 10 Minutes (2026 Edition) \- Adven Boost, accessed March 1, 2026, [https://advenboost.com/openclaw-setup-fast-tutorial/](https://advenboost.com/openclaw-setup-fast-tutorial/)  
50. Solved: Elastic Integrator App \- Splunk Community, accessed March 1, 2026, [https://community.splunk.com/t5/Getting-Data-In/Elastic-Integrator-App/m-p/710756](https://community.splunk.com/t5/Getting-Data-In/Elastic-Integrator-App/m-p/710756)  
51. Security \- OpenClaw, accessed March 1, 2026, [https://docs.openclaw.ai/gateway/security](https://docs.openclaw.ai/gateway/security)  
52. EU AI Act Compliance Checklist: 7 Steps to Prepare Your Business in 2026 \- DSALTA, accessed March 1, 2026, [https://www.dsalta.com/resources/ai-compliance/eu-ai-act-compliance-checklist-7-steps-to-prepare-your-business-in-2026](https://www.dsalta.com/resources/ai-compliance/eu-ai-act-compliance-checklist-7-steps-to-prepare-your-business-in-2026)  
53. AI Evaluation Metrics 2026: Tested by Conversation Experts \- Master of Code, accessed March 1, 2026, [https://masterofcode.com/blog/ai-agent-evaluation](https://masterofcode.com/blog/ai-agent-evaluation)  
54. Agent Evaluation Framework 2026: Metrics, Rubrics & Benchmarks \- Galileo AI, accessed March 1, 2026, [https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks](https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks)  
55. AI tooling benchmarks: PR throughput and usage by tool (Q1 2026), accessed March 1, 2026, [https://getdx.com/blog/ai-tooling-benchmarks-pr-throughput-and-usage-by-tool/](https://getdx.com/blog/ai-tooling-benchmarks-pr-throughput-and-usage-by-tool/)  
56. How 18 companies measure AI's impact in engineering, accessed March 1, 2026, [https://getdx.com/blog/how-top-companies-measure-ai-impact-in-engineering/](https://getdx.com/blog/how-top-companies-measure-ai-impact-in-engineering/)  
57. Top 5 AI Agent Evaluation Tools in 2026 \- Maxim AI, accessed March 1, 2026, [https://www.getmaxim.ai/articles/top-5-ai-agent-evaluation-tools-in-2026/](https://www.getmaxim.ai/articles/top-5-ai-agent-evaluation-tools-in-2026/)