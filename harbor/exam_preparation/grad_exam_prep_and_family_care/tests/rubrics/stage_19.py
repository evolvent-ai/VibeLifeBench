from __future__ import annotations
from ._helpers import *


def r36_health_stability_and_quiet_boundary_logged(env) -> bool:
    try:
        durable = wfile(env, "HEALTH_LOG.md") + "\n" + wfile(env, "HEARTBEAT.md") + "\n" + _notion_text(env)
        return (
            _stage_trace_all(env, 19, [["health_tracker"], ["get_metrics"], ["notion"], ["api-patch-block-children"]])
            and count_hits(durable, [["3/10", "pain3", "pain 3"], ["stable", "improved"], ["pre-exam", "quiet", "do not disturb"], ["exception", "seek care", "Dr. Wang"]]) == 4
        )
    except Exception:
        return False


CHECKS = [("r36_health_stability_and_quiet_boundary_logged", r36_health_stability_and_quiet_boundary_logged, 1.25)]
