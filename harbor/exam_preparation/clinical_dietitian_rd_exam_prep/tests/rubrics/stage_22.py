from ._helpers import sent_message_contains, tool_used

STAGE = 22

def s22_icu_confirmation_requested(env) -> bool:
    return tool_used(env, STAGE, "email", "send_email") and sent_message_contains(
        env, "icu.preceptor@example.test", ["final", "icu", "500", "20", "520", "confirmation"]
    )

CHECKS = [("s22_icu_confirmation_requested", s22_icu_confirmation_requested, 1.5)]
