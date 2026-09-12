from ._stage_checks import run_stage


def s17_payment_state_integrity(env):
    return run_stage(env, 17)


CHECKS = [("s17_payment_state_integrity", s17_payment_state_integrity, 2.0)]
