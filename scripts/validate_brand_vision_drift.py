#!/usr/bin/env python3
"""Validate BRAND_VISION public-region drift against boilerplate /vision (I66 P7)."""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.brand_vision_drift")

VISION_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Marketing"
    / "Brand"
    / "BRAND_VISION.md"
)
BOILERPLATE_ROOT = REPO_ROOT.parent / "root_cd" / "boilerplate"
BOILERPLATE_VISION_PAGE = BOILERPLATE_ROOT / "app" / "vision" / "page.tsx"
BOILERPLATE_EN_MESSAGES = BOILERPLATE_ROOT / "i18n" / "messages" / "en.json"

PUBLIC_START = "<!-- public-vision:start -->"
PUBLIC_END = "<!-- public-vision:end -->"

REQUIRED_PUBLIC_FRAGMENTS = (
    "Most companies operate without seeing themselves clearly.",
    "Holistika exists to give companies a clearer view of their own operation",
    "We change the inside of a company, not the outside.",
    "Three operational arms working as a flywheel.",
    "Holistika Research & Strategy",
    "Think Big",
    "HLK Tech Lab",
    "Research validates",
    "strategy guides execution",
    "execution validates research",
    "The founder, Fay",
    "seven venues",
    "We are not a generic transformation consultancy.",
    "We are an operating company",
)


@dataclass(frozen=True)
class VisionDriftError:
    rule: str
    detail: str
    file: Path


def extract_public_region(text: str) -> str:
    start = text.find(PUBLIC_START)
    end = text.find(PUBLIC_END)
    if start < 0 or end < 0 or end <= start:
        raise ValueError("BRAND_VISION public markers are missing or misordered")
    return text[start + len(PUBLIC_START):end].strip()


def flatten_json_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for child in value.values():
            out.extend(flatten_json_strings(child))
        return out
    if isinstance(value, list):
        out: list[str] = []
        for child in value:
            out.extend(flatten_json_strings(child))
        return out
    return []


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def check_vision_drift(
    vision_path: Path = VISION_PATH,
    page_path: Path = BOILERPLATE_VISION_PAGE,
    messages_path: Path = BOILERPLATE_EN_MESSAGES,
) -> list[VisionDriftError]:
    errors: list[VisionDriftError] = []
    if not vision_path.exists():
        return [VisionDriftError("missing_vision_canonical", "BRAND_VISION.md not found", vision_path)]
    if not page_path.exists():
        errors.append(VisionDriftError("missing_vision_page", "boilerplate /vision page not found", page_path))
    if not messages_path.exists():
        errors.append(VisionDriftError("missing_vision_messages", "boilerplate EN messages not found", messages_path))
    if errors:
        return errors

    try:
        public_region = extract_public_region(vision_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [VisionDriftError("vision_markers_invalid", str(exc), vision_path)]

    message_data = json.loads(messages_path.read_text(encoding="utf-8"))
    vision_messages = message_data.get("vision", {})
    flattened = "\n".join(flatten_json_strings(vision_messages))
    normalized_messages = normalize(flattened)
    normalized_page = normalize(page_path.read_text(encoding="utf-8"))

    for fragment in REQUIRED_PUBLIC_FRAGMENTS:
        if normalize(fragment) not in normalized_messages:
            errors.append(
                VisionDriftError(
                    "missing_public_fragment",
                    f"required public-vision fragment absent from EN messages: {fragment!r}",
                    messages_path,
                )
            )

    for key in (
        "whyExists",
        "whatChange",
        "howChange",
        "whatThisMeans",
        "howGotHere",
        "whatNot",
    ):
        if key not in vision_messages:
            errors.append(
                VisionDriftError("missing_vision_section", f"vision.{key} missing", messages_path)
            )
        if normalize(key) not in normalized_page:
            errors.append(
                VisionDriftError("page_not_rendering_section", f"page does not reference translation key {key}", page_path)
            )

    forbidden_public_tokens = ("AKOS", "TODO[OPERATOR]", "counterparty", "elicitation")
    normalized_public = normalize(public_region)
    for token in forbidden_public_tokens:
        if normalize(token) in normalized_public:
            errors.append(
                VisionDriftError(
                    "forbidden_token_in_public_vision",
                    f"forbidden token present in public region: {token}",
                    vision_path,
                )
            )

    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate BRAND_VISION public-region drift")
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    errors = check_vision_drift()
    if errors:
        for err in errors:
            logger.error("%s: %s (%s)", err.rule, err.detail, err.file)
        return 1
    logger.info("BRAND_VISION_DRIFT OK - boilerplate /vision tracks the public vision region")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
