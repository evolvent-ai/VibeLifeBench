from __future__ import annotations

from ._helpers import check_by_id

def stage_14_pre_exam_checklist_reply(env) -> bool:
    return check_by_id(env, 'stage_14_pre_exam_checklist_reply')

CHECKS = [
    ('stage_14_pre_exam_checklist_reply', stage_14_pre_exam_checklist_reply, 1.5),
]
