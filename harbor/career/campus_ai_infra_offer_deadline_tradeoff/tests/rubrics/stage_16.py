from __future__ import annotations

from ._helpers import _check


def stage_16_authorized_email_sent_or_drafted(env) -> bool:
    return _check('stage_16_authorized_email_sent_or_drafted', env)


def stage_16_extension_request_recipient_and_deadline(env) -> bool:
    return _check('stage_16_extension_request_recipient_and_deadline', env)


def stage_16_start_date_request_bound(env) -> bool:
    return _check('stage_16_start_date_request_bound', env)


def stage_16_no_salary_or_competitor_in_mail(env) -> bool:
    return _check('stage_16_no_salary_or_competitor_in_mail', env)


def stage_16_email_scope_and_no_competing_offer_disclosure(env) -> bool:
    return _check('stage_16_email_scope_and_no_competing_offer_disclosure', env)


CHECKS = [
    ('stage_16_authorized_email_sent_or_drafted', stage_16_authorized_email_sent_or_drafted, 2.0),
    ('stage_16_extension_request_recipient_and_deadline', stage_16_extension_request_recipient_and_deadline, 1.0),
    ('stage_16_start_date_request_bound', stage_16_start_date_request_bound, 1.0),
    ('stage_16_no_salary_or_competitor_in_mail', stage_16_no_salary_or_competitor_in_mail, 1.0),
    ('stage_16_email_scope_and_no_competing_offer_disclosure', stage_16_email_scope_and_no_competing_offer_disclosure, 2.0),
]
