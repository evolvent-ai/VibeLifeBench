"""Trusted main-service collector for one Harbor turn.

This program runs only from Harbor's verifier collect phase, after Harbor has
uploaded the current agent logs and before the world-controller sidecar freezes
them.  It replaces, rather than merges with, the agent-writable staging bundle.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

SCENARIO_CLOCK_PATH = Path(
    os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json")
)
SCENARIO_CLOCK_REQUIRED = os.environ.get("WORLD_CLOCK_REQUIRED", "0") == "1"

ORACLE_STDOUT_FILE = "oracle.txt"
ORACLE_EXIT_CODE_FILE = "exit-code.txt"

from response_capture import (  # noqa: E402
    _codex_session_items,
    _jsonable,
    _load_trajectory,
    _tool_result_success,
    atif_step_slice,
    step_text_and_calls,
)

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if not isinstance(payload.get("step"), str) or not isinstance(payload.get("now"), str):
            raise ValueError("invalid scenario clock payload")
        parsed = datetime.fromisoformat(payload["now"].replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("scenario clock must include an offset")
        return {
            "schema_version": 1,
            "step": payload["step"],
            "now": parsed.isoformat(),
        }
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}"
            ) from exc
        now = datetime.now(timezone.utc).isoformat()
        return {"schema_version": 1, "step": "unknown", "now": now}


def utc_now() -> str:
    return scenario_clock()["now"]


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )


def _latest_session(logs_root: Path) -> Path | None:
    candidates = [
        path
        for pattern in ("sessions/**/rollout-*.jsonl", "sessions/**/*.jsonl")
        for path in logs_root.glob(pattern)
        if path.is_file() and not path.is_symlink()
    ]
    return max(candidates, key=lambda path: path.stat().st_mtime_ns) if candidates else None


def _oracle_run_marker(workspace_root: Path, logs_root: Path) -> bool:
    """Legacy compatibility hook; workspace files never identify Oracle runs.

    Evidence source selection is trajectory-first for both Oracle and real
    agents.  Harbor owns the lifecycle around ``oracle.txt``/``exit-code.txt``;
    a file created by the agent in ``/workspace`` is never sufficient.
    """
    return False


def _oracle_exit_code(logs_root: Path) -> None:
    """Fail closed when Harbor recorded a non-zero Oracle solution exit."""
    path = logs_root / ORACLE_EXIT_CODE_FILE
    if not path.is_file():
        return
    raw = path.read_text(encoding="utf-8").strip()
    try:
        code = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"invalid Oracle exit code in {path}: {raw!r}") from exc
    if code != 0:
        raise RuntimeError(f"Oracle solution exited with code {code}")


def _session_mcp_calls(path: Path, event_id: str | None) -> list[dict[str, Any]]:
    """Extract task MCP calls from Codex rollout JSONL."""
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or '"McpToolCall"' not in line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("type") != "event_msg":
            continue
        payload = row.get("payload") or {}
        if payload.get("type") != "item_completed":
            continue
        item = payload.get("item") or {}
        if item.get("type") != "McpToolCall":
            continue
        server = str(item.get("server") or "")
        tool = str(item.get("tool") or "")
        if not server or not tool or server == "codex":
            continue
        result = item.get("result")
        result_block = dict(item)
        result_block["content"] = result
        out.append({
            "event_id": event_id,
            "id": str(item.get("id") or ("mcp-%d" % len(out))),
            "name": f"{server}__{tool}",
            "arguments": item.get("arguments") if isinstance(item.get("arguments"), dict) else {},
            "success": str(item.get("status") or "").lower() == "completed"
            and _tool_result_success(result_block),
            "result": _jsonable(result),
        })
    return out




def _empty_atif_bytes() -> bytes:
    return (
        json.dumps(
            {"schema_version": "ATIF-v1.7", "steps": []},
            ensure_ascii=False,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _trajectory_document_valid(trajectory: Any) -> bool:
    """Accept the ATIF/legacy containers emitted by Harbor, not arbitrary JSON."""
    if not isinstance(trajectory, dict):
        return False
    steps = trajectory.get("steps")
    messages = trajectory.get("messages")
    return isinstance(steps, list) or isinstance(messages, list)


def _validate_session_jsonl(path: Path) -> None:
    """Fail closed when a discovered Codex session is empty or malformed."""
    try:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError as exc:
        raise RuntimeError(f"unreadable Harbor session log: {path}") from exc
    if not lines:
        raise RuntimeError(f"empty Harbor session log: {path}")
    for line_number, line in enumerate(lines, start=1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"invalid Harbor session JSONL at {path}:{line_number}"
            ) from exc
        if not isinstance(row, dict):
            raise RuntimeError(
                f"invalid Harbor session record at {path}:{line_number}"
            )


def _trajectory_and_items(
    logs_root: Path, step_name: str, source_event_id: str, *, workspace_root: Path | None = None
) -> tuple[bytes, str, list[dict[str, Any]], str, Path | None]:
    workspace_root = Path(workspace_root) if workspace_root is not None else Path("/workspace")
    # Oracle and real agents publish the same native trajectory contract.  Do
    # not inspect or trust any workspace call log when choosing the source.
    _oracle_exit_code(logs_root)

    if not logs_root.is_dir():
        raise RuntimeError(f"Harbor agent log directory is unavailable: {logs_root}")
    if not any(logs_root.iterdir()):
        # Harbor's native NopAgent intentionally emits no files. Preserve that
        # fact as an explicit empty turn instead of treating it as telemetry loss.
        return _empty_atif_bytes(), "", [], "empty-agent-log", None

    trajectory_path = logs_root / "trajectory.json"
    trajectory_valid = False
    if trajectory_path.exists():
        if not trajectory_path.is_file() or trajectory_path.is_symlink():
            raise RuntimeError(f"invalid Harbor trajectory path: {trajectory_path}")
        raw = trajectory_path.read_bytes()
        trajectory = _load_trajectory(trajectory_path)
        trajectory_valid = _trajectory_document_valid(trajectory)
        if not trajectory_valid:
            raise RuntimeError(f"invalid Harbor trajectory: {trajectory_path}")
        # Freeze only this step's turns; see atif_step_slice for why. Falls back
        # to the raw bytes whenever the document is a valid legacy container.
        sliced = atif_step_slice(trajectory)
        if sliced is not None:
            raw = (
                json.dumps(sliced, ensure_ascii=False, sort_keys=True, allow_nan=False)
                + "\n"
            ).encode("utf-8")
        text, calls = step_text_and_calls(trajectory, step_name, source_event_id)
        if text.strip() or calls:
            # Unified exec records MCP calls inside session event messages while
            # ATIF may expose only function_name="exec"; merge structured calls.
            session_path = _latest_session(logs_root)
            if session_path is not None:
                try:
                    calls = calls + _session_mcp_calls(session_path, source_event_id)
                except (OSError, ValueError):
                    # Keep the trajectory evidence if session parsing is unavailable.
                    pass
            return raw, text, calls, "trajectory.json", None
    else:
        raw = _empty_atif_bytes()

    session_path = _latest_session(logs_root)
    if session_path is not None:
        _validate_session_jsonl(session_path)
        text, calls = _codex_session_items(session_path)
        for call in calls:
            call["event_id"] = source_event_id
        return raw, text, calls, "session.jsonl", session_path
    if trajectory_valid:
        # A valid empty ATIF document is legitimate for a no-op/empty response.
        return raw, "", [], "trajectory.json", None
    raise RuntimeError("Harbor produced neither a valid trajectory nor a session log")


def _replace_directory(tmp: Path, target: Path) -> None:
    old: Path | None = None
    if target.exists() or target.is_symlink():
        old = target.parent / f".{target.name}.old-{os.getpid()}"
        if old.exists() or old.is_symlink():
            if old.is_dir() and not old.is_symlink():
                shutil.rmtree(old)
            else:
                old.unlink()
        os.replace(target, old)
    try:
        os.replace(tmp, target)
    except Exception:
        if old is not None and old.exists() and not target.exists():
            os.replace(old, target)
        raise
    if old is not None:
        if old.is_dir() and not old.is_symlink():
            shutil.rmtree(old)
        elif old.exists() or old.is_symlink():
            old.unlink()


def collect_turn(
    *,
    workspace_root: Path,
    logs_root: Path,
    step_name: str,
    virtual_stage: int,
    source_event_id: str,
    stage_boundary: bool,
) -> Path:
    """Replace the current staging bundle with evidence from this Harbor turn."""
    workspace_root = Path(workspace_root)
    logs_root = Path(logs_root)
    stage_root = workspace_root / ".harbor-stage"
    stage_root.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=".current.tmp-", dir=stage_root))
    target = stage_root / "current"
    try:
        raw, text, calls, trajectory_source, session_path = _trajectory_and_items(
            logs_root, step_name, source_event_id, workspace_root=workspace_root
        )
        (tmp / "trajectory.json").write_bytes(raw)
        (tmp / "response.txt").write_text(text, encoding="utf-8")
        _write_json(tmp / "trace.json", calls)
        if session_path is not None:
            shutil.copy2(session_path, tmp / "session.jsonl")


        metadata = {
            "schema_version": 1,
            "step": step_name,
            "virtual_stage": virtual_stage,
            "source_event_id": source_event_id,
            "stage_boundary": bool(stage_boundary),
            "trajectory_source": trajectory_source,
            "captured_at": utc_now(),
            "scenario_clock": scenario_clock(),
        }
        _write_json(tmp / "metadata.json", metadata)
        _replace_directory(tmp, target)
        return target
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("step_name")
    parser.add_argument("virtual_stage", type=int)
    parser.add_argument("source_event_id")
    parser.add_argument("stage_boundary", choices=("0", "1"))
    args = parser.parse_args(argv)
    collect_turn(
        workspace_root=Path("/workspace"),
        logs_root=Path("/logs/agent"),
        step_name=args.step_name,
        virtual_stage=args.virtual_stage,
        source_event_id=args.source_event_id,
        stage_boundary=args.stage_boundary == "1",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
