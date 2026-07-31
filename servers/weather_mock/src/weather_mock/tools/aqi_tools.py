from __future__ import annotations

import json
from typing import Any, Union

from mcp.server.fastmcp import FastMCP

from ..services.aqi_service import AQIService
from ..utils.exceptions import InvalidGeo, WeatherNotFound


def _dumps(obj: Any) -> str:
    return json.dumps(obj, default=str, ensure_ascii=False)


def register_aqi_tools(mcp: FastMCP, service: AQIService) -> None:

    @mcp.tool()
    async def get_aqi(geo: Union[dict, str]) -> str:
        """Return the current Air Quality Index for ``geo``.

        Args:
            geo: supported city name or {lat,lng}.
        """
        try:
            return _dumps(service.get_aqi(geo))
        except WeatherNotFound as e:
            return _dumps({"error": str(e)})
        except InvalidGeo as e:
            return _dumps({"error": f"invalid_geo: {e}"})
        except Exception as e:
            return _dumps({"error": f"internal_error: {e}"})
