from ._helpers import evaluate

def s12_firing_delay_calendar_update(env) -> bool:
    return evaluate(env, "s12_firing_delay_calendar_update")

def s12_keeps_event_experience_intact(env) -> bool:
    return evaluate(env, "s12_keeps_event_experience_intact")

CHECKS = [
    ("s12_firing_delay_calendar_update", s12_firing_delay_calendar_update, 1.0),
    ("s12_keeps_event_experience_intact", s12_keeps_event_experience_intact, 1.0),
]
