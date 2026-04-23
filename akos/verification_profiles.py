"""Load verification workflow registry (SSOT: config/verification-profiles.json)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from akos.io import REPO_ROOT

REGISTRY_RELATIVE = Path("config") / "verification-profiles.json"
PYTEST_PREFIX = "__pytest__"


@dataclass(frozen=True, slots=True)
class VerificationStep:
    """One runnable step in a profile."""

    step_id: str
    description: str
    argv: list[str]


def registry_path() -> Path:
    return REPO_ROOT / REGISTRY_RELATIVE


def load_registry() -> dict[str, Any]:
    path = registry_path()
    if not path.is_file():
        raise FileNotFoundError(f"verification registry not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    _validate_registry(data)
    return data


def governance_rubric_suites() -> list[str]:
    """Eval suite directory names for rubric mode (release gate + run-evals --governance-rubric)."""
    data = load_registry()
    out = data.get("eval_rubric_governance_suites")
    if not isinstance(out, list) or not all(isinstance(x, str) and x.strip() for x in out):
        raise ValueError("eval_rubric_governance_suites must be a non-empty list of non-empty strings")
    return [str(x).strip() for x in out]


def list_profile_ids() -> list[str]:
    data = load_registry()
    prof = data.get("profiles")
    if not isinstance(prof, dict):
        return []
    return sorted(prof.keys())


def get_profile(name: str) -> dict[str, Any]:
    data = load_registry()
    prof = data.get("profiles")
    if not isinstance(prof, dict) or name not in prof:
        raise KeyError(f"unknown profile: {name!r} (use {list_profile_ids()!r})")
    return prof[name]


def iter_profile_steps(name: str) -> Iterator[VerificationStep]:
    p = get_profile(name)
    steps = p.get("steps")
    if not isinstance(steps, list):
        raise ValueError(f"profile {name!r} has no steps list")
    for i, row in enumerate(steps):
        if not isinstance(row, dict):
            raise ValueError(f"profile {name!r} step {i} is not an object")
        sid = row.get("id")
        if not isinstance(sid, str) or not sid.strip():
            raise ValueError(f"profile {name!r} step {i} missing id")
        desc = row.get("description", "")
        if not isinstance(desc, str):
            desc = str(desc)
        raw = row.get("argv")
        if not isinstance(raw, list) or not all(isinstance(x, str) for x in raw):
            raise ValueError(f"profile {name!r} step {sid!r} argv must be a list of strings")
        yield VerificationStep(
            step_id=sid.strip(),
            description=desc,
            argv=[str(x) for x in raw],
        )


def profile_description(name: str) -> str:
    p = get_profile(name)
    d = p.get("description", "")
    return d if isinstance(d, str) else str(d)


def resolve_argv(argv: list[str], *, repo_root: Path | None = None) -> list[str]:
    """Turn registry argv into a subprocess argument list (includes sys.executable)."""
    root = repo_root or REPO_ROOT
    if not argv:
        raise ValueError("empty argv in verification step")
    first = argv[0]
    if first == PYTEST_PREFIX:
        return [sys.executable, "-m", "pytest", *argv[1:]]
    norm = first.replace("\\", "/")
    if not norm.startswith("scripts/"):
        raise ValueError(
            f"verification argv must start with {PYTEST_PREFIX!r} or scripts/... got {first!r}"
        )
    script = (root / first).resolve()
    if not script.is_file():
        raise FileNotFoundError(f"script not found: {script}")
    return [sys.executable, str(script), *argv[1:]]


def _validate_registry(data: Any) -> None:
    if not isinstance(data, dict):
        raise ValueError("registry root must be an object")
    v = data.get("version")
    if v != 1:
        raise ValueError(f"unsupported registry version: {v!r}")
    suites = data.get("eval_rubric_governance_suites")
    if not isinstance(suites, list) or not suites:
        raise ValueError("eval_rubric_governance_suites must be a non-empty list")
    if not all(isinstance(x, str) and str(x).strip() for x in suites):
        raise ValueError("eval_rubric_governance_suites must be non-empty strings")
    prof = data.get("profiles")
    if not isinstance(prof, dict) or not prof:
        raise ValueError("profiles must be a non-empty object")
    for pname, pbody in prof.items():
        if not isinstance(pname, str) or not pname.strip():
            raise ValueError("profile names must be non-empty strings")
        if not isinstance(pbody, dict):
            raise ValueError(f"profile {pname!r} must be an object")
        steps = pbody.get("steps")
        if not isinstance(steps, list) or not steps:
            raise ValueError(f"profile {pname!r} must have a non-empty steps array")
        for s in steps:
            if not isinstance(s, dict):
                raise ValueError(f"profile {pname!r} step must be an object")
            _ = s.get("id")
            if not isinstance(_, str) or not _.strip():
                raise ValueError(f"profile {pname!r} step id missing")
            av = s.get("argv")
            if not isinstance(av, list) or not av:
                raise ValueError(f"profile {pname!r} step {s.get('id')!r} needs argv")
            for piece in av:
                if not isinstance(piece, str):
                    raise ValueError(f"profile {pname!r} argv must be strings")
            # Dry-resolve to catch bad paths / forms (no subprocess)
            try:
                resolve_argv([str(x) for x in av], repo_root=REPO_ROOT)
            except (FileNotFoundError, ValueError) as e:
                raise ValueError(
                    f"profile {pname!r} step {s.get('id')!r} argv invalid: {e}"
                ) from e
