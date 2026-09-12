"""Stable, code-tagged exceptions for the notion mock server.

Each exception carries a short string ``code`` that becomes the ``code``
field in ``{"error", "code"}`` JSON responses. Never raised across the
MCP boundary — the tool decorator in ``tools/_common.py`` catches them
and returns JSON.
"""
from typing import Optional


class NotionMockError(Exception):
    """Base exception for the notion mock server."""

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(NotionMockError):
    code = "BAD_ARG"


class PageNotFoundError(NotionMockError):
    code = "PAGE_NOT_FOUND"


class BlockNotFoundError(NotionMockError):
    code = "BLOCK_NOT_FOUND"


class DatabaseNotFoundError(NotionMockError):
    code = "DATABASE_NOT_FOUND"


class UserNotFoundError(NotionMockError):
    code = "USER_NOT_FOUND"


class BadParentError(NotionMockError):
    code = "BAD_PARENT"


class BadPropertyError(NotionMockError):
    code = "BAD_PROPERTY"


class BadBlockTypeError(NotionMockError):
    code = "BAD_BLOCK_TYPE"


class NotImplementedStubError(NotionMockError):
    code = "NOT_IMPL"
