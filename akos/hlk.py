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
import re
from dataclasses import dataclass
from pathlib import Path

from akos.io import REPO_ROOT
from akos.models import HlkResponse, OrgRole, ProcessItem

logger = logging.getLogger("akos.hlk")

HLK_COMPLIANCE_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
ORG_CSV = HLK_COMPLIANCE_DIR / "baseline_organisation.csv"
PROCESS_CSV = HLK_COMPLIANCE_DIR / "process_list.csv"
MAX_SEARCH_RESULTS_PER_TYPE = 8

_MULTISPACE_RE = re.compile(r"\s+")
_ROLE_DESC_SUFFIX_RE = re.compile(r"\s*\(.*?\)\s*")
_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
_QUERY_PREFIX_PATTERNS = (
    re.compile(r"^(?:who|what|which)\s+(?:is|are)\s+", re.IGNORECASE),
    re.compile(r"^(?:show me|find|look up|lookup|search(?:\s+hlk)?\s+for|return|tell me about)\s+", re.IGNORECASE),
)
_LEADING_ARTICLE_RE = re.compile(r"^(?:the|a|an)\s+", re.IGNORECASE)


@dataclass(frozen=True)
class _RankedRole:
    score: int
    reason: str
    role: OrgRole


@dataclass(frozen=True)
class _RankedProcess:
    score: int
    reason: str
    process: ProcessItem


def _clean_role_description(value: str) -> str:
    """Strip non-canonical suffixes from role descriptions for alias matching."""
    if not value:
        return ""
    cleaned = _ROLE_DESC_SUFFIX_RE.sub(" ", value)
    return _MULTISPACE_RE.sub(" ", cleaned).strip()


def _normalize_lookup_key(value: str) -> str:
    """Normalize a user or tool lookup string into a comparison-safe key."""
    normalized = value.strip().strip(" \t\r\n'\"`“”‘’()[]{}<>.,!?;:")
    normalized = normalized.casefold()
    normalized = _MULTISPACE_RE.sub(" ", normalized).strip()
    for pattern in _QUERY_PREFIX_PATTERNS:
        normalized = pattern.sub("", normalized)
    normalized = _LEADING_ARTICLE_RE.sub("", normalized).strip()
    normalized = _NON_ALNUM_RE.sub(" ", normalized)
    return _MULTISPACE_RE.sub(" ", normalized).strip()


def _score_text_match(
    query_key: str,
    target_value: str,
    *,
    exact: int,
    prefix: int,
    contains: int,
    label: str,
) -> tuple[int, str]:
    """Return a score and reason for one normalized query/target pair."""
    target_key = _normalize_lookup_key(target_value)
    if not query_key or not target_key:
        return 0, ""
    if query_key == target_key:
        return exact, f"{label}_exact"
    if target_key.startswith(query_key) or query_key.startswith(target_key):
        return prefix, f"{label}_prefix"
    if query_key in target_key:
        return contains, f"{label}_contains"
    return 0, ""


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
    and builds lookup indexes for deterministic typed queries.
    """

    def __init__(self) -> None:
        self._roles: list[OrgRole] = _load_csv(ORG_CSV, OrgRole)
        self._processes: list[ProcessItem] = _load_csv(PROCESS_CSV, ProcessItem)

        self._roles_by_name: dict[str, OrgRole] = {role.role_name: role for role in self._roles}
        self._roles_by_normalized_name: dict[str, OrgRole] = {}
        self._roles_by_alias: dict[str, OrgRole] = {}
        self._processes_by_id: dict[str, ProcessItem] = {process.item_id: process for process in self._processes}
        self._processes_by_normalized_id: dict[str, ProcessItem] = {}
        self._processes_by_parent: dict[str, list[ProcessItem]] = {}
        self._processes_by_parent_normalized: dict[str, list[ProcessItem]] = {}

        for role in self._roles:
            normalized_name = _normalize_lookup_key(role.role_name)
            if normalized_name and normalized_name not in self._roles_by_normalized_name:
                self._roles_by_normalized_name[normalized_name] = role

            for alias in {
                normalized_name,
                _normalize_lookup_key(_clean_role_description(role.role_description)),
            }:
                if alias and alias not in self._roles_by_alias:
                    self._roles_by_alias[alias] = role

        for process in self._processes:
            normalized_id = _normalize_lookup_key(process.item_id)
            if normalized_id and normalized_id not in self._processes_by_normalized_id:
                self._processes_by_normalized_id[normalized_id] = process

            if process.item_parent_1:
                self._processes_by_parent.setdefault(process.item_parent_1, []).append(process)
                parent_key = _normalize_lookup_key(process.item_parent_1)
                if parent_key:
                    self._processes_by_parent_normalized.setdefault(parent_key, []).append(process)

        logger.info("HLK registry loaded: %d roles, %d processes", len(self._roles), len(self._processes))

    def get_role(self, role_name: str) -> HlkResponse:
        """Look up a single role by canonical name or normalized title alias."""
        role, normalized_query, strategy = self._resolve_role(role_name)
        if role is None:
            return HlkResponse(
                status="not_found",
                normalized_query=normalized_query,
                error_detail=f"Role '{role_name}' not found",
            )
        return HlkResponse(
            status="ok",
            roles=[role],
            best_role=role,
            role_count=1,
            normalized_query=normalized_query,
            resolution_strategy=strategy,
        )

    def get_role_chain(self, role_name: str) -> HlkResponse:
        """Traverse the reports_to chain from a role up to Admin."""
        start_role, normalized_query, strategy = self._resolve_role(role_name)
        if start_role is None:
            return HlkResponse(
                status="not_found",
                normalized_query=normalized_query,
                error_detail=f"Role '{role_name}' not found",
            )

        chain: list[OrgRole] = []
        visited: set[str] = set()
        current = start_role.role_name
        while current and current not in visited:
            visited.add(current)
            role = self._roles_by_name.get(current)
            if role is None:
                break
            chain.append(role)
            if role.reports_to == current:
                break
            current = role.reports_to

        return HlkResponse(
            status="ok",
            roles=chain,
            best_role=chain[0] if chain else None,
            role_count=len(chain),
            normalized_query=normalized_query,
            resolution_strategy=f"{strategy};chain_traversal",
        )

    def get_area_roles(self, area: str) -> HlkResponse:
        """Return all roles in a given area."""
        normalized_query = _normalize_lookup_key(area)
        matches = [role for role in self._roles if _normalize_lookup_key(role.area) == normalized_query]
        if not matches:
            return HlkResponse(
                status="not_found",
                normalized_query=normalized_query,
                error_detail=f"No roles in area '{area}'",
            )
        return HlkResponse(status="ok", roles=matches, role_count=len(matches), normalized_query=normalized_query)

    def list_areas(self) -> HlkResponse:
        """Return a summary of all areas with role counts."""
        area_counts: dict[str, int] = {}
        for role in self._roles:
            area_counts[role.area] = area_counts.get(role.area, 0) + 1
        summary_roles = [
            OrgRole(role_name=area, role_description=f"{count} roles", access_level=0, area=area)
            for area, count in sorted(area_counts.items())
        ]
        return HlkResponse(status="ok", roles=summary_roles, role_count=len(self._roles))

    def get_process(self, item_id: str) -> HlkResponse:
        """Look up a single process item by canonical item ID."""
        normalized_query = _normalize_lookup_key(item_id)
        process = self._processes_by_id.get(item_id) or self._processes_by_normalized_id.get(normalized_query)
        if process is None:
            return HlkResponse(
                status="not_found",
                normalized_query=normalized_query,
                error_detail=f"Process '{item_id}' not found",
            )
        strategy = "item_id_exact" if process.item_id == item_id else "item_id_normalized"
        return HlkResponse(
            status="ok",
            processes=[process],
            best_process=process,
            process_count=1,
            normalized_query=normalized_query,
            resolution_strategy=strategy,
        )

    def get_process_tree(self, item_name: str) -> HlkResponse:
        """Return all direct children of a process item by parent name."""
        normalized_query = _normalize_lookup_key(item_name)
        children = self._processes_by_parent.get(item_name, [])
        strategy = "item_parent_exact"
        if not children:
            children = self._processes_by_parent_normalized.get(normalized_query, [])
            strategy = "item_parent_normalized"
        if not children:
            return HlkResponse(
                status="not_found",
                normalized_query=normalized_query,
                error_detail=f"No children under '{item_name}'",
            )
        return HlkResponse(
            status="ok",
            processes=children,
            process_count=len(children),
            normalized_query=normalized_query,
            resolution_strategy=strategy,
        )

    def get_project_summary(self) -> HlkResponse:
        """Return all projects with their direct child counts."""
        projects = [process.model_copy(deep=True) for process in self._processes if process.item_granularity == "project"]
        for project in projects:
            child_count = len(self._processes_by_parent.get(project.item_name, []))
            project.description = f"{child_count} direct children"
        return HlkResponse(status="ok", processes=projects, process_count=len(projects))

    def get_gaps(self) -> HlkResponse:
        """Identify items with missing metadata, TBD owners, or empty descriptions."""
        gap_items: list[ProcessItem] = []
        gap_warnings: list[str] = []
        for process in self._processes:
            issues: list[str] = []
            if process.role_owner in ("TBD", "Process Owner", ""):
                issues.append("unassigned_owner")
            if not process.description and process.item_granularity in ("process", "task"):
                issues.append("missing_description")
            if not process.item_parent_1 and process.item_granularity != "project":
                issues.append("orphan")
            if issues:
                gap_items.append(process)
                gap_warnings.append(f"{process.item_id}: {', '.join(issues)}")
        return HlkResponse(
            status="ok",
            processes=gap_items,
            process_count=len(gap_items),
            warnings=gap_warnings,
        )

    def search(self, query: str) -> HlkResponse:
        """Ranked search across roles and processes by canonical names and descriptions."""
        query_key = _normalize_lookup_key(query)
        if not query_key:
            return HlkResponse(status="not_found", error_detail=f"No results for '{query}'")

        ranked_roles = self._rank_roles(query_key)
        ranked_processes = self._rank_processes(query_key)
        if not ranked_roles and not ranked_processes:
            return HlkResponse(
                status="not_found",
                normalized_query=query_key,
                error_detail=f"No results for '{query}'",
            )

        roles = [entry.role for entry in ranked_roles[:MAX_SEARCH_RESULTS_PER_TYPE]]
        processes = [entry.process for entry in ranked_processes[:MAX_SEARCH_RESULTS_PER_TYPE]]
        warnings: list[str] = []
        if len(ranked_roles) > len(roles):
            warnings.append(
                f"role_results_truncated: showing top {len(roles)} of {len(ranked_roles)} role matches"
            )
        if len(ranked_processes) > len(processes):
            warnings.append(
                f"process_results_truncated: showing top {len(processes)} of {len(ranked_processes)} process matches"
            )

        best_role, role_strategy = self._select_clear_best_role(ranked_roles)
        best_process, process_strategy = self._select_clear_best_process(ranked_processes)
        strategy_parts = [part for part in (role_strategy, process_strategy) if part]
        return HlkResponse(
            status="ok",
            roles=roles or None,
            processes=processes or None,
            best_role=best_role,
            best_process=best_process,
            role_count=len(ranked_roles),
            process_count=len(ranked_processes),
            normalized_query=query_key,
            resolution_strategy=";".join(strategy_parts),
            warnings=warnings,
        )

    def _resolve_role(self, role_name: str) -> tuple[OrgRole | None, str, str]:
        """Resolve a role name via canonical and normalized aliases."""
        if role_name in self._roles_by_name:
            return self._roles_by_name[role_name], _normalize_lookup_key(role_name), "role_name_exact"

        normalized_query = _normalize_lookup_key(role_name)
        if not normalized_query:
            return None, normalized_query, ""

        normalized_match = self._roles_by_normalized_name.get(normalized_query)
        if normalized_match is not None:
            return normalized_match, normalized_query, "role_name_normalized"

        alias_match = self._roles_by_alias.get(normalized_query)
        if alias_match is not None:
            return alias_match, normalized_query, "role_alias_exact"

        return None, normalized_query, ""

    def _rank_roles(self, query_key: str) -> list[_RankedRole]:
        """Return ranked role matches for a normalized search query."""
        ranked: list[_RankedRole] = []
        for role in self._roles:
            score, reason = self._score_role(query_key, role)
            if score:
                ranked.append(_RankedRole(score=score, reason=reason, role=role))
        return sorted(ranked, key=lambda item: (-item.score, item.role.role_name))

    def _score_role(self, query_key: str, role: OrgRole) -> tuple[int, str]:
        """Score one role for a given normalized query."""
        candidates = [
            _score_text_match(query_key, role.role_name, exact=100, prefix=86, contains=72, label="role_name"),
            _score_text_match(
                query_key,
                _clean_role_description(role.role_description),
                exact=96,
                prefix=82,
                contains=62,
                label="role_description",
            ),
            _score_text_match(query_key, role.role_full_description, exact=48, prefix=34, contains=24, label="role_full"),
        ]
        return max(candidates, key=lambda item: item[0])

    def _rank_processes(self, query_key: str) -> list[_RankedProcess]:
        """Return ranked process matches for a normalized search query."""
        ranked: list[_RankedProcess] = []
        for process in self._processes:
            score, reason = self._score_process(query_key, process)
            if score:
                ranked.append(_RankedProcess(score=score, reason=reason, process=process))
        return sorted(ranked, key=lambda item: (-item.score, item.process.item_id, item.process.item_name))

    def _score_process(self, query_key: str, process: ProcessItem) -> tuple[int, str]:
        """Score one process item for a normalized query."""
        candidates = [
            _score_text_match(query_key, process.item_id, exact=100, prefix=90, contains=80, label="item_id"),
            _score_text_match(query_key, process.item_name, exact=96, prefix=84, contains=70, label="item_name"),
            _score_text_match(query_key, process.description, exact=42, prefix=30, contains=22, label="description"),
        ]
        return max(candidates, key=lambda item: item[0])

    def _select_clear_best_role(self, ranked_roles: list[_RankedRole]) -> tuple[OrgRole | None, str]:
        """Return a clear role winner when the ranking is sufficiently decisive."""
        if not ranked_roles:
            return None, ""
        top = ranked_roles[0]
        if top.score >= 95:
            return top.role, top.reason
        if len(ranked_roles) == 1 and top.score >= 70:
            return top.role, top.reason
        if top.score >= 80 and top.score - ranked_roles[1].score >= 15:
            return top.role, top.reason
        return None, ""

    def _select_clear_best_process(self, ranked_processes: list[_RankedProcess]) -> tuple[ProcessItem | None, str]:
        """Return a clear process winner when the ranking is sufficiently decisive."""
        if not ranked_processes:
            return None, ""
        top = ranked_processes[0]
        if top.score >= 95:
            return top.process, top.reason
        if len(ranked_processes) == 1 and top.score >= 70:
            return top.process, top.reason
        if top.score >= 80 and top.score - ranked_processes[1].score >= 15:
            return top.process, top.reason
        return None, ""


_registry: HlkRegistry | None = None


def get_hlk_registry() -> HlkRegistry:
    """Return the module-level HLK registry singleton."""
    global _registry
    if _registry is None:
        _registry = HlkRegistry()
    return _registry
