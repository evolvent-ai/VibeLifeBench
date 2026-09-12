"""Event CRUD + listing/search service."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import (
    assert_time_range,
    now_iso_z,
    parse_datetime,
    to_storage_offset,
)
from ..utils.exceptions import BadArgError
from ..utils.ids import event_id as make_event_id
from ._common import (
    fetch_calendar,
    fetch_event_row,
    format_event,
)

logger = logging.getLogger(__name__)

VALID_STATUS = ("confirmed", "tentative", "cancelled")
VALID_ATTENDEE_RESPONSE = ("needsAction", "accepted", "declined", "tentative")
VALID_REMINDER_METHOD = ("popup", "email")
VALID_ORDER_BY = ("startTime", "updated")


class EventService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- list / get / search --------------------------------------------
    def list_events(
        self,
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        calendar_id: Optional[str] = None,
        max_results: int = 20,
        order_by: str = "startTime",
        page: int = 1,
    ) -> dict:
        if order_by not in VALID_ORDER_BY:
            raise BadArgError(f"order_by must be one of {VALID_ORDER_BY}")
        if max_results is None or int(max_results) < 1:
            raise BadArgError("max_results must be >= 1")
        max_results = min(int(max_results), 500)
        if page is None or page < 1:
            raise BadArgError("page must be >= 1")
        # Validate, then rewrite each bound into the stored offset so the TEXT
        # comparison below matches on the instant rather than on the spelling.
        if time_min:
            time_min = to_storage_offset(time_min)
        if time_max:
            time_max = to_storage_offset(time_max)
        if calendar_id:
            fetch_calendar(self.conn, calendar_id)

        # `max_results` is a page size, not a data-loss cap: the matching set is
        # materialised as a COUNT first, then sliced, and `has_more` signals
        # whether a later page exists.
        where = ["1=1"]
        args: List = []
        if calendar_id:
            where.append("calendar_id = ?")
            args.append(calendar_id)
        if time_min:
            # An event overlaps the window if its end is after time_min.
            where.append("end_dt > ?")
            args.append(time_min)
        if time_max:
            where.append("start_dt < ?")
            args.append(time_max)

        total = int(self.conn.execute(
            f"SELECT COUNT(*) AS n FROM events WHERE {' AND '.join(where)}", args
        ).fetchone()["n"])

        if order_by == "updated":
            order = "ORDER BY updated_at DESC, event_id DESC"
        else:
            order = "ORDER BY start_dt ASC, event_id ASC"

        offset = (page - 1) * max_results
        rows = self.conn.execute(
            f"SELECT * FROM events WHERE {' AND '.join(where)} {order} LIMIT ? OFFSET ?",
            args + [max_results, offset],
        ).fetchall()
        return {
            "items": [format_event(self.conn, r) for r in rows],
            "total": total,
            "page": int(page),
            "page_size": max_results,
            "has_more": page * max_results < total,
        }

    def get_event(
        self, event_id: str, calendar_id: Optional[str] = None
    ) -> dict:
        row = fetch_event_row(self.conn, event_id, calendar_id)
        return format_event(self.conn, row)

    def search_events(
        self,
        query: str,
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        max_results: int = 50,
        page: int = 1,
    ) -> dict:
        if not query or not isinstance(query, str):
            raise BadArgError("query is required")
        # Validate, then rewrite each bound into the stored offset so the TEXT
        # comparison below matches on the instant rather than on the spelling.
        if time_min:
            time_min = to_storage_offset(time_min)
        if time_max:
            time_max = to_storage_offset(time_max)
        max_results = min(max(int(max_results or 50), 1), 500)
        if page is None or page < 1:
            raise BadArgError("page must be >= 1")
        like = f"%{query.lower()}%"

        where = (
            "(LOWER(COALESCE(e.summary,'')) LIKE ? "
            " OR LOWER(COALESCE(e.description,'')) LIKE ? "
            " OR LOWER(COALESCE(e.location,'')) LIKE ? "
            " OR LOWER(COALESCE(a.email,'')) LIKE ? "
            " OR LOWER(COALESCE(a.name,'')) LIKE ?)"
        )
        args: List = [like, like, like, like, like]
        if time_min:
            where += " AND e.end_dt > ?"
            args.append(time_min)
        if time_max:
            where += " AND e.start_dt < ?"
            args.append(time_max)

        # The search joins attendees, so a matching event can fan out to many
        # rows; COUNT(DISTINCT event_id) is the true size of the result set.
        total = int(self.conn.execute(
            "SELECT COUNT(DISTINCT e.event_id) AS n FROM events e "
            "LEFT JOIN attendees a ON a.event_id = e.event_id "
            f"WHERE {where}", args
        ).fetchone()["n"])

        offset = (page - 1) * max_results
        rows = self.conn.execute(
            "SELECT DISTINCT e.* FROM events e "
            "LEFT JOIN attendees a ON a.event_id = e.event_id "
            f"WHERE {where} ORDER BY e.start_dt ASC, e.event_id ASC LIMIT ? OFFSET ?",
            args + [max_results, offset],
        ).fetchall()
        return {
            "items": [format_event(self.conn, r) for r in rows],
            "total": total,
            "page": int(page),
            "page_size": max_results,
            "has_more": page * max_results < total,
        }

    # ---- create / update / delete ---------------------------------------
    def create_event(
        self,
        summary: str,
        start: str,
        end: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        calendar_id: Optional[str] = None,
        attendees: Optional[List[dict]] = None,
        reminders: Optional[List[dict]] = None,
    ) -> dict:
        if not summary or not isinstance(summary, str):
            raise BadArgError("summary is required")
        assert_time_range(start, end)
        cal_id = self._resolve_calendar(calendar_id)
        attendees = attendees or []
        reminders = reminders or []
        self._validate_attendees(attendees)
        self._validate_reminders(reminders)

        seq = next_counter(self.conn, "event_seq")
        new_id = make_event_id(seq)
        now = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO events
              (event_id, calendar_id, summary, description, location,
               start_dt, end_dt, all_day, status,
               created_at, updated_at, recurrence_rule, parent_event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, 'confirmed', ?, ?, NULL, NULL)
            """,
            (new_id, cal_id, summary, description, location,
             start, end, now, now),
        )
        for att in attendees:
            self.conn.execute(
                """
                INSERT INTO attendees (event_id, email, name, response_status)
                VALUES (?, ?, ?, ?)
                """,
                (new_id, att["email"], att.get("name"),
                 att.get("response_status", "needsAction")),
            )
        for rem in reminders:
            self.conn.execute(
                """
                INSERT INTO reminders (event_id, method, minutes_before)
                VALUES (?, ?, ?)
                """,
                (new_id, rem.get("method", "popup"), int(rem["minutes_before"])),
            )
        row = fetch_event_row(self.conn, new_id)
        return format_event(self.conn, row)

    def update_event(
        self,
        event_id: str,
        summary: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        calendar_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        existing = fetch_event_row(self.conn, event_id)
        new_start = start if start is not None else existing["start_dt"]
        new_end = end if end is not None else existing["end_dt"]
        if start is not None or end is not None:
            assert_time_range(new_start, new_end)
        if status is not None and status not in VALID_STATUS:
            raise BadArgError(f"status must be one of {VALID_STATUS}")
        new_cal = (
            self._resolve_calendar(calendar_id)
            if calendar_id is not None
            else existing["calendar_id"]
        )

        self.conn.execute(
            """
            UPDATE events
            SET summary = COALESCE(?, summary),
                description = CASE WHEN ? = 1 THEN ? ELSE description END,
                location    = CASE WHEN ? = 1 THEN ? ELSE location END,
                start_dt = ?,
                end_dt = ?,
                calendar_id = ?,
                status = COALESCE(?, status),
                updated_at = ?
            WHERE event_id = ?
            """,
            (
                summary,
                1 if description is not None else 0, description,
                1 if location is not None else 0, location,
                new_start, new_end, new_cal, status,
                now_iso_z(), event_id,
            ),
        )
        row = fetch_event_row(self.conn, event_id)
        return format_event(self.conn, row)

    def delete_event(
        self, event_id: str, calendar_id: Optional[str] = None
    ) -> dict:
        fetch_event_row(self.conn, event_id, calendar_id)
        self.conn.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
        return {"event_id": event_id, "deleted": True}

    # ---- internals -------------------------------------------------------
    def _resolve_calendar(self, calendar_id: Optional[str]) -> str:
        if calendar_id:
            fetch_calendar(self.conn, calendar_id)
            return calendar_id
        row = self.conn.execute(
            "SELECT calendar_id FROM calendars WHERE is_primary = 1 "
            "ORDER BY created_at ASC, calendar_id ASC LIMIT 1"
        ).fetchone()
        if row:
            return row["calendar_id"]
        row = self.conn.execute(
            "SELECT calendar_id FROM calendars "
            "ORDER BY created_at ASC, calendar_id ASC LIMIT 1"
        ).fetchone()
        if not row:
            raise BadArgError(
                "no calendars exist; pass calendar_id or seed one first"
            )
        return row["calendar_id"]

    def _validate_attendees(self, attendees: List[dict]) -> None:
        for att in attendees:
            if not isinstance(att, dict) or "email" not in att:
                raise BadArgError(
                    "each attendee must be {email, name?, response_status?}"
                )
            rs = att.get("response_status", "needsAction")
            if rs not in VALID_ATTENDEE_RESPONSE:
                raise BadArgError(
                    f"attendee response_status must be one of {VALID_ATTENDEE_RESPONSE}"
                )

    def _validate_reminders(self, reminders: List[dict]) -> None:
        for rem in reminders:
            if not isinstance(rem, dict) or "minutes_before" not in rem:
                raise BadArgError(
                    "each reminder must be {minutes_before, method?}"
                )
            method = rem.get("method", "popup")
            if method not in VALID_REMINDER_METHOD:
                raise BadArgError(
                    f"reminder method must be one of {VALID_REMINDER_METHOD}"
                )
            try:
                if int(rem["minutes_before"]) < 0:
                    raise ValueError
            except (TypeError, ValueError):
                raise BadArgError("reminder minutes_before must be a non-negative integer")
