# `git filter-repo` history rewrite — re-evaluation trigger contract

**Status**: TEMPLATE / NOT FIRED (2026-04-29).  
**Owners**: Compliance (primary), Legal Counsel (secondary), Founder (sign-off on force-push windows).  
**Authority**: [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) §7 (Forward-only history posture); Initiative 21 [`decision-log.md`](../../21-hlk-adviser-engagement-and-goipoi/decision-log.md) D-CH-2; Initiative 22 [`decision-log.md`](../decision-log.md) D-IH-6.

## Why this template exists

The Initiative-21 plan promoted "redact-forward, history-not-rewritten" as the canonical privacy posture (D-CH-2). The transcript redaction SOP §7 lists two **explicit triggers** that would justify reopening that decision and scheduling a `git filter-repo` initiative:

1. A `restricted` POI is later identified in commit history **without an explicit register row flagged for public reference**.
2. **Counsel issues a privilege-protection demand** (litigation, client-confidentiality assertion, regulatory disclosure constraint).

This template captures the *facts of the trigger* and the *operator approvals* that are required before any history rewrite begins, so the next operator can act fast without having to reconstruct the rationale from scratch. Until either trigger fires, this file remains a template; the row in [`uat-adviser-handoff-20260428.md`](../../21-hlk-adviser-engagement-and-goipoi/reports/uat-adviser-handoff-20260428.md) reads "DEFERRED — trigger not met".

## Trigger record (fill on activation)

```yaml
fired_on: <YYYY-MM-DD>
trigger_kind: <restricted_poi_in_history | counsel_privilege_demand>
detected_by: <role / person>
evidence:
  - <link to commit hash, transcript path, or counsel correspondence reference>
  - <…>
scope_to_purge:
  - <repo-relative path>
  - <git revision range or specific commit shas>
operator_approvals:
  - <founder | legal counsel | compliance>
collaborators_to_notify:
  - <list of git remotes / contributor handles>
force_push_window:
  start: <ISO timestamp>
  end:   <ISO timestamp>
backup_bundle:
  location: <off-repo path>
  sha256:   <hex>
post_rewrite_validation:
  - py scripts/validate_hlk.py
  - py scripts/validate_hlk_vault_links.py
  - py scripts/validate_hlk_km_manifests.py
  - rg "<sensitive_term>" docs/  (must return 0 hits)
```

## Force-push pre-flight checklist (do NOT skip steps)

- [ ] **Trigger documented** above. The trigger MUST fall into one of the two categories above; if it does not, raise a separate decision before proceeding.
- [ ] **Operator approval** captured in this initiative's `decision-log.md` (or a new initiative's log). Founder sign-off REQUIRED for any rewrite touching the public `main` branch.
- [ ] **All collaborators notified** with at least 24h notice (or the agreed window). Reason: a force-push to `main` requires every clone to re-fetch + reset local branches.
- [ ] **Off-repo backup bundle** created (`git bundle create <ts>-pre-filter-repo.bundle --all`). Store on operator-managed Drive; record sha256 in the trigger record.
- [ ] **Dry-run** performed locally first: `git filter-repo --analyze` then the planned `--path-glob` / `--replace-text` script.
- [ ] **Force-push window** scheduled (typically a low-traffic period, e.g. weekend EU morning).
- [ ] **Post-rewrite validators** queued: `py scripts/validate_hlk.py`, `py scripts/validate_hlk_vault_links.py`, `py scripts/validate_hlk_km_manifests.py`, plus `rg <sensitive_term> docs/` to confirm zero residual hits in the rewritten history.

## Cursor-rule guardrails (always-on)

Per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) (Git Safety Protocol section in tool descriptions for the agent runtime):

- NEVER run force-push to `main` or `master` without explicit operator request.
- NEVER skip hooks (`--no-verify`, `--no-gpg-sign`) unless the user explicitly requests it.
- An agent that detects a trigger is to **stop and ask**, not act, even if the SOP would technically authorise the rewrite.

## Cross-references

- [Initiative 21 master roadmap](../../21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)
- [Initiative 21 decision log (D-CH-2)](../../21-hlk-adviser-engagement-and-goipoi/decision-log.md)
- [Transcript redaction SOP](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md)
- [Initiative 22 decision log (D-IH-6)](../decision-log.md)
- [Initiative 21 UAT report](../../21-hlk-adviser-engagement-and-goipoi/reports/uat-adviser-handoff-20260428.md) — row C is annotated as "DEFERRED — trigger not met" pointing back here.
