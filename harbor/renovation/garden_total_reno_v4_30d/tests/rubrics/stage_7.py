"""Stage 7 — compare surface-only work against root-cause remediation."""
from .shared import _helpers as R

def s7_servers(env):
    backend = (
        R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qgrd_cp",))
        and R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qgrd_patch_scope",))
    )
    return backend and R.trace_has_success(env, 7, ("notification_hub",), min_count=1) and R.artifact_active(env, "/workspace/gear_plan.md")

def s7_args(env):
    return R.backend_and_artifact(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qgrd_cp",), "/workspace/gear_plan.md", (("surface-channel-only option", "surface diversion channel"), ("base-course grading",)))

def s7_result(env):
    backend = (
        R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=? AND payload_json LIKE ?", ("ntf_qgrd_cp", "%base_slope%"))
        and R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=? AND payload_json LIKE ?", ("ntf_qgrd_patch_scope", "%lamp_joint_recheck%"))
        and R.no_new_order(env, after="2026-06-21T00:00:00+08:00")
    )
    return backend and R.artifact_has(env, "/workspace/gear_plan.md", (("surface diversion channel",), ("localized pavement removal",), ("third party",), ("rain test",), ("drainage-channel connection",), ("nursery stock",), ("light wiring",), ("net cost", "net_cost_minor"), ("duration",)))

CHECKS = [("s7_servers", s7_servers, 0.5), ("s7_args", s7_args, 0.5), ("s7_result", s7_result, 1.0)]
