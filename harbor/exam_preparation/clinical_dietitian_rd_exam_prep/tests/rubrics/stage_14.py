from ._helpers import icu_base_calendar_ready, icu_makeup_calendar_ready, sent_message_contains, tool_used

STAGE = 14

def s14_icu_makeup_request_sent(env) -> bool:
    return tool_used(env, STAGE, "email", "send_email") and sent_message_contains(
        env, "icu.preceptor@example.test", ["icu", "500", "20", "520", "make-up", "confirmation"]
    )

def s14_calendar_makeup_added(env) -> bool:
    return (
        s14_icu_makeup_request_sent(env)
        and tool_used(env, STAGE, "calendar", "create_event")
        and icu_base_calendar_ready(env)
        and icu_makeup_calendar_ready(env)
    )

CHECKS = [
    ("s14_icu_makeup_request_sent", s14_icu_makeup_request_sent, 1.75),
    ("s14_calendar_makeup_added", s14_calendar_makeup_added, 1.5),
]
