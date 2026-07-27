from typing import Optional


class CalendarMockError(Exception):
    """Base exception for the calendar mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(CalendarMockError):
    code = "BAD_ARG"


class BadDateError(CalendarMockError):
    code = "BAD_DATE"


class BadTimeRangeError(CalendarMockError):
    code = "BAD_TIME_RANGE"


class EventNotFoundError(CalendarMockError):
    code = "EVENT_NOT_FOUND"


class CalendarNotFoundError(CalendarMockError):
    code = "CALENDAR_NOT_FOUND"


class OverlappingEventError(CalendarMockError):
    code = "OVERLAPPING_EVENT"
