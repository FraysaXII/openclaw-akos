"""Initiative 49 P15 — i18n parity assertions for `static/madeira_control.html`.

Parses the inline ``i18n`` JS dictionary (en/es/fr) and ensures every key
declared in any locale exists in the other two with a non-empty string. Also
verifies that every ``data-i18n`` attribute used by the markup has a matching
entry in the English dictionary (the fallback locale).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

CONTROL_HTML_PATH = REPO_ROOT / "static" / "madeira_control.html"

I18N_BLOCK_RE = re.compile(r"const\s+i18n\s*=\s*(\{.*?\});", re.DOTALL)
LOCALE_BLOCK_RE = re.compile(
    r"(en|es|fr)\s*:\s*\{(?P<body>.*?)\}\s*,?\s*(?=(?:en|es|fr)\s*:|$)",
    re.DOTALL,
)
ENTRY_RE = re.compile(
    r"\b(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*"
    r"(?P<value>(?:\"(?:[^\"\\]|\\.)*\"))",
    re.DOTALL,
)
DATA_I18N_RE = re.compile(r'data-i18n="([^"]+)"')


def _load_html() -> str:
    return CONTROL_HTML_PATH.read_text(encoding="utf-8")


def _parse_i18n(html_text: str) -> dict[str, dict[str, str]]:
    """Walk the inline `i18n` dictionary using a depth counter so nested
    template-literal braces inside string values do not confuse the parser."""
    out: dict[str, dict[str, str]] = {}
    head = "const i18n = {"
    start = html_text.find(head)
    assert start != -1, "i18n constant not found in HTML"
    pos = start + len(head)
    depth = 1
    end = pos
    while end < len(html_text) and depth:
        ch = html_text[end]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        end += 1
    block_body = html_text[start + len(head) - 1: end]

    for locale in ("en", "es", "fr"):
        loc_start = block_body.find(f"{locale}:")
        assert loc_start != -1, f"locale {locale!r} missing from i18n dictionary"
        depth_local = 0
        scan = block_body.find("{", loc_start)
        cursor = scan
        depth_local = 1
        while cursor < len(block_body) and depth_local:
            cursor += 1
            if cursor >= len(block_body):
                break
            if block_body[cursor] == "{":
                depth_local += 1
            elif block_body[cursor] == "}":
                depth_local -= 1
        body = block_body[scan + 1: cursor]
        loc_dict: dict[str, str] = {}
        for entry in ENTRY_RE.finditer(body):
            key = entry.group("key")
            raw = entry.group("value")
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                value = raw.strip().strip('"')
            loc_dict[key] = value
        out[locale] = loc_dict
    return out


@pytest.fixture(scope="module")
def html_text() -> str:
    return _load_html()


@pytest.fixture(scope="module")
def i18n(html_text: str) -> dict[str, dict[str, str]]:
    return _parse_i18n(html_text)


def test_three_locales_present(i18n: dict[str, dict[str, str]]) -> None:
    assert set(i18n) == {"en", "es", "fr"}


def test_each_locale_has_keys(i18n: dict[str, dict[str, str]]) -> None:
    for locale, table in i18n.items():
        assert table, f"locale {locale} dictionary is empty"


def test_locale_key_parity(i18n: dict[str, dict[str, str]]) -> None:
    en_keys = set(i18n["en"].keys())
    es_keys = set(i18n["es"].keys())
    fr_keys = set(i18n["fr"].keys())
    missing_es = en_keys - es_keys
    missing_fr = en_keys - fr_keys
    extra_es = es_keys - en_keys
    extra_fr = fr_keys - en_keys
    assert not missing_es, f"es missing keys: {missing_es}"
    assert not missing_fr, f"fr missing keys: {missing_fr}"
    assert not extra_es, f"es has extra keys: {extra_es}"
    assert not extra_fr, f"fr has extra keys: {extra_fr}"


def test_all_locale_values_non_empty(i18n: dict[str, dict[str, str]]) -> None:
    for locale, table in i18n.items():
        for key, value in table.items():
            assert value.strip(), f"empty translation: {locale}.{key}"


def test_html_data_i18n_keys_have_english_translation(html_text: str, i18n: dict[str, dict[str, str]]) -> None:
    keys_in_html = set(DATA_I18N_RE.findall(html_text))
    en_keys = set(i18n["en"].keys())
    missing = sorted(keys_in_html - en_keys)
    assert not missing, f"data-i18n keys missing from English dictionary: {missing}"
