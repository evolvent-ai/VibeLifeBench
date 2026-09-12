from . import _helpers as h

def s24_final_review_page(env):
    return h.s24_final_review_page(env)

def s24_subscriptions_checked_or_closed(env):
    return h.s24_subscriptions_checked_or_closed(env)

CHECKS = [
    ("s24_final_review_page", s24_final_review_page, 1.5),
    ("s24_subscriptions_checked_or_closed", s24_subscriptions_checked_or_closed, 1.25),
]
