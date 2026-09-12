"""Stage 12 rubric — vendor confirmations + precision (D12).

Stage 12 is fully covered by cross-stage checkers.
"""
from __future__ import annotations

from .cross_stage import (
    doctor_letter_reminder_before_s13,
    s12_no_overexplain_confirmations,
)


CHECKS = [
    ("d_doctor_letter_reminder_before_s13", doctor_letter_reminder_before_s13, 2),
    ("d_s12_no_overexplain_confirmations",  s12_no_overexplain_confirmations,  1),
]
