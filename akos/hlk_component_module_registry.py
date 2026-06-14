"""Pydantic SSOT for COMPONENT_MODULE_REGISTRY.csv (I100 / D-IH-100-C).

Classifies every COMPONENT_SERVICE_MATRIX row into governance depth D0–D3 and
links optional dimension registries. Used by validate_component_module_registry.py.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

GovernanceDepth = Literal["D0", "D1", "D2", "D3"]
GovernedStatus = Literal[
    "governed", "partial", "ungoverned", "inventory", "alias", "forward"
]
VolatilityClass = Literal["high", "medium", "low", "n_a"]
Priority = Literal["critical", "high", "medium", "low", "forward"]


class ComponentModuleRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    module_id: str = Field(min_length=1, max_length=40)
    component_id: str = Field(min_length=1, max_length=60)
    module_name: str = Field(min_length=1, max_length=120)
    module_family: str = Field(min_length=1, max_length=60)
    governed_status: GovernedStatus
    governance_depth: GovernanceDepth
    dimension_registry_path: str = Field(default="", max_length=300)
    doc_url: str = Field(default="", max_length=400)
    volatility_class: VolatilityClass
    next_verify_by: str = Field(default="", max_length=20)
    gap: str = Field(default="", max_length=300)
    owner_role: str = Field(min_length=1, max_length=60)
    priority: Priority
    notes: str = Field(default="", max_length=400)

    @field_validator("module_id")
    @classmethod
    def id_shape(cls, v: str) -> str:
        if not v.startswith("COMP-MOD-"):
            raise ValueError("module_id must start with COMP-MOD-")
        return v

    @field_validator("component_id")
    @classmethod
    def component_fk(cls, v: str) -> str:
        if not (v.startswith("comp_matriz_") or v.startswith("comp_i93_")):
            raise ValueError("component_id must be a matrix FK (comp_matriz_* or comp_i93_*)")
        return v


FIELDNAMES = (
    "module_id",
    "component_id",
    "module_name",
    "module_family",
    "governed_status",
    "governance_depth",
    "dimension_registry_path",
    "doc_url",
    "volatility_class",
    "next_verify_by",
    "gap",
    "owner_role",
    "priority",
    "notes",
)

# Canonical matrix rows (non-alias) for D3 ecosystem families.
D3_CANONICAL: dict[str, str] = {
    "comp_matriz_00008": "supabase",
    "comp_matriz_00015": "vercel",
    "comp_matriz_00087": "cloudflare",
    "comp_matriz_00023": "github",
    "comp_matriz_00004": "openclaw_akos",
    "comp_i93_openclaw_akos": "openclaw_akos",
}

ALIAS_OF: dict[str, str] = {
    "comp_matriz_00009": "comp_matriz_00008",
    "comp_matriz_00048": "comp_matriz_00008",
    "comp_matriz_00052": "comp_matriz_00008",
    "comp_matriz_00053": "comp_matriz_00008",
    "comp_matriz_00054": "comp_matriz_00008",
    "comp_matriz_00026": "comp_matriz_00023",
    "comp_matriz_00064": "comp_matriz_00015",
    "comp_matriz_00065": "comp_matriz_00015",
    "comp_matriz_00088": "comp_matriz_00087",
    "comp_matriz_00089": "comp_matriz_00087",
    "comp_matriz_00090": "comp_matriz_00087",
}

D2_COMPONENTS: dict[str, str] = {
    "comp_i93_hlk_erp": "vercel",
    "comp_i93_sentry": "sentry",
    "comp_i93_langfuse": "langfuse",
    "comp_matriz_00005": "make",
    "comp_matriz_00011": "n8n",
    "comp_matriz_00085": "stripe",
}

D1_KEYWORDS = (
    "perplexity",
    "notebooklm",
    "huggingface",
    "runpod",
    "openai",
    "anthropic",
    "gemini",
    "cursor",
    "figma",
    "notion",
    "obsidian",
    "research",
    "ai ",
    "llm",
    "copilot",
)

DIMENSION_REGISTRY_BY_FAMILY: dict[str, str] = {
    "vercel": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/VERCEL_PROJECT_SETTINGS_REGISTRY.csv"
    ),
    "cloudflare": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/CLOUDFLARE_ZONE_SURFACE_REGISTRY.csv"
    ),
    "github": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/GITHUB_REPO_CI_POSTURE_REGISTRY.csv"
    ),
    "supabase": (
        "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
        "dimensions/SUPABASE_MODULE_REGISTRY.csv"
    ),
    "sentry": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/SENTRY_PROJECT_POSTURE_REGISTRY.csv"
    ),
    "langfuse": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/LANGFUSE_PROJECT_POSTURE_REGISTRY.csv"
    ),
    "stripe": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/STRIPE_INTEGRATION_POSTURE_REGISTRY.csv"
    ),
    "make": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/MAKE_SCENARIO_POSTURE_REGISTRY.csv"
    ),
    "n8n": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/N8N_WORKFLOW_POSTURE_REGISTRY.csv"
    ),
    "render": (
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/"
        "dimensions/RENDER_SERVICE_POSTURE_REGISTRY.csv"
    ),
}

DOC_URL_BY_FAMILY: dict[str, str] = {
    "vercel": "https://vercel.com/docs",
    "cloudflare": "https://developers.cloudflare.com/dns/",
    "github": "https://docs.github.com/en/actions",
    "supabase": "https://supabase.com/docs",
    "openclaw_akos": "docs/ARCHITECTURE.md",
    "sentry": "https://docs.sentry.io/",
    "langfuse": "https://langfuse.com/docs",
    "stripe": "https://docs.stripe.com/",
    "make": "https://www.make.com/en/help",
    "n8n": "https://docs.n8n.io/",
}
