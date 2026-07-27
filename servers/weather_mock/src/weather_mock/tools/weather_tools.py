from __future__ import annotations

import json
from typing import Any, Union

from mcp.server.fastmcp import FastMCP

from ..services.weather_service import WeatherService
from ..utils.exceptions import InvalidGeo, WeatherNotFound
from ..utils.units import convert_obs_units


def _dumps(obj: Any) -> str:
    return json.dumps(obj, default=str, ensure_ascii=False)


def register_weather_tools(mcp: FastMCP, service: WeatherService) -> None:
    """Register get_current_weather / get_forecast_hourly / get_forecast_daily."""

    @mcp.tool()
    async def get_current_weather(geo: Union[dict, str], units: str = "metric") -> str:
        """Return current observed weather for a location.

        Args:
            geo: Either a supported city name (e.g. "Tokyo", "Hakone") or a
                 {"lat": ..., "lng": ...} dict (snapped to the nearest known
                 location within 50 km).
            units: "metric" (default) or "imperial" — swaps °C/km·h for °F/mph.
        """
        try:
            obs = service.get_current(geo)
            return _dumps(convert_obs_units(obs, units))
        except WeatherNotFound as e:
            return _dumps({"error": str(e)})
        except InvalidGeo as e:
            return _dumps({"error": f"invalid_geo: {e}"})
        except Exception as e:
            return _dumps({"error": f"internal_error: {e}"})

    @mcp.tool()
    async def get_forecast_hourly(
        geo: Union[dict, str], hours: int = 72
    ) -> str:
        """Return hourly forecast starting at next whole hour after sim-now.

        Args:
            geo: supported city name or {lat,lng}.
            hours: clamped to 1..120 (default 72).
        """
        try:
            rows = service.get_forecast_hourly(geo, hours=hours)
            return _dumps(rows)
        except WeatherNotFound as e:
            return _dumps({"error": str(e)})
        except InvalidGeo as e:
            return _dumps({"error": f"invalid_geo: {e}"})
        except Exception as e:
            return _dumps({"error": f"internal_error: {e}"})

    @mcp.tool()
    async def get_forecast_daily(
        geo: Union[dict, str], days: int = 10
    ) -> str:
        """Return daily forecast starting at sim-date.

        Args:
            geo: supported city name or {lat,lng}.
            days: clamped to 1..14 (default 10).
        """
        try:
            rows = service.get_forecast_daily(geo, days=days)
            return _dumps(rows)
        except WeatherNotFound as e:
            return _dumps({"error": str(e)})
        except InvalidGeo as e:
            return _dumps({"error": f"invalid_geo: {e}"})
        except Exception as e:
            return _dumps({"error": f"internal_error: {e}"})
