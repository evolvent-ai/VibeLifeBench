"""Stage 2 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s2_servers(env) -> bool:
    """L1: stage 2 must query at least two expected MCP servers."""
    if not H._stage_servers_correct(env, 2, min_count=2):
        return False
    return True


def s2_args(env) -> bool:
    """L2: stage 2 tool arguments must reference expected entities."""
    return H._stage_tool_args_reference(env, 2, ['prod_iscac_main', 'sku_iscac_main', 'ord_iscac_0001', 'oa_iscac_brand'], min_count=2)


def s2_result(env) -> bool:
    """Require persisted model/service identifiers and a matching backend SKU batch."""
    text = H.scoped_text(env, ['tracker', 'decision', 'risk', 'gear'], idx=2)
    semantic = H._count_any(text, ['model', 'installer credentials', 'home-visit service code', 'fee rules', 'licensed', 'floor charges']) >= 3
    identifiers = H._count_any(text, ['cmx-3r1-2074', 'vrf-iscac-2074g', '2025q4']) >= 2
    if not (semantic and identifiers):
        return False
    return H._backend_batch_verified(env, 'prod_iscac_main', '2025Q4') is True


def s2_options(env) -> bool:
    """Compare the three observable remediation paths across cost, time and evidence."""
    text = H.scoped_text(env, ['gear', 'decision', 'tracker'], idx=2)
    return (
        H._count_any(text, ['official rework', 'licensed third-party', 'self-remediation', 'reimbursement']) >= 3
        and H._count_any(text, ['780', '450', '600']) >= 2
        and H._count_any(text, ['fees', 'time', 'timeline', 'acceptance', 'evidence']) >= 3
    )


CHECKS = guard_stage_checks(2, [
    ("s2_servers", s2_servers, 0.5),
    ("s2_args", s2_args, 1.0),
    ("s2_result", s2_result, 2.0),
    ("s2_options", s2_options, 2.0),
])
