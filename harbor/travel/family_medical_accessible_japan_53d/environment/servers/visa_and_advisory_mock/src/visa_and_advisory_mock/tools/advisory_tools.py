"""Advisory MCP tool registration."""

import json

from mcp.server.fastmcp import FastMCP

from ..services.advisory_service import AdvisoryService
from ..utils.exceptions import VisaError


def register_advisory_tools(mcp: FastMCP, advisory_service: AdvisoryService) -> None:
    @mcp.tool()
    async def get_advisory(country_code: str) -> str:
        """Return the latest travel advisory (level 1-4 + text) for a country."""
        try:
            result = advisory_service.get_advisory(country_code)
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)

    @mcp.tool()
    async def subscribe_advisory(country_code: str, sink: str) -> str:
        """Subscribe a sink (opaque delivery address) to advisory updates for a country."""
        try:
            result = advisory_service.subscribe(country_code, sink)
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)
