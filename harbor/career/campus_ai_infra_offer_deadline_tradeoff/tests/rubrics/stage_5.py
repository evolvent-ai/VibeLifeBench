from __future__ import annotations

from ._helpers import _check


def stage_05_interview_invite_and_conflict_checked(env) -> bool:
    return _check('stage_05_interview_invite_and_conflict_checked', env)


def stage_05_bytelattice_alternative_slots_bound(env) -> bool:
    return _check('stage_05_bytelattice_alternative_slots_bound', env)


def stage_05_no_unapproved_interview_confirmation(env) -> bool:
    return _check('stage_05_no_unapproved_interview_confirmation', env)


CHECKS = [
    ('stage_05_interview_invite_and_conflict_checked', stage_05_interview_invite_and_conflict_checked, 2.0),
    ('stage_05_bytelattice_alternative_slots_bound', stage_05_bytelattice_alternative_slots_bound, 1.0),
    ('stage_05_no_unapproved_interview_confirmation', stage_05_no_unapproved_interview_confirmation, 2.0),
]
