from typing import Optional


class HotelMockError(Exception):
    """Base exception class for the mock hotel server."""

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(HotelMockError):
    code = "BAD_ARG"


class BadDateRangeError(HotelMockError):
    code = "BAD_DATE_RANGE"


class HotelNotFoundError(HotelMockError):
    code = "HOTEL_NOT_FOUND"


class RatePlanNotFoundError(HotelMockError):
    code = "RATE_PLAN_NOT_FOUND"


class SoldOutError(HotelMockError):
    code = "SOLD_OUT"


class OverbookError(HotelMockError):
    code = "OVERBOOKED"


class ReservationNotFoundError(HotelMockError):
    code = "RES_NOT_FOUND"


class AlreadyCancelledError(HotelMockError):
    code = "ALREADY_CANCELLED"


class UncancellableError(HotelMockError):
    code = "UNCANCELLABLE"


class ModifyNoAvailabilityError(HotelMockError):
    code = "MODIFY_NO_AVAILABILITY"


class BadDayIndexError(HotelMockError):
    code = "BAD_DAY_INDEX"


class SimFailedError(HotelMockError):
    code = "SIM_FAILED"
