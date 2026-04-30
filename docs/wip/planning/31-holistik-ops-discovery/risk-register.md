---
language: en
---

# Initiative 31 — Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:-----|:-----------|:-------|:-----------|
| **R-31-1** | `validate_goipoi_register.py` breaks because the existing 6 rows do not yet have the new columns when the validator runs mid-migration | High | High (CI red mid-migration) | Run schema bump + backfill in a single commit; validator only validates the post-bump state |
| **R-31-2** | Mirror migration applied out-of-order with the CSV change (DDL on Postgres before CSV is on `main`) | Medium | High (live mirror diverges from CSV) | Operator runs `npx supabase db push` **only after PR squash-merge**; SOP runbook explicit; `probe_compliance_mirror_drift.py --verify` post-apply |
| **R-31-3** | `bridge_via` FK creates a cycle (A bridges B, B bridges A) | Low | Medium | Validator detects cycle (depth-first traversal); fails the row and reports the cycle |
| **R-31-4** | Operator confuses persona archetype distance vs. individual GOI/POI distance | Medium | Low | SOP §4.X explicitly distinguishes; persona's `typical_distance_band` is informational; GOI/POI's `distance_band` is operational source of truth |
| **R-31-5** | Auto-rendered PMO hub MD churns whitespace because `render_pmo_hub.py` re-runs with a wider table | Low | Low (one-time diff) | Run renderer once during P2.2 and commit the resulting whitespace shift in the same commit |
| **R-31-6** | FR brand-voice stub introduces churn when first real FR deliverable lands | Low | Low | Stub is `status: stub` and explicitly marked TODO; no canonical claims yet; future initiative promotes to canonical |
| **R-31-7** | `language:` frontmatter migration touches ~80 files and breaks `git blame` annotations | Medium | Low | Acceptable; `git log --follow` recovers history; CHANGELOG calls out the migration |
| **R-31-8** | Pre-existing `validate_configs.py` AKOS sandbox-config failures (out of scope per I29/I30) get attributed to this initiative in CI | Low | Low | UAT report explicitly excludes them, same posture as I29 + I30 |
| **R-31-9** | The 16-persona seed list is too coarse or too fine for the founder's actual routing needs | Medium | Low | Operator follow-up after P2 review; trivial to add/remove rows; persona_id is the only stable handle |
| **R-31-10** | The 10-channel seed list misses a real touchpoint the founder uses (e.g., WhatsApp groups, Telegram, voice messages) | Medium | Low | Same — easy to add `CHAN-WHATSAPP-DM`, `CHAN-TELEGRAM-DM`, `CHAN-VOICE-NOTE` rows post-review |
| **R-31-11** | Touchpoint kit in-file variants (D-IH-31-H) become unwieldy when a single template needs substantially different copy per N-band | Low | Low | Trigger condition documented; D-IH-31-H carries the explicit re-eval rule (split into separate files via render script when needed) |
| **R-31-12** | The HOLISTIK_OPS_DISCOVERY.md meta-doc gets outdated as new registries / axes get added | Low (this initiative) → Medium (long-term) | Medium | Doc has `last_review` frontmatter + cross-references that break the validator if a registered axis is missing |

## Risk-acceptance posture

R-31-1 (validator breaks mid-migration) is the only High × High risk. Mitigation is to use a single commit for the schema bump + backfill + validator update + test extension. The PR cannot be partially-merged; either the whole package ships green or the whole package stays on the branch. Same posture as I21 / I22 / I27 P7 mirror migrations.
