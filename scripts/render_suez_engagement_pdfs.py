#!/usr/bin/env python3
"""Render SUEZ-WeBuy engagement FR deliverables to brand-aligned PDF.

Thin wrapper around ``akos.hlk_pdf_render.render_pdf_branded`` covering the
seven surfaces of the SUEZ-WeBuy procure-to-pay engagement, in two audience
packs (operator-and-collaborator + customer-facing):

Operator pack (4):

1. ``cdc-feasibility-shape.fr.md`` — point-by-point cahier des charges (centerpiece).
2. ``discovery-questionnaire.fr.md`` — discovery questionnaire (live walk-through).
3. ``proposal.fr.md`` — full proposal with internal tarification annex.
4. ``deck-suez-webuy.fr.md`` — operator-and-collaborator presentation deck.

Customer pack (3):

5. ``proposal.customer.fr.md`` — pricing-free customer-facing proposal.
6. ``tarification.customer.fr.md`` — separate tarification annex.
7. ``deck.customer.fr.md`` — customer-facing slide deck (slides profile).

Source markdowns live under the canonical client-engagement home:
``docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/`` with audience
sub-folders ``01-operator-pack/`` and ``02-customer-pack/`` (per
``BRAND_COBRANDING_PATTERN.md`` and the engagement README).

Output PDFs land at the engagement's own ``_exports/`` sub-folder with a
sha256 manifest for the checkpoint trail. The PDFs and ``render-manifest.json``
are **tracked in git** as a distribution surface (this repo is shared with
non-technical readers via git + Google Drive sync; most stakeholders consume
PDFs, not markdown). The render-time markdown sidecars in ``_exports/`` are
gitignored — they duplicate the canonical sources in the audience sub-folders
and tracking them would create drift risk.

Each surface carries its own cover metadata (title / subtitle / discipline) so
the brand cover hero band reads naturally in FR. The ``Programme`` field
references the engagement slug so any future re-render aligns deterministically.

Usage::

    py scripts/render_suez_engagement_pdfs.py
    py scripts/render_suez_engagement_pdfs.py --smoke
    py scripts/render_suez_engagement_pdfs.py --only proposal

Soft-success behaviour matches ``render_pdf_branded``: when no PDF renderer is
available, a markdown sidecar is written next to the target PDF and the script
returns 0.

Exit codes::

    0 — all surfaces rendered (or soft-success markdown sidecars).
    1 — at least one source markdown is missing.
    2 — usage error.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import inspect
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_pdf_render import render_pdf_branded  # noqa: E402

ENGAGEMENT_SLUG = "2026-suez-webuy"
ENGAGEMENT_PROGRAM = "ENG-SUEZ-WEBUY-2026"

# Canonical client-engagement home (Think Big/Clients/) per
# WORKSPACE_BLUEPRINT_HOLISTIKA.md (P13.1) and the SUEZ engagement README at
# docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/README.md.
ENGAGEMENT_DIR = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Think Big"
    / "Clients"
    / ENGAGEMENT_SLUG
)

# Audience-segmented sub-folders. Each surface declares its audience so paths
# are derivable and never hard-coded per-surface.
OPERATOR_PACK = ENGAGEMENT_DIR / "01-operator-pack"
CUSTOMER_PACK = ENGAGEMENT_DIR / "02-customer-pack"
EXTERNAL_MARKS = ENGAGEMENT_DIR / "_external_marks"

OUT_DIR = ENGAGEMENT_DIR / "_exports"

BOILERPLATE_LOGO_PATH = (
    REPO_ROOT.parent / "root_cd" / "boilerplate" / "public" / "holistika-short-100x100.svg"
)

# EFA Académie guest brand assets (per BRAND_COBRANDING_PATTERN.md §3.3 and the
# engagement's _external_marks/ folder). Two paths are kept: a primary mark and
# a light-background "fonds Blancs" variant. Slide 02 host-card uses the light
# variant (the slide background is light); the cover-strip carries the partner
# *name only* (no logo) per BRAND_COBRANDING_PATTERN.md §3.2.
EFA_LOGO_PATH = EXTERNAL_MARKS / "efa-academie-logo.png"
EFA_LOGO_LIGHT_PATH = EXTERNAL_MARKS / "efa-academie-logo-light.png"

# Co-branding metadata applied to customer-pack surfaces (per D-12-5 and the
# engagement README). Threaded through render_pdf_branded as
# collaboration_partner + guest_logo_path. Operator-pack surfaces stay solo-host
# (no cover-strip 4-field, no host-card slide insertion) since their audience
# already knows the partnership context.
COLLABORATION_PARTNER = "EFA Académie"


SURFACES: dict[str, dict[str, str]] = {
    "cdc": {
        "audience": "operator",
        "source": "cdc-feasibility-shape.fr.md",
        "out": "cdc-feasibility-shape.fr.pdf",
        "title": "Cahier des charges fonctionnel",
        "subtitle": "Processus de demande d'achat WeBuy, forme de faisabilité",
        "discipline": "Cadrage fonctionnel et faisabilité",
        "eyebrow": "Holistika Research · Cadrage fonctionnel",
    },
    "questionnaire": {
        "audience": "operator",
        "source": "discovery-questionnaire.fr.md",
        "out": "discovery-questionnaire.fr.pdf",
        "title": "Questionnaire de découverte",
        "subtitle": "Premier rendez-vous, cadrage opérationnel",
        "discipline": "Découverte client",
        "eyebrow": "Holistika Research · Découverte",
    },
    "proposal": {
        "audience": "operator",
        "source": "proposal.fr.md",
        "out": "proposal.fr.pdf",
        "title": "Proposition d'engagement",
        "subtitle": "Automatisation du processus de demande d'achat WeBuy",
        "discipline": "Engagement, version commerciale et collaborateurs",
        "eyebrow": "Holistika Research · Proposition (version complète)",
    },
    "deck": {
        "audience": "operator",
        "source": "deck-suez-webuy.fr.md",
        "out": "deck-suez-webuy.fr.pdf",
        "title": "Présentation Holistika × WeBuy",
        "subtitle": "Faciliter votre processus de demande d'achat",
        "discipline": "Présentation commerciale",
        "eyebrow": "Holistika Research · Présentation",
    },
    # Customer-facing pack (P10 + P11 + P12): brand-impeccable, pricing-free
    # proposal, detachable tarification annex, plus a slide-shaped customer
    # presentation. Distinct audience from the four above: a procurement reader
    # at SUEZ. Co-branded host/guest pattern per BRAND_COBRANDING_PATTERN.md
    # carries the EFA Académie attribution on the cover-strip and slide-02
    # host-card.
    "proposal_customer": {
        "audience": "customer",
        "source": "proposal.customer.fr.md",
        "out": "proposal.customer.fr.pdf",
        "title": "Proposition d'engagement",
        "subtitle": "Cadrer · prototyper · transférer",
        "discipline": "Automatisation de la demande d'achat WeBuy",
        "eyebrow": "Holistika Research · Proposition",
    },
    "tarification_customer": {
        "audience": "customer",
        "source": "tarification.customer.fr.md",
        "out": "tarification.customer.fr.pdf",
        "title": "Calendrier commercial",
        "subtitle": "Variantes A, B, C, édition mai 2026",
        "discipline": "Annexe à la Proposition d'engagement",
        "eyebrow": "Holistika Research · Calendrier commercial",
    },
    "deck_customer": {
        "audience": "customer",
        "source": "deck.customer.fr.md",
        "out": "deck.customer.fr.pdf",
        "title": "Facilitez votre processus de demande d'achat WeBuy",
        "subtitle": "Automatiser la composition. Tracer la commande. Prévenir le litige.",
        "discipline": "Présentation commerciale",
        "eyebrow": "Holistika Research · Présentation",
        "profile": "slides",
    },
    # Wave R+1 Commit 4 (D-IH-86-EH): architecture addendum FR — 2-page
    # customer-pack addendum complementing proposal.customer.fr.md with the
    # three-phase Microsoft Power Platform architecture (Power Query / Power
    # Apps + SharePoint + Power Automate / Power BI feasibility) + Aïsha-led
    # continuity narrative + SUEZ CTO office replicability narrative + the
    # 3-surface ERP-engagement-governance UX shape from D-IH-82-V.
    "architecture_addendum": {
        "audience": "customer",
        "source": "architecture-addendum.fr.md",
        "out": "architecture-addendum.fr.pdf",
        "title": "Addenda architecturale en trois temps",
        "subtitle": "Power Query · Power Platform · faisabilité ERP + continuité opératrice partenaire",
        "discipline": "Annexe à la Proposition d'engagement",
        "eyebrow": "Holistika Research · Addenda architecturale",
    },
}


def _audience_dir(audience: str) -> Path:
    """Return the audience sub-folder for a given surface audience tag."""
    if audience == "operator":
        return OPERATOR_PACK
    if audience == "customer":
        return CUSTOMER_PACK
    raise ValueError(f"render_suez_engagement_pdfs: unknown audience {audience!r}")


def strip_frontmatter(md: str) -> str:
    return re.sub(r"^---\s*\n.*?\n---\s*\n", "", md, count=1, flags=re.DOTALL)


_INTERNAL_CHECKLIST_RE = re.compile(
    r"\n\s*---\s*\n+##\s+Liste de validation interne.*\Z",
    re.DOTALL | re.IGNORECASE,
)


def strip_internal_checklist(md: str) -> str:
    """Remove an embedded ``## Liste de validation interne`` block.

    The proposal carries an internal operator review checklist appended after a
    horizontal rule. The checklist is kept in the source markdown for operator
    audit + the SOP-ENG_PROPOSAL_001 review trail, but it must NOT appear in
    the rendered PDF that ships externally — it intentionally cites internal
    register vocabulary as a "make sure none of these terms leaked" guard.

    The renderer strips any section whose heading starts with
    ``## Liste de validation interne`` plus the preceding ``---`` separator,
    through end-of-file.
    """
    return _INTERNAL_CHECKLIST_RE.sub("", md)


def _sha256_of_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--only",
        choices=list(SURFACES.keys()),
        default=None,
        help="Render only one surface (default: all six).",
    )
    parser.add_argument(
        "--issue-date",
        default=None,
        help="ISO date stamped on the cover and footer (default: today UTC).",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke-mode: verify all source markdowns exist + cover metadata resolves; no PDF written.",
    )
    args = parser.parse_args(argv)

    issue_date = args.issue_date or _dt.datetime.now(_dt.UTC).date().isoformat()
    monogram_path = str(BOILERPLATE_LOGO_PATH) if BOILERPLATE_LOGO_PATH.is_file() else None

    surfaces_to_render = (
        {args.only: SURFACES[args.only]} if args.only else SURFACES
    )

    missing: list[str] = []
    for meta in surfaces_to_render.values():
        src = _audience_dir(meta["audience"]) / meta["source"]
        if not src.is_file():
            missing.append(str(src.relative_to(REPO_ROOT)).replace("\\", "/"))
    if missing:
        sys.stderr.write(
            "render_suez_engagement_pdfs: REFUSED — missing source(s): "
            f"{', '.join(missing)}\n"
        )
        return 1

    if args.smoke:
        for key, meta in surfaces_to_render.items():
            md_path = _audience_dir(meta["audience"]) / meta["source"]
            text = md_path.read_text(encoding="utf-8")
            body = strip_internal_checklist(strip_frontmatter(text))
            print(
                f"render_suez_engagement_pdfs: smoke OK — surface={key} "
                f"audience={meta['audience']} "
                f"source={md_path.relative_to(REPO_ROOT)} body_chars={len(body)} "
                f"title={meta['title']!r} discipline={meta['discipline']!r} "
                f"monogram={'present' if monogram_path else 'absent'}"
            )
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    efa_logo = str(EFA_LOGO_PATH) if EFA_LOGO_PATH.is_file() else None
    efa_logo_light = (
        str(EFA_LOGO_LIGHT_PATH) if EFA_LOGO_LIGHT_PATH.is_file() else None
    )

    manifest_entries: list[dict] = []
    overall_rc = 0
    for key, meta in surfaces_to_render.items():
        md_path = _audience_dir(meta["audience"]) / meta["source"]
        out_path = OUT_DIR / meta["out"]
        text = md_path.read_text(encoding="utf-8")
        body = strip_internal_checklist(strip_frontmatter(text))

        md_sidecar = out_path.with_suffix(".md")
        if not md_sidecar.is_file() or md_sidecar.read_text(encoding="utf-8") != text:
            md_sidecar.write_text(text, encoding="utf-8")

        # Co-branding metadata (per BRAND_COBRANDING_PATTERN.md): customer-pack
        # surfaces carry the EFA host/guest attribution; operator-pack surfaces
        # stay solo-host. The render_pdf_branded keyword set is introspected
        # so this script stays forward-compatible: P12.3 stages the metadata
        # here, P12.7 adds collaboration_partner + guest_logo_path to the
        # renderer signature, and at that point this dispatch starts threading
        # the kwargs through. Until then, the metadata is silently dropped
        # rather than crashing the render.
        is_customer = meta["audience"] == "customer"
        cobranding_kwargs: dict = {}
        if is_customer:
            cobranding_kwargs["collaboration_partner"] = COLLABORATION_PARTNER
            if efa_logo is not None:
                cobranding_kwargs["guest_logo_path"] = efa_logo
            if efa_logo_light is not None:
                cobranding_kwargs["guest_logo_light_path"] = efa_logo_light

        renderer_params = set(inspect.signature(render_pdf_branded).parameters.keys())
        accepted_cobranding = {
            k: v for k, v in cobranding_kwargs.items() if k in renderer_params
        }

        rc = render_pdf_branded(
            body,
            out_path,
            profile=meta.get("profile", "dossier"),
            title=meta["title"],
            subtitle=meta["subtitle"],
            program_id=ENGAGEMENT_PROGRAM,
            discipline=meta["discipline"],
            issue_date=issue_date,
            monogram_path=monogram_path,
            source_label=f"render_suez:{key}",
            language="fr",
            eyebrow=meta.get("eyebrow"),
            **accepted_cobranding,
        )
        if rc != 0 and overall_rc == 0:
            overall_rc = rc

        md_sha = _sha256_of_text(text)
        pdf_sha = _sha256_of_path(out_path) if out_path.is_file() else None
        manifest_entries.append(
            {
                "surface": key,
                "source_md": str(md_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "source_md_sha256": md_sha,
                "rendered_pdf": str(out_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "rendered_pdf_sha256": pdf_sha,
                "title": meta["title"],
                "subtitle": meta["subtitle"],
                "discipline": meta["discipline"],
                "renderer_rc": rc,
            }
        )

    manifest_path = OUT_DIR / "render-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "engagement_slug": ENGAGEMENT_SLUG,
                "program_id": ENGAGEMENT_PROGRAM,
                "issue_date": issue_date,
                "monogram_path": monogram_path,
                "surfaces": manifest_entries,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    print(f"render_suez_engagement_pdfs: manifest -> {manifest_path.relative_to(REPO_ROOT)}")

    for entry in manifest_entries:
        sha = entry["rendered_pdf_sha256"]
        print(
            f"render_suez_engagement_pdfs: surface={entry['surface']} "
            f"md_sha={entry['source_md_sha256'][:16]}... "
            f"pdf_sha={(sha[:16] + '...') if sha else 'absent (soft-success md sidecar only)'}"
        )

    return overall_rc


if __name__ == "__main__":
    raise SystemExit(main())
