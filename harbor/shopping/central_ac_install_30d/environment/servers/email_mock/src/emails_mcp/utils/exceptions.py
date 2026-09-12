from typing import Optional


class EmailsMockError(Exception):
    """Base exception for the emails mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(EmailsMockError):
    code = "BAD_ARG"


class ValidationError(EmailsMockError):
    code = "VALIDATION_ERROR"


class FolderNotFoundError(EmailsMockError):
    code = "FOLDER_NOT_FOUND"


class FolderExistsError(EmailsMockError):
    code = "FOLDER_EXISTS"


class FolderProtectedError(EmailsMockError):
    code = "FOLDER_PROTECTED"


class EmailNotFoundError(EmailsMockError):
    code = "EMAIL_NOT_FOUND"


class DraftNotFoundError(EmailsMockError):
    code = "DRAFT_NOT_FOUND"


class AttachmentNotFoundError(EmailsMockError):
    code = "ATTACHMENT_NOT_FOUND"


class FileError(EmailsMockError):
    code = "FILE_ERROR"
