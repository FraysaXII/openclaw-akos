---
initiative_id: I81
linked_initiative: INIT-OPENCLAW_AKOS-90
ops_id: OPS-90-6
ratifying_decisions:
  - D-IH-90-X
  - D-IH-81-A
process_ids:
  - env_tech_dtp_255
  - env_tech_dtp_256
authored: 2026-06-01
status: forward-charter
role_owner: System Owner
language: en
---

# OPS-90-6 forward — KiRBe GDrive / connector vault pairing (I81 P6)

**Purpose:** Close the **forward** half of [OPS-90-6](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) from [I90 P3.5](../../90-routing-and-wiring/reports/kirbe-production-routing-ops-2026-06-01.md) without blocking production routing on full I81 KB PASS.

**Ordnance vs vault:** I90 P3.5 fixed **where** clients call KiRBe ([`KIRBE_ROUTING_AND_HOSTING.md`](../../../../docs/references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Repositories/KIRBE_ROUTING_AND_HOSTING.md), decision `D-IH-90-X`). I81 P6 owns **how** vault SOPs + addenda + runbooks pair to `process_list` rows for connector + ingestion work.

---

## 1 — Scope split

| `process_list` row | Granularity | I90 P3.5 (done) | I81 P6 (remaining) |
|:---|:---|:---|:---|
| **env_tech_dtp_255** | workstream | KiRBe Multi-Source Connector Setup — routing SSOT + repo runbooks cite `https://kirbe.holistikaresearch.com` | Mint / retrofit v3.0 SOP for connector OAuth + GDrive; `CONNECTOR_SETUP_GUIDE` reference in row; holistika_ops GDrive SOP vault alignment |
| **env_tech_dtp_256** | process | Canonical Ingestion Envelope — API host in routing canonical; kirbe `docs/kirbe_sops/*` hostname cleanup merged | v3.0 SOP body + addendum per `pattern_sop_addendum_split`; paired runbook row in `process_list`; audience + cadence tags |

---

## 2 — KNOWLEDGE_PAIRING rows minted (routing-forward)

Interim registry rows (audit substring match on `env_tech_dtp_255` / `env_tech_dtp_256` in `pairing_id` + notes):

| pairing_id | parent SSOT | Notes |
|:---|:---|:---|
| `pair_env_tech_dtp_255_kirbe_connector_001` | `KIRBE_ROUTING_AND_HOSTING.md` | Workstream; I81 P6 completes SOP graph |
| `pair_env_tech_dtp_256_kirbe_ingestion_001` | `KIRBE_ROUTING_AND_HOSTING.md` | Process; kb-integrity matrix `knowledge_pairing` → matched after this commit |

**Not claimed:** `paired_sop_status` PASS for v3.0 vault SOPs — those files do not exist under `docs/references/hlk/v3.0/` yet.

---

## 3 — I81 P6 acceptance criteria (closes OPS-90-6)

OPS-90-6 flips **closed** when **all** of:

1. v3.0 Tech/System Owner SOP (+ addendum where required) exists for **env_tech_dtp_256** and cites `KIRBE_ROUTING_AND_HOSTING.md` for hostnames (no duplicate routing tables).
2. Workstream **env_tech_dtp_255** has either a v3.0 SOP pointer row or an explicit `process_list` link to the governing SOP `item_id` for GDrive connector setup (per `CONNECTOR_SETUP_GUIDE` intent in row description).
3. `py scripts/audit_kb_integrity.py` shows `env_tech_dtp_256` with `paired_sop_status: matched` (and pairing matched).
4. Operator sign-off on I81 P6 pause record (or inline-ratify) naming holistika_ops GDrive SOP disposition.

---

## 4 — Repo-local runbooks (sibling; not vault SSOT)

| Repo | Path | Rule |
|:---|:---|:---|
| kirbe-platform | `docs/kirbe_sops/render_deployment_gdrive.md` | Cite AKOS `KIRBE_ROUTING_AND_HOSTING.md` for `PROD_URL` / health |
| hlk-erp | `documentation/KIRBE_API_ENV.md` | `KIRBE_API_URL` server-only; BFF `/api/kirbe/*` |

Merged at I90 P3.5: kirbe PR #26 (`03c152d`), hlk-erp PR #25 (`c45e06e`).

---

## 5 — Cross-references

- I90 routing ops: [`kirbe-production-routing-ops-2026-06-01.md`](../../90-routing-and-wiring/reports/kirbe-production-routing-ops-2026-06-01.md)
- I81 milestone: [`master-roadmap.md`](../master-roadmap.md) — `I81-TECH-RETROFIT` / P6
- Pairing SSOT: [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv)
