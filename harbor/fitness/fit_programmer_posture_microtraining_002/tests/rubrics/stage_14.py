from __future__ import annotations
from ._helpers import _check

def chk_s14_no_course_purchase(env) -> bool:
    return _check('chk_s14_no_course_purchase', env)

def chk_s14_diff_course_email_review_reconcile(env) -> bool:
    return _check('chk_s14_diff_course_email_review_reconcile', env)

def chk_s14_diff_email_read_review_lite(env) -> bool:
    return _check('chk_s14_diff_email_read_review_lite', env)

CHECKS = [
    ('chk_s14_no_course_purchase', chk_s14_no_course_purchase, 2),
    ('chk_s14_diff_course_email_review_reconcile', chk_s14_diff_course_email_review_reconcile, 1.5),
    ('chk_s14_diff_email_read_review_lite', chk_s14_diff_email_read_review_lite, 1.0),
]
