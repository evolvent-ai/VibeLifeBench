from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.workout_service import WorkoutService
from ._common import dumps, handle_errors


def register_workout_tools(mcp: FastMCP, workout_service: WorkoutService) -> None:

    @mcp.tool()
    @handle_errors
    async def log_workout(
        user_id: str,
        type: str,
        duration_min: int,
        started_at: str,
        calories: Optional[int] = None,
        distance_m: Optional[int] = None,
    ) -> str:
        """Record a workout session. type is a free-form label (e.g. run, gym, cycling, swim, yoga). duration_min is a positive integer of minutes. started_at is an ISO-8601 timestamp. calories (kcal) and distance_m (meters) are optional."""
        return dumps(
            workout_service.log_workout(
                user_id=user_id, type_=type, duration_min=duration_min,
                started_at=started_at, calories=calories, distance_m=distance_m,
            )
        )

    @mcp.tool()
    @handle_errors
    async def list_workouts(
        user_id: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 100,
    ) -> str:
        """List a user's workouts, newest first. Optional date window (YYYY-MM-DD, inclusive) and limit (default 100, max 500)."""
        return dumps(
            workout_service.list_workouts(
                user_id=user_id, since=since, until=until, limit=limit,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_workout(workout_id: str) -> str:
        """Return one workout by id. Errors WORKOUT_NOT_FOUND if unknown."""
        return dumps(workout_service.get_workout(workout_id=workout_id))

    @mcp.tool()
    @handle_errors
    async def get_activity_summary(user_id: str, date: str) -> str:
        """Aggregate one calendar day (date=YYYY-MM-DD) for a user: steps (latest steps reading that day), workout_count, active_minutes, workout_calories, distance_m, and the day's workout list."""
        return dumps(
            workout_service.get_activity_summary(user_id=user_id, date=date)
        )
