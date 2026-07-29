from typing import Annotated, Optional, TypedDict

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from ..services.reservation_service import ReservationService
from ._common import dumps, handle_errors


class GuestProfile(TypedDict):
    """Guest identity and ownership fields required by ReservationService."""

    first_name: Annotated[str, Field(description="Guest given/first name.")]
    last_name: Annotated[str, Field(description="Guest family/last name.")]
    email: Annotated[str, Field(description="Guest contact email address.")]
    phone: Annotated[str, Field(description="Guest contact phone number.")]
    user_id: Annotated[
        str,
        Field(description="Stable user_id that owns and can list this reservation."),
    ]


RatePlanId = Annotated[
    str,
    Field(
        description=(
            "Use the exact rate_plan_id returned by get_room_availability; "
            "its opaque format is "
            "rp_<hotel_id>_<room_type_slug>_<flavor>_<YYYYMMDD>_<YYYYMMDD>."
        )
    ),
]


def register_reservation_tools(mcp: FastMCP, reservation_service: ReservationService) -> None:

    @mcp.tool()
    @handle_errors
    async def create_reservation(
        rate_plan_id: RatePlanId,
        guest_profile: GuestProfile,
        payment_method_id: str,
        special_requests: Optional[str] = None,
    ) -> str:
        """Create a reservation for a rate_plan_id returned by get_room_availability."""
        result = reservation_service.create_reservation(
            rate_plan_id=rate_plan_id,
            guest_profile=guest_profile,
            payment_method_id=payment_method_id,
            special_requests=special_requests,
        )
        return dumps(result)

    @mcp.tool()
    @handle_errors
    async def get_reservation(reservation_id: str) -> str:
        """Return full detail for a reservation, including nights, special requests, modifications."""
        return dumps(reservation_service.get_reservation(reservation_id))

    @mcp.tool()
    @handle_errors
    async def list_reservations(user_id: str) -> str:
        """Return reservation IDs (newest first) for a user. Details via get_reservation."""
        return dumps(reservation_service.list_reservations(user_id))

    @mcp.tool()
    @handle_errors
    async def modify_reservation(
        reservation_id: str,
        new_check_in: Optional[str] = None,
        new_check_out: Optional[str] = None,
        new_room_type: Optional[str] = None,
    ) -> str:
        """Modify an existing reservation (dates and/or room type). Applies change fees per policy."""
        result = reservation_service.modify_reservation(
            reservation_id=reservation_id,
            new_check_in=new_check_in,
            new_check_out=new_check_out,
            new_room_type=new_room_type,
        )
        return dumps(result)

    @mcp.tool()
    @handle_errors
    async def cancel_reservation(reservation_id: str) -> str:
        """Cancel a reservation. Refund/penalty follow the rate-plan flavor and refund window."""
        return dumps(reservation_service.cancel_reservation(reservation_id))
