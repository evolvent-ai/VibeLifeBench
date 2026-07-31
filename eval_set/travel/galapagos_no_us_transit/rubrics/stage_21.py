from ._stage_checks import run_stage


def s21_registration_deadline_response(env):
    return run_stage(env, 21)


CHECKS = [("s21_registration_deadline_response", s21_registration_deadline_response, 2.0)]
