"""Geocode / reverse_geocode tools."""

import logging
from mcp.server.fastmcp import FastMCP

from ..services.geocode_service import GeocodeService
from ..utils.exceptions import MapsMCPError

logger = logging.getLogger(__name__)


def register_geocode_tools(mcp: FastMCP, service: GeocodeService) -> None:

    @mcp.tool()
    async def geocode(address: str) -> dict:
        """Forward-geocode a free-form address to coordinates + place_id.

        Args:
            address: Free-form address or place name (e.g. "Tokyo Station").

        Returns:
            Dict with place_id, formatted, geo{lat,lng}, country, city,
            match_confidence — or {"error", "code"} on failure.
        """
        try:
            logger.info("geocode: %s", address)
            return service.geocode(address)
        except MapsMCPError as e:
            return {"error": str(e), "code": e.code}
        except Exception as e:
            logger.exception("geocode failed")
            return {"error": str(e), "code": "INTERNAL_ERROR"}

    @mcp.tool()
    async def reverse_geocode(lat: float, lng: float) -> dict:
        """Reverse-geocode (lat, lng) to the nearest known place (≤ 500m).

        Args:
            lat: Latitude in decimal degrees.
            lng: Longitude in decimal degrees.
        """
        try:
            logger.info("reverse_geocode: %s, %s", lat, lng)
            return service.reverse_geocode(float(lat), float(lng))
        except MapsMCPError as e:
            return {"error": str(e), "code": e.code}
        except Exception as e:
            logger.exception("reverse_geocode failed")
            return {"error": str(e), "code": "INTERNAL_ERROR"}
