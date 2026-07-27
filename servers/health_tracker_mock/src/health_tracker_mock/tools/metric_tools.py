from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.metric_service import MetricService
from ._common import dumps, handle_errors


def register_metric_tools(mcp: FastMCP, metric_service: MetricService) -> None:

    @mcp.tool()
    @handle_errors
    async def log_metric(
        user_id: str,
        type: str,
        value: float,
        recorded_at: str,
        unit: Optional[str] = None,
        value_text: Optional[str] = None,
    ) -> str:
        """Record a personal health metric reading. type ∈ {weight, steps, heart_rate, sleep_minutes, blood_pressure, body_fat}. value is numeric (default units: weight=g, steps=count, heart_rate=bpm, sleep_minutes=min, blood_pressure=mmHg systolic, body_fat=percent); pass unit to override. For composite readings like blood pressure, put "120/80" in value_text and the systolic number in value. recorded_at is an ISO-8601 timestamp. Records data only; never interprets it medically."""
        return dumps(
            metric_service.log_metric(
                user_id=user_id, type_=type, value=value,
                recorded_at=recorded_at, unit=unit, value_text=value_text,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_metrics(
        user_id: str,
        type: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 100,
    ) -> str:
        """List a user's readings of one metric type, newest first. Optional date window (YYYY-MM-DD, inclusive) and limit (default 100, max 1000)."""
        return dumps(
            metric_service.get_metrics(
                user_id=user_id, type_=type, since=since, until=until, limit=limit,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_latest_metric(user_id: str, type: str) -> str:
        """Return the single most recent reading of a metric type for a user. Errors METRIC_NOT_FOUND if none exist."""
        return dumps(metric_service.get_latest_metric(user_id=user_id, type_=type))

    @mcp.tool()
    @handle_errors
    async def get_metric_summary(user_id: str, type: str, period: str) -> str:
        """Summarize a metric over the trailing window ending at the user's latest reading: min/max/avg/first/last/delta/trend (up/down/flat). period ∈ {week (7d), month (30d)}. Descriptive statistics only — no medical interpretation."""
        return dumps(
            metric_service.get_metric_summary(user_id=user_id, type_=type, period=period)
        )
