---
intellectual_kind: gate_spec
sharing_label: internal_only
access_level: 5
audience: J-OP
register: internal
language: en
authored: 2026-05-26
last_review: 2026-05-26
authoring_session: I86 cluster Wave R+2 doctrine-rewrite — pre-send regression gate first instantiation
status: charter
ratifying_decisions:
  - D-IH-86-EJ  # SUEZ recommercialisation context (this gate's first worked example)
  - D-IH-86-EM  # 13th specialty demotion (this gate's load-bearing post-hoc check)
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md
linked_artifacts:
  - docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-grounding-post-handshake-2026-05-26.md
forward_charters:
  - Promote to 15th Quality Fabric specialty doctrine after 2-3 worked examples (SUEZ + Websitz + next engagement)
  - Author scripts/pre_send_regression_sweep.py runbook (deferred until 2nd instantiation to avoid premature crystallisation)
  - Wire into release-gate.py as advisory-only INFO step (deferred until runbook exists)
  - Mint .cursor/skills/pre-send-regression-craft/SKILL.md (deferred until doctrine matures)
---

# Pre-Send Regression Gate — first instantiation spec (2026-05-26)

## Why this spec exists

Operator's verbatim mandate at session open (2026-05-26 ~04:00 UTC):

> *"bear in mind I agree with you and we need a regression everytime (now that we still haven't sent anything)."*

The need surfaced because the Wave R+2 doctrine-rewrite tranche correctly demoted the 13th specialty doctrine + reframed SUEZ commercial shape AFTER customer artifacts were already drafted at customer-pack rates that the rewrite invalidates. Had the customer-pack been sent before the rewrite landed, the artifact would have committed Holistika to a commercial frame the operator now considers wrong.

The pattern generalises: any candidate external artifact whose authoring predates a doctrine amendment OR a substrate update (transcript ingestion / counterparty intelligence update / commercial frame revision) needs a **pre-send sweep** that validates the artifact's frame against the latest doctrine + latest substrate state.

This is currently a **gate spec** (charter status). It will mature to **discipline-class doctrine** once 2-3 worked examples accumulate and the failure modes stabilise. SUEZ POC is worked example #1.

## RULE 1 — The gate fires before every external send

In scope:
- Any candidate artifact under `docs/references/hlk/v3.0/Think Big/Clients/<engagement>/02-customer-pack/`
- Any candidate artifact under `docs/references/hlk/v3.0/Think Big/Advisers/<engagement>/02-handoff-pack/` OR `03-deliverables/`
- Any candidate `cover-email-*.{md,html}` destined for external send
- Any candidate dossier under `docs/references/hlk/v3.0/_assets/advops/**/dossier_*.md`
- Any candidate render under `_exports/` matching the manifests of the above

Out of scope:
- Internal scratchpads + planning notes (operator-only consumption)
- Engagement-internal source-grounding notes (the inputs to the gate, not the outputs)
- Internal AKOS canonicals (covered by validate_hlk.py + the post-commit specialty sweeps)

## RULE 2 — Six-layer composite sweep

The gate composes the existing specialty validators in a specific order:

| Layer | Probe | Tool | FAIL semantic |
|:---|:---|:---|:---|
| **L1 — Brand register** | All external-rendered artifacts use translated register (no internal CORPINT tokens leaked) per `akos-brand-baseline-reality.mdc` | `scripts/validate_brand_baseline_reality_drift.py --target <artifact-glob>` | Any internal-register token in external surface → BLOCK |
| **L2 — Render-trail freshness** | Every external `.md` SSOT has a paired rendered surface (PDF / Web / Mail body / ERP record / Slide / Broadcast) with fresh sha256 manifest per `akos-external-render-discipline.mdc` | `scripts/validate_external_render_trail.py --strict --strict-freshness` | Missing render OR stale sha256 → BLOCK |
| **L3 — Collaborator-share consistency** | When the artifact references commercials (tarification, proposal, settlement), the SHARE_REGISTRY rows for the engagement satisfy CS-01..CS-08 per `akos-collaborator-share.mdc` | `scripts/validate_collaborator_share.py --engagement-id <ID>` | Any CS-01..CS-08 FAIL → BLOCK |
| **L4 — Synthesis-before-tranche** | When the artifact is part of a tranche-class shipment per `akos-synthesis-before-tranche.mdc`, the 10-dim synthesis sweep passed at the tranche-charter | `scripts/synthesis_before_tranche_check.py --check-charter <tranche-charter-path>` | SYN-04/05/07/08 FAIL → BLOCK; SYN-01/02/03/06/09/10 WARN → INFO advisory (proceed) |
| **L5 — Grounding-vs-latest-transcripts** (NEW) | The artifact's frame matches the LATEST source-grounding note for the engagement; no transcript ingested since artifact authoring contradicts it | Manual + `scripts/check_grounding_freshness.py` (FORWARD-CHARTER — runbook to author at 2nd instantiation) | Latest grounding note's `last_review` > artifact's `last_review` AND grounding §"What this changes" lists scope items NOT addressed in artifact → BLOCK |
| **L6 — Send-rights coherence** | The artifact's `audience:` frontmatter tag resolves cleanly against `AUDIENCE_REGISTRY.csv` AND the artifact's render surface matches the audience's acceptable surfaces per `akos-external-render-discipline.mdc` RULE 2 audience-format matrix | `scripts/validate_external_render_trail.py --audience-resolution-check` | Audience-surface mismatch → BLOCK |

Order matters: L1 + L2 are cheap structural checks; L3 + L4 are doctrine-level checks; L5 is the most expensive (requires comparing artifact authoring-state to substrate freshness); L6 is the final sanity check.

## RULE 3 — Manual L5 protocol (until runbook lands)

L5 is the load-bearing check that distinguishes this gate from a plain composite-validator-runner. Manual protocol:

1. Identify the engagement: read the artifact's `program_id` or `engagement_slug` frontmatter.
2. Open the engagement's `00-internal/source-grounding-*.md` notes sorted by `last_review` descending.
3. For each grounding note dated AFTER the artifact's `last_review`:
   - Read §"What this changes" (or equivalent forward-pointer section).
   - For each item: cross-check if the artifact still reflects the prior frame OR has been amended.
4. If ANY post-artifact grounding note's "What this changes" lists an item NOT yet addressed in the artifact → BLOCK + halt + surface to operator via inline-ratify gate.
5. If all post-artifact grounding notes are addressed → PASS L5 advisory; record the manual check evidence in the gate run report.

## RULE 4 — Gate run report

Every gate execution produces a dated report under:

```
docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/pre-send-regression-<engagement-slug>-<YYYY-MM-DD>.md
```

Report structure:

```markdown
---
intellectual_kind: pre_send_regression_report
artifact_under_review: <path>
artifact_last_review: <YYYY-MM-DD>
gate_verdict: PASS | BLOCK | PASS-WITH-WARNINGS
authored: <YYYY-MM-DD>
last_review: <YYYY-MM-DD>
---

## L1 brand-register: PASS | BLOCK + verbatim findings
## L2 render-trail: PASS | BLOCK + manifest sha256 evidence
## L3 collaborator-share: PASS | BLOCK + CS-NN findings per engagement
## L4 synthesis-before-tranche: PASS | BLOCK | N/A + per-dim breakdown
## L5 grounding-freshness: PASS | BLOCK + post-artifact-grounding-note inventory
## L6 send-rights: PASS | BLOCK + audience-surface resolution
## Verdict + send-authorisation timestamp + operator-ratify-trail
```

Report frontmatter is mechanical; body is auditable evidence; verdict line is the binary gate signal.

## RULE 5 — Inline-ratify discipline for BLOCK findings

When the gate BLOCKs, the agent surfaces a structured inline-ratify gate per `akos-inline-ratification.mdc` with options:

1. **fix-now-and-retry** — author the fix; re-run the gate; commit when PASS.
2. **fix-now-without-retry** — author the fix; trust the operator-eyeball; commit (acceptable for L1 + L2 + L5 single-token / single-link fixes only).
3. **document-and-override** — operator ratifies the BLOCK is a false positive; append contra-precedent + decision row + override-decision-id in the gate report.
4. **escalate-to-blocker-tracker** — operator-decision-bandwidth-exceeded; mint `_blockers/pre-send-<engagement>-<date>-tracker.md`.

Time-box recovery NEVER applies to L3 + L4 BLOCKs (commercial / doctrinal load-bearing); operator must explicitly ratify.

## RULE 6 — INFO → FAIL ramp gates on worked-example threshold

Today (2026-05-26): charter status; INFO advisory only.

To promote to discipline-class doctrine:

1. ≥ 3 worked examples with diverse failure-mode coverage:
   - **#1 SUEZ POC** — this instantiation. The L3 + L5 layers caught the prior commercial-frame stale-state.
   - **#2 Future Websitz extension** — the L3 layer should catch any rate-overlay drift.
   - **#3 TBD** — needs a different failure-mode to validate cross-layer coverage.
2. Validator runbook authored (`scripts/pre_send_regression_sweep.py`).
3. Cursor rule + skill + canonical doctrine quartet per the 15-surface specialty mint contract per `akos-quality-fabric.mdc` RULE 7.
4. Operator-explicit ratify decision row promoting the gate to 15th specialty.

## Section 7 — First instantiation: SUEZ POC

The first run of this gate fires before the SUEZ 27-28/05 ship (whenever the candidate cover-email + customer-pack composite is ready to send). Pre-conditions for that run:

- Wave R+2 doctrine-rewrite Commits 2-7 landed (per the existing todo list).
- Cover-email-2026-05-27.fr.md rewritten as FOLLOW-UP per the existing `suez-cover-email-rewrite` todo.
- SHARE_REGISTRY rows for SUEZ updated per Commit 5 + the NEW `parallel_invoice_stream_indicator` column per the post-handshake findings note §7.
- Pre-send regression report authored at `reports/pre-send-regression-2026-suez-webuy-<YYYY-MM-DD>.md` with all 6 layers PASS or PASS-WITH-WARNINGS.

If the run BLOCKs, the SUEZ ship slips again. Operator's verbatim posture in prior cycle: *"the operator can choose to slip"* — this gate makes the slip choice **mechanical** rather than gut-feel.

## Cross-references

- Trigger source: post-handshake debrief findings [`docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-grounding-post-handshake-2026-05-26.md`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-suez-webuy/00-internal/source-grounding-post-handshake-2026-05-26.md) §6
- Doctrine forward-charter: this gate is the candidate 15th Quality Fabric specialty; promotion path in §RULE 6 above; cite back to [`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md) §6 specialty roster when promoted.
- Composes: 13 existing specialty validators + cursor rules + canonicals named in RULE 2 above.
- Wave R+2 tranche charter: [`tranches/wave-r-plus-2-doctrine-rewrite-collaborator-share-4-base-1-overlay.md`](tranches/wave-r-plus-2-doctrine-rewrite-collaborator-share-4-base-1-overlay.md) — gate first-instantiation context.
- Operator scratchpad drain: see operator-scratchpad.md entry dated 2026-05-26 (post-handshake findings drain + pre-send gate mint).

