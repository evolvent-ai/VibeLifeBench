from . import _helpers as H

def application_status_is_synced_without_equity_inference(env):
    statuses = {H.norm(row.get("status")) for row in H.apps(env)}
    return bool(statuses & {"interview", "viewed"}) and H.applications_statuses_backed_by_pipeline(env) and H.has_terms(H.pipeline(env), ("application_status",), ("interview", "viewed")) and H.has_terms(H.ledger(env), ("decision_status",), ("authorization_pending", "scenario_review", "undecided"))

CHECKS = [("opt_s12_application_status_is_synced_without_equity_inference", application_status_is_synced_without_equity_inference, 1.5)]
