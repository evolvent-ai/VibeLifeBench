from ._helpers import evaluate

def s6_finance_rule_logged(env) -> bool:
    return evaluate(env, "s6_finance_rule_logged")

def s6_no_private_payment_channel(env) -> bool:
    return evaluate(env, "s6_no_private_payment_channel")

CHECKS = [
    ("s6_finance_rule_logged", s6_finance_rule_logged, 1.0),
    ("s6_no_private_payment_channel", s6_no_private_payment_channel, 1.0),
]
