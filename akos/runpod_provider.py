"""RunPod GPU infrastructure provider for AKOS.

Typed wrapper around the RunPod Python SDK for managing serverless vLLM
endpoints.  Provides idempotent endpoint creation, health monitoring,
scaling, inference, and teardown.

Graceful no-op when RUNPOD_API_KEY is not set (dev-local without RunPod).
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any

from akos.models import RunPodEndpointConfig

logger = logging.getLogger("akos.runpod")

_runpod_available = False
try:
    import runpod

    _runpod_available = True
except ImportError:
    runpod = None  # type: ignore[assignment]


# ── Response Dataclasses ─────────────────────────────────────────────


@dataclass
class EndpointInfo:
    endpoint_id: str
    url: str
    template_id: str


@dataclass
class HealthStatus:
    healthy: bool
    workers_ready: int = 0
    workers_running: int = 0
    queue_depth: int = 0
    idle_time_seconds: float = 0
    raw: dict = field(default_factory=dict)


@dataclass
class InferenceResult:
    output: str
    status: str
    latency_ms: float = 0
    tokens_used: int = 0
    raw: dict = field(default_factory=dict)


@dataclass
class GpuInfo:
    gpu_id: str
    display_name: str
    memory_gb: int
    available: bool
    price_per_sec: float = 0.0


# ── Provider ─────────────────────────────────────────────────────────


class RunPodProvider:
    """Manages RunPod serverless vLLM endpoints for AKOS.

    All public methods are no-ops returning sensible defaults when the
    ``runpod`` package is missing or ``RUNPOD_API_KEY`` is not set.
    """

    def __init__(self, config: RunPodEndpointConfig | None = None) -> None:
        self._config = config or RunPodEndpointConfig()
        self._enabled = False
        self._endpoint_id: str | None = os.environ.get("RUNPOD_ENDPOINT_ID")

        api_key = os.environ.get("RUNPOD_API_KEY")
        if not api_key:
            logger.info("RUNPOD_API_KEY not set; RunPod provider disabled")
            return
        if not _runpod_available:
            logger.warning("runpod package not installed; RunPod provider disabled")
            return

        runpod.api_key = api_key
        self._enabled = True
        logger.info("RunPod provider initialized (template=%s)", self._config.templateName)

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def endpoint_id(self) -> str | None:
        return self._endpoint_id

    # ── Endpoint Lifecycle ───────────────────────────────────────────

    def ensure_endpoint(self) -> EndpointInfo | None:
        """Create the vLLM serverless endpoint if it doesn't exist.

        Idempotent: if ``RUNPOD_ENDPOINT_ID`` is set and the endpoint
        exists, returns its info without creating a new one.
        """
        if not self._enabled:
            return None

        if self._endpoint_id:
            existing = self._get_endpoint(self._endpoint_id)
            if existing:
                logger.info("Endpoint %s already exists", self._endpoint_id)
                return existing
            logger.warning(
                "RUNPOD_ENDPOINT_ID=%s not found; creating new endpoint",
                self._endpoint_id,
            )

        cfg = self._config
        try:
            template = runpod.create_template(
                name=cfg.templateName,
                image_name=cfg.vllmImage,
                is_serverless=True,
                env=self._build_env_vars(),
            )
            template_id = template["id"]
            logger.info("Created template %s (%s)", cfg.templateName, template_id)

            endpoint = runpod.create_endpoint(
                name=f"akos-{cfg.templateName}",
                template_id=template_id,
                gpu_ids=",".join(cfg.gpuIds),
                workers_min=cfg.activeWorkers,
                workers_max=cfg.maxWorkers,
                idle_timeout=cfg.idleTimeoutSeconds,
            )
            self._endpoint_id = endpoint["id"]
            url = f"https://api.runpod.ai/v2/{self._endpoint_id}"
            logger.info("Created endpoint %s -> %s", self._endpoint_id, url)
            return EndpointInfo(
                endpoint_id=self._endpoint_id,
                url=url,
                template_id=template_id,
            )
        except Exception as exc:
            logger.error("Failed to create RunPod endpoint: %s", exc)
            return None

    def health_check(self) -> HealthStatus:
        """Check the health of the current endpoint."""
        if not self._enabled or not self._endpoint_id:
            return HealthStatus(healthy=False)

        try:
            endpoint = runpod.Endpoint(self._endpoint_id)
            status = endpoint.health()
            workers = status.get("workers", {})
            return HealthStatus(
                healthy=status.get("status") == "READY"
                or workers.get("ready", 0) > 0,
                workers_ready=workers.get("ready", 0),
                workers_running=workers.get("running", 0),
                queue_depth=status.get("jobsInQueue", 0),
                idle_time_seconds=status.get("idleTime", 0),
                raw=status,
            )
        except Exception as exc:
            logger.warning("Health check failed: %s", exc)
            return HealthStatus(healthy=False)

    def scale(self, min_workers: int, max_workers: int) -> bool:
        """Adjust the scaling parameters for the endpoint."""
        if not self._enabled or not self._endpoint_id:
            return False

        try:
            runpod.update_endpoint_template(
                endpoint_id=self._endpoint_id,
                workers_min=min_workers,
                workers_max=max_workers,
            )
            logger.info(
                "Scaled endpoint %s: min=%d, max=%d",
                self._endpoint_id,
                min_workers,
                max_workers,
            )
            return True
        except Exception as exc:
            logger.error("Scale failed: %s", exc)
            return False

    def teardown(self, *, delete: bool = False) -> bool:
        """Scale to zero. Optionally delete the endpoint entirely."""
        if not self._enabled or not self._endpoint_id:
            return False

        try:
            if delete:
                runpod.delete_endpoint(self._endpoint_id)
                logger.info("Deleted endpoint %s", self._endpoint_id)
                self._endpoint_id = None
            else:
                self.scale(min_workers=0, max_workers=0)
                logger.info("Scaled endpoint %s to zero", self._endpoint_id)
            return True
        except Exception as exc:
            logger.error("Teardown failed: %s", exc)
            return False

    # ── Inference ────────────────────────────────────────────────────

    def infer(
        self,
        prompt: str,
        *,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        timeout: int = 120,
        **kwargs: Any,
    ) -> InferenceResult:
        """Run synchronous inference against the vLLM endpoint."""
        if not self._enabled or not self._endpoint_id:
            return InferenceResult(output="", status="disabled")

        payload: dict[str, Any] = {
            "input": {
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
                **kwargs,
            }
        }

        t0 = time.monotonic()
        try:
            endpoint = runpod.Endpoint(self._endpoint_id)
            result = endpoint.run_sync(payload, timeout=timeout)
            latency = (time.monotonic() - t0) * 1000

            output_text = ""
            tokens = 0
            if isinstance(result, dict):
                output_text = result.get("output", result.get("text", str(result)))
                usage = result.get("usage", {})
                tokens = usage.get("total_tokens", 0)
            else:
                output_text = str(result)

            return InferenceResult(
                output=output_text,
                status="completed",
                latency_ms=latency,
                tokens_used=tokens,
                raw=result if isinstance(result, dict) else {"text": output_text},
            )
        except Exception as exc:
            latency = (time.monotonic() - t0) * 1000
            logger.error("Inference failed (%.0fms): %s", latency, exc)
            return InferenceResult(
                output="",
                status="error",
                latency_ms=latency,
            )

    # ── GPU Discovery ────────────────────────────────────────────────

    def get_gpu_availability(self) -> list[GpuInfo]:
        """List available GPU types with pricing."""
        if not self._enabled:
            return []

        try:
            gpus = runpod.get_gpus()
            result: list[GpuInfo] = []
            for gpu in gpus:
                result.append(
                    GpuInfo(
                        gpu_id=gpu.get("id", ""),
                        display_name=gpu.get("displayName", ""),
                        memory_gb=gpu.get("memoryInGb", 0),
                        available=gpu.get("communityCloud", False)
                        or gpu.get("secureCloud", False),
                        price_per_sec=gpu.get("communityPrice", 0.0),
                    )
                )
            return result
        except Exception as exc:
            logger.warning("GPU listing failed: %s", exc)
            return []

    # ── Private ──────────────────────────────────────────────────────

    def _get_endpoint(self, endpoint_id: str) -> EndpointInfo | None:
        """Look up an existing endpoint by ID."""
        try:
            endpoints = runpod.get_endpoints()
            for ep in endpoints:
                if ep.get("id") == endpoint_id:
                    return EndpointInfo(
                        endpoint_id=endpoint_id,
                        url=f"https://api.runpod.ai/v2/{endpoint_id}",
                        template_id=ep.get("templateId", ""),
                    )
        except Exception as exc:
            logger.debug("Endpoint lookup failed: %s", exc)
        return None

    def _build_env_vars(self) -> dict[str, str]:
        """Merge config envVars with required vLLM settings."""
        base: dict[str, str] = {
            "MODEL_NAME": self._config.modelName,
            "MAX_MODEL_LEN": str(self._config.maxModelLen),
        }
        base.update(self._config.envVars)
        return base
