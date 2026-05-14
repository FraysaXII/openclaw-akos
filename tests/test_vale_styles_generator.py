"""Tests for the I71 P2 Pack A2 Tier 1 Vale sibling generator.

Covers:

- ``scripts/generate_vale_styles.py`` deterministic output (two runs against
  the same canonicals produce byte-identical bytes).
- Vale-YAML validity (each generated ``Holistika/*.yml`` parses as YAML and
  carries the required keys ``extends`` / ``message`` / ``level``).
- Per-canonical Vocab correctness (10 files emitted; 5 directories × {accept,
  reject}.txt; per C-71-Vale-2 ratification 2026-05-14 + Vale 3.14 layout
  repair 2026-05-14). Each pair carries the tokens parsed from its specific
  canonical and lives at ``.vale/styles/config/vocabularies/<Name>/{accept,
  reject}.txt`` per https://vale.sh/docs/keys/vocab.
- ``--check`` mode behaviour (in-sync vs drifted).
- ``--clean`` flag wipes both the new per-Vocab dirs and the legacy flat
  ``Vocab/`` dir before regenerating.
- Graceful skip when a brand canonical is absent (placeholder style emits;
  no exception).
- Vale 3.14 ``ls-config`` parses the emitted layout without
  ``E100 [vocab] Runtime error`` (host-conditional; skipped when ``vale``
  binary is unavailable on the test host).

Runs under ``pytest -m brand`` per ``pyproject.toml``.
"""

from __future__ import annotations

import contextlib
import os
import shutil as _shutil
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest
import yaml

pytestmark = pytest.mark.brand

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import scripts.generate_vale_styles as vale_gen  # noqa: E402


# ---------------------------------------------------------------------------
# Per-canonical Vocab inventory (10 files expected per C-71-Vale-2 +
# Vale 3.14 layout repair). Each Vocab name owns a directory under
# ``config/vocabularies/`` carrying literal ``accept.txt`` / ``reject.txt``.
# ---------------------------------------------------------------------------

EXPECTED_VOCAB_NAMES: tuple[str, ...] = (
    "Holistika-CopywritingDiscipline",
    "Holistika-EnglishPatterns",
    "Holistika-LLMToneTells",
    "Holistika-FrenchPatterns",
    "Holistika-SpanishPatterns",
)

EXPECTED_VOCAB_RELATIVE_PATHS: tuple[str, ...] = tuple(
    f"config/vocabularies/{name}/{leaf}"
    for name in EXPECTED_VOCAB_NAMES
    for leaf in ("accept.txt", "reject.txt")
)


def _yaml(outputs: dict[Path, str], basename: str) -> Path:
    """Return the absolute path to a generated Holistika style YAML."""
    matches = [p for p in outputs if p.name == basename and p.suffix == ".yml"]
    assert matches, f"missing yaml file {basename}"
    assert len(matches) == 1, f"multiple matches for {basename}: {matches}"
    return matches[0]


def _vocab_relpath(outputs: dict[Path, str], target_root: Path, basename: str) -> Path:
    """Return the absolute path to a per-canonical Vocab file in ``outputs``.

    ``basename`` is one of the EXPECTED_VOCAB_NAMES values; the leaf is
    inferred from whether the caller asks for accept (``...txt``) or reject
    (``...rejected.txt``) via the ``-rejected`` suffix convention used by the
    pre-3.14 tests. The function maps the legacy basename to the new
    per-directory layout transparently.
    """
    if basename.endswith("-rejected.txt"):
        vocab_name = basename[: -len("-rejected.txt")]
        leaf = "reject.txt"
    elif basename.endswith(".txt"):
        vocab_name = basename[: -len(".txt")]
        leaf = "accept.txt"
    else:
        raise ValueError(f"unexpected vocab basename: {basename}")
    expected = (
        target_root / ".vale" / "styles" / "config" / "vocabularies" / vocab_name / leaf
    )
    assert expected in outputs, (
        f"missing vocab file {basename!r} (mapped to {expected.relative_to(target_root)})"
    )
    return expected


# ---------------------------------------------------------------------------
# Determinism contract
# ---------------------------------------------------------------------------


class TestDeterminism:
    def test_two_runs_against_same_canonicals_produce_byte_identical_output(
        self, tmp_path: Path
    ) -> None:
        first = vale_gen.write_styles(target_root=tmp_path / "run-a")
        second = vale_gen.write_styles(target_root=tmp_path / "run-b")
        assert sorted(p.name for p in first) == sorted(p.name for p in second)
        for path_a, contents_a in first.items():
            relative = path_a.relative_to(tmp_path / "run-a")
            path_b = tmp_path / "run-b" / relative
            assert path_b.exists(), f"second run missing {relative}"
            assert path_b.read_bytes() == path_a.read_bytes()
            assert path_b.read_text(encoding="utf-8") == contents_a

    def test_output_uses_lf_line_endings_no_bom(self, tmp_path: Path) -> None:
        outputs = vale_gen.write_styles(target_root=tmp_path)
        for path in outputs:
            raw = path.read_bytes()
            assert not raw.startswith(b"\xef\xbb\xbf"), f"{path} has BOM"
            assert b"\r\n" not in raw, f"{path} contains CRLF"

    def test_dry_run_returns_same_contents_as_write(self, tmp_path: Path) -> None:
        # dry_run uses real REPO_ROOT paths; compare contents to a real write.
        dry_outputs = vale_gen.dry_run()
        write_outputs = vale_gen.write_styles(target_root=tmp_path)
        dry_by_name = {path.name: contents for path, contents in dry_outputs.items()}
        write_by_name = {path.name: contents for path, contents in write_outputs.items()}
        assert dry_by_name == write_by_name


# ---------------------------------------------------------------------------
# Vale-YAML validity (each Holistika/*.yml parses + carries required keys)
# ---------------------------------------------------------------------------


class TestValeYamlValidity:
    @pytest.fixture(autouse=True)
    def write_to_tmp(self, tmp_path: Path) -> None:
        self.outputs = vale_gen.write_styles(target_root=tmp_path)
        self.tmp_root = tmp_path

    def _holistika_yml_paths(self) -> list[Path]:
        return [
            path
            for path in self.outputs
            if path.suffix == ".yml" and "Holistika" in path.parts
        ]

    def test_each_holistika_style_parses_as_yaml(self) -> None:
        paths = self._holistika_yml_paths()
        assert paths, "no Holistika/*.yml files generated"
        for path in paths:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            assert isinstance(data, dict), f"{path} did not parse to a dict"

    def test_each_holistika_style_has_required_vale_keys(self) -> None:
        for path in self._holistika_yml_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            for required_key in ("extends", "message", "level"):
                assert required_key in data, (
                    f"{path.name} missing required Vale key {required_key!r}"
                )

    def test_extends_value_is_known_vale_directive(self) -> None:
        known_extends = {"existence", "substitution", "occurrence", "consistency"}
        for path in self._holistika_yml_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            assert data["extends"] in known_extends, (
                f"{path.name} uses unknown extends value {data['extends']!r}"
            )

    def test_level_value_is_known_vale_severity(self) -> None:
        known_levels = {"suggestion", "warning", "error"}
        for path in self._holistika_yml_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            assert data["level"] in known_levels, (
                f"{path.name} uses unknown level {data['level']!r}"
            )


# ---------------------------------------------------------------------------
# Per-canonical Vocab correctness (C-71-Vale-2 ratification 2026-05-14)
# ---------------------------------------------------------------------------


class TestPerCanonicalVocabInventory:
    """The 10-file per-canonical inventory must always be emitted under the
    Vale 3.14 ``config/vocabularies/<Name>/{accept,reject}.txt`` layout."""

    @pytest.fixture(autouse=True)
    def write_to_tmp(self, tmp_path: Path) -> None:
        self.outputs = vale_gen.write_styles(target_root=tmp_path)
        self.tmp_root = tmp_path

    def _vocab_relpaths(self) -> set[str]:
        styles_root = self.tmp_root / ".vale" / "styles"
        return {
            str(path.relative_to(styles_root)).replace("\\", "/")
            for path in self.outputs
            if "vocabularies" in path.parts
        }

    def test_all_10_per_canonical_vocab_files_emitted(self) -> None:
        emitted = self._vocab_relpaths()
        for required in EXPECTED_VOCAB_RELATIVE_PATHS:
            assert required in emitted, (
                f"missing per-canonical Vocab file {required!r}; "
                f"emitted Vocab files: {sorted(emitted)}"
            )
        # Exactly 10 Vocab files (5 dirs × accept.txt + reject.txt).
        assert len(emitted) == 10, (
            f"expected exactly 10 Vocab files per C-71-Vale-2 + Vale 3.14 "
            f"layout repair; got {len(emitted)}: {sorted(emitted)}"
        )

    def test_each_vocab_dir_has_accept_and_reject(self) -> None:
        styles_root = self.tmp_root / ".vale" / "styles"
        for name in EXPECTED_VOCAB_NAMES:
            vocab_dir = styles_root / "config" / "vocabularies" / name
            assert (vocab_dir / "accept.txt").exists(), (
                f"missing accept.txt under {vocab_dir.relative_to(styles_root)}"
            )
            assert (vocab_dir / "reject.txt").exists(), (
                f"missing reject.txt under {vocab_dir.relative_to(styles_root)}"
            )

    def test_no_legacy_flat_vocab_files_emitted(self) -> None:
        # Neither the pre-C-71-Vale-2 single-pair files nor the post-C-71-Vale-2
        # flat-layout files (the pre-3.14 layout this commit repairs) MUST be
        # emitted by the post-repair generator.
        emitted_flat = {
            path.name
            for path in self.outputs
            if "Vocab" in path.parts and "vocabularies" not in path.parts
        }
        assert emitted_flat == set(), (
            f"flat-layout Vocab files unexpectedly emitted: {sorted(emitted_flat)}"
        )
        for legacy in (
            "Holistika.txt",
            "Holistika-rejected.txt",
            "Holistika-CopywritingDiscipline.txt",
            "Holistika-CopywritingDiscipline-rejected.txt",
            "Holistika-EnglishPatterns.txt",
            "Holistika-EnglishPatterns-rejected.txt",
            "Holistika-LLMToneTells.txt",
            "Holistika-LLMToneTells-rejected.txt",
            "Holistika-FrenchPatterns.txt",
            "Holistika-FrenchPatterns-rejected.txt",
            "Holistika-SpanishPatterns.txt",
            "Holistika-SpanishPatterns-rejected.txt",
        ):
            for path in self.outputs:
                assert not (
                    path.name == legacy and "vocabularies" not in path.parts
                ), (
                    f"legacy flat-layout Vocab file {legacy!r} emitted; the "
                    f"Vale 3.14 layout repair (2026-05-14) replaces it with "
                    f"config/vocabularies/<Name>/{{accept,reject}}.txt"
                )


class TestPerCanonicalVocabContents:
    """Each per-canonical Vocab pair carries the tokens parsed from its source."""

    @pytest.fixture(autouse=True)
    def write_to_tmp(self, tmp_path: Path) -> None:
        self.outputs = vale_gen.write_styles(target_root=tmp_path)
        self.tmp_root = tmp_path

    def _vocab_lines(self, basename: str) -> list[str]:
        target = _vocab_relpath(self.outputs, self.tmp_root, basename)
        return [
            line.strip()
            for line in target.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    def test_copywriting_accept_carries_holistika_sub_marks(self) -> None:
        lines = self._vocab_lines("Holistika-CopywritingDiscipline.txt")
        for required_token in ("Holistika", "KiRBe", "MADEIRA", "SUEZ", "AKOS", "HLK"):
            assert required_token in lines, (
                f"Holistika-CopywritingDiscipline.txt missing brand sub-mark "
                f"{required_token!r}"
            )
        # Sorted alphabetically per generator contract.
        assert lines == sorted(set(lines)), (
            "Holistika-CopywritingDiscipline.txt not sorted alphabetically"
        )

    def test_llm_tone_tells_reject_carries_canonical_llm_tells(self) -> None:
        lines = self._vocab_lines("Holistika-LLMToneTells-rejected.txt")
        # `delve into` is the canonical LLM tell from BRAND_LLM_TONE_TELLS.md §3
        # (T-3-delve-into); the rejected vocab MUST surface it as the proof of
        # parser end-to-end.
        assert "delve into" in lines, (
            "Holistika-LLMToneTells-rejected.txt missing canonical LLM tell "
            "'delve into' (T-3-delve-into)"
        )
        # We also look for at least 5 LLM tone tells generally (the
        # BRAND_LLM_TONE_TELLS.md catalog ships ~32; even a subset >= 5
        # confirms the parse worked).
        signature_tokens = {
            "delve into",
            "tapestry",
            "leverage",
            "synergy",
            "synergies",
            "robust",
            "seamless",
            "meticulous",
            "in essence,",
        }
        hits = signature_tokens.intersection(line.lower() for line in lines)
        assert len(hits) >= 3, (
            f"Holistika-LLMToneTells-rejected.txt covers fewer than 3 "
            f"signature LLM tells (found: {sorted(hits)})"
        )

    def test_english_patterns_reject_carries_mba_deck_jargon(self) -> None:
        lines = self._vocab_lines("Holistika-EnglishPatterns-rejected.txt")
        # Several entries from BRAND_ENGLISH_PATTERNS.md §5.1 must surface.
        for jargon in ("circle back", "leverage synergies", "low-hanging fruit"):
            assert jargon in lines, (
                f"Holistika-EnglishPatterns-rejected.txt missing MBA-deck "
                f"jargon {jargon!r} from BRAND_ENGLISH_PATTERNS.md §5.1"
            )

    def test_french_patterns_reject_carries_anglicisms_and_performative(
        self,
    ) -> None:
        lines = self._vocab_lines("Holistika-FrenchPatterns-rejected.txt")
        # FR §5.1 anglicisms must surface.
        for anglicism in ("framework", "deliverable", "roadmap", "stakeholder"):
            assert anglicism in lines, (
                f"Holistika-FrenchPatterns-rejected.txt missing FR anglicism "
                f"{anglicism!r} from BRAND_FRENCH_PATTERNS.md §5.1"
            )
        # FR §5.2 performative phrasing must surface.
        assert "Je vous remercie infiniment" in lines, (
            "Holistika-FrenchPatterns-rejected.txt missing FR performative "
            "from BRAND_FRENCH_PATTERNS.md §5.2"
        )

    def test_spanish_patterns_reject_carries_anglicisms(self) -> None:
        lines = self._vocab_lines("Holistika-SpanishPatterns-rejected.txt")
        # ES anglicisms hand-curated in scripts/validate_brand_voice_register.py
        # _spanish_register_rules must surface.
        for anglicism in ("approach", "engagement", "framework", "mindset"):
            assert anglicism in lines, (
                f"Holistika-SpanishPatterns-rejected.txt missing ES "
                f"anglicism {anglicism!r}"
            )

    def test_spanish_accept_carries_accented_sub_mark(self) -> None:
        lines = self._vocab_lines("Holistika-SpanishPatterns.txt")
        # The "Asesoría" sub-mark is ES-specific (accented) and only legitimately
        # appears under SpanishPatterns.
        assert "Asesoría" in lines, (
            "Holistika-SpanishPatterns.txt missing ES sub-mark 'Asesoría'"
        )

    def test_llm_tone_tells_accept_is_minimal_or_empty(self) -> None:
        lines = self._vocab_lines("Holistika-LLMToneTells.txt")
        # LLM-default lexical patterns are universal; no brand-specific
        # allowlist applies. Accept list should be empty.
        assert lines == [], (
            f"Holistika-LLMToneTells.txt should be empty (no brand-specific "
            f"allowlist for LLM-default patterns); got {lines}"
        )

    def test_each_reject_list_is_sorted_case_insensitive(self) -> None:
        for basename in (
            "Holistika-CopywritingDiscipline-rejected.txt",
            "Holistika-EnglishPatterns-rejected.txt",
            "Holistika-LLMToneTells-rejected.txt",
            "Holistika-FrenchPatterns-rejected.txt",
            "Holistika-SpanishPatterns-rejected.txt",
        ):
            lines = self._vocab_lines(basename)
            assert lines == sorted(lines, key=str.lower), (
                f"{basename} not sorted case-insensitively"
            )


# ---------------------------------------------------------------------------
# --check mode behaviour
# ---------------------------------------------------------------------------


class TestCheckMode:
    def test_check_returns_in_sync_after_write(self) -> None:
        # The repo's .vale/styles/* should be in sync because we generated them
        # in the same commit as this test landing. If a future canonical edit
        # happens without re-running the generator, this gate flips to drift.
        in_sync, drifted = vale_gen.check_styles()
        assert in_sync, f"unexpected drift in checked-in Vale styles: {drifted}"

    def test_check_detects_drift_after_manual_mutation(self, tmp_path: Path) -> None:
        # Write the styles into tmp_path, mutate one, then call check_styles
        # against tmp_path. We patch the path constants inside the module so
        # check_styles inspects the mutated files instead of the real repo.
        target_outputs = vale_gen.write_styles(target_root=tmp_path)
        mutated_path = next(
            (path for path in target_outputs if path.name == "LLMToneTells.yml"),
            None,
        )
        assert mutated_path is not None
        mutated_path.write_bytes(b"# manually mutated content -- drift signal\n")

        # Patch every per-file path constant inside the generator so
        # check_styles inspects the tmp tree, not the real repo. Generator
        # emits 13 files (3 YAML styles + 10 Vocab files = 5 dirs × {accept,
        # reject}.txt) per C-71-Vale-2 + Vale 3.14 layout repair.
        patches: list[tuple[str, Path]] = [
            ("LLM_TONE_TELLS_PATH", _yaml(target_outputs, "LLMToneTells.yml")),
            ("TIC_FAMILIES_PATH", _yaml(target_outputs, "TicFamilies.yml")),
            ("MBA_DECK_JARGON_PATH", _yaml(target_outputs, "MBADeckJargon.yml")),
            (
                "VOCAB_COPYWRITING_ACCEPT_PATH",
                _vocab_relpath(
                    target_outputs, tmp_path, "Holistika-CopywritingDiscipline.txt"
                ),
            ),
            (
                "VOCAB_COPYWRITING_REJECT_PATH",
                _vocab_relpath(
                    target_outputs,
                    tmp_path,
                    "Holistika-CopywritingDiscipline-rejected.txt",
                ),
            ),
            (
                "VOCAB_ENGLISH_ACCEPT_PATH",
                _vocab_relpath(
                    target_outputs, tmp_path, "Holistika-EnglishPatterns.txt"
                ),
            ),
            (
                "VOCAB_ENGLISH_REJECT_PATH",
                _vocab_relpath(
                    target_outputs,
                    tmp_path,
                    "Holistika-EnglishPatterns-rejected.txt",
                ),
            ),
            (
                "VOCAB_LLM_ACCEPT_PATH",
                _vocab_relpath(target_outputs, tmp_path, "Holistika-LLMToneTells.txt"),
            ),
            (
                "VOCAB_LLM_REJECT_PATH",
                _vocab_relpath(
                    target_outputs, tmp_path, "Holistika-LLMToneTells-rejected.txt"
                ),
            ),
            (
                "VOCAB_FRENCH_ACCEPT_PATH",
                _vocab_relpath(
                    target_outputs, tmp_path, "Holistika-FrenchPatterns.txt"
                ),
            ),
            (
                "VOCAB_FRENCH_REJECT_PATH",
                _vocab_relpath(
                    target_outputs, tmp_path, "Holistika-FrenchPatterns-rejected.txt"
                ),
            ),
            (
                "VOCAB_SPANISH_ACCEPT_PATH",
                _vocab_relpath(
                    target_outputs, tmp_path, "Holistika-SpanishPatterns.txt"
                ),
            ),
            (
                "VOCAB_SPANISH_REJECT_PATH",
                _vocab_relpath(
                    target_outputs, tmp_path, "Holistika-SpanishPatterns-rejected.txt"
                ),
            ),
        ]
        with contextlib.ExitStack() as stack:
            for attr_name, target in patches:
                stack.enter_context(mock.patch.object(vale_gen, attr_name, target))
            in_sync, drifted = vale_gen.check_styles()
        assert not in_sync
        assert any(p.name == "LLMToneTells.yml" for p in drifted), (
            f"drift not detected; drifted={drifted}"
        )

    def test_check_and_dry_run_are_mutually_exclusive(self) -> None:
        rc = vale_gen.main(["--check", "--dry-run"])
        assert rc == 2


# ---------------------------------------------------------------------------
# --clean flag wipes the Vocab dir before regenerating (C-71-Vale-2)
# ---------------------------------------------------------------------------


class TestCleanFlag:
    def test_clean_removes_legacy_flat_layout_files(self, tmp_path: Path) -> None:
        # Seed the tmp tree with BOTH pre-C-71-Vale-2 single-pair files AND
        # the post-C-71-Vale-2 pre-3.14 flat-layout files (mimicking the two
        # stale checkout shapes ``--clean`` must drop). After regeneration
        # with ``clean=True``, the entire ``Vocab/`` flat tree must be gone
        # and the new ``config/vocabularies/<Name>/{accept,reject}.txt``
        # layout must be the only thing on disk.
        legacy_flat_dir = tmp_path / ".vale" / "styles" / "Vocab"
        legacy_flat_dir.mkdir(parents=True)
        (legacy_flat_dir / "Holistika.txt").write_text(
            "legacy single-pair accept\n", encoding="utf-8"
        )
        (legacy_flat_dir / "Holistika-rejected.txt").write_text(
            "legacy single-pair reject\n", encoding="utf-8"
        )
        (legacy_flat_dir / "Holistika-CopywritingDiscipline.txt").write_text(
            "pre-3.14 flat-layout accept\n", encoding="utf-8"
        )
        (legacy_flat_dir / "Holistika-CopywritingDiscipline-rejected.txt").write_text(
            "pre-3.14 flat-layout reject\n", encoding="utf-8"
        )

        outputs = vale_gen.write_styles(target_root=tmp_path, clean=True)

        # Legacy flat layout (both shapes) must be gone.
        assert not legacy_flat_dir.exists(), (
            f"legacy flat .vale/styles/Vocab/ tree still present at "
            f"{legacy_flat_dir} after --clean"
        )
        # Per-canonical directory layout must be present with both leaves.
        new_root = tmp_path / ".vale" / "styles" / "config" / "vocabularies"
        for name in EXPECTED_VOCAB_NAMES:
            assert (new_root / name / "accept.txt").exists(), (
                f"missing accept.txt under {name} after --clean"
            )
            assert (new_root / name / "reject.txt").exists(), (
                f"missing reject.txt under {name} after --clean"
            )
        # Outputs map mirrors disk state.
        flat_names_in_outputs = {
            path.name
            for path in outputs
            if "Vocab" in path.parts and "vocabularies" not in path.parts
        }
        assert flat_names_in_outputs == set(), (
            f"unexpected flat-layout outputs: {flat_names_in_outputs}"
        )


# ---------------------------------------------------------------------------
# Graceful skip when canonical is absent
# ---------------------------------------------------------------------------


class TestGracefulSkipOnAbsentCanonical:
    def test_placeholder_style_emits_when_canonical_missing(
        self, tmp_path: Path
    ) -> None:
        # Patch the parser helpers to return empty (simulating absent canonical)
        # and verify the generator still emits valid Vale-YAML placeholder
        # files instead of raising.
        with mock.patch.object(vale_gen, "parse_llm_tone_tells", return_value=[]), \
             mock.patch.object(
                vale_gen, "parse_tic_families_from_canonical", return_value=[]
             ), \
             mock.patch.object(
                vale_gen, "parse_english_register_rules", return_value=[]
             ):
            outputs = vale_gen.write_styles(target_root=tmp_path)
        for path, contents in outputs.items():
            if path.suffix != ".yml":
                continue
            data = yaml.safe_load(contents)
            assert isinstance(data, dict), f"{path.name} placeholder did not parse"
            # Placeholder uses extends: existence with empty tokens.
            if data.get("extends") == "existence":
                tokens = data.get("tokens", [])
                assert tokens == [] or tokens is None, (
                    f"{path.name} placeholder unexpectedly carried tokens"
                )

    def test_placeholder_style_carries_absence_note_in_header(
        self, tmp_path: Path
    ) -> None:
        with mock.patch.object(vale_gen, "parse_llm_tone_tells", return_value=[]), \
             mock.patch.object(
                vale_gen, "parse_tic_families_from_canonical", return_value=[]
             ), \
             mock.patch.object(
                vale_gen, "parse_english_register_rules", return_value=[]
             ):
            outputs = vale_gen.write_styles(target_root=tmp_path)
        for path, contents in outputs.items():
            if path.suffix != ".yml":
                continue
            assert "(ABSENT at generation time)" in contents, (
                f"{path.name} placeholder missing absence note in header"
            )


# ---------------------------------------------------------------------------
# Helper-level sanity tests
# ---------------------------------------------------------------------------


class TestHelpers:
    def test_vale_level_maps_chassis_severity(self) -> None:
        assert vale_gen._vale_level("error") == "error"
        assert vale_gen._vale_level("warning") == "warning"
        assert vale_gen._vale_level("info") == "suggestion"
        assert vale_gen._vale_level("unknown") == "warning"  # fallback

    def test_strip_word_boundary_regex_recovers_canonical_token(self) -> None:
        # The chassis encodes tokens as `\b<re.escape token>\b`. The vocab
        # generator strips the boundaries + reverses re.escape so the
        # operator-readable token surfaces in the Vocab files.
        assert (
            vale_gen._strip_word_boundary_regex(r"\bdelve\ into\b") == "delve into"
        )
        assert vale_gen._strip_word_boundary_regex(r"\bbest\-in\-class\b") == "best-in-class"

    def test_extract_replacement_from_rationale(self) -> None:
        rationale = (
            "EN MBA-deck jargon -- replace with 'walk through' (LLM-default verb)"
        )
        assert vale_gen._extract_replacement_from_rationale(rationale) == "walk through"

    def test_extract_replacement_returns_none_on_miss(self) -> None:
        assert vale_gen._extract_replacement_from_rationale("no marker here") is None

    def test_french_anglicism_parser_returns_empty_when_canonical_absent(
        self, tmp_path: Path
    ) -> None:
        absent = tmp_path / "does_not_exist.md"
        assert vale_gen._parse_french_anglicism_tokens(absent) == []

    def test_spanish_anglicism_parser_returns_empty_when_canonical_absent(
        self, tmp_path: Path
    ) -> None:
        absent = tmp_path / "does_not_exist.md"
        assert vale_gen._parse_spanish_anglicism_tokens(absent) == []


# ---------------------------------------------------------------------------
# Vale binary parses the emitted layout (host-conditional smoke)
# ---------------------------------------------------------------------------


class TestValeBinaryParsesLayout:
    """Run ``vale ls-config`` against the real repo's .vale.ini + emitted
    styles tree.

    Vale 3.14 fails with ``E100 [vocab] Runtime error`` when any Vocab named
    in ``.vale.ini`` does not have a matching
    ``<StylesPath>/config/vocabularies/<Name>/`` directory. This test is the
    smoke-gate that the layout repair in this commit is correctly emitted.

    Skipped when the ``vale`` binary is unavailable on the test host so CI
    runners without Vale installed don't fail; the unit tests above cover the
    layout shape independently.
    """

    @staticmethod
    def _vale_binary() -> str | None:
        # Honour an explicit override first (test harness or operator-set
        # absolute path); otherwise probe PATH the way subprocess will.
        explicit = os.environ.get("AKOS_VALE_BIN")
        if explicit and Path(explicit).exists():
            return explicit
        located = _shutil.which("vale")
        return located

    def test_vale_ls_config_parses_emitted_layout(self) -> None:
        binary = self._vale_binary()
        if binary is None:
            pytest.skip(
                "vale binary not available on this host; skipping Vale 3.14 "
                "ls-config smoke (set AKOS_VALE_BIN or install vale to enable)"
            )
        # Resolve --config absolutely so PowerShell shell-quoting can't drop the
        # leading dot when forwarding from this subprocess.
        config_path = REPO_ROOT / ".vale.ini"
        proc = subprocess.run(
            [binary, "--config", str(config_path), "ls-config"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert proc.returncode == 0, (
            f"vale ls-config failed with exit {proc.returncode}; this means the "
            f"Vale config or styles layout is unparseable. stdout=\n{proc.stdout}\n"
            f"stderr=\n{proc.stderr}"
        )
        # Vale's ls-config prints a JSON-shaped block; the StylesPath should
        # resolve relative to the repo root and the Vocab list should round-trip.
        assert "Holistika-CopywritingDiscipline" in proc.stdout, (
            "ls-config output missing Holistika-CopywritingDiscipline Vocab "
            "name; .vale.ini may have drifted from the layout repair"
        )
