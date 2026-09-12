from ._helpers import evaluate

def s15_deposit_anomaly_pause(env) -> bool:
    return evaluate(env, "s15_deposit_anomaly_pause")

def s15_statement_line_identified(env) -> bool:
    return evaluate(env, "s15_statement_line_identified")

CHECKS = [
    ("s15_deposit_anomaly_pause", s15_deposit_anomaly_pause, 2.0),
    ("s15_statement_line_identified", s15_statement_line_identified, 1.5),
]
