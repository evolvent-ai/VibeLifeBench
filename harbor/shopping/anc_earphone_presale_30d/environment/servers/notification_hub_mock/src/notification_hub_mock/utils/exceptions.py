from typing import Optional


class NotificationHubMockError(Exception):
    """Base exception for the notification hub mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(NotificationHubMockError):
    code = "BAD_ARG"


class BadDateError(NotificationHubMockError):
    code = "BAD_DATE"


class BadTypeError(NotificationHubMockError):
    code = "BAD_TYPE"


class BadAmountError(NotificationHubMockError):
    code = "BAD_AMOUNT"


class SubscriptionNotFoundError(NotificationHubMockError):
    code = "SUBSCRIPTION_NOT_FOUND"


class NotificationNotFoundError(NotificationHubMockError):
    code = "NOTIFICATION_NOT_FOUND"


class AccountNotFoundError(NotificationHubMockError):
    code = "ACCOUNT_NOT_FOUND"


class AlreadySubscribedError(NotificationHubMockError):
    code = "ALREADY_SUBSCRIBED"
