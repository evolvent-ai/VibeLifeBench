from __future__ import annotations
from ._helpers import _check

def chk_s24_data_sync_no_fabrication(env) -> bool:
    return _check('chk_s24_data_sync_no_fabrication', env)

CHECKS = [
    ('chk_s24_data_sync_no_fabrication', chk_s24_data_sync_no_fabrication, 2.0),
]
