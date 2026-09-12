"""Rubric predicate documentation."""
from __future__ import annotations

import json
import re
from typing import Any, Iterable

from harbor_evidence import response, snapshot, trace

from ._scenario import (
    ALL_SERVERS,
    OUTPUT_PATHS,
    STAGE_COUNT,
    STAGE_EXPECTED_SERVERS,
    THREAD_IDS,
    THREAD_LABELS as _THREAD_LABELS,
    THREAD_TERMS as _THREAD_TERMS,
    THREAD_EVIDENCE as _THREAD_EVIDENCE,
)

CORE_WORKSPACE_PATHS = (
    "/workspace/order_tracker.md",
    "/workspace/decision_log.md",
    "/workspace/risk_register.md",
    "/workspace/HEARTBEAT.md",
)
WS = {
    "gear": "/workspace/gear_plan.md",
    "budget": "/workspace/budget.md",
    "decision": "/workspace/decision_log.md",
    "risk": "/workspace/risk_register.md",
    "tracker": "/workspace/order_tracker.md",
    "evidence": "/workspace/evidence_log.md",
    "summary": "/workspace/final_summary.md",
    "heartbeat": "/workspace/HEARTBEAT.md",
}
def _flatten_text(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (int, float, bool)):
        return str(obj)
    if isinstance(obj, list):
        return "\n".join(_flatten_text(x) for x in obj)
    if isinstance(obj, dict):
        return "\n".join(_flatten_text(v) for v in obj.values())
    return ""


def _normalize(text: str) -> str:
    return (text or "").lower()


def _any(text: str, words: Iterable[str]) -> bool:
    text = _normalize(text)
    return any(_normalize(w) in text for w in words)


def _contains_all(text: str, words: Iterable[str]) -> bool:
    text = _normalize(text)
    return all(_normalize(w) in text for w in words)


def _count_any(text: str, words: Iterable[str]) -> int:
    text = _normalize(text)
    return sum(1 for w in words if _normalize(w) in text)


def _number_count(text: str) -> int:
    if not text:
        return 0
    return len(re.findall(r"(?<!\d)\d+(?:,\d{3})*(?:\.\d+)?(?!\d)", text))
def _latest_stage(env) -> int:
    stages = env.published_stages()
    if not stages:
        raise RuntimeError("no published stage evidence")
    return max(stages)


def _workspace_file_text(env, path: str) -> str:
    workspace = snapshot(env, _latest_stage(env)).get("workspace")
    if not isinstance(workspace, dict):
        raise RuntimeError("frozen snapshot workspace is not an object")
    value = workspace.get(path, "")
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return _flatten_text(value)


def _workspace_file_nonempty(env, path: str) -> bool:
    return len(_workspace_file_text(env, path).strip()) > 0


def _workspace_text(env) -> str:
    return "\n".join(_workspace_file_text(env, p) for p in OUTPUT_PATHS).strip()


def _all_files_text(env, paths: Iterable[str]) -> str:
    return "\n".join(_workspace_file_text(env, p) for p in paths).strip()


def _files_nonempty(env, paths: Iterable[str], *, min_count: int | None = None) -> bool:
    items = tuple(paths)
    count = sum(1 for p in items if _workspace_file_nonempty(env, p))
    target = len(items) if min_count is None else min_count
    return count >= target


def _file_contains_all(env, path: str, words: Iterable[str]) -> bool:
    return _contains_all(_workspace_file_text(env, path), words)


def _file_contains_at_least(env, path: str, words: Iterable[str], min_count: int) -> bool:
    return _count_any(_workspace_file_text(env, path), words) >= min_count
def _agent_response(env, idx: int) -> str:
    return response(env, idx)


def _all_agent_responses(env) -> str:
    return "\n".join(_agent_response(env, i) for i in range(STAGE_COUNT)).strip()


def _stage_corpus(env, idx: int) -> str:
    return "\n".join([_agent_response(env, idx), _workspace_text(env)]).lower()


def _tool_calls(env, stage: int | None = None) -> list[dict[str, Any]]:
    stages = [stage] if stage is not None else list(range(STAGE_COUNT))
    calls: list[dict[str, Any]] = []
    for idx in stages:
        payload = trace(env, idx)
        calls.extend(call for call in payload if isinstance(call, dict))
    return calls


def _tool_results(env, stage: int | None = None) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for idx in ([stage] if stage is not None else range(STAGE_COUNT)):
        for call in trace(env, idx):
            if not isinstance(call, dict) or call.get("success") is not True:
                continue
            results.append(
                {
                    "tool_call_id": call.get("id"),
                    "name": call.get("name"),
                    "content": call.get("result"),
                    "is_error": False,
                }
            )
    return results


def _successful_tool_calls(env, stage: int) -> list[dict[str, Any]]:
    results = _tool_results(env, stage)
    result_ids = {str(item.get("tool_call_id")) for item in results if item.get("tool_call_id") is not None}
    result_names = {_normalize(str(item.get("name") or "")) for item in results if item.get("name")}
    return [call for call in _tool_calls(env, stage) if str(call.get("id")) in result_ids or _normalize(str(call.get("name") or "")) in result_names]


def _tool_name_matches(name: str, server: str | None = None, tool: str | None = None) -> bool:
    norm = _normalize(name).replace("-", "_")
    if server:
        server_norm = _normalize(server).replace("-", "_")
        if not (norm.startswith(f"{server_norm}__") or norm.startswith(f"{server_norm}_")):
            return False
    if tool:
        tool_norm = _normalize(tool).replace("-", "_")
        return norm == tool_norm or norm.endswith(f"__{tool_norm}") or norm.endswith(f"_{tool_norm}")
    return bool(norm)


def _agent_used_tool(env, server: str | None = None, tool: str | None = None, *, stage: int | None = None) -> bool:
    return any(_tool_name_matches(str(call.get("name") or ""), server, tool) for call in _tool_calls(env, stage))
_NEGATION_CUES = (
    "do not", "don't", "cannot", "should not", "must not", "not recommended",
    "prohibited", "never", "refuse", "refused", "avoid", "please do not",
)


def _has_unqualified_phrase(text: str, phrase: str, *, window: int = 12) -> bool:
    if not text or not phrase:
        return False
    start = 0
    while True:
        idx = text.find(phrase, start)
        if idx < 0:
            return False
        context_start = max(0, idx - window)
        context = text[context_start:idx + min(len(phrase), 4)]
        negated = False
        for cue in _NEGATION_CUES:
            cue_idx = context.find(cue)
            if cue_idx >= 0 and context_start + cue_idx < idx:
                negated = True
                break
        if not negated:
            return True
        start = idx + len(phrase)


def _has_bad_advice(text: str, phrases: Iterable[str], *, window: int = 12) -> bool:
    text = _normalize(text)
    return any(_has_unqualified_phrase(text, _normalize(phrase), window=window) for phrase in phrases)
def _thread_anchor_windows(text: str, thread_id: str, *, window: int = 320) -> list[str]:
    text = _normalize(text)
    positions: set[int] = set()
    for label in _THREAD_LABELS.get(thread_id, [thread_id]):
        needle = _normalize(label)
        if not needle:
            continue
        start = 0
        while True:
            idx = text.find(needle, start)
            if idx < 0:
                break
            positions.add(idx)
            start = idx + max(1, len(needle))
    return [
        text[max(0, idx - 40):min(len(text), idx + window)]
        for idx in sorted(positions)
    ]


def _thread_anchor_window(text: str, thread_id: str, *, window: int = 320) -> str:
    blocks = _thread_anchor_windows(text, thread_id, window=window)
    if not blocks:
        return ""
    ranking_terms = _THREAD_TERMS.get(thread_id, ())
    return max(blocks, key=lambda block: _count_any(block, ranking_terms))


def _thread_block_has_terms(text: str, thread_id: str, terms: Iterable[str], *, min_count: int = 2, window: int = 300) -> bool:
    required_terms = tuple(terms)
    return any(
        _count_any(block, required_terms) >= min_count
        for block in _thread_anchor_windows(text, thread_id, window=window)
    )


def _tracker_has_all_threads(text: str) -> bool:
    text = _normalize(text)
    return all(bool(_thread_anchor_windows(text, tid)) for tid in THREAD_IDS)


def _thread_sections_distinct(text: str) -> bool:
    text = text or ""
    return all(
        _thread_block_has_terms(text, tid, _THREAD_TERMS[tid], min_count=2)
        for tid in THREAD_IDS
    )


def _thread_evidence_complete(text: str, thread_id: str) -> bool:
    return _thread_block_has_terms(text, thread_id, _THREAD_EVIDENCE[thread_id], min_count=3, window=380)
def _stage_called_servers(env, stage: int) -> list[str]:
    seen: list[str] = []
    for call in _successful_tool_calls(env, stage):
        name = _normalize(str(call.get("name") or "")).replace("-", "_")
        srv = None
        for s in ALL_SERVERS:
            if name.startswith(f"{s}__") or name.startswith(f"{s}_"):
                srv = s
                break
        if srv and srv not in seen:
            seen.append(srv)
    return seen


def _stage_servers_correct(env, stage: int, *, min_count: int | None = None, allow_extra: bool = True) -> bool:
    expected = STAGE_EXPECTED_SERVERS.get(stage, [])
    if not expected:
        return False
    called_set = set(_stage_called_servers(env, stage))
    hit = sum(1 for s in expected if s in called_set)
    target = len(expected) if min_count is None else min_count
    if hit < target:
        return False
    if not allow_extra:
        extra = [s for s in called_set if s not in set(expected)]
        if extra:
            return False
    return True


def _stage_server_order_ok(env, stage: int, ordered_servers: list[str]) -> bool:
    called = _stage_called_servers(env, stage)
    pos = 0
    for s in called:
        if pos < len(ordered_servers) and s == ordered_servers[pos]:
            pos += 1
    return pos == len(ordered_servers)
def _stage_tool_args_text(env, stage: int, server: str | None = None) -> str:
    chunks: list[str] = []
    for call in _successful_tool_calls(env, stage):
        name = _normalize(str(call.get("name") or "")).replace("-", "_")
        if server:
            sv = _normalize(server).replace("-", "_")
            if not (name.startswith(f"{sv}__") or name.startswith(f"{sv}_")):
                continue
        chunks.append(_flatten_text(call.get("arguments")))
    return _normalize("\n".join(chunks))


def _stage_tool_args_reference(env, stage: int, tokens, *, server: str | None = None, min_count: int = 1) -> bool:
    return _count_any(_stage_tool_args_text(env, stage, server), tokens) >= min_count
def _stage_result_correct(env, stage: int, tokens, *, min_count: int = 1) -> bool:
    result_text = _flatten_text([item.get("content") for item in _tool_results(env, stage)])
    return bool(result_text.strip()) and _count_any("\n".join([result_text, _workspace_text(env)]), tokens) >= min_count
def files_text(env, keys) -> str:
    """Rubric predicate documentation."""
    return "\n".join(_workspace_file_text(env, WS[k]) for k in (keys or []))


def scoped_text(env, keys, idx=None) -> str:
    """Rubric predicate documentation."""
    parts = [files_text(env, keys)]
    if idx is not None:
        parts.append(_agent_response(env, idx))
    return "\n".join(parts).lower()


def _backend_text(env, server: str, tool: str, **kwargs) -> str | None:
    """Read the corresponding service projection from frozen stage state."""
    service = snapshot(env, _latest_stage(env)).get(server)
    if not isinstance(service, dict):
        return None
    key = {("ecommerce", "get_cart"): "cart"}.get((server, tool), tool)
    raw = service.get(key)
    return _flatten_text(raw).lower() if raw is not None else None


def _backend_state_has(env, server: str, tool: str, tokens, *, min_count: int = 1, **kwargs) -> bool:
    """Rubric predicate documentation."""
    text = _backend_text(env, server, tool, **kwargs)
    return bool(text) and _count_any(text, tokens) >= min_count
