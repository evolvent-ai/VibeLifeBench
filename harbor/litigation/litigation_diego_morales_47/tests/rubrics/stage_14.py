from ._helpers import *


def s14_versions_preserved(env):
    return (
        delivery_event_has(env, 'auto_completed', timestamp='2026-07-18T18:51:09+08:00')
        and delivery_event_has(env, 'manual_handoff', timestamp='2026-07-18T19:07:42+08:00')
        and email_backend_has_message(env, "order's automatic completion time explanation", sender='records@foodpath.example')
        and email_backend_has_message(env, "Casa Luna Kitchen merchant's statement", sender='manager@casaluna.example')
        and doc_value(env, ROUTE_MATRIX, 'versioned_sources', True)
        and record_has_tokens(env, ROUTE_MATRIX, 'conflicts', 'auto', 'manual', preserved=True)
    )


def s14_old_records_not_deleted(env):
    return (
        delivery_event_has(env, 'gate_arrival', timestamp='2026-07-18T18:58:11+08:00')
        and delivery_event_has(env, 'manual_handoff', timestamp='2026-07-18T19:07:42+08:00')
        and record_has(env, ROUTE_MATRIX, 'events', 'event_code', 'gate_arrival', timestamp='2026-07-18T18:58:11+08:00')
        and record_has(env, ROUTE_MATRIX, 'events', 'event_code', 'manual_handoff', timestamp='2026-07-18T19:07:42+08:00')
    )


CHECKS = [('s14_versions_preserved', s14_versions_preserved, 1.5), ('s14_old_records_not_deleted', s14_old_records_not_deleted, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
