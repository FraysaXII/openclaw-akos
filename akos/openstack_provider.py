"""ShadowPC OpenStack GPU infrastructure provider for AKOS.

Typed wrapper around the ``openstacksdk`` Python SDK for managing GPU
instances on Shadow's OpenStack infrastructure.  Provides idempotent
instance creation, health monitoring, vLLM deployment via cloud-init,
spot termination detection, and teardown.

Graceful no-op when ``OS_AUTH_URL`` is not set (dev-local without Shadow).
"""

from __future__ import annotations

import json
import logging
import os
import textwrap
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger("akos.openstack")

_openstack_available = False
try:
    import openstack  # type: ignore[import-untyped]

    _openstack_available = True
except ImportError:
    openstack = None  # type: ignore[assignment]


# ── Response Dataclasses ─────────────────────────────────────────────


@dataclass
class InstanceInfo:
    instance_id: str
    name: str
    status: str
    flavor: str = ""
    ip_address: str = ""
    floating_ip: str = ""
    url: str = ""
    raw: dict = field(default_factory=dict)


@dataclass
class SpotTermination:
    scheduled: bool = False
    scheduled_at: float = 0
    termination_at: float = 0


CLOUD_INIT_TEMPLATE = textwrap.dedent("""\
    #!/bin/bash
    set -euo pipefail

    export DEBIAN_FRONTEND=noninteractive

    apt-get update -qq
    apt-get install -y -qq python3-pip python3-venv curl > /dev/null 2>&1

    python3 -m venv /opt/vllm-env
    source /opt/vllm-env/bin/activate

    pip install -q vllm

    HF_TOKEN="{hf_token}"
    if [ -n "$HF_TOKEN" ]; then
        export HF_TOKEN
    fi

    nohup python3 -m vllm.entrypoints.openai.api_server \\
        {vllm_args} \\
        > /var/log/vllm.log 2>&1 &

    echo "vLLM starting on port {port}..."
""")


class OpenStackProvider:
    """Manages ShadowPC OpenStack GPU instances for AKOS.

    All public methods are no-ops returning sensible defaults when the
    ``openstacksdk`` package is missing or ``OS_AUTH_URL`` is not set.
    """

    def __init__(
        self,
        *,
        cloud_name: str | None = None,
        auth_url: str | None = None,
        project_id: str | None = None,
        username: str | None = None,
        password: str | None = None,
        region: str | None = None,
    ) -> None:
        self._enabled = False
        self._conn: Any = None

        self._auth_url = auth_url or os.environ.get("OS_AUTH_URL", "")
        self._project_id = project_id or os.environ.get("OS_PROJECT_ID", "")
        self._username = username or os.environ.get("OS_USERNAME", "")
        self._password = password or os.environ.get("OS_PASSWORD", "")
        self._region = region or os.environ.get("OS_REGION_NAME", "")
        self._cloud_name = cloud_name or os.environ.get("OS_CLOUD", "")

        if not _openstack_available:
            logger.warning("openstacksdk not installed; OpenStack provider disabled")
            return

        if not self._auth_url and not self._cloud_name:
            logger.info("OS_AUTH_URL / OS_CLOUD not set; OpenStack provider disabled")
            return

        try:
            self._conn = self._connect()
            self._enabled = True
            logger.info(
                "OpenStack provider initialized (region=%s, project=%s)",
                self._region or "default",
                self._project_id[:12] + "..." if len(self._project_id) > 12 else self._project_id,
            )
        except Exception as exc:
            logger.error("OpenStack connection failed: %s", exc)

    def _connect(self) -> Any:
        if self._cloud_name:
            return openstack.connect(cloud=self._cloud_name)

        return openstack.connect(
            auth_url=self._auth_url,
            project_id=self._project_id,
            username=self._username,
            password=self._password,
            region_name=self._region or None,
            user_domain_name=os.environ.get("OS_USER_DOMAIN_NAME", "Default"),
            project_domain_name=os.environ.get("OS_PROJECT_DOMAIN_NAME", "Default"),
        )

    @property
    def enabled(self) -> bool:
        return self._enabled

    # ── Instance Lifecycle ────────────────────────────────────────────

    def create_instance(
        self,
        *,
        name: str,
        flavor: str,
        image: str,
        network: str,
        security_groups: list[str] | None = None,
        key_name: str | None = None,
        vllm_args: list[str] | None = None,
        vllm_port: int = 8080,
        hf_token: str = "",
    ) -> InstanceInfo | None:
        """Create a GPU instance with vLLM cloud-init bootstrapping."""
        if not self._enabled:
            logger.warning("OpenStack provider not enabled")
            return None

        userdata = self._build_cloud_init(
            vllm_args=vllm_args or [],
            port=vllm_port,
            hf_token=hf_token,
        )

        try:
            create_kwargs: dict[str, Any] = {
                "name": name,
                "flavor_id": self._resolve_flavor(flavor),
                "image_id": self._resolve_image(image),
                "networks": [{"uuid": self._resolve_network(network)}],
                "user_data": userdata,
            }
            if security_groups is not None:
                create_kwargs["security_groups"] = security_groups
            if key_name is not None:
                create_kwargs["key_name"] = key_name

            server = self._conn.compute.create_server(
                **create_kwargs,
            )
            server = self._conn.compute.wait_for_server(server, wait=600)
            info = self._parse_instance(server)
            logger.info("Created instance %s (%s)", info.instance_id, info.name)
            return info
        except Exception as exc:
            logger.error("Instance creation failed: %s", exc)
            return None

    def get_instance(self, instance_id: str) -> InstanceInfo | None:
        """Get instance status by ID."""
        if not self._enabled:
            return None
        try:
            server = self._conn.compute.get_server(instance_id)
            return self._parse_instance(server)
        except Exception as exc:
            logger.debug("Instance lookup failed: %s", exc)
            return None

    def list_instances(self, name_prefix: str = "akos-") -> list[InstanceInfo]:
        """List instances matching a name prefix."""
        if not self._enabled:
            return []
        try:
            servers = self._conn.compute.servers(name=f"^{name_prefix}")
            return [self._parse_instance(s) for s in servers]
        except Exception as exc:
            logger.warning("Instance list failed: %s", exc)
            return []

    def delete_instance(self, instance_id: str) -> bool:
        """Delete an instance."""
        if not self._enabled:
            return False
        try:
            self._conn.compute.delete_server(instance_id)
            logger.info("Deleted instance %s", instance_id)
            return True
        except Exception as exc:
            logger.error("Instance deletion failed: %s", exc)
            return False

    # ── Floating IP Management ───────────────────────────────────────

    def assign_floating_ip(
        self,
        instance_id: str,
        network: str = "public",
    ) -> str | None:
        """Allocate and assign a floating IP to an instance."""
        if not self._enabled:
            return None
        try:
            fip = self._conn.network.create_ip(floating_network_id=self._resolve_network(network))
            server = self._conn.compute.get_server(instance_id)
            self._conn.compute.add_floating_ip_to_server(server, fip["floating_ip_address"])
            logger.info("Assigned floating IP %s to %s", fip["floating_ip_address"], instance_id)
            return fip["floating_ip_address"]
        except Exception as exc:
            logger.error("Floating IP assignment failed: %s", exc)
            return None

    # ── Spot Termination Detection ───────────────────────────────────

    def check_spot_termination(self, instance_id: str) -> SpotTermination:
        """Poll instance metadata for spot termination signals.

        ShadowPC injects ``cloud_termination_time`` and
        ``cloud_termination_scheduled_event_time`` into instance metadata
        when a preemptible instance is scheduled for termination.
        """
        if not self._enabled:
            return SpotTermination()
        try:
            server = self._conn.compute.get_server(instance_id)
            meta = server.get("metadata", {})
            term_time = meta.get("cloud_termination_time")
            sched_time = meta.get("cloud_termination_scheduled_event_time")
            if term_time:
                return SpotTermination(
                    scheduled=True,
                    scheduled_at=float(sched_time or 0),
                    termination_at=float(term_time),
                )
        except Exception as exc:
            logger.debug("Spot termination check failed: %s", exc)
        return SpotTermination()

    # ── Security Group Management ────────────────────────────────────

    def ensure_security_group(
        self,
        name: str = "akos-vllm",
        vllm_port: int = 8080,
    ) -> str | None:
        """Ensure a security group allowing SSH and vLLM port exists."""
        if not self._enabled:
            return None
        try:
            existing = self._conn.network.find_security_group(name)
            if existing:
                return existing["id"]

            sg = self._conn.network.create_security_group(
                name=name,
                description="AKOS vLLM inference security group",
            )
            self._conn.network.create_security_group_rule(
                security_group_id=sg["id"],
                direction="ingress",
                protocol="tcp",
                port_range_min=22,
                port_range_max=22,
                remote_ip_prefix="0.0.0.0/0",
            )
            self._conn.network.create_security_group_rule(
                security_group_id=sg["id"],
                direction="ingress",
                protocol="tcp",
                port_range_min=vllm_port,
                port_range_max=vllm_port,
                remote_ip_prefix="0.0.0.0/0",
            )
            logger.info("Created security group %s (id=%s)", name, sg["id"])
            return sg["id"]
        except Exception as exc:
            logger.error("Security group setup failed: %s", exc)
            return None

    # ── Flavor / Image / Network Discovery ───────────────────────────

    def list_flavors(self) -> list[dict[str, Any]]:
        """List available flavors (GPU instance types)."""
        if not self._enabled:
            return []
        try:
            return [
                {
                    "id": f["id"],
                    "name": f["name"],
                    "vcpus": f.get("vcpus"),
                    "ram_mb": f.get("ram"),
                    "disk_gb": f.get("disk"),
                }
                for f in self._conn.compute.flavors()
            ]
        except Exception as exc:
            logger.warning("Flavor listing failed: %s", exc)
            return []

    def list_images(self) -> list[dict[str, Any]]:
        """List available images."""
        if not self._enabled:
            return []
        try:
            return [
                {
                    "id": img["id"],
                    "name": img["name"],
                    "status": img.get("status"),
                }
                for img in self._conn.image.images()
            ]
        except Exception as exc:
            logger.warning("Image listing failed: %s", exc)
            return []

    # ── vLLM Health Probe (reuses same HTTP logic as RunPod) ─────────

    @staticmethod
    def probe_vllm_health(base_url: str, *, timeout: float = 5.0) -> dict:
        """HTTP health probe for a vLLM endpoint (provider-agnostic).

        Tries GET ``{base_url}/models`` then falls back to ``/health``.
        """
        url = base_url.rstrip("/")
        if url.endswith("/v1"):
            models_url = url + "/models"
        else:
            models_url = url + "/v1/models"

        for probe_url in (models_url, url.rsplit("/v1", 1)[0] + "/health"):
            try:
                req = urllib.request.Request(probe_url, method="GET")
                req.add_header("User-Agent", "akos-gpu-cli/1.0")
                req.add_header("Accept", "application/json")
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    if resp.status == 200:
                        return {"healthy": True, "probe_url": probe_url}
            except (urllib.error.URLError, OSError, TimeoutError):
                continue
        return {"healthy": False, "probe_url": base_url, "error": "unreachable"}

    # ── Private Helpers ──────────────────────────────────────────────

    def _resolve_flavor(self, name_or_id: str) -> str:
        """Resolve a flavor name to its ID."""
        try:
            flavor = self._conn.compute.find_flavor(name_or_id)
            return flavor["id"] if flavor else name_or_id
        except Exception:
            return name_or_id

    def _resolve_image(self, name_or_id: str) -> str:
        """Resolve an image name to its ID."""
        try:
            image = self._conn.image.find_image(name_or_id)
            return image["id"] if image else name_or_id
        except Exception:
            return name_or_id

    def _resolve_network(self, name_or_id: str) -> str:
        """Resolve a network name to its ID."""
        try:
            net = self._conn.network.find_network(name_or_id)
            return net["id"] if net else name_or_id
        except Exception:
            return name_or_id

    @staticmethod
    def _parse_instance(server: Any) -> InstanceInfo:
        addresses = server.get("addresses", {})
        ip_address = ""
        floating_ip = ""
        for net_addrs in addresses.values():
            if isinstance(net_addrs, list):
                for addr in net_addrs:
                    if addr.get("OS-EXT-IPS:type") == "floating":
                        floating_ip = addr.get("addr", "")
                    elif not ip_address:
                        ip_address = addr.get("addr", "")

        return InstanceInfo(
            instance_id=server.get("id", ""),
            name=server.get("name", ""),
            status=server.get("status", "UNKNOWN"),
            flavor=server.get("flavor", {}).get("original_name", ""),
            ip_address=ip_address,
            floating_ip=floating_ip,
            url=f"http://{floating_ip or ip_address}:8080/v1" if (floating_ip or ip_address) else "",
            raw=dict(server) if hasattr(server, "items") else {},
        )

    @staticmethod
    def _build_cloud_init(
        vllm_args: list[str],
        port: int,
        hf_token: str,
    ) -> str:
        import base64

        args_str = " \\\n        ".join(vllm_args) if vllm_args else "--help"
        script = CLOUD_INIT_TEMPLATE.format(
            vllm_args=args_str,
            port=port,
            hf_token=hf_token,
        )
        return base64.b64encode(script.encode()).decode()
