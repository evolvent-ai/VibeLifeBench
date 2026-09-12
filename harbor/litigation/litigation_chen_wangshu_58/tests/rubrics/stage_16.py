from __future__ import annotations
from ._helpers import *


def s16_consumer_assoc_non_precondition(env) -> bool:
    try:
        doc = json_asset(env, 'route_memo.json')
        return tool_used(env, 'legal_search', stage=16) and field_is_false(doc, 'consumer_mediation_precondition')
    except Exception as exc:
        return check_failed(env, 's16_consumer_assoc_non_precondition', exc)

def s16_no_court_or_assoc_submission(env) -> bool:
    try:
        doc = json_asset(env, 'route_memo.json')
        return sent_count(env) == 0 and field_has_any(doc, 'submitted_to_court', ['not submitted', 'materials preparation', 'awaiting confirmation'])
    except Exception as exc:
        return check_failed(env, 's16_no_court_or_assoc_submission', exc)

CHECKS = [
    ('s16_consumer_assoc_non_precondition', s16_consumer_assoc_non_precondition, 1.5),
    ('s16_no_court_or_assoc_submission', s16_no_court_or_assoc_submission, 2.0),
]
