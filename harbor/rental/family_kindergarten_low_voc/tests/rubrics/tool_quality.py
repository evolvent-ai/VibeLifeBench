from __future__ import annotations

import json

from harbor_evidence import trace
from ._helpers import STAGE_COUNT


def _records(env):
    rows = []
    for stage in env.published_stages():
        data = trace(env, stage)
        if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
            raise RuntimeError(f"tool trace for stage {stage} must be a list of objects")
        rows.extend(data)
    return rows


def successful_tool_result(env) -> bool:
    rows = _records(env)
    return bool(rows) and all(row.get("success") is True and row.get("result") not in (None, "") for row in rows)


def no_missing_or_failed_tool_result(env) -> bool:
    rows = _records(env)
    return bool(rows) and not any(row.get("success") is not True or row.get("error") for row in rows)


def cross_service_evidence(env) -> bool:
    servers = set()
    for row in _records(env):
        if row.get("success") is not True:
            continue
        name = str(row.get("name") or "").lower().replace("-", "_")
        for server in (
            "listing_platform", "maps", "calendar", "email", "notion", "review_platform",
            "notification_hub", "ecommerce", "delivery_logistics", "banking", "legal_search",
        ):
            if server in name:
                servers.add(server)
    return len(servers) >= 4


CHECKS = [
    ("tool_quality_successful_results", successful_tool_result, 3.0),
    ("tool_quality_no_missing_or_failed_results", no_missing_or_failed_tool_result, 3.0),
    ("tool_quality_cross_service_evidence", cross_service_evidence, 2.0),
]
