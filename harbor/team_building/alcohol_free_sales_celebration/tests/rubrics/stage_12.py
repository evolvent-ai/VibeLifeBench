from ._helpers import evaluate

def s12_return_budget_calendar_update(env) -> bool:
    return evaluate(env, "s12_return_budget_calendar_update")

def s12_keeps_event_experience_intact(env) -> bool:
    return evaluate(env, "s12_keeps_event_experience_intact")

CHECKS = [
    ("s12_return_budget_calendar_update", s12_return_budget_calendar_update, 1.75),
    ("s12_keeps_event_experience_intact", s12_keeps_event_experience_intact, 1.25),
]
