---
candidate_id: I-NN-OUTPUT-ARCHITECTURE
title: Output architecture — 4-layer hierarchy below the Quality Fabric (output type / artifact class / component primitive)
status: candidate
authored: 2026-05-20
last_review: 2026-05-20
parent_initiatives: [86]
related_initiatives: [66, 70, 72, 79, 85]
priority: 3
language: en
audience: J-OP;J-AIC
access_level: 3
parent_lane: I86 Wave K (regression of Wave J Quality Fabric mint)
charter_decisions:
  - D-IH-86-BB  # 4-layer output-architecture meta-decision
  - D-IH-86-BC  # candidate mint
forward_charter_authority: D-IH-86-BB (operator G4 extension 2026-05-20: 'we are speaking of components in a UI and there could be more scenarios slides of pdf/pptx images voice for agents reading for different readers platforms scenarios excalidraw mermaids graphs gantts please try to think of a way to properly organize the output type')
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - .cursor/rules/akos-external-render-discipline.mdc
supersedes_candidate: I-NN-MESSAGE-COMPONENT-LIBRARY (the previously-named single-axis Component initiative; reframed per D-IH-86-BB regression as 3-layer hierarchy below fabric)
---

# I-NN-OUTPUT-ARCHITECTURE — 4-layer hierarchy below the 5-axis Quality Fabric

> **Spawned by I86 Wave K** (Wave J regression operator-ratify 2026-05-20). Reframes the previously-proposed `I-NN-MESSAGE-COMPONENT-LIBRARY` from a single 6th axis ("Component") into a 4-layer hierarchy beneath the existing 5-axis Quality Fabric. The fabric stays at 5 axes; below it sit 4 orthogonal layers naming the output medium / artifact purpose / component primitive / render surface decomposition that lets a creative user reach Shadcn/Radix/NextUI-class depth on every Holistika output.

## 1. Operating story

The 5-axis Quality Fabric (`HOLISTIKA_QUALITY_FABRIC.md` mint at status: charter, Wave J 2026-05-20) answers *who/how/what/look-feel/governance* for any artifact. It does **not** answer *what shape the artifact takes*. Operator regression 2026-05-20:

> *"we are speaking of components in a UI and there could be more scenarios, slides of pdf/pptx, images, voice for agents, reading for different readers platforms, scenarios, etc, excalidraw, mermaids, graphs, gantts, please try to think of a way to properly organize the output type"*

Without this layer, Holistika has the audience axis + channel axis + brand axis + governance axis but **no per-component depth**. Component libraries that have understood UI to the highest level — [Shadcn/UI](https://ui.shadcn.com/docs), [NextUI / HeroUI](https://nextui.org/docs/guide/design-principles), [Radix](https://www.radix-ui.com/), [Aceternity](https://ui.aceternity.com/) — define per-primitive doctrine pages with variants × states × accessibility × composition × research grounding. Holistika message outputs need the same depth, with the additional complication that messaging is **multi-modal** (prose + slide + voice + diagram + image + chart) in a way pure UI is not.

This initiative names the load-bearing organisation that lets a creative user (operator + AICs + future hire) make the most of every output:

```
Quality Fabric (Audience × Channel × Scenario × Brand × Governance)
   ↓ derives quality bar, parametrised by:
Layer 1: OUTPUT TYPE (medium / shape: prose / slide / image / voice / mermaid / gantt / excalidraw / web / pdf / video; ~17 codes)
   ↓ assembled into:
Layer 2: ARTIFACT CLASS (named purpose: dossier / cover_email / intro_message / deck / topic_graph / km_diagram / uat_report; ~20 codes)
   ↓ composed of:
Layer 3: COMPONENT PRIMITIVE (sub-units: greeting / hook / CTA / signature / evidence-block / slide-hero / slide-the-ask; ~25 codes)
   ↓ rendered to:
Layer 4: RENDER SURFACE (PDF / Web / ERP / Mail / Slide / Broadcast — already exists per akos-external-render-discipline.mdc RULE 1)
```

Each layer = registry CSV + canonical MD library doctrine. The Quality Fabric `compose()` runbook (forward-chartered per D-IH-86-BA) applies at every layer with derived bar varying by layer. Per-primitive doctrine pages = **exactly Shadcn-shape**: purpose / inputs / variants by audience / variants by channel / brand-voice rules / accessibility / anti-patterns / good+bad examples / research grounding / cross-references.

## 2. Why activation is gated

Per `akos-conflict-surfacing-and-blocker-trackers.mdc` Option 5 default posture: this initiative is candidate-tier today because two architectural prerequisites must clear before the registries can mature into per-row doctrine pages:

### 2.1 Activation criteria (all three required; AND-gate)

| # | Criterion | Why required | Source of truth |
|:---:|:---|:---|:---|
| **A1** | **Quality Fabric at status: active** (gates on `D-IH-86-BA` compose() runbook landing) | The 4-layer hierarchy is parametrised BY the 5 axes. Without compose() implemented as code, agents resolve axes by reading docs each time and per-layer bars cannot be deterministically derived. The hierarchy is structurally reasonable today; the per-row doctrine depth requires the runbook. | `HOLISTIKA_QUALITY_FABRIC.md` frontmatter `status: active` + `scripts/derive_quality_bar.py` lands + `tests/test_derive_quality_bar.py` PASS in CI |
| **A2** | **UAT_DISCIPLINE at status: active** (gates on `D-IH-86-AY` 11-class promotion landing) | UAT verifies the 4-layer hierarchy works in practice. Without 11-class UAT (especially accessibility-class + localisation-class) the per-primitive doctrine pages can claim things the system can't actually verify. | `UAT_DISCIPLINE.md` frontmatter `status: active` + 11-class taxonomy ratified in §4 + 1+ closure UAT report exercising 4 of 11 classes |
| **A3** | **≥ 1 channel doctrine POC** (per `D-IH-86-AW` I-NN-CHANNEL-DOCTRINES P1 deliverable) | Component primitives' variants-by-channel rules must derive from real channel doctrine, not speculation. At least one channel (e.g., CHAN-EMAIL-OUTBOUND or CHAN-LINKEDIN-DM) must have its own DOCTRINE.md authored with researched goods/bads before per-primitive variants can claim "behaviour Z on channel Y". | First `<CHAN-CODE>_DOCTRINE.md` under `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/channels/` with researched do/don't list + channel-specific anti-patterns |

### 2.2 Why AND-gate (not OR-gate)

The initiative's value is the **per-primitive doctrine depth at Shadcn quality**. Skipping any of A1/A2/A3 would produce shallow doctrine: A1-skip → axes resolve manually each time (drift); A2-skip → claims the system can't verify; A3-skip → channel-variants are speculation. The AND-gate ensures the registries land with depth that actually unblocks creative-user mode.

### 2.3 Wave K landing posture (registries land NOW; doctrine pages mature post-activation)

Per operator velocity-bless 2026-05-20 (opt-arch-plus-all-three with "wire whatever we left up" directive), Wave K lands the **architectural skeleton**: 3 registries + 3 libraries with:
- All ~17 / ~20 / ~25 codes registered with full FK structure.
- 1 worked-example doctrine page per layer (proves shape).
- Retro-tag of touchpoint-kit's 15 files + retro-classify of 11 render scripts.

The remaining ~52 per-row doctrine pages mature inside this initiative once activation gates clear. The Wave K landing is **architectural proof-of-shape**; the initiative is **doctrine-depth-proof**.

## 3. Forward-charter scope (when promoted)

When all three A1+A2+A3 gates clear, this candidate promotes to active with the following phase plan:

### 3.1 Phase shape

| Phase | Effort | Deliverable | Gate |
|:---|:---|:---|:---|
| **P0** — Charter | 1d | Inline-ratify open conundrums (per-row doctrine depth bar; Mermaid/Excalidraw/Gantt authoring tool registry; voice-rendering format priority); mint INITIATIVE_REGISTRY + DECISION_REGISTER rows | operator approval |
| **P1** — Layer 1 OUTPUT_TYPE per-row doctrine | 3-5d | Per-row doctrine page for ~17 output types (medium-specific authoring rules; render targets; accessibility concerns; brand visual anchor); pages live as `OUTPUT_TYPE_LIBRARY.md` §3.<code> sub-sections OR as standalone files under `output_types/` | operator approval per batch of 5 codes |
| **P2** — Layer 2 ARTIFACT_CLASS per-row doctrine + retro-tag scripts | 5-7d | Per-row doctrine page for ~20 artifact classes (purpose + typical audience+channel + render script + worked examples); retro-classify all 11 `render_*.py` scripts in registry; bind ARTIFACT_CLASS_REGISTRY → render scripts via `render_script_path` FK | operator approval per batch |
| **P3** — Layer 3 COMPONENT_PRIMITIVE per-row doctrine (Shadcn-shape) | 7-10d | Per-row doctrine page for ~25 component primitives at Shadcn-equivalent depth (purpose / inputs / variants by audience / variants by channel / brand-voice rules / accessibility / anti-patterns / good+bad examples / research grounding / cross-references); pages live as standalone `.md` files under `component_primitives/<CP-CODE>.md` | operator approval per batch of 5 codes |
| **P4** — Touchpoint-kit + ENISA dossier full backfill | 2-3d | Backfill all per-engagement folders (`docs/references/hlk/v3.0/_assets/advops/**`) with `output_type` + `artifact_class` + `component_primitive_inventory` frontmatter; convert touchpoint-kit's intro_message bundles into composable primitive references (`<Greeting> + <Hook> + ...` instead of atomic inline) | operator approval |
| **P5** — `derive_quality_bar.py` per-layer integration | 2d | Extend compose() runbook from D-IH-86-BA with `--layer output-type|artifact-class|component-primitive` flag returning per-layer derived bar; emit JSON for ERP planning panel + Markdown for human reading; tests for cross-layer consistency | CI gate (release-gate.py wires the validator) |
| **P6** — ERP planning panel surface | 3-5d | Mint `/operator/output-architecture/` route in `hlk-erp` reading from 3 mirror tables (output_type_mirror / artifact_class_mirror / component_primitive_mirror); operator-facing search + filter + Shadcn-shape doctrine viewer | sibling-repo PR + Vercel deploy verification per akos-quality-fabric.mdc RULE 3 |
| **P7** — UAT closure | 2d | 11-class UAT report exercising 5+ classes (closure / brand / accessibility / persona / regression at minimum); flip Quality Fabric reference table §6 from "5 specialty composes" to "8 specialty composes including output-architecture-aware bars" | operator approval; INITIATIVE_REGISTRY status flip to closed |
| **Total** | **~25-35d (5-7 weeks)** | | |

### 3.2 Open conundrums (resolve at P0 via inline-ratify)

| ID | Question | Default verdict | Decision target |
|:---|:---|:---|:---|
| C-NN-1 | Per-row doctrine depth bar: 1-page Shadcn-shape vs 3-page deep with code samples vs 5-page with full audience/channel matrix | 1-page Shadcn-shape at v1; deeper variants emerge per primitive based on usage | D-IH-NN-A |
| C-NN-2 | Authoring tool registry (Mermaid / Excalidraw / Figma / D3 / mermaid-cli / etc) — separate registry vs Layer 1 OUTPUT_TYPE column | Layer 1 column (`authoring_tool` field) at v1; if tool ecosystem proliferates beyond ~10 tools, promote to standalone TOOL_REGISTRY in successor initiative | D-IH-NN-B |
| C-NN-3 | Voice-rendering format priority — TTS-first (operator instructs Madeira; agent renders) vs human-narration-first (founder records; agent transcribes) | TTS-first at v1; human-narration as future variant | D-IH-NN-C |
| C-NN-4 | Component primitive registry FK direction — primitive → applicable_artifact_classes (M:M) vs artifact_class → component_primitive_inventory (1:M ordered) | Both: M:M FK in registry (primitive-can-belong-to-N-artifact-classes) + ordered 1:M inventory in artifact-class doctrine page (this artifact-class composes-of these primitives in this order) | D-IH-NN-D |
| C-NN-5 | Cross-area ownership of Layer 1 vs Layer 2+3 | Layer 1 = Front-End Developer primary + Brand & Narrative Manager co-owner (medium concerns); Layer 2+3 = Brand & Narrative Manager primary + Front-End Developer co-owner (purpose + composition concerns) per 2026-05-15 absorption | D-IH-NN-E |
| C-NN-6 | What constitutes a "creative user" mastery test (the bar the operator named verbatim) | A creative user composes a new artifact using primitives + variants such that the composition resolves cleanly through compose() with no ambiguity findings | D-IH-NN-F |

## 4. Cross-references and wiring

- **Origin**: I86 Wave J regression `D-IH-86-AU` (Quality Fabric architecture mint) → operator G4 extension 2026-05-20 → Wave K reframe `D-IH-86-BB` (4-layer hierarchy) → forward-charter `D-IH-86-BC` (this candidate).
- **Sibling forward-charters**: `D-IH-86-AW` (I-NN-CHANNEL-DOCTRINES; A3 prerequisite); `D-IH-86-AX` (UX_DISCIPLINE.md mint; depends on A3 too).
- **Cross-area inheritance**: Per `UAT_DISCIPLINE.md` §5 cross-area inheritance contract, Marketing / Tech Lab / Operations / Research / Legal / People / Compliance all consume Layer 1+2+3 registries via composition into their own area-specific quality bars (MKTOPS uses CTA primitive variants for funnel components; TECHOPS uses error-message primitive variants for system surfaces; etc.).
- **Mechanical landing**: Wave K commit lands 6 new canonicals (3 registries + 3 libraries) + retro-tag of 15 touchpoint-kit files + retro-classify 11 render scripts. Per akos-applied-research-discipline.mdc RULE 2: novel framings require external research grounding; the 4-layer architecture cites Shadcn / NextUI / Radix / Aceternity (UI primitive doctrine bar) + Mailchimp pattern library (email primitive precedent) + Material Design 3 (cross-modal output types) per per-row library doctrine pages.
- **Cursor rule binding**: `akos-quality-fabric.mdc` extends with RULE 8 (4-layer hierarchy resolution) at I-NN-OUTPUT-ARCHITECTURE P5 once compose() runbook delegates to per-layer bars.

## 5. Decision lineage (preview)

| Decision | Status | Source | Notes |
|:---|:---|:---|:---|
| D-IH-86-AU | active | Wave J | Quality Fabric architecture mint (5-axis) |
| D-IH-86-BB | **NEW** Wave K | Wave K regression | 4-layer output-architecture (this candidate's parent) |
| D-IH-86-BC | **NEW** Wave K | Wave K regression | Candidate mint (this file) |
| D-IH-NN-A..F | future | I-NN-OUTPUT-ARCHITECTURE P0 | Conundrum resolutions |
| D-IH-NN-CLOSURE | future | I-NN-OUTPUT-ARCHITECTURE P7 | Initiative closure decision |

## 6. Activation tracker

| Date | Event | Notes |
|:---|:---|:---|
| 2026-05-20 | Candidate mint (Wave K) | Per D-IH-86-BC; activation gates A1/A2/A3 not met today |
| TBD | A1 cleared | When `derive_quality_bar.py` lands per D-IH-86-BA |
| TBD | A2 cleared | When UAT_DISCIPLINE 11-class promotion lands per D-IH-86-AY |
| TBD | A3 cleared | When first channel doctrine MD lands per D-IH-86-AW |
| TBD | All gates cleared → promote to active | INITIATIVE_REGISTRY append + status flip |
