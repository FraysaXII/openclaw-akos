---
intellectual_kind: phase_report
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
linked_decisions:
  - D-IH-90-W
language: en
---

# Regression sweep — I90 run + sibling mirror delivery (2026-06-01)

Thorough pass over everything landed in this run: **GATE #2** (routing / rule tiers), **sibling mirror PRs**, and full **AKOS** mechanical gates. Vendor surfaces checked: **GitHub Actions**, **Vercel**; **Supabase** (kirbe RLS workflow); **Neo4j** (I91 — still blocked); **Cloudflare** (no kirbe/hlk-erp Pages project in scope for this mirror change).

## Executive verdict

| Layer | Verdict | Notes |
|:---|:---|:---|
| **I90 scope (AKOS tiers + pairing + hooks)** | **PASS** | Targeted validators + 30 I90-focused pytest cases |
| **Sibling mirror contract (AKOS)** | **PASS** | `check_external_repo_contract` + `test_release_gate_external_repo_check` |
| **hlk-erp GitHub Actions** | **PASS** | Full CI green on mirror merge to `main` |
| **hlk-erp Vercel production** | **PASS** | `dpl_8yq1eqxQU1bVLQUiBPLmWrvSejd2` **READY** (PR #24 squash) |
| **kirbe GitHub Actions** | **FAIL (pre-existing)** | Red since ≥ 2026-05-07; mirror commit did not introduce |
| **kirbe Vercel** | **FAIL (pre-existing)** | All recent production deploys **ERROR**; mirror merge triggered another ERROR build |
| **kirbe Supabase RLS (pgTAP)** | **PASS** | `rls-pgtap` job green on mirror merge |
| **AKOS full `pre_commit` / `release-gate`** | **FAIL (known debt)** | 1 test: deck slide 11 topic count (28 vs 39) — deferred, not I90 |
| **Neo4j (I91)** | **N/A** | No `NEO4J_*` in env — unchanged |

**Bottom line:** The mirror realign + I90 routing work did **not** regress hlk-erp CI/CD or production deploy. Kirbe was already red on GHA and Vercel before this run; the mirror-only commit is not the root cause.

---

## 1 — AKOS mechanical (I90 + governance)

| Check | Command / surface | Result |
|:---|:---|:---|
| Rule tiers | `py scripts/validate_cursor_rule_tiers.py` | **PASS** (34 rules; 3 always-on; max 4) |
| Rule–skill pairing | `py scripts/validate_rule_skill_pairing.py` | **PASS** (21/21 paired) |
| HLK umbrella | `py scripts/validate_hlk.py` | **OVERALL PASS** |
| External repo contract | `py scripts/check_external_repo_contract.py` | **OK** — 2 repos (hlk-erp, kirbe-platform) |
| I90 pytest slice | `test_validate_cursor_rule_tiers`, `test_validate_rule_skill_pairing`, `test_release_gate_external_repo_check`, `test_repo_health_snapshot` | **30 passed** |
| Full test suite | `py scripts/verify.py pre_commit` → `test_all` | **FAIL** — `test_slide_11_pillar_1_quotes_governance_metrics` only (3503 passed) |
| Release gate | `py scripts/release-gate.py` (includes full pytest) | **FAIL** — same deck test |

Deck failure: slide 11 still says **28** governance topics; `TOPIC_REGISTRY.csv` has **39**. Tracked as pre-existing debt (OPS-86-23 / brand deck), not introduced by I90.

---

## 2 — GitHub Actions (sibling repos)

### hlk-erp — mirror merge `main` (2026-06-01T03:11:47Z)

Workflow: **CI** — run [26733100945](https://github.com/FraysaXII/hlk-erp/actions/runs/26733100945) — **success**

| Job | Result |
|:---|:---|
| Unit tests (Jest) | success |
| Dependency audit | success |
| Lint, types & jargon | success |
| Build | success |
| Playwright on preview | skipped |
| Lighthouse on preview | skipped |

PR: [#24](https://github.com/FraysaXII/hlk-erp/pull/24) merged (squash). Commit on `main` includes only `.cursor/rules/akos-mirror.mdc` + `.akos-mirror.sha256`.

### kirbe — mirror merge `main` (2026-06-01T03:11:44Z)

Three workflows fired on the same push; **all failed**, but failures match **May 7** pattern (already red on `chore(i63)` and Dependabot runs).

| Workflow | Run | Result | Failure locus |
|:---|:---|:---|:---|
| CI (kirbe-platform) | [26733099682](https://github.com/FraysaXII/kirbe/actions/runs/26733099682) | failure | `actions/setup-node@v4` (audit/lint/typecheck/unit jobs) |
| Kirbe Test Pipeline | [26733099674](https://github.com/FraysaXII/kirbe/actions/runs/26733099674) | failure | `Run linting checks` (product Python lint) |
| kirbe-ci-rls-and-auth | [26733099683](https://github.com/FraysaXII/kirbe/actions/runs/26733099683) | failure | `Tests + Coverage` unit jobs; **`rls-pgtap` success** |

**Attribution:** Mirror commit touches two cursor rule files only. Kirbe `main` has been failing CI since at least **2026-05-07** (same three workflows on unrelated commits). **Not a regression from I90 mirror work.**

PR: [#23](https://github.com/FraysaXII/kirbe/pull/23) merged. Remote `main` at `8d5f7c2` contains `akos-mirror.mdc` (verified via GitHub API).

### openclaw-akos — `main`

Recent runs: **eval-tier-b** scheduled workflow — **failure** (2026-06-01, 2026-05-25, …). Orthogonal to I90 mirror/tier work; eval harness debt.

---

## 3 — Vercel (deploy-class)

Verified via Vercel MCP (`list_deployments`, team Holistika).

### hlk-erp (`prj_ieZqgduSs2u2BZTJVqxCsZxtbQwd`)

| Deploy ID | Target | State | Trigger |
|:---|:---|:---|:---|
| `dpl_8yq1eqxQU1bVLQUiBPLmWrvSejd2` | production | **READY** | PR #24 merge → `main` (`16a7b22…`) |
| `dpl_6UHkeUo2J6WSZYVizZHrDkfKPqa8` | preview | **READY** | PR branch push (`625dd46…`) |

**PASS** — production deploy healthy after mirror merge.

### kirbe (`prj_V82A8wCa1NbBtQblLt1FpSMkzNQl`)

| Deploy ID | Target | State | Trigger | Notes |
|:---|:---|:---|:---|:---|
| `dpl_Gudei1T57BhLpXJA1jQ1udytVzLs` | production | **READY** | `main` post-`b5958c2` health-only gateway | **Current contract** per D-IH-90-X — `/health` only; not full FastAPI |
| `dpl_wJDD7D5Zq8iyTi3YqCMofbcu6Aaz` | production | **ERROR** | PR #23 mirror merge (`8d5f7c2…`) | Historical full-API bundle attempt |
| `dpl_BkRJ71uL5y51M5dn6ayCj63J8yrR` | preview | **ERROR** | PR branch (`8c9a3cc…`) | Historical |

**Narrative (OPS-90-5 / P3.5):** Through **2026-05**, production deploys on the Vercel `kirbe` project failed when building the **full** FastAPI surface (~245 MB serverless limit). Commit **`b5958c2`** on `main` narrowed the Vercel project to a **health-only** gateway; production deploy **`dpl_Gudei1T57BhLpXJA1jQ1udytVzLs`** is **READY**. **Full KiRBe API** lives on **Render** at `https://kirbe.holistikaresearch.com` — see [`KIRBE_ROUTING_AND_HOSTING.md`](../../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Repositories/KIRBE_ROUTING_AND_HOSTING.md). **Do not** point GDrive scripts or `KIRBE_API_URL` at `kirbe-holistika.vercel.app`. Mirror-only PR #23 did not change this posture; kirbe **GHA CI** remains red (pre-existing, separate initiative).

---

## 4 — Supabase

- **kirbe `kirbe-ci-rls-and-auth` → `rls-pgtap`:** **success** on mirror-merge run (Postgres service container + pgTAP RLS tests).
- **AKOS `supabase db` / mirror emit:** Not part of this tranche; no migration or mirror emit in mirror PRs.
- **hlk-erp:** Supabase client usage in app code; no Supabase-specific GHA job on mirror push; CI build+jest passed.

---

## 5 — Neo4j

- **I91** store inventory / graph preflight: still **BLOCKED-ENV** (no `NEO4J_*` in operator session).
- No Neo4j CI job triggered by mirror commits.

---

## 6 — Cloudflare

- **hlk-erp** and **kirbe** consumer deploys observed on **Vercel**, not Cloudflare Pages, for this change set.
- No Cloudflare build triggered by mirror-only commits (no `wrangler`/Pages workflow in scope).

---

## 7 — What this run shipped (checklist)

| Item | Status |
|:---|:---|
| GATE #2 ratified (`D-IH-90-W`) | Done |
| `config/cursor-rule-tiers.json` + 3 always-on rules | Done |
| `validate_cursor_rule_tiers` + `validate_rule_skill_pairing` | Done |
| Sibling mirror PRs merged (hlk-erp #24, kirbe #23) | Done |
| AKOS `check_external_repo_contract` | **PASS** |
| hlk-erp CI + Vercel prod | **PASS** |
| kirbe CI / Vercel | **Pre-existing FAIL** |
| Full AKOS pytest | **1 known FAIL** (deck) |

---

## 8 — Recommended follow-ups (not blocking I90 mirror)

1. **kirbe GHA:** Fix `actions/setup-node` / frontend CI kit workflow (`.github/workflows/ci.yml` from bless kit) — infra, not doctrine.
2. **kirbe Vercel:** Inspect `dpl_wJDD7D5Zq8iyTi3YqCMofbcu6Aaz` build logs (vendor MCP `get_deployment_build_logs`) — likely same root as months of ERROR deploys.
3. **AKOS deck:** Update slide 11 topic count when brand deck tranche runs (OPS-86-23).
4. **I91:** Operator supplies Neo4j creds for graph-store coverage tranche.

---

## Cross-references

- [p2-gate2-rule-tier-review-2026-06-01.md](./p2-gate2-rule-tier-review-2026-06-01.md)
- [post-gate2-sibling-mirror-realign-2026-06-01.md](./post-gate2-sibling-mirror-realign-2026-06-01.md)
- [regression-pre-continue-2026-06-01.md](./regression-pre-continue-2026-06-01.md)
