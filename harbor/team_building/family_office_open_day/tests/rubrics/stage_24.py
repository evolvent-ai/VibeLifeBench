from __future__ import annotations
from ._helpers import *


def s24_final_archive_sop(env) -> bool:
    archive = stage_persisted(env, 24, [["review", "SOP"], ["child", "safety"], ["photography"]])
    feedback = stage_persisted(env, 24, [["vendor", "evaluation"], ["manual", "pending"]])
    return archive and feedback


CHECKS = [
    ("s24_final_archive_sop", s24_final_archive_sop, 1.5),
]
