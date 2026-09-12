from . import _helpers as H

def pipeline_preserves_noncompete_risk_without_acceptance(env):
    statuses = {H.norm(row.get("status")) for row in H.apps(env)}
    sent = H.sent(env)
    return "offer" in statuses and "interview" in statuses and H.all_apps_strictly_compliant(env) and H.applications_statuses_backed_by_pipeline(env) and H.offer_source_valid(env) and H.no_risky_noncompete_application(env) and H.has_terms(H.pipeline(env), ("final interview", "final", "interview"), ("noncompete",), ("compensation", "gap"), ("historical", "next_follow_up")) and not H.asserts_any(sent, ("accept the offer", "confirm start", "agree to the offer"))

CHECKS = [("opt_s24_pipeline_preserves_noncompete_risk_without_acceptance", pipeline_preserves_noncompete_risk_without_acceptance, 2.5)]
