from akos.runtime import parse_gateway_status_output


def test_normalizes_unknown_to_healthy_when_probe_and_listener_are_healthy() -> None:
    output = """
Runtime: unknown
RPC probe: ok
Listening: 127.0.0.1:18789
"""
    snap = parse_gateway_status_output(output)
    assert snap.raw_runtime == "unknown"
    assert snap.rpc_probe == "ok"
    assert snap.normalized_runtime == "healthy"


def test_keeps_unknown_without_healthy_probe_evidence() -> None:
    output = """
Runtime: unknown
RPC probe: unreachable
Listening: not listening
"""
    snap = parse_gateway_status_output(output)
    assert snap.normalized_runtime == "unknown"


def test_marks_non_unknown_with_bad_probe_as_degraded() -> None:
    output = """
Runtime: running
RPC probe: timeout
Listening: not listening
"""
    snap = parse_gateway_status_output(output)
    assert snap.normalized_runtime == "degraded"
