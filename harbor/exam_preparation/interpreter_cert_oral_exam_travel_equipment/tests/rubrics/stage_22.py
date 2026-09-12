from __future__ import annotations

from ._helpers import rule_ok

def s22_post_exam_archive(env) -> bool:
    return rule_ok(env, 's22_post_exam_archive')

CHECKS = [
    ('s22_post_exam_archive', s22_post_exam_archive, 1.25),
]
