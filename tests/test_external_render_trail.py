"""Tests for ``scripts/validate_external_render_trail.py`` (D-IH-86-P / Wave E + Tier 1).

Mirrors the I85 P2 validator-test discipline (registry / audience / heuristics)
and adds Tier-1 sha256-freshness coverage (advisory + strict modes).

Group: ``-m brand`` (consistent with sibling external-discipline drift tests).
"""
from __future__ import annotations

import hashlib
import json
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_external_render_trail as drift  # noqa: E402


# ---- Section 1: structural / canonical ------------------------------------


@pytest.mark.brand
def test_canonical_scan_passes_default() -> None:
    """Repo scan PASS at this commit — all 6 in-scope external surfaces have a render trail."""
    assert drift.validate() == 0


@pytest.mark.brand
def test_canonical_scan_passes_strict() -> None:
    """Strict mode also PASS at this commit — render-pending tracker is empty."""
    assert drift.validate(strict=True) == 0


@pytest.mark.brand
def test_canonical_scan_passes_strict_freshness() -> None:
    """Strict-freshness PASS at this commit — all manifests reflect current sources."""
    drift._MANIFEST_INDEX_CACHE = None  # bust cache for deterministic re-read
    assert drift.validate(strict=True, strict_freshness=True) == 0


# ---- Section 2: audience extraction ---------------------------------------


@pytest.mark.brand
def test_extract_audience_single_string() -> None:
    text = "---\naudience: J-IN\nstatus: active\n---\n\n# Body\n"
    assert drift._extract_audience(text) == ["J-IN"]


@pytest.mark.brand
def test_extract_audience_list_inline() -> None:
    text = "---\naudience: [J-IN, J-CU, J-PT]\n---\n\n# Body\n"
    assert drift._extract_audience(text) == ["J-IN", "J-CU", "J-PT"]


@pytest.mark.brand
def test_extract_audience_no_field_returns_none() -> None:
    text = "---\nstatus: active\n---\n\n# Body\n"
    assert drift._extract_audience(text) is None


@pytest.mark.brand
def test_extract_audience_no_frontmatter_returns_none() -> None:
    text = "# Body only\n\nNo frontmatter.\n"
    assert drift._extract_audience(text) is None


# ---- Section 3: template exemption ----------------------------------------


@pytest.mark.brand
def test_template_artifact_kind_is_exempt() -> None:
    """Frontmatter ``artifact_kind: deck_template`` flips ``_is_template_surface``."""
    text = "---\naudience: J-IN\nartifact_kind: deck_template\n---\n# Skel\n"
    assert drift._is_template_surface(text) is True


@pytest.mark.brand
def test_artifact_kind_suffix_template_is_exempt() -> None:
    """Any ``*_template`` or ``*-template`` artifact_kind is exempt."""
    text = "---\nartifact_kind: dossier_template\n---\n# Skel\n"
    assert drift._is_template_surface(text) is True
    text2 = "---\nartifact_kind: invoice-template\n---\n# Skel\n"
    assert drift._is_template_surface(text2) is True


@pytest.mark.brand
def test_artifact_kind_dossier_es_is_not_exempt() -> None:
    """Real dossiers (``dossier_es``) are NOT exempt — must have render trail."""
    text = "---\naudience: J-ENISA\nartifact_kind: dossier_es\n---\n# Body\n"
    assert drift._is_template_surface(text) is False


# ---- Section 4: heuristic helpers (pure, isolated) ------------------------


@pytest.mark.brand
def test_has_registered_url_with_holistika_passes() -> None:
    text = "Visit https://holistikaresearch.com/about for more."
    assert drift._has_registered_url(text) is True


@pytest.mark.brand
def test_has_registered_url_without_registered_domain_fails() -> None:
    text = "Visit https://example.com/ — not a registered domain."
    assert drift._has_registered_url(text) is False


@pytest.mark.brand
def test_has_uuid_detects_canonical_uuid() -> None:
    text = "record_id: 550e8400-e29b-41d4-a716-446655440000"
    assert drift._has_uuid(text) is True


@pytest.mark.brand
def test_has_uuid_rejects_non_uuid_string() -> None:
    text = "record_id: ABC-123-not-a-uuid"
    assert drift._has_uuid(text) is False


# ---- Section 5: manifest reverse-lookup (PDF heuristic) -------------------


@pytest.mark.brand
def test_manifest_reverse_lookup_surfaces_cover_email_sources() -> None:
    """Cover-email HTML manifests reverse-lookup their .md sources via _manifest_sources()."""
    drift._MANIFEST_INDEX_CACHE = None
    sources = drift._manifest_sources()
    assert any(s.endswith("/cover_email_es.md") for s in sources), \
        f"cover_email_es.md not surfaced; got {sorted(sources)}"
    assert any(s.endswith("/cover_email_company_dossier_es.md") for s in sources), \
        f"cover_email_company_dossier_es.md not surfaced; got {sorted(sources)}"
    assert any(s.endswith("/cover_email_legal_constitutor_es.md") for s in sources), \
        f"cover_email_legal_constitutor_es.md not surfaced; got {sorted(sources)}"


@pytest.mark.brand
def test_load_manifest_index_returns_dicts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """``_load_manifest_index`` parses JSON and includes ``_manifest_path`` for each entry."""
    fake_exports = tmp_path / "exports"
    fake_exports.mkdir()
    fake_manifest = fake_exports / "fake.manifest.json"
    fake_manifest.write_text(
        json.dumps({
            "source_path": "docs/fake/source.md",
            "source_sha256": "deadbeef" * 8,
            "render_sha256": "cafebabe" * 8,
        }),
        encoding="utf-8",
    )
    monkeypatch.setattr(drift, "EXPORTS_DIR", fake_exports)
    drift._MANIFEST_INDEX_CACHE = None
    index = drift._manifest_index()
    assert "docs/fake/source.md" in index
    entries = index["docs/fake/source.md"]
    assert len(entries) == 1
    assert entries[0]["_manifest_path"] == str(fake_manifest)
    assert entries[0]["source_sha256"] == "deadbeef" * 8


# ---- Section 6: sha256-freshness sub-validator ----------------------------


@pytest.mark.brand
def test_freshness_no_manifest_returns_fresh(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A source with no manifest entries is treated as fresh (undefined, not stale)."""
    src = tmp_path / "no-manifest.md"
    src.write_text("# Hello\n", encoding="utf-8")
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    drift._MANIFEST_INDEX_CACHE = {}  # empty index
    is_fresh, stale = drift._check_freshness(src)
    assert is_fresh is True
    assert stale == []


@pytest.mark.brand
def test_freshness_matching_sha_returns_fresh(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A source whose sha256 matches the manifest's recorded value is fresh."""
    src = tmp_path / "fresh.md"
    src.write_bytes(b"# Hello\n")
    src_sha = hashlib.sha256(b"# Hello\n").hexdigest()
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    drift._MANIFEST_INDEX_CACHE = {
        "fresh.md": [{
            "source_path": "fresh.md",
            "source_sha256": src_sha,
            "_manifest_path": str(tmp_path / "fake.manifest.json"),
        }],
    }
    is_fresh, stale = drift._check_freshness(src)
    assert is_fresh is True
    assert stale == []


@pytest.mark.brand
def test_freshness_mismatched_sha_returns_stale(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A source whose sha256 differs from the manifest's recorded value is stale."""
    src = tmp_path / "stale.md"
    src.write_bytes(b"# Updated content\n")
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    drift._MANIFEST_INDEX_CACHE = {
        "stale.md": [{
            "source_path": "stale.md",
            "source_sha256": "0" * 64,
            "_manifest_path": str(tmp_path / "fake.manifest.json"),
        }],
    }
    is_fresh, stale = drift._check_freshness(src)
    assert is_fresh is False
    assert len(stale) == 1
    manifest_path, recorded, current = stale[0]
    assert recorded == "0" * 64
    assert current == hashlib.sha256(b"# Updated content\n").hexdigest()


@pytest.mark.brand
def test_freshness_manifest_without_source_sha_skipped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Manifests lacking ``source_sha256`` are skipped (advisory: not stale, just unknown)."""
    src = tmp_path / "nosha.md"
    src.write_bytes(b"# Body\n")
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    drift._MANIFEST_INDEX_CACHE = {
        "nosha.md": [{
            "source_path": "nosha.md",
            "_manifest_path": str(tmp_path / "fake.manifest.json"),
        }],
    }
    is_fresh, stale = drift._check_freshness(src)
    assert is_fresh is True
    assert stale == []


# ---- Section 7: end-to-end strict-mode behaviour --------------------------


@pytest.mark.brand
def test_unknown_audience_skipped_no_external_tag(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Surface tagged J-OP-only is not in scope (no render trail required)."""
    fake_file = tmp_path / "operator-only.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-OP]
            ---

            # Operator only
            """
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    drift._MANIFEST_INDEX_CACHE = {}
    assert drift.validate(strict=True) == 0


@pytest.mark.brand
def test_external_audience_without_trail_strict_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """External-tagged surface with no render trail FAILs in strict mode."""
    fake_file = tmp_path / "external-no-trail.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-IN]
            artifact_kind: dossier_es
            ---

            # Investor body
            """
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(drift, "EXPORTS_DIR", tmp_path / "exports")
    drift._MANIFEST_INDEX_CACHE = {}
    assert drift.validate(strict=True) == 1


@pytest.mark.brand
def test_external_audience_template_exempt_strict_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """External-tagged template skeleton is exempt — strict mode PASS."""
    fake_file = tmp_path / "deck-template.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-IN]
            artifact_kind: deck_template
            ---

            # Skeleton
            """
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    drift._MANIFEST_INDEX_CACHE = {}
    assert drift.validate(strict=True) == 0


@pytest.mark.brand
def test_external_audience_in_pending_tracker_strict_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """External-tagged surface listed in the pending tracker is OK in strict mode."""
    fake_file = tmp_path / "tracked.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-IN]
            artifact_kind: dossier_es
            ---

            # Investor body
            """
        ),
        encoding="utf-8",
    )
    fake_tracker = tmp_path / "tracker.md"
    fake_tracker.write_text(
        "# Tracker\n\n- tracked.md — dossier render-pending\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(drift, "PENDING_TRACKER_PATH", fake_tracker)
    monkeypatch.setattr(drift, "EXPORTS_DIR", tmp_path / "exports")
    drift._MANIFEST_INDEX_CACHE = {}
    assert drift.validate(strict=True) == 0


# ---- Section 8: channel-touchpoint FK-resolution (Wave F / RULE 7 / D-IH-86-P) ----


@pytest.mark.brand
def test_extract_channel_single_string() -> None:
    text = "---\naudience: J-IN\nchannel: CHAN-EMAIL-OUTBOUND\n---\n\n# Body\n"
    assert drift._extract_channel(text) == ["CHAN-EMAIL-OUTBOUND"]


@pytest.mark.brand
def test_extract_channel_list_inline() -> None:
    text = "---\naudience: J-IN\nchannel: [CHAN-EMAIL-OUTBOUND, CHAN-LINKEDIN-DM]\n---\n\n# Body\n"
    assert drift._extract_channel(text) == ["CHAN-EMAIL-OUTBOUND", "CHAN-LINKEDIN-DM"]


@pytest.mark.brand
def test_extract_channel_no_field_returns_none() -> None:
    text = "---\naudience: J-IN\n---\n\n# Body\n"
    assert drift._extract_channel(text) is None


@pytest.mark.brand
def test_extract_channel_no_frontmatter_returns_none() -> None:
    text = "# No frontmatter\n"
    assert drift._extract_channel(text) is None


@pytest.mark.brand
def test_channel_registry_loads_canonical_codes() -> None:
    """The canonical CHANNEL_TOUCHPOINT_REGISTRY.csv is FK-resolvable."""
    drift._CHANNEL_CODES_CACHE = None
    codes = drift._channel_codes()
    assert "CHAN-LINKEDIN-DM" in codes
    assert "CHAN-EMAIL-INBOUND" in codes
    assert "CHAN-WEB-FORM" in codes


@pytest.mark.brand
def test_known_channel_advisory_no_op(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Surface declaring a known CHAN- code passes (FK-resolves)."""
    drift._CHANNEL_CODES_CACHE = None
    fake_file = tmp_path / "cover_email_es.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-IN]
            channel: CHAN-EMAIL-OUTBOUND
            ---

            # Investor cover body
            """
        ),
        encoding="utf-8",
    )
    paired_html = tmp_path / "cover_email_es.html"
    paired_html.write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(drift, "EXPORTS_DIR", tmp_path / "exports")
    drift._MANIFEST_INDEX_CACHE = {}
    assert drift.validate(strict=True) == 0


@pytest.mark.brand
def test_unknown_channel_logs_info_does_not_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture,
) -> None:
    """Surface declaring an UN-registered CHAN- code surfaces INFO; never FAILs."""
    drift._CHANNEL_CODES_CACHE = None
    fake_file = tmp_path / "cover_email_es.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-IN]
            channel: CHAN-UNKNOWN-FUTURE-PATH
            ---

            # Investor cover body
            """
        ),
        encoding="utf-8",
    )
    paired_html = tmp_path / "cover_email_es.html"
    paired_html.write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(drift, "EXPORTS_DIR", tmp_path / "exports")
    drift._MANIFEST_INDEX_CACHE = {}
    import logging as _logging
    with caplog.at_level(_logging.INFO):
        result = drift.validate(strict=True)
    assert result == 0
    info_messages = [r.getMessage() for r in caplog.records if r.levelno == _logging.INFO]
    assert any("channel FK-unresolved" in m and "CHAN-UNKNOWN-FUTURE-PATH" in m for m in info_messages)


@pytest.mark.brand
def test_absent_channel_no_finding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Surface WITHOUT channel: frontmatter is unaffected (Wave F backfill posture)."""
    drift._CHANNEL_CODES_CACHE = None
    fake_file = tmp_path / "cover_email_es.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-IN]
            ---

            # Investor cover body
            """
        ),
        encoding="utf-8",
    )
    paired_html = tmp_path / "cover_email_es.html"
    paired_html.write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(drift, "EXPORTS_DIR", tmp_path / "exports")
    drift._MANIFEST_INDEX_CACHE = {}
    assert drift.validate(strict=True) == 0
