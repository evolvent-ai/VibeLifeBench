"""Stage 7 — in the quiet period maintain an explicit monitoring and review."""
from __future__ import annotations

from ._helpers import record_text, text_has


def s7_quiet_monitor(env) -> bool:
    record = record_text(env, "decision_log.md")
    return text_has(record, [
        ["monitoring"], ["hr", "company"], ["progress", "progress", "progress"],
        ["review", "review"], ["inbox", "email"],
    ])


CHECKS = [("s7_quiet_monitor", s7_quiet_monitor, 1.0)]
