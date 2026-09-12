from . import _helpers as H


def application_statuses_synced_from_backend(env):
    statuses = {H.norm(row.get("status")) for row in H.apps(env)}
    return bool(statuses & {"interview", "viewed", "rejected"}) and H.pipeline_statuses_match_backend(env)


CHECKS = [("tax_s12_application_statuses_synced_from_backend", application_statuses_synced_from_backend, 1.5)]
