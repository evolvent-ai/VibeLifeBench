"""Stage 1 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s1_servers(env) -> bool:
    """L1: stage 1 must query at least three expected MCP servers."""
    if not H._stage_servers_correct(env, 1, min_count=3):
        return False
    return True


def s1_args(env) -> bool:
    """Stage 1 queries must reference the two orders or the card without unrelated fixture IDs."""
    return H._stage_tool_args_reference(
        env, 1, ['ord_iscac_0001', 'ord_iscac_0002', 'card_iscac_01'], min_count=2
    )


def s1_result(env) -> bool:
    """L3: stage 1 responses and records must contain backend truth tokens."""
    return H._stage_result_correct(env, 1, ['sf2074520001cn', 'ytoscac5520002cn', '2074'], min_count=1)


CHECKS = guard_stage_checks(1, [
    ("s1_servers", s1_servers, 0.5),
    ("s1_args", s1_args, 0.5),
    ("s1_result", s1_result, 1.0),
])
