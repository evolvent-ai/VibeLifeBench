"""Shared service helpers — extract title from properties, current ISO time."""
import json
import sqlite3
from typing import Any, Dict, Optional

from ..utils.dates import DEFAULT_WRITE_TIME


def now_for(conn: sqlite3.Connection) -> str:  # noqa: ARG001
    """Return the Notion-style ISO timestamp used for newly-written rows.

    v3 has no simulated clock. The server stamps every write with
    ``DEFAULT_WRITE_TIME`` so timestamps are deterministic relative to
    the env. Tasks that need a different timestamp set it directly via
    event-yaml mutations.
    """
    return DEFAULT_WRITE_TIME


def extract_title(properties: Dict[str, Any]) -> str:
    """Pull a plain-text title out of a Notion-style properties dict.

    Looks for ``properties.title`` first (real Notion page convention),
    then for the first ``type == "title"`` property if the schema uses a
    custom property name (e.g. database rows).
    """
    if not isinstance(properties, dict):
        return ""
    candidates = []
    if "title" in properties:
        candidates.append(properties["title"])
    for v in properties.values():
        if isinstance(v, dict) and v.get("type") == "title":
            candidates.append(v)
    for cand in candidates:
        if isinstance(cand, dict):
            rich = cand.get("title") or cand.get("rich_text") or []
            if isinstance(rich, list) and rich:
                parts = []
                for chunk in rich:
                    if isinstance(chunk, dict):
                        t = chunk.get("plain_text")
                        if t is None and isinstance(chunk.get("text"), dict):
                            t = chunk["text"].get("content", "")
                        parts.append(t or "")
                joined = "".join(parts).strip()
                if joined:
                    return joined
        elif isinstance(cand, str):
            return cand
    return ""


def dump_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def parse_json_col(s: Optional[str], default: Any) -> Any:
    if s is None or s == "":
        return default
    try:
        return json.loads(s)
    except (TypeError, ValueError):
        return default
