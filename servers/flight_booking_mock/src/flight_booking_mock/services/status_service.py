"""Flight-status lookup + subscribe service."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from ..backends.sqlite_backend import SQLiteBackend
from ..utils import ids, timewin
from ..utils.exceptions import FlightBookingError


def _wall_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class StatusService:
    def __init__(self, backend: SQLiteBackend) -> None:
        self.backend = backend

    def get_flight_status(self, flight_no: str, date: str) -> dict[str, Any]:
        fs = self.backend.get_flight_status(flight_no, date)
        flight = self.backend.get_flight(flight_no, date)
        if not flight:
            flight = self.backend.get_flight_any_date(flight_no)
        if not flight:
            raise FlightBookingError("flight_not_found",
                                     f"{flight_no} on {date}")

        # Scheduled depart/arrive: pull from flights row for that date.
        sched_depart = flight["depart_dt"] if timewin.dt_date(flight["depart_dt"]) == date else \
            self._synth_scheduled_for(flight, date, is_arrive=False)
        sched_arrive = flight["arrive_dt"] if timewin.dt_date(flight["arrive_dt"])[:10] == date else \
            self._synth_scheduled_for(flight, date, is_arrive=True)

        status = fs["status"] if fs else "SCHEDULED"
        delay_min = fs["delay_min"] if fs else 0
        gate = fs["gate"] if fs else None
        terminal = fs["terminal"] if fs else None
        actual_depart = fs["actual_depart"] if fs else None
        actual_arrive = fs["actual_arrive"] if fs else None
        last_updated = fs["last_updated"] if fs else _wall_now_iso()

        return {
            "flight_no": flight_no,
            "date": date,
            "status": status,
            "scheduled_depart": sched_depart,
            "scheduled_arrive": sched_arrive,
            "actual_depart": actual_depart,
            "actual_arrive": actual_arrive,
            "delay_min": delay_min,
            "gate": gate,
            "terminal": terminal,
            "equipment": flight["equipment"],
            "last_updated": last_updated,
        }

    def subscribe_flight_status(self, *, flight_no: str, date: str,
                                sink: str = "stdout",
                                webhook_url: Optional[str] = None) -> dict[str, Any]:
        if sink not in {"stdout", "email", "webhook"}:
            raise FlightBookingError("invalid_sink", sink)
        now_iso = _wall_now_iso()
        seed = f"{flight_no}|{date}"
        sub_id = ids.sub_id_gen(self.backend.conn, seed)
        while self.backend.query_one(
                "SELECT 1 FROM status_subscriptions WHERE sub_id=?", (sub_id,)):
            sub_id = ids.sub_id_gen(self.backend.conn, seed)
        self.backend.insert_subscription(sub_id, flight_no, date, sink,
                                         webhook_url, now_iso)
        return {
            "sub_id": sub_id, "flight_no": flight_no, "date": date,
            "created_at": now_iso,
        }

    def _synth_scheduled_for(self, flight_row: Any, date: str,
                             is_arrive: bool) -> str:
        # Fallback if the per-date flights row isn't present.
        source = flight_row["arrive_dt"] if is_arrive else flight_row["depart_dt"]
        tz = source[-6:]
        return f"{date}T{source[11:19]}{tz}"
