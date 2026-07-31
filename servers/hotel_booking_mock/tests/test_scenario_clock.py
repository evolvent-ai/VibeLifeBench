from __future__ import annotations

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import pytest

SERVER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER_ROOT / "src"))

from hotel_booking_mock.backends.db import init_schema  # noqa: E402
from hotel_booking_mock.services.availability_service import AvailabilityService  # noqa: E402
from hotel_booking_mock.services.catalog_service import CatalogService  # noqa: E402
from hotel_booking_mock.services.guest_service import GuestService  # noqa: E402
from hotel_booking_mock.services.reservation_service import ReservationService  # noqa: E402
from hotel_booking_mock.utils import dates as date_utils  # noqa: E402

SEED = Path(__file__).resolve().parent / "fixtures" / "scenario_clock_seed.sql"


class _HostClockMustNotBeRead(datetime):
    @classmethod
    def now(cls, tz=None):
        raise AssertionError("scenario-backed hotel operations must not read the host clock")


def _connection() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    init_schema(conn)
    conn.executescript(SEED.read_text(encoding="utf-8"))
    return conn


def _set_clock(conn: sqlite3.Connection, value: str) -> None:
    conn.execute(
        "INSERT INTO scenario_clock(clock_id,scenario_date) VALUES('default',?) "
        "ON CONFLICT(clock_id) DO UPDATE SET scenario_date=excluded.scenario_date",
        (value,),
    )


def _book(conn: sqlite3.Connection) -> tuple[ReservationService, dict]:
    availability = AvailabilityService(conn)
    reservations = ReservationService(conn)
    plans = availability.get_room_availability(
        "htl_cd_chunxi_courtyard", "2026-08-10", "2026-08-14", 1
    )
    flex = next(plan for plan in plans if plan["flavor"] == "flex")
    created = reservations.create_reservation(
        flex["rate_plan_id"],
        {"first_name": "Wan", "last_name": "Lin", "email": "linwan@example.com", "phone": "13800000000", "user_id": "usr_lin_wan"},
        "pm_lw_visa",
    )
    return reservations, created


def test_seeded_scenario_clock_controls_catalog_without_reading_host_clock(monkeypatch: pytest.MonkeyPatch):
    conn = _connection()
    monkeypatch.setattr(date_utils, "datetime", _HostClockMustNotBeRead)
    try:
        assert conn.execute(
            "SELECT scenario_date FROM scenario_clock WHERE clock_id='default'"
        ).fetchone()[0] == "2026-07-23"
        catalog = CatalogService(conn)

        _set_clock(conn, "2026-08-07")
        before = catalog.search_hotels("成都", "2026-08-10", "2026-08-14", 1, {"refundable_only": True})
        target_before = next(row for row in before if row["hotel_id"] == "htl_cd_chunxi_courtyard")
        assert target_before["refundable"] is True

        _set_clock(conn, "2026-08-09")
        after = catalog.search_hotels("成都", "2026-08-10", "2026-08-14", 1, {"refundable_only": True})
        target_after = next(row for row in after if row["hotel_id"] == "htl_cd_chunxi_courtyard")
        assert target_after["refundable"] is False
    finally:
        conn.close()


def test_reservation_refund_and_guest_summary_follow_scenario_clock(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(date_utils, "datetime", _HostClockMustNotBeRead)

    before_conn = _connection()
    try:
        _set_clock(before_conn, "2026-07-25")
        reservations, created = _book(before_conn)
        guest = GuestService(before_conn)
        assert created["reservation_id"].startswith("res_20260725_")
        assert guest.get_user_bookings_summary("usr_lin_wan")["upcoming_check_in"] == "2026-08-10"

        _set_clock(before_conn, "2026-08-07")
        cancelled = reservations.cancel_reservation(created["reservation_id"])
        assert cancelled["penalty"] == 0
        assert cancelled["refund_amount"] == created["total_charged"]
    finally:
        before_conn.close()

    after_conn = _connection()
    try:
        _set_clock(after_conn, "2026-07-25")
        reservations, created = _book(after_conn)
        guest = GuestService(after_conn)

        _set_clock(after_conn, "2026-08-09")
        cancelled = reservations.cancel_reservation(created["reservation_id"])
        assert cancelled["penalty"] == 520
        assert cancelled["refund_amount"] == created["total_charged"] - 520

        _set_clock(after_conn, "2026-08-15")
        assert guest.get_user_bookings_summary("usr_lin_wan")["upcoming_check_in"] is None
    finally:
        after_conn.close()
