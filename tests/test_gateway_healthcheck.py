from sandbox.sandbox_manager import SandboxManager


def test_gateway_healthcheck_url_uses_health_for_base_url():
    assert (
        SandboxManager._gateway_healthcheck_url("http://192.168.1.10:8000")
        == "http://192.168.1.10:8000/health"
    )


def test_gateway_healthcheck_url_uses_health_for_root_path():
    assert (
        SandboxManager._gateway_healthcheck_url("http://192.168.1.10:8000/")
        == "http://192.168.1.10:8000/health"
    )


def test_gateway_healthcheck_url_preserves_existing_path():
    assert (
        SandboxManager._gateway_healthcheck_url("http://192.168.1.10:8000/api/inference")
        == "http://192.168.1.10:8000/api/inference"
    )
