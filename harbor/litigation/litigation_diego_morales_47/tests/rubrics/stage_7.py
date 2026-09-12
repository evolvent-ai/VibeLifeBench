from ._helpers import *


def s7_platform_time_indexed(env):
    return (
        email_stage_topic_used(env, 7, "order's automatic completion time explanation")
        and email_backend_has_message(env, "order's automatic completion time explanation", sender='records@foodpath.example')
        and any(
            source_matches(row.get('source'), 'email_platform')
            and row.get('timestamp') == '2026-07-18T18:51:09+08:00'
            for row in list_from_doc(env, ROUTE_MATRIX, 'events')
        )
    )


CHECKS = [('s7_platform_time_indexed', s7_platform_time_indexed, 1.75)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
