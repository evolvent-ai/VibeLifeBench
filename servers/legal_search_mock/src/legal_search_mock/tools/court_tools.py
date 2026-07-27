from mcp.server.fastmcp import FastMCP

from ..services.court_service import CourtService
from ._common import dumps, handle_errors


def register_court_tools(mcp: FastMCP, court_service: CourtService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_courts() -> str:
        """List all courts and arbitration commissions in the corpus (court_id/name/level/region). level is one of the stored Chinese labels 基层法院/中级法院/高级法院/最高法院/仲裁委员会 (basic-level court/intermediate court/high court/supreme court/arbitration commission)."""
        return dumps(court_service.list_courts())

    @mcp.tool()
    @handle_errors
    async def get_court(court_id: str) -> str:
        """Return one court's detail plus case_count (number of judgments in the corpus from this court). Errors COURT_NOT_FOUND."""
        return dumps(court_service.get_court(court_id))
