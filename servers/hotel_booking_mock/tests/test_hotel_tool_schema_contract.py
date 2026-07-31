from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

SERVER_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SERVER_ROOT.parents[1]
sys.path.insert(0, str(SERVER_ROOT / "src"))

from hotel_booking_mock.server import build_server  # noqa: E402

SEED = PROJECT_ROOT / "envs/hotel_booking/galapagos_no_us_transit/init.sql"


def _build(tmp_path: Path):
    env_dir = tmp_path / "hotel-env"
    env_dir.mkdir()
    shutil.copy(SEED, env_dir / "init.sql")
    return build_server(env_dir)


def _tool_schema(server, name: str) -> dict:
    tool = next(tool for tool in server._tool_manager.list_tools() if tool.name == name)
    return tool.parameters


def _resolve(schema: dict, node: dict) -> dict:
    ref = node.get("$ref")
    if not ref:
        return node
    assert ref.startswith("#/$defs/")
    return schema["$defs"][ref.rsplit("/", 1)[-1]]


def test_create_reservation_schema_exposes_required_guest_profile_fields(tmp_path: Path) -> None:
    server = _build(tmp_path)
    schema = _tool_schema(server, "create_reservation")
    guest = _resolve(schema, schema["properties"]["guest_profile"])

    assert guest.get("additionalProperties") is not True
    assert set(guest["required"]) == {
        "first_name",
        "last_name",
        "email",
        "phone",
        "user_id",
    }
    assert set(guest["properties"]) == set(guest["required"])
    assert all(guest["properties"][field].get("description") for field in guest["required"])


def test_create_reservation_schema_documents_rate_plan_identity(tmp_path: Path) -> None:
    server = _build(tmp_path)
    schema = _tool_schema(server, "create_reservation")
    description = schema["properties"]["rate_plan_id"].get("description", "")

    assert "get_room_availability" in description
    assert "rp_" in description
    assert "YYYYMMDD" in description


def test_server_dependency_contract_excludes_mcp_v2() -> None:
    import tomllib

    from packaging.requirements import Requirement
    from packaging.version import Version

    project = tomllib.loads((SERVER_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    mcp_requirement = next(
        Requirement(item)
        for item in project["project"]["dependencies"]
        if Requirement(item).name == "mcp"
    )

    assert Version("1.28.1") in mcp_requirement.specifier
    assert Version("2.0.0") not in mcp_requirement.specifier
