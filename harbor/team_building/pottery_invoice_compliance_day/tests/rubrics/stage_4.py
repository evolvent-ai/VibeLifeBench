from ._helpers import evaluate

def s4_roster_minimized(env) -> bool:
    return evaluate(env, "s4_roster_minimized")

def s4_food_and_glove_constraints(env) -> bool:
    return evaluate(env, "s4_food_and_glove_constraints")

CHECKS = [
    ("s4_roster_minimized", s4_roster_minimized, 1.0),
    ("s4_food_and_glove_constraints", s4_food_and_glove_constraints, 1.0),
]
