from __future__ import annotations
from ._helpers import *

def s16_recall_notice_draft_saved(env) -> bool:
    try:
        return recall_notice_draft_saved(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s16_recall_notice_not_sent(env) -> bool:
    try:
        return recall_notice_not_sent(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s16_recall_notice_draft_saved', s16_recall_notice_draft_saved, 1.5),
    ('s16_recall_notice_not_sent', s16_recall_notice_not_sent, 2.0),
]
