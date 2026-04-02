from __future__ import annotations

from akos.policy import CapabilityMatrix


def test_madeira_runtime_profile_override_is_coding() -> None:
    matrix = CapabilityMatrix.load()
    madeira_policy = matrix.get_policy("madeira")

    assert madeira_policy is not None
    assert madeira_policy.runtime_profile == "coding"
    assert "read" in madeira_policy.allowed_categories
    assert "write" not in madeira_policy.allowed_categories
