from __future__ import annotations
from ._helpers import *

def s5_catering_diet_labels_before_confirm(env) -> bool:
    # Dietary alternatives are intentionally accepted as separate phrases.
    return used(env, 5, 'review_platform') and state_has(env, 5, [['catering'], ['halal', 'lactose-free', 'lactose', 'dairy'], ['invoice'], ['alcohol']])

CHECKS = [
    ('s5_catering_diet_labels_before_confirm', s5_catering_diet_labels_before_confirm, 2.0),
]
