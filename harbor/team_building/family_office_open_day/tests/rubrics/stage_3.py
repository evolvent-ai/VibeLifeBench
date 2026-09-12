from __future__ import annotations
from ._helpers import *

def s3_select_accessible_venue(env) -> bool:
    searched = used(env, 3, "review_platform", "search") or used(env, 3, "review_platform", "get")
    recorded = stage_persisted(env, 3, [["workshop_spark_lab", "workshop"], ["catering_garden_box", "catering"], ["photo_clear_lens", "photography"], ["credentials", "invoice"]])
    return searched and recorded

def s3_reject_bad_accessibility(env) -> bool:
    searched = used(env, 3, "review_platform", "search") or used(env, 3, "review_platform", "get")
    return searched and stage_persisted(env, 3, [["photo", "authorization"], ["nut", "allergy"], ["account", "deposit"], ["pending", "pause", "alternative"]])

CHECKS = [
    ('s3_select_accessible_venue', s3_select_accessible_venue, 2.0),
    ('s3_reject_bad_accessibility', s3_reject_bad_accessibility, 1.25),
]
