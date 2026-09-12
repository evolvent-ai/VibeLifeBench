from . import _helpers as h

def cx_no_defer_application_submitted(env):
    return h.cx_no_defer_application_submitted(env)

def cx_final_room_consistency_b216(env):
    return h.cx_final_room_consistency_b216(env)

def cx_integrity_privacy_chain(env):
    return h.cx_integrity_privacy_chain(env)

def cx_longitudinal_sources_and_auth(env):
    return h.cx_longitudinal_sources_and_auth(env)

CHECKS = [
    ("cx_no_defer_application_submitted", cx_no_defer_application_submitted, 2.0),
    ("cx_final_room_consistency_b216", cx_final_room_consistency_b216, 2.0),
    ("cx_integrity_privacy_chain", cx_integrity_privacy_chain, 2.0),
    ("cx_longitudinal_sources_and_auth", cx_longitudinal_sources_and_auth, 1.75),
]
