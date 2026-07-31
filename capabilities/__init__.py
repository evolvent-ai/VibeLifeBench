"""vibe-agent-benchmark Terrarium capabilities.

One ``BaseCapability`` subclass per mock server. The base class
``AgentMockServerCapability`` factors out everything common to the 20 mock
servers — concrete capabilities only declare 4 class-level constants.

PROJECT_ROOT discovery:
At runtime we need to resolve ``<root>/envs/<server>/<env_name>/`` and
``<root>/servers/<name>/``. The default walks parents until both are
siblings; can be overridden with ``$VIBE_AGENT_BENCHMARK_ROOT``.

Re-exports for convenience:
    from capabilities import agent_caps_config, BankingMockCapability
"""
from __future__ import annotations

import os
from pathlib import Path


def _find_project_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "envs").is_dir() and (parent / "servers").is_dir():
            return parent
    raise RuntimeError(
        "Could not locate vibe-agent-benchmark project root from "
        f"{here}. Set $VIBE_AGENT_BENCHMARK_ROOT to override."
    )


PROJECT_ROOT: Path = Path(
    os.environ.get("VIBE_AGENT_BENCHMARK_ROOT") or _find_project_root()
)

from capabilities.base import AgentMockServerCapability  # noqa: E402
from capabilities.banking_mock import BankingMockCapability  # noqa: E402
from capabilities.brokerage_mock import BrokerageMockCapability  # noqa: E402
from capabilities.credit_card_mock import CreditCardMockCapability  # noqa: E402
from capabilities.delivery_logistics_mock import DeliveryLogisticsMockCapability  # noqa: E402
from capabilities.ecommerce_mock import EcommerceMockCapability  # noqa: E402
from capabilities.weather_mock import WeatherMockCapability  # noqa: E402
from capabilities.maps_mock import MapsMockCapability  # noqa: E402
from capabilities.calendar_mock import CalendarMockCapability  # noqa: E402
from capabilities.visa_and_advisory_mock import VisaAndAdvisoryMockCapability  # noqa: E402
from capabilities.flight_booking_mock import FlightBookingMockCapability  # noqa: E402
from capabilities.hotel_booking_mock import HotelBookingMockCapability  # noqa: E402
from capabilities.rail_booking_mock import RailBookingMockCapability  # noqa: E402
from capabilities.car_rental_mock import CarRentalMockCapability  # noqa: E402
from capabilities.notion_mock import NotionMockCapability  # noqa: E402
from capabilities.email_mock import EmailMockCapability  # noqa: E402
from capabilities.content_platform_mock import ContentPlatformMockCapability  # noqa: E402
from capabilities.listing_platform_mock import ListingPlatformMockCapability  # noqa: E402
from capabilities.review_platform_mock import ReviewPlatformMockCapability  # noqa: E402
from capabilities.job_board_mock import JobBoardMockCapability  # noqa: E402
from capabilities.legal_search_mock import LegalSearchMockCapability  # noqa: E402
from capabilities.health_tracker_mock import HealthTrackerMockCapability  # noqa: E402
from capabilities.notification_hub_mock import NotificationHubMockCapability  # noqa: E402
from capabilities.helpers import agent_caps_config  # noqa: E402

__all__ = [
    "PROJECT_ROOT",
    "AgentMockServerCapability",
    "BankingMockCapability",
    "BrokerageMockCapability",
    "CreditCardMockCapability",
    "DeliveryLogisticsMockCapability",
    "EcommerceMockCapability",
    "WeatherMockCapability",
    "MapsMockCapability",
    "CalendarMockCapability",
    "VisaAndAdvisoryMockCapability",
    "FlightBookingMockCapability",
    "HotelBookingMockCapability",
    "RailBookingMockCapability",
    "CarRentalMockCapability",
    "NotionMockCapability",
    "EmailMockCapability",
    "ContentPlatformMockCapability",
    "ListingPlatformMockCapability",
    "ReviewPlatformMockCapability",
    "JobBoardMockCapability",
    "LegalSearchMockCapability",
    "HealthTrackerMockCapability",
    "NotificationHubMockCapability",
    "agent_caps_config",
]
