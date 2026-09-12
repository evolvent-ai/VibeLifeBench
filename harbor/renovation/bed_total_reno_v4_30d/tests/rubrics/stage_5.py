"""Stage 5 — partition evidence into four business domains."""
from .shared import _helpers as R
from .shared import _backend as B

def s5_evidence(env):
    return B.evidence_partition_sources(env) and R.artifact_has(env, "/workspace/evidence_log.md", (("contracting party", "authorization letter"), ("millwork", "edge sealing"), ("paint finish", "indoor air"), ("funds", "retainage"), ("service", "source"), ("observed_at_stage", "date"))) and R.heartbeat_has_stage(env, 5)

CHECKS = [("s5_evidence", s5_evidence, 4.0)]
