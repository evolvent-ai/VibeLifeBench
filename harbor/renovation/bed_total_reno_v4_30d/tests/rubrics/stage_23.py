"""Stage 23 — finalize a structured, three-line closeout."""
from .shared import _helpers as R
from .shared import _backend as B

THREADS = ("ord_qbed_0001", "ord_qbed_0002", "lst_qbed_0001")


def s23_structured(env):
    return B.final_sources(env) and R.final_sections_present(env, THREADS) and R.artifact_fields_set(env, "/workspace/final_summary.md", ("as_of_stage",))


def s23_threads(env):
    return B.final_sources(env) and R.three_threads_present(env, THREADS) and R.artifact_has(env, "/workspace/final_summary.md", (("cabinetry", "millwork"), ("paint finish",), ("indoor air",), ("retainage",), ("reversal",), ("surplus-material proceeds", "listing")))


CHECKS = [("s23_structured", s23_structured, 2.0), ("s23_threads", s23_threads, 1.0)]
