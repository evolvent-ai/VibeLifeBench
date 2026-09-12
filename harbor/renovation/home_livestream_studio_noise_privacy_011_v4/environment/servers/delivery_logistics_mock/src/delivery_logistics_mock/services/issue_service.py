"""IssueService — open / list customer-care tickets attached to a shipment."""
import logging
import sqlite3
from typing import Optional

from ..backends.db import current_date as _today, next_counter
from ..utils.dates import add_days, now_iso_z
from ..utils.exceptions import BadArgError
from ..utils.ids import ticket_id as make_ticket_id
from ._common import fetch_shipment_row

logger = logging.getLogger(__name__)

VALID_ISSUE_TYPES = (
    "lost",
    "damaged",
    "wrong_address",
    "missing_item",
    "delivery_failed",
)
VALID_ISSUE_STATUSES = ("open", "in_review", "resolved", "closed")

# Response SLAs in days, indexed by issue_type.
RESPONSE_SLA_DAYS = {
    "lost": 3,
    "damaged": 2,
    "wrong_address": 1,
    "missing_item": 2,
    "delivery_failed": 1,
}


class IssueService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def report_issue(self, tracking_no: str, issue_type: str, description: str) -> dict:
        if issue_type not in VALID_ISSUE_TYPES:
            raise BadArgError(
                f"issue_type must be one of {VALID_ISSUE_TYPES}, got {issue_type!r}"
            )
        if not description or not isinstance(description, str):
            raise BadArgError("description must be a non-empty string")
        row = fetch_shipment_row(self.conn, tracking_no=tracking_no)

        now = now_iso_z()
        current_date = _today()
        sla = RESPONSE_SLA_DAYS[issue_type]
        expected = add_days(current_date, sla)

        seq = next_counter(self.conn, "ticket_seq")
        tkt = make_ticket_id(seq)
        self.conn.execute(
            "INSERT INTO issue_tickets ("
            "ticket_id, shipment_id, issue_type, description, status, "
            "opened_at, expected_response_date"
            ") VALUES (?, ?, ?, ?, 'open', ?, ?)",
            (tkt, row["shipment_id"], issue_type, description, now, expected),
        )
        return {
            "ticket_id": tkt,
            "shipment_id": row["shipment_id"],
            "tracking_no": tracking_no,
            "issue_type": issue_type,
            "status": "open",
            "opened_at": now,
            "expected_response_date": expected,
        }

    def list_issues(
        self,
        user_id: str,
        status_filter: Optional[str] = None,
    ) -> dict:
        if not user_id or not isinstance(user_id, str):
            raise BadArgError("user_id must be a non-empty string")
        if status_filter and status_filter not in VALID_ISSUE_STATUSES:
            raise BadArgError(
                f"status_filter must be one of {VALID_ISSUE_STATUSES}"
            )

        params: list = [user_id]
        sql = (
            "SELECT t.ticket_id, t.shipment_id, s.tracking_no, t.issue_type, "
            "t.description, t.status, t.opened_at, t.expected_response_date, t.resolved_at "
            "FROM issue_tickets t JOIN shipments s ON s.shipment_id = t.shipment_id "
            "WHERE s.user_id = ?"
        )
        if status_filter:
            sql += " AND t.status = ?"
            params.append(status_filter)
        sql += " ORDER BY t.opened_at DESC, t.ticket_id DESC"
        rows = self.conn.execute(sql, params).fetchall()

        items = [
            {
                "ticket_id": r["ticket_id"],
                "shipment_id": r["shipment_id"],
                "tracking_no": r["tracking_no"],
                "issue_type": r["issue_type"],
                "description": r["description"],
                "status": r["status"],
                "opened_at": r["opened_at"],
                "expected_response_date": r["expected_response_date"],
                "resolved_at": r["resolved_at"],
            }
            for r in rows
        ]
        return {"user_id": user_id, "count": len(items), "items": items}
