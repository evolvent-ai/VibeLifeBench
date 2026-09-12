from __future__ import annotations
from ._helpers import *

def s22_confirm_1830_viewing_with_buffer(env) -> bool:
    return run_stage_requirement(env, 's22_confirm_1830_viewing_with_buffer')

def s22_authorization_logged_for_viewing(env) -> bool:
    return run_stage_requirement(env, 's22_authorization_logged_for_viewing')

CHECKS = [
    ('s22_confirm_1830_viewing_with_buffer', s22_confirm_1830_viewing_with_buffer, 1.75),
    ('s22_authorization_logged_for_viewing', s22_authorization_logged_for_viewing, 1.5),
]
