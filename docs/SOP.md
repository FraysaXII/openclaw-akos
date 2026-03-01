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
| **Version & Revision Date** | 2.0 — March 2026 |

## **1.0 Executive Summary and Architectural Vision**

The contemporary landscape of autonomous software systems has shifted dramatically, moving rapidly from conversational interfaces to deep-execution architectures. Out-of-the-box, vanilla deployments of the OpenCLAW framework operate fundamentally as isolated, high-latency conversational agents. While they possess basic utility, they lack the persistent identity, deterministic workflow orchestration, and cognitive depth required to match sophisticated internal frameworks like the Kirbe Agentic Knowledge Operating System (AKOS) or proprietary solutions such as Gemini Deep Research and Cursor's dual-mode IDE planners.1

The analysis indicates that achieving an enterprise-grade, highly autonomous assistant requires transcending the concept of a rudimentary "chatbot" and architecting a Large Language Model Operating System (LLMOS). This transformation necessitates the integration of the Four-Layer LLMOS paradigm: a Control Plane (Gateway), an Integration Layer, an Execution Layer (Agent Runner), and an Intelligence Layer.1 When an agent is forced to simultaneously architect a solution and write the underlying syntax, it suffers from severe cognitive overload. This results in context degradation, systemic hallucinations, and infinite debugging loops.1 To overcome this, the architecture must embrace a dual-agent paradigm, separating the cognitive workload into an "Architect" (operating in a read-only, high-context planning mode) and an "Executor" (a fast, read-write model executing strict directives).1

Furthermore, the introduction of the Model Context Protocol (MCP) serves as the universal integration layer for this ecosystem, replacing brittle, bespoke API wrappers with standardized, discoverable tool schemas.4 By standardizing how models interact with external data sources, the agent can achieve exhaustive, multi-layered research capabilities.1

However, expanding an agent's capabilities to include filesystem access, continuous background processing, and deep browser automation introduces severe existential security risks. The discovery of the ClawHavoc campaign, which successfully distributed the Atomic Stealer (AMOS) malware via malicious ClawHub skills, dictates that a Zero-Trust, highly sandboxed operational posture is strictly mandatory.6

This Standard Operating Procedure (SOP) provides the exhaustive, step-by-step technical blueprints required to upgrade a vanilla OpenCLAW instance into a secure, modular, and deeply integrated LLMOS. It incorporates comprehensive Data Integration (DI) frameworks modeled on the Holistika intelligence methodology 8, Security Operations Center (SOC) logging protocols 10, Developer Experience (DX) evaluation metrics 11, and EU AI Act compliance mechanisms designed for the 2026 regulatory environment.12

## **2.0 The Holistika Methodological Trinity applied to Agentic Architecture**

The transformation of a vanilla OpenCLAW instance requires grounding the technical deployment in a robust business logic framework. Based on the Holistika corporate intelligence methodology, operational efficiency is contingent upon a deep understanding of the underlying logic governing the entity.9 For an AI agent to function as a corporate asset rather than a novelty, its architecture must reflect the "Methodological Trinity": Strategy, Tactics, and Processes.2

### **2.1 Strategy: The Agentic Knowledge Operating System (AKOS)**

The primary responsibility of the enterprise architecture is to define the agent's strategic direction. A vanilla OpenCLAW deployment acts as a passive responder; an upgraded LLMOS must act as an active participant.2 This is achieved by evolving the agent into an Agentic Knowledge Operating System (AKOS).2 The strategy dictates that the agent must not merely retrieve data, but must validate that data against defined methodologies, acting effectively as an automated consultant.2

This strategic layer is technically enforced through "Strict Mode" Logic and Data Governance frameworks.1 Recent industry demands for comprehensive data governance—including the structuring of Critical Data Elements (CDEs), data lineage coordination, and cross-functional alignment—highlight the necessity of moving beyond unstructured data retrieval.13 The agent's memory must utilize a Knowledge Graph (GraphRAG) that enforces predicate allowlists and confidence thresholds, ensuring the AI only forms relationships that possess a cryptographically verifiable "Source of Truth" (SSOT).2

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
3. **Define the Workspace Routing:** Configure the openclaw.json to route specific channels to dedicated workspaces. This isolation ensures that casual messages from WhatsApp do not pollute the context window of an agent performing intensive codebase analysis.  
   Modify \~/.openclaw/openclaw.json to include:  
   JSON  
   {  
     "gateway": {  
       "port": 18789,  
       "host": "127.0.0.1"  
     },  
     "workspaces": {  
       "deep\_research": {  
         "channels": \["telegram\_bot\_1", "slack\_engineering"\],  
         "mcpServers": {}  
       }  
     }  
   }

4. **Diagnostics:** Run the built-in diagnostic tool to validate syntax and dependencies: openclaw doctor \--fix.25

### **4.2 The A2UI Canvas Integration**

To emulate the sophisticated interfaces of modern proprietary tools, the LLMOS must move beyond terminal outputs. OpenCLAW supports an Agent-to-UI (A2UI) protocol, allowing the agent to dynamically render interactive web components, charts, and GraphRAG visualizations directly on a user-facing canvas.26

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

## **8.0 Cursor Agent Implementation Directives**

To operationalize this SOP effectively, the deployment should be orchestrated using an AI-assisted IDE (such as Cursor Planner). Provide the following precise directives to the Cursor agent to execute the deployment systematically under human supervision.

**Prompt Directives for Cursor Agent:**

1. **Phase 1: Environment Assessment:** "Execute a shell command to verify the current operating system. If Windows, confirm the presence of WSL2 and Ubuntu-24.04. If macOS/Linux, verify the installation of Docker Desktop and the Docker Model Runner. Halt and request user intervention if dependencies are missing."  
2. **Phase 2: Configuration Bootstrapping:** "Navigate to \~/.openclaw/ (create the directory if necessary). Read the current openclaw.json if it exists. If absent, generate a base JSON schema ensuring the daemon is bound exclusively to 127.0.0.1 on port 18789."  
3. **Phase 3: MCP Provisioning:** "Install the mcporter skill via the CLI. Create the \~/.mcporter/mcporter.json file. Inject the exact JSON blocks for the @modelcontextprotocol/server-sequential-thinking and @playwright/mcp@latest servers as defined in section 5.0 of this SOP. Ensure all JSON syntax is strictly valid."  
4. **Phase 4: Security Implementation:** "Clone the skillvet repository into the skills/ directory. Create a bash script utility (vet-install.sh) that aliases the safe-install.sh command so that all future skills are routed through the security scanner automatically. Set execution permissions using chmod 700."  
5. **Phase 5: Agent Prompts & Dual-Mode Setup:** "Create two markdown files in the workspace root: ARCHITECT\_PROMPT.md and EXECUTOR\_PROMPT.md. Populate the Architect prompt with instructions to exclusively use the sequential\_thinking tool for planning, restricting it from utilizing file-write or shell tools. Populate the Executor prompt to require reading the Architect's output before executing terminal commands."  
6. **Phase 6: Logging Configuration:** "Modify the OpenCLAW runtime configuration to output standard logs in structured JSON format to /opt/openclaw/logs/agent\_activity.json, preparing the directory for Splunk Universal Forwarder ingestion. Create the inputs.conf file structure for Splunk."

*Constraint to Cursor:* Execute these steps sequentially. You must request explicit human approval before initiating any mutative shell commands, network downloads, or file writes.

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