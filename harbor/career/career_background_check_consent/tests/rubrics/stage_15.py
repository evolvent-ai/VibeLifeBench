"""Stage 15: prepare from the Meituan description."""
from __future__ import annotations
from ._helpers import derived_text, used_tool


def s15_prep_from_jd(env) -> bool:
    if not used_tool(env, "get_job", stage=15, server="job_board", arg_substr="jb-dqs7vegrnhjsx"):
        return False
    corpus = derived_text(env)
    return bool(corpus.strip()) and sum(phrase in corpus for phrase in ("sharding", "configuration", "governance", "tracing", "transactions", "concurrency")) >= 2


CHECKS = [("s15_prep_from_jd", s15_prep_from_jd, 2.5)]
