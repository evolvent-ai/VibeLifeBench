"""Offer repricing tool."""
from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..services.pricing_service import PricingService


def register_pricing_tools(mcp: FastMCP, pricing_service: PricingService) -> None:
    @mcp.tool()
    async def price_offer(offer_id: str) -> dict[str, Any]:
        """Reprice an offer prior to booking. May return a different total than
        `search_flights` reported (seat depletion, fare-bucket drift)."""
        return pricing_service.price_offer(offer_id)
