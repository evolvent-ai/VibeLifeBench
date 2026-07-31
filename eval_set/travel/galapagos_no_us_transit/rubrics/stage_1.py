from ._stage_checks import run_stage


def s1_registration_transfer_gate(env):
    return run_stage(env, 1)


CHECKS = [("s1_registration_transfer_gate", s1_registration_transfer_gate, 2.0)]
