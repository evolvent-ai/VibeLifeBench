from typing import Optional


class ContentPlatformMockError(Exception):
    """Base exception for the content platform mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(ContentPlatformMockError):
    code = "BAD_ARG"


class NoteNotFoundError(ContentPlatformMockError):
    code = "NOTE_NOT_FOUND"


class UserNotFoundError(ContentPlatformMockError):
    code = "USER_NOT_FOUND"


class TopicNotFoundError(ContentPlatformMockError):
    code = "TOPIC_NOT_FOUND"


class AlreadyExistsError(ContentPlatformMockError):
    code = "ALREADY_EXISTS"


class NotFollowingError(ContentPlatformMockError):
    code = "NOT_FOLLOWING"


class NotCollectedError(ContentPlatformMockError):
    code = "NOT_COLLECTED"


class SelfFollowError(ContentPlatformMockError):
    code = "SELF_FOLLOW"
