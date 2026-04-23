"""Pytest oracle file (not named test_*.py — not collected by default suite)."""

from target_module import VALUE


def test_value_is_two():
    assert VALUE == 2
