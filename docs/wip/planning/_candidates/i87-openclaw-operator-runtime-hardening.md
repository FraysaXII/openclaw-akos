---
candidate_id: I87
title: OpenClaw operator-runtime hardening (health-monitor escalation + plugin pinning + modelsConfig hygiene + gateway-token UX + SOP+runbook pairing)
status: candidate
authored: 2026-05-16
last_review: 2026-05-16
parent_initiatives: [84, 86]
related_initiatives: [09]
priority: 4
language: en
---

# I87 candidate — OpenClaw operator-runtime hardening

> **Spawned from substrate audit evidence.** Five-strand charter scope is recorded verbatim from [`openclaw-observed-symptoms-2026-05-16.md`](../../intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md) §2 (Proposed I87 charter scope). **I87** sits as the operational sibling to **I84** (research): I84 decides which substrate Holistika commits to long-term; I87 makes the currently deployed substrate stop bleeding silently.

## 1. Operating story

Operator-visible OpenClaw / gateway logs surfaced five symptom classes on 2026-05-16 (Docker sandbox churn, low LLM context warnings, gateway WebSocket auth churn, `plugins.allow` trust posture, bonjour self-heal — see audit §1 triage table). Research initiative **I84** owns substrate doctrine and competitive framing; **I87** owns **operator-runtime reliability**: escalation when health monitors loop failure without surfacing, explicit pinning for AKOS-authored plugins, modelsConfig hygiene so warnings stop lying, gateway-token session-loss investigation, and a **paired** triage SOP + executable runbook so every class routes to a governed action.

## 2. Scope

### 2a. In scope

Verbatim charter strands from audit §2:

| Strand | Scope | Effort | Cursor-rule operationalised |
|:---|:---|:---|:---|
| **P1 — Health-monitor escalation patch** | After N (default 3) consecutive 30-min cycles failing the same way, emit operator-visible escalation (Slack? toast? `OPERATOR_INBOX.md` row?). Closes the "silent multi-hour outage" failure mode. | ~1-2d | [`akos-governance-remediation.mdc`](../../../.cursor/rules/akos-governance-remediation.mdc) §"Runtime contract" verbatim: *"Treat `Runtime: unknown` as an observability contract bug, not a healthy state."* |
| **P2 — `plugins.allow` AKOS plugin pinning** | One-line config in `~/.openclaw/openclaw.json` to explicitly trust `akos-runtime-tools` (and any future AKOS-authored OpenClaw plugins). Optional: `scripts/validate_openclaw_plugin_pinning.py` validator (mirrors I77 P4.C wiring pattern in miniature). | ~0.5d | [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 2 (adapter/integration registry status metadata pattern adapted to plugin trust) |
| **P3 — modelsConfig hygiene patch** | Bump `ollama/qwen3:8b` ctx in the modelsConfig where it's registered (raise to 32K+ to clear the warn threshold) OR remove the model entry if unused since fallback to vLLM is happening anyway. Decide via inline-ratify. | ~0.5d | none-rule-specific; standard config hygiene |
| **P4 — Gateway-token auto-paste UX investigation** | Root cause Class #3 (control UI repeatedly losing the gateway token between sessions). Either OpenClaw upstream bug (file ticket; defer) OR operator-config issue (document the rotation flow in SOP). | ~1d (mostly investigation) | none-rule-specific; UX investigation |
| **P5 — `SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md` + paired runbook** | New SOP at `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/` documenting the 5 symptom classes + triage decision tree (start Docker Desktop / disable Docker-dependent agent in modelsConfig / rotate gateway token / pin `akos-runtime-tools`). Paired `scripts/openclaw_health_triage.py` runbook that scans the gateway log + reports symptom class + recommended action per class. | ~2-3d | [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 (SOP+runbook pairing — every executable process needs both surfaces) |

**Cross-cluster wiring** (verbatim from audit §2): I87 has no hard-blockers. Can run in any wave. **Recommended slot**: before I84 P4 ratification (Wave 3) so the `D-IH-84-B` substrate decision (OpenClaw vs Cursor-SDK vs hybrid) compares against the *patched* OpenClaw baseline, not the bleeding one.

### 2b. Out of scope

- **Substrate ratification** (OpenClaw vs Cursor SDK vs hybrid) — owned by **I84** P4 (`D-IH-84-B`).
- **Vault SSOT canonical mints** beyond the paired SOP + optional small validators — no new dimensional CSV families in I87 unless operator expands charter at P0.

### 2c. Cross-area touchpoints

- **Tech Lab / System Owner** (owner): runtime config, gateway logs, SOP+runbook pairing.
- **Research** (consumer): I84 P1 evidence may cite I87 patches as “patched baseline” for substrate comparison.
- **PMO / I86** (coordination): cluster wave spotlight may sequence I87 before I84 Wave 3 per recommended slot.

## 3. Phase shape (provisional; ratify at P0 charter)

| Phase | Effort | Deliverable | Gate |
|:---|:---|:---|:---|
| P0 — Charter | 0.5d | Inline-ratify sequencing vs I84 Wave 3; INIT/DECISION/OPS rows; master-roadmap mirror | operator approval |
| P1 — Escalation patch | 1-2d | Health-monitor escalation path + observable signal | validate_hlk if touching governed docs |
| P2 — Plugin pinning | 0.5d | `plugins.allow` one-liner + optional validator | inline-ratify |
| P3 — modelsConfig | 0.5d | Context bump or removal per inline-ratify | inline-ratify |
| P4 — Gateway-token UX | ~1d | Root-cause memo + ticket or SOP note | inline-ratify |
| P5 — SOP + runbook | 2-3d | Paired SOP + `scripts/openclaw_health_triage.py` | operator approval if new process_list row |
| **Total** | **~5-7d** | | |

## 4. Open conundrums (resolve at P0 charter via inline-ratify)

| ID | Question | Default verdict | Decision target |
|:---|:---|:---|:---|
| C-87-1 | Escalation sink: Slack vs toast vs OPERATOR_INBOX row vs all three behind feature flag? | OPERATOR_INBOX row first (low coupling) | D-IH-87-A |
| C-87-2 | Validator for `plugins.allow`: ship in P2 or defer to hygiene pass? | Ship miniature validator mirroring I77 P4.C wiring | D-IH-87-B |
| C-87-3 | modelsConfig: bump ctx vs delete unused Ollama row? | Inline-ratify with gateway log evidence | D-IH-87-C |

## 5. Cross-references

- **Evidence SSOT**: [`openclaw-observed-symptoms-2026-05-16.md`](../../intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md) §1–§3.
- **Cluster coordinator**: [`86-initiative-cluster-execution-coordinator/master-roadmap.md`](../86-initiative-cluster-execution-coordinator/master-roadmap.md) (I87 slot on wave diagram).
- **Prior hygiene initiative**: [`09-openclaw-hygiene/`](../09-openclaw-hygiene/master-roadmap.md) (gateway SSOT alignment precedent).
- **Governing rules**: [`akos-governance-remediation.mdc`](../../../.cursor/rules/akos-governance-remediation.mdc) · [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) · [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc).

## 6. Promotion criteria (to `active` initiative folder)

1. Operator ratifies C-87-1..3 at P0 inline-ratify.
2. Slot confirmed relative to **I84** P4 Wave 3 (recommended: execute I87 strands before substrate ratification batch).
3. System Owner bandwidth acknowledged for SOP + runbook pairing (P5).

## 7. Files this candidate will mint (when promoted)

- **NEW SOP**: `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md` (path per audit §2).
- **NEW runbook**: `scripts/openclaw_health_triage.py` (log scan + symptom class + recommended action).
- **OPTIONAL validator**: `scripts/validate_openclaw_plugin_pinning.py`.
- **MODIFIED**: operator-local `openclaw.json` / modelsConfig documentation in `docs/` or `USER_GUIDE.md` as surfaced by P4 UX outcome.
- **MODIFIED**: `INITIATIVE_REGISTRY.csv`, `DECISION_REGISTER.csv`, `OPS_REGISTER.csv`, `docs/wip/planning/_templates/INITIATIVE_DEPENDENCIES.md`, initiative folder under `docs/wip/planning/87-openclaw-operator-runtime-hardening/` (exact slug ratified at promotion).
