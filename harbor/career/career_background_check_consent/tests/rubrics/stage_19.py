"""Stage 19: maintain the combined state during a quiet gap."""
from __future__ import annotations
from ._helpers import derived_text, list_applications, severance_deposit_minor, text_has


def s19_maintains_state(env) -> bool:
    raw = derived_text(env)
    return severance_deposit_minor(env) == 20450000 and bool(list_applications(env)) and text_has(raw, [["severance", "shortfall", "arbitration", "negotiation"], ["offer", "interview", "application", "search"], ["unresolved", "pending", "next", "follow-up"]])


CHECKS = [("s19_maintains_state", s19_maintains_state, 1.5)]
