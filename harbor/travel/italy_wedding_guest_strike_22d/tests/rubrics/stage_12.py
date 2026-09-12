from __future__ import annotations
from ._helpers import *

def s12_restaurant_qa_rechecked(env) -> bool:
    return trace_has(env, 12, S_REVIEW, "get_merchant_qa", [["rest_la_quercia"]]) and allergy_answer_confirmed(env)

def s12_safe_restaurant_reserved(env) -> bool:
    return trace_has(env, 12, S_REVIEW, "list_reservations", [[USER_ID]]) and restaurant_reserved_safe(env) and no_unsafe_restaurant(env)

CHECKS = [
    ("s12_restaurant_qa_rechecked", s12_restaurant_qa_rechecked, 0.1),
    ("s12_safe_restaurant_reserved", s12_safe_restaurant_reserved, 2.0),
]
