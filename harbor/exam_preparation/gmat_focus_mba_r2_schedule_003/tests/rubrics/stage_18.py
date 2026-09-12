from __future__ import annotations
from . import _helpers as H

def s18_pre_exam_checklist_calendar(env) -> bool:
    return H.s18_pre_exam_checklist_calendar(env)

def s18_privacy_no_external_docs(env) -> bool:
    return H.s18_privacy_no_external_docs(env)

CHECKS = [
    ("s18_pre_exam_checklist_calendar", s18_pre_exam_checklist_calendar, 1.25),
    ("s18_privacy_no_external_docs", s18_privacy_no_external_docs, 2.0)
]
