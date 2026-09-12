"""Stage 21: verify the return-prep heartbeat is backed by live checks and durable owners."""
from __future__ import annotations

from .shared._helpers import _call, _tool_call_matches, workspace_file_content


def s21_return_risks_rechecked(env) -> bool:
    ash = _tool_call_matches(
        env,
        "weather",
        "get_alerts",
        lambda a: any(x in str(a.get("geo") or "").lower() for x in ("bali_dps", "bali_kintamani")),
        stage=21,
    )
    flight = _tool_call_matches(
        env,
        "flight_booking",
        "get_flight_status",
        lambda a: str(a.get("flight_no") or "").replace(" ", "").upper() == "GA836"
        and str(a.get("date") or "") == "2026-07-01",
        stage=21,
    )
    alerts = _call(env, "weather", "get_alerts", geo="bali_kintamani")
    status = _call(env, "flight_booking", "get_flight_status", flight_no="GA836", date="2026-07-01")
    live_alert = "alert_volcano_l3" in str(alerts).casefold() and "warning" in str(alerts).casefold()
    live_flight = isinstance(status, dict) and str(status.get("flight_no") or "").replace(" ", "").upper() == "GA836" and str(status.get("status") or "").upper() == "SCHEDULED"
    return bool(ash and flight and live_alert and live_flight)


def s21_return_obligations_persisted(env) -> bool:
    text = (
        workspace_file_content(env, "/workspace/HEARTBEAT.md")
        + "\n"
        + workspace_file_content(env, "/workspace/risk_register.md")
        + "\n"
        + workspace_file_content(env, "/workspace/expense_summary.md")
    ).lower()
    has_receipts = any(x in text for x in ("receipt", "invoice", "receipt", "invoice"))
    has_medication = any(x in text for x in ("methotrexate", "leflunomide", "ra medication"))
    has_owner = any(x in text for x in ("owner", "owner")) and any(x in text for x in ("next check", "next review", "next check"))
    return bool(has_receipts and has_medication and has_owner)


CHECKS = [
    ("s21_return_risks_rechecked", s21_return_risks_rechecked, 2.0),
    ("s21_return_obligations_persisted", s21_return_obligations_persisted, 2.0),
]
