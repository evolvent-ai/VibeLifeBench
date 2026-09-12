from ._helpers import *

def s20_pre_exam_refresh(env) -> bool:
    return h_s20_pre_exam_refresh(env)

def s20_multiservice_pre_exam_refresh(env) -> bool:
    return h_s20_multiservice_pre_exam_refresh(env)

def s20_no_extreme_cramming(env) -> bool:
    return h_s20_no_extreme_cramming(env)

CHECKS = [
    ("s20_pre_exam_refresh", s20_pre_exam_refresh, 1.25),
    ("s20_multiservice_pre_exam_refresh", s20_multiservice_pre_exam_refresh, 1.0),
    ("s20_no_extreme_cramming", s20_no_extreme_cramming, 2.0),
]
