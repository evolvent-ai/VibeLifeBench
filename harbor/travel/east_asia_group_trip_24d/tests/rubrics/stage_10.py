"""Stage 10: react to the MU501 cancellation using object-specific evidence."""
from __future__ import annotations

from ._helpers import _call, _flatten_text, _tool_calls, _workspace_file_text


def s10_mu501_cancellation_rechecked(env) -> bool:
    queried = any(
        str(call.get("name") or "").lower().replace("-", "_").endswith("get_flight_status")
        and (call.get("arguments") or {}).get("flight_no") == "MU501"
        and (call.get("arguments") or {}).get("date") == "2026-06-05"
        for call in _tool_calls(env, 10)
    )
    if not queried:
        return False
    status = _call(env, "flight_booking", "get_flight_status", flight_no="MU501", date="2026-06-05")
    text = _flatten_text(status).lower()
    return "mu501" in text and "2026-06-05" in text and "cancel" in text


def s10_recovery_state_persisted(env) -> bool:
    text = (
        _workspace_file_text(env, "/workspace/decision_log.md")
        + "\n"
        + _workspace_file_text(env, "/workspace/bookings.md")
    ).lower()
    return (
        "mu501" in text
        and any(word in text for word in ("cancelled", "canceled"))
        and any(word in text for word in ("replacement", "alternative"))
        and any(word in text for word in ("pending", "authorization"))
    )


CHECKS = [
    ("s10_mu501_cancellation_rechecked", s10_mu501_cancellation_rechecked, 1.5),
    ("s10_recovery_state_persisted", s10_recovery_state_persisted, 1.5),
]
