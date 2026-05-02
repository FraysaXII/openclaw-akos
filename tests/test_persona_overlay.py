"""Initiative 47 P11 tests — persona-conditioned MADEIRA prompts.

Coverage:
- prompts/overlays/PERSONA_OVERLAY.md exists
- All 4 Tier-1 personas have prompts/personas/<id>/MADEIRA_HINTS.md
- Each persona hint fragment <= PERSONA_HINT_MAX_CHARS (operator floor)
- assemble-prompts.py --persona flag exists in CLI
- Persona-conditioned MADEIRA standard variant <= bootstrapMaxChars (R-47-9)
- Persona-conditioned variant SWAPS OUT OVERLAY_HLK_GRAPH (architectural decision)
- Soft-fail: missing persona fragment does not crash assembly
- All MADEIRA_BASE invariants survive in persona-conditioned variant
- Non-MADEIRA agents are NOT affected by --persona flag (only MADEIRA gets persona overlay)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

ASSEMBLE = REPO_ROOT / "scripts" / "assemble-prompts.py"
OVERLAY = REPO_ROOT / "prompts" / "overlays" / "PERSONA_OVERLAY.md"
PERSONAS_DIR = REPO_ROOT / "prompts" / "personas"
MADEIRA_BASE = REPO_ROOT / "prompts" / "base" / "MADEIRA_BASE.md"
BOOTSTRAP_MAX_CHARS = 20_000
PERSONA_HINT_MAX_CHARS = 500

TIER1_PERSONAS = [
    "PERSONA-INVESTOR-COLD",
    "PERSONA-INVESTOR-WARM",
    "PERSONA-ADVISOR-REFERRAL",
    "PERSONA-CUSTOMER-KIRBE-PROSPECT",
]


# ---------------------------------------------------------------------------
# File existence + size discipline
# ---------------------------------------------------------------------------

def test_persona_overlay_framework_exists() -> None:
    assert OVERLAY.is_file()


def test_all_tier1_personas_have_madeira_hints() -> None:
    for pid in TIER1_PERSONAS:
        hints = PERSONAS_DIR / pid / "MADEIRA_HINTS.md"
        assert hints.is_file(), f"missing MADEIRA_HINTS.md for Tier-1 persona {pid}"


@pytest.mark.parametrize("persona_id", TIER1_PERSONAS)
def test_persona_hint_within_size_floor(persona_id: str) -> None:
    """D-IH-47-I: operator-authored fragment <= PERSONA_HINT_MAX_CHARS (500)."""
    hints = PERSONAS_DIR / persona_id / "MADEIRA_HINTS.md"
    chars = len(hints.read_text(encoding="utf-8"))
    assert chars <= PERSONA_HINT_MAX_CHARS, (
        f"{persona_id} MADEIRA_HINTS.md is {chars} chars (cap {PERSONA_HINT_MAX_CHARS})"
    )


# ---------------------------------------------------------------------------
# CLI surface
# ---------------------------------------------------------------------------

def test_assemble_prompts_help_exposes_persona_flag() -> None:
    proc = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--help"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    assert proc.returncode == 0
    assert "--persona" in proc.stdout
    assert "PERSONA_OVERLAY" in proc.stdout or "MADEIRA_HINTS" in proc.stdout


# ---------------------------------------------------------------------------
# Bootstrap size discipline (R-47-9)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("persona_id", TIER1_PERSONAS)
def test_persona_conditioned_madeira_under_bootstrap_max(persona_id: str) -> None:
    """R-47-9: persona-conditioned MADEIRA standard <= bootstrapMaxChars (20000)."""
    proc = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--variant", "standard", "--dry-run", "--persona", persona_id],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # Find the MADEIRA line and parse its char count.
    for line in proc.stdout.splitlines():
        if f"MADEIRA_PROMPT.standard.{persona_id}.md" in line:
            # "[DRY-RUN] MADEIRA_PROMPT.standard.X.md: NNN chars, ..."
            import re
            m = re.search(r":\s*(\d+)\s*chars", line)
            assert m, f"failed to parse char count in: {line}"
            chars = int(m.group(1))
            assert chars <= BOOTSTRAP_MAX_CHARS, (
                f"{persona_id} pushes MADEIRA standard to {chars} chars (cap {BOOTSTRAP_MAX_CHARS})"
            )
            return
    pytest.fail(f"no MADEIRA_PROMPT.standard.{persona_id}.md line found in dry-run output")


@pytest.mark.parametrize("persona_id", TIER1_PERSONAS)
def test_persona_conditioned_swaps_out_hlk_graph(persona_id: str, tmp_path: Path) -> None:
    """Architectural: persona-conditioned MADEIRA does NOT include OVERLAY_HLK_GRAPH."""
    # Build the persona variant to a temp output by reading the dry-run preview's content
    # via an auxiliary approach: assemble live to temp dir.
    proc = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--variant", "standard", "--persona", persona_id],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

    out = REPO_ROOT / "prompts" / "assembled" / f"MADEIRA_PROMPT.standard.{persona_id}.md"
    assert out.is_file()
    content = out.read_text(encoding="utf-8")
    # OVERLAY_HLK_GRAPH content should NOT appear (it gets swapped out for persona variant).
    overlay_hlk_graph = (REPO_ROOT / "prompts" / "overlays" / "OVERLAY_HLK_GRAPH.md").read_text(encoding="utf-8")
    # Pick a unique signature line from OVERLAY_HLK_GRAPH that should NOT be in persona variant.
    # Use a cluster of words distinctive to that overlay.
    for marker_line in overlay_hlk_graph.splitlines():
        marker_line = marker_line.strip()
        if marker_line and len(marker_line) > 30 and not marker_line.startswith("#"):
            # Found a non-trivial marker line.
            assert marker_line not in content, (
                f"OVERLAY_HLK_GRAPH content leaked into persona variant: {marker_line[:60]!r}..."
            )
            break


@pytest.mark.parametrize("persona_id", TIER1_PERSONAS)
def test_persona_conditioned_includes_persona_hints(persona_id: str) -> None:
    """Persona variant must INCLUDE the per-persona hint header."""
    proc = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--variant", "standard", "--persona", persona_id],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert proc.returncode == 0
    out = REPO_ROOT / "prompts" / "assembled" / f"MADEIRA_PROMPT.standard.{persona_id}.md"
    content = out.read_text(encoding="utf-8")
    assert f"### {persona_id}" in content, f"persona hint header missing for {persona_id}"


# ---------------------------------------------------------------------------
# Soft-fail behaviour
# ---------------------------------------------------------------------------

def test_persona_overlay_soft_fail_for_missing_persona() -> None:
    """Missing persona fragment must NOT crash; framework only is appended."""
    proc = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--variant", "standard", "--persona", "PERSONA-NONE-EXISTS"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = REPO_ROOT / "prompts" / "assembled" / "MADEIRA_PROMPT.standard.PERSONA-NONE-EXISTS.md"
    assert out.is_file()
    content = out.read_text(encoding="utf-8")
    # Framework is appended; no per-persona fragment header.
    assert "### PERSONA-NONE-EXISTS" not in content


def test_persona_flag_does_not_affect_non_madeira_agents() -> None:
    """Only MADEIRA gets persona overlay; other agents have no persona suffix in filename."""
    proc = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--variant", "standard", "--persona", "PERSONA-INVESTOR-COLD"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert proc.returncode == 0
    # Non-MADEIRA agents should be the regular file (no persona suffix)
    for agent in ("ORCHESTRATOR", "ARCHITECT", "EXECUTOR", "VERIFIER"):
        regular = REPO_ROOT / "prompts" / "assembled" / f"{agent}_PROMPT.standard.md"
        with_persona = REPO_ROOT / "prompts" / "assembled" / f"{agent}_PROMPT.standard.PERSONA-INVESTOR-COLD.md"
        # The regular file should exist (was built); the persona-suffixed one should NOT.
        assert regular.is_file(), f"{agent} standard prompt should still build"
        assert not with_persona.is_file(), f"{agent} should not get a persona-suffixed variant"


# ---------------------------------------------------------------------------
# MADEIRA_BASE invariant survival (R-47-14)
# ---------------------------------------------------------------------------

def test_madeira_base_invariants_survive_persona_overlay() -> None:
    """R-47-14: persona overlay must not override MADEIRA_BASE invariants."""
    proc = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--variant", "standard", "--persona", "PERSONA-INVESTOR-COLD"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert proc.returncode == 0
    base_content = MADEIRA_BASE.read_text(encoding="utf-8")
    out = REPO_ROOT / "prompts" / "assembled" / "MADEIRA_PROMPT.standard.PERSONA-INVESTOR-COLD.md"
    persona_content = out.read_text(encoding="utf-8")
    # Pick at least one marker line from MADEIRA_BASE that should still be in persona variant.
    base_lines = [
        ln for ln in base_content.splitlines() if ln.strip() and not ln.startswith("#")
    ]
    assert len(base_lines) > 5, "MADEIRA_BASE.md should have >5 substantive lines"
    # Check first few invariant-like lines persist
    survived = sum(1 for ln in base_lines[:20] if ln in persona_content)
    assert survived >= 15, f"only {survived}/20 MADEIRA_BASE lines survived; persona overlay may be overriding"
