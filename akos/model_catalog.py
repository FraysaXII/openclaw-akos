"""Model catalog: SSOT mapping HuggingFace models to GPU/vLLM/OpenClaw config.

Each entry specifies the VRAM footprint, recommended GPU, vLLM tool-call and
reasoning parsers, and the OpenClaw served-model name so that ``scripts/gpu.py``
can auto-configure everything from a single model selection.
"""

from __future__ import annotations

import math
from pathlib import Path

from pydantic import BaseModel, Field

from akos.io import REPO_ROOT

_CATALOG_PATH = REPO_ROOT / "config" / "model-catalog.json"


class GpuDefault(BaseModel):
    type: str
    count: int = Field(ge=1)


class CatalogEntry(BaseModel):
    hfId: str
    displayName: str
    family: str
    paramsBillions: int = Field(gt=0)
    vramGb: int = Field(gt=0)
    toolCallParser: str
    reasoningParser: str | None = None
    chatTemplate: str | None = None
    servedModelName: str
    reasoning: bool = False
    defaultGpu: GpuDefault
    maxModelLen: int = Field(default=131072, gt=0)
    envOverrides: dict[str, str] = Field(default_factory=dict)

    def min_gpus_for(self, gpu_vram: int) -> int:
        """Minimum GPU count to fit this model on GPUs with *gpu_vram* GB each."""
        return max(1, math.ceil(self.vramGb / gpu_vram))


def load_catalog(path: Path | None = None) -> list[CatalogEntry]:
    """Load and validate config/model-catalog.json."""
    import json

    p = path or _CATALOG_PATH
    raw = json.loads(p.read_text(encoding="utf-8"))
    return [CatalogEntry.model_validate(entry) for entry in raw]
