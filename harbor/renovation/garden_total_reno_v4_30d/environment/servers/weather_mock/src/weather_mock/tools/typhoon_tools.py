from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from ..services.typhoon_service import TyphoonService
from ..utils.exceptions import UnknownStorm


def _dumps(obj: Any) -> str:
    return json.dumps(obj, default=str, ensure_ascii=False)


def register_typhoon_tools(mcp: FastMCP, service: TyphoonService) -> None:

    @mcp.tool()
    async def get_typhoon_track(storm_id: str) -> str:
        """Return the best-track / forecast track for a named typhoon.

        Args:
            storm_id: identifier supplied when the typhoon event was injected.
        """
        try:
            return _dumps(service.get_track(storm_id))
        except UnknownStorm:
            return _dumps({"error": "unknown_storm"})
        except Exception as e:
            return _dumps({"error": f"internal_error: {e}"})
