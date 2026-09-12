from __future__ import annotations
from ._helpers import *

def s23_final_packet_not_submitted(env) -> bool:
    return (
        packet_covers_backend(env)
        and not_submitted(env, 'final_pretrial_packet.json')
        and artifact_has_terms(env, 'final_pretrial_packet.json', [['final', 'review'], ['source'], ['version'], ['unresolved', 'resolved', 'open']])
    )

CHECKS = [('s23_final_packet_not_submitted', s23_final_packet_not_submitted, 2.0)]
