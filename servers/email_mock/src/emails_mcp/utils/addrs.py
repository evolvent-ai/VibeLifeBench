"""Tiny helpers for the comma-separated address strings used by the tool surface.

The SQLite backend stores ``to_addr`` / ``cc_addr`` / ``bcc_addr`` as JSON
arrays (text). On the tool boundary the agent supplies / sees a flat
comma-separated string, mirroring the upstream emails-mcp shape so existing
benchmark tasks keep working.
"""
import json
from typing import List, Optional


def parse_addr_list(value: Optional[str]) -> List[str]:
    """``"a@x, b@x"`` -> ``["a@x", "b@x"]``. ``None``/``""`` -> ``[]``."""
    if not value:
        return []
    return [a.strip() for a in value.split(",") if a.strip()]


def addrs_to_json(value: Optional[str]) -> str:
    return json.dumps(parse_addr_list(value), ensure_ascii=False)


def json_to_csv(value) -> str:
    """``'["a","b"]'`` (or list) -> ``"a, b"``. ``None``/empty -> ``""``."""
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    if isinstance(value, list):
        return ", ".join(str(v) for v in value if v)
    return str(value)
