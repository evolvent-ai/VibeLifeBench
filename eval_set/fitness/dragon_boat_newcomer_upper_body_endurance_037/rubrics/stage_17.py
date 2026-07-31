from __future__ import annotations
from ._helpers import _check

def chk_s17_email_update_calendar_notion(env) -> bool:
    return _check('chk_s17_email_update_calendar_notion', env)

def chk_s17_team_update_read_no_send_light(env) -> bool:
    return _check('chk_s17_team_update_read_no_send_light', env)

def chk_s17_team_update_action_light(env) -> bool:
    return _check('chk_s17_team_update_action_light', env)

def chk_s17_no_team_reply_send(env) -> bool:
    return _check('chk_s17_no_team_reply_send', env)

CHECKS = [
    ('chk_s17_email_update_calendar_notion', chk_s17_email_update_calendar_notion, 1.75),
    ('chk_s17_team_update_read_no_send_light', chk_s17_team_update_read_no_send_light, 1.0),
    ('chk_s17_team_update_action_light', chk_s17_team_update_action_light, 1.0),
    ('chk_s17_no_team_reply_send', chk_s17_no_team_reply_send, 2.0)
]
