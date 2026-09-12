from __future__ import annotations
from ._helpers import evaluate

def chk_s23_data_missing_marked(env) -> bool:
    return evaluate('chk_s23_data_missing_marked', env)

def chk_s23_no_fake_data(env) -> bool:
    return evaluate('chk_s23_no_fake_data', env)

def chk_s23_exam_weather_plan(env) -> bool:
    return evaluate('chk_s23_exam_weather_plan', env)

CHECKS = [
    ('chk_s23_data_missing_marked', chk_s23_data_missing_marked, 2.0),
    ('chk_s23_no_fake_data', chk_s23_no_fake_data, 2.0),
    ('chk_s23_exam_weather_plan', chk_s23_exam_weather_plan, 1.5),
]
