from __future__ import annotations
from ._helpers import *

def s3_renewal_cap_computed(env) -> bool:
    return (
        tool_stage(env, 3, 'notion', None, ['5616'])
        and workspace_file_has_groups(env, 'BUDGET_LEDGER.md', [('5200',), ('5616',), ('lease renewal',)])
    )

def s3_commute_cap_checked(env) -> bool:
    return (
        tool_stage(env, 3, 'maps', None, ['current_home'])
        and workspace_file_has_groups(env, 'DUAL_TRACK_STATUS.md', [('34',), ('49',), ('commute',)])
    )

CHECKS = [
    ('s3_renewal_cap_computed', s3_renewal_cap_computed, 1.5),
    ('s3_commute_cap_checked', s3_commute_cap_checked, 1.5),
]
