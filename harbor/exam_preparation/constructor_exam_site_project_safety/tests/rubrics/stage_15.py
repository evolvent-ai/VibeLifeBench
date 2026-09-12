from ._helpers import (
    s15_exam_site_official_map_crosscheck as _s15_exam_site_official_map_crosscheck,
    structured_check_id,
)

def s15_exam_site_official_notice(env) -> bool:
    return structured_check_id(env, 's15_exam_site_official_notice')

def s15_exam_site_map_unique(env) -> bool:
    return structured_check_id(env, 's15_exam_site_map_unique')

def s15_exam_site_official_map_crosscheck(env) -> bool:
    return _s15_exam_site_official_map_crosscheck(env)

CHECKS = [
    ('s15_exam_site_official_notice', s15_exam_site_official_notice, 1.0),
    ('s15_exam_site_map_unique', s15_exam_site_map_unique, 1.0),
    ('s15_exam_site_official_map_crosscheck', s15_exam_site_official_map_crosscheck, 1.0),
]
