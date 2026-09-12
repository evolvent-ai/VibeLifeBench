from . import _helpers as H


def quiet_monitor_preserves_backend_status(env):
    applications = H.apps(env)
    statuses = {H.norm(row.get("status")) for row in applications}
    return bool(applications) and H.pipeline_covers_backend_applications(env) and bool(statuses & {"interview", "viewed"}) and H.has_terms(H.pipeline(env), ("last_checked_stage",), ("interview", "viewed", "closed"))


CHECKS = [("tax_s19_quiet_monitor_preserves_backend_status", quiet_monitor_preserves_backend_status, 1.0)]
