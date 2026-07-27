from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from ..utils.exceptions import SinkOutsideWorkspace


_MEMORY_CHANNELS: dict[str, list[dict]] = {}


def deliver(sink_uri: str, payload: dict, workspace_root: Optional[str] = None) -> bool:
    """Attempt to deliver ``payload`` to ``sink_uri``.

    Supported schemes:
      - file://  appends one JSON line (\\n terminated) to an absolute path. When
        ``workspace_root`` is provided, the path must live under it.
      - memory:// enqueues to an in-process channel (inspect with ``memory_drain``).

    Returns True on success, False on any failure (no exception escapes).
    """
    try:
        parsed = urlparse(sink_uri)
    except Exception:
        return False

    scheme = parsed.scheme.lower()

    if scheme == "memory":
        channel = parsed.netloc or parsed.path.lstrip("/")
        _MEMORY_CHANNELS.setdefault(channel, []).append(payload)
        return True

    if scheme == "file":
        path = parsed.path
        if not path:
            return False
        if workspace_root:
            try:
                root = Path(workspace_root).resolve()
                p = Path(path).resolve()
                if not p.is_relative_to(root):
                    raise SinkOutsideWorkspace(
                        f"sink {path} not under workspace {root}"
                    )
            except SinkOutsideWorkspace:
                raise
            except Exception:
                return False
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
            return True
        except Exception:
            return False

    return False


def memory_drain(channel: str) -> list[dict]:
    """Pop and return all queued payloads for a memory:// channel (test helper)."""
    return _MEMORY_CHANNELS.pop(channel, [])


def memory_peek(channel: str) -> list[dict]:
    return list(_MEMORY_CHANNELS.get(channel, []))


def validate_file_sink(sink_uri: str, workspace_root: Optional[str]) -> None:
    """Raise SinkOutsideWorkspace if a file:// sink is outside ``workspace_root``.

    No-op for memory:// or when ``workspace_root`` is falsy.
    """
    if not workspace_root:
        return
    try:
        parsed = urlparse(sink_uri)
    except Exception:
        raise SinkOutsideWorkspace(f"invalid sink URI {sink_uri}")
    if parsed.scheme.lower() != "file":
        return
    path = parsed.path
    if not path:
        raise SinkOutsideWorkspace(f"invalid file sink {sink_uri}")
    root = Path(workspace_root).resolve()
    p = Path(path).resolve()
    if not p.is_relative_to(root):
        raise SinkOutsideWorkspace(
            f"sink {p} is outside workspace {root}"
        )
