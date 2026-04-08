# Ad hoc operator scripts

One-off helpers for RunPod, endpoints, branding checks, and similar tasks. **Not** part of the release gate or documented operator runbooks unless called out elsewhere.

- Run from the **repository root** so relative paths behave as when these lived at the root, for example:  
  `py scripts/adhoc/_check_endpoint_health.py`
- Prefer promoting stable workflows into `scripts/*.py` with tests and docs when they become routine.

Do not import these modules from `akos/` or from gate scripts.
