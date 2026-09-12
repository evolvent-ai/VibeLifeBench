from . import _helpers as h

def s17_review_deadline_updated_calendar(env):
    return h.s17_review_deadline_updated_calendar(env)

def s17_source_evidence_updated(env):
    return h.s17_source_evidence_updated(env)

CHECKS = [
    ("s17_review_deadline_updated_calendar", s17_review_deadline_updated_calendar, 1.75),
    ("s17_source_evidence_updated", s17_source_evidence_updated, 1.5),
]
