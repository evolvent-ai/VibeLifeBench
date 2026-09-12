from . import _helpers as h

def s23_score_rule_read(env):
    return h.s23_score_rule_read(env)

def s23_review_draft_pending_not_sent(env):
    return h.s23_review_draft_pending_not_sent(env)

CHECKS = [
    ("s23_score_rule_read", s23_score_rule_read, 1.75),
    ("s23_review_draft_pending_not_sent", s23_review_draft_pending_not_sent, 1.75),
]
