from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.case_service import CaseService
from ._common import dumps, handle_errors


def register_case_tools(mcp: FastMCP, case_service: CaseService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_cases(
        keyword: Optional[str] = None,
        court: Optional[str] = None,
        case_type: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 20,
    ) -> str:
        """Search anonymized case judgments, newest first. Filters: keyword (matches title/cause of action/holding/summary/keywords), court (court_id or court-name substring), case_type (one of the stored Chinese labels 劳动争议/合同纠纷/侵权责任/婚姻家庭/劳动仲裁/其他, i.e. labor dispute/contract dispute/tort liability/marriage & family/labor arbitration/other), date_from/date_to (judgment_date window, YYYY-MM-DD), limit (1-100, default 20). Returns compact case summaries."""
        return dumps(
            case_service.search_cases(
                keyword=keyword,
                court=court,
                case_type=case_type,
                date_from=date_from,
                date_to=date_to,
                limit=limit,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_case(case_id: str) -> str:
        """Return the full judgment for a case: anonymized parties/cause of action/facts/reasoning/holding/disposition/result/keywords. Errors CASE_NOT_FOUND if unknown."""
        return dumps(case_service.get_case(case_id))

    @mcp.tool()
    @handle_errors
    async def get_similar_cases(case_id: str, limit: int = 5) -> str:
        """Return cases of the same case_type ranked by shared-keyword overlap (then recency). limit 1-50, default 5. Each result includes shared_keyword_count. Errors CASE_NOT_FOUND."""
        return dumps(case_service.get_similar_cases(case_id, limit))

    @mcp.tool()
    @handle_errors
    async def get_case_citations(case_id: str) -> str:
        """Return what a case cites: statutes_cited (statute articles with article_id/article_no/statute_name) and cases_cited (referenced judgments). Errors CASE_NOT_FOUND."""
        return dumps(case_service.get_case_citations(case_id))
