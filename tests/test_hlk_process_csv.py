"""Unit tests for akos.hlk_process_csv SSOT helpers."""

from __future__ import annotations

from akos.hlk_process_csv import (
    item_name_uniqueness_errors,
    resolve_all_parent_ids,
    suggest_item_id_renames_for_duplicate_names,
)


def test_item_name_uniqueness_errors_empty_when_unique():
    rows = [
        {"item_name": "Alpha", "item_id": "a1", "item_parent_1": "", "item_parent_2": ""},
        {"item_name": "Beta", "item_id": "b1", "item_parent_1": "", "item_parent_2": ""},
    ]
    assert item_name_uniqueness_errors(rows) == []


def test_item_name_uniqueness_errors_detects_duplicate_display_names():
    rows = [
        {"item_name": "Same", "item_id": "x1", "item_parent_1": "", "item_parent_2": ""},
        {"item_name": "Same", "item_id": "x2", "item_parent_1": "", "item_parent_2": ""},
    ]
    errs = item_name_uniqueness_errors(rows)
    assert len(errs) == 1
    assert "Same" in errs[0]
    assert "x1" in errs[0] and "x2" in errs[0]


def test_suggest_renames_two_tasks_smallest_id_keeps_name():
    rows = [
        {"item_name": "Dup", "item_id": "z9", "item_granularity": "task", "item_parent_1": ""},
        {"item_name": "Dup", "item_id": "a1", "item_granularity": "task", "item_parent_1": ""},
    ]
    sugg = suggest_item_id_renames_for_duplicate_names(rows)
    assert "a1" not in sugg
    assert sugg.get("z9") == "Dup (z9)"


def test_suggest_renames_prefers_workstream_over_task():
    rows = [
        {"item_name": "X", "item_id": "ws", "item_granularity": "workstream", "item_parent_1": ""},
        {"item_name": "X", "item_id": "t1", "item_granularity": "task", "item_parent_1": ""},
    ]
    sugg = suggest_item_id_renames_for_duplicate_names(rows)
    assert "ws" not in sugg
    assert sugg["t1"] == "X (t1)"


def test_resolve_all_parent_ids_skips_ambiguous_parent_name():
    rows = [
        {"item_name": "P1", "item_id": "p1", "item_parent_1": "", "item_parent_2": ""},
        {"item_name": "P1", "item_id": "p2", "item_parent_1": "", "item_parent_2": ""},
        {"item_name": "Child", "item_id": "c1", "item_parent_1": "P1", "item_parent_2": ""},
    ]
    out = resolve_all_parent_ids(rows)
    child = next(r for r in out if r["item_id"] == "c1")
    assert child.get("item_parent_1_id") == ""
