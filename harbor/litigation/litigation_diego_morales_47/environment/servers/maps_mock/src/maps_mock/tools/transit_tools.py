"""Transit + traffic-estimate tools."""

import logging
from typing import Any, List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.transit_service import TransitService
from ..services.traffic_service import TrafficService
from ..services.directions_service import DirectionsService
from ..utils.exceptions import MapsMCPError

logger = logging.getLogger(__name__)


def register_transit_tools(
    mcp: FastMCP,
    transit_service: TransitService,
    traffic_service: TrafficService,
    directions_service: DirectionsService,
) -> None:

    @mcp.tool()
    async def get_transit(
        origin: str,
        dest: str,
        depart_at: str,
    ) -> Any:
        """Scheduled transit itineraries (up to 3).

        Args:
            origin:   Address or place_id near a transit stop.
            dest:     Address or place_id near a transit stop.
            depart_at: ISO-8601 departure datetime (required).
        """
        try:
            logger.info("get_transit: %s → %s @ %s", origin, dest, depart_at)
            if not depart_at:
                return {"error": "depart_at is required", "code": "INVALID_REQUEST"}
            result = transit_service.plan(origin, dest, depart_at)
            # Normalize: success returns a list; disruption/empty returns dict
            return result
        except MapsMCPError as e:
            return {"error": str(e), "code": e.code}
        except Exception as e:
            logger.exception("get_transit failed")
            return {"error": str(e), "code": "INTERNAL_ERROR"}

    @mcp.tool()
    async def get_traffic_estimate(
        origin: str,
        dest: str,
        depart_at: Optional[str] = None,
    ) -> dict:
        """Driving-only normal vs. with-traffic comparison.

        Args:
            origin:   Address or place_id.
            dest:     Address or place_id.
            depart_at: Optional ISO-8601 departure datetime.
        """
        try:
            logger.info("get_traffic_estimate: %s → %s", origin, dest)
            # Piggy-back on directions_service to get the baseline driving duration
            base = directions_service.directions(origin, dest, mode="driving",
                                                 depart_at=depart_at)
            if base.get("status") != "OK":
                return {"error": "could not compute baseline route",
                        "code": base.get("code", "ZERO_RESULTS")}
            route = base["routes"][0]
            origin_r = directions_service.geocode.resolve(origin)
            dest_r = directions_service.geocode.resolve(dest)
            if origin_r is None or dest_r is None:
                return {"error": "ZERO_RESULTS", "code": "ZERO_RESULTS"}
            return traffic_service.estimate(
                origin=origin_r,
                dest=dest_r,
                base_distance_m=route["distance_m"],
                base_duration_s=route["duration_s"],
                depart_at_iso=depart_at,
                current_date_iso="2026-05-01",
            )
        except MapsMCPError as e:
            return {"error": str(e), "code": e.code}
        except Exception as e:
            logger.exception("get_traffic_estimate failed")
            return {"error": str(e), "code": "INTERNAL_ERROR"}
