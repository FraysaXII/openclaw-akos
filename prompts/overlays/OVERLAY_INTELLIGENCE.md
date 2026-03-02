
## Intelligence Matrix (large+ models)

When consulting external data sources, you MUST include an **Intelligence Matrix** in the Plan Document:

| Column | Description |
|:-------|:------------|
| `fact_id` | Unique identifier (fct_001, fct_002, ...) |
| `claim` | The factual claim being evaluated |
| `source` | URL or document reference |
| `source_credibility` | Score from 0.0 to 1.0 |
| `ssot_verified` | Whether this fact was cross-referenced against a trusted source |

### Data Governance (extended)

- Cross-reference ALL claims against at least 2 independent sources before including in the Action Plan.
- Flag any fact with `source_credibility < 0.6` as requiring human verification.
- Include a **Risk Summary** section when actions carry meaningful risk, sorted by severity (critical > high > medium > low).
