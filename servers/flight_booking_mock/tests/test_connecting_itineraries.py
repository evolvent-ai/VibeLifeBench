from __future__ import annotations

import sys
from pathlib import Path

SERVER_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SERVER_ROOT.parents[1]
sys.path.insert(0, str(SERVER_ROOT / "src"))

from flight_booking_mock.backends.sqlite_backend import SQLiteBackend  # noqa: E402
from flight_booking_mock.services.search_service import SearchService  # noqa: E402

SEED = PROJECT_ROOT / "envs/flight_booking/galapagos_no_us_transit/init.sql"


def _service(tmp_path: Path) -> tuple[SearchService, SQLiteBackend]:
    backend = SQLiteBackend(str(tmp_path / "flight.db"))
    backend.apply_init_sql(str(SEED))
    return SearchService(backend), backend


def test_search_builds_bookable_one_stop_offer_from_seeded_legs(tmp_path: Path) -> None:
    service, backend = _service(tmp_path)
    try:
        result = service.search_flights(
            origin="PVG",
            destination="UIO",
            departure_date="2026-08-14",
            cabin="ECONOMY",
            carriers=["KLM"],
        )

        assert result["returned"] == 1
        outbound = result["offers"][0]["itinerary"]["slices"][0]
        assert outbound["origin"] == "PVG"
        assert outbound["destination"] == "UIO"
        assert outbound["stops"] == 1
        assert [segment["flight_no"] for segment in outbound["segments"]] == [
            "KL896",
            "KL755",
        ]

        non_stop = service.search_flights(
            origin="PVG",
            destination="UIO",
            departure_date="2026-08-14",
            cabin="ECONOMY",
            carriers=["KLM"],
            non_stop=True,
        )
        assert non_stop["returned"] == 0
    finally:
        backend.close()
