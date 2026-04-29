"""Tests for the Initiative 27 ENISA dossier renderer.

Covers:
- ``akos.hlk_pdf_render`` brand token table mirrors ``BRAND_VISUAL_PATTERNS.md``
  (smoke + drift safeguard).
- ``scripts/render_dossier.py`` resolves the canonical dossier markdown and
  parses cleanly under ``--smoke``.
- ``dossier_es.md`` cites every concrete adviser question by ``Q-…`` row id
  (citation-discipline guardrail).
- ``compose_adviser_message.py --body cover_email_es.md`` inlines the
  hand-authored body into the Layer 4 block instead of emitting the TODO
  marker.
"""
from __future__ import annotations

import importlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DOSSIER_MD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "advops"
    / "PRJ-HOL-FOUNDING-2026"
    / "enisa_evidence"
    / "dossier_es.md"
)
COVER_EMAIL_MD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "advops"
    / "PRJ-HOL-FOUNDING-2026"
    / "enisa_evidence"
    / "cover_email_es.md"
)
BRAND_VISUAL_PATTERNS_MD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Marketing"
    / "Brand"
    / "BRAND_VISUAL_PATTERNS.md"
)
ADVISER_QUESTIONS_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "ADVISER_OPEN_QUESTIONS.csv"
)
TOPIC_REGISTRY_CSV = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "compliance"
    / "dimensions"
    / "TOPIC_REGISTRY.csv"
)

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


# ---------- Brand token presence ---------------------------------------------


def test_brand_tokens_light_match_pattern_doc():
    """The Python-side BRAND_TOKENS_LIGHT must mirror BRAND_VISUAL_PATTERNS.md.

    Drift safeguard: when the brand pattern doc edits a token, this test fails
    until the constant table in ``akos/hlk_pdf_render.py`` is updated.

    The pattern-doc table cites HSL as ``168 55% 38%`` (the inner triple) inside
    backticks; the Python constants wrap them with ``hsl(...)``. Compare on the
    inner triple to stay format-tolerant.
    """
    mod = importlib.import_module("akos.hlk_pdf_render")
    md_text = BRAND_VISUAL_PATTERNS_MD.read_text(encoding="utf-8")

    for token_name, hsl_value in mod.BRAND_TOKENS_LIGHT.items():
        match = re.match(r"hsl\((.+)\)", hsl_value)
        assert match, f"{token_name} value {hsl_value!r} is not a hsl(...) string"
        inner = match.group(1)
        assert inner in md_text, (
            f"{token_name}=hsl({inner}) not present in BRAND_VISUAL_PATTERNS.md; "
            "either update the pattern doc or the constant table - they must agree."
        )


def test_brand_pdf_css_contains_all_dossier_classes():
    """Initiative 27 follow-up — visual upgrade replaced the old single-block
    cover (`.cover-rule` / `.cover-meta`) with a clean cover-strip + eyebrow
    + oversized title layout. The remaining mandatory primitives stay."""
    mod = importlib.import_module("akos.hlk_pdf_render")
    css = mod._brand_pdf_css(profile="dossier")
    for needed in (
        ".cover-hero",
        ".cover-monogram",
        ".cover-eyebrow",
        ".cover-strip",
        "callout-question",
        "callout-risk",
        "page-break-after: always",
        "Inter",
        "hsl(168 55% 38%)",
        "hsl(38 80% 50%)",
        "hsl(220 16% 7%)",
    ):
        assert needed in css, f"branded PDF CSS missing: {needed!r}"


def test_render_pdf_branded_signature():
    mod = importlib.import_module("akos.hlk_pdf_render")
    fn = mod.render_pdf_branded
    import inspect
    params = inspect.signature(fn).parameters
    for required in (
        "md_text",
        "out_path",
        "profile",
        "title",
        "subtitle",
        "program_id",
        "discipline",
        "issue_date",
        "status_label",
        "monogram_path",
    ):
        assert required in params, f"render_pdf_branded missing kwarg {required!r}"


# ---------- render_dossier.py smoke ------------------------------------------


def test_render_dossier_smoke_resolves_canonical_markdown():
    """``--smoke`` must report ``smoke OK`` for the default program/language."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "render_dossier.py"), "--smoke"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, f"render_dossier --smoke failed: {proc.stderr}\n{proc.stdout}"
    assert "smoke OK" in proc.stdout
    assert "PRJ-HOL-FOUNDING-2026" in proc.stdout
    assert "language=" not in proc.stdout or "es" in proc.stdout


def test_render_dossier_refuses_unknown_language():
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "render_dossier.py"),
            "--smoke",
            "--language",
            "en",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode != 0
    assert "REFUSED" in proc.stderr or "REFUSED" in proc.stdout


# ---------- Citation discipline -----------------------------------------------


def _question_ids() -> set[str]:
    if not ADVISER_QUESTIONS_CSV.is_file():
        return set()
    out: set[str] = set()
    for line in ADVISER_QUESTIONS_CSV.read_text(encoding="utf-8").splitlines()[1:]:
        if not line.strip():
            continue
        qid = line.split(",", 1)[0].strip()
        if qid:
            out.add(qid)
    return out


def test_dossier_cites_every_active_q_row():
    """Every ``Q-…`` row from ``ADVISER_OPEN_QUESTIONS.csv`` must appear in the
    dossier — citation discipline. If a row is added to the CSV, the dossier
    must learn about it before the next render.
    """
    md = DOSSIER_MD.read_text(encoding="utf-8")
    cited_in_md = set(re.findall(r"Q-[A-Z]{3}-\d{3}", md))
    canonical = _question_ids()
    if not canonical:
        pytest.skip("ADVISER_OPEN_QUESTIONS.csv unreadable")
    missing = canonical - cited_in_md
    assert not missing, (
        f"dossier_es.md must cite every Q-row in ADVISER_OPEN_QUESTIONS.csv; "
        f"missing: {sorted(missing)}"
    )


def test_dossier_cites_program_id_explicitly():
    md = DOSSIER_MD.read_text(encoding="utf-8")
    assert "PRJ-HOL-FOUNDING-2026" in md
    assert "program_id: PRJ-HOL-FOUNDING-2026" in md  # frontmatter SSOT


def test_dossier_includes_5_capability_cards():
    """The Apéndice C must still surface five concrete production deliveries
    after the Initiative 27 follow-up rewrite. Labels updated to match the
    new card titles (which moved from English/code-y names to Spanish prose
    per the jargon-free rewrite)."""
    md = DOSSIER_MD.read_text(encoding="utf-8")
    for card_marker in (
        "Sitio público y CRM",          # 01 — boilerplate marketing site
        "HLK ERP",                       # 02 — internal ERP (kept brand label)
        "KiRBe",                         # 03 — KM SaaS product
        "Holística × Websitz",           # 04 — Shopify partner app
        "Rushly",                        # 05 — partner SaaS scaffold
    ):
        assert card_marker in md, f"capability card missing: {card_marker!r}"


# ---------- Initiative 27 follow-up: jargon-free external rule ---------------

# Forbidden internal codenames that must NOT appear in the dossier body
# (per BRAND_JARGON_AUDIT.md §4). The Q-tracker appendix and provenance footer
# carry an audited subset (Q-row ids, INST-… ids, program_id, topic_id);
# everything else stays internal.
_FORBIDDEN_TOKENS_IN_BODY: tuple[str, ...] = (
    # 4.1 Internal codenames in prose
    "AKOS Strict",
    "ADVOPS",
    "TECHOPS",
    "FINOPS",
    "MKTOPS",
    "topic_external_adviser_handoff",
    "topic_kirbe_billing_plane_routing",
    "GOI-",
    "POI-",
    "ref_id",
    "process_list.csv",
    "GOI_POI_REGISTER",
    "ADVISER_OPEN_QUESTIONS.csv",
    "FOUNDER_FILED_INSTRUMENTS.csv",
    "TOPIC_REGISTRY.csv",
    "PROGRAM_REGISTRY.csv",
    "holistika_ops.",
    "kirbe.",
    "compliance.",
    "repo_slug",
    # 4.2 Stack jargon
    "RBAC",
    "RLS",
    "RRF",
    "pgvector",
    "Logfire",
    "Cohere",
    "BullMQ",
    "Cloudflare R2",
    "FastAPI",
    "Pydantic",
    "shadcn",
    "Polaris",
    "Liquid",
    "next-intl",
    "Mermaid",
    "WeasyPrint",
    "pandoc",
    "mmdc",
    # 4.3 Methodology shorthand
    "Topic-Fact-Source",
    "derived view",
)

# Tokens permitted because they're part of the audit-explicit allowlist
# (Q-row ids, INST ids, program_id, topic_id stay only in the appendix /
# metadata; we don't strip them, but they cluster in Apéndice A/B/E + fm).
_ALLOWED_IN_APPENDIX_OR_METADATA: tuple[str, ...] = (
    "PRJ-HOL-FOUNDING-2026",
    "topic_enisa_evidence",
    "topic_enisa_dossier_es",
    "topic_brand_voice",
    "Q-LEG-",
    "Q-FIS-",
    "Q-IPT-",
    "Q-BNK-",
    "Q-CRT-",
    "INST-LEG-",
)


def _dossier_body_only() -> str:
    """Return the prose body of dossier_es.md, stripped of frontmatter and
    the structured appendices (Q-tracker, instruments, provenance)."""
    text = DOSSIER_MD.read_text(encoding="utf-8")
    text = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)
    cut_at = text.find("# Apéndice A")
    if cut_at == -1:
        cut_at = text.find("Apéndice A")
    if cut_at == -1:
        return text
    return text[:cut_at]


def test_dossier_es_body_is_jargon_free():
    """Operator-flagged rule (BRAND_JARGON_AUDIT §4): external dossier prose
    must not carry internal codenames or stack jargon. The Q-tracker appendix
    and provenance footer carry an audited subset (Q-row ids, INST-…,
    program_id, topic_id); everything else is forbidden in the prose body."""
    body = _dossier_body_only()
    leaks: list[str] = []
    for forbidden in _FORBIDDEN_TOKENS_IN_BODY:
        if forbidden in body:
            leaks.append(forbidden)
    assert not leaks, (
        f"BRAND_JARGON_AUDIT.md §4 violation — these internal/stack tokens "
        f"appeared in the dossier body (excluding appendices A/B/E and "
        f"frontmatter): {leaks}. Rewrite to plain Spanish per the audit "
        f"translation gallery (§5)."
    )


def test_dossier_es_uses_visual_primitives():
    """The rewrite introduced stat callouts, lead paragraphs, pull-quotes,
    and capability cards. Verify the markdown source actually uses those
    primitives (otherwise the rendered PDF will look like the old plain
    Markdown dump)."""
    text = DOSSIER_MD.read_text(encoding="utf-8")
    for primitive in (
        '<p class="lead">',
        '<div class="stat-grid">',
        '<div class="capability-card">',
        '<span class="card-eyebrow">',
        '<span class="tag">',
    ):
        assert primitive in text, f"dossier missing visual primitive: {primitive!r}"


def test_friendly_callout_transform_strips_todo_label():
    """The render-time HTML post-processor must strip the operator-side
    ``TODO[OPERATOR]`` label from any blockquote and replace it with the
    Spanish friendly label. Source markdown still carries the marker for
    audit; rendered HTML must not."""
    mod = importlib.import_module("akos.hlk_pdf_render")
    sample_html = (
        "<blockquote><p><strong>TODO[OPERATOR]</strong> — Decisión del "
        "fundador.</p><ul><li>Opción A</li></ul></blockquote>"
    )
    out = mod._friendly_callout_labels_html(sample_html, language="es")
    assert "TODO[OPERATOR]" not in out
    assert 'class="callout-question"' in out
    assert "Pregunta abierta para tu confirmación" in out
    assert "Decisión del fundador" in out
    assert "Opción A" in out


def test_friendly_callout_transform_english_variant():
    mod = importlib.import_module("akos.hlk_pdf_render")
    sample_html = "<blockquote><p><strong>TODO[OPERATOR]</strong> — Founder decision.</p></blockquote>"
    out = mod._friendly_callout_labels_html(sample_html, language="en")
    assert "TODO[OPERATOR]" not in out
    assert "Open question for your confirmation" in out


def test_brand_pdf_css_includes_new_visual_classes():
    """Initiative 27 follow-up — verify the brand CSS ships the new visual
    primitives so the dossier markdown render visually."""
    mod = importlib.import_module("akos.hlk_pdf_render")
    css = mod._brand_pdf_css()
    for cls in (
        ".cover-eyebrow",
        ".cover-strip",
        ".strip-item",
        ".stat-grid",
        ".stat-num",
        ".stat-label",
        ".pull-quote",
        ".lead",
        ".capability-card",
        ".card-head",
        ".card-eyebrow",
        ".card-title",
        ".card-tags",
        ".card-body",
        ".card-foot",
        "callout-question",
        "callout-label",
    ):
        assert cls in css, f"brand CSS missing class hook: {cls!r}"
    # Numbered section indicator via CSS counter
    assert "counter-increment: section" in css
    assert "counter(section, decimal-leading-zero)" in css


# ---------- Topic registry row ------------------------------------------------


def test_topic_registry_has_dossier_es_row():
    text = TOPIC_REGISTRY_CSV.read_text(encoding="utf-8")
    assert "topic_enisa_dossier_es" in text
    assert "parent_topic" in text.splitlines()[0]
    rows = [r for r in text.splitlines()[1:] if r.startswith("topic_enisa_dossier_es,")]
    assert len(rows) == 1
    row = rows[0]
    assert "PRJ-HOL-FOUNDING-2026" in row
    assert "advops" in row
    assert "topic_enisa_evidence" in row  # parent_topic
    assert "dossier_es.md" in row  # manifest_path


# ---------- Composer body inlining --------------------------------------------


def test_compose_adviser_inlines_body_file(composer=None):
    """``--body`` flag inlines the canonical Spanish body into Layer 4."""
    spec = importlib.util.spec_from_file_location(
        "_compose_adviser_message_inline", REPO_ROOT / "scripts" / "compose_adviser_message.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("_compose_adviser_message_inline", mod)
    spec.loader.exec_module(mod)

    rec = {"ref_id": "POI-LEG-ENISA-LEAD-2026", "lens": "legal_certification", "class": "external_legal_adviser", "sensitivity": "confidential"}
    disc = {"discipline_id": "legal", "discipline_code": "LEG", "discipline_name": "Legal Counsel"}
    md = mod.render_md(
        recipient=rec,
        discipline=disc,
        program=None,
        voice_register="peer_consulting",
        voice_source="recipient",
        language="es",
        pronoun="tu",
        sharing_label="counsel_and_named_counterparty",
        evidence_path=None,
        body_path=COVER_EMAIL_MD,
    )
    assert "## Layer 4 — Eloquence" in md
    assert "TODO operator" not in md
    assert "Buenos días, Guillermo" in md
    assert "Q-LEG-001" in md
    assert "Un saludo," in md


def test_compose_adviser_emits_todo_when_no_body():
    spec = importlib.util.spec_from_file_location(
        "_compose_adviser_message_inline_b", REPO_ROOT / "scripts" / "compose_adviser_message.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("_compose_adviser_message_inline_b", mod)
    spec.loader.exec_module(mod)

    rec = {"ref_id": "POI-LEG-ENISA-LEAD-2026", "lens": "legal_certification", "class": "external_legal_adviser", "sensitivity": "confidential"}
    disc = {"discipline_id": "legal", "discipline_code": "LEG", "discipline_name": "Legal Counsel"}
    md = mod.render_md(
        recipient=rec,
        discipline=disc,
        program=None,
        voice_register="peer_consulting",
        voice_source="recipient",
        language="es",
        pronoun="tu",
        sharing_label="counsel_and_named_counterparty",
        evidence_path=None,
        body_path=None,
    )
    assert "TODO operator" in md
