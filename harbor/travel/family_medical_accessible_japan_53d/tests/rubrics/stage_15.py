from __future__ import annotations

from ._helpers import _card_detail, _cards, _tool_call_matches, _workspace_file_text, text_has


def s15_checks_credit_limit(env) -> bool:
    tool_ok = _tool_call_matches(
        env,
        ["credit_card__list_cards", "credit_card__get_card"],
        lambda a: a.get("user_id") == "trav_liwei" or a.get("card_id") == "card_travel_visa",
        stage=15,
    )
    cards = _cards(env)
    travel = _card_detail(env, "card_travel_visa")
    backup = _card_detail(env, "card_backup_mc")
    state_ok = len(cards) >= 2 and travel.get("available_credit_minor") == 2800000 and bool(backup)
    durable = text_has(
        _workspace_file_text(env, "budget_ledger.md") + _workspace_file_text(env, "decision_log.md"),
        [["card_travel_visa"], ["2800000", "28,000"], ["available credit", "available credit"], ["backup", "split", "alternate card", "card", "split", "alternate card"]],
    )
    return bool(tool_ok and state_ok and durable)


CHECKS = [("s15_checks_credit_limit", s15_checks_credit_limit, 2.0)]
