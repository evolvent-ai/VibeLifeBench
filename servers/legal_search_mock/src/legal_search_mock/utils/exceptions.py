from typing import Optional


class LegalSearchMockError(Exception):
    """Base exception for the legal_search mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(LegalSearchMockError):
    code = "BAD_ARG"


class BadDateError(LegalSearchMockError):
    code = "BAD_DATE"


class CaseNotFoundError(LegalSearchMockError):
    code = "CASE_NOT_FOUND"


class StatuteNotFoundError(LegalSearchMockError):
    code = "STATUTE_NOT_FOUND"


class ArticleNotFoundError(LegalSearchMockError):
    code = "ARTICLE_NOT_FOUND"


class CourtNotFoundError(LegalSearchMockError):
    code = "COURT_NOT_FOUND"


class SavedCaseNotFoundError(LegalSearchMockError):
    code = "SAVED_CASE_NOT_FOUND"
