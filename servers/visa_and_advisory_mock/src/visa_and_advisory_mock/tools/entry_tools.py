"""check_entry_requirements MCP tool registration."""

import json
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.entry_service import EntryService
from ..utils.exceptions import VisaError


def register_entry_tools(mcp: FastMCP, entry_service: EntryService) -> None:
    @mcp.tool()
    async def check_entry_requirements(
        nationality: str,
        destination: str,
        purpose: str,
        transit_countries: Optional[List[str]] = None,
    ) -> str:
        """Look up entry rules for (nationality, destination, purpose).

        Args:
            nationality: ISO 3166-1 alpha-2 code (e.g. "CN").
            destination: ISO 3166-1 alpha-2 code (e.g. "JP").
            purpose: One of "tourism", "business", "transit".
            transit_countries: Ordered list of ISO alpha-2 transit-leg codes.
        """
        try:
            result = entry_service.check(
                nationality=nationality,
                destination=destination,
                purpose=purpose,
                transit_countries=transit_countries,
            )
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover — defensive
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)
