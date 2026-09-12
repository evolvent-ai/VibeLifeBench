from ._helpers import *

def s6_followup_channel_created(env):
    return (delivery_subscription_exists(env) or delivery_issue_exists(env)) and doc_value(env, 'object_index.json', 'followup_channel_created', True)

CHECKS = [('s6_followup_channel_created', s6_followup_channel_created, 1.5)]

def evaluate_stage(env):
    return evaluate(CHECKS, env)
