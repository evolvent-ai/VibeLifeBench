from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.issue_service import IssueService
from ._common import dumps, handle_errors


def register_issue_tools(mcp: FastMCP, issues: IssueService) -> None:

    @mcp.tool()
    @handle_errors
    async def report_issue(tracking_no: str, issue_type: str, description: str) -> str:
        """Open a customer-care ticket against a shipment.

        ``issue_type`` is one of {"lost", "damaged", "wrong_address", "missing_item",
        "delivery_failed"}. Returns ticket_id, status (always 'open'), and an
        expected_response_date computed from the per-type SLA.
        """
        return dumps(issues.report_issue(tracking_no, issue_type, description))

    @mcp.tool()
    @handle_errors
    async def list_issues(
        user_id: str,
        status_filter: Optional[str] = None,
    ) -> str:
        """List all support tickets owned by a user, newest first.

        Optional ``status_filter`` is one of {"open", "in_review", "resolved", "closed"}.
        """
        return dumps(issues.list_issues(user_id, status_filter))
