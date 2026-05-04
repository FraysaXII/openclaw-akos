# AKOS Content Navigator

**Audience:** anyone who has just been asked "what does AKOS *actually do* — and how do I see what it's doing?" and wants the answer in under thirty seconds without trawling vault prose.

This guide does **not** replace [USER_GUIDE.md](../USER_GUIDE.md) (operator runbook), [SOP.md](../SOP.md) (formal procedures), or the vault SOPs under `docs/references/hlk/v3.0/`. It is a one-screen *index* of where the live content lives, what each surface tells you, and which command lights it up.

## 30-second health check

Two commands, both safe to run at any time:

```bash
py scripts/release-gate.py
py scripts/render_wip_dashboard.py
```

`release-gate` returns either `8/8 PASS` (everything is green; ship verdict positive) or a list of failing gates with hint lines. `render_wip_dashboard` regenerates [WIP_DASHBOARD.md](../wip/planning/WIP_DASHBOARD.md) (initiative status board + open OPS items + open follow-ups). If both look healthy, AKOS is operating at first-class.

If you only want to *prove the stack runs at all*, hit one URL each:

- `http://127.0.0.1:8420/health` — FastAPI control plane (orchestration, MADEIRA, persona/scenario lookup, eval surface)
- `http://127.0.0.1:18789/health` — OpenClaw gateway (the dashboard surface; the chat/madeira/agents UI lives here)

Start them with `py scripts/serve-api.py` and `py scripts/doctor.py --repair-gateway` respectively (see [USER_GUIDE.md § Two-gateway boot](../USER_GUIDE.md)).

## Where do I look for X?

| You want to see… | Open this | What you'll find |
|:------|:------|:------|
| The latest dossier (operator's read-out: prompts + answers + citations + ship verdict per section) | `artifacts/uat-dossier/uat-dossier-<UTC>/dossier-console.html` | Eleven-section operator console with raw prompt/answer pairs, judge axis scores, three-light verdict, drift warnings, cost ceilings, and per-section copy buttons |
| The initiatives that are open and what's coming next | [`WIP_DASHBOARD.md`](../wip/planning/WIP_DASHBOARD.md) | Per-initiative status, open OPS-* items, open follow-ups, today's verdict |
| Every persona × skill × topic combination AKOS evaluates | [`docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv`](../references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv) | The full UAT scenario library (the canonical CSV; mirrored to `compliance.persona_scenario_registry_mirror`) |
| The actual prompts + answers used in a cassette replay | [`tests/evals/cassettes/`](../../tests/evals/cassettes/) | One `.jsonl` per cassette, recorded once via `py scripts/eval.py record …`; replayed offline by `--mode replay` |
| The brand voice that AKOS speaks in | [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md`](../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md) + sibling `BRAND_REGISTER_MATRIX.md`, `BRAND_DO_DONT.md` | Operator-confirmed voice charter, do/don't pairs, and the (relationship × channel → register) matrix |
| The compliance + HLK doctrine that governs every decision | [`docs/references/hlk/compliance/PRECEDENCE.md`](../references/hlk/compliance/PRECEDENCE.md) + [`docs/references/hlk/v3.0/index.md`](../references/hlk/v3.0/index.md) | What is canonical, what is mirrored, what is reference-only |
| What changed in the last cycle (or any cycle) | [`CHANGELOG.md`](../../CHANGELOG.md) | Imperative-mood entries grouped by Unreleased / dated releases |
| Which evaluation runs are passing and how cost is tracking | `py scripts/render_uat_dossier.py --filter madeira --mode snapshot` then open `dossier-console.html` § 8 | Operational health: endpoint cost, per-skill envelope, recovery rate, surface UX |
| The decision log for any initiative (why a thing was decided) | `docs/wip/planning/<NN-initiative>/decision-log.md` | Dated `D-IH-<NN>-<X>` rows with rationale and reversibility |
| Open SQL operator gates / Supabase parity state | `docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md` | The discover → propose → approve → execute → verify workflow |

## The dossier console — operator's main microscope

The richest single artifact in AKOS. Re-render it any time:

```bash
py scripts/render_uat_dossier.py --filter madeira --mode snapshot --format all
```

Output (under `artifacts/uat-dossier/uat-dossier-<UTC>/`):

| File | Read this when… |
|:---|:---|
| `dossier.md` | You want plain markdown for `gh pr comment` / email |
| `dossier.html` | You want a branded HTML view for an internal share-link |
| `dossier.pdf` | You want a portable PDF for an external share |
| `dossier-console.html` | You want the operator-facing **detailed** view: per-section panels with raw prompts, raw answers, judge scores per axis, citations, three-light verdicts, copy-buttons. **This is where you go to see test content.** |
| `manifest.json` | You want the structured per-section metrics (sha256 + char_count + status); also the input to `regression_artifact_diff.py` |

Eleven sections in `dossier-console.html` (Section 1 is the three-light verdict; sections 2–11 cover registry coverage, eval health, persona library + judge calibration, drift, recovery, scenario quarantine, operational health + endpoint cost, surface UX, brand voice, trends).

## Three-lights — what "first class" means

The dossier surfaces three independent traffic lights in Section 1 (madeira flavor):

| Light | Question | Goes red when… |
|:---|:---|:---|
| **Conversational** | Is the model giving good answers? | Multi-judge consensus fails or persona-fit drifts |
| **Operator** | Can the operator trust the surface and the data? | Drift / cost / mirror parity / a11y critical findings |
| **Surface (CI)** | Are the rails (release-gate + tests + smoke) green? | Any of the 8 release-gate gates fails |

`madeira_ship_go: true` requires all three lights green. The dossier records each cycle's state into `manifest.json`, and `regression_artifact_diff.py` compares cycles to detect material change.

A separate `[FAIL] Browser smoke` line in `release-gate.py` almost always means **a gateway is not running** — start it with `py scripts/serve-api.py` (8420) or `py scripts/doctor.py --repair-gateway` (18789); see [USER_GUIDE.md § Two-gateway boot](../USER_GUIDE.md).

## Operator paths cheatsheet

Run from the repo root in PowerShell or bash:

```bash
# Health
py scripts/release-gate.py
py scripts/render_wip_dashboard.py
py scripts/validate_hlk.py

# Dossier
py scripts/render_uat_dossier.py --filter madeira --mode snapshot --format all

# Eval cycles
py scripts/eval.py list                  # what cassettes / suites exist
py scripts/eval.py --mode replay --tier A # offline replay
py scripts/eval.py --mode replay --tier B # live LLM (requires AKOS_RECORD_LIVE=1; cost-gated)

# Regression-to-advisor loop (Initiative 55)
py scripts/regression_artifact_diff.py --current <…>/manifest.json [--last-sent <…>/manifest.json]
py scripts/propose_advisor_update.py --diff <…>/regression-diff.json --use-defaults --dry-run

# Live a11y (Initiative 54)
py scripts/browser-smoke.py --playwright --axe
py scripts/audit_a11y_live.py            # per-rule-id detail dump

# Supabase parity (operator SQL gate)
py scripts/check-drift.py
py scripts/verify.py compliance_mirror_emit
```

## When in doubt

1. Open [`WIP_DASHBOARD.md`](../wip/planning/WIP_DASHBOARD.md). If the initiative you care about is not there, it doesn't exist yet.
2. Open the latest `dossier-console.html`. If a section is amber or red, click its `<details>` panel for the raw prompts and answers.
3. Open [`CHANGELOG.md`](../../CHANGELOG.md) and search for the relevant `D-IH-<NN>-<X>` decision id.
4. If still stuck, run `py scripts/doctor.py --help`.
