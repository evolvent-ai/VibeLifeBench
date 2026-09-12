"""Parse the current Harbor trajectory into response and tool-call evidence.

This module is deliberately read-only: it never merges prior workspace files
and never writes historical evidence. The world-controller performs all
private event accumulation after this parser returns the current turn only.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def _field(obj: Any, name: str, default: Any = None) -> Any:
    return obj.get(name, default) if isinstance(obj, dict) else getattr(obj, name, default)


def _jsonable(value: Any) -> Any:
    try:
        json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(value)
    return value


def _errorish(value: Any) -> bool:
    """True when a decoded payload has the mocks' error-response shape."""
    if isinstance(value, str):
        text = value.strip()
        if not (text.startswith("{") or text.startswith("[")):
            return False
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            return False
    if isinstance(value, list):
        return any(_errorish(item) for item in value)
    if not isinstance(value, dict):
        return False
    if value.get("isError") is True or value.get("is_error") is True:
        return True
    if str(value.get("status", "")).lower() == "error":
        return True
    # ``error_response`` emits {"error": <message>, "code": <CODE>}. Require a
    # non-empty error field so a row with error=None/"" is not counted.
    return bool(value.get("error")) and "code" in value


def _tool_result_success(block: Any) -> bool:
    """Whether a tool call succeeded, judged structurally.

    A call is a failure only when the transport flags it, or when the payload
    itself has the mocks' error shape. The previous implementation scanned the
    serialized text for phrases like "not found", so a *successful* call whose
    results merely contained that wording was recorded as failed.
    """
    if _field(block, "is_error", False) or _field(block, "isError", False):
        return False
    content = _field(block, "content", "")
    return not _errorish(content)


def _content_blocks(message: Any) -> list[Any]:
    content = _field(message, "content", "")
    if isinstance(content, list):
        return content
    return []


def extract_assistant_text(messages: Iterable[Any]) -> str:
    """Port of the source ``_extract_assistant_text`` (joins with ``\\n``)."""
    chunks: list[str] = []
    for message in messages or []:
        if _field(message, "role") != "assistant":
            continue
        content = _field(message, "content", "")
        if isinstance(content, str):
            if content:
                chunks.append(content)
            continue
        for block in content or []:
            if _field(block, "type") == "text":
                text = _field(block, "text", "") or ""
                if text:
                    chunks.append(text)
    return "\n".join(chunks)


def extract_tool_calls(messages: Iterable[Any], event_id: str | None = None) -> list[dict[str, Any]]:
    """Port of the source ``_extract_tool_calls`` over ``role``/``content``."""
    calls: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    for message in messages or []:
        role = _field(message, "role")
        if role == "assistant":
            for block in _content_blocks(message):
                if _field(block, "type", "") not in ("toolCall", "tool_call", "tool_use"):
                    continue
                call = {
                    "event_id": event_id,
                    "id": _field(block, "id", _field(block, "tool_call_id", _field(block, "toolCallId"))),
                    "name": _field(block, "name"),
                    "arguments": _jsonable(_field(block, "arguments", _field(block, "input", {}))),
                    "success": None,
                    "result": None,
                }
                calls.append(call)
                if call["id"] is not None:
                    by_id[str(call["id"])] = call
        blocks = _content_blocks(message)
        if role in ("user", "tool", "toolResult", "tool_result") and not blocks:
            blocks = [message]
        for block in blocks:
            typ = _field(block, "type", "")
            if typ not in ("toolResult", "tool_result") and role not in (
                "tool",
                "toolResult",
                "tool_result",
            ):
                continue
            tool_id = _field(
                block,
                "tool_use_id",
                _field(block, "tool_call_id", _field(block, "toolCallId", _field(block, "id"))),
            )
            if tool_id is None:
                continue
            call = by_id.get(str(tool_id))
            if call is not None:
                call["success"] = _tool_result_success(block)
                call["result"] = _jsonable(_field(block, "content", ""))
    return calls


def _is_atif(trajectory: Any) -> bool:
    steps = trajectory.get("steps") if isinstance(trajectory, dict) else None
    return isinstance(steps, list) and any(
        isinstance(step, dict) and "source" in step for step in steps
    )


def _atif_window(trajectory: dict[str, Any]) -> list[dict[str, Any]]:
    """Turns after the last user turn — the work belonging to this step.

    Earlier turns belong to earlier steps; including them would replay every
    previous step's prose and tool calls into each later stage.
    """
    steps = [step for step in trajectory.get("steps") or [] if isinstance(step, dict)]
    last_user = -1
    for index, step in enumerate(steps):
        if str(step.get("source", "")).lower() == "user":
            last_user = index
    return steps[last_user + 1 :]


def atif_step_slice(trajectory: Any) -> dict[str, Any] | None:
    """This step's own turns, in the ATIF envelope the verifier expects.

    Harbor rewrites ``trajectory.json`` as the whole cumulative session on every
    step, so step N carries steps 1..N-1 verbatim. Freezing that per stage costs
    O(steps^2) on disk for no scoring value: the rubrics read only ``response``
    and ``trace``, and the last step's copy already holds the full session.
    Keep the envelope (``schema_version``/``session_id``/``agent``) so the file
    stays a valid ATIF document.

    Returns None for non-ATIF input, leaving the caller on its raw-bytes path.
    """
    if not _is_atif(trajectory):
        return None
    steps = [step for step in trajectory.get("steps") or [] if isinstance(step, dict)]
    last_user = -1
    for index, step in enumerate(steps):
        if str(step.get("source", "")).lower() == "user":
            last_user = index
    window = steps[last_user + 1 :]
    sliced = {key: value for key, value in trajectory.items() if key != "steps"}
    sliced["steps"] = window
    return sliced


def _atif_text(trajectory: dict[str, Any]) -> str:
    chunks: list[str] = []
    for step in _atif_window(trajectory):
        if str(step.get("source", "")).lower() != "agent":
            continue
        message = step.get("message")
        if isinstance(message, str) and message.strip():
            chunks.append(message)
        elif isinstance(message, list):
            for block in message:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text") or ""
                    if text:
                        chunks.append(text)
    return "\n".join(chunks)


def _atif_tool_calls(trajectory: dict[str, Any], event_id: str | None) -> list[dict[str, Any]]:
    """Pair ATIF ``tool_calls`` with ``observation.results`` by ``source_call_id``."""
    ordered: list[str] = []
    calls: dict[str, dict[str, Any]] = {}
    results: dict[str, Any] = {}
    for step in _atif_window(trajectory):
        if str(step.get("source", "")).lower() != "agent":
            continue
        for call in step.get("tool_calls") or []:
            if not isinstance(call, dict):
                continue
            call_id = str(call.get("tool_call_id") or call.get("id") or "")
            if not call_id or call_id in calls:
                continue
            name = call.get("function_name") or call.get("name")
            function = call.get("function")
            if isinstance(function, dict):
                name = name or function.get("name")
                arguments = function.get("arguments", call.get("arguments", {}))
            else:
                arguments = call.get("arguments", {})
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}
            calls[call_id] = {
                "event_id": event_id,
                "id": call_id,
                "name": str(name or ""),
                "arguments": arguments if isinstance(arguments, dict) else {},
                "success": None,
                "result": None,
            }
            ordered.append(call_id)
        observation = step.get("observation")
        rows = observation.get("results", []) if isinstance(observation, dict) else []
        for row in rows:
            if not isinstance(row, dict):
                continue
            call_id = str(row.get("source_call_id") or row.get("tool_call_id") or "")
            if call_id:
                results[call_id] = row.get("content")
    out: list[dict[str, Any]] = []
    for call_id in ordered:
        call = calls[call_id]
        if call_id in results:
            content = results[call_id]
            call["success"] = _tool_result_success({"content": content})
            call["result"] = _jsonable(content)
        out.append(call)
    return out


def _messages_for_step(trajectory: Any, step_name: str) -> list[Any]:
    """``role``/``content`` messages for this step, for non-ATIF dialects."""
    if not isinstance(trajectory, dict):
        return []
    steps = trajectory.get("steps")
    if isinstance(steps, list):
        for step in steps:
            if isinstance(step, dict) and step.get("name") == step_name:
                messages = step.get("messages")
                return messages if isinstance(messages, list) else []
        return []
    messages = trajectory.get("messages")
    return messages if isinstance(messages, list) else []


def _codex_session_items(path: Path) -> tuple[str, list[dict[str, Any]]]:
    """Read a Codex session JSONL into (prose, tool calls).

    Harbor's codex agent converts sessions to ATIF *on the host*, so the
    container only ever has ``/logs/agent/sessions/**/rollout-*.jsonl``. Reading
    it directly is what keeps the Tool Call and Final buckets scorable — without
    this the verifier sees an empty trajectory and those 20 points are
    unreachable no matter what the agent did.
    """
    texts: list[str] = []
    calls: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    outputs: dict[str, Any] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "", []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("type") != "response_item":
            continue
        payload = row.get("payload") or {}
        kind = payload.get("type")
        if kind == "message" and payload.get("role") == "assistant":
            for block in payload.get("content") or []:
                if isinstance(block, dict):
                    text = block.get("text") or ""
                    if text:
                        texts.append(text)
        elif kind == "function_call":
            call_id = str(payload.get("call_id") or "")
            if not call_id:
                continue
            args = payload.get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            calls[call_id] = {
                "event_id": None,
                "id": call_id,
                "name": str(payload.get("name") or ""),
                "arguments": args if isinstance(args, dict) else {},
                "success": None,
                "result": None,
            }
            order.append(call_id)
        elif kind == "function_call_output":
            call_id = str(payload.get("call_id") or "")
            if call_id:
                outputs[call_id] = payload.get("output")
    out: list[dict[str, Any]] = []
    for call_id in order:
        call = calls[call_id]
        if call_id in outputs:
            content = outputs[call_id]
            call["success"] = _tool_result_success({"content": content})
            call["result"] = _jsonable(content)
        out.append(call)
    return "\n".join(texts), out


def _load_trajectory(path: Path) -> Any:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def step_text_and_calls(
    trajectory: Any, step_name: str, event_id: str | None
) -> tuple[str, list[dict[str, Any]]]:
    """Prose and tool calls for one Harbor step, whichever dialect was written."""
    if not isinstance(trajectory, dict):
        return "", []
    if _is_atif(trajectory):
        return _atif_text(trajectory), _atif_tool_calls(trajectory, event_id)
    messages = _messages_for_step(trajectory, step_name)
    return extract_assistant_text(messages), extract_tool_calls(messages, event_id)
