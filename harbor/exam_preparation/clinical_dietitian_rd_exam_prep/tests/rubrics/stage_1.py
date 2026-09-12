from ._helpers import email_message_read_and_contains, tool_used

STAGE = 1

def s1_outpatient_email_checked(env) -> bool:
    return tool_used(env, STAGE, "email", "read_email") and email_message_read_and_contains(
        env,
        "msg_outpatient_timesheet_20260731",
        "outpatient.preceptor@example.test",
        ["outpatient", "300", "provisional", "not approved", "approved hours"],
    )

CHECKS = [("s1_outpatient_email_checked", s1_outpatient_email_checked, 1.0)]
