"""Minimal agent-output postprocessing chain (MADEIRA context economics T2).

Ordered gates per context-economics-wip-spec-2026-06-15.md §5:
citation → brand lint hook → secret/PII placeholder → optional channel truncate.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from akos.eval_harness.adversarial import scan_text_for_pii

GateName = Literal["citation", "brand_lint", "secret_pii", "channel_truncate"]

_CITATION_PATTERN = re.compile(
    r"(SRC-[A-Z0-9-]+|docs/references/hlk/v3\.0/[^\s)\]]+)",
    re.IGNORECASE,
)

# Mirrors tests/conftest.py SECRET_PATTERNS — agent-output gate only.
_SECRET_PATTERNS: tuple[str, ...] = ("sk-", "ghp_", "Bearer ", "-----BEGIN")


@dataclass(frozen=True)
class PostprocessResult:
    ok: bool
    blocked_gates: tuple[GateName, ...] = ()
    messages: tuple[str, ...] = ()


def check_citation_gate(text: str, *, require_citation: bool) -> PostprocessResult:
    if not require_citation:
        return PostprocessResult(ok=True)
    if _CITATION_PATTERN.search(text):
        return PostprocessResult(ok=True)
    return PostprocessResult(
        ok=False,
        blocked_gates=("citation",),
        messages=("Research-facing output must cite SRC-* or a vault canonical path.",),
    )


def check_brand_lint_gate(text: str) -> PostprocessResult:
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from scripts.lint_brand_voice_offline import lint_text

    violations = lint_text(text, Path("<agent-output>"))
    if not violations:
        return PostprocessResult(ok=True)
    first = violations[0]
    return PostprocessResult(
        ok=False,
        blocked_gates=("brand_lint",),
        messages=(
            f"Brand lint blocked output ({first.category}): {first.snippet}",
        ),
    )


def check_secret_pii_gate(text: str) -> PostprocessResult:
    for pat in _SECRET_PATTERNS:
        if pat in text:
            return PostprocessResult(
                ok=False,
                blocked_gates=("secret_pii",),
                messages=(f"Secret-like pattern blocked ({pat!r}).",),
            )
    pii = scan_text_for_pii(text)
    if pii:
        return PostprocessResult(
            ok=False,
            blocked_gates=("secret_pii",),
            messages=(f"PII blocked: {pii[0]}.",),
        )
    return PostprocessResult(ok=True)


def check_channel_truncate_gate(text: str, *, max_chars: int | None) -> PostprocessResult:
    if max_chars is None or len(text) <= max_chars:
        return PostprocessResult(ok=True)
    return PostprocessResult(
        ok=False,
        blocked_gates=("channel_truncate",),
        messages=(f"Output exceeds channel limit ({len(text)} > {max_chars} chars).",),
    )


def run_postprocess_chain(
    text: str,
    *,
    require_citation: bool = False,
    max_channel_chars: int | None = None,
    skip_gates: frozenset[GateName] = frozenset(),
) -> PostprocessResult:
    """Run α0 postprocess chain; failures surface as governed blocks."""
    blocked: list[GateName] = []
    messages: list[str] = []

    checks: list[tuple[GateName, PostprocessResult]] = []
    if "citation" not in skip_gates:
        checks.append(("citation", check_citation_gate(text, require_citation=require_citation)))
    if "brand_lint" not in skip_gates:
        checks.append(("brand_lint", check_brand_lint_gate(text)))
    if "secret_pii" not in skip_gates:
        checks.append(("secret_pii", check_secret_pii_gate(text)))
    if "channel_truncate" not in skip_gates:
        checks.append(
            (
                "channel_truncate",
                check_channel_truncate_gate(text, max_chars=max_channel_chars),
            )
        )

    for _name, result in checks:
        if not result.ok:
            blocked.extend(result.blocked_gates)
            messages.extend(result.messages)

    return PostprocessResult(
        ok=not blocked,
        blocked_gates=tuple(blocked),
        messages=tuple(messages),
    )
