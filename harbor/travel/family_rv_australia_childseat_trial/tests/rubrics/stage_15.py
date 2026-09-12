from __future__ import annotations
from ._helpers import *

def s15_close_visa_risk_after_granted(env) -> bool:
    return _used_visa_application_lookup(env, 15) and _has_visa(env, [['granted', 'approved'], ['vac_lc_2026_09_au']]) and _workspace_file_has(env, FILE_RISK_LOG, [['Australian visa', 'visa'], ['granted', 'approved'], ['resolved', 'closed', 'close'], ['additional documents', 'additional']])

def s15_preserve_arrival_rest(env) -> bool:
    return _check_text(env, 15, [['arrival', 'arrival', 'sydney'], ['rest break', 'hotel', 'rest'], ['no vehicle pickup', 'no long-distance drive', 'no long drive']])
CHECKS = [('s15_close_visa_risk_after_granted', s15_close_visa_risk_after_granted, 1.5), ('s15_preserve_arrival_rest', s15_preserve_arrival_rest, 2.0)]
