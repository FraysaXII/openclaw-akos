"""Aura username misconfiguration helpers."""

from __future__ import annotations

from akos.hlk_neo4j import _aura_instance_id_from_uri, _resolve_neo4j_username


def test_aura_instance_id_from_uri() -> None:
    assert _aura_instance_id_from_uri("neo4j+s://abc123.databases.neo4j.io") == "abc123"
    assert _aura_instance_id_from_uri("bolt://127.0.0.1:7687") == ""


def test_resolve_username_heals_instance_id_copy_paste() -> None:
    uri = "neo4j+s://b6d76b10.databases.neo4j.io"
    assert _resolve_neo4j_username(uri, "b6d76b10") == "neo4j"
    assert _resolve_neo4j_username(uri, "cicd-akos") == "cicd-akos"
    assert _resolve_neo4j_username(uri, "") == "neo4j"
