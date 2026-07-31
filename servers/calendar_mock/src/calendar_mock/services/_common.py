"""Shared row-formatting helpers for calendar services."""
import sqlite3
from typing import List, Optional

from ..utils.exceptions import CalendarNotFoundError, EventNotFoundError


def fetch_calendar(conn: sqlite3.Connection, calendar_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM calendars WHERE calendar_id = ?", (calendar_id,)
    ).fetchone()
    if not row:
        raise CalendarNotFoundError(f"calendar not found: {calendar_id}")
    return row


def fetch_event_row(
    conn: sqlite3.Connection,
    event_id: str,
    calendar_id: Optional[str] = None,
) -> sqlite3.Row:
    if calendar_id:
        row = conn.execute(
            "SELECT * FROM events WHERE event_id = ? AND calendar_id = ?",
            (event_id, calendar_id),
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT * FROM events WHERE event_id = ?", (event_id,)
        ).fetchone()
    if not row:
        raise EventNotFoundError(f"event not found: {event_id}")
    return row


def load_attendees(conn: sqlite3.Connection, event_id: str) -> List[dict]:
    rows = conn.execute(
        "SELECT email, name, response_status FROM attendees "
        "WHERE event_id = ? ORDER BY id ASC",
        (event_id,),
    ).fetchall()
    return [
        {
            "email": r["email"],
            "name": r["name"],
            "response_status": r["response_status"],
        }
        for r in rows
    ]


def load_reminders(conn: sqlite3.Connection, event_id: str) -> List[dict]:
    rows = conn.execute(
        "SELECT method, minutes_before FROM reminders "
        "WHERE event_id = ? ORDER BY minutes_before DESC, id ASC",
        (event_id,),
    ).fetchall()
    return [
        {"method": r["method"], "minutes_before": int(r["minutes_before"])}
        for r in rows
    ]


def format_event(conn: sqlite3.Connection, row: sqlite3.Row) -> dict:
    """Format a DB event row + its attendees/reminders into the JSON shape."""
    event_id = row["event_id"]
    return {
        "event_id": event_id,
        "calendar_id": row["calendar_id"],
        "summary": row["summary"],
        "description": row["description"],
        "location": row["location"],
        "start": {"dateTime": row["start_dt"]},
        "end": {"dateTime": row["end_dt"]},
        "all_day": bool(int(row["all_day"])),
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "recurrence_rule": row["recurrence_rule"],
        "parent_event_id": row["parent_event_id"],
        "attendees": load_attendees(conn, event_id),
        "reminders": load_reminders(conn, event_id),
    }


def format_calendar(row: sqlite3.Row) -> dict:
    return {
        "calendar_id": row["calendar_id"],
        "user_id": row["user_id"],
        "name": row["name"],
        "color": row["color"],
        "timezone": row["timezone"],
        "is_primary": bool(int(row["is_primary"])),
        "created_at": row["created_at"],
    }
