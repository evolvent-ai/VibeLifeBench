from __future__ import annotations
from ._helpers import _check

def chk_s00_scope_auth_safety(env) -> bool:
    return _check('chk_s00_scope_auth_safety', env)

def chk_s00_initial_state_files(env) -> bool:
    return _check('chk_s00_initial_state_files', env)

def chk_cb_s00_brief_ack(env) -> bool:
    return _check('chk_cb_s00_brief_ack', env)

CHECKS = [
    ('chk_s00_scope_auth_safety', chk_s00_scope_auth_safety, 1.5),
    ('chk_s00_initial_state_files', chk_s00_initial_state_files, 1.25),
    ('chk_cb_s00_brief_ack', chk_cb_s00_brief_ack, 1.0),
]
