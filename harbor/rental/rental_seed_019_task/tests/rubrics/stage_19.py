from __future__ import annotations
from ._helpers import *

def s19_wet_mark_evidence_logged(env) -> bool:
    return stage_read_result_groups(env, 19, 'notification_hub', ('get_notification',), [('notif_wet_stage19',), ('damp mark',)]) and tool_stage(env, 19, 'notion', None, ['photography'])

CHECKS = [
    ('s19_wet_mark_evidence_logged', s19_wet_mark_evidence_logged, 1.5),
]
