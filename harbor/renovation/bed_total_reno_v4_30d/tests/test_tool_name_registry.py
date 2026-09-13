"""Pin L6 — tool-name registry contract.

Every tool reference in the task must resolve to a mock the task actually
ships: each referenced pair is (a) a server registered in tests/services.json
and (b) a tool that mock's ``tools/`` package exposes. The snapshot pipeline is
included because a phantom capture call (e.g. ``delivery_logistics.
list_addresses``) silently freezes ``{"error": ...}`` into every stage
snapshot, and dead captures for unregistered servers (``notion.*``) are shape
noise that no rubric can ever score.

Runnable standalone: ``python3 tests/test_tool_name_registry.py``.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def mock_tool_surface():
    """Map server name -> set of tool names declared in its mock's tools/."""
    surface = {}
    servers_dir = os.path.join(ROOT, "environment", "servers")
    for server in sorted(os.listdir(servers_dir)):
        if not server.endswith("_mock"):
            continue
        tools = set()
        for dirpath, _dirs, files in os.walk(os.path.join(servers_dir, server, "src")):
            if os.path.basename(dirpath) != "tools":
                continue
            for name in files:
                if name.endswith(".py"):
                    with open(os.path.join(dirpath, name), encoding="utf-8") as fh:
                        tools |= set(re.findall(r"async def (\w+)\(", fh.read()))
        surface[server[: -len("_mock")]] = tools
    return surface


def referenced_pairs(text):
    """(server, tool) pairs from oracle rec.call and snapshot _call/_paged_call."""
    pairs = set()
    pairs |= set(re.findall(r'rec\.call\(\s*"([a-z_]+)"\s*,\s*"([A-Za-z0-9_-]+)"', text))
    pairs |= set(re.findall(r'_call\(\s*env\s*,\s*"([a-z_]+)"\s*,\s*"([A-Za-z0-9_-]+)"', text))
    pairs |= set(re.findall(r'_paged_call\(\s*env\s*,\s*"([a-z_]+)"\s*,\s*"([A-Za-z0-9_-]+)"', text))
    return pairs


def test_services_registry_matches_shipped_mocks():
    with open(os.path.join(HERE, "services.json"), encoding="utf-8") as fh:
        registered = set(json.load(fh)["mcp_servers"])
    surface = mock_tool_surface()
    assert registered == set(surface), (
        f"services.json vs shipped mocks mismatch: registry-only={registered - set(surface)} "
        f"mock-only={set(surface) - registered}"
    )
    assert all(tools for tools in surface.values()), "a registered mock exposes no tools"


def test_all_tool_references_resolve():
    surface = mock_tool_surface()
    sources = [os.path.join(HERE, "run_verifier.py")]
    sources.append(os.path.join(ROOT, "environment", "evidence-collector", "snapshot_capture.py"))
    for dirpath, _dirs, files in os.walk(os.path.join(ROOT, "steps")):
        for name in files:
            if name == "oracle.py":
                sources.append(os.path.join(dirpath, name))
    unresolved = []
    for path in sources:
        with open(path, encoding="utf-8") as fh:
            for pair in sorted(referenced_pairs(fh.read())):
                server, tool = pair
                if server not in surface or tool not in surface[server]:
                    unresolved.append((os.path.relpath(path, ROOT), server, tool))
    assert not unresolved, f"tool references with no mock implementation: {unresolved}"


def test_server_from_name_normalization():
    sys_path = os.path.join(HERE)
    if sys_path not in __import__("sys").path:
        __import__("sys").path.insert(0, sys_path)
    from rubrics.shared import _helpers as R

    assert R._server_from_name("ecommerce__get_cart") == "ecommerce"
    assert R._server_from_name("ecommerce_get_cart") == "ecommerce"
    assert R._server_from_name("Ecommerce-Get-Cart") == "ecommerce"
    assert R._server_from_name("delivery-logistics__list_shipments") == "delivery_logistics"
    assert R._server_from_name("unknown_service") is None


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
