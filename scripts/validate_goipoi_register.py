#!/usr/bin/env python3
"""Validate GOI_POI_REGISTER.csv against org, process_list, and ref-id discipline.

Usage: py scripts/validate_goipoi_register.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
# I32 P7 (D-IH-32-D): GOI/POI relocated from compliance/ to compliance/dimensions/.
# Deprecation alias supported for one initiative cycle: validator falls back to
# the legacy path when the dimensions/ path is absent. Remove the alias in I33.
GOIPOI_CSV = HLK_COMPLIANCE / "dimensions" / "GOI_POI_REGISTER.csv"
GOIPOI_CSV_LEGACY = HLK_COMPLIANCE / "GOI_POI_REGISTER.csv"  # deprecation alias
if not GOIPOI_CSV.is_file() and GOIPOI_CSV_LEGACY.is_file():
    GOIPOI_CSV = GOIPOI_CSV_LEGACY
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"
PROC_CSV = HLK_COMPLIANCE / "process_list.csv"

ENTITY_KINDS = {"person", "organisation"}
# `class` enum — Initiative 22 P4 (D-IH-5) extended set so the dimension supports
# multi-program reuse across MKTOPS / FINOPS / ADVOPS / public-affairs touchpoints.
# Backwards-compatible: existing rows (Initiative 21) only use the first nine entries.
CLASSES = {
    # Original Initiative 21 set (founder-incorporation seed scope)
    "external_adviser",
    "banking_channel",
    "supplier",
    "research_benchmark",
    "lead",
    "client_org",
    "collaborator",
    "public_authority",
    "other",
    # Initiative 22 P4 extension — multi-program / multi-plane reuse
    "client",          # active client of Holistika (engagement-keyed via program_id)
    "partner",         # strategic partner / channel partner / SI partner
    "investor",        # angel, VC, public-funding agency operating as investor (private flow)
    "regulator",       # public regulator authority (typically is_public_entity=true)
    "vendor",          # paid commercial supplier (FINOPS counterparty); cross-references FINOPS_COUNTERPARTY_REGISTER.csv
    "media",           # press, podcast host, public-relations contact
}
SENSITIVITY = {"public", "internal", "confidential", "restricted"}
BOOLS = {"true", "false"}

# Initiative 24 P2 (D-IH-11) optional voice profile enums.
# Backwards-compatible: empty string is allowed and triggers fallback to discipline default.
VOICE_REGISTERS = {
    "",
    "formal_legal",
    "peer_consulting",
    "casual_internal",
    "regulator_neutral",
    "investor_aspirational",
}
LANGUAGE_PREFERENCES = {"", "es", "en", "bilingual"}
PRONOUN_REGISTERS = {"", "tu", "usted"}

# Initiative 31 P2.2 (D-IH-31-G) — distance dimension on the social graph.
DISTANCE_BANDS = {"N1", "N2", "N3", "N4"}
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REF_ID_RE = re.compile(r"^(POI|GOI)-[A-Z0-9]{2,5}-[A-Z0-9-]{1,40}-\d{4}$")
PROGRAM_ID_RE = re.compile(r"^(PRJ-[A-Z0-9]+-[A-Z0-9]+-\d{4})?$")
LENS_RE = re.compile(r"^[a-z][a-z0-9_]{1,40}$")


def load_org_roles() -> set[str]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return {r["role_name"].strip() for r in csv.DictReader(f) if r.get("role_name")}


def load_process_ids() -> set[str]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return {r["item_id"].strip() for r in csv.DictReader(f) if r.get("item_id")}


def main() -> int:
    print("\n  GOI_POI_REGISTER Validator")
    print("  " + "=" * 40)
    if not GOIPOI_CSV.is_file():
        print("  FAIL: GOI_POI_REGISTER.csv not found")
        return 1

    org_roles = load_org_roles()
    proc_ids = load_process_ids()

    errors: list[str] = []
    with open(GOIPOI_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(GOIPOI_REGISTER_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(GOIPOI_REGISTER_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        ref = (r.get("ref_id") or "").strip()
        if not ref:
            errors.append(f"row {i}: empty ref_id")
            continue
        if ref in seen:
            errors.append(f"row {i}: duplicate ref_id {ref}")
        seen.add(ref)
        if not REF_ID_RE.match(ref):
            errors.append(f"row {i}: ref_id must match POI/GOI-<class>-<slug>-<YYYY>: {ref!r}")

        kind = (r.get("entity_kind") or "").strip()
        if kind not in ENTITY_KINDS:
            errors.append(f"row {i}: invalid entity_kind {kind!r}")
        if ref.startswith("POI-") and kind != "person":
            errors.append(f"row {i}: ref_id {ref} starts with POI- but entity_kind={kind!r}")
        if ref.startswith("GOI-") and kind != "organisation":
            errors.append(f"row {i}: ref_id {ref} starts with GOI- but entity_kind={kind!r}")

        cls = (r.get("class") or "").strip()
        if cls not in CLASSES:
            errors.append(f"row {i}: invalid class {cls!r}")

        public = (r.get("is_public_entity") or "").strip().lower()
        if public not in BOOLS:
            errors.append(f"row {i}: is_public_entity must be 'true' or 'false', got {public!r}")

        display = (r.get("display_name") or "").strip()
        if not display:
            errors.append(f"row {i}: display_name required")
        if "@" in display or "@" in (r.get("notes") or ""):
            errors.append(f"row {i}: '@' in display_name or notes (potential email leak)")

        lens = (r.get("lens") or "").strip()
        if lens and not LENS_RE.match(lens):
            errors.append(f"row {i}: lens must be lowercase_snake (1-40 chars): {lens!r}")

        sens = (r.get("sensitivity") or "").strip()
        if sens not in SENSITIVITY:
            errors.append(f"row {i}: invalid sensitivity {sens!r}")

        prog = (r.get("program_id") or "").strip()
        if prog and not PROGRAM_ID_RE.match(prog):
            errors.append(f"row {i}: program_id must match PRJ-<E>-<TOPIC>-<YYYY> or empty: {prog!r}")

        role = (r.get("role_owner") or "").strip()
        if role and role not in org_roles:
            errors.append(f"row {i}: role_owner {role!r} not in baseline_organisation")

        pid = (r.get("process_item_id") or "").strip()
        if pid and pid not in proc_ids:
            errors.append(f"row {i}: process_item_id {pid!r} not in process_list")

        link = (r.get("primary_link") or "").strip()
        if link and ".." in link:
            errors.append(f"row {i}: primary_link must not contain '..': {link!r}")

        if public == "false" and sens == "public":
            errors.append(f"row {i}: is_public_entity=false but sensitivity=public (inconsistent)")

        # Initiative 24 P2 (D-IH-11): voice profile columns. All optional;
        # empty value triggers fallback to discipline default at composer time.
        voice = (r.get("voice_register") or "").strip()
        if voice not in VOICE_REGISTERS:
            errors.append(
                f"row {i}: invalid voice_register {voice!r}; expected one of "
                f"{sorted(VOICE_REGISTERS - {''})} or empty"
            )
        lang = (r.get("language_preference") or "").strip()
        if lang not in LANGUAGE_PREFERENCES:
            errors.append(
                f"row {i}: invalid language_preference {lang!r}; expected one of "
                f"{sorted(LANGUAGE_PREFERENCES - {''})} or empty"
            )
        pron = (r.get("pronoun_register") or "").strip()
        if pron not in PRONOUN_REGISTERS:
            errors.append(
                f"row {i}: invalid pronoun_register {pron!r}; expected one of "
                f"{sorted(PRONOUN_REGISTERS - {''})} or empty"
            )
        # Sanity: if pronoun_register is set, language_preference should support it.
        if pron in {"tu", "usted"} and lang not in {"", "es", "bilingual"}:
            errors.append(
                f"row {i}: pronoun_register={pron!r} requires language_preference in {{es, bilingual}} or empty; "
                f"got {lang!r}"
            )

        # Initiative 31 P2.2 (D-IH-31-G): distance band invariants.
        dist = (r.get("distance_band") or "").strip()
        if dist not in DISTANCE_BANDS:
            errors.append(
                f"row {i}: invalid distance_band {dist!r}; expected one of {sorted(DISTANCE_BANDS)}"
            )
        bridge = (r.get("bridge_via") or "").strip()
        if dist == "N1":
            if bridge:
                errors.append(
                    f"row {i}: distance_band=N1 but bridge_via={bridge!r} (must be empty for N1)"
                )
        elif dist in {"N2", "N3", "N4"}:
            if not bridge:
                errors.append(
                    f"row {i}: distance_band={dist} requires bridge_via to be set "
                    f"(an immediate intermediary's POI/GOI ref_id)"
                )
            elif bridge == ref:
                errors.append(
                    f"row {i}: bridge_via={bridge!r} points at self ref_id; impossible cycle"
                )
        assessed = (r.get("distance_assessed_date") or "").strip()
        if not assessed:
            errors.append(f"row {i}: distance_assessed_date is required (ISO date)")
        elif not ISO_DATE_RE.match(assessed):
            errors.append(
                f"row {i}: distance_assessed_date {assessed!r} not in ISO format (YYYY-MM-DD)"
            )

    # Pass 2: bridge_via FK + cycle detection. Collect all ref_ids first.
    all_refs = {(row.get("ref_id") or "").strip() for row in rows}
    bridge_graph: dict[str, str] = {}
    for i, r in enumerate(rows, start=2):
        ref = (r.get("ref_id") or "").strip()
        bridge = (r.get("bridge_via") or "").strip()
        if bridge and bridge not in all_refs:
            errors.append(
                f"row {i}: bridge_via={bridge!r} does not resolve to any ref_id in this register"
            )
        if bridge:
            bridge_graph[ref] = bridge
    # Cycle detection (depth-first traversal of the bridge graph).
    for start_node in list(bridge_graph.keys()):
        seen_chain: set[str] = set()
        cur: str | None = start_node
        depth = 0
        while cur is not None and cur in bridge_graph:
            if cur in seen_chain:
                errors.append(
                    f"bridge_via cycle detected starting at ref_id {start_node!r}: chain {sorted(seen_chain)}"
                )
                break
            seen_chain.add(cur)
            cur = bridge_graph.get(cur)
            depth += 1
            # Defensive cap: a chain longer than 10 hops is almost certainly a bug.
            if depth > 10:
                errors.append(
                    f"bridge_via chain longer than 10 hops starting at {start_node!r}; possible runaway"
                )
                break

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
