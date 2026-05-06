---
language: en
status: archived
initiative: 05-hlk-vault-envoy-repos
initiative_id: INIT-OPENCLAW_AKOS-05
report_kind: master-roadmap
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-05
archived_at: 2026-05-05
superseded_by: INIT-OPENCLAW_AKOS-32
---
# Initiative 05 — HLK v3.0 Envoy repository hub + entity placement

**Folder:** `docs/wip/planning/05-hlk-vault-envoy-repos/`
**Status:** **Archived** (2026-05-05) — superseded by Initiatives 13 (HLK v3.0 vault) + 22 (compliance mirror) + 27 (canonical layer hardening) + 31 (CHANNEL_TOUCHPOINT_REGISTRY + 5-axis Holistik Ops) + 32 (6-axis upgrade + skill / touchpoint-kit / policy substrate).
**Archived by:** Initiative 58 D.1 (Cycle 2 multi-track forward) per [`docs/wip/planning/58-cycle-2-multi-track-forward/reports/d1-archive-i05-i20-2026-05-05.md`](../58-cycle-2-multi-track-forward/reports/d1-archive-i05-i20-2026-05-05.md).
**Original Cursor plan:** `~/.cursor/plans/hlk_vault_repo_hub_f3b5cb56.plan.md` (do not treat as canonical vault content).

## 1. Why this initiative existed

I05 was the **first** governed pass at standing up the HLK v3.0 Envoy Tech Lab "Repositories" hub: a registry-of-registries surface where every code repository under Holistika oversight gets a row, a topic FK, and a `source` pointer. It pre-dated the unified compliance-mirror substrate (I22) and the canonical-layer hardening (I27) that ultimately made the registry pattern the default for **all** governed dimensions, not just code repos.

I05 P1 shipped the first registry surface and SOP scaffolds; subsequent initiatives generalised the pattern.

## 2. Why it is archived now

I05 was operationally **superseded** by:

- **I13** — HLK v3.0 vault structure made the Envoy Tech Lab folder layout permanent.
- **I22** — `compliance_mirror_emit` made the registry-mirror pattern uniform across every dimension CSV.
- **I27** — canonical-layer hardening (`PRECEDENCE.md`, `dimensions/` folder, validate_* scripts) made registry FK enforcement repeatable.
- **I29 P5** — `sync_deck_from_strategy.py` cemented the "registry → derived artifact" wiring pattern.
- **I31 P3** — `CHANNEL_TOUCHPOINT_REGISTRY.csv` extended the registry pattern to operational touchpoints.
- **I32 P2-P4** — `SKILL_REGISTRY.csv`, touchpoint-kit cell registry, `POLICY_REGISTER.csv` extended the registry pattern to skills, cells, and policies.

There is no I05-specific scope still open: the `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/` folder is live and maintained as part of the I13/I22/I27 governance mesh, not as I05 follow-up work.

The dashboard previously surfaced I05 as `unknown` because no master-roadmap.md existed in the folder. This one-paragraph archive frontmatter clears the unknown without claiming any new scope.

## 3. Surviving artifacts (governed elsewhere)

- `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/` — live folder, governed by I13/I22/I27.
- [`phase-1-plan.md`](phase-1-plan.md) — original P1 plan, reference-only.
- [`reports/phase-1-report.md`](reports/phase-1-report.md) — original P1 closure report, reference-only.

## 4. Reactivation path (if ever needed)

If a new code-repo onboarding flow needs first-class governance (e.g., when MADEIRA productizes per `MADEIRA_PLATFORM.md`), spawn a fresh initiative under `docs/wip/planning/<NN>-<slug>/` rather than reopening I05. Per `.cursor/rules/akos-mirror-template.mdc`, the canonical SSOT is the AKOS HLK v3.0 vault, not this archive folder.
