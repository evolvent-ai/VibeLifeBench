from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS
def s19_result(env):
    text = H.files_text(env, ["tracker", "decision", "evidence"]) + "\n" + H._agent_response(env, 19)
    return H._stage_has_server(env, 19, "ecommerce", tool="get_order") and H._stage_has_server(env, 19, "notification_hub") and H._thread_block_has_terms(text, THREAD_IDS[1], ["platform intervention", "return approved", "evidence", "refund", "proof"], min_count=3, window=320) and H._backend_refund_status_is(env, "ord_strr_0002", "ref_strr_b", "approved") is True and H._refund_amount(env, "ord_strr_0002", "ref_strr_b") == 53760
CHECKS = guard_stage_checks(19, [("s19_result", s19_result, 2.5)])
