from ._helpers import sent_message_contains, tool_used

STAGE = 2

def s2_outpatient_auth_request_sent(env) -> bool:
    return tool_used(env, STAGE, "email", "send_email") and sent_message_contains(
        env, "outpatient.preceptor@example.test", ["outpatient", "300", "confirmation"]
    )

CHECKS = [("s2_outpatient_auth_request_sent", s2_outpatient_auth_request_sent, 1.5)]
