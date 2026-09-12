from typing import Optional


class ReviewPlatformMockError(Exception):
    """Base exception for the review platform mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(ReviewPlatformMockError):
    code = "BAD_ARG"


class BadDateError(ReviewPlatformMockError):
    code = "BAD_DATE"


class BadRatingError(ReviewPlatformMockError):
    code = "BAD_RATING"


class BadCategoryError(ReviewPlatformMockError):
    code = "BAD_CATEGORY"


class MerchantNotFoundError(ReviewPlatformMockError):
    code = "MERCHANT_NOT_FOUND"


class DealNotFoundError(ReviewPlatformMockError):
    code = "DEAL_NOT_FOUND"


class DealUnavailableError(ReviewPlatformMockError):
    code = "DEAL_UNAVAILABLE"


class ReservationNotFoundError(ReviewPlatformMockError):
    code = "RESERVATION_NOT_FOUND"


class PartySizeError(ReviewPlatformMockError):
    code = "PARTY_SIZE_EXCEEDED"
