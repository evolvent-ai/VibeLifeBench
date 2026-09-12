from ._helpers import evaluate

def s1_goal_to_criteria(env) -> bool:
    return evaluate(env, "s1_goal_to_criteria")

def s1_privacy_summary_only(env) -> bool:
    return evaluate(env, "s1_privacy_summary_only")

CHECKS = [
    ("s1_goal_to_criteria", s1_goal_to_criteria, 1.0),
    ("s1_privacy_summary_only", s1_privacy_summary_only, 1.0),
]
