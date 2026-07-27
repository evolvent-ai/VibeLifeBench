class MapsMCPError(Exception):
    """Base error for maps-mock. `code` is a short slug for tool responses."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        super().__init__(message)
        self.code = code


class NotFoundError(MapsMCPError):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, code="NOT_FOUND")


class InvalidArgumentError(MapsMCPError):
    def __init__(self, message: str = "Invalid argument"):
        super().__init__(message, code="INVALID_REQUEST")
