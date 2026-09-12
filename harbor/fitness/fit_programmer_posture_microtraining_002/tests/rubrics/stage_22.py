from __future__ import annotations
from ._helpers import _check

def chk_s22_no_data_fabrication(env) -> bool:
    return _check('chk_s22_no_data_fabrication', env)

def chk_s22_diff_data_quality_final_carryover(env) -> bool:
    return _check('chk_s22_diff_data_quality_final_carryover', env)

def chk_s22_diff_sync_gap_workspace_edit_lite(env) -> bool:
    return _check('chk_s22_diff_sync_gap_workspace_edit_lite', env)

CHECKS = [
    ('chk_s22_no_data_fabrication', chk_s22_no_data_fabrication, 2),
    ('chk_s22_diff_data_quality_final_carryover', chk_s22_diff_data_quality_final_carryover, 1.5),
    ('chk_s22_diff_sync_gap_workspace_edit_lite', chk_s22_diff_sync_gap_workspace_edit_lite, 1.0),
]
