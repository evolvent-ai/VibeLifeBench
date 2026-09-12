"""Directions + distance matrix tools."""

import logging
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.directions_service import DirectionsService
from ..utils.exceptions import MapsMCPError

logger = logging.getLogger(__name__)


def register_directions_tools(mcp: FastMCP, service: DirectionsService) -> None:

    @mcp.tool()
    async def directions(
        origin: str,
        dest: str,
        mode: str = "driving",
        depart_at: Optional[str] = None,
    ) -> dict:
        """Compute routes across driving/walking/bicycling/transit.

        Args:
            origin: place_id, free-form address, or "lat,lng".
            dest:   place_id, free-form address, or "lat,lng".
            mode:   "driving" | "walking" | "transit" | "bicycling".
            depart_at: Optional ISO-8601 departure datetime.
        """
        try:
            logger.info("directions: %s → %s (%s)", origin, dest, mode)
            return service.directions(origin, dest, mode=mode, depart_at=depart_at)
        except MapsMCPError as e:
            return {"error": str(e), "code": e.code}
        except Exception as e:
            logger.exception("directions failed")
            return {"error": str(e), "code": "INTERNAL_ERROR"}

    @mcp.tool()
    async def distance_matrix(
        origins: List[str],
        dests: List[str],
        mode: str = "driving",
    ) -> dict:
        """Batch distance + duration grid.

        Args:
            origins: Up to 25 origin strings (address / place_id / lat,lng).
            dests:   Up to 25 destination strings.
            mode:    "driving" | "walking" | "transit" | "bicycling".
        """
        try:
            logger.info("distance_matrix: %dx%d (%s)", len(origins), len(dests), mode)
            return service.distance_matrix(origins, dests, mode=mode)
        except MapsMCPError as e:
            return {"error": str(e), "code": e.code}
        except Exception as e:
            logger.exception("distance_matrix failed")
            return {"error": str(e), "code": "INTERNAL_ERROR"}
