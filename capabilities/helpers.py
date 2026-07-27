"""DX helpers for task authors.

Use ``agent_caps_config`` to build the ``capabilities_config`` dict for
``@entry`` without having to memorize each capability's import_path::

    @entry(
        capabilities=["banking_mock"],
        capabilities_config=agent_caps_config(banking_mock="li_wei_personal"),
    )
    def my_task(env, agent):
        ...
"""
from __future__ import annotations

from typing import Any

# Map cap_name → import_path. Add new entries as we wire up more servers.
_CAP_REGISTRY: dict[str, str] = {
    "banking_mock":            "capabilities.banking_mock:BankingMockCapability",
    "brokerage_mock":          "capabilities.brokerage_mock:BrokerageMockCapability",
    "credit_card_mock":        "capabilities.credit_card_mock:CreditCardMockCapability",
    "delivery_logistics_mock": "capabilities.delivery_logistics_mock:DeliveryLogisticsMockCapability",
    "ecommerce_mock":          "capabilities.ecommerce_mock:EcommerceMockCapability",
    "weather_mock":            "capabilities.weather_mock:WeatherMockCapability",
    "maps_mock":               "capabilities.maps_mock:MapsMockCapability",
    "calendar_mock":           "capabilities.calendar_mock:CalendarMockCapability",
    "visa_and_advisory_mock":  "capabilities.visa_and_advisory_mock:VisaAndAdvisoryMockCapability",
    "flight_booking_mock":     "capabilities.flight_booking_mock:FlightBookingMockCapability",
    "hotel_booking_mock":      "capabilities.hotel_booking_mock:HotelBookingMockCapability",
    "rail_booking_mock":       "capabilities.rail_booking_mock:RailBookingMockCapability",
    "car_rental_mock":         "capabilities.car_rental_mock:CarRentalMockCapability",
    "notion_mock":             "capabilities.notion_mock:NotionMockCapability",
    "email_mock":              "capabilities.email_mock:EmailMockCapability",
    "content_platform_mock":   "capabilities.content_platform_mock:ContentPlatformMockCapability",
    "listing_platform_mock":   "capabilities.listing_platform_mock:ListingPlatformMockCapability",
    "review_platform_mock":    "capabilities.review_platform_mock:ReviewPlatformMockCapability",
    "job_board_mock":          "capabilities.job_board_mock:JobBoardMockCapability",
    "legal_search_mock":       "capabilities.legal_search_mock:LegalSearchMockCapability",
    "health_tracker_mock":     "capabilities.health_tracker_mock:HealthTrackerMockCapability",
    "notification_hub_mock":   "capabilities.notification_hub_mock:NotificationHubMockCapability",
}


def agent_caps_config(**caps: str | dict) -> dict[str, dict[str, Any]]:
    """Build a ``capabilities_config`` dict for the given capabilities.

    Each kwarg is ``cap_name=<env_name>`` (string) or
    ``cap_name={"env_name": ..., extra_keys: ...}`` (dict).

    Example::

        agent_caps_config(banking_mock="li_wei_personal")
        # → {"banking_mock": {"import_path": "...", "env_name": "li_wei_personal"}}
    """
    # ``task_dir`` is an optional non-capability kwarg some tasks pass so the
    # loader can locate the task's local envs/; it's not a mock capability.
    caps.pop("task_dir", None)
    out: dict[str, dict[str, Any]] = {}
    for cap_name, value in caps.items():
        if cap_name not in _CAP_REGISTRY:
            raise KeyError(
                f"Unknown agent capability {cap_name!r}. "
                f"Known: {sorted(_CAP_REGISTRY)}"
            )
        import_path = _CAP_REGISTRY[cap_name]

        if isinstance(value, str):
            cfg: dict[str, Any] = {"env_name": value}
        elif isinstance(value, dict):
            cfg = dict[str, Any](value)
        else:
            raise TypeError(
                f"{cap_name}: value must be str (env_name) or dict; "
                f"got {type(value).__name__}"
            )

        cfg["import_path"] = import_path
        out[cap_name] = cfg
    return out
