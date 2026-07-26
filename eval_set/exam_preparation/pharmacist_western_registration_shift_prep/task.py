"""HF task runner for western-pharmacist registration and shift-study prep."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

from loguru import logger
from terrarium.models.checker import CheckerResults
from terrarium.task.decorator import entry

from capabilities import agent_caps_config
from hf.lib.handbook_task_runtime import (
    bootstrap_workspace,
    dispatch_event,
    load_events,
    persist_environment_fingerprint as _persist_environment_fingerprint,
    persist_stage_score as _persist_stage_score,
    register_all_mcp,
    run_rubric_checks,
)

THIS_DIR = Path(__file__).resolve().parent
RESPONSES_DIR = "/terrarium/agent_responses"
TRACE_DIR = "/terrarium/agent_traces"
SCORES_DIR = "/terrarium/stage_scores"
SNAPSHOTS_DIR = "/terrarium/stage_snapshots"
SERVICES = ("notification_hub", "ecommerce", "calendar", "email", "notion")

_CAPABILITIES_CONFIG = agent_caps_config(
    notification_hub_mock="pharmacist_western_registration_shift_prep",
    ecommerce_mock="pharmacist_western_registration_shift_prep",
    calendar_mock="pharmacist_western_registration_shift_prep",
    email_mock="pharmacist_western_registration_shift_prep",
    notion_mock="pharmacist_western_registration_shift_prep",
)


def _rubric_pkg_name() -> str:
    for path in sys.path:
        try:
            relative = THIS_DIR.relative_to(Path(path).resolve())
        except ValueError:
            continue
        return ".".join(relative.parts) + ".rubrics"
    raise RuntimeError(f"cannot derive rubric package for {THIS_DIR}")


_RUBRIC_PKG = _rubric_pkg_name()


def _expected_stage_count() -> int:
    count = 0
    for path in (THIS_DIR / "rubrics").glob("stage_*.py"):
        try:
            count = max(count, int(path.stem.split("_", 1)[1]) + 1)
        except (IndexError, ValueError):
            continue
    return count


def _load_rubric(name: str):
    return importlib.import_module(f"{_RUBRIC_PKG}.{name}")


@entry(
    capabilities=[
        "notification_hub_mock",
        "ecommerce_mock",
        "calendar_mock",
        "email_mock",
        "notion_mock",
        "workspace",
    ],
    capabilities_config=_CAPABILITIES_CONFIG,
)
def pharmacist_western_registration_shift_prep(env, agent):
    register_all_mcp(env, agent)
    bootstrap_workspace(env, THIS_DIR)

    event_stage_count, events_by_stage = load_events(THIS_DIR / "event.yaml")
    stage_count = max(_expected_stage_count(), event_stage_count)
    stage_modules = {stage: _load_rubric(f"stage_{stage}") for stage in range(stage_count)}

    all_checks = []
    total_weight = 0.0
    passed_weight = 0.0

    for stage_idx in range(stage_count):
        events = sorted(
            events_by_stage.get(stage_idx, []),
            key=lambda event: (str(event.get("time", "")), str(event.get("id", ""))),
        )
        responses: list[str] = []
        tool_calls: list[dict] = []
        for event in events:
            text, calls = dispatch_event(event, env, agent, THIS_DIR)
            if text:
                responses.append(text)
            tool_calls.extend(calls)

        env.workspace.fs.write_file(
            f"{RESPONSES_DIR}/stage_{stage_idx}.txt",
            "\n---\n".join(responses).encode("utf-8"),
        )
        env.workspace.fs.write_file(
            f"{TRACE_DIR}/stage_{stage_idx}.json",
            json.dumps(tool_calls, ensure_ascii=False, indent=2).encode("utf-8"),
        )
        _persist_environment_fingerprint(env, stage_idx, SERVICES)
        checks, stage_total, stage_passed = run_rubric_checks(
            stage_modules[stage_idx].CHECKS, env, f"stage{stage_idx}"
        )
        _persist_stage_score(env, stage_idx, checks, stage_total, stage_passed)
        all_checks.extend(checks)
        total_weight += stage_total
        passed_weight += stage_passed

    for name, tag in (("final", "final"), ("cross_stage", "cross_stage")):
        checks, bucket_total, bucket_passed = run_rubric_checks(
            _load_rubric(name).CHECKS, env, tag
        )
        all_checks.extend(checks)
        total_weight += bucket_total
        passed_weight += bucket_passed

    score = (passed_weight / total_weight) if total_weight else 0.0
    logger.info(
        f"flat-pool score: passed={passed_weight:.2f} total={total_weight:.2f} score={score:.3f}"
    )
    return CheckerResults(checks=all_checks, score=score)
