"""Map DATA_CONTRACT_REGISTRY rows to ODCS v3.1.0 documents (Initiative 93 P3).

Holistika git CSV remains SSOT; ODCS YAML is the **tool projection** for OpenMetadata
import/validate (see DATA_CATALOG_INTEGRATION_POSTURE.md).
"""

from __future__ import annotations

from typing import Any

from akos.hlk_data_contract_csv import DataContractRegistryRow

ODCS_API_VERSION = "v3.1.0"
ODCS_KIND = "DataContract"

_SURFACE_SERVER_TYPE: dict[str, str] = {
    "canonical_csv": "git",
    "mirror_table": "postgres",
    "fdw_projection": "postgres",
    "graph": "neo4j",
}


def _parse_sla_freshness(raw: str) -> list[dict[str, Any]]:
    text = (raw or "").strip()
    if not text:
        return []
    lowered = text.lower()
    if lowered.endswith("h"):
        try:
            value = int(lowered[:-1])
            return [{
                "property": "latency",
                "value": value,
                "unit": "hour",
                "driver": "operational",
            }]
        except ValueError:
            pass
    if lowered == "quarterly":
        return [{
            "property": "frequency",
            "value": "quarterly",
            "unit": "calendar",
            "driver": "regulatory",
        }]
    return [{
        "property": "frequency",
        "value": text,
        "unit": "unspecified",
        "driver": "operational",
    }]


def _parse_sla_availability(raw: str) -> list[dict[str, Any]]:
    text = (raw or "").strip()
    if not text:
        return []
    return [{
        "property": "availability",
        "value": text,
        "unit": "percent",
        "driver": "operational",
    }]


def _quality_rules(rules: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for code in (rules or "").split(";"):
        code = code.strip()
        if not code:
            continue
        out.append({
            "type": "custom",
            "description": f"Holistika DataOps dimension {code}",
            "rule": code,
        })
    return out


def contract_row_to_odcs(row: DataContractRegistryRow | dict[str, str]) -> dict[str, Any]:
    """Return an ODCS v3.1-shaped dict for one registry row."""
    if isinstance(row, dict):
        row = DataContractRegistryRow.model_validate(row)

    surface = row.data_surface
    server_type = _SURFACE_SERVER_TYPE.get(surface, "custom")
    schema_name = row.schema_ref.rsplit("/", 1)[-1].replace(".csv", "").replace(".md", "")

    sla_props = _parse_sla_freshness(row.sla_freshness) + _parse_sla_availability(row.sla_availability)

    doc: dict[str, Any] = {
        "kind": ODCS_KIND,
        "apiVersion": ODCS_API_VERSION,
        "id": row.contract_id,
        "info": {
            "title": row.contract_id,
            "version": row.version,
            "status": row.status,
            "description": row.semantics_ref or row.notes or "",
        },
        "team": {
            "name": row.owner_role,
            "members": [],
        },
        "servers": {
            "production": {
                "type": server_type,
                "location": row.schema_ref,
                "environment": surface,
            },
        },
        "schema": [
            {
                "name": schema_name,
                "physicalType": surface,
                "description": row.schema_ref,
            },
        ],
        "quality": _quality_rules(row.quality_rules),
        "terms": {
            "usage": f"Producer process {row.producer_process_id} ({row.producer_area}); "
            f"consumers: {row.consumer_area_ids}",
        },
    }
    if sla_props:
        doc["slaProperties"] = sla_props
    if row.classification:
        doc["info"]["classification"] = row.classification
    if row.retention_policy_ref:
        doc["info"]["retentionPolicyRef"] = row.retention_policy_ref
    return doc


def validate_odcs_document(doc: dict[str, Any]) -> list[str]:
    """Structural check without external JSON Schema download."""
    errors: list[str] = []
    for key in ("kind", "apiVersion", "id", "info", "servers", "schema"):
        if key not in doc:
            errors.append(f"missing required key {key!r}")
    if doc.get("kind") != ODCS_KIND:
        errors.append(f"kind must be {ODCS_KIND!r}")
    if doc.get("apiVersion") != ODCS_API_VERSION:
        errors.append(f"apiVersion must be {ODCS_API_VERSION!r}")
    info = doc.get("info")
    if not isinstance(info, dict) or not info.get("title"):
        errors.append("info.title required")
    return errors
