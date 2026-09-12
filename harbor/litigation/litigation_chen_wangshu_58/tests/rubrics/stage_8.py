from __future__ import annotations
from ._helpers import *


def s8_usage_matrix_logged(env) -> bool:
    try:
        doc = json_asset(env, 'performance_records.json')
        source = usage_email(env)
        usage_value = flatten_struct(get_value(doc, 'watched_units', ''))
        return (
            tool_used(env, 'email', stage=8)
            and bool(source)
            and '回放' in flatten_struct(source)
            and field_is_false(doc, 'materials_received')
            and all(term in usage_value for term in ['recorded session', 'livestream replay'])
        )
    except Exception as exc:
        return check_failed(env, 's8_usage_matrix_logged', exc)


CHECKS = [('s8_usage_matrix_logged', s8_usage_matrix_logged, 1.25)]
