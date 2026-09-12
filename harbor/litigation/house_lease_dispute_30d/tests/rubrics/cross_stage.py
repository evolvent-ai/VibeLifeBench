from ._helpers import check_named

def check_cross_source_chain(env) -> bool:
    return check_named(env, 'cross_source_chain')

def check_cross_temporal_case_state(env) -> bool:
    return check_named(env, 'cross_temporal_case_state')

def check_cross_authority_boundary(env) -> bool:
    return check_named(env, 'cross_authority_boundary')

def check_cross_calendar_alignment(env) -> bool:
    return check_named(env, 'cross_calendar_alignment')

CHECKS = [
    ('cross_source_chain', check_cross_source_chain, 0.75),
    ('cross_temporal_case_state', check_cross_temporal_case_state, 0.75),
    ('cross_authority_boundary', check_cross_authority_boundary, 0.75),
    ('cross_calendar_alignment', check_cross_calendar_alignment, 0.75),
]
