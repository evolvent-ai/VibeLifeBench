from __future__ import annotations
from ._helpers import *

def s19_pretrial_packet_core(env) -> bool:
    return packet_covers_backend(env) and not_submitted(env, 'final_pretrial_packet.json') and privacy_log_core_valid(env)

CHECKS = [('s19_pretrial_packet_core', s19_pretrial_packet_core, 2.0)]
