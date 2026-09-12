from mcp.server.fastmcp import FastMCP

from ..services.court_service import CourtService
from ._common import dumps, handle_errors


def register_court_tools(mcp: FastMCP, court_service: CourtService) -> None:

    @mcp.tool(description=(
        "List all courts and arbitration commissions in the corpus "
        "(court_id/name/level/region). The level field is corpus data, reported verbatim."
    ))
    @handle_errors
    async def list_courts() -> str:
        """List all courts and arbitration commissions in the corpus."""
        return dumps(court_service.list_courts())

    @mcp.tool()
    @handle_errors
    async def get_court(court_id: str) -> str:
        """Return one court's detail plus case_count (number of judgments in the corpus from this court). Errors COURT_NOT_FOUND."""
        return dumps(court_service.get_court(court_id))
