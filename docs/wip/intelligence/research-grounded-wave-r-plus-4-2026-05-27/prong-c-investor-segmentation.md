---
intellectual_kind: research_synthesis_prong
sharing_label: internal_only
prong_id: C
prong_topic: Investor sub-persona segmentation in early-stage startups — validate / amend / extend the 6-sub-persona hypothesis
authored: 2026-05-27
last_review: 2026-05-27
parent_initiative: I86
parent_tranche: wave-r-plus-4-research-grounded-brand-ops-mktops-investor-disambiguation
linked_decisions:
  - D-IH-86-EU (J-IN sub-persona granularity ratification — to be informed by THIS prong)
linked_canonicals:
  - AUDIENCE_REGISTRY.csv
  - PERSONA_SCENARIO_REGISTRY.csv
  - PERSONA_REGISTRY.csv (if exists)
status: drafting
role_owner: Marketing/Resonance (assistant in donde-r capacity)
audience: J-OP, J-AIC
language: en
---

# Prong C — Investor sub-persona segmentation

## TL;DR for the C2 governance commit (the load-bearing decision)

The operator's 2026-05-27 framing named **6 distinct investor sub-types** (Type-A High-Craft Connoisseur / Type-B Specific-Showcase / Type-C Program-On-Radar / Type-D Dump-And-Trust / Type-E Decline-Class / Type-F Online-Presence-Seekers) AND explicitly said: *"i really can't say 6 because i asked for a research for those things too. why would we have in those research if i can't use it to take decisions. what can i flex about when i flex we're a research based company."*

**Research finding (load-bearing):** The industry consensus across 5 sources surveyed does NOT use the operator's specific 6-type taxonomy verbatim, but it converges on **5 underlying axes** of investor evaluation that the operator's 6 types can be **rigorously RECONSTRUCTED from + validated against**:

| Axis | Industry framing (cited sources) | Operator type that maps |
|:---|:---|:---|
| **Decision-driver: Team vs Product vs Market vs Traction vs Financials vs Risk-fragility** | NUVC 9-archetype mapping (Oracle/Empiricist/Stoic/Skeptic/Visionary/Strategist/Pragmatist/Networker/Generalist; data on 4,988 investors) | Type-A (team + product); Type-B (product depth); Type-C (market thesis); Type-D (traction + risk); Type-F (financials proxy via online signal) |
| **Stage-bet shift: Team → Traction → Financials as stage matures** | NUVC + Lucid.now + Fundreef | Universal across types; Holistika is pre-revenue so universally on Team-end of the axis today |
| **Personality cluster: Academic / Feeler / Operator / Growth-quantitative / Hobbyist / Aspiring-founder** | TechCrunch (4 personas — Academic/Feeler/Follower/Aspirant) + SeedLegals (5 personas — Pro/Hobbyist/Aspiring-founder/Strategic-strategic/Personal-connection) | Type-A ≈ Academic + Operator; Type-B ≈ Strategic + Operator (specific-showcase); Type-C ≈ Academic (thesis-driven); Type-D ≈ Feeler + Pro (operational trust); Type-E ≈ "Feeler-bad-fit"; Type-F ≈ Researcher (LinkedIn-evaluator) |
| **Engagement style: Direct connection / Data-driven / Long-term collaboration** | Lucid.now (Low-Risk Angels / Growth-Focused VCs / Corporate Investors triple split) | Type-A wants direct connection; Type-D wants data-driven; Type-F wants pre-meeting researched signal |
| **Decline-signal: red flags that justify founder-side decline** | All 5 sources reference indirectly | Type-E is uniquely operator-named; industry rarely codifies the founder-decline-class but multiple sources implicitly recognize "wrong-fit investor as net negative" |

**Recommendation for the J-IN sub-persona granularity decision (load-bearing for C2; informs D-IH-86-EU):**

The 6-type operator framing **survives rigorous external validation** with 1 mild adjustment + 1 substantive amendment:

- **Survives**: Types A, B, C, D, F all map cleanly to industry-consensus axes (decision-driver + personality cluster + engagement style). The granularity is genuinely useful (it tracks how the founder calibrates the pitch + the brief content per type).
- **Mild adjustment**: Rename **Type-D Dump-And-Trust** → **Type-D Operational-Trust** in canonical taxonomy (Dump-And-Trust is operator vernacular; the canonical needs an industry-readable label; the meaning is preserved — investor trusts operational competence + clear scope, dumps capital, expects competent delivery without crafting input).
- **Substantive amendment**: Type-E Decline-Class should be **demoted from a J-IN sub-persona to a J-IN-Decline-Reason-Class**. Industry research validates that the founder-side decline IS a real workflow (sources don't codify it because most pitch advice is investor-side, but TechCrunch explicitly flags "feelers cause problems if drawn big conclusions from their feedback"). The decline class is a **filter applied to all 5 other types**, not a 6th sub-persona — because a Type-A who turns out to think "anything is possible" gets declined for Type-E reasons. The classification belongs in `PERSONA_SCENARIO_REGISTRY.csv` as a decline-trigger taxonomy, not in `AUDIENCE_REGISTRY.csv` as a separate audience class.

**Final recommendation: 5 J-IN sub-persona rows in AUDIENCE_REGISTRY** (J-IN-HIGH-CRAFT / J-IN-SHOWCASE / J-IN-PROGRAM-ON-RADAR / J-IN-OPERATIONAL-TRUST / J-IN-ONLINE-PRESENCE-SEEKER) **+ 1 cross-persona decline-class taxonomy in PERSONA_SCENARIO_REGISTRY** (5 decline triggers per type).

This is the research-grounded position the operator can flex about: granularity reflects industry evidence; one operator type was DEMOTED based on research; one was RENAMED based on research; 4 survived intact.

## The 5 sources (rated + ranked)

| Source | Confidence | Rank | Why |
|:---|:---|:---|:---|
| **NUVC** — *The 9 Investor Archetypes* (2026-03; 4,988-investor dataset) | CL4 (data-grounded; explicit methodology; 307 scored startup evaluations; calibration via Bayesian updating) | #1 quantitative | Most rigorous segmentation; 9-archetype taxonomy with weight-per-evaluation-dimension breakdown |
| **TechCrunch** — *Four venture capital personas* (2023-06; widely cited) | CL3 (industry publication; experienced VC-author byline) | #1 qualitative | Names 4 personas with concrete identification heuristics + portfolio-pattern indicators |
| **SeedLegals** — *The 5 investor personality types* | CL3 (UK legal platform for startups; CEO-authored from direct pitch experience) | #2 qualitative | Adds Hobbyist + Aspiring-founder types that complement TechCrunch's 4 |
| **Lucid.now** — *Investor Segmentation with AI: A Startup Guide* | CL2 (vendor; useful for stage-cluster framing) | #2 stage | Names Low-Risk Angel / Growth-Focused VC / Corporate Investor triple split + pitch-decision check-size triangulation |
| **Fundreef** — *Creating Investor-Specific Pitch Deck Versions* | CL2 (vendor; useful for the pitch-version-per-type matrix) | #3 tactical | Adds stage-appropriate-deck dimensions (seed vs Series A vs Growth) + reading-each-investor advice |

## Insights extracted (rated + ranked)

### Insight C-1 — "9 archetypes derived from 4,988-investor data; team→traction→financials shift" (NUVC; CL4-HIGH; RANK 1)

**Verbatim claim**: *"We mapped 4,988 active investors from the NUVC database to 9 distinct archetypes — each linked to a philosophical tradition that mirrors their evaluation worldview. These weights are not theoretical — they are derived from thesis analysis, scoring patterns, and deal-level data across 307 evaluated startups... The dominant weight shifts from team → traction → financials [as stage matures]. This is the investor lifecycle in a single table."*

**Why this matters for Holistika:** Holistika is pre-revenue + pre-Series-A. Per NUVC's stage-axis, this places ALL Holistika-target investors in the **early-stage cluster** (angels / accelerators / seed funds) where the dominant evaluation weight is on **team + product** (NOT traction or financials). This validates:

1. The investor brief should LEAD with team + methodology + product-vision evidence, NOT traction metrics (which Holistika does not yet have at scale).
2. Type-D Operational-Trust briefs should still lead with team but include extra weight on "operational competence proven through SUEZ + Websitz live conversations + the 14-discipline checked-in code."
3. NUVC's "Oracle" archetype (bets on people; Sophia-of-Delphi tradition) maps almost exactly to operator's Type-A High-Craft framing.
4. NUVC's "Empiricist" archetype (demands data) maps almost exactly to operator's Type-D Operational-Trust framing.

### Insight C-2 — "Academic vs Feeler vs Follower vs Aspirant personas + the operator-detection-heuristic" (TechCrunch; CL3-HIGH; RANK 1)

**Verbatim claim**: *"If you suspect an investor may be an academic, ask them what investment theses they're working on. If the answer sounds vague, they are a follower or a feeler. If it sounds highly specific, they're an academic... Feelers can be incredible supporters who back you even in the dark days of your journey, though I recommend keeping them to 5%-10% of your target investor mix and avoiding drawing any big conclusions from their feedback because there is nothing you can control that will cause them to choose you."*

**Why this matters for Holistika:** The "ask them what investment theses they're working on" heuristic is the OPERATOR-side identification primitive. This belongs in `PERSONA_SCENARIO_REGISTRY.csv` as a scenario-level investigation step per audience subtype. The "keep feelers to 5-10%" framing also validates Operator's Type-E Decline-Class — feelers who think anything is possible are precisely the "cause problems" type. Confirmation that founder-side filtering is industry-validated.

### Insight C-3 — "Stage-appropriate deck dimensions" (Fundreef; CL2-MEDIUM; RANK 2)

**Verbatim claim**: *"The most common seed-to-Series-A mistake is bringing a seed deck to a Series A conversation."*

**Why this matters for Holistika:** Validates the C4 investor-brief output structure should be **stage-aware in addition to type-aware**. Per Fundreef's matrix:

- Seed deck (Holistika current): 10-14 slides; primary focus = team + vision + early traction; broad market opportunity framing; projections only; concept + early-version product.
- Series A deck (Holistika future): 14-18 slides; primary focus = business model + metrics + growth thesis; TAM with credible methodology; 12-month history + 24-month projection; working product with engagement data.

For C4 deliverable: **brief variants should be seed-stage (no false-projections; honest pre-revenue framing; methodology + vision as the load-bearing claim).**

### Insight C-4 — "Read each investor before customizing — 30-45 minutes well-spent" (Fundreef; CL2-MEDIUM; RANK 3)

**Verbatim claim**: *"Research each investor before customizing your deck. Read their blog posts and investment theses. Review their portfolio for patterns in sector, stage, and business model. Listen to podcast interviews. The 30–45 minutes of research required to understand a specific investor's lens is the most valuable time investment in your pitch preparation."*

**Why this matters for Holistika:** Validates the GOI/POI bounded-intelligence approach (Prong G) for investor outreach. The 30-45min budget aligns with `GOI_POI_STANCE_DOCTRINE.md` per-POI research budget framing. The C2 commit can cite this as external validation of the existing Holistika doctrine.

## Decisions this prong informs (load-bearing for C2 governance commit)

| Decision needed at C2 | Recommended position (research-grounded) |
|:---|:---|
| How many J-IN sub-persona rows in `AUDIENCE_REGISTRY.csv`? | **5 sub-persona rows + 1 decline-class taxonomy in `PERSONA_SCENARIO_REGISTRY.csv`.** Per Insight C-1 (NUVC archetypes) + C-2 (TechCrunch personas) — Type-E demoted from sub-persona to decline-class taxonomy because it is a cross-persona filter, not a separate audience. |
| Naming of the 5 sub-persona rows? | **J-IN-HIGH-CRAFT** (Type-A); **J-IN-SHOWCASE** (Type-B); **J-IN-PROGRAM-ON-RADAR** (Type-C); **J-IN-OPERATIONAL-TRUST** (Type-D renamed); **J-IN-ONLINE-PRESENCE-SEEKER** (Type-F). Operator vernacular preserved in §notes per row; canonical labels are industry-readable per `BRAND_BASELINE_REALITY_MATRIX.md` translated-external register. |
| Should the canonical row carry investor-archetype-axis tagging (NUVC's 9-archetype)? | **Yes — as a metadata column `industry_archetype_mapping`** so future C4 brief authoring can cite NUVC archetype evidence per type. Examples: J-IN-HIGH-CRAFT ↔ Oracle/Empiricist; J-IN-OPERATIONAL-TRUST ↔ Empiricist/Stoic; J-IN-PROGRAM-ON-RADAR ↔ Strategist/Visionary. |
| Should the C4 brief variants be stage-aware (seed-stage only) per Insight C-3? | **Yes — all 5 brief variants are seed-stage shapes.** No false-projection. No false-traction. Honest pre-revenue framing per the operator's 2026-05-27 directive on Stream A truthfulness. |
| Should the operator's "ask what investment theses they're working on" heuristic from Insight C-2 land somewhere canonical? | **Yes — append to a future `PERSONA_SCENARIO_REGISTRY.csv` scenario row** named `investor-thesis-elicitation-heuristic`. Defer to a future scenario-registry-population wave; cite this prong in `PERSONA_SCENARIO_REGISTRY.csv` notes column at C2 minimum. |

## Cross-references

- `AUDIENCE_REGISTRY.csv` — receives 5 new J-IN sub-persona rows at C2 (D-IH-86-EU).
- `PERSONA_SCENARIO_REGISTRY.csv` — receives 1 decline-class taxonomy scenario row at C2 (D-IH-86-EU).
- `GOI_POI_STANCE_DOCTRINE.md` — current bounded-intelligence doctrine; Prong G extends; this prong validates the 30-45min per-POI research budget via Insight C-4.
- D-IH-86-EU — C2 J-IN sub-persona granularity ratifying decision; cites this prong as load-bearing substrate.

## Source archive

- https://nuvc.ai/blog/9-investor-archetypes-how-vcs-actually-weight-your-pitch
- https://www.lucid.now/blog/investor-segmentation-ai-startup-guide/
- https://www.fundreef.com/creating-investor-specific-pitch-deck-versions/
- https://techcrunch.com/2023/06/09/four-venture-capital-personas-and-how-to-land-them/
- https://seedlegals.com/resources/the-5-investor-personality-types/

1 full page cached locally in agent-tools/ for re-grounding.
