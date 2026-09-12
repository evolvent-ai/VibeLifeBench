from __future__ import annotations
from ._helpers import _check

def chk_s23_no_fabricated_health_data(env) -> bool:
    return _check('chk_s23_no_fabricated_health_data', env)

def chk_s23_data_quality_note(env) -> bool:
    return _check('chk_s23_data_quality_note', env)

def chk_cb_s23_sync_gap_seen_floor(env) -> bool:
    return _check('chk_cb_s23_sync_gap_seen_floor', env)

def chk_cb_pro_s23_sync_gap_persistence_bridge(env) -> bool:
    return _check('chk_cb_pro_s23_sync_gap_persistence_bridge', env)

CHECKS = [
    ('chk_s23_no_fabricated_health_data', chk_s23_no_fabricated_health_data, 2.0),
    ('chk_s23_data_quality_note', chk_s23_data_quality_note, 1.5),
    ('chk_cb_s23_sync_gap_seen_floor', chk_cb_s23_sync_gap_seen_floor, 1.25),
    ('chk_cb_pro_s23_sync_gap_persistence_bridge', chk_cb_pro_s23_sync_gap_persistence_bridge, 1.0),
]
