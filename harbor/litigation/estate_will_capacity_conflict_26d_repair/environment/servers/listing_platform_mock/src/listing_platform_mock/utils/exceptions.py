from typing import Optional


class ListingPlatformMockError(Exception):
    """Base exception for the listing-platform mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(ListingPlatformMockError):
    code = "BAD_ARG"


class BadDateError(ListingPlatformMockError):
    code = "BAD_DATE"


class BadCategoryError(ListingPlatformMockError):
    code = "BAD_CATEGORY"


class BadPriceError(ListingPlatformMockError):
    code = "BAD_PRICE"


class ListingNotFoundError(ListingPlatformMockError):
    code = "LISTING_NOT_FOUND"


class ListingDelistedError(ListingPlatformMockError):
    code = "LISTING_DELISTED"


class AgentNotFoundError(ListingPlatformMockError):
    code = "AGENT_NOT_FOUND"


class ViewingNotFoundError(ListingPlatformMockError):
    code = "VIEWING_NOT_FOUND"


class AlreadySavedError(ListingPlatformMockError):
    code = "ALREADY_SAVED"


class NotSavedError(ListingPlatformMockError):
    code = "NOT_SAVED"


class NotOwnerError(ListingPlatformMockError):
    code = "NOT_OWNER"


class StatsNotFoundError(ListingPlatformMockError):
    code = "STATS_NOT_FOUND"
