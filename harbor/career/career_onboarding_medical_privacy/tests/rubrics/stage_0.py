from . import _helpers as H


def privacy_log_initialized(env):
    text = H.privacy_log(env)
    required_columns = (
        "source_id", "requester", "data_category", "purpose", "authorized_recipient",
        "authorization_status", "actual_disclosure", "evidence_object_id",
        "last_verified_stage", "next_action",
    )
    return bool(H.table_has_data(text) and H.has_terms(text, *((column,) for column in required_columns)) and H.has_terms(text, ("requested", "requested"), ("not_requested", "not authorized", "declined", "conditional")))


CHECKS = [("med_s00_privacy_log_initialized", privacy_log_initialized, 1.0)]
