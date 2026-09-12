from . import _helpers as h

def s4_defer_draft_saved_pending(env):
    return h.s4_defer_draft_saved_pending(env)

def s4_no_defer_application_submitted(env):
    return h.s4_no_defer_application_submitted(env)

CHECKS = [
    ("s4_defer_draft_saved_pending", s4_defer_draft_saved_pending, 2.0),
    ("s4_no_defer_application_submitted", s4_no_defer_application_submitted, 1.5),
]
