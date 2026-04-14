"""Tests for HLK domain models, registry service, and API endpoints."""

from __future__ import annotations

import csv

import pytest
from fastapi.testclient import TestClient

from akos.api import app
from akos.hlk import HlkRegistry, get_hlk_registry
from akos.hlk_process_csv import item_name_uniqueness_errors
from akos.io import REPO_ROOT
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

    def test_role_lookup_case_insensitive(self):
        resp = self.reg.get_role("cto")
        assert resp.status == "ok"
        assert resp.best_role is not None
        assert resp.best_role.role_name == "CTO"

    def test_role_lookup_resolves_full_title_alias(self):
        resp = self.reg.get_role("Chief Technology Officer")
        assert resp.status == "ok"
        assert resp.best_role is not None
        assert resp.best_role.role_name == "CTO"

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

    def test_process_lookup_normalized_id(self):
        resp = self.reg.get_process("HOL_RESEA_PRJ_1")
        assert resp.status == "ok"
        assert resp.best_process is not None
        assert resp.best_process.item_id == "hol_resea_prj_1"

    def test_process_tree(self):
        resp = self.reg.get_process_tree("Holistika Research and Methodology")
        assert resp.status == "ok"
        assert resp.process_count >= 5

    def test_process_tree_prefers_parent_id_index(self):
        """Name-based tree should use item_parent_1_id children when present."""
        resp = self.reg.get_process_tree("MADEIRA Platform")
        assert resp.status == "ok"
        assert resp.resolution_strategy == "item_parent_1_id_exact"
        assert resp.process_count >= 1

    def test_process_tree_by_parent_id(self):
        madeira = self.reg.get_process("env_tech_prj_3")
        assert madeira.status == "ok" and madeira.best_process is not None
        pid = madeira.best_process.item_id
        resp = self.reg.get_process_tree_by_parent_id(pid)
        assert resp.status == "ok"
        assert resp.process_count >= 1
        assert all((c.item_parent_1_id or "").strip() == pid for c in (resp.processes or []))

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

    def test_search_returns_best_role_for_exact_title(self):
        resp = self.reg.search("CTO")
        assert resp.status == "ok"
        assert resp.best_role is not None
        assert resp.best_role.role_name == "CTO"
        assert resp.roles is not None
        assert resp.roles[0].role_name == "CTO"
        assert resp.resolution_strategy

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

    def test_hlk_role_by_title_alias(self):
        r = client.get("/hlk/roles/Chief%20Technology%20Officer")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert data["best_role"]["role_name"] == "CTO"

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

    def test_hlk_process_tree_by_parent_id_route(self):
        r = client.get("/hlk/processes/id/env_tech_prj_3/tree")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert data["process_count"] >= 1

    def test_hlk_gaps(self):
        r = client.get("/hlk/gaps")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_hlk_search(self):
        r = client.get("/hlk/search", params={"q": "research"})
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_hlk_search_returns_best_role(self):
        r = client.get("/hlk/search", params={"q": "CTO"})
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert data["best_role"]["role_name"] == "CTO"

    def test_hlk_search_empty(self):
        r = client.get("/hlk/search", params={"q": ""})
        assert r.status_code == 400


class TestHlkIntegrity:
    """Validate canonical vault referential and graph integrity."""

    @pytest.fixture(autouse=True)
    def registry(self):
        self.reg = get_hlk_registry()

    def test_no_broken_parent_refs(self):
        names = {p.item_name for p in self.reg._processes}
        for p in self.reg._processes:
            if p.item_parent_1:
                assert p.item_parent_1 in names, f"{p.item_id}: parent '{p.item_parent_1}' not found"

    def test_no_orphan_items(self):
        for p in self.reg._processes:
            if p.item_granularity != "project":
                assert p.item_parent_1, f"{p.item_id}: non-project without item_parent_1"

    def test_role_owner_resolves(self):
        role_names = {r.role_name for r in self.reg._roles}
        alias_owners = {"Process Owner", "TBD"}
        for p in self.reg._processes:
            if p.role_owner and p.role_owner not in alias_owners:
                assert p.role_owner in role_names, f"{p.item_id}: role_owner '{p.role_owner}' not in org"

    def test_no_duplicate_item_ids(self):
        ids = [p.item_id for p in self.reg._processes if p.item_id]
        assert len(ids) == len(set(ids)), f"Duplicate item_ids: {[i for i in ids if ids.count(i) > 1]}"

    def test_no_duplicate_org_ids(self):
        ids = [r.org_id for r in self.reg._roles if r.org_id]
        assert len(ids) == len(set(ids)), f"Duplicate org_ids: {[i for i in ids if ids.count(i) > 1]}"

    def test_valid_granularity_values(self):
        valid = {"project", "workstream", "process", "task"}
        for p in self.reg._processes:
            if p.item_granularity:
                assert p.item_granularity in valid, f"{p.item_id}: invalid granularity '{p.item_granularity}'"

    def test_program_layer_rows_exist(self):
        """Pattern 3: MADEIRA and Think Big program workstreams (hlk_prog_*)."""
        ids = {p.item_id for p in self.reg._processes}
        assert "hlk_prog_madeira_product_research" in ids
        assert "hlk_prog_madeira_engineering_ux" in ids
        assert "hlk_prog_think_big_pmo" in ids
        by_id = {p.item_id: p for p in self.reg._processes}
        pr = by_id["hlk_prog_madeira_product_research"]
        assert pr.item_granularity == "workstream"
        assert pr.item_parent_1 == "MADEIRA Platform" and pr.item_parent_2 == "MADEIRA Platform"
        ws = by_id["gtm_ws_madeira_radar"]
        assert "MADEIRA product and research program" in (ws.item_parent_1, ws.item_parent_2)

    def test_gtm_rows_have_resolved_parent_chain(self):
        """Policy: promoted GTM rows keep a two-hop parent chain (p2 workstream or project, p1 cluster or process)."""
        names = {p.item_name for p in self.reg._processes if p.item_name}
        for p in self.reg._processes:
            if not (p.item_id or "").startswith("gtm_"):
                continue
            if (p.item_granularity or "").strip() == "project":
                continue
            assert (p.item_parent_2 or "").strip(), f"{p.item_id}: GTM row missing item_parent_2"
            assert p.item_parent_2 in names, f"{p.item_id}: item_parent_2 not in item_name set"
            assert (p.item_parent_1 or "").strip(), f"{p.item_id}: GTM row missing item_parent_1"
            assert p.item_parent_1 in names, f"{p.item_id}: item_parent_1 not in item_name set"


class TestHlkProvenance:
    """Verify structural provenance of the canonical vault."""

    @pytest.fixture(autouse=True)
    def registry(self):
        self.reg = get_hlk_registry()

    def test_org_csv_loaded(self):
        assert len(self.reg._roles) >= 60

    def test_proc_csv_loaded(self):
        assert len(self.reg._processes) >= 300

    def test_all_projects_have_children(self):
        projects = [p for p in self.reg._processes if p.item_granularity == "project"]
        for proj in projects:
            children = self.reg._processes_by_parent.get(proj.item_name, [])
            assert len(children) > 0, f"Project '{proj.item_name}' has no children"

    def test_all_areas_have_roles(self):
        areas = {r.area for r in self.reg._roles}
        assert len(areas) >= 10
        for area in areas:
            roles_in_area = [r for r in self.reg._roles if r.area == area]
            assert len(roles_in_area) > 0, f"Area '{area}' has no roles"

    def test_research_area_exists(self):
        research_roles = [r for r in self.reg._roles if r.area == "Research"]
        assert len(research_roles) >= 7

    def test_eleven_projects(self):
        projects = [p for p in self.reg._processes if p.item_granularity == "project"]
        assert len(projects) == 11

    def test_canonical_process_list_has_no_ambiguous_item_names(self):
        """Duplicate item_name values block parent-id resolution; canonical data must have none."""
        proc_csv = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"
        assert proc_csv.is_file()
        with proc_csv.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        errs = item_name_uniqueness_errors(rows)
        assert not errs, errs[:10]


class TestHlkApiEdgeCases:
    """Test API edge cases and input safety."""

    def test_role_with_special_chars(self):
        r = client.get("/hlk/roles/Ethics%20%26%20Learning")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_role_not_found_graceful(self):
        r = client.get("/hlk/roles/../../../../etc/passwd")
        assert r.status_code in (200, 404)

    def test_area_case_insensitive(self):
        r = client.get("/hlk/areas/research")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_search_special_chars(self):
        r = client.get("/hlk/search", params={"q": "<script>alert(1)</script>"})
        assert r.status_code == 200
        assert r.json()["status"] == "not_found"

    def test_process_tree_not_found(self):
        r = client.get("/hlk/processes/nonexistent/tree")
        assert r.status_code == 200
        assert r.json()["status"] == "not_found"
