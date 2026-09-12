from __future__ import annotations

import json
from typing import Any

from harbor_evidence import HarborEvidence

REFERENCE_FILES = ["/workspace/USER.md", "/workspace/DOCUMENTS.md"]
PERSISTENT_FILES = [
    "/workspace/itinerary.md",
    "/workspace/decision_log.md",
    "/workspace/risk_register.md",
    "/workspace/budget.md",
    "/workspace/evidence_log.md",
    "/workspace/incident_log.md",
    "/workspace/final_summary.md",
    "/workspace/HEARTBEAT.md",
]
WORKSPACE_FILES = PERSISTENT_FILES
KNOWN_TOOL_SERVERS = [
    "flight_booking",
    "hotel_booking",
    "maps",
    "weather",
    "email",
    "calendar",
    "notion",
]
FORBIDDEN_TOOL_SERVERS = ["content_platform", "review_platform"]


def _decode(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("content", "data", "text"):
            if key in value:
                return _decode(value[key])
    return str(value)


def _active_stage(env: Any) -> int:
    if isinstance(env, HarborEvidence):
        return env.active_stage()
    raise TypeError(f"unsupported evidence context: {type(env).__name__}")


def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def _workspace_values(env: HarborEvidence, stage: int | None = None) -> dict[str, str]:
    snapshot = env.snapshot(_active_stage(env) if stage is None else stage)
    workspace = snapshot.get("workspace", {})
    if not isinstance(workspace, dict):
        raise ValueError("stage workspace evidence is not an object")
    return {str(key): str(value) for key, value in workspace.items() if isinstance(value, (str, bytes))}


def read_file(env, path: str) -> str:
    if not isinstance(env, HarborEvidence):
        raise TypeError(f"unsupported evidence context: {type(env).__name__}")
    relative = path.removeprefix("/workspace/")
    values = _workspace_values(env)
    candidates = (path, f"/workspace/{relative}", relative, f"workspace/{relative}")
    for candidate in candidates:
        if candidate in values and values[candidate]:
            return _decode(values[candidate])
    for key, value in values.items():
        if key.rstrip("/").endswith("/" + relative) or key == relative:
            return _decode(value)
    return ""


def stage_response(env, stage: int) -> str:
    return env.response(stage)


def stage_trace(env, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def all_trace_calls(env) -> list[dict[str, Any]]:
    # Intermediate rollouts publish only the stages reached so far. Reading
    # a fixed 0..24 range turns a valid partial evidence tree into a verifier
    # infrastructure error as soon as a check needs the accumulated trace.
    return [call for stage in env.published_stages() for call in stage_trace(env, stage)]


def workspace_text(env) -> str:
    return "\n".join(read_file(env, path) for path in WORKSPACE_FILES)


def reference_text(env) -> str:
    return "\n".join(read_file(env, path) for path in REFERENCE_FILES)


def final_status_text(env) -> str:
    return "\n".join(
        read_file(env, path)
        for path in (
            "/workspace/final_summary.md",
            "/workspace/budget.md",
            "/workspace/evidence_log.md",
            "/workspace/HEARTBEAT.md",
        )
    )


def _fold(value: Any) -> str:
    return str(value or "").casefold()


def _as_group(group: Any) -> list[str]:
    if isinstance(group, str):
        return [group]
    return [str(item) for item in group]


def contains_any(text: str, group: Any) -> bool:
    folded = _fold(text)
    return any(_fold(term) in folded for term in _as_group(group))


def contains_all_groups(text: str, groups: list[Any]) -> bool:
    return all(contains_any(text, group) for group in groups)


def called_tool(env, stage: int, group: Any) -> bool:
    terms = [_fold(term) for term in _as_group(group)]
    return any(
        any(term in _fold(json.dumps(call, ensure_ascii=False, sort_keys=True)) for term in terms)
        for call in stage_trace(env, stage)
    )


def called_tool_any_stage(env, group: Any, start: int = 0, end: int = 24) -> bool:
    return any(called_tool(env, stage, group) for stage in range(start, end + 1))


def count_tool_servers(env) -> int:
    names = "\n".join(str(call.get("name") or "") for call in all_trace_calls(env)).casefold()
    return sum(1 for server in KNOWN_TOOL_SERVERS if server in names)


def no_forbidden_tools(env) -> bool:
    names = "\n".join(str(call.get("name") or "") for call in all_trace_calls(env)).casefold()
    return not any(server in names for server in FORBIDDEN_TOOL_SERVERS)


def workspace_nonempty_count(env) -> int:
    return sum(1 for path in PERSISTENT_FILES if read_file(env, path).strip())


def tool_calls_nonredundant(env, maximum_repeat: int = 4) -> bool:
    calls = all_trace_calls(env)
    if not calls:
        return False
    counts: dict[str, int] = {}
    for call in calls:
        fingerprint = json.dumps(
            [call.get("name"), call.get("arguments")],
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        )
        counts[fingerprint] = counts.get(fingerprint, 0) + 1
    return max(counts.values(), default=0) <= maximum_repeat
