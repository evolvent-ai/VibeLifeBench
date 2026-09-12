from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.goal_service import GoalService
from ._common import dumps, handle_errors


def register_goal_tools(mcp: FastMCP, goal_service: GoalService) -> None:

    @mcp.tool()
    @handle_errors
    async def set_goal(
        user_id: str,
        type: str,
        target: float,
        period: str,
        unit: Optional[str] = None,
        direction: str = "at_least",
        start_date: Optional[str] = None,
    ) -> str:
        """Create a health goal. type is a label (e.g. weight, run_distance, steps, workouts). target is the numeric goal. period ∈ {day, week, month, once}. direction ∈ {at_least (more is better, e.g. weekly run distance), at_most (less is better, e.g. target weight)}. unit and start_date (YYYY-MM-DD) optional. Returns the goal with status='active'."""
        return dumps(
            goal_service.set_goal(
                user_id=user_id, type_=type, target=target, period=period,
                unit=unit, direction=direction, start_date=start_date,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_goals(user_id: str, status: Optional[str] = None) -> str:
        """List a user's goals. Optional status filter ∈ {active, achieved, abandoned}."""
        return dumps(goal_service.get_goals(user_id=user_id, status=status))

    @mcp.tool()
    @handle_errors
    async def get_goal_progress(user_id: str, goal_id: str) -> str:
        """Compute descriptive progress for a goal over its current period window: current value, percent_of_target, and a boolean on_track. Reports numbers only — no advice or diagnosis. Errors GOAL_NOT_FOUND if unknown."""
        return dumps(
            goal_service.get_goal_progress(user_id=user_id, goal_id=goal_id)
        )
