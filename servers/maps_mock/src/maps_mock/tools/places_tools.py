"""Places search + details tools."""

import logging
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from ..services.places_service import PlacesService
from ..utils.exceptions import MapsMCPError

logger = logging.getLogger(__name__)


def register_places_tools(mcp: FastMCP, service: PlacesService) -> None:

    @mcp.tool()
    async def search_places(
        query: str,
        geo: Optional[dict] = None,
        radius_m: int = 5000,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> Any:
        """Search for places by text (+ optional geo center and category).

        Args:
            query: Free-form text (e.g. "ramen", "temple").
            geo: Optional center {"lat": <float>, "lng": <float>}; if set, results
                are filtered by radius_m and sorted by distance.
            radius_m: Radius in metres when geo is set (default 5000).
            category: One of temple, museum, restaurant, station, airport,
                hotel, park, shrine, shopping, viewpoint, clinic, hospital,
                pharmacy, attraction.
            limit: Max results, 1..50 (default 10).

        Returns a list of places on success or a ``{"error","code"}`` dict on
        bad input (spec §3.3).
        """
        try:
            logger.info("search_places: %s (geo=%s cat=%s)", query, geo, category)
            return service.search(query, geo=geo, radius_m=radius_m,
                                  category=category, limit=limit)
        except MapsMCPError as e:
            return {"error": str(e), "code": e.code}
        except Exception as e:
            logger.exception("search_places failed")
            return {"error": str(e), "code": "INTERNAL_ERROR"}

    @mcp.tool()
    async def get_place_details(place_id: str) -> dict:
        """Full detail view for one place by id.

        Args:
            place_id: Place identifier (e.g. "pl_kiyomizu_dera").
        """
        try:
            logger.info("get_place_details: %s", place_id)
            return service.details(place_id)
        except MapsMCPError as e:
            return {"error": str(e), "code": e.code}
        except Exception as e:
            logger.exception("get_place_details failed")
            return {"error": str(e), "code": "INTERNAL_ERROR"}
