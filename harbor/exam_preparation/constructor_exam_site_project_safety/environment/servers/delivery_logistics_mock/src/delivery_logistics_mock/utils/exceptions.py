"""Stable error-code exceptions for delivery_logistics_mock.

All tool-layer code MUST catch these and translate them to
``{"error": msg, "code": CODE}`` responses (see tools/_common.py). The
``code`` attribute is the stable string the agent will observe — never
rename one without versioning the SPEC.
"""
from typing import Optional


class DeliveryMockError(Exception):
    """Base exception for the mock delivery server."""

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(DeliveryMockError):
    code = "BAD_ARG"


class BadDateError(DeliveryMockError):
    code = "BAD_DATE"


class BadAddressError(DeliveryMockError):
    code = "BAD_ADDRESS"


class BadServiceTypeError(DeliveryMockError):
    code = "BAD_SERVICE_TYPE"


class ShipmentNotFoundError(DeliveryMockError):
    code = "SHIPMENT_NOT_FOUND"


class InvalidStatusForOpError(DeliveryMockError):
    code = "INVALID_STATUS_FOR_OP"


class InTransitLockedError(DeliveryMockError):
    code = "IN_TRANSIT_LOCKED"


class CancelTooLateError(DeliveryMockError):
    code = "CANCEL_TOO_LATE"


class SubscriptionNotFoundError(DeliveryMockError):
    code = "SUBSCRIPTION_NOT_FOUND"
