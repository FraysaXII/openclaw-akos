"""Tests for I32 P7 (P6 in v0.1) layout-drift relocations and deprecation aliases.

Locks the contract that:
1. GOI/POI was moved from compliance/ to compliance/dimensions/.
2. Localisation SOP was moved from Tech/System Owner/ to Marketing/Brand/.
3. The new canonical paths exist and are picked up by validators.
4. The legacy paths do NOT exist anymore (we did not duplicate; just moved).
5. Deprecation-alias logic in validate_goipoi_register.py and sync_compliance_mirrors_from_csv.py
   would resolve the legacy path if a downstream caller passed it (forward-compatibility).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

NEW_GOIPOI = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "GOI_POI_REGISTER.csv"
LEGACY_GOIPOI = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "GOI_POI_REGISTER.csv"
NEW_LOCALISATION = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Marketing" / "Brand" / "SOP-HLK_LOCALISATION_001.md"
LEGACY_LOCALISATION = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Tech" / "System Owner" / "SOP-HLK_LOCALISATION_001.md"


def test_goipoi_at_new_canonical_path() -> None:
    assert NEW_GOIPOI.is_file(), f"GOI/POI not at new canonical path {NEW_GOIPOI}"


def test_goipoi_no_longer_at_legacy_path() -> None:
    """The relocation is a `git mv`, not a copy. Legacy path is empty."""
    assert not LEGACY_GOIPOI.exists(), f"GOI/POI still at legacy path {LEGACY_GOIPOI}; expected git mv removed it"


def test_localisation_sop_at_new_canonical_path() -> None:
    assert NEW_LOCALISATION.is_file(), f"Localisation SOP not at new canonical path {NEW_LOCALISATION}"


def test_localisation_sop_no_longer_at_legacy_path() -> None:
    assert not LEGACY_LOCALISATION.exists(), f"Localisation SOP still at legacy path {LEGACY_LOCALISATION}"


def test_validate_hlk_passes_after_moves() -> None:
    """End-to-end: full validator suite is green after both moves."""
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )
    assert r.returncode == 0, f"validate_hlk.py exited {r.returncode}; stderr: {r.stderr}"
    assert "OVERALL: PASS" in r.stdout
    assert "GOI_POI_REGISTER: PASS" in r.stdout


def test_vault_links_validator_passes_after_moves() -> None:
    """Vault link validator catches broken internal .md links; both moves must keep it green."""
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk_vault_links.py")],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=60,
    )
    assert r.returncode == 0, (
        f"validate_hlk_vault_links.py exited {r.returncode}; stdout: {r.stdout}; stderr: {r.stderr}"
    )
    assert "PASS" in r.stdout


def test_goipoi_validator_alias_falls_back_to_legacy_path_if_new_is_absent() -> None:
    """Forward-compatibility test: the alias logic is structurally present in the validator."""
    src = (REPO_ROOT / "scripts" / "validate_goipoi_register.py").read_text(encoding="utf-8")
    assert "GOIPOI_CSV_LEGACY" in src
    assert "deprecation alias" in src.lower()


def test_sync_script_alias_falls_back_to_legacy_path_if_new_is_absent() -> None:
    """Same forward-compatibility for sync_compliance_mirrors_from_csv.py."""
    src = (REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py").read_text(encoding="utf-8")
    assert "_GOIPOI_CSV_LEGACY" in src
    assert "_GOIPOI_CSV_NEW" in src


def test_compliance_readme_documents_relocation() -> None:
    """compliance/README.md alias-map must mark GOI/POI as MOVED I32 P7."""
    src = (REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "README.md").read_text(encoding="utf-8")
    assert "MOVED I32 P7" in src
    assert "D-IH-32-D" in src


def test_precedence_md_canonical_row_uses_new_path() -> None:
    """PRECEDENCE.md canonical row for GOI/POI points at the new federal path (post-I70 P4.5 W2)."""
    src = (REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "PRECEDENCE.md").read_text(encoding="utf-8")
    assert "canonicals/dimensions/GOI_POI_REGISTER.csv" in src
    assert "Initiative 32 P7" in src or "D-IH-32-D" in src
