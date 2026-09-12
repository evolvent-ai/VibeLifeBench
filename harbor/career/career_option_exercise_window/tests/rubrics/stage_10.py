from . import _helpers as H

def default_rule_and_personal_deadline_are_not_conflated(env):
    text = H.ledger(env)
    deadline_values = {
        H.norm(row.get("exercise_deadline"))
        for row in H.markdown_table_rows(text)
        if "exercise_deadline" in row
    }
    conflated = any(value in {"90 days", "90-day", "90 day", "90-day rule"} for value in deadline_values)
    return H.pending_window_source_valid(env) and H.has_terms(text, ("default 90-day", "90 days"), ("personal deadline", "pending", "pending administrator"), ("portal maintenance",), ("maintenance compensation", "pending")) and not conflated

CHECKS = [("opt_s10_default_rule_and_personal_deadline_are_not_conflated", default_rule_and_personal_deadline_are_not_conflated, 2.5)]
