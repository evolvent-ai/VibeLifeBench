"""Stage 7: maintain the verified state during a quiet gap."""
from __future__ import annotations
from ._helpers import derived_text, norm_num, text_has


def s7_quiet_monitor(env) -> bool:
    raw = derived_text(env)
    compact = norm_num(raw)
    return all(value in compact for value in ("33500", "204500", "301500", "97000")) and text_has(raw, [["authorization"], ["search", "application", "position"]])


CHECKS = [("s7_quiet_monitor", s7_quiet_monitor, 1.5)]
