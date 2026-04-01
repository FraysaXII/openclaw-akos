# Confidence Levels

**Item Name**: Confidence Level Taxonomy
**Item Number**: HLK-COMPLIANCE-CONFIDENCE-001
**Object Class**: Baseline Reference
**Confidence Level**: Safe
**Security Level**: 2 (Internal Use)
**Entity Owner**: Holistika
**Area Owner**: Compliance, Data Architecture
**Version**: 1.0
**Revision Date**: 2026-03-31

---

## Description

This document freezes the canonical confidence level taxonomy used to classify objects, processes, and intelligence items by their risk profile and required control intensity.

The naming convention is inspired by containment classification principles: the higher the level, the more stringent the controls.

## Confidence Level Definitions

| Level | Name | Description | Typical use |
|-------|------|-------------|-------------|
| 1 | Safe | Minimal risk; standard operating procedures are sufficient. Well-understood items with predictable behavior. | Routine processes, stable infrastructure, established SOPs |
| 2 | Euclid | Moderate risk requiring standard control measures. Items that are generally understood but may exhibit unexpected behavior under certain conditions. | Evolving processes, integrations with external systems, growing workstreams |
| 3 | Keter | High risk; requires stringent controls and restricted access. Items that are difficult to contain, predict, or standardize. | Experimental processes, AI agent execution chains, novel research, high-impact decisions |

## Governance Rules

- Every SOP and process item should carry a confidence level in its metadata.
- Confidence levels inform the depth of review, approval requirements, and monitoring intensity.
- Items without an assigned confidence level default to Euclid (moderate) until explicitly classified.

## Alias Resolution

Several legacy SOPs use the label "High" as a confidence level. This is not a canonical value. The following mapping applies:

| Legacy label | Canonical mapping | Rationale |
|--------------|-------------------|-----------|
| High | Euclid (2) | Default for established SOPs with standard control measures |
| Low | Safe (1) | Minimal risk items with routine procedures |

Validators and ingestion pipelines must normalize legacy labels to canonical values before storing or indexing.

## KiRBe Schema Reference

```
compliance.confidence_level
  id: uuid (PK)
  created_at: timestamptz
  confidence_level: integer
  confidence_level_name: text
  modified_at: timestamptz
  confidence_description: text
```

## Frozen Values

| UUID | Level | Name |
|------|-------|------|
| 9b1f56de-aa36-4edb-9d1e-0841b192d665 | 1 | Safe |
| 6de45a73-bf85-4cce-9342-f268391fed45 | 2 | Euclid |
| c3a417b7-d09e-4e91-8678-7c19a1689d62 | 3 | Keter |
