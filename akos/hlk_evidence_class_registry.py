"""Pydantic SSOT for Data Governance EVIDENCE_CLASS_REGISTRY + PROOF_ADAPTER_REGISTRY (I90 P4c+)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

EVIDENCE_CLASS_REGISTRY_CSV_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/EVIDENCE_CLASS_REGISTRY.csv"
)
PROOF_ADAPTER_REGISTRY_CSV_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/PROOF_ADAPTER_REGISTRY.csv"
)
DEPRECATED_EVIDENCE_CLASS_REGISTRY_PATHS: tuple[str, ...] = (
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/"
    "dimensions/EVIDENCE_CLASS_REGISTRY.csv",
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/"
    "dimensions/PROOF_ADAPTER_REGISTRY.csv",
)

EVIDENCE_CLASS_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "binding_id",
    "claim_surface",
    "evidence_class",
    "proof_adapter_id",
    "required_from_iso_date",
    "severity",
    "validator_script",
    "sister_discipline_ref",
    "proof_artifact_kind",
    "proof_path_pattern",
    "owner_role",
    "status",
    "notes",
)

PROOF_ADAPTER_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "adapter_id",
    "adapter_slug",
    "evidence_class",
    "tool_or_vendor",
    "runbook_path",
    "proof_artifact_kind",
    "status",
    "owner_role",
    "notes",
)

CORE_EVIDENCE_CLASSES: frozenset[str] = frozenset(
    {
        "git_shape",
        "url_verify",
        "live_probe",
        "browser_experiential",
        "operator_ratify",
        "meta_regression",
    }
)

VALID_BINDING_STATUSES: frozenset[str] = frozenset({"active", "charter", "retired"})
VALID_ADAPTER_STATUSES: frozenset[str] = frozenset({"active", "charter", "retired"})
VALID_SEVERITIES: frozenset[str] = frozenset({"FAIL", "WARN", "INFO"})


class EvidenceClassRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    binding_id: str = Field(pattern=r"^ECB-\d{4}$")
    claim_surface: str = Field(min_length=1, max_length=80)
    evidence_class: str = Field(min_length=1, max_length=80)
    proof_adapter_id: str = ""
    required_from_iso_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    severity: str
    validator_script: str = Field(min_length=1, max_length=120)
    sister_discipline_ref: str = ""
    proof_artifact_kind: str = Field(min_length=1, max_length=80)
    proof_path_pattern: str = Field(min_length=1, max_length=200)
    owner_role: str = Field(min_length=1, max_length=80)
    status: str
    notes: str = ""


class ProofAdapterRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    adapter_id: str = Field(pattern=r"^PAD-\d{3}$")
    adapter_slug: str = Field(min_length=1, max_length=80)
    evidence_class: str = Field(min_length=1, max_length=80)
    tool_or_vendor: str = Field(min_length=1, max_length=80)
    runbook_path: str = Field(min_length=1, max_length=120)
    proof_artifact_kind: str = Field(min_length=1, max_length=80)
    status: str
    owner_role: str = Field(min_length=1, max_length=80)
    notes: str = ""
