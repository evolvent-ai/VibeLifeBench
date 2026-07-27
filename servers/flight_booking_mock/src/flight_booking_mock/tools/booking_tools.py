"""Booking management tools."""
from __future__ import annotations

from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from ..services.booking_service import BookingService


def register_booking_tools(mcp: FastMCP, booking_service: BookingService) -> None:
    @mcp.tool()
    async def create_booking(
        offer_id: str,
        passengers: list[dict[str, Any]],
        contact: dict[str, str],
        payment: dict[str, Any],
        seat_selections: Optional[list[dict[str, Any]]] = None,
        hold: bool = False,
    ) -> dict[str, Any]:
        """Issue a PNR for a priced offer.

        Args:
            offer_id: Offer id from search_flights/price_offer.
            passengers: List of {type, given_name, family_name, dob, ...}.
            contact: {email, phone}.
            payment: {method: "CARD"|"POINTS", card_last4?}.
            seat_selections: Optional seat picks {segment_idx, pax_idx, seat}.
            hold: If true, issue a HOLD instead of TICKETED.
        """
        return booking_service.create_booking(
            offer_id=offer_id, passengers=passengers, contact=contact,
            payment=payment, seat_selections=seat_selections, hold=hold,
        )

    @mcp.tool()
    async def get_booking(pnr: str) -> dict[str, Any]:
        """Retrieve a booking by PNR."""
        return booking_service.get_booking(pnr)

    @mcp.tool()
    async def list_bookings(
        user_id: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        """List bookings for a user/email with optional status filter."""
        return booking_service.list_bookings(
            user_id=user_id, email=email, status=status,
            page=page, page_size=page_size,
        )

    @mcp.tool()
    async def cancel_booking(pnr: str, reason: Optional[str] = None) -> dict[str, Any]:
        """Cancel a PNR and return refund breakdown."""
        return booking_service.cancel_booking(pnr=pnr, reason=reason)

    @mcp.tool()
    async def change_booking(
        pnr: str,
        new_offer_id: str,
        segment_indices: Optional[list[int]] = None,
    ) -> dict[str, Any]:
        """Exchange one or more segments on a PNR for a new priced offer."""
        return booking_service.change_booking(
            pnr=pnr, new_offer_id=new_offer_id,
            segment_indices=segment_indices,
        )

    @mcp.tool()
    async def check_in(
        pnr: str,
        segment_idx: int,
        pax_indices: Optional[list[int]] = None,
        preferred_seats: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """Online check-in for a segment (must be within T-48h to T-45m)."""
        return booking_service.check_in(
            pnr=pnr, segment_idx=segment_idx,
            pax_indices=pax_indices, preferred_seats=preferred_seats,
        )
