---
language: en
---

# Initiative 31 — Evidence matrix

Maps every claim made by this initiative to its source of truth.

| Claim | Source | Verifiable how |
|:------|:-------|:---------------|
| Holistika operates in EN/ES/FR daily | Founder testimony + existing artifacts in EN (most internal) + ES (dossier_es.md, deck_story_es.md, cover_email_*_es.md) + FR (none today, will be enabled by stub) | Inspect `git ls-files` + frontmatter `language:` field after P1.3 migration |
| Existing GOI/POI register has no distance column today | [`GOI_POI_REGISTER.csv`](../../references/hlk/compliance/GOI_POI_REGISTER.csv) headers row | `head -1 GOI_POI_REGISTER.csv` shows no `distance_band` column |
| Distance bands are N1-N4 ordinal (terminal) | Founder definition (D-IH-31-G) + this initiative's SOP | Read `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` §4.X (after P2 update) |
| All 6 existing GOI/POI rows are direct operational contacts (default N1) | Initiative 21 P0-P5 narrative — every row was created from a direct adviser/banker engagement | Inspect each row's `notes` field; "Operator-managed identity mapping" implies direct relationship |
| Persona registry archetype for joint-equity partner aligns with I30 P2 Channel 6 | [`CHANNEL_STRATEGY.md`](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/CHANNEL_STRATEGY.md) Channel 6 + new `PERSONA-PARTNER-JOINT-EQUITY` row | Cross-reference; both should describe the same archetype with the same intent |
| The 8 highest-leverage touchpoint cells cover the founder's most-used routes | Founder testimony (LinkedIn DMs, email inbound, web form, advisor referrals, joint-equity inbound, hourly-rate vendor outbound, idea-proposer warm DMs, random catch-all) | Read seed table in P4; founder confirms during P4 review |
| Distance-aware routing changes the right template | Operational reality: a cold N4 LinkedIn DM gets a qualifying gate; a warm N1 advisor email gets immediate scheduling | Read in-file variants of `intro_message_*` templates; the N1 vs N3-N4 sections are visibly different |
| Locale-derivation pipeline works | TEMPLATE_OUTBOUND_BRIEF.md ships in EN + ES + FR variants from a single structural source | Read the three files; structure matches; brand voice differs per locale |
| HOLISTIK_OPS_DISCOVERY.md names what was built | Read the meta-doc — it cross-references every register, SOP, and template produced by this initiative | All paths in the doc resolve via `validate_hlk_vault_links.py` |

## How a future operator audits the system

1. Open `discovery-taxonomy.md` to see the 5-axis map.
2. Open each registry CSV to see actual rows.
3. Open `SOP-HLK_LOCALISATION_001.md` to see when to write in which language.
4. Open `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` §4.X to see how to assess distance.
5. Open `HOLISTIK_OPS_DISCOVERY.md` for the cross-axis routing diagram.
6. Run `py scripts/validate_hlk.py` to confirm all axes resolve cleanly.
