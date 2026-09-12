from __future__ import annotations
from . import _helpers as H

def final_review_page_exists(env) -> bool:
    return H.final_review_page_exists(env)

def final_mutation_recovery_logged(env) -> bool:
    return H.final_mutation_recovery_logged(env)

def final_service_set_limited(env) -> bool:
    return H.final_service_set_limited(env)

def final_light_refresh_three_services(env) -> bool:
    return H.final_light_refresh_three_services(env)

def final_active_subscriptions_closed(env) -> bool:
    return H.final_active_subscriptions_closed(env)

CHECKS = [
    ("final_review_page_exists", final_review_page_exists, 1.5),
    ("final_mutation_recovery_logged", final_mutation_recovery_logged, 1.5),
    ("final_service_set_limited", final_service_set_limited, 1.0),
    ("final_light_refresh_three_services", final_light_refresh_three_services, 1.0),
    ("final_active_subscriptions_closed", final_active_subscriptions_closed, 1.25)
]
