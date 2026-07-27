from typing import Optional


class HealthTrackerMockError(Exception):
    """Base exception for the health tracker mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(HealthTrackerMockError):
    code = "BAD_ARG"


class BadTypeError(HealthTrackerMockError):
    code = "BAD_TYPE"


class BadDateError(HealthTrackerMockError):
    code = "BAD_DATE"


class BadPeriodError(HealthTrackerMockError):
    code = "BAD_PERIOD"


class BadValueError(HealthTrackerMockError):
    code = "BAD_VALUE"


class MetricNotFoundError(HealthTrackerMockError):
    code = "METRIC_NOT_FOUND"


class WorkoutNotFoundError(HealthTrackerMockError):
    code = "WORKOUT_NOT_FOUND"


class GoalNotFoundError(HealthTrackerMockError):
    code = "GOAL_NOT_FOUND"
