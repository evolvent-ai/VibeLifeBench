from typing import Optional


class JobBoardMockError(Exception):
    """Base exception for the job-board mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(JobBoardMockError):
    code = "BAD_ARG"


class BadDateError(JobBoardMockError):
    code = "BAD_DATE"


class JobNotFoundError(JobBoardMockError):
    code = "JOB_NOT_FOUND"


class CompanyNotFoundError(JobBoardMockError):
    code = "COMPANY_NOT_FOUND"


class ResumeNotFoundError(JobBoardMockError):
    code = "RESUME_NOT_FOUND"


class ApplicationNotFoundError(JobBoardMockError):
    code = "APPLICATION_NOT_FOUND"


class ChatNotFoundError(JobBoardMockError):
    code = "CHAT_NOT_FOUND"


class JobClosedError(JobBoardMockError):
    code = "JOB_CLOSED"


class AlreadyAppliedError(JobBoardMockError):
    code = "ALREADY_APPLIED"


class ResumeOwnershipError(JobBoardMockError):
    code = "RESUME_OWNERSHIP"
