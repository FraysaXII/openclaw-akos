"""HLK domain registry service for AKOS.

Provides typed lookups over the canonical HLK compliance baselines:
baseline_organisation.csv and process_list.csv. All provider-specific
details are hidden behind normalised Pydantic models so the API layer,
MCP tools, and tests share a stable contract.

The vault CSVs are the database. No external DB dependency is required.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from akos.io import REPO_ROOT
from akos.models import HlkResponse, OrgRole, ProcessItem

logger = logging.getLogger("akos.hlk")

HLK_COMPLIANCE_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
ORG_CSV = HLK_COMPLIANCE_DIR / "baseline_organisation.csv"
PROCESS_CSV = HLK_COMPLIANCE_DIR / "process_list.csv"


def _load_csv(path: Path, model_cls: type) -> list:
    """Load a CSV into a list of Pydantic model instances."""
    if not path.exists():
        logger.warning("HLK CSV not found: %s", path)
        return []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            cleaned = {k: (v or "") for k, v in row.items() if k is not None}
            try:
                rows.append(model_cls.model_validate(cleaned))
            except Exception as exc:
                logger.debug("Skipping row %s: %s", row.get("item_id") or row.get("role_name"), exc)
        return rows


class HlkRegistry:
    """In-memory registry over the HLK canonical vault CSVs.

    Loads baseline_organisation.csv and process_list.csv on first access
    and builds lookup indexes for fast typed queries.
    """

    def __init__(self) -> None:
        self._roles: list[OrgRole] = _load_csv(ORG_CSV, OrgRole)
        self._processes: list[ProcessItem] = _load_csv(PROCESS_CSV, ProcessItem)

        self._roles_by_name: dict[str, OrgRole] = {r.role_name: r for r in self._roles}
        self._processes_by_id: dict[str, ProcessItem] = {p.item_id: p for p in self._processes}
        self._processes_by_parent: dict[str, list[ProcessItem]] = {}
        for p in self._processes:
            if p.item_parent_1:
                self._processes_by_parent.setdefault(p.item_parent_1, []).append(p)

        logger.info("HLK registry loaded: %d roles, %d processes", len(self._roles), len(self._processes))

    def get_role(self, role_name: str) -> HlkResponse:
        """Look up a single role by name."""
        role = self._roles_by_name.get(role_name)
        if role is None:
            return HlkResponse(status="not_found", error_detail=f"Role '{role_name}' not found")
        return HlkResponse(status="ok", roles=[role])

    def get_role_chain(self, role_name: str) -> HlkResponse:
        """Traverse the reports_to chain from a role up to Admin."""
        chain: list[OrgRole] = []
        visited: set[str] = set()
        current = role_name
        while current and current not in visited:
            visited.add(current)
            role = self._roles_by_name.get(current)
            if role is None:
                break
            chain.append(role)
            if role.reports_to == current:
                break
            current = role.reports_to
        if not chain:
            return HlkResponse(status="not_found", error_detail=f"Role '{role_name}' not found")
        return HlkResponse(status="ok", roles=chain)

    def get_area_roles(self, area: str) -> HlkResponse:
        """Return all roles in a given area."""
        matches = [r for r in self._roles if r.area.lower() == area.lower()]
        if not matches:
            return HlkResponse(status="not_found", error_detail=f"No roles in area '{area}'")
        return HlkResponse(status="ok", roles=matches, role_count=len(matches))

    def list_areas(self) -> HlkResponse:
        """Return a summary of all areas with role counts."""
        area_counts: dict[str, int] = {}
        for r in self._roles:
            area_counts[r.area] = area_counts.get(r.area, 0) + 1
        summary_roles = [
            OrgRole(role_name=area, role_description=f"{count} roles", access_level=0, area=area)
            for area, count in sorted(area_counts.items())
        ]
        return HlkResponse(status="ok", roles=summary_roles, role_count=len(self._roles))

    def get_process(self, item_id: str) -> HlkResponse:
        """Look up a single process item by ID."""
        proc = self._processes_by_id.get(item_id)
        if proc is None:
            return HlkResponse(status="not_found", error_detail=f"Process '{item_id}' not found")
        return HlkResponse(status="ok", processes=[proc])

    def get_process_tree(self, item_name: str) -> HlkResponse:
        """Return all direct children of a process item by parent name."""
        children = self._processes_by_parent.get(item_name, [])
        if not children:
            return HlkResponse(status="not_found", error_detail=f"No children under '{item_name}'")
        return HlkResponse(status="ok", processes=children, process_count=len(children))

    def get_project_summary(self) -> HlkResponse:
        """Return all projects with their direct child counts."""
        projects = [p for p in self._processes if p.item_granularity == "project"]
        for proj in projects:
            child_count = len(self._processes_by_parent.get(proj.item_name, []))
            proj.description = f"{child_count} direct children"
        return HlkResponse(status="ok", processes=projects, process_count=len(projects))

    def get_gaps(self) -> HlkResponse:
        """Identify items with missing metadata, TBD owners, or empty descriptions."""
        gap_items: list[ProcessItem] = []
        gap_warnings: list[str] = []
        for p in self._processes:
            issues: list[str] = []
            if p.role_owner in ("TBD", "Process Owner", ""):
                issues.append("unassigned_owner")
            if not p.description and p.item_granularity in ("process", "task"):
                issues.append("missing_description")
            if not p.item_parent_1 and p.item_granularity != "project":
                issues.append("orphan")
            if issues:
                gap_items.append(p)
                gap_warnings.append(f"{p.item_id}: {', '.join(issues)}")
        return HlkResponse(
            status="ok",
            processes=gap_items,
            process_count=len(gap_items),
            warnings=gap_warnings,
        )

    def search(self, query: str) -> HlkResponse:
        """Fuzzy search across roles and processes by name, description, or ID."""
        q = query.lower()
        matched_roles = [
            r for r in self._roles
            if q in r.role_name.lower() or q in r.role_description.lower() or q in r.role_full_description.lower()
        ]
        matched_procs = [
            p for p in self._processes
            if q in p.item_name.lower() or q in p.item_id.lower() or q in p.description.lower()
        ]
        if not matched_roles and not matched_procs:
            return HlkResponse(status="not_found", error_detail=f"No results for '{query}'")
        return HlkResponse(
            status="ok",
            roles=matched_roles or None,
            processes=matched_procs or None,
            role_count=len(matched_roles),
            process_count=len(matched_procs),
        )


_registry: HlkRegistry | None = None


def get_hlk_registry() -> HlkRegistry:
    """Return the module-level HLK registry singleton."""
    global _registry
    if _registry is None:
        _registry = HlkRegistry()
    return _registry
