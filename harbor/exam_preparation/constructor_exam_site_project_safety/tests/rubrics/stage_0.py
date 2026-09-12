from ._helpers import response_check_id, structured_check_id

def s00_workspace_plan(env) -> bool:
    return structured_check_id(env, 's00_workspace_plan')

def s00_policy_subscription(env) -> bool:
    return structured_check_id(env, 's00_policy_subscription')

CHECKS = [
    ('s00_workspace_plan', s00_workspace_plan, 1.0),
    ('s00_policy_subscription', s00_policy_subscription, 1.0),
]
