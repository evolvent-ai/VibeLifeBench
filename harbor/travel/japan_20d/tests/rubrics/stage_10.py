"""Stage 10 rubric — typhoon watch (low confidence) (D10).

NOTE: ``s10_typhoon_acknowledged`` was deleted — required transcript /
turn_log inspection.
"""
from __future__ import annotations


from .cross_stage import no_premature_cancel_d10_d11

from loguru import logger


CHECKS = [
    # s10_typhoon_acknowledged — DELETED (turn_log / transcript dependency)
    ("d_no_premature_cancel_d10_d11", no_premature_cancel_d10_d11, 1),
]
