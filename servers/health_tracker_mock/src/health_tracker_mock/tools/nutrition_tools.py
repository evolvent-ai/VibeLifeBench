from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.nutrition_service import NutritionService
from ._common import dumps, handle_errors


def register_nutrition_tools(mcp: FastMCP, nutrition_service: NutritionService) -> None:

    @mcp.tool()
    @handle_errors
    async def log_nutrition(
        user_id: str,
        meal: str,
        calories: int,
        logged_at: str,
        description: Optional[str] = None,
        protein_g: Optional[float] = None,
        carbs_g: Optional[float] = None,
        fat_g: Optional[float] = None,
    ) -> str:
        """Record a logged meal. meal ∈ {breakfast, lunch, dinner, snack}. calories is kcal (non-negative integer). logged_at is an ISO-8601 timestamp. description and macros (protein_g, carbs_g, fat_g in grams) are optional."""
        return dumps(
            nutrition_service.log_nutrition(
                user_id=user_id, meal=meal, calories=calories, logged_at=logged_at,
                description=description, protein_g=protein_g, carbs_g=carbs_g, fat_g=fat_g,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_nutrition_summary(user_id: str, date: str) -> str:
        """Sum a user's calories and macros for one calendar day (date=YYYY-MM-DD), with the meal entries. Reports totals only — no dietary advice."""
        return dumps(
            nutrition_service.get_nutrition_summary(user_id=user_id, date=date)
        )
