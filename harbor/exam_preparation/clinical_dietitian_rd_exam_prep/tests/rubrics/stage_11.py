from ._helpers import email_message_read_and_contains, peds_cancelled_state, tool_used

STAGE = 11

def s11_leave_email_read(env) -> bool:
    return tool_used(env, STAGE, "email", "read_email") and email_message_read_and_contains(
        env,
        "msg_li_leave_20260826",
        "dr.li@example.test",
        ["pediatrics", "two", "10", "actual calendar"],
    )

def s11_calendar_rechecked(env) -> bool:
    return s11_leave_email_read(env) and tool_used(env, STAGE, "calendar", None) and peds_cancelled_state(env)

CHECKS = [
    ("s11_leave_email_read", s11_leave_email_read, 1.0),
    ("s11_calendar_rechecked", s11_calendar_rechecked, 1.25),
]
