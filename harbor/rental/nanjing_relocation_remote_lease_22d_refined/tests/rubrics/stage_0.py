"""Stage 0 — persist the relocation brief and operating constraints."""
from __future__ import annotations
from ._helpers import file_has


def s0_understands_brief(env) -> bool:
    return file_has(env, 'HEARTBEAT.md', ['budget', 'commute', 'verification', 'remote'], minimum=3)


CHECKS = [('s0_understands_brief', s0_understands_brief, 0.1863799283154122)]
