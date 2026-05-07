---
language: en
status: charter
initiative: 64-governance-mission-control
report_kind: asset-classification
last_review: 2026-05-07
---

# Asset classification — Initiative 64

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md).

## Canonical (proposed)

- **`governance.canonical_change_log` Supabase table** — append-only;
  each row records (csv_name, sha256_before, sha256_after, changed_at,
  consumer_repo_slug, broadcast_status). RLS: service-role write,
  operator read. Migration ships in P1.

- **3 GitHub Actions reusable workflows in AKOS** — codified entry
  points for the dashboard:
  - `governance-bless-repo.yml`
  - `governance-regen-types.yml`
  - `governance-broadcast-change.yml`

## Mirrored / derived

- `hlk-erp/lib/types/akos-mirrors.generated.ts` — already wired by
  `regen_consumer_types.py` (I63 P0). I64 consumes; doesn't change
  generation.

- `hlk-erp/app/operator/governance/external-repos/page.tsx` — derived
  presentation surface. The truth-source remains AKOS canonical CSVs
  + Supabase mirrors.

- `hlk-erp/components/governance/*` — derived presentation
  components.

## Reference-only

- This charter folder.
- All `reports/*.md` artefacts.

## No baseline_organisation.csv changes

The dashboard inherits the existing operator role / RBAC posture from
hlk-erp (operator-only routes). No new role minting required.

## No process_list.csv changes

The dashboard *visualises* the three processes minted in I63 P4
(`SOP-EXTERNAL_REPO_BLESSING_001` /
`SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001` /
`SOP-CROSS_REPO_SCHEMA_PROPAGATION_001`). Visualising existing
processes does not require new process rows per the AKOS rule
"Visualisation surfaces are reference-only".

## Subdomain registration

If a separate URL like `governance.holistika.com` is desired, an
entry is added to
[`SUBDOMAINS_REGISTRY.md`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/SUBDOMAINS_REGISTRY.md)
in P3 / P4. Default plan is to host under
`madeira.holistika.com/operator/governance/external-repos/`.
