"""Stage 5 — partition flooring evidence into four domains."""
from .shared import _helpers as R
from .shared import _helpers as H

def s5_evidence(env):
    return H.protocol(env) and H.claim(env, "submitted", 2418000) and (R.artifact_has(env, "/workspace/evidence_log.md", (("contract", "contractor"), ("underfloor heating", "pressure test"), ("leveling", "moisture content"), ("flooring", "expansion joints"), ("funds", "retainage"), ("service", "source"), ("observed_at_stage", "date"))) and R.heartbeat_has_stage(env, 5))

CHECKS = [("s5_evidence", s5_evidence, 4.0)]
