from ._helpers import approval_message, exact_1200_tracker_ready, icu_makeup_calendar_ready, no_premature_cdr_submission, peds_cancelled_state, used_all_tools

STAGE = 23


def _three_approvals(env) -> bool:
    return (
        approval_message(env, "msg_outpatient_approved_20260805", "outpatient.preceptor@example.test", ["outpatient", "300"])
        and approval_message(env, "msg_pediatrics_approved_20260831", "pediatrics.preceptor@example.test", ["pediatrics", "400", "380", "20"])
        and approval_message(env, "msg_icu_approved_20261005", "icu.preceptor@example.test", ["icu", "500", "20", "520"])
    )


def s23_exact_1200_chain_submitted(env) -> bool:
    return _three_approvals(env) and exact_1200_tracker_ready(env) and used_all_tools(
        env, STAGE, [("email", None), ("calendar", None), ("notion", None)]
    )


def s23_all_three_approvals_present(env) -> bool:
    return (
        _three_approvals(env)
        and peds_cancelled_state(env)
        and icu_makeup_calendar_ready(env)
        and no_premature_cdr_submission(env)
        and exact_1200_tracker_ready(env)
    )


CHECKS = [
    ("s23_exact_1200_chain_submitted", s23_exact_1200_chain_submitted, 2.0),
    ("s23_all_three_approvals_present", s23_all_three_approvals_present, 1.75),
]
