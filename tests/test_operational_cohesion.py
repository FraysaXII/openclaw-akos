"""Tests for scripts/render_operational_cohesion_index.py + the paired
OPERATIONAL_COHESION_DOCTRINE.md PMO canonical (I86 Wave I Lane I-B;
D-IH-86-AM + D-IH-86-AN).

Covers:
- Frontmatter parse roundtrip (positive valid doctrine; negative missing
  delimiters or required fields).
- `linked_canonicals` path-existence check (positive existing path;
  negative missing-path detection).
- J-* extraction from markdown (positive code extraction; negative unknown
  code flagged against AUDIENCE_REGISTRY.csv).
- governance_rules existence check (positive + negative).
- `--dry-run` flag behavior on index subcommand (no file writes).
- `validate` subcommand exit code (0 on clean; 1 on failure).
- `index` subcommand basic emit (file created in artifacts/cohesion/).
- Canonical doctrine on disk validates clean (integration smoke).

All tests grouped under @pytest.mark.unit (the default lane in scripts/test.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import render_operational_cohesion_index as cohesion  # noqa: E402

pytestmark = pytest.mark.unit


# ---------- fixtures ----------


VALID_FRONTMATTER = """\
---
intellectual_kind: doctrine
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md
governance_rules:
  - akos-external-render-discipline.mdc
  - akos-holistika-operations.mdc
language: en
---

# Sample doctrine

Routing for J-OP primary. Forward-charters: J-IN, J-CU, J-PT, J-AD,
J-ENISA, J-RC, J-CO.
"""


@pytest.fixture
def sample_doctrine(tmp_path: Path) -> Path:
    path = tmp_path / "doctrine.md"
    path.write_text(VALID_FRONTMATTER, encoding="utf-8")
    return path


@pytest.fixture
def sample_registry(tmp_path: Path) -> Path:
    path = tmp_path / "AUDIENCE_REGISTRY.csv"
    path.write_text(
        "audience_code,name,register_side\n"
        "J-OP,Operator,internal\n"
        "J-IN,Investor,external\n"
        "J-CU,Customer SME,external\n"
        "J-PT,Partner,external\n"
        "J-AD,Advisor,hybrid\n"
        "J-ENISA,ENISA reviewer,external\n"
        "J-RC,Recruiter,external\n"
        "J-CO,Collaborator,hybrid\n",
        encoding="utf-8",
    )
    return path


@pytest.fixture
def sample_rules_dir(tmp_path: Path) -> Path:
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    (rules_dir / "akos-external-render-discipline.mdc").write_text("stub", encoding="utf-8")
    (rules_dir / "akos-holistika-operations.mdc").write_text("stub", encoding="utf-8")
    return rules_dir


# ---------- frontmatter parse ----------


def test_frontmatter_parses_linked_canonicals_and_rules(sample_doctrine: Path) -> None:
    fm, body = cohesion.parse_doctrine_frontmatter(sample_doctrine)
    assert "HLK_ERP_ARCHITECTURE.md" in fm.linked_canonicals[0]
    assert fm.governance_rules == (
        "akos-external-render-discipline.mdc",
        "akos-holistika-operations.mdc",
    )
    assert "# Sample doctrine" in body


def test_frontmatter_missing_delimiter_raises(tmp_path: Path) -> None:
    path = tmp_path / "broken.md"
    path.write_text("# no frontmatter\n", encoding="utf-8")
    with pytest.raises(ValueError, match="does not start with YAML frontmatter"):
        cohesion.parse_doctrine_frontmatter(path)


def test_frontmatter_unterminated_raises(tmp_path: Path) -> None:
    path = tmp_path / "unterminated.md"
    path.write_text("---\nfoo: bar\n", encoding="utf-8")
    with pytest.raises(ValueError, match="not terminated"):
        cohesion.parse_doctrine_frontmatter(path)


def test_frontmatter_linked_canonicals_must_be_list(tmp_path: Path) -> None:
    path = tmp_path / "bad-list.md"
    path.write_text(
        "---\nlinked_canonicals: a-string-not-a-list\n---\nbody\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="must be a YAML list"):
        cohesion.parse_doctrine_frontmatter(path)


# ---------- audience-code extraction ----------


def test_extract_audience_codes_all_eight(sample_doctrine: Path) -> None:
    _, body = cohesion.parse_doctrine_frontmatter(sample_doctrine)
    codes = cohesion.extract_audience_codes(body)
    assert codes == {"J-OP", "J-IN", "J-CU", "J-PT", "J-AD", "J-ENISA", "J-RC", "J-CO"}


def test_extract_audience_codes_ignores_lowercase_or_partial() -> None:
    body = "References to j-op (lowercase) and JOP (no dash) should not match."
    assert cohesion.extract_audience_codes(body) == set()


def test_load_audience_registry_codes(sample_registry: Path) -> None:
    codes = cohesion.load_audience_registry_codes(sample_registry)
    assert codes == {
        "J-OP", "J-IN", "J-CU", "J-PT", "J-AD", "J-ENISA", "J-RC", "J-CO",
    }


def test_load_audience_registry_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        cohesion.load_audience_registry_codes(tmp_path / "absent.csv")


# ---------- validate_doctrine ----------


def test_validate_clean_when_paths_and_codes_resolve(
    sample_doctrine: Path,
    sample_registry: Path,
    sample_rules_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(cohesion, "REPO_ROOT", REPO_ROOT)
    report = cohesion.validate_doctrine(
        sample_doctrine, sample_registry, sample_rules_dir
    )
    assert report.is_clean
    assert report.missing_canonicals == []
    assert report.unknown_audience_codes == []
    assert report.missing_rules == []


def test_validate_flags_missing_canonical(
    tmp_path: Path,
    sample_registry: Path,
    sample_rules_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    doctrine = tmp_path / "doc.md"
    doctrine.write_text(
        "---\nlinked_canonicals:\n  - does/not/exist.md\ngovernance_rules:\n  - akos-external-render-discipline.mdc\n---\nbody mentions J-OP\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(cohesion, "REPO_ROOT", REPO_ROOT)
    report = cohesion.validate_doctrine(doctrine, sample_registry, sample_rules_dir)
    assert "does/not/exist.md" in report.missing_canonicals
    assert not report.is_clean


def test_validate_flags_unknown_audience_code(
    tmp_path: Path,
    sample_registry: Path,
    sample_rules_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    doctrine = tmp_path / "doc.md"
    doctrine.write_text(
        "---\nlinked_canonicals: []\ngovernance_rules: []\n---\nJ-OP is fine but J-ZZZ is not.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(cohesion, "REPO_ROOT", REPO_ROOT)
    report = cohesion.validate_doctrine(doctrine, sample_registry, sample_rules_dir)
    assert "J-ZZZ" in report.unknown_audience_codes
    assert not report.is_clean


def test_validate_flags_missing_governance_rule(
    tmp_path: Path,
    sample_registry: Path,
    sample_rules_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    doctrine = tmp_path / "doc.md"
    doctrine.write_text(
        "---\nlinked_canonicals: []\ngovernance_rules:\n  - nonexistent-rule.mdc\n---\nbody J-OP\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(cohesion, "REPO_ROOT", REPO_ROOT)
    report = cohesion.validate_doctrine(doctrine, sample_registry, sample_rules_dir)
    assert "nonexistent-rule.mdc" in report.missing_rules
    assert not report.is_clean


# ---------- render_index ----------


def test_render_index_dry_run_writes_nothing(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    expected = cohesion.render_index(
        cohesion.DOCTRINE_PATH, output_dir, dry_run=True
    )
    assert expected.parent == output_dir
    assert not output_dir.exists()


def test_render_index_writes_stub(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    written = cohesion.render_index(
        cohesion.DOCTRINE_PATH, output_dir, dry_run=False
    )
    assert written.exists()
    content = written.read_text(encoding="utf-8")
    assert "Operational cohesion index" in content
    assert "OPERATIONAL_COHESION_DOCTRINE.md" in content


# ---------- subcommand routing ----------


def test_validate_subcommand_exit_zero_on_canonical_doctrine() -> None:
    """The canonical doctrine on disk validates clean (integration smoke)."""
    assert cohesion.cmd_validate(_make_args(json_log=False, dry_run=False)) == 0


def test_index_subcommand_dry_run_exits_zero() -> None:
    rc = cohesion.cmd_index(_make_args(json_log=False, dry_run=True))
    assert rc == 0


def test_main_defaults_to_validate() -> None:
    rc = cohesion.main([])
    assert rc == 0


# ---------- helpers ----------


def _make_args(*, json_log: bool, dry_run: bool):
    import argparse

    return argparse.Namespace(json_log=json_log, dry_run=dry_run)
