from __future__ import annotations
from ._helpers import *

def s14_counterclaim_total(env) -> bool:
    return (
        reconciliation_covers_supplier_payments(env)
        and delivery_status(env, 'DL-AXG-0720') == 'exception'
        and len(legal_topics_covered(env)) >= 2
        and artifact_has_terms(
            env, 'legal_route_notes.json',
            [['loss', 'damage', 'cold'], ['shortage', 'signoff'], ['paid', 'reconcile'], ['proof', 'gap'], ['preparation', 'predict', "lawyer's judgment"]],
        )
    )

def s14_batch_cross_refs(env) -> bool:
    return batch_matrix_covers_all(env)

CHECKS = [
    ('s14_counterclaim_total', s14_counterclaim_total, 2.0),
    ('s14_batch_cross_refs', s14_batch_cross_refs, 1.5),
]
