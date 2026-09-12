from __future__ import annotations
from ._helpers import *

def s3_screen_low_pressure_vendor(env) -> bool:
    # Keep voluntary and low-pressure wording as alternatives because the agent
    # may describe the interaction rather than repeat one fixed phrase.
    return used(env, 3, 'review_platform') and state_has(env, 3, [['stress-relief'], ['voluntary', 'low-pressure', 'recovery'], ['capacity'], ['invoice']])

def s3_reject_bad_theme(env) -> bool:
    return used(env, 3, 'review_platform') and state_has(env, 3, [['forced', 'diagnostic'], ['exclude', 'reject', 'avoid'], ['opt out']])

CHECKS = [
    ('s3_screen_low_pressure_vendor', s3_screen_low_pressure_vendor, 1.75),
    ('s3_reject_bad_theme', s3_reject_bad_theme, 1.25),
]
