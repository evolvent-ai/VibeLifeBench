from . import _helpers as H


def fallback_statuses_are_synced_without_abandonment_claim(env):
    text = H.pipeline(env)
    return bool(
        H.pipeline_matches_applications(env, require_statuses=("viewed", "interview"))
        and H.has_terms(text, ("application_status",), ("viewed", "viewed"), ("interview", "interview"))
        and not H.asserts_any(text, ("Hanyu abandoned", "abandon Hanyu"))
    )


CHECKS = [("med_s12_fallback_statuses_are_synced_without_abandonment_claim", fallback_statuses_are_synced_without_abandonment_claim, 1.5)]
