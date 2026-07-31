"""Error classes for flight booking. Message convention: `<code>: <human>`."""
from __future__ import annotations


class FlightBookingError(ValueError):
    """Raised for domain-level errors. Keep the code as the first token of the message."""

    def __init__(self, code: str, message: str = "") -> None:
        self.code = code
        super().__init__(f"{code}: {message}" if message else code)
