---
report_type: sop-runbook-pair
intellectual_kind: uat_methodology
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P-G5-preview-uat
sharing_label: internal_only
authored: 2026-06-14
audience: J-AIC
status: active
paired_runbook: scripts/validate_uat_screenshot_evidence.py
linked_ladder: research-center-experiential-uat-ladder-2026-06-12.md
incident_trigger: I96 Preview UAT v1 — agent claimed 8/8 journey PASS without reading PNGs; duplicate sha256 on director captures; sidebar-expanded crops passed as VALID
---

# SOP — Experiential UAT agent visual review (L3.0 binding)

> **Vault SSOT (promoted 2026-06-14):** [`SOP-PEOPLE_UAT_VISUAL_EVIDENCE_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UAT_VISUAL_EVIDENCE_001.md) under People UAT governance (**D-IH-96-K**). This planning copy is the I96 worked example + incident record; edit vault first for doctrine changes.

> **Functional name:** the rule that says *capture is not review* — an agent must **look at every screenshot** before a UAT verdict may cite it.
>
> **What it prevents:** PASS verdicts backed by favicon crops, duplicate files, or manifest fiction. **What it does not do:** replace operator L4 sign-off on check-links.

## Scope

All **L3 / L3.5 experiential walks** (localhost, Vercel Preview, production smoke) where `artifacts/uat-screenshots/<session>/` PNGs feed a `uat-*.md` verdict.

## Roles (single agent, four hats — no delegation split)

| Hat | Responsibility |
|:---|:---|
| **Capture** | Browser MCP or Playwright @ 1280×800; collapse sidebar before each shot |
| **Visual review (binding)** | **Same session, foreground parent agent** reads every PNG with the Read tool |
| **Knowledge manager** | Writes `agent_visual_review.json` + updates MANIFEST supersession |
| **UAT author** | Verdict line only after `validate_uat_screenshot_evidence.py` PASS |

**Forbidden:** Subagent or background worker marks VALID in workflow notes without the parent agent reading PNG bytes in the same turn chain.

## Procedure

### 1 — Capture hygiene (before shutter)

1. Set viewport **1280×800** (CDP `Emulation.setDeviceMetricsOverride`).
2. **Collapse sidebar** (`Collapse sidebar` / icon rail only).
3. Wait for **Research Center** heading + insight cards (not loader).
4. Journey stages: Discover → Triage → Act (drawer open) → Audit (accordion expanded).
5. Scroll audit panels into view before audit capture — do not reuse triage frame.

### 2 — Visual review (mandatory, non-delegable)

For **each** journey PNG:

1. `Read` the file (image).
2. Record in `agent_visual_review.json`:
   - `file`, `verdict` (`VALID` | `INVALID` | `SUPERSEDED`)
   - `observations` — plain-language: badge, POV, journey stage, key copy, env warnings
   - `reviewed_by`: `parent-agent-foreground`
3. **INVALID** if: favicon/loader only, sidebar-only crop, duplicate of another stage, missing Research Center heading.

### 3 — Mechanical gate (before UAT verdict)

```powershell
py scripts/validate_uat_screenshot_evidence.py --session-dir artifacts/uat-screenshots/<session>/
```

Exit **0** required. FAIL codes:

| Code | Meaning |
|:---|:---|
| `UAT-SS-01-DUP-HASH` | Two journey files are byte-identical |
| `UAT-SS-02-UNDERSIZE` | File &lt; 35KB — likely crop |
| `UAT-SS-03-MISSING-JOURNEY` | Missing lens/stage token |
| `UAT-SS-04-NO-VISUAL-REVIEW` | No `agent_visual_review.json` or missing rows |
| `UAT-SS-05-SUBAGENT-ONLY` | Review file marks delegation_allowed |
| `UAT-SS-06-INVALID-VISUAL` | Row verdict ≠ VALID |

### 4 — Supersession

When re-capturing, suffix `-v2` or bump MANIFEST `supersedes` — never delete v1; mark prior rows `SUPERSEDED` in visual review.

## Acceptance criteria

- [ ] `agent_visual_review.json` exists with 8 VALID journey rows (Operator + Director)
- [ ] `validate_uat_screenshot_evidence.py` PASS on session dir
- [ ] UAT report §browser evidence cites v2 files where v1 was INVALID
- [ ] Charter checklist L3.0 row checked

## Cross-references

- Ladder L3.0: [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md)
- Preview charter: [`uat-i96-research-center-preview-charter-2026-06-13.md`](uat-i96-research-center-preview-charter-2026-06-13.md)
- I96 incident report: [`uat-i96-research-center-preview-2026-06-13.md`](uat-i96-research-center-preview-2026-06-13.md) §recapture
