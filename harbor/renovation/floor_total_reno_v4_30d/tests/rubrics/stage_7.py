"""Stage 7 — compare the rush-paving offer against evidence-complete options."""
from .shared import _helpers as R
from .shared import _helpers as H

def s7_servers(env):
    return H.notification(env, "ntf_qflr_cp", ("ord_qflr_0001", "missing_tests")) and (R.trace_has_success(env, 7, ("notification_hub",), min_count=1) and R.artifact_active(env, "/workspace/gear_plan.md"))

def s7_args(env):
    return R.backend_and_artifact(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qflr_cp",), "/workspace/gear_plan.md", (("skip reinspection", "install directlyflooring installation"), ("moisture content",)))

def s7_result(env):
    return H.notification(env, "ntf_qflr_cp", ("ord_qflr_0001", "moisture", "flatness", "pressure")) and (R.artifact_has(env, "/workspace/gear_plan.md", (("continue reinspection", "original contractor"), ("localized rework",), ("independent third party",), ("pressure test",), ("flatness",), ("expansion joints",), ("net cost", "net_cost_minor"), ("schedule",))))

CHECKS = [("s7_servers", s7_servers, 0.5), ("s7_args", s7_args, 0.5), ("s7_result", s7_result, 1.0)]
