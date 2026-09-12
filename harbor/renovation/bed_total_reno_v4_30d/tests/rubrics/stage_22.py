"""Stage 22 — cross-check weather, order, refund, card, mail, calendar and listing evidence."""
from .shared import _helpers as R
from .shared import _backend as B


def s22_consistency(env):
    return B.final_sources(env) and R.artifact_has(env, "/workspace/evidence_log.md", (("weather",), ("ecommerce", "order"), ("credit_card", "credit card"), ("email",), ("calendar",), ("listing_platform", "listing"), ("limits", "cannot replace"))) and R.artifact_has(env, "/workspace/decision_log.md", (("status conflict", "cross-check"), ("acceptance",), ("funds posting",)))


CHECKS = [("s22_consistency", s22_consistency, 2.0)]
