from dataclasses import dataclass
from typing import Optional


@dataclass
class Metric:
    """A single recorded health metric.

    ``value`` is numeric; for composite readings (e.g. blood_pressure
    ``120/80``) the human-readable form is also kept in ``value_text`` and
    ``value`` carries the systolic component for ordering/summaries.

    Units by type: weight=g, steps=count, heart_rate=bpm,
    sleep_minutes=min, blood_pressure=mmHg, body_fat=percent.
    """
    metric_id: str
    user_id: str
    type: str
    value: float
    value_text: Optional[str]
    unit: str
    recorded_at: str


@dataclass
class Workout:
    """A logged workout session."""
    workout_id: str
    user_id: str
    type: str
    duration_min: int
    calories: Optional[int]
    distance_m: Optional[int]
    started_at: str


@dataclass
class Goal:
    """A user health goal.

    ``direction`` is ``at_least`` (e.g. weekly run distance) or ``at_most``
    (e.g. target weight). ``period`` is the recurrence the target applies to.
    """
    goal_id: str
    user_id: str
    type: str
    target: float
    unit: str
    period: str
    direction: str
    start_date: str
    status: str


@dataclass
class NutritionLog:
    """A logged meal."""
    nutrition_id: str
    user_id: str
    meal: str
    description: Optional[str]
    calories: int
    protein_g: Optional[float]
    carbs_g: Optional[float]
    fat_g: Optional[float]
    logged_at: str


__all__ = ["Metric", "Workout", "Goal", "NutritionLog"]
