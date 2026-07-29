from __future__ import annotations

import sys
from pathlib import Path

import pytest

SERVER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER_ROOT / "src"))

from hotel_booking_mock.services.availability_service import (  # noqa: E402
    make_rate_plan_id,
    parse_rate_plan_id,
)


@pytest.mark.parametrize(
    "hotel_id",
    [
        "htl_cd_chunxi_courtyard",
        "hotel_guayaquil_aero",
        "prov_office_fitout_hotel",
    ],
)
def test_generated_rate_plan_id_round_trips_for_seeded_hotel_id_styles(
    hotel_id: str,
) -> None:
    rate_plan_id = make_rate_plan_id(
        hotel_id,
        "superior_king",
        "flex",
        "2026-08-10",
        "2026-08-14",
    )

    parsed = parse_rate_plan_id(rate_plan_id)

    assert parsed == (
        hotel_id,
        "superior-king",
        "flex",
        "2026-08-10",
        "2026-08-14",
    )
