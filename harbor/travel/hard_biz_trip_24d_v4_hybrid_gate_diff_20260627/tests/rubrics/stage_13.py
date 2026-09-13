"""Stage 13: weakening weather and no-direct conclusion must be observable in backends."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _workspace_file_text, _typhoon_stage13_backend, _cancelled_direct_state


def _text(env) -> str:
    return "\n".join(_workspace_file_text(env,p) for p in ["/workspace/incident_log.md","/workspace/decision_log.md","/workspace/risk_register.md","/workspace/itinerary.md"]).lower()


# The world update (event-022) phrases the facts as "nonstop", "July 21", and
# "connecting"; accept those alongside the original direct/7/21/connection
# wordings so a faithful restatement is not misjudged.
_DIRECT_WORDS = ["direct", "nonstop", "non-stop"]
_JULY21_WORDS = ["7/21", "21st", "july 21", "july21", "2026-07-21"]
_CONNECTION_WORDS = ["transit", "connection", "connecting"]


def s13_updated_on_situation(env) -> bool:
    text=_text(env)
    described=_any(text,["improving","weakened","cat 1","cat1"]) and _any(text,_DIRECT_WORDS) and _any(text,["sold out","cancelled","unavailable"]) and _any(text,_JULY21_WORDS) and _any(text,_CONNECTION_WORDS)
    ok=described and _typhoon_stage13_backend(env) and _cancelled_direct_state(env) and s13_persisted_no_direct_return(env)
    logger.info(f"s13_update_backend: {ok}"); return ok


def s13_persisted_no_direct_return(env) -> bool:
    text=_text(env); described=_any(text,_DIRECT_WORDS) and _any(text,_CONNECTION_WORDS+["hkg","hong kong","7/21","july 21"]) and _any(text,["visa","mct","connection","risk"])
    ok=described and _typhoon_stage13_backend(env) and _cancelled_direct_state(env)
    logger.info(f"s13_persist_backend: {ok}"); return ok


CHECKS=[("s13_updated_on_situation",s13_updated_on_situation,1.5),("s13_persisted_no_direct_return",s13_persisted_no_direct_return,1.0)]
