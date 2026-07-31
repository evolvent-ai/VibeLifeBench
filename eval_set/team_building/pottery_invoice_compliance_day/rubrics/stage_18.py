from ._helpers import evaluate

def s18_preflight_checklist(env) -> bool:
    return evaluate(env, "s18_preflight_checklist")

def s18_food_label_and_contact_sync(env) -> bool:
    return evaluate(env, "s18_food_label_and_contact_sync")

CHECKS = [
    ("s18_preflight_checklist", s18_preflight_checklist, 1.0),
    ("s18_food_label_and_contact_sync", s18_food_label_and_contact_sync, 1.0),
]
