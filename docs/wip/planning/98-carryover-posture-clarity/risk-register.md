# I98 — Risk Register

| ID | Risk | L | I | Mitigation |
|:---|:---|:---|:---|:---|
| R-IH-98-1 | Agents continue bare "deferred" prose | M | M | Operator comm RULE 5 + validate_carryover_posture on index |
| R-IH-98-2 | Index drift from decision logs | M | H | P2 backfill + INITIATIVE_DEPENDENCIES carryover edges |
| R-IH-98-3 | Vault promotion before sweep evidence | L | H | P4 hard stop before P5 |
| R-IH-98-4 | Cross-area sweep scope explosion | M | M | Batched subagents + parent synthesis only |
