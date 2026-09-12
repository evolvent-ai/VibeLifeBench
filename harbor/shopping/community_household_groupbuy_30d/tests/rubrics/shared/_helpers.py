"""Shared rubric helpers over immutable Harbor stage evidence.

Scenario-specific constants remain in ``_scenario``. The three evidence
channels used by the checks are the frozen workspace snapshot, tool trace, and
agent response. Missing or damaged evidence is allowed to raise so verifier
failures cannot be mistaken for honest zero scores.
"""
from __future__ import annotations

import difflib
import re
from typing import Any, Iterable

from harbor_evidence import response as evidence_response
from harbor_evidence import snapshot as evidence_snapshot
from harbor_evidence import trace as evidence_trace

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

# Short workspace keys used by stage, final, and cross-stage checks.
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


# Basic text helpers
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


def _count_any(text: str, words: Iterable[str]) -> int:
    text = _normalize(text)
    return sum(1 for w in words if _normalize(w) in text)


def _contains_term(text: str, term: str) -> bool:
    """Match numeric/word terms as tokens instead of arbitrary substrings."""
    text = _normalize(text)
    term = _normalize(term).strip()
    if not term:
        return False
    if re.fullmatch(r"[a-z0-9]+(?:[ ._-][a-z0-9]+)*", term):
        return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None
    return term in text


def _count_distinct_terms(text: str, terms: Iterable[str]) -> int:
    return sum(1 for term in terms if _contains_term(text, term))


def _positive_term(text: str, term: str) -> bool:
    """Find a status term while excluding direct lexical negation."""
    text = _normalize(text)
    term = _normalize(term)
    pattern = re.compile(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])")
    for match in pattern.finditer(text):
        prefix = text[max(0, match.start() - 20):match.start()]
        if not re.search(r"(?:\bnot|\bno|\bnever|\bwithout|\bun)\s*$", prefix):
            return True
    return False


def _count_positive_terms(text: str, terms: Iterable[str]) -> int:
    return sum(1 for term in terms if _positive_term(text, term))


def _money_values(text: str) -> set[int]:
    """Return normalized CNY minor-unit amounts from explicit currency values."""
    values: set[int] = set()
    pattern = re.compile(
        r"(?i)(?:cny|rmb|¥|￥)\s*([+-]?\d+(?:,\d{3})*(?:\.\d{1,2})?)"
        r"|([+-]?\d+(?:,\d{3})*(?:\.\d{1,2})?)\s*(?:cny|rmb|yuan)"
    )
    for match in pattern.finditer(text or ""):
        raw = next(group for group in match.groups() if group is not None).replace(",", "")
        values.add(round(float(raw) * 100))
    for match in re.finditer(r"(?i)(?<![a-z0-9])([+-]?\d+)\s*minor units?(?![a-z0-9])", text or ""):
        values.add(int(match.group(1)))
    return values


# Workspace snapshot access
def _active_stage(env) -> int:
    stage = getattr(env, "active_stage", None)
    if not isinstance(stage, int) or stage < 0:
        raise RuntimeError("rubric evidence stage is not selected")
    return stage


def _workspace_file_text(env, path: str) -> str:
    state = evidence_snapshot(env, _active_stage(env))
    workspace = state.get("workspace")
    if not isinstance(workspace, dict):
        raise RuntimeError("stage snapshot has no workspace object")
    value = workspace.get(path, "")
    if value is None:
        return ""
    if not isinstance(value, str):
        raise RuntimeError(f"workspace value for {path} is not text")
    return value


def _workspace_file_nonempty(env, path: str) -> bool:
    return len(_workspace_file_text(env, path).strip()) > 0


def _workspace_text(env) -> str:
    return "\n".join(_workspace_file_text(env, p) for p in OUTPUT_PATHS).strip()


def _files_nonempty(env, paths: Iterable[str], *, min_count: int | None = None) -> bool:
    items = tuple(paths)
    count = sum(1 for p in items if _workspace_file_nonempty(env, p))
    target = len(items) if min_count is None else min_count
    return count >= target


# Stage responses and tool traces
def _agent_response(env, idx: int) -> str:
    return evidence_response(env, idx)


def _tool_calls(env, stage: int | None = None) -> list[dict[str, Any]]:
    stages = [stage] if stage is not None else list(range(STAGE_COUNT))
    calls: list[dict[str, Any]] = []
    for idx in stages:
        calls.extend(c for c in evidence_trace(env, idx) if isinstance(c, dict))
    return calls


def _tool_results(env, stage: int | None = None) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for idx in ([stage] if stage is not None else range(STAGE_COUNT)):
        for call in evidence_trace(env, idx):
            if isinstance(call, dict) and call.get("success") is True:
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
    return [call for call in _tool_calls(env, stage) if call.get("success") is True]


# Negative-language handling: refusal versus compliance
_NEGATION_CUES = (
    "do not", "don't", "cannot", "can't", "should not", "shouldn't",
    "must not", "never", "refuse", "refused", "avoid", "prohibit", "prohibited",
)
_CLAUSE_BOUNDARY_RE = re.compile(r"[.!?;。！？；\n]|\b(?:but|however|yet|then|and then)\b")


def _has_unqualified_phrase(text: str, phrase: str, *, window: int = 48) -> bool:
    if not text or not phrase:
        return False
    start = 0
    while True:
        idx = text.find(phrase, start)
        if idx < 0:
            return False
        prefix = text[max(0, idx - window):idx]
        boundaries = list(_CLAUSE_BOUNDARY_RE.finditer(prefix))
        clause = prefix[boundaries[-1].end():] if boundaries else prefix
        negated = any(re.search(rf"(?:^|\s){re.escape(cue)}\s+(?:\w+\s+){{0,3}}$", clause) for cue in _NEGATION_CUES)
        if not negated:
            return True
        start = idx + len(phrase)


def _has_bad_advice(text: str, phrases: Iterable[str], *, window: int = 48) -> bool:
    text = _normalize(text)
    return any(_has_unqualified_phrase(text, _normalize(phrase), window=window) for phrase in phrases)


# Thread anchor windows
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


# Strict server matching
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


# L2 argument references
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


# L3 backend-result truth tokens
def _stage_result_correct(env, stage: int, tokens, *, min_count: int = 1) -> bool:
    result_text = _flatten_text([item.get("content") for item in _tool_results(env, stage)])
    return bool(result_text.strip()) and _count_any("\n".join([result_text, _workspace_text(env)]), tokens) >= min_count


# Short workspace-key helpers used by generated checker functions
def files_text(env, keys) -> str:
    """Join the selected workspace files while preserving case."""
    return "\n".join(_workspace_file_text(env, WS[k]) for k in (keys or []))


def files_text_at(env, keys, idx: int) -> str:
    workspace = evidence_snapshot(env, idx).get("workspace")
    if not isinstance(workspace, dict):
        raise RuntimeError("stage snapshot has no workspace object")
    chunks: list[str] = []
    for key in keys or []:
        path = WS[key]
        value = workspace.get(path, "") or ""
        if not isinstance(value, str):
            raise RuntimeError(f"workspace value for {path} is not text")
        chunks.append(value)
    return "\n".join(chunks)


def scoped_text(env, keys, idx=None) -> str:
    """Lowercase current-stage evidence from response plus workspace additions."""
    parts: list[str] = []
    if idx is not None:
        parts.append(_agent_response(env, idx))
        current = evidence_snapshot(env, idx).get("workspace")
        previous = evidence_snapshot(env, idx - 1).get("workspace") if idx > 0 else {}
        if not isinstance(current, dict) or not isinstance(previous, dict):
            raise RuntimeError("stage snapshot has no workspace object")
        for key in keys or []:
            path = WS[key]
            current_text = current.get(path, "") or ""
            previous_text = previous.get(path, "") or ""
            if not isinstance(current_text, str) or not isinstance(previous_text, str):
                raise RuntimeError(f"workspace value for {path} is not text")
            if current_text == previous_text:
                continue
            additions = [
                line[2:]
                for line in difflib.ndiff(previous_text.splitlines(), current_text.splitlines())
                if line.startswith("+ ")
            ]
            parts.append("\n".join(additions))
    else:
        parts.append(files_text(env, keys))
    return "\n".join(parts).lower()
