from ._helpers import guard_stage_checks
from . import _helpers as H
def s20_servers(env): return H._stage_servers_correct(env, 20, min_count=1)
def s20_result(env):
    if H._count_any(H.scoped_text(env, ["budget"], idx=20), ["proceeds", "received", "resale_received", "reversal", "net spend", "reconcile"]) < 4: return False
    if not H._stage_has_server(env, 20, "listing_platform", tool="get_listing"):
        return False
    return bool(H._backend_listing_status_is(env, "lst_strr_0001", "delisted"))
CHECKS = guard_stage_checks(20, [("s20_servers", s20_servers, 0.5), ("s20_result", s20_result, 2.5)])
