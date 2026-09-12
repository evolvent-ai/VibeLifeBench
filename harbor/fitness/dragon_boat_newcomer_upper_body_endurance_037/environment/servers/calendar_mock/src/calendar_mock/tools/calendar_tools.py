from mcp.server.fastmcp import FastMCP

from ..services.calendar_service import CalendarService
from ._common import dumps, handle_errors


def register_calendar_tools(mcp: FastMCP, calendar_service: CalendarService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_calendars(user_id: str) -> str:
        """List a user's calendars (e.g. Personal, Work). Returns id, name, color, timezone, and whether it is the primary."""
        return dumps(calendar_service.list_calendars(user_id))
