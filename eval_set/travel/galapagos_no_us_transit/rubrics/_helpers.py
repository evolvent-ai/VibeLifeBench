from __future__ import annotations

import json
from typing import Any

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


def _path_candidates(path: str) -> list[str]:
    candidates = [path]
    if path.startswith("/workspace/"):
        relative = path.removeprefix("/workspace/")
        candidates.extend(
            [
                f"/terrarium/openclaw/workspace/{relative}",
                f"/terrarium/workspace/{relative}",
                f"workspace/{relative}",
                relative,
            ]
        )
    return list(dict.fromkeys(candidates))


def read_file(env, path: str) -> str:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return ""
    for candidate in _path_candidates(path):
        try:
            value = fs.read_file(candidate)
        except Exception:
            continue
        text = _decode(value)
        if text:
            return text
    return ""


def stage_response(env, stage: int) -> str:
    return read_file(env, f"/terrarium/agent_responses/stage_{stage}.txt")


def stage_trace(env, stage: int) -> list[dict[str, Any]]:
    raw = read_file(env, f"/terrarium/agent_traces/stage_{stage}.json")
    if not raw.strip():
        return []
    try:
        payload = json.loads(raw)
    except Exception:
        return []
    return [row for row in payload if isinstance(row, dict)] if isinstance(payload, list) else []


def all_trace_calls(env) -> list[dict[str, Any]]:
    return [call for stage in range(25) for call in stage_trace(env, stage)]


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
