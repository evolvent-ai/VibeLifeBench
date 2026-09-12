from . import _helpers as H

def interview_is_scheduled_without_grant_id_in_title(env):
    return H.one_email_has(env, H.INTERVIEW_MESSAGE_ID, ("afternoon of July 1",), ("morning of July 2",), ("60-minute", "60 minutes")) and H.valid_interview_event(env)

CHECKS = [("opt_s11_interview_is_scheduled_without_grant_id_in_title", interview_is_scheduled_without_grant_id_in_title, 2.0)]
