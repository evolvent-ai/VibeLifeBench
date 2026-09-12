"""Stage 11: user asks handle passport/EVUS."""
from __future__ import annotations
from loguru import logger
from ._helpers import _ws, _tool_called_in_stage, _evus_renewal_submitted

_EVUS_WRITE_TOOLS = ["submit_visa_application", "upload_document", "start_visa_application"]


def s11_passport_remedy(env) -> bool:
    """Durable files record exact dates, official confirmation and a contingency."""
    plan = _ws(env, "/workspace/trip_plan.md").lower()
    dl = _ws(env, "/workspace/decision_log.md").lower()
    text = plan + "\n" + dl
    expiry = "2026-05-30" in text or "2026/05/30" in text
    trip_end = "2026-03-30" in text or "2026/03/30" in text or "march 30" in text
    margin = any(w in text for w in ["short margin", "limited margin", "short margin", "limited margin", "near expiry"])
    confirmation = (
        any(w in text for w in ["carrier", "operating airline", "operating airline", "airline"])
        and any(w in text for w in ["cbp", "official", "CBP", "official"])
        and any(w in text for w in ["confirm", "verify", "written confirmation", "verify", "confirm"])
    )
    contingency = any(w in text for w in ["renew passport", "replace passport", "new passport", "hold booking", "refundable", "refundable", "escalate"])
    ok = expiry and trip_end and margin and confirmation and contingency
    logger.info(
        f"s11_passport_remedy: expiry={expiry} trip_end={trip_end} margin={margin} "
        f"confirmation={confirmation} contingency={contingency} -> {ok}"
    )
    return bool(ok)


def s10_submitted_evus_renewal(env) -> bool:
    """The authorized stage submitted the discoverable EVUS draft through the real write API."""
    tool_ok = _tool_called_in_stage(env, 11, _EVUS_WRITE_TOOLS)
    if not tool_ok:
        logger.info("s10_submitted_evus_renewal: tool_ok=False -> False")
        return False
    backend_ok = _evus_renewal_submitted(env)
    ok = tool_ok and backend_ok
    logger.info(f"s10_submitted_evus_renewal: tool_ok={tool_ok} backend_ok={backend_ok} -> {ok}")
    return ok


CHECKS = [
    ("s11_passport_remedy", s11_passport_remedy, 1.75),
    ("s10_submitted_evus_renewal", s10_submitted_evus_renewal, 2.0),
]
