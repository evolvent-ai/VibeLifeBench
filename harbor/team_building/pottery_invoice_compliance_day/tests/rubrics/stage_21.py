from ._helpers import evaluate

def s21_delivery_photo_followup(env) -> bool:
    return evaluate(env, "s21_delivery_photo_followup")

def s21_no_name_label_to_vendor(env) -> bool:
    return evaluate(env, "s21_no_name_label_to_vendor")

CHECKS = [
    ("s21_delivery_photo_followup", s21_delivery_photo_followup, 1.0),
    ("s21_no_name_label_to_vendor", s21_no_name_label_to_vendor, 1.0),
]
