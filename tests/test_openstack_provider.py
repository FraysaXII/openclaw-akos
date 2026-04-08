from types import SimpleNamespace
from unittest.mock import Mock

from akos.openstack_provider import InstanceInfo, OpenStackProvider


def _provider_with_mocked_conn() -> OpenStackProvider:
    provider = OpenStackProvider.__new__(OpenStackProvider)
    provider._enabled = True
    provider._conn = SimpleNamespace(compute=Mock())
    provider._resolve_flavor = Mock(return_value="flavor-id")
    provider._resolve_image = Mock(return_value="image-id")
    provider._resolve_network = Mock(return_value="network-id")
    provider._build_cloud_init = Mock(return_value="#cloud-init")
    provider._parse_instance = Mock(
        return_value=InstanceInfo(
            instance_id="inst-1",
            name="akos-vllm",
            status="ACTIVE",
        )
    )
    provider._conn.compute.create_server.return_value = {"id": "server-1"}
    provider._conn.compute.wait_for_server.return_value = {"id": "server-1"}
    return provider


def test_create_instance_omits_security_groups_when_not_provided():
    provider = _provider_with_mocked_conn()

    provider.create_instance(
        name="akos-vllm",
        flavor="power-c32m112-gpu-A4500-4",
        image="Ubuntu-22.04",
        network="default",
        security_groups=None,
        vllm_args=["--model", "foo/bar"],
    )

    kwargs = provider._conn.compute.create_server.call_args.kwargs
    assert "security_groups" not in kwargs
    assert "key_name" not in kwargs


def test_create_instance_passes_security_groups_when_provided():
    provider = _provider_with_mocked_conn()

    provider.create_instance(
        name="akos-vllm",
        flavor="power-c32m112-gpu-A4500-4",
        image="Ubuntu-22.04",
        network="default",
        security_groups=[{"name": "default"}],
        vllm_args=["--model", "foo/bar"],
    )

    kwargs = provider._conn.compute.create_server.call_args.kwargs
    assert kwargs["security_groups"] == [{"name": "default"}]


def test_create_instance_passes_key_name_when_provided():
    provider = _provider_with_mocked_conn()

    provider.create_instance(
        name="akos-vllm",
        flavor="power-c32m112-gpu-A4500-4",
        image="Ubuntu-22.04",
        network="public",
        key_name="shadow-key",
        vllm_args=["--model", "foo/bar"],
    )

    kwargs = provider._conn.compute.create_server.call_args.kwargs
    assert kwargs["key_name"] == "shadow-key"
