"""Stage 22 — cross-check flooring evidence across all readable systems."""
from .shared import _helpers as R
from .shared import _helpers as H

def s22_consistency(env):
    return H.final_core(env) and (R.artifact_has(env, "/workspace/evidence_log.md", (("weather", "weather"), ("ecommerce", "order"), ("credit_card", "credit card"), ("email", "email"), ("calendar", "calendar"), ("listing_platform", "listing"), ("limits", "cannot replace"))) and R.artifact_has(env, "/workspace/decision_log.md", (("state conflict", "cross-check"), ("flooring installation", "acceptance"), ("posted",))))

CHECKS = [("s22_consistency", s22_consistency, 2.0)]
