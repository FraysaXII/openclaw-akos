---
report_type: uat-evidence
intellectual_kind: uat_report
parent_initiative: INIT-OPENCLAW_AKOS-90
phase: P4b
sharing_label: internal_only
authored: 2026-06-14
authored_by: PMO
last_review: 2026-06-14
audience: J-OP
language: en
status: closed
verdict: PASS-WITH-FOLLOWUP
closure_decision_source: agent_inline_default
evidence_class: browser_experiential
evidence_proof_ref: artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/MANIFEST.json
ratifying_decisions:
  - D-IH-90-AF
linked_canonicals:
  - EVIDENCE_CLASS_GATE_DISCIPLINE.md
  - SOP-PMO_EVIDENCE_CLASS_GATE_001.md
linked_runbooks:
  - scripts/run_automated_uat_evidence_sweep.py
  - scripts/lab_platform_registry_reconcile.py
verdict_followup_rationale:
  followup_class: monitoring-obligation
  closure_target: "browser-smoke gateway scenarios PASS after openclaw gateway run warmup"
  owner: System Owner
  tracker_path: docs/wip/planning/_trackers/carryover-posture-index.md
  notes: >-
    Preview vertical slice proof complete (10 PNGs + MANIFEST + live Preview 401 probe).
    Local gateway config repaired (sandbox.mode strict to off); HTTP/RPC still hang after
    ready — CO-90-004 scheduled, not dropped.
---

# I90 P4b — Preview evidence-class gate vertical slice (2026-06-14)

> **Outcome:** The evidence-class gate now has a **worked consumer proof** — hlk-erp Preview
> Research Center with `browser_experiential` manifest bound to closure UAT frontmatter.
> Local AKOS gateway smoke remains **scheduled follow-up** (`CO-90-004`).

## Section 1 — Closure summary

| Dimension | Target | Actual | Status |
|:---|:---|:---|:---:|
| **Verdict** | PASS or PWF with honest proof | PASS-WITH-FOLLOWUP | PASS |
| **Preview deploy live** | Vercel Preview READY | HTTP 401 auth gate on Preview host (deploy alive) | PASS |
| **Browser experiential proof** | >=8 journey PNGs + MANIFEST | 10/10 captures; validator PASS | PASS |
| **Evidence-class gate cross-check** | validate_evidence_class_gate PASS | PASS | PASS |
| **Lab registry reconcile** | registry-only or live probe | registry-only PASS (vercel CLI absent) | PASS |
| **Local AKOS gateway smoke** | browser-smoke gateway scenarios | HTTP timeout post-ready; CLOSE_WAIT | PWF |
| **Operator sign-off** | 7-item checklist | agent_inline_default | PWF |

**Closure decision:** P4b slice **closes with follow-up** on local gateway only. Preview proof satisfies the federated gate bar for consumer surfaces.

## Section 2 — Closure-criteria verification

| # | Closure criterion | Verification command | Expected | Actual | Status |
|:---|:---|:---|:---|:---|:---:|
| 1 | P4c+ singularity landed | git log -1 --oneline | P4c commit present | `32521d2f` on branch | PASS |
| 2 | Preview MANIFEST sha256 rows | `py scripts/validate_uat_screenshot_evidence.py --session-dir artifacts/uat-screenshots/i96-research-center-preview-2026-06-13` | exit 0 | PASS (WARN=0) | PASS |
| 3 | Evidence-class gate | `py scripts/validate_evidence_class_gate.py` | exit 0 | PASS | PASS |
| 4 | Preview host reachable | HTTP GET Preview `/research-center` | non-5xx | 401 (auth required) | PASS |
| 5 | Lab platform reconcile | `py scripts/lab_platform_registry_reconcile.py` | registry PASS | PASS (8 Vercel rows; live probe SKIP) | PASS |
| 6 | Local gateway browser-smoke | `py scripts/browser-smoke.py --playwright` | gateway scenarios PASS | gateway HTTP hang | FAIL |
| 7 | Automated UAT sweep | `py scripts/run_automated_uat_evidence_sweep.py` | exit 0 | evidence gate PASS; `--all` historical UAT debt | PWF |

## Section 3 — Mechanical evidence

### §3.1 Validators

```text
py scripts/validate_uat_screenshot_evidence.py --session-dir artifacts/uat-screenshots/i96-research-center-preview-2026-06-13
  PASS — screenshot evidence clean (WARN=0)

py scripts/validate_evidence_class_gate.py
  PASS: evidence-class gate (initiative closure cross-check)

py scripts/lab_platform_registry_reconcile.py
  PASS (registry-only; vercel CLI not on PATH — live probe SKIP per I100 R-IH-100-2)

py scripts/run_automated_uat_evidence_sweep.py
  evidence gate + registry validators PASS; validate_uat_report --all exits 1 on historical WIP UAT shape debt (not P4b scope)
```

### §3.2 Preview deploy verification

| Field | Value |
|:---|:---|
| Platform | Vercel |
| Hostname | `https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app` |
| PR | [#36](https://github.com/FraysaXII/hlk-erp/pull/36) |
| Deploy ID | `5VYPNb5wyNfWHisS26X6hfnh9qcq` |
| Source SHA | `eedcd1d` |
| Vendor state | READY (MANIFEST) |
| Live probe (2026-06-14) | GET `/research-center` → **401** (auth gate; not 5xx) |

### §3.3 Browser-evidence pattern (browser_experiential)

**Evidence bundle:** [`artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/MANIFEST.json`](../../../../artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/MANIFEST.json)

| # | Journey | Viewport | POV | SHA256 (prefix) | Verdict |
|:---|:---|:---|:---|:---|:---:|
| 1–4 | operator discover→audit | 1280 | operator | 9c20… / c113… / faed… / 03e9… | PASS |
| 5–8 | director discover→audit | 1280 | director | c092… / 841b… / be15… / 841b… | PASS |
| 9–10 | planning index + I96 detail | 1280 | — | ee2c… / f11f… | PASS |

Auth: magic-link operator session (L3.5 Preview). Capture tool: Cursor Browser MCP.

### §3.4 Local gateway remediation attempted

| Step | Result |
|:---|:---|
| Fix invalid `sandbox.mode: strict` → `off` (OpenClaw 2026.4.x allows off/non-main/all) | Config valid |
| `tools.exec.host` → `gateway` when sandbox off | Applied |
| `openclaw gateway run` (foreground) | Log: **ready** @ ~48s |
| HTTP GET `127.0.0.1:18789/` | **Timeout** (CLOSE_WAIT accumulation) |
| `openclaw gateway call health` | Timeout / 1006 closure |

## Section 4 — Per-dimension findings

| Dimension | Finding | Disposition |
|:---|:---|:---|
| Preview browser_experiential | 10 PNGs + MANIFEST; validator clean | PASS |
| live_probe (Preview) | Deploy READY + HTTP 401 auth | PASS |
| live_probe (AKOS gateway) | Listener up; HTTP/RPC hang | PWF → CO-90-004 |
| git_shape | PR #36 + SHA in MANIFEST | PASS |
| UAT sweep `--all` | Historical WIP reports missing sections | scheduled (not P4b scope) |

## Section 5 — D-IH-86-D mechanical cross-check

N/A — P4b is an evidence supplement under I90 (`D-IH-90-AF`), not an I86 wave-close. Cross-check satisfied via `validate_evidence_class_gate.py` import of `akos.evidence_class_gate` shared with I86 validators.

## Section 6 — SOP + runbook pair

| SOP | Runbook | Status |
|:---|:---|:---:|
| `SOP-PMO_EVIDENCE_CLASS_GATE_001.md` | `scripts/run_automated_uat_evidence_sweep.py` | PASS (self-test + sweep artifact) |

## Section 7 — Risk register closure

| Risk | Status |
|:---|:---:|
| Shape-only PASS without browser proof (I100 FM-13 class) | **Mitigated** — manifest bound |
| Preview auth dev-password false PASS | **Avoided** — magic-link bundle used |
| Gateway down blocks AKOS dashboard UAT | **Open** — CO-90-004 |

## Section 8 — Decision close-outs

| Decision | Close-out |
|:---|:---|
| D-IH-90-AF (federated evidence-class gate) | P4b worked example: Preview slice + frontmatter binding |

## Section 9 — Closure registry edits

| Registry / index | Edit |
|:---|:---|
| Carryover `CO-90-001` | **superseded** — P4b slice closed |
| Carryover `CO-90-004` | **scheduled** — local gateway HTTP/RPC recovery |
| I90 master-roadmap §P4b | closed PWF |

## Section 10 — Verdict + operator sign-off checklist

**Verdict: PASS-WITH-FOLLOWUP**

| # | Item | Status |
|:---|:---|:---:|
| 1 | Preview manifest cites real deploy + SHA | PASS |
| 2 | evidence_class + evidence_proof_ref in frontmatter | PASS |
| 3 | Screenshot validator exit 0 | PASS |
| 4 | No dev-password false PASS on Preview | PASS |
| 5 | Gateway follow-up named + tracker row | PASS |
| 6 | Singularity tranche precedes slice (P4c+ first) | PASS |
| 7 | Operator would accept Preview proof as gate demo | PASS |

## Section 11 — Cross-references

- Slice spec: [`evidence-class-gate-phase-b-preview-slice-2026-06-14.md`](evidence-class-gate-phase-b-preview-slice-2026-06-14.md)
- Prep (superseded): [`p4b-preview-slice-prep-2026-06-14.md`](p4b-preview-slice-prep-2026-06-14.md)
- Singularity ratification: [`evidence-class-gate-singularity-ratification-2026-06-14.md`](evidence-class-gate-singularity-ratification-2026-06-14.md)
- I96 Preview context: [`../96-research-data-plane-and-research-center/reports/uat-i96-research-center-production-2026-06-14.md`](../96-research-data-plane-and-research-center/reports/uat-i96-research-center-production-2026-06-14.md)
- Sweep artifact: `artifacts/evidence-gate/uat-sweep-2026-06-14.json`
