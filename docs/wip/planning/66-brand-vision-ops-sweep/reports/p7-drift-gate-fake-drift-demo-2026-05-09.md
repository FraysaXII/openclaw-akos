---
phase: P7
phase_name: Vision + dossier companion drift gates
initiative: I66
date: 2026-05-09
status: complete
report_kind: deliberate_drift_verification
---

# P7 Deliberate Drift Verification

P7 validates drift behavior through fixture-backed tests rather than mutating live canonicals.

## Vision drift

Test coverage:

- `test_extract_public_region_requires_ordered_markers`
- `test_extract_public_region_fails_without_markers`
- `test_real_vision_gate_passes`

Drift mode verified:

- Missing or misordered public-region markers raise a hard error.
- Boilerplate `/vision` must contain required public-vision fragments in EN messages and must reference the expected translation sections.

## Dossier companion drift

Test coverage:

- `test_complete_deck_set_passes`
- `test_public_deck_body_rejects_internal_token`
- `test_missing_companion_fails`

Drift mode verified:

- A deck set without an `.objections.md` companion fails.
- A public deck body containing internal-register vocabulary fails.
- Valid operator-private companions require `access_level: 5`, `classification: operator_private`, and the expected `artifact_kind`.

## Verification Command

```powershell
py scripts\validate_brand_vision_drift.py; py scripts\validate_dossier_companion_drift.py; py -m pytest tests\test_validate_brand_drift_gates.py -q
```

Result:

```text
BRAND_VISION_DRIFT OK
DOSSIER_COMPANION_DRIFT OK - 6 deck(s) have valid companions
33 passed
```

## Rationale

The fixture-backed approach gives the same failure proof without introducing transient bad states into the live brand canon or deck suite. This is safer for a long-running branch with many active files and still proves both validators reject deliberate drift.
