"""Stage 3: claims selection matrix."""
from __future__ import annotations
from ._helpers import _stage_corpus
from .cross_stage import d_refund_plus_penalty, d_ten_vs_three_higher, d_medical_loss_separate, d_no_mental_damages, d_platform_liability

def s3_reads_claims_draft(env) -> bool:
    text = _stage_corpus(env, 3)
    return any(k in text for k in ("refund plus tenfold compensation", "refund", "medical", "mental", "platform", "negative reviews"))
CHECKS = [("d_refund_plus_penalty", d_refund_plus_penalty, 1), ("d_ten_vs_three_higher", d_ten_vs_three_higher, 1), ("d_medical_loss_separate", d_medical_loss_separate, 1), ("d_no_mental_damages", d_no_mental_damages, 2), ("d_platform_liability", d_platform_liability, 2)]

