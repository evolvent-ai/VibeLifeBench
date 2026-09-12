"""Stage 1: country-specific passport and visa requirements."""
from __future__ import annotations

from ._helpers import _call, _flatten_text, _tool_calls, _workspace_file_text


def _exact_requirement_calls(env) -> set[str]:
    destinations: set[str] = set()
    for call in _tool_calls(env, 1):
        name = str(call.get("name") or "").lower().replace("-", "_")
        args = call.get("arguments") or {}
        if (
            name.endswith("check_entry_requirements")
            and args.get("nationality") == "CN"
            and args.get("purpose") == "tourism"
            and args.get("destination") in {"JP", "KR"}
        ):
            destinations.add(str(args["destination"]))
    return destinations


def s1_country_specific_requirements_rechecked(env) -> bool:
    """Exact CN→JP and CN→KR tourism calls match distinct backend rules."""
    if _exact_requirement_calls(env) != {"JP", "KR"}:
        return False
    jp = _call(
        env,
        "visa_and_advisory",
        "check_entry_requirements",
        nationality="CN",
        destination="JP",
        purpose="tourism",
    )
    kr = _call(
        env,
        "visa_and_advisory",
        "check_entry_requirements",
        nationality="CN",
        destination="KR",
        purpose="tourism",
    )
    if not isinstance(jp, dict) or not isinstance(kr, dict):
        raise ValueError("entry requirement tool returned an invalid payload")
    jp_text = _flatten_text(jp).casefold()
    kr_text = _flatten_text(kr).casefold()
    return (
        jp.get("destination") == "JP"
        and jp.get("passport_validity_months") in {0, None}
        and "valid" in jp_text
        and "stay" in jp_text
        and any(term in jp_text for term in ("no universal six-month", "not a universal six-month"))
        and kr.get("destination") == "KR"
        and kr.get("passport_validity_months") == 6
        and "visa" in kr_text
        and "appl" in kr_text
        and any(term in kr_text for term in ("six months", "6 months"))
    )


def s1_wang_hao_exact_passport_risk_persisted(env) -> bool:
    """The risk record preserves exact dates, math, country distinction, owner, and block."""
    risk = _workspace_file_text(env, "/workspace/risk_register.md").casefold()
    return (
        "usr_wang_hao" in risk
        and "wang hao" in risk
        and "2026-11-25" in risk
        and "2026-05-26" in risk
        and "5 months 30 days" in risk
        and "japan" in risk
        and "korea" in risk
        and "valid through intended stay" in risk
        and "no universal six-month" in risk
        and "visa application" in risk
        and "blocked" in risk
        and "renew" in risk
        and "owner" in risk
    )


CHECKS = [
    ("s1_country_specific_requirements_rechecked", s1_country_specific_requirements_rechecked, 1.5),
    ("s1_wang_hao_exact_passport_risk_persisted", s1_wang_hao_exact_passport_risk_persisted, 1.5),
]
