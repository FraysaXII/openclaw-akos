---
report_type: experiential-uat-walk
intellectual_kind: uat_evidence
parent_initiative: INIT-OPENCLAW_AKOS-96
wave: B1.5
authored: 2026-06-13
audience: J-OP;J-AIC
verdict: PASS-WITH-FOLLOWUP
ladder_tier: L3
capture_session: artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/
linked_charter: reports/p9b-wave-b1-revision-charter-2026-06-13.md
---

# I96 Research Center B1.5 — L3 experiential walk (2026-06-13)

> **Purpose:** Agent execution-seat experiential UAT for Wave B1.5 (insight-machine revision) on **Operator + Director** lenses @1280, with **mandatory L3.0 self-verify** on all PNGs before check-links READY.

## §1 Closure summary

| Target | Actual | Status |
|:---|:---|:---:|
| Re-capture B1.5 localhost screenshots (8 journey stages) | 8 PNGs + MANIFEST sha256 | **PASS** |
| L3.0 agent self-verify (Research Center heading + full UI) | 8/8 VALID (see workflow notes) | **PASS** |
| Operator + Director discover→triage→act→audit | Checklist below | **PASS-WITH-FOLLOWUP** |
| Impeccable vs P9b VIS-B blockers | Major items closed; 2 scheduled | **PWF** |
| Operator L4 ratify | Pending your production walk | **PENDING** |

**Verdict: PASS-WITH-FOLLOWUP** — B1.5 ships enough operator value to ratify with eyes open; follow-ups are production parity, IntelligenceOps register depth, and drawer charts (B1.5-02 stretch).

---

## §2 Dual-hat review

### Operator UX (J-OP)

The page now reads as an **ERP insight machine**, not a debug console. The **Local dev** deploy badge, persona one-liners (“Fix env gaps…”, “Program phase and research-pack completion”), and journey step strip (Discover → Triage → Act → Verify) give a clear first-run path. Operator sees **3 signals** with plain-language headlines (staleness register, KiRBe env, ledger coverage) and **navigate** primary CTAs (“Open intelligence register”, “Open KiRBe program”, “Open ledger summary”) — not clipboard-only drawer opens. Drawer runbook blocks show outcome / when / command with a copy button. v1 audit accordion expands with WIP pack list for expert review.

**Friction remaining:** Radar strip still shows empty queue on localhost (honest, but noisy next to critical cards). Global **RED** header pill lacks Research Center context. Operator discover and triage captures are pixel-identical (scroll did not change viewport) — acceptable for L3 but not ideal regression signal.

### Technical / governance (J-AIC)

| Axis | Assessment |
|:---|:---|
| **GOJ matrix** | JourneyStepIndicator, persona subtitle, InsightRailHeader, LensEmptyState N/A (cards present), prong strip @ discover — matrix rows for Operator/Director T2 **implemented** |
| **Dashboard synthesis** | Navigate CTAs + deploy badge land B1.5-01/04/05; **Recharts drawer charts (B1.5-02) not evidenced** in drawer captures — scheduled stretch |
| **Brand T0–T3** | No `fixture` chips on card face; no bare “BFF” on T0; technical paths relegated to drawer T3 accordion — **Gate B + VIS-B03 cleared on this walk** |
| **CTA taxonomy** | Primary actions execute `navigate` / open routes — **VIS-B04 closed** for Operator/Director top cards |
| **Data honesty** | Ledger reader healthy (401 rows, 7 packs); radar queue empty stated explicitly; KiRBe env unset stated — **Gate B satisfied** |

---

## §3 Browser evidence (L3 + L3.0)

**Capture tool:** Playwright @ 1280×800 · `hlk-erp/scripts/_one_off/_i96_b15_l3_experiential_screenshots.js`  
**Auth:** `http://localhost:3010/api/dev/sign-in?next=/research-center`  
**Server:** `npx next dev -p 3010`  
**Manifest:** [`artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/MANIFEST.json`](../../../../artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/MANIFEST.json)

### L3.0 self-verify (binding)

| File | Heading | Full UI | Agent verdict |
|:---|:---:|:---:|:---|
| `01-operator-discover-1280-auth-dev-password.png` | ✓ | ✓ | VALID |
| `02-operator-triage-1280-auth-dev-password.png` | ✓ | ✓ | VALID |
| `03-operator-drawer-open-1280-auth-dev-password.png` | ✓ | ✓ | VALID |
| `04-operator-audit-1280-auth-dev-password.png` | ✓ | ✓ | VALID |
| `05-director-discover-1280-auth-dev-password.png` | ✓ | ✓ | VALID |
| `06-director-triage-1280-auth-dev-password.png` | ✓ | ✓ | VALID |
| `07-director-drawer-open-1280-auth-dev-password.png` | ✓ | ✓ | VALID |
| `08-director-audit-1280-auth-dev-password.png` | ✓ | ✓ | VALID |

**Supersedes invalid captures:** `01-operator-b15-1280.png`, `02-director-b15-1280.png` (favicon-only — deleted).

---

## §4 Per-lens journey checklist

| Lens | Discover | Triage | Act (drawer) | Audit | Overall |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Operator** | PASS — POV, persona, strip, prong, Local dev badge | PASS — 3 signals, remediation sort | PASS — Details → outcome/when/command | PASS — v1 accordion expanded | **PASS** |
| **Director** | PASS — distinct persona + 5-signal header | PASS — ICS + ledger cards visible | PASS — drawer on charter gap card | PASS — WIP packs in accordion | **PASS** |

**SKIP:** Auditor / Finance / Compliance — out of B1.5 tranche scope (T3 lenses scheduled post–Operator+Director L4).

---

## §5 Impeccable disposition vs P9b VIS-B

| ID | Prior severity | B1.5 disposition | Evidence |
|:---|:---|:---|:---|
| **VIS-B01** | Blocker (empty POV lenses) | **Scheduled** — T3 lenses not in B1.5 scope | N/A this walk |
| **VIS-B02** | Blocker (strip vs card contradiction) | **PASS-WITH-FOLLOWUP** — strip shows honest empty radar + ledger row count; KiRBe critical still contrasts with green-adjacent radar copy | `01-operator-discover` |
| **VIS-B03** | Blocker (fixture/BFF on T0) | **CLOSED** — product copy, Local dev badge, no fixture chips | `02-operator-triage` |
| **VIS-B04** | Blocker (CTA drawer-only) | **CLOSED** — navigate CTAs on card face | `04-operator-audit` |
| **VIS-B05** | Blocker (missing journey UI) | **CLOSED** — journey strip, persona, prong, navigate CTAs | discover shots |
| **VIS-M01** | Major (POV wrap) | **PASS** — single-row POV @1280 | discover shots |
| **VIS-M03** | Major (drawer truncate) | **PASS-WITH-FOLLOWUP** — command visible with copy button; production re-check | `03`, `07` drawer |
| **VIS-M04** | Major (Figma vs ERP shell) | **Scheduled** — document gap accepted | N/A |
| **VIS-N02** | Minor (no 375) | **Scheduled** — P11 multi-viewport | N/A |

---

## §6 Topics / radar data honesty note

**Ledger (git reader healthy):** Freshness strip and prong strip report **401 governed sources · 7 active packs**. Director **Research pack coverage 42.2%** card reflects real aggregate — not a fixture.

**Radar / IntelligenceOps:** Strip reads **“Queue empty — register may be unloaded or connection gap”** and Operator staleness card reads **“Register loaded with zero targets”**. This is **honest empty-state** for localhost when `INTELLIGENCEOPS_REGISTER.csv` has no loaded targets — it is **not** a substitute from source-ledger `topic_cluster` counts. Do not treat prong badges (BL-DATA 0, A 117, …) as staleness queue rows; they are pack taxonomy aggregates per harmonization note in GOJ implementation spec §5.

**KiRBe:** `KIRBE_API_URL is not configured` — expected localhost gap; card + CTA name the blocker.

**Production follow-up:** Re-walk on `https://erp.holistikaresearch.com/research-center` to confirm Production badge, radar queue when register mirrored, and KiRBe health on deployed env.

---

## §7 Verdict follow-up (PWF)

| Class | Item | Carryover posture | Tracker |
|:---|:---|:---|:---|
| Production parity | Operator L4 walk @ erp.holistikaresearch.com | **Scheduled** — before B3 | check-links §1–2 |
| Data plane | Populate / mirror IntelligenceOps targets for meaningful radar queue | **Scheduled** — not dropped | `INTELLIGENCEOPS_REGISTER.csv`; staleness loop spec |
| Product | Recharts drawer charts (B1.5-02) | **Scheduled** — optional stretch pre-B3 | B1.5 charter item 2 |
| UAT ladder | Magic-link auth path + 375/768 Operator | **Scheduled** — P11 closure | experiential UAT ladder G-P11-04/05 |
| Mechanical | Playwright RC with production build | **Scheduled** | full regression §2 |

---

## §8 Cross-references

| Artifact | Path |
|:---|:---|
| Experiential UAT ladder (L3.0 gate) | [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md) |
| Operator check-links | [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md) |
| B1.5 charter | [`p9b-wave-b1-revision-charter-2026-06-13.md`](p9b-wave-b1-revision-charter-2026-06-13.md) |
| P9b visual audit baseline | [`p9b-visual-audit-2026-06-12.md`](p9b-visual-audit-2026-06-12.md) |
| Governance corpus | [`research-center-governance-corpus-2026-06-12.md`](research-center-governance-corpus-2026-06-12.md) |
| GOJ harmonization pointer | [`implementation-spec-2026-06-12.md`](../../../intelligence/governed-operator-journey-ux-uat-2026-06-12/implementation-spec-2026-06-12.md) §5 |
