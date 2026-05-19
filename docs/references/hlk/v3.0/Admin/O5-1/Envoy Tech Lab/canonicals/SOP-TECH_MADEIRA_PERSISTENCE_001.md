---
intellectual_kind: sop
sharing_label: internal_only
authored: 2026-05-19
status: active
owner_role: System Owner
co_owner_role: Founder
co_owner_role_2: PMO
authority: System Owner + Founder + PMO
language: en
last_review_at: 2026-05-19
last_review_by: System Owner
last_review_decision_id: D-IH-76-F
methodology_version_at_review: v3.0
linked_decisions:
  - D-IH-76-A
  - D-IH-76-D
  - D-IH-76-E
  - D-IH-76-F
  - D-IH-86-O
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_MODE_PARITY.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_TOOL_CATALOG.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_TOOL_RBAC.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv
linked_initiatives:
  - INIT-OPENCLAW_AKOS-76
paired_runbook: scripts/madeira_persistence_check.py
canonical_dependencies:
  - MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv
  - DECISION_REGISTER.csv
  - TOPIC_REGISTRY.csv
---

# SOP — MADEIRA persistence operations

> Registry-driven operations contract for the persistence vehicles Madeira (current AI O5-1) reads from and writes to.[^role-class] The vehicles themselves are listed in [`dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv`](./dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv) — do not duplicate the row inventory in this prose. This SOP names the **read / write / add / deprecate** behaviours, the **staleness posture** semantics, and the **target-audience** rules that the registry rows parameterise.

[^role-class]: AI O5-1 is the role class; Madeira is the current embodiment per the I76 charter (`D-IH-76-A`). When the role-class population grows beyond one, this SOP refers to the class; specific embodiments are documented at [`docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/MADEIRA-AKOS/STATUS.md`](../MADEIRA-AKOS/STATUS.md) when present.

## 1. Purpose

The 5-mode taxonomy in [`MADEIRA_MODE_PARITY.md`](./MADEIRA_MODE_PARITY.md) declares what Madeira may **do** in each mode (Ask / Plan / Agent / Debug / Methodology). The tool RBAC matrix in [`dimensions/MADEIRA_TOOL_RBAC.csv`](./dimensions/MADEIRA_TOOL_RBAC.csv) declares which tools each mode may **call**. This SOP closes the third side of the triangle: which **persistence vehicles** Madeira reads at session entry, which it writes back to during the session, who else can read what is written, and how stale a vehicle is allowed to be before its content must be re-ratified.

The doctrine in one sentence: **memory is registry-shaped, not prose-shaped.** Operator framing per the I76 P3 axis 1 ratify gate (2026-05-19, novel option d): persistence vehicles must be co-designed and scalable — adding a new vehicle is a CSV row append + validator pass, never an SOP rewrite.

## 2. Scope + out of scope

**In scope.** Read + write + add + deprecate operations for the rows in [`MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv`](./dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv); per-row staleness posture semantics; per-row target-audience semantics; the runbook that enforces staleness automatically.

**Out of scope.** Per-session prompt routing (the `MADEIRA_METHODOLOGY_MODE.md` SOP owns that); tool RBAC enforcement (the `MADEIRA_TOOL_RBAC.csv` validator owns that); voice or personality posture (the personality-side SOP — `SOP-TECH_MADEIRA_PERSONALITY_001.md` — owns that and is forward-chartered to Lane B of I76 P3 pending voice canonical research closure).

## 3. Inputs

### 3.1 The SSOT: the registry CSV

The single source of truth is [`dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv`](./dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv) (21 columns). Every operation in this SOP is parameterised by a row in that CSV — the CSV is the inventory; this SOP is the contract on what the columns mean. Do not enumerate vehicles in this prose; query the CSV.

### 3.2 Per-row metadata Madeira reads

Each row carries:

- `vehicle_id` (PK; matches `^vehicle_[a-z0-9_]+$`).
- `vehicle_path` — the file / path-pattern / external-system reference.
- `vehicle_scope` — `per_session` / `cross_session` / `methodology_scoped` / `wave_bounded`.
- `target_audience` — semicolon-list of `operator_private` / `operator_plus_aics` / `external_handoff`.
- `write_authority` — `operator_only` / `madeira_writes_flagged` / `agent_writes_auto`.
- `read_cadence` — `every_session` / `on_demand` / `methodology_checkpoint` / `wave_boundary` / `next_session_entry`.
- `staleness_days` (optional int) + `staleness_posture` — `none` / `cite_and_flag` / `refuse_without_ratify`.
- `provenance`, `memory_class`, `owner_role`, `topic_ids`, `depends_on_vehicle_ids`, `status`, `added_at`, `last_review_at`, `last_review_by`, `methodology_version_at_review`, `last_review_decision_id`, `notes`.

The Pydantic SSOT at [`akos/hlk_madeira_persistence_vehicle.py`](../../../../../../akos/hlk_madeira_persistence_vehicle.py) is the schema authority; the validator at [`scripts/validate_madeira_persistence_vehicle.py`](../../../../../../scripts/validate_madeira_persistence_vehicle.py) is the gate.

## 4. Steps

### 4.1 Read a vehicle

The read contract is parameterised by the row's `read_cadence` + `staleness_posture`:

1. **Locate the row** in the registry by `vehicle_id` (or by glob over `vehicle_path` when answering "what does Madeira read at session entry?").
2. **Honour `read_cadence`.** Rows with `every_session` are read at every chat session start. Rows with `methodology_checkpoint` are read at each LOGIC_CHANGE_LOG candidate moment + each decision-row mint. Rows with `wave_boundary` are read at I86-style wave entry + exit. Rows with `next_session_entry` are read once at the start of the immediately-following session, then archived. Rows with `on_demand` are searched (not read) when relevant — they are not active substrate.
3. **Honour `target_audience` on read.** A row tagged `operator_private` is operator-only; Madeira may read but never quote in an external-handoff artefact. A row tagged `operator_plus_aics` may flow into AKOS-internal SOPs / decision logs / agent transcripts. A row tagged `external_handoff` may flow into adviser handoff packs / dossiers / external dossiers when the engagement's audience tag matches per [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc).
4. **Apply the staleness posture** (see §5 below) — Madeira does not read a stale row silently.

### 4.2 Write a vehicle

The write contract is parameterised by the row's `write_authority`:

1. **`operator_only`.** Madeira may **surface candidate text** via inline AskQuestion per [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc), but the operator types the bytes. Madeira never writes the file. Examples: cursor rules, cursor skills (today).
2. **`madeira_writes_flagged`.** Madeira may write when the operator ratifies inline + the write commits via git (mechanical trail). Every such write produces a commit — no silent / out-of-band writes. Examples: decision register, logic change log, master roadmap, files-modified CSVs, session-FYI tracker (planned).
3. **`agent_writes_auto`.** A runbook / agent writes automatically without per-write ratification. Reserved for per-session ephemeral surfaces or external-system writes whose authoritative store lives outside the repo (e.g. agent transcripts, future Cursor-memory layer once activated). Should be rare for cross-session vehicles.
4. **Audience-tag re-check on write.** Before persisting bytes, Madeira re-evaluates `target_audience` against the bytes-being-written. If the bytes contain content forbidden by the audience tag (e.g. an external-handoff row gaining operator-private content; or vice versa), surface the conflict via inline ratify rather than write the row.

### 4.3 Add a new vehicle

Adding a vehicle is a registry-row-append, not an SOP edit. The contract:

1. **Author the row** in [`dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv`](./dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv) with all 21 columns populated. Pick `status: planned` if the vehicle is not yet in active use; `status: active` only after the read / write surfaces are implemented and tested.
2. **Open a PR** with the CSV change + any sibling deliverables (e.g. if the vehicle is a new markdown file, the file lands in the same PR).
3. **Operator ratify gate.** Adding a vehicle is a canonical-CSV gate per [`akos-governance-remediation.mdc`](../../../../../../.cursor/rules/akos-governance-remediation.mdc): explicit operator approval before merge.
4. **Validators must pass.** [`scripts/validate_madeira_persistence_vehicle.py`](../../../../../../scripts/validate_madeira_persistence_vehicle.py) (header parity + per-row Pydantic + uniqueness + depends_on closure + FK to `DECISION_REGISTER.csv` and `TOPIC_REGISTRY.csv`) must pass; in `--strict` mode it gates the release.
5. **Append a `D-IH-NN-X` decision row** to [`DECISION_REGISTER.csv`](../../../People/Compliance/canonicals/DECISION_REGISTER.csv) describing why the vehicle was added; cite that decision in the new row's `last_review_decision_id`.

### 4.4 Deprecate a vehicle

Deprecating a vehicle is the inverse of adding it:

1. **Flip `status` to `deprecated`** in the CSV row (do not delete — the row remains for traceability).
2. **Update `last_review_at` + `last_review_by` + `last_review_decision_id`** to point at the deprecation decision row.
3. **Append a `D-IH-NN-X` decision row** to [`DECISION_REGISTER.csv`](../../../People/Compliance/canonicals/DECISION_REGISTER.csv) explaining the deprecation rationale + the successor vehicle (if any).
4. **Audit `depends_on_vehicle_ids`.** Any active row that depends on the deprecated row must be updated to depend on the successor (or have its own deprecation queued).
5. **Audit `vehicle_path` consumers.** Search the codebase for the path; any reader still pointing at it must be migrated.

## 5. Staleness posture

Each row's `staleness_posture` controls Madeira's read-time behaviour when the underlying file's mtime is older than the row's `staleness_days`:

| Posture | Behaviour |
|:---|:---|
| `none` | No staleness check. The row is always treated as fresh. Used when freshness is enforced by another mechanism (wave-boundary discipline; per-row `commit_date` audit trail; etc.). `staleness_days` MUST be empty. |
| `cite_and_flag` | Madeira may quote the row, but appends an inline staleness note at quotation time. The operator decides whether to re-ratify. `staleness_days` MUST be set. |
| `refuse_without_ratify` | Madeira will NOT act on the row's content until the operator re-ratifies it via an inline AskQuestion gate per [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc). Reserved for the highest-blast-radius decisions. `staleness_days` MUST be set. |

**Inline staleness note shape** (for `cite_and_flag`): when Madeira quotes a row whose staleness threshold is exceeded, it appends a one-sentence inline note immediately after the quotation, pointing at the row's `last_review_at` + `last_review_decision_id` and asking whether to re-ratify before the operator depends on the quote. Example: *"(Quoted from `D-IH-76-A` ratified 2026-05-15; row passed its 90-day staleness window on 2026-08-13 — re-ratify before depending on this for an external commitment.)"*

The Pydantic SSOT enforces alignment mechanically: `posture: none` requires `staleness_days: null`; `posture in {cite_and_flag, refuse_without_ratify}` requires `staleness_days` non-empty. Misalignment is a `ValidationError` at validator-run time, not a runtime surprise.

## 6. Audience-tag awareness

The `target_audience` column closes the read + write half of the [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc) discipline. The three values:

- **`operator_private`** — current operator only. The vehicle MAY contain CORPINT-internal vocabulary per [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc). Never quoted in external-handoff artefacts.
- **`operator_plus_aics`** — operator + future AICs in the same role-class (J-OP + AI O5-1 role-class). May flow between Madeira sessions across operator instances. Internal register OK; never rendered to a non-cleared audience.
- **`external_handoff`** — also reachable by external-handoff AICs / human receivers when their engagement exposes a quoted decision (J-AD post-NDA; J-CU; J-PT post-NDA per [`akos-adviser-engagement.mdc`](../../../../../../.cursor/rules/akos-adviser-engagement.mdc)). Must be **dual-register clean** — the row's content must read as professional research / structured methodology in the external register before it ships externally.

When a vehicle is tagged with multiple audiences (semicolon-list), Madeira treats the union: `operator_plus_aics;external_handoff` means the row may flow inward to AICs AND outward to external-handoff packs; Madeira must hold both registers (the internal operator register AND the translated external register) when authoring rows tagged that way.

## 7. Failure modes

### 7.1 Stale-constraint mis-encoded

`staleness_days` set with `staleness_posture: none`, OR vice versa. The Pydantic validator catches this at row mint time — never lands. If it surfaces in a regression, the row was minted out-of-band and the validator wasn't run; re-run [`scripts/validate_madeira_persistence_vehicle.py`](../../../../../../scripts/validate_madeira_persistence_vehicle.py) to flag.

### 7.2 Audience leak on write

Madeira writes `external_handoff`-bound bytes into an `operator_private` row, OR vice versa. Audit trail lives in the commit's diff against the row's `target_audience`. Mitigation: the [`scripts/madeira_personality_check.py`](../../../../../../scripts/madeira_personality_check.py) runbook scans every output for internal-register tokens before showing to operator; rows tagged `external_handoff` MUST pass the personality check before persistence.

### 7.3 Self-dependency or unknown depends_on FK

A row's `depends_on_vehicle_ids` references itself, OR references a `vehicle_id` that does not exist in the registry. The Pydantic validator catches both at registry-level. Mitigation: regenerate the FK list when a depended-on row is deprecated.

### 7.4 Stale read against a `refuse_without_ratify` row

Madeira encounters a row past its staleness threshold whose posture is `refuse_without_ratify`. Madeira halts execution + surfaces an inline AskQuestion gate. Operator either (a) re-ratifies inline + advances `last_review_at` in the row + lands the change in the same commit, or (b) accepts the stop-and-clarify and routes the work elsewhere.

### 7.5 Vehicle path glob expands to zero files

A row's `vehicle_path` is a path-pattern (e.g. `<NN>` or `*`) that matches no files at runtime. The runbook reports SKIPPED for that row + the operator decides whether the row should flip to `inactive` (no longer used) or remain `active` (the absence is structural, e.g. a wave-bounded vehicle drained at wave-close).

## 8. Paired runbook

The paired runbook per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1 is [`scripts/madeira_persistence_check.py`](../../../../../../scripts/madeira_persistence_check.py). It:

- Reads the registry CSV.
- For each `active` row with `staleness_days` set, computes `(today - file mtime)` against the resolved `vehicle_path` (with glob expansion for `<NN>` / `*` / `<date>` / `<slug>` patterns).
- Flags rows whose mtime exceeds `staleness_days` as `STALE`.
- Returns a human-readable summary table (`vehicle_id`, `last_modified`, `age_days`, `staleness_posture`, verdict).
- Supports `--json` for machine-readable output.
- Supports `--vehicle-id <id>` to check a single vehicle.
- Skips `planned` + `inactive` rows.

The runbook is the call surface for operator-initiated freshness audits; the validator is the gate that runs in CI.

## 9. Cross-references

### 9.1 Cursor rules

- [`akos-holistika-operations.mdc`](../../../../../../.cursor/rules/akos-holistika-operations.mdc) — canonical-CSV gate posture (Pydantic + validator + Supabase mirror pattern).
- [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1 — paired SOP + runbook pairing rule (this SOP + `scripts/madeira_persistence_check.py`).
- [`akos-planning-traceability.mdc`](../../../../../../.cursor/rules/akos-planning-traceability.mdc) — initiative discipline; this SOP lands as part of I76 P3.
- [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) — when persistence-vehicle conflicts surface (e.g. an audience-tag conflict between operator and Madeira), surface as inline ratify or executive-call recovery.
- [`akos-agent-checkpoint-discipline.mdc`](../../../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — pause records + self-checkpoints are themselves vehicles in the registry (`vehicle_pause_record` + `vehicle_self_checkpoint`).
- [`akos-brand-baseline-reality.mdc`](../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — dual-register vocabulary contract; `external_handoff`-tagged rows must hold both registers.
- [`akos-external-render-discipline.mdc`](../../../../../../.cursor/rules/akos-external-render-discipline.mdc) — six-surface render contract; `external_handoff` rows that ship to non-J-OP audiences need a render trail.

### 9.2 Sibling MADEIRA canonicals

- [`MADEIRA_MODE_PARITY.md`](./MADEIRA_MODE_PARITY.md) — the 5-mode taxonomy that names what Madeira may do.
- [`MADEIRA_TOOL_CATALOG.md`](./MADEIRA_TOOL_CATALOG.md) + [`dimensions/MADEIRA_TOOL_RBAC.csv`](./dimensions/MADEIRA_TOOL_RBAC.csv) — the tool catalog that names which tools Madeira may call.
- [`dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv`](./dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv) — the registry this SOP operationalises.
- `SOP-TECH_MADEIRA_PERSONALITY_001.md` — forward-chartered to Lane B of I76 P3 (voice canonical research pending); will pair with [`scripts/madeira_personality_check.py`](../../../../../../scripts/madeira_personality_check.py) which already exists as the call surface for self-policing.

### 9.3 Compliance cross-references

- [`PRECEDENCE.md`](../../../People/Compliance/canonicals/PRECEDENCE.md) — registers `MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv` as a canonical CSV.
- [`DECISION_REGISTER.csv`](../../../People/Compliance/canonicals/DECISION_REGISTER.csv) — `D-IH-76-F` mints this canonical; `last_review_decision_id` per row FK-resolves here.
- [`dimensions/TOPIC_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv) — `topic_ids` per row FK-resolves here.

## 10. Maintenance

- **Owner.** System Owner (primary); Founder + PMO co-owners.
- **Cadence.** `event_triggered` per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 3 — fires on (a) registry row append / status flip / deprecation, (b) staleness-runbook reporting STALE on an `active` row, (c) audience-tag drift surfaced by [`scripts/madeira_personality_check.py`](../../../../../../scripts/madeira_personality_check.py).
- **Revision rule.** Schema changes (column add / remove / rename) require a `D-IH-76-*` revision decision + Pydantic SSOT update + validator update + this SOP §3.2 update in the same commit; row content edits do not require an SOP revision.
