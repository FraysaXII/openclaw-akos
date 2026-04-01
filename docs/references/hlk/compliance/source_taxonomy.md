# Source Taxonomy

**Item Name**: Source Category and Source Level Taxonomy
**Item Number**: HLK-COMPLIANCE-SOURCE-001
**Object Class**: Baseline Reference
**Confidence Level**: Safe
**Security Level**: 2 (Internal Use)
**Entity Owner**: Holistika
**Area Owner**: Compliance, Research
**Version**: 1.0
**Revision Date**: 2026-03-31

---

## Description

This document freezes the canonical source taxonomy used to classify the provenance and credibility of intelligence, facts, and information assets. It governs how the Intelligence Matrix and fact tables attribute their source material.

The taxonomy has two tiers:

- **Source categories**: broad classification of information origin
- **Source levels**: granular credibility ladder within each category

## Source Categories

| UUID | Enum value | Name | Description |
|------|------------|------|-------------|
| 76ec559d-d0eb-465a-84e2-49a5fbc63130 | OSINT | Open Source Intelligence | Publicly available information curated for insights |
| 2c63ea92-7a95-4a53-9818-8a97e8802a83 | HUMINT | Human Intelligence | Information obtained directly from human sources |
| 3653d507-56cb-495b-b5aa-9ba6bcb59d85 | SIGINT | Signal Intelligence | Data derived from electronic signals and communications |
| 6710e9bb-e55b-4ba0-9420-69c11daa5f2c | CORPINT | Corporate Intelligence | Derived from internal corporate data and analysis |
| d4e2bded-576c-4c05-953d-f111942d9140 | MOTINT | Mother Intelligence | Primary intelligence source central to operational insights |
| 61595af7-c0d2-4371-895d-a1266a6f221b | TBD | To Be Determined | Source categorization pending further analysis |

## Source Levels

Source levels use a `category.sublevel` numbering scheme where the integer part maps to a source category tier and the decimal part distinguishes credibility granularity within that tier.

| UUID | Level | Name | Category | Category Name | Description |
|------|-------|------|----------|---------------|-------------|
| c2d94771-414d-4c63-b659-6b4b3aaa792d | 1.1 | Public Opinion | 1 | Public | Information reflecting the collective sentiment of the public |
| 28803ca0-a71b-43f2-abc4-442c648719a5 | 1.2 | Public Figure | 1 | Public | Data input from prominent public individuals providing influential insights |
| ad866ea4-e973-44ab-a0a0-f806c07ba991 | 1.3 | Public Knowledge | 1 | Public | General knowledge verified from widely trusted sources |
| f196f797-dfb6-46b1-88b3-d1445e5281f7 | 2.1 | Specialized Content Creator | 2 | Social | Expert content contributed by specialists in the field |
| 80fa2410-4e7a-4e08-8178-f7a43e869951 | 2.2 | Specialised Source Facilitator | 2 | Social | Facilitator for access to specialized and curated sources |
| 4aadc272-d140-4743-b270-608c8aa664f8 | 2.3 | Specialised Researcher | 2 | Social | In-depth insights provided by experts actively engaged in research |
| 7b76ff74-5ee5-42ac-aacf-817e427ddde9 | 3.1 | Research Community | 3 | Academia | Aggregated data from a community of researchers sharing best practices |
| b54f1d04-379b-4d3b-b976-4d9dd4e1d10c | 3.2 | Research Organisation | 3 | Academia | Structured research findings by dedicated research organizations |
| 984f7f2f-257b-49f1-b038-c93ae124ab1c | 3.3 | Research Standardisation | 3 | Academia | Standards and benchmarks established within the research sector |
| c0715b8c-97a2-4ecb-92c6-5a1d59b69ef7 | 4.1 | Mainstream Job Knowledge | 4 | Professional | Insights based on common industry practices and job experiences |
| 547cb321-9dfc-4a14-bd90-c42a21b90b9d | 4.2 | Par Job Knowledge | 4 | Professional | Partial insights serving as preliminary references from industry roles |
| b23bdc69-c524-491a-9ba4-4cd08ae47f5a | 4.3 | State-Of-The-Art | 4 | Professional | Cutting-edge research reflecting the latest best practices |
| 8ab8182a-2349-49d2-97e7-ae790136b4c6 | 5.1 | Organisation Capability Improver | 5 | Organisational | Data and methods aimed at enhancing organizational performance |
| f1f26be4-2be5-45b5-84cf-5193e44349c8 | 5.2 | Organisation Capability Designer | 5 | Organisational | Concepts for designing robust organizational capabilities |
| d9d7a049-8ed1-4ad4-9899-308fa2c4acd6 | 5.3 | Organisation Capability Approver | 5 | Organisational | Validated approaches for organizational improvement |
| 6652142f-210e-48e3-bbf7-767d486ab66d | 6.1 | Secret | 6 | Secret | Highly classified internal information under strict access controls |
| 43a97d24-b2fc-40a0-9fd8-98e477df9f0b | 6.2 | Secret | 6 | Secret | Highly classified internal information under strict access controls |
| b105979e-fb51-4ec6-b3cc-9c86140a8115 | 6.3 | Secret | 6 | Secret | Highly classified internal information under strict access controls |

## Usage In The Intelligence Matrix

When classifying a fact or intelligence item:

1. Assign the `source_category` enum (OSINT, HUMINT, SIGINT, CORPINT, MOTINT, or TBD).
2. Assign the `source_level` numeric value from the ladder above.
3. Record the `intel_source_public_credibility` as a 1-5 score compared to the average for that source type (0 = unknown).
4. Record the `intel_source_holistika_credibility` as the internal assessment score.

## KiRBe Schema Reference

```
compliance.source_category
  id: uuid (PK)
  created_at: timestamptz
  source_category_name: text
  modified_at: timestamptz
  auth_id_last_modify: uuid
  source_category: public.source_category (enum, NOT NULL, default 'TBD')
  category_description: text

compliance.source_level
  source_id: uuid (PK)
  created_at: timestamptz
  source_level: real
  source_name: text
  source_category: smallint (NOT NULL)
  source_category_name: text
  modified_at: timestamptz
  source_description: text
```
