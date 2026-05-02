---
language: en
status: active
---

# Calibration baseline outputs

Operator-local outputs from `scripts/calibrate_scenarios.py` (Initiative 47 P10).

Files in this directory are gitignored except this README. Regenerate with:

```bash
py scripts/calibrate_scenarios.py
```

To hard-fail in CI when any persona drifts outside the ±5pp tolerance:

```bash
py scripts/calibrate_scenarios.py --hard-fail-on-drift
```

The calibration target per D-IH-47-C is 40/40/10/10 (hard/moderate/trivial/impossible).
