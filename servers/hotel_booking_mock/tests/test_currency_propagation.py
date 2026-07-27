from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

SERVER_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SERVER_ROOT.parents[1]
sys.path.insert(0, str(SERVER_ROOT / "src"))

from hotel_booking_mock.backends.db import init_schema  # noqa: E402
from hotel_booking_mock.services.availability_service import AvailabilityService  # noqa: E402
from hotel_booking_mock.services.catalog_service import CatalogService  # noqa: E402
from hotel_booking_mock.services.reservation_service import ReservationService  # noqa: E402

SEED = (
    PROJECT_ROOT
    / "train_set/career/career_onboarding_hotel_cancel/envs/hotel_booking/career_onboarding_hotel_cancel/init.sql"
)


def _connection() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    init_schema(conn)
    conn.executescript(SEED.read_text(encoding="utf-8"))
    return conn


def test_search_availability_reservation_and_cancellation_preserve_seed_currency():
    conn = _connection()
    try:
        catalog = CatalogService(conn)
        availability = AvailabilityService(conn)
        reservations = ReservationService(conn)

        hotels = catalog.search_hotels(
            "成都",
            "2026-08-10",
            "2026-08-14",
            1,
            {"refundable_only": True, "max_nightly_price": 680},
        )
        assert hotels and {hotel["currency"] for hotel in hotels} == {"CNY"}

        plans = availability.get_room_availability(
            "htl_cd_chunxi_courtyard", "2026-08-10", "2026-08-14", 1
        )
        flex = next(plan for plan in plans if plan["flavor"] == "flex")
        assert flex["currency"] == "CNY"

        created = reservations.create_reservation(
            flex["rate_plan_id"],
            {"first_name": "Wan", "last_name": "Lin", "email": "linwan@example.com", "phone": "13800000000", "user_id": "usr_lin_wan"},
            "pm_lw_visa",
        )
        assert created["currency"] == "CNY"
        assert reservations.get_reservation(created["reservation_id"])["currency"] == "CNY"

        cancelled = reservations.cancel_reservation(created["reservation_id"])
        assert cancelled["currency"] == "CNY"
    finally:
        conn.close()
