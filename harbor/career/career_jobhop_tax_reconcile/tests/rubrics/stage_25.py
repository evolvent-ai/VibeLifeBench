from . import _helpers as H


def followups_have_owner_and_date(env):
    return H.followups_are_actionable(H.handoff(env))


CHECKS = [("tax_s25_followups_have_owner_and_date", followups_have_owner_and_date, 1.0)]
