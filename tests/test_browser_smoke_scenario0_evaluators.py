"""Unit tests for Scenario 0 golden evaluators in ``scripts/browser-smoke.py``."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def browser_smoke_mod():
    path = REPO_ROOT / "scripts" / "browser-smoke.py"
    spec = importlib.util.spec_from_file_location("browser_smoke_scenario0", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["browser_smoke_scenario0"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_evaluate_cto_pass(browser_smoke_mod):
    data = {
        "status": "ok",
        "best_role": {
            "role_name": "CTO",
            "access_level": 5,
            "role_description": "Chief Technology Officer",
            "role_full_description": "",
        },
    }
    r = browser_smoke_mod.evaluate_scenario0_cto_payload(data)
    assert r["status"] == "PASS"
    assert r["scenario"] == "scenario0_hlk_cto"


def test_evaluate_cto_wrong_level(browser_smoke_mod):
    data = {
        "status": "ok",
        "best_role": {"role_name": "CTO", "access_level": 4, "role_description": "Chief Technology Officer"},
    }
    r = browser_smoke_mod.evaluate_scenario0_cto_payload(data)
    assert r["status"] == "FAIL"


def test_evaluate_research_area_pass(browser_smoke_mod):
    data = {
        "status": "ok",
        "roles": [
            {"role_name": "Holistik Researcher", "area": "Research"},
            {"role_name": "Lead Researcher", "area": "Research"},
        ],
    }
    r = browser_smoke_mod.evaluate_scenario0_research_area_payload(data)
    assert r["status"] == "PASS"


def test_evaluate_research_area_bad_area(browser_smoke_mod):
    data = {
        "status": "ok",
        "roles": [
            {"role_name": "Holistik Researcher", "area": "Research"},
            {"role_name": "CFO", "area": "Finance"},
        ],
    }
    r = browser_smoke_mod.evaluate_scenario0_research_area_payload(data)
    assert r["status"] == "FAIL"


def test_evaluate_kirbe_children_pass(browser_smoke_mod):
    data = {
        "status": "ok",
        "processes": [
            {"item_name": "KiRBe Security and Governance"},
            {"item_name": "KiRBe Multi-Source Connector Setup"},
            {"item_name": "KiRBe Reader Operations (per source)"},
        ],
    }
    r = browser_smoke_mod.evaluate_scenario0_kirbe_children_payload(data)
    assert r["status"] == "PASS"


def test_evaluate_kirbe_children_missing(browser_smoke_mod):
    data = {"status": "ok", "processes": [{"item_name": "KiRBe Security and Governance"}]}
    r = browser_smoke_mod.evaluate_scenario0_kirbe_children_payload(data)
    assert r["status"] == "FAIL"


def test_evaluate_admin_escalation_pass(browser_smoke_mod):
    r = browser_smoke_mod.evaluate_scenario0_admin_escalation_payload(
        {"route": "admin_escalate", "must_escalate": True}
    )
    assert r["status"] == "PASS"
