"""Tests for ``akos.graph_stack`` (supervisor health + fingerprint helpers)."""

from __future__ import annotations

import os

import pytest

from akos.graph_stack import (
    fingerprint_canonical_csvs,
    graph_health_payload,
    set_graph_stack_supervisor,
)
from akos.hlk_neo4j import neo4j_env_non_placeholder
from akos.model_catalog import load_model_workflow_ssot

pytestmark = pytest.mark.graph


def test_fingerprint_canonical_csvs_stable():
    fp1 = fingerprint_canonical_csvs()
    fp2 = fingerprint_canonical_csvs()
    assert len(fp1) == 64
    assert fp1 == fp2


def test_graph_health_payload_without_supervisor():
    set_graph_stack_supervisor(None)
    geo, mir = graph_health_payload()
    assert geo["state"] == "not_supervised"
    assert mir["pending"] is False


def test_neo4j_env_non_placeholder_false_when_empty(monkeypatch):
    monkeypatch.delenv("NEO4J_URI", raising=False)
    monkeypatch.delenv("NEO4J_PASSWORD", raising=False)
    assert neo4j_env_non_placeholder() is False


def test_neo4j_env_non_placeholder_false_for_template(monkeypatch):
    monkeypatch.setenv("NEO4J_URI", "neo4j+s://xxxx.databases.neo4j.io")
    monkeypatch.setenv("NEO4J_PASSWORD", "YOUR_AURA_PASSWORD")
    assert neo4j_env_non_placeholder() is False


def test_load_model_workflow_ssot_has_tiers():
    data = load_model_workflow_ssot()
    assert "tiers" in data
    assert "variantOverlays" in data


@pytest.mark.neo4j
@pytest.mark.skipif(
    not os.environ.get("NEO4J_URI", "").strip() or not os.environ.get("NEO4J_PASSWORD", "").strip(),
    reason="NEO4J_URI and NEO4J_PASSWORD required for live Bolt test",
)
def test_neo4j_bolt_handshake():
    from akos.hlk_neo4j import get_neo4j_driver

    drv = get_neo4j_driver()
    assert drv is not None
    try:
        drv.verify_connectivity()
    finally:
        drv.close()
