from __future__ import annotations
from ._helpers import *


def s10_refund_rejection_persisted(env) -> bool:
    try:
        doc = json_asset(env, 'academy_complaint.json')
        return (
            tool_used(env, 'ecommerce', stage=10)
            and refund_status(env) == 'rejected'
            and field_has_any(doc, 'refund_status', ['rejected', 'rejected'])
        )
    except Exception as exc:
        return check_failed(env, 's10_refund_rejection_persisted', exc)


CHECKS = [('s10_refund_rejection_persisted', s10_refund_rejection_persisted, 1.75)]
