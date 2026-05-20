"""One-off: backfill 4-layer-architecture frontmatter into touchpoint-kit intro-message files.

Per D-IH-86-BB ratification (I86 Wave K9), each touchpoint-kit intro_message file
gets:
  - output_type_source: OT-PROSE-MARKDOWN  (the SSOT shape)
  - output_type_render: <channel-derived> (OT-PROSE-EMAIL-RICH or OT-PROSE-DM)
  - artifact_class: AC-INTRO-MESSAGE  (canonical code from ARTIFACT_CLASS_REGISTRY.csv)
  - component_primitive_inventory: list of CP-* codes
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "touchpoint-kit"

CHAN_TO_OUTPUT_TYPE_RENDER = {
    "CHAN-EMAIL-INBOUND": "OT-PROSE-EMAIL-RICH",
    "CHAN-LINKEDIN-DM": "OT-PROSE-DM",
    "CHAN-DIRECT-DM": "OT-PROSE-DM",
    "CHAN-WEB-FORM": "OT-PROSE-MARKDOWN",
}

CHAN_TO_PRIMITIVES = {
    "CHAN-EMAIL-INBOUND": [
        "CP-GREETING",
        "CP-CONTEXT-ANCHOR",
        "CP-HOOK",
        "CP-BODY",
        "CP-CTA",
        "CP-SIGNATURE",
    ],
    "CHAN-LINKEDIN-DM": [
        "CP-GREETING",
        "CP-CONTEXT-ANCHOR",
        "CP-BODY",
        "CP-CTA",
        "CP-SIGNATURE",
    ],
    "CHAN-DIRECT-DM": [
        "CP-GREETING",
        "CP-CONTEXT-ANCHOR",
        "CP-BODY",
        "CP-CTA",
        "CP-SIGNATURE",
    ],
    "CHAN-WEB-FORM": [
        "CP-GREETING",
        "CP-BODY",
        "CP-CTA",
        "CP-SIGNATURE",
    ],
}


def channel_from_path(p: Path) -> str:
    for part in p.parts:
        if part.startswith("CHAN-"):
            return part
    raise ValueError(f"No channel in path: {p}")


def upgrade_frontmatter(text: str, channel: str) -> str:
    """Upgrade 'artifact_class: intro_message' → canonical code + add layer fields."""
    output_type_render = CHAN_TO_OUTPUT_TYPE_RENDER[channel]
    primitives = CHAN_TO_PRIMITIVES[channel]
    primitives_yaml = "\n".join(f"  - {cp}" for cp in primitives)

    new_block = (
        f"output_type_source: OT-PROSE-MARKDOWN\n"
        f"output_type_render: {output_type_render}\n"
        f"artifact_class: AC-INTRO-MESSAGE\n"
        f"component_primitive_inventory:\n{primitives_yaml}\n"
        f"layered_architecture_version: D-IH-86-BB"
    )

    if "artifact_class: AC-INTRO-MESSAGE" in text:
        return text

    pattern = re.compile(r"^artifact_class:\s*intro_message\s*$", re.MULTILINE)
    if not pattern.search(text):
        raise ValueError(
            "Could not find 'artifact_class: intro_message' line to upgrade"
        )
    return pattern.sub(new_block, text, count=1)


def main() -> None:
    files = sorted(KIT.rglob("intro_message_*.md"))
    print(f"Found {len(files)} intro-message files")
    upgraded = 0
    skipped = 0
    for f in files:
        channel = channel_from_path(f)
        text = f.read_text(encoding="utf-8")
        try:
            new_text = upgrade_frontmatter(text, channel)
        except ValueError as exc:
            print(f"  SKIP {f.relative_to(ROOT)}: {exc}")
            skipped += 1
            continue
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            print(f"  UPGRADED {f.relative_to(ROOT)} (channel={channel})")
            upgraded += 1
        else:
            print(f"  ALREADY-UPGRADED {f.relative_to(ROOT)}")
            skipped += 1
    print(f"\nTotal: {upgraded} upgraded, {skipped} skipped")


if __name__ == "__main__":
    main()
