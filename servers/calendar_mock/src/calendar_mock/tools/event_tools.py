from typing import Any, List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.event_service import EventService
from ._common import dumps, handle_errors


def register_event_tools(mcp: FastMCP, event_service: EventService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_events(
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        calendar_id: Optional[str] = None,
        max_results: int = 20,
        order_by: str = "startTime",
    ) -> str:
        """List events overlapping a time window (ISO 8601). Optional `calendar_id` restricts to a single calendar; without it, all calendars are searched. `order_by` is `startTime` or `updated`. Default limit 20, max 500."""
        return dumps(
            event_service.list_events(
                time_min=time_min,
                time_max=time_max,
                calendar_id=calendar_id,
                max_results=int(max_results),
                order_by=order_by,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_event(
        event_id: str, calendar_id: Optional[str] = None
    ) -> str:
        """Return full detail for a single event, including attendees and reminders. `calendar_id` is optional but, when supplied, scopes the lookup."""
        return dumps(event_service.get_event(event_id, calendar_id))

    @mcp.tool()
    @handle_errors
    async def create_event(
        summary: str,
        start: str,
        end: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        calendar_id: Optional[str] = None,
        attendees: Optional[List[dict]] = None,
        reminders: Optional[List[dict]] = None,
    ) -> str:
        """Create a new calendar event. `start`/`end` are ISO 8601 datetimes (e.g. `2026-05-10T09:00:00+08:00`). If `calendar_id` is omitted, the primary calendar is used. `attendees` is a list of `{email, name?, response_status?}` and `reminders` a list of `{minutes_before, method?}` where method is `popup` or `email`."""
        return dumps(
            event_service.create_event(
                summary=summary,
                start=start,
                end=end,
                description=description,
                location=location,
                calendar_id=calendar_id,
                attendees=attendees,
                reminders=reminders,
            )
        )

    @mcp.tool()
    @handle_errors
    async def update_event(
        event_id: str,
        summary: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        calendar_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """Patch an event. Only the supplied fields change. `status` is one of `confirmed`, `tentative`, `cancelled`. To move between calendars set `calendar_id`."""
        return dumps(
            event_service.update_event(
                event_id=event_id,
                summary=summary,
                start=start,
                end=end,
                description=description,
                location=location,
                calendar_id=calendar_id,
                status=status,
            )
        )

    @mcp.tool()
    @handle_errors
    async def delete_event(
        event_id: str, calendar_id: Optional[str] = None
    ) -> str:
        """Delete an event. Returns EVENT_NOT_FOUND if the id is unknown (or does not belong to the supplied calendar_id, if given)."""
        return dumps(event_service.delete_event(event_id, calendar_id))

    @mcp.tool()
    @handle_errors
    async def search_events(
        query: str,
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        max_results: int = 50,
    ) -> str:
        """Substring search over event summary, description, location, and attendee name/email. Case-insensitive. Optional `time_min`/`time_max` (ISO 8601) restrict the window."""
        return dumps(
            event_service.search_events(
                query=query,
                time_min=time_min,
                time_max=time_max,
                max_results=int(max_results),
            )
        )
