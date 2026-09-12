"""Stage 0 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s0_servers(env) -> bool:
    """L1: stage 0 must query at least three expected MCP servers."""
    if not H._stage_servers_correct(env, 0, min_count=3):
        return False
    return True


def s0_args(env) -> bool:
    """L2: stage 0 tool arguments must reference expected entities."""
    return H._stage_tool_args_reference(env, 0, ['ord_iscac_0001', 'ord_iscac_0002', 'usr_luo_wei', 'card_iscac_01'], min_count=2)


def s0_result(env) -> bool:
    """L3: stage 0 responses and records must contain backend truth tokens."""
    return H._stage_result_correct(env, 0, ['sf2074520001cn', 'ytoscac5520002cn', '2074'], min_count=1)


def s0_files(env) -> bool:
    """Require at least three non-empty workspace tracking files."""
    return H._files_nonempty(env, H.CORE_WORKSPACE_PATHS, min_count=3)


CHECKS = guard_stage_checks(0, [
    ("s0_servers", s0_servers, 0.5),
    ("s0_args", s0_args, 1.0),
    ("s0_result", s0_result, 1.5),
    ("s0_files", s0_files, 0.5),
])
