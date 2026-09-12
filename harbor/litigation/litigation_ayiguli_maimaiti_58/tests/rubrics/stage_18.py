from __future__ import annotations
from ._helpers import *

def s18_lawyer_questions_packet(env) -> bool:
    return (
        packet_ready(env)
        and not_submitted(env, 'final_pretrial_packet.json')
        and artifact_has_terms(
            env, 'final_pretrial_packet.json',
            [['counsel', 'questions'], ['gap', 'open'], ['redacted', 'privacy'], ['handoff', 'internal']],
        )
    )

CHECKS = [('s18_lawyer_questions_packet', s18_lawyer_questions_packet, 1.25)]
