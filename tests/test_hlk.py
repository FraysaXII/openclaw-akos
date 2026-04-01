"""Tests for HLK domain models, registry service, and API endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from akos.api import app
from akos.hlk import HlkRegistry, get_hlk_registry
from akos.models import HlkResponse, OrgRole, ProcessItem


client = TestClient(app)


class TestHlkModels:
    """Validate that Pydantic models parse real CSV-shaped data."""

    def test_org_role_parses(self):
        role = OrgRole.model_validate({
            "org_uuid": "abc-123",
            "role_name": "Admin",
            "role_description": "Administrator",
            "access_level": 6,
            "reports_to": "Admin",
            "area": "Admin",
            "entity": "Holistika",
        })
        assert role.role_name == "Admin"
        assert role.access_level == 6

    def test_process_item_parses(self):
        item = ProcessItem.model_validate({
            "type": "Internal",
            "orientation": "Employee",
            "entity": "Holistika",
            "area": "Research",
            "role_parent_1": "Holistik Researcher",
            "role_owner": "Lead Researcher",
            "item_parent_1": "Research Techniques",
            "item_name": "HxPESTAL",
            "item_id": "hol_resea_dtp_99",
            "item_granularity": "process",
        })
        assert item.item_id == "hol_resea_dtp_99"
        assert item.item_granularity == "process"

    def test_hlk_response_envelope(self):
        resp = HlkResponse(status="ok", role_count=5)
        assert resp.status == "ok"
        assert resp.warnings == []

    def test_hlk_response_not_found(self):
        resp = HlkResponse(status="not_found", error_detail="test")
        assert resp.error_detail == "test"


class TestHlkRegistry:
    """Test registry lookups against the real canonical CSVs."""

    @pytest.fixture(autouse=True)
    def registry(self):
        self.reg = get_hlk_registry()

    def test_loads_roles(self):
        assert len(self.reg._roles) > 0

    def test_loads_processes(self):
        assert len(self.reg._processes) > 0

    def test_role_lookup_found(self):
        resp = self.reg.get_role("Admin")
        assert resp.status == "ok"
        assert resp.roles is not None
        assert resp.roles[0].role_name == "Admin"

    def test_role_lookup_not_found(self):
        resp = self.reg.get_role("NonexistentRole")
        assert resp.status == "not_found"

    def test_role_chain(self):
        resp = self.reg.get_role_chain("DevOPS")
        assert resp.status == "ok"
        assert len(resp.roles) >= 2
        names = [r.role_name for r in resp.roles]
        assert "DevOPS" in names
        assert "CTO" in names

    def test_area_roles(self):
        resp = self.reg.get_area_roles("Research")
        assert resp.status == "ok"
        assert resp.role_count >= 4

    def test_list_areas(self):
        resp = self.reg.list_areas()
        assert resp.status == "ok"
        area_names = [r.role_name for r in resp.roles]
        assert "Research" in area_names
        assert "Tech" in area_names

    def test_process_lookup(self):
        resp = self.reg.get_process("hol_resea_prj_1")
        assert resp.status == "ok"
        assert resp.processes[0].item_name == "Holistika Research and Methodology"

    def test_process_tree(self):
        resp = self.reg.get_process_tree("Holistika Research and Methodology")
        assert resp.status == "ok"
        assert resp.process_count >= 5

    def test_project_summary(self):
        resp = self.reg.get_project_summary()
        assert resp.status == "ok"
        assert resp.process_count == 11

    def test_gaps(self):
        resp = self.reg.get_gaps()
        assert resp.status == "ok"

    def test_search_roles(self):
        resp = self.reg.search("engineer")
        assert resp.status == "ok"
        assert resp.role_count >= 1

    def test_search_processes(self):
        resp = self.reg.search("MADEIRA")
        assert resp.status == "ok"
        assert resp.process_count >= 1

    def test_search_not_found(self):
        resp = self.reg.search("zzzznonexistentzzzz")
        assert resp.status == "not_found"


class TestHlkApi:
    """Test FastAPI endpoints via TestClient."""

    def test_hlk_roles(self):
        r = client.get("/hlk/roles")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert data["role_count"] > 0

    def test_hlk_role_by_name(self):
        r = client.get("/hlk/roles/CTO")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_hlk_role_chain(self):
        r = client.get("/hlk/roles/DevOPS/chain")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert len(data["roles"]) >= 2

    def test_hlk_areas(self):
        r = client.get("/hlk/areas")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_hlk_area_roles(self):
        r = client.get("/hlk/areas/Tech")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_hlk_projects(self):
        r = client.get("/hlk/processes")
        assert r.status_code == 200
        data = r.json()
        assert data["process_count"] == 11

    def test_hlk_process_by_id(self):
        r = client.get("/hlk/processes/hol_resea_prj_1")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_hlk_gaps(self):
        r = client.get("/hlk/gaps")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_hlk_search(self):
        r = client.get("/hlk/search", params={"q": "research"})
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_hlk_search_empty(self):
        r = client.get("/hlk/search", params={"q": ""})
        assert r.status_code == 400
