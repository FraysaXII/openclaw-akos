# I86 P2 — one-shot diff (notes prefix -> program_anchors column)

| Date | 2026-05-17 |
|:---|:---|
| Rows mutated | 24 |
| Decision | D-IH-86-J |
| Source script | `scripts/_oneshot_anchors_notes_to_column.py` |
| Validator post-apply | `scripts/validate_initiative_registry.py` (FK block) + `scripts/validate_initiative_program_anchors.py --strict` (cutover hygiene WARN) |

## Per-row diff

### INIT-OPENCLAW_AKOS-01

- Anchors extracted: `PRJ-HOL-PGF-2026;PRJ-HOL-INF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-INF-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-03

- Anchors extracted: `PRJ-HOL-PGF-2026;PRJ-HOL-DAT-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-DAT-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-04

- Anchors extracted: `PRJ-HOL-FOUNDING-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-FOUNDING-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-06

- Anchors extracted: `PRJ-HOL-PGF-2026;PRJ-HOL-OPS-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-OPS-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-08

- Anchors extracted: `PRJ-HOL-INF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-INF-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-11

- Anchors extracted: `PRJ-HOL-MAD-2026;PRJ-HOL-INF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-MAD-2026; PRJ-HOL-INF-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-14

- Anchors extracted: `PRJ-HOL-MKT-2026;PRJ-HOL-OPS-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-MKT-2026; PRJ-HOL-OPS-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-17

- Anchors extracted: `PRJ-HOL-MAD-2026;PRJ-HOL-INF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-MAD-2026; PRJ-HOL-INF-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-19

- Anchors extracted: `PRJ-HOL-FIN-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-FIN-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-24

- Anchors extracted: `PRJ-HOL-MKT-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-MKT-2026. Promoted active per D-IH-86-G (gated_operator lifted at registry layer for execution visibility). Plan-local YAML Sections 2/3/5 + G-24-3 send checklist remain operator-owned per Initiative 24 roadmap.`
- notes AFTER:  `Promoted active per D-IH-86-G (gated_operator lifted at registry layer for execution visibility). Plan-local YAML Sections 2/3/5 + G-24-3 send checklist remain operator-owned per Initiative 24 roadmap.`

### INIT-OPENCLAW_AKOS-55

- Anchors extracted: `PRJ-HOL-MKT-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-MKT-2026. seeded by I59 P3 audit pass`
- notes AFTER:  `seeded by I59 P3 audit pass`

### INIT-OPENCLAW_AKOS-56

- Anchors extracted: `PRJ-HOL-OPS-2026;PRJ-HOL-LEG-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-OPS-2026; PRJ-HOL-LEG-2026. Promoted active per D-IH-86-G (gated_external lifted at registry layer). Adviser reply sequencing remains OPS-56-1 / master-roadmap discipline.`
- notes AFTER:  `Promoted active per D-IH-86-G (gated_external lifted at registry layer). Adviser reply sequencing remains OPS-56-1 / master-roadmap discipline.`

### INIT-OPENCLAW_AKOS-62

- Anchors extracted: `PRJ-HOL-INF-2026;PRJ-HOL-PGF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-INF-2026; PRJ-HOL-PGF-2026. Mission Control magnificent ERP shell on hlk-erp; sibling to I63+I64+I65; P0-P10 charter+build; Supabase migrations P1+P3 applied 2026-05-07 (P2 deferred — see reports/migration-application-2026-05-07.md)`
- notes AFTER:  `Mission Control magnificent ERP shell on hlk-erp; sibling to I63+I64+I65; P0-P10 charter+build; Supabase migrations P1+P3 applied 2026-05-07 (P2 deferred — see reports/migration-application-2026-05-07.md)`

### INIT-OPENCLAW_AKOS-63

- Anchors extracted: `PRJ-HOL-INF-2026;PRJ-HOL-PGF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-INF-2026; PRJ-HOL-PGF-2026. External Repo Bless Pattern + 3 active SOPs; canonical CSVs + 9 automation scripts; secrets walkthrough operated via MCPs 2026-05-07 (D-IH-63-G)`
- notes AFTER:  `External Repo Bless Pattern + 3 active SOPs; canonical CSVs + 9 automation scripts; secrets walkthrough operated via MCPs 2026-05-07 (D-IH-63-G)`

### INIT-OPENCLAW_AKOS-64

- Anchors extracted: `PRJ-HOL-PGF-2026;PRJ-HOL-INF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-INF-2026. Governance dashboard for external-repo bless health (sibling to I62 Mission Control); v2 page-spec promoted 2026-05-07 with 5 user journeys + impeccable laws`
- notes AFTER:  `Governance dashboard for external-repo bless health (sibling to I62 Mission Control); v2 page-spec promoted 2026-05-07 with 5 user journeys + impeccable laws`

### INIT-OPENCLAW_AKOS-65

- Anchors extracted: `PRJ-HOL-PGF-2026;PRJ-HOL-INF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-INF-2026. New /operator/planning/ panel surfacing docs/wip/planning/ workspace; sibling to I62+I63+I64; chartered + promoted same-day with full page-spec/journeys/data-model`
- notes AFTER:  `New /operator/planning/ panel surfacing docs/wip/planning/ workspace; sibling to I62+I63+I64; chartered + promoted same-day with full page-spec/journeys/data-model`

### INIT-OPENCLAW_AKOS-67

- Anchors extracted: `PRJ-HOL-MKT-2026;PRJ-HOL-OPS-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-MKT-2026; PRJ-HOL-OPS-2026. Research-first successor to I66; investigates positioning channels offers pricing partner economics tooling KPIs and route promotion before any implementation plan. Promoted active per D-IH-86-G (gated_operator lifted at registry layer); interview brief cadence stays plan-local.`
- notes AFTER:  `Research-first successor to I66; investigates positioning channels offers pricing partner economics tooling KPIs and route promotion before any implementation plan. Promoted active per D-IH-86-G (gated_operator lifted at registry layer); interview brief cadence stays plan-local.`

### INIT-OPENCLAW_AKOS-68

- Anchors extracted: `PRJ-HOL-INF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-INF-2026. CICD discipline + visual regression + Sentry deploy-health telemetry + GitHub Actions/Vercel/Render CI baseline + build-time discipline + InfraMonitor v0 namespace shell with InfraHealth as first module (D-IH-68-K reframe); promoted active 2026-05-10 with I66 closed + Render MCP unblocked + Round-2 plan accepted; 4 explicit operator pause-points (P0 promotion`
- notes AFTER:  `CICD discipline + visual regression + Sentry deploy-health telemetry + GitHub Actions/Vercel/Render CI baseline + build-time discipline + InfraMonitor v0 namespace shell with InfraHealth as first module (D-IH-68-K reframe); promoted active 2026-05-10 with I66 closed + Render MCP unblocked + Round-2 plan accepted; 4 explicit operator pause-points (P0 promotion`

### INIT-OPENCLAW_AKOS-86

- Anchors extracted: `PRJ-HOL-PGF-2026;PRJ-HOL-OPS-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-OPS-2026. Operational coordinator co-owned PMO plus System Owner per D-IH-86-A; coordinated siblings I81 I82 I84 I85 I87 plus active I78; I24 I56 I67 promoted active per D-IH-86-G (gated_* clearance). Forward-charter candidates I74/I75/I76/I83 stay _candidates-only until charter. Continuous/program_line methodology for intertwined initiatives — operator ratifies via D-IH-86-G follow-on AskQuestion batch. D-IH-86-D closure cross-check before each sibling closure ratifies; manifests_processes empty by design.`
- notes AFTER:  `Operational coordinator co-owned PMO plus System Owner per D-IH-86-A; coordinated siblings I81 I82 I84 I85 I87 plus active I78; I24 I56 I67 promoted active per D-IH-86-G (gated_* clearance). Forward-charter candidates I74/I75/I76/I83 stay _candidates-only until charter. Continuous/program_line methodology for intertwined initiatives — operator ratifies via D-IH-86-G follow-on AskQuestion batch. D-IH-86-D closure cross-check before each sibling closure ratifies; manifests_processes empty by design.`

### INIT-OPENCLAW_AKOS-85

- Anchors extracted: `PRJ-HOL-MKT-2026;PRJ-HOL-PGF-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-MKT-2026; PRJ-HOL-PGF-2026. I85 P0 charter promoted under I86 Wave 1 batch ratify (2026-05-16); 5 P0 decisions D-IH-85-A through E ratified with decision_source agent_inline_default after operator skip on inline-ratify AskQuestion. Five-phase shape ~3.5d total. Co-owned Brand & Narrative Manager (owner) + System Owner (validator wiring co-owner). Wired to I81 P1 via forward-link audience_tags_coverage column. Mirrors I77 P4.C RENDERING_PIPELINE_REGISTRY wiring pattern row-for-row.`
- notes AFTER:  `I85 P0 charter promoted under I86 Wave 1 batch ratify (2026-05-16); 5 P0 decisions D-IH-85-A through E ratified with decision_source agent_inline_default after operator skip on inline-ratify AskQuestion. Five-phase shape ~3.5d total. Co-owned Brand & Narrative Manager (owner) + System Owner (validator wiring co-owner). Wired to I81 P1 via forward-link audience_tags_coverage column. Mirrors I77 P4.C RENDERING_PIPELINE_REGISTRY wiring pattern row-for-row.`

### INIT-OPENCLAW_AKOS-87

- Anchors extracted: `PRJ-HOL-INF-2026;PRJ-HOL-MAD-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-INF-2026; PRJ-HOL-MAD-2026. I87 P0 charter promoted under I86 Wave 1 batch ratify (2026-05-16); 3 P0 decisions D-IH-87-A through C ratified with decision_source agent_inline_default after operator skip. Six-phase shape ~5-7d total. Recommended cluster slot before I84 Wave 3 substrate ratification so D-IH-84-B compares against patched OpenClaw baseline. Closes Open R-IH-86-3 substrate-decision lag risk.`
- notes AFTER:  `I87 P0 charter promoted under I86 Wave 1 batch ratify (2026-05-16); 3 P0 decisions D-IH-87-A through C ratified with decision_source agent_inline_default after operator skip. Six-phase shape ~5-7d total. Recommended cluster slot before I84 Wave 3 substrate ratification so D-IH-84-B compares against patched OpenClaw baseline. Closes Open R-IH-86-3 substrate-decision lag risk.`

### INIT-OPENCLAW_AKOS-81

- Anchors extracted: `PRJ-HOL-PGF-2026;PRJ-HOL-PEO-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-PEO-2026. I81 P0 charter promoted under I86 Wave 1 batch ratify (2026-05-16); 5 P0 decisions D-IH-81-A through E plus D-IH-81-H ratified with decision_source agent_inline_default after operator skip on inline-ratify AskQuestion. Ten-phase shape ~10-25d total (absorbed mode per D-IH-81-A). Wired to I82 P2 via forward-link kb-integrity-matrix and to I85 P1 via reverse-link audience_tags_coverage column. Heavy canonical-CSV touch at P2 layout migration (operator gates per tranche).`
- notes AFTER:  `I81 P0 charter promoted under I86 Wave 1 batch ratify (2026-05-16); 5 P0 decisions D-IH-81-A through E plus D-IH-81-H ratified with decision_source agent_inline_default after operator skip on inline-ratify AskQuestion. Ten-phase shape ~10-25d total (absorbed mode per D-IH-81-A). Wired to I82 P2 via forward-link kb-integrity-matrix and to I85 P1 via reverse-link audience_tags_coverage column. Heavy canonical-CSV touch at P2 layout migration (operator gates per tranche).`

### INIT-OPENCLAW_AKOS-82

- Anchors extracted: `PRJ-HOL-PEO-2026;PRJ-HOL-RES-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-PEO-2026; PRJ-HOL-RES-2026. I82 P0 charter promoted under I86 Wave 1 batch ratify (2026-05-16); 5 P0 decisions D-IH-82-A/B/NAME/ARCHIVIST/SEQUENCE ratified with decision_source agent_inline_default after operator skip. Seven-phase shape ~7-10d total. Third foundational doctrine sibling to ORGANISING + AGENTIC. Wired to I81 P1 via kb-integrity-matrix consumption (D-IH-82-SEQUENCE; D-IH-82-PREREQ waiver at P2). AI Archivist + KiRBe ingestor forward-chartered to I83.`
- notes AFTER:  `I82 P0 charter promoted under I86 Wave 1 batch ratify (2026-05-16); 5 P0 decisions D-IH-82-A/B/NAME/ARCHIVIST/SEQUENCE ratified with decision_source agent_inline_default after operator skip. Seven-phase shape ~7-10d total. Third foundational doctrine sibling to ORGANISING + AGENTIC. Wired to I81 P1 via kb-integrity-matrix consumption (D-IH-82-SEQUENCE; D-IH-82-PREREQ waiver at P2). AI Archivist + KiRBe ingestor forward-chartered to I83.`

### INIT-OPENCLAW_AKOS-78

- Anchors extracted: `PRJ-HOL-MKT-2026;PRJ-HOL-DAT-2026`
- notes BEFORE: `Program anchors: PRJ-HOL-MKT-2026; PRJ-HOL-DAT-2026. P0 strategic scaffold 2026-05-14 (_candidates/i78-brand-voice-llm-judge.md + planning template integration). Activated active 2026-05-17 per D-IH-78-A operator directive (prior TRIGGER-only posture superseded for registry purposes). P1 judge Pydantic chassis + CLI + release-gate INFO advisory wiring pending; strict-mode promotion remains bias-audit gated per candidate Strand D. Coordinates with closed I71 deterministic Pack A1 + Vale floor.`
- notes AFTER:  `P0 strategic scaffold 2026-05-14 (_candidates/i78-brand-voice-llm-judge.md + planning template integration). Activated active 2026-05-17 per D-IH-78-A operator directive (prior TRIGGER-only posture superseded for registry purposes). P1 judge Pydantic chassis + CLI + release-gate INFO advisory wiring pending; strict-mode promotion remains bias-audit gated per candidate Strand D. Coordinates with closed I71 deterministic Pack A1 + Vale floor.`

