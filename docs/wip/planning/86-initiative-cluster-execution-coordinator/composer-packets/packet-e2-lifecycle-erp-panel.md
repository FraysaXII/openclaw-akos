---
intellectual_kind: composer_bounded_packet
packet_id: E2-lifecycle-erp-panel
target_seat: Composer (execution)
owning_initiative: INIT-OPENCLAW_AKOS-89
authored: 2026-05-29
status: ready
---

# Composer packet — E2 Lifecycle → ERP operator panel

## Objective

Surface CORPINT lifecycle + Research Radar stale queue in **hlk-erp** as an operator research
dashboard (backlog E2).

## Read first

- `docs/wip/planning/89-hlk-erp-program-rollup-implementation/master-roadmap.md`
- `docs/references/hlk/v3.0/Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md`
- `scripts/research_radar_sweep.py` output shape

## Deliverables

| Repo | Path |
|:---|:---|
| `hlk-erp` | `app/(operator)/research/lifecycle/page.tsx` (or existing operator namespace) |
| `hlk-erp` | Server component reading `compliance.intelligenceops_register_mirror` via service role |
| `openclaw-akos` | Page-spec stub under `docs/wip/planning/89-.../reports/p-spec-research-lifecycle-panel-2026-05-29.md` |

## UI minimum (v0)

1. Six lifecycle stages as nav / legend (ACQUIRE … PROTECT).
2. Table: IntelligenceOps rows with `staleness_posture` + `next_verify_by` (requires OPS-86-32 DML).
3. Link-out to AKOS vault paths (no raw markdown render to externals).

## Validators

- Playwright smoke on desktop viewport per I68 template (when panel lands).
- `validate_external_render_trail` N/A (J-OP internal).

## Acceptance

- Panel loads against prod mirror post-resync with ≥4 IntelligenceOps rows visible.
- No secrets in client bundle; RLS respected (server-side fetch only).

## Escalate to Opus if

- Panel copy touches external audience classes.
- New ERP route needs REPOSITORY_REGISTRY blessing row.
