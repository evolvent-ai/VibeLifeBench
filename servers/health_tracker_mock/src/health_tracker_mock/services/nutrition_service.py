"""Nutrition logging + per-day summary."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import parse_date, parse_ts
from ..utils.exceptions import BadValueError
from ..utils.ids import nutrition_id as make_nutrition_id

logger = logging.getLogger(__name__)

VALID_MEALS = ("breakfast", "lunch", "dinner", "snack")


def _row_to_nutrition(r: sqlite3.Row) -> dict:
    return {
        "nutrition_id": r["nutrition_id"],
        "user_id": r["user_id"],
        "meal": r["meal"],
        "description": r["description"],
        "calories": int(r["calories"]),
        "protein_g": float(r["protein_g"]) if r["protein_g"] is not None else None,
        "carbs_g": float(r["carbs_g"]) if r["carbs_g"] is not None else None,
        "fat_g": float(r["fat_g"]) if r["fat_g"] is not None else None,
        "logged_at": r["logged_at"],
    }


class NutritionService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def log_nutrition(
        self,
        user_id: str,
        meal: str,
        calories: int,
        logged_at: str,
        description: Optional[str] = None,
        protein_g: Optional[float] = None,
        carbs_g: Optional[float] = None,
        fat_g: Optional[float] = None,
    ) -> dict:
        if not user_id:
            raise BadValueError("user_id is required")
        if meal not in VALID_MEALS:
            raise BadValueError(f"meal must be one of {VALID_MEALS}")
        if calories is None or int(calories) < 0:
            raise BadValueError("calories must be a non-negative integer")
        parse_ts(logged_at)

        seq = next_counter(self.conn, "nutrition_seq")
        nid = make_nutrition_id(seq)
        self.conn.execute(
            """
            INSERT INTO nutrition_logs
              (nutrition_id, user_id, meal, description, calories, protein_g, carbs_g, fat_g, logged_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                nid, user_id, meal, description, int(calories),
                float(protein_g) if protein_g is not None else None,
                float(carbs_g) if carbs_g is not None else None,
                float(fat_g) if fat_g is not None else None,
                logged_at,
            ),
        )
        row = self.conn.execute(
            "SELECT * FROM nutrition_logs WHERE nutrition_id = ?", (nid,)
        ).fetchone()
        return _row_to_nutrition(row)

    def get_nutrition_summary(self, user_id: str, date: str) -> dict:
        """Sum calories and macros for one calendar day, with the meal entries."""
        if not user_id:
            raise BadValueError("user_id is required")
        parse_date(date)
        rows = self.conn.execute(
            """
            SELECT * FROM nutrition_logs
            WHERE user_id = ? AND substr(logged_at, 1, 10) = ?
            ORDER BY logged_at ASC, nutrition_id ASC
            """,
            (user_id, date),
        ).fetchall()
        meals: List[dict] = [_row_to_nutrition(r) for r in rows]

        def _sum(key: str) -> float:
            return round(sum(m[key] or 0 for m in meals), 1)

        return {
            "user_id": user_id,
            "date": date,
            "meal_count": len(meals),
            "total_calories": sum(m["calories"] for m in meals),
            "total_protein_g": _sum("protein_g"),
            "total_carbs_g": _sum("carbs_g"),
            "total_fat_g": _sum("fat_g"),
            "meals": meals,
        }
