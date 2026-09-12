from __future__ import annotations
from . import _helpers as H

def s5_score_rule_logged(env) -> bool:
    return H.s5_score_rule_logged(env)

def s5_score_check_reminders(env) -> bool:
    return H.s5_score_check_reminders(env)

CHECKS = [
    ("s5_score_rule_logged", s5_score_rule_logged, 1.25),
    ("s5_score_check_reminders", s5_score_check_reminders, 1.25)
]
