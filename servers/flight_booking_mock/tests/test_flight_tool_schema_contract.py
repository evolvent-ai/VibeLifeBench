from __future__ import annotations

import shutil
import sys
from pathlib import Path

SERVER_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SERVER_ROOT.parents[1]
sys.path.insert(0, str(SERVER_ROOT / "src"))

from flight_booking_mock.config import AppConfig  # noqa: E402
from flight_booking_mock.server import build_server  # noqa: E402

SEED = PROJECT_ROOT / "envs/flight_booking/galapagos_no_us_transit/init.sql"


def _build(tmp_path: Path):
    env_dir = tmp_path / "flight-env"
    env_dir.mkdir()
    shutil.copy(SEED, env_dir / "init.sql")
    server, backend = build_server(
        AppConfig(
            env=str(env_dir),
            host="127.0.0.1",
            port=8000,
            debug=False,
            transport="stdio",
        )
    )
    return server, backend


def _tool_schema(server, name: str) -> dict:
    tool = next(tool for tool in server._tool_manager.list_tools() if tool.name == name)
    return tool.parameters


def _resolve(schema: dict, node: dict) -> dict:
    ref = node.get("$ref")
    if not ref:
        return node
    assert ref.startswith("#/$defs/")
    return schema["$defs"][ref.rsplit("/", 1)[-1]]


def test_create_booking_schema_exposes_nested_passenger_contact_and_payment_fields(tmp_path: Path) -> None:
    server, backend = _build(tmp_path)
    try:
        schema = _tool_schema(server, "create_booking")
        passenger = _resolve(schema, schema["properties"]["passengers"]["items"])
        contact = _resolve(schema, schema["properties"]["contact"])
        payment = _resolve(schema, schema["properties"]["payment"])

        assert passenger.get("additionalProperties") is not True
        assert set(passenger["required"]) == {"type", "given_name", "family_name"}
        assert {"dob", "passport_no", "nationality", "frequent_flyer"}.issubset(
            passenger["properties"]
        )
        assert set(contact["required"]) == {"email", "phone"}
        assert set(payment["required"]) == {"method"}
        assert "card_last4" in payment["properties"]
    finally:
        backend.close()


def test_seat_selection_schema_exposes_indices_and_seat(tmp_path: Path) -> None:
    server, backend = _build(tmp_path)
    try:
        schema = _tool_schema(server, "create_booking")
        selection_union = schema["properties"]["seat_selections"]["anyOf"]
        array_schema = next(option for option in selection_union if option.get("type") == "array")
        selection = _resolve(schema, array_schema["items"])

        assert set(selection["required"]) == {"segment_idx", "pax_idx", "seat"}
        assert selection.get("additionalProperties") is not True
    finally:
        backend.close()


def test_check_in_preferred_seat_schema_matches_service_payload(tmp_path: Path) -> None:
    server, backend = _build(tmp_path)
    try:
        schema = _tool_schema(server, "check_in")
        selection_union = schema["properties"]["preferred_seats"]["anyOf"]
        array_schema = next(option for option in selection_union if option.get("type") == "array")
        selection = _resolve(schema, array_schema["items"])

        assert set(selection["required"]) == {"pax_idx", "seat"}
        assert "segment_idx" not in selection["properties"]
        assert selection.get("additionalProperties") is not True
    finally:
        backend.close()


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
