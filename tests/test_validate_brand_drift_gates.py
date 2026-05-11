"""Tests for the four I66 P2 brand drift gates.

Covered scripts:

- ``scripts/validate_brand_canon_drift.py``
- ``scripts/validate_brand_jargon.py``
- ``scripts/validate_brand_voice_register.py``
- ``scripts/validate_brand_baseline_reality_drift.py``

These tests use small in-tmpdir fixtures + import the validator modules
directly so we exercise the parsers + scanners without requiring real sibling
consumer repos.
"""

from __future__ import annotations

import importlib
import json
import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scripts.validate_brand_canon_drift as canon_drift  # noqa: E402
import scripts.validate_brand_jargon as brand_jargon  # noqa: E402
import scripts.validate_brand_voice_register as voice_register  # noqa: E402
import scripts.validate_brand_baseline_reality_drift as baseline_reality  # noqa: E402
import scripts.validate_brand_vision_drift as vision_drift  # noqa: E402
import scripts.validate_dossier_companion_drift as companion_drift  # noqa: E402


# ---------------------------------------------------------------------------
# validate_brand_canon_drift.py
# ---------------------------------------------------------------------------


class TestBrandCanonDrift:
    def test_required_canonicals_all_present_with_active_status(self) -> None:
        """All P0+P1 canonicals exist with status: active."""
        errors = canon_drift._check_required_canonicals_present()
        assert errors == [], "All required canonicals should be active"

    def test_vision_markers_present_and_ordered(self) -> None:
        errors = canon_drift._check_vision_markers()
        assert errors == [], f"Vision marker check failed: {errors}"

    def test_baseline_reality_external_register_clean(self) -> None:
        errors = canon_drift._check_baseline_reality_external_register_clean()
        assert errors == [], f"External register contains internal tokens: {errors}"

    def test_logo_system_cross_refs_present(self) -> None:
        errors = canon_drift._check_logo_system_cross_refs()
        assert errors == [], f"Logo system cross-refs missing: {errors}"

    def test_hierarchy_supersedes_v1(self) -> None:
        errors = canon_drift._check_hierarchy_supersedes()
        assert errors == [], (
            "BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md must declare "
            "'supersedes:' frontmatter (the I66 P1 v2.0 rewrite)"
        )

    def test_main_returns_zero_against_clean_canon(self) -> None:
        rc = canon_drift.main(["--skip-upstream"])
        assert rc == 0


# ---------------------------------------------------------------------------
# validate_brand_jargon.py
# ---------------------------------------------------------------------------


class TestBrandJargon:
    def test_tokens_extracted_from_canonical(self) -> None:
        tokens = brand_jargon._extract_tokens_from_jargon_audit(
            brand_jargon.JARGON_AUDIT_PATH
        )
        token_set = {t.token for t in tokens}
        assert "AKOS" in token_set, "AKOS must be in §4.1 forbidden list"
        assert "HLK" in token_set, "HLK must be in §4.1 forbidden list"
        assert "RBAC" in token_set, "RBAC must be in §4.2 stack jargon list"
        assert "Holistika" not in token_set, (
            "Holistika is the canonical brand and must never be in the "
            "forbidden list (CANONICAL_ALLOWLIST guard)"
        )
        assert "BRAND_BASELINE_REALITY_MATRIX.md" not in token_set

    def test_hlk_paired_form_passes(self) -> None:
        tokens = [t for t in brand_jargon._extract_tokens_from_jargon_audit(
            brand_jargon.JARGON_AUDIT_PATH
        ) if t.token == "HLK"]
        assert len(tokens) == 1
        hlk = tokens[0]
        assert hlk.pattern.search("HLK is bad") is not None
        assert hlk.pattern.search("HLK Tech Lab is the canonical sub-mark") is None

    def test_abbreviation_locale_only_only_fires_in_messages_json(self, tmp_path: Path) -> None:
        msg_dir = tmp_path / "messages"
        msg_dir.mkdir()
        (msg_dir / "en.json").write_text(json.dumps({"key": "Visit MA today"}), encoding="utf-8")

        non_locale = tmp_path / "app" / "page.tsx"
        non_locale.parent.mkdir(parents=True, exist_ok=True)
        non_locale.write_text("export const Page = () => <div>MA team works here</div>", encoding="utf-8")

        tokens = brand_jargon._extract_tokens_from_abbreviations(brand_jargon.ABBREVIATIONS_PATH)
        assert any(t.token == "MA" for t in tokens)

        msg_hits = brand_jargon._scan_file(msg_dir / "en.json", tokens)
        page_hits = brand_jargon._scan_file(non_locale, tokens)

        assert any(h.token.token == "MA" for h in msg_hits)
        assert all(h.token.category != "abbreviation_locale_only" for h in page_hits)

    def test_import_lines_skipped_in_typescript(self, tmp_path: Path) -> None:
        f = tmp_path / "component.tsx"
        f.write_text(
            'import { useTranslations } from "next-intl";\n'
            'export const X = () => <div>plain text</div>;\n',
            encoding="utf-8",
        )
        tokens = [
            brand_jargon.ForbiddenToken(
                token="next-intl",
                pattern=__import__("re").compile(r"\bnext-intl\b", __import__("re").IGNORECASE),
                category="stack_jargon",
                canonical_source="test",
            )
        ]
        hits = brand_jargon._scan_file(f, tokens)
        assert hits == [], "Import lines must be skipped"

    def test_prose_tokens_still_caught(self, tmp_path: Path) -> None:
        f = tmp_path / "page.tsx"
        f.write_text(
            'export const Page = () => <p>We use the AKOS framework everywhere.</p>',
            encoding="utf-8",
        )
        tokens = [
            brand_jargon.ForbiddenToken(
                token="AKOS",
                pattern=__import__("re").compile(r"\bAKOS\b"),
                category="codename",
                canonical_source="test",
            )
        ]
        hits = brand_jargon._scan_file(f, tokens)
        assert len(hits) == 1
        assert "AKOS" in hits[0].snippet

    def test_dashboard_legacy_path_excluded(self, tmp_path: Path) -> None:
        repo_name = "boilerplate"
        legacy = tmp_path / "app" / "dashboard" / "ui" / "x.tsx"
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_text("legacy code", encoding="utf-8")

        ok = tmp_path / "app" / "page.tsx"
        ok.parent.mkdir(parents=True, exist_ok=True)
        ok.write_text("public page", encoding="utf-8")

        results = list(brand_jargon._walk_subpath(tmp_path, "app", repo_name))
        rel_strs = {str(p.relative_to(tmp_path)) for p in results}
        assert "app\\page.tsx" in rel_strs or "app/page.tsx" in rel_strs
        assert all("dashboard" not in s for s in rel_strs)

    def test_strict_empty_fails_when_no_consumer_repos(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Skip-default-roots: assert rc == 1 when no consumer repos resolve and --strict-empty is set."""
        monkeypatch.setattr(brand_jargon, "DEFAULT_CONSUMER_ROOTS", ())
        rc = brand_jargon.main(["--strict-empty", "--consumer-root", "/nonexistent/path/here"])
        assert rc == 1

    def test_graceful_skip_when_no_consumer_repos(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Skip-default-roots: graceful skip is the no-strict-empty case."""
        monkeypatch.setattr(brand_jargon, "DEFAULT_CONSUMER_ROOTS", ())
        rc = brand_jargon.main(["--consumer-root", str(tmp_path / "nonexistent")])
        assert rc == 0


# ---------------------------------------------------------------------------
# validate_brand_voice_register.py
# ---------------------------------------------------------------------------


class TestBrandVoiceRegister:
    def test_french_anglicisms_extracted(self) -> None:
        rules = voice_register._extract_french_anglicisms(voice_register.FRENCH_PATTERNS_PATH)
        tokens = {r.token for r in rules}
        assert "de-risquer" in tokens or "process" in tokens, (
            "FR anglicism table must yield at least the canonical de-risquer / process entries"
        )
        assert all(r.locale == "fr" for r in rules)

    def test_spanish_register_rules_present(self) -> None:
        rules = voice_register._spanish_register_rules(voice_register.SPANISH_PATTERNS_PATH)
        tokens = {r.token for r in rules}
        assert "humildemente" in tokens
        assert "pricing" in tokens
        assert all(r.locale == "es" for r in rules)

    def test_fr_message_file_with_anglicism_flagged(self, tmp_path: Path) -> None:
        msg = tmp_path / "messages" / "fr.json"
        msg.parent.mkdir(parents=True, exist_ok=True)
        msg.write_text(
            json.dumps({"hero": {"cta": "Nous allons de-risquer votre projet"}}),
            encoding="utf-8",
        )
        rules = voice_register._load_rules()
        hits = voice_register._scan_message_file(msg, rules)
        assert any(h.locale == "fr" and "de-risquer" in h.rule.token for h in hits)

    def test_fr_clean_message_file_no_hits(self, tmp_path: Path) -> None:
        msg = tmp_path / "messages" / "fr.json"
        msg.parent.mkdir(parents=True, exist_ok=True)
        msg.write_text(
            json.dumps({"hero": {"cta": "Nous reduisons le risque de votre projet"}}),
            encoding="utf-8",
        )
        rules = voice_register._load_rules()
        hits = voice_register._scan_message_file(msg, rules)
        assert hits == []

    def test_es_performative_humility_flagged(self, tmp_path: Path) -> None:
        msg = tmp_path / "messages" / "es.json"
        msg.parent.mkdir(parents=True, exist_ok=True)
        msg.write_text(
            json.dumps({"footer": "humildemente le ofrecemos nuestros servicios"}),
            encoding="utf-8",
        )
        rules = voice_register._load_rules()
        hits = voice_register._scan_message_file(msg, rules)
        assert any(h.rule.token == "humildemente" for h in hits)

    def test_en_locale_no_rules(self, tmp_path: Path) -> None:
        msg = tmp_path / "messages" / "en.json"
        msg.parent.mkdir(parents=True, exist_ok=True)
        msg.write_text(json.dumps({"key": "humildemente — performative humility"}), encoding="utf-8")
        rules = voice_register._load_rules()
        hits = voice_register._scan_message_file(msg, rules)
        assert hits == [], "EN locale has no register rules in I66 P1; expected 0 hits"

    def test_main_graceful_skip_on_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Skip-default-roots: assert rc == 0 when no consumer repos resolve."""
        monkeypatch.setattr(voice_register, "DEFAULT_CONSUMER_ROOTS", ())
        rc = voice_register.main(["--consumer-root", "/nonexistent/path"])
        assert rc == 0


# ---------------------------------------------------------------------------
# validate_brand_baseline_reality_drift.py
# ---------------------------------------------------------------------------


class TestBaselineRealityDrift:
    def test_internal_tokens_extracted_or_fallback(self) -> None:
        tokens = baseline_reality._extract_internal_tokens_from_matrix(
            baseline_reality.MATRIX_PATH
        )
        token_set = {t.token.lower() for t in tokens}
        assert "counterparty" in token_set
        assert "elicitation" in token_set
        assert "intelligence report" in token_set

    def test_companion_files_are_exempt(self, tmp_path: Path) -> None:
        f = tmp_path / "investor.objections.md"
        f.write_text("counterparty assessment for the investor audience", encoding="utf-8")
        tokens = baseline_reality._build_token_patterns(["counterparty"])
        hits = baseline_reality._scan_text(f, tokens)
        assert hits == [], "companion *.objections.md files are exempt"

    def test_counterparty_brief_is_exempt(self, tmp_path: Path) -> None:
        f = tmp_path / "deck.counterparty-brief.md"
        f.write_text("elicitation framework for this counterparty", encoding="utf-8")
        tokens = baseline_reality._build_token_patterns(["elicitation", "counterparty"])
        hits = baseline_reality._scan_text(f, tokens)
        assert hits == []

    def test_dossier_file_flags_internal_tokens(self, tmp_path: Path) -> None:
        f = tmp_path / "dossier_es.md"
        f.write_text(
            "Holistika es una empresa de investigación. We perform elicitation and intelligence collection.",
            encoding="utf-8",
        )
        tokens = baseline_reality._build_token_patterns(["elicitation", "intelligence collection"])
        hits = baseline_reality._scan_text(f, tokens)
        assert len(hits) == 2
        assert {h.token.token for h in hits} == {"elicitation", "intelligence collection"}

    def test_skip_consumer_mode_only_scans_advops(self) -> None:
        rc = baseline_reality.main(["--skip-consumer"])
        assert rc == 0

    def test_default_run_passes_against_clean_repo(self) -> None:
        rc = baseline_reality.main([])
        assert rc == 0


# ---------------------------------------------------------------------------
# validate_brand_vision_drift.py
# ---------------------------------------------------------------------------


class TestBrandVisionDrift:
    def test_extract_public_region_requires_ordered_markers(self) -> None:
        text = "x\n<!-- public-vision:start -->\nPublic\n<!-- public-vision:end -->\ny"
        assert vision_drift.extract_public_region(text) == "Public"

    def test_extract_public_region_fails_without_markers(self) -> None:
        with pytest.raises(ValueError):
            vision_drift.extract_public_region("No markers")

    def test_real_vision_gate_passes(self) -> None:
        errors = vision_drift.check_vision_drift()
        assert errors == []


# ---------------------------------------------------------------------------
# validate_dossier_companion_drift.py
# ---------------------------------------------------------------------------


class TestDossierCompanionDrift:
    def _write_deck_set(self, root: Path, name: str = "sample") -> None:
        root.mkdir(parents=True, exist_ok=True)
        (root / f"{name}.deck.md").write_text(
            textwrap.dedent(
                """\
                ---
                status: active
                companions:
                  - sample.counterparty-brief.md
                ---

                # Public deck

                Clean public prose.
                """
            ),
            encoding="utf-8",
        )
        (root / f"{name}.objections.md").write_text(
            textwrap.dedent(
                """\
                ---
                access_level: 5
                classification: operator_private
                artifact_kind: deck_objection_companion
                ---

                # Objections
                """
            ),
            encoding="utf-8",
        )
        (root / f"{name}.counterparty-brief.md").write_text(
            textwrap.dedent(
                """\
                ---
                access_level: 5
                classification: operator_private
                artifact_kind: deck_counterparty_brief
                ---

                # Brief
                """
            ),
            encoding="utf-8",
        )

    def test_complete_deck_set_passes(self, tmp_path: Path) -> None:
        self._write_deck_set(tmp_path)
        assert companion_drift.check_dossier_companions(tmp_path) == []

    def test_public_deck_body_rejects_internal_token(self, tmp_path: Path) -> None:
        self._write_deck_set(tmp_path)
        deck = tmp_path / "sample.deck.md"
        deck.write_text(
            deck.read_text(encoding="utf-8") + "\nCounterparty wording leaks.\n",
            encoding="utf-8",
        )
        errors = companion_drift.check_dossier_companions(tmp_path)
        assert any(e.rule == "internal_token_in_public_deck" for e in errors)

    def test_missing_companion_fails(self, tmp_path: Path) -> None:
        self._write_deck_set(tmp_path)
        (tmp_path / "sample.objections.md").unlink()
        errors = companion_drift.check_dossier_companions(tmp_path)
        assert any(e.rule == "missing_companion" for e in errors)
