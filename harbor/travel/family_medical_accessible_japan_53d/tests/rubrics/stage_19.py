from __future__ import annotations

import re

from ._helpers import _tool_call_matches, _tool_call_results, _workspace_file_text, text_has


def _amount_near(text: str, labels: tuple[str, ...]) -> float | None:
    number = r"([0-9][0-9,]*(?:\.[0-9]+)?)"
    for label in labels:
        match = re.search(rf"{label}.{{0,36}}?{number}", text, flags=re.I | re.S)
        if match:
            return float(match.group(1).replace(",", ""))
        match = re.search(rf"{number}.{{0,24}}?{label}", text, flags=re.I | re.S)
        if match:
            return float(match.group(1).replace(",", ""))
    return None


def s19_budget_for_wagyu(env) -> bool:
    wagyu_search = _tool_call_matches(env, ["maps__search_places"], lambda a: any(x in str(a.get("query") or "").lower() for x in ("wagyu", "wagyu beef")), stage=19)
    indoor_search = _tool_call_matches(env, ["maps__search_places"], lambda a: any(x in str(a.get("query") or "").lower() for x in ("museum", "indoor", "tea", "rail", "itinerary", "ceremony")), stage=19)
    wagyu = _tool_call_results(env, ["maps__get_place_details"], lambda a: a.get("place_id") == "pl_osaka_wagyu", stage=19)
    indoor = _tool_call_results(env, ["maps__get_place_details"], lambda a: a.get("place_id") in {"pl_kyoto_rail_museum", "pl_kyoto_tea"}, stage=19)
    backend = any(isinstance(x, dict) and x.get("place_id") == "pl_osaka_wagyu" and x.get("category") == "restaurant" and x.get("city") == "Osaka" for x in wagyu) and any(isinstance(x, dict) and x.get("place_id") in {"pl_kyoto_rail_museum", "pl_kyoto_tea"} and x.get("city") == "Kyoto" for x in indoor)
    text = _workspace_file_text(env, "budget_ledger.md") + "\n" + _workspace_file_text(env, "decision_log.md") + "\n" + _workspace_file_text(env, "trip_plan.md")
    remaining = _amount_near(text, (r"remaining(?: budget)?", r"budget left", r"unspent(?: budget)?", r"budget balance"))
    meal = _amount_near(text, (r"wagyu(?: meal)?(?: estimate| allowance| budget)?", r"wagyu beef(?: meal)?(?: estimate| budget| allowance)?"))
    buffer = _amount_near(text, (r"buffer", r"contingency", r"reserve buffer", r"discretionary reserve"))
    amounts = remaining is not None and meal is not None and buffer is not None and remaining >= meal + buffer > 0
    durable = text_has(text, [["pl_osaka_wagyu"], ["pl_kyoto_rail_museum", "pl_kyoto_tea"], ["42000", "42,000", "42k"], ["candidate", "option", "estimate", "estimated"]])
    return bool(wagyu_search and indoor_search and backend and amounts and durable)


CHECKS = [("s19_budget_for_wagyu", s19_budget_for_wagyu, 1.5)]
