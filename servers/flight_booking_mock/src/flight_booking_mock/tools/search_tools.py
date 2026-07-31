"""Search + offer detail + seat map tools."""
from __future__ import annotations

from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from ..services.search_service import SearchService


def register_search_tools(mcp: FastMCP, search_service: SearchService) -> None:
    @mcp.tool()
    async def search_flights(
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        adults: int = 1,
        children: int = 0,
        infants: int = 0,
        cabin: str = "ECONOMY",
        currency: str = "CNY",
        max_results: int = 20,
        sort: str = "price_asc",
        non_stop: bool = False,
        carriers: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Search flight offers for the given route and date(s).

        Args:
            origin: IATA 3-letter origin (e.g. "PVG").
            destination: IATA 3-letter destination (e.g. "NRT").
            departure_date: Outbound date "YYYY-MM-DD".
            return_date: Optional return date for round-trip search.
            adults: Paid adult pax (1..9).
            children: Children (0..8).
            infants: Lap infants (0..adults).
            cabin: ECONOMY | PREMIUM_ECONOMY | BUSINESS | FIRST.
            currency: ISO 4217 currency code (e.g. "CNY", "USD", "JPY").
            max_results: 1..50.
            sort: price_asc | duration_asc | depart_asc.
            non_stop: If true, only direct itineraries.
            carriers: Optional filter, e.g. ["JL","NH"].
        """
        return search_service.search_flights(
            origin=origin, destination=destination,
            departure_date=departure_date, return_date=return_date,
            adults=adults, children=children, infants=infants,
            cabin=cabin, currency=currency, max_results=max_results,
            sort=sort, non_stop=non_stop, carriers=carriers,
        )

    @mcp.tool()
    async def get_flight_offer(offer_id: str) -> dict[str, Any]:
        """Fetch the full expanded offer for a previously returned offer_id."""
        return search_service.get_flight_offer(offer_id)

    @mcp.tool()
    async def get_seat_map(
        segment_idx: int,
        offer_id: Optional[str] = None,
        pnr: Optional[str] = None,
    ) -> dict[str, Any]:
        """Return the seat map for a given offer/booking segment.

        Exactly one of offer_id or pnr must be provided.
        """
        return search_service.get_seat_map(offer_id, pnr, segment_idx)
