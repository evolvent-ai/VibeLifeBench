from __future__ import annotations
from ._helpers import check_s3_legal_search_temp_id, check_s3_no_sensitive_email

def s3_legal_search_temp_id(env) -> bool:
    return check_s3_legal_search_temp_id(env)

def s3_no_sensitive_email(env) -> bool:
    return check_s3_no_sensitive_email(env)

CHECKS = [
    ("s3_legal_search_temp_id", s3_legal_search_temp_id, 1.5),
    ("s3_no_sensitive_email", s3_no_sensitive_email, 1.5),
]
