"""Custom exception types for the visa_and_advisory_mock server.

Tools generally return structured error dicts rather than raising. These
exceptions exist for service-internal control flow.
"""


class VisaError(Exception):
    """Base class for visa_and_advisory_mock errors."""

    code: str = "visa_error"

    def __init__(self, message: str, code: str | None = None):
        super().__init__(message)
        if code is not None:
            self.code = code

    def to_payload(self) -> dict:
        return {"error": str(self), "code": self.code}


class NotFound(VisaError):
    code = "not_found"


class InvalidState(VisaError):
    code = "invalid_state"


class ValidationError(VisaError):
    code = "validation_error"
