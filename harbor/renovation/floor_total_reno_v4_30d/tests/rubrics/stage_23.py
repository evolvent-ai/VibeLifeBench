"""Stage 23 — finalize a structured, three-line flooring closeout."""
from .shared import _helpers as R
from .shared import _helpers as H
THREADS = ("ord_qflr_0001", "ord_qflr_0002", "lst_qflr_0001")

def s23_structured(env):
    return H.final_core(env) and (R.final_sections_present(env, THREADS) and R.artifact_fields_set(env, "/workspace/final_summary.md", ("as_of_stage",)))

def s23_threads(env):
    return H.final_core(env) and (R.three_threads_present(env, THREADS) and R.artifact_has(env, "/workspace/final_summary.md", (("underfloor heating",), ("leveling",), ("moisture content",), ("flatness",), ("expansion joints",), ("retainage",), ("reversal",), ("surplus-material proceeds", "listing"))))

CHECKS = [("s23_structured", s23_structured, 2.0), ("s23_threads", s23_threads, 1.0)]
