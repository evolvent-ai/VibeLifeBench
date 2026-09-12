from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.case_service import CaseService
from ._common import dumps, handle_errors


def register_case_tools(mcp: FastMCP, case_service: CaseService) -> None:

    @mcp.tool(description=(
        "Search anonymized case judgments, newest first. Filters: keyword "
        "(matches title/cause of action/holding/summary/keywords), court "
        "(court_id or court-name substring), "
        "case_type filter; values are corpus data and differ per deployment — "
        "take one from a previous result's case_type field and pass it back "
        "verbatim rather than composing one. "
        "date_from/date_to (judgment_date window, YYYY-MM-DD). "
        "Paginated: limit (1-100, default 20) is the page size, page (≥1) "
        "selects which page. Returns an envelope {items, total, page, "
        "page_size, has_more}; pass page=2,3,… while has_more is true to read "
        "the full result set. The outcome field is corpus data, reported "
        "verbatim."
    ))
    @handle_errors
    async def search_cases(
        keyword: Optional[str] = None,
        court: Optional[str] = None,
        case_type: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> str:
        """Search anonymized case judgments, newest first."""
        return dumps(
            case_service.search_cases(
                keyword=keyword,
                court=court,
                case_type=case_type,
                date_from=date_from,
                date_to=date_to,
                limit=limit,
                page=page,
            )
        )

    @mcp.tool(description=(
        "Return the full judgment for a case: anonymized parties/cause of "
        "action/facts/reasoning/holding/disposition/result/keywords. "
        "The result's outcome field is corpus data, reported verbatim. "
        "Errors CASE_NOT_FOUND if unknown."
    ))
    @handle_errors
    async def get_case(case_id: str) -> str:
        """Return the full judgment for a case."""
        return dumps(case_service.get_case(case_id))

    @mcp.tool(description=(
        "Return cases of the same case_type ranked by shared-keyword overlap "
        "(then recency). Paginated: limit (1-50, default 5) is the page size, "
        "page (≥1) selects which page. Each item includes "
        "shared_keyword_count. Returns an envelope {items, total, page, "
        "page_size, has_more}; pass page=2,3,… while has_more is true to read "
        "the full result set. Errors CASE_NOT_FOUND."
    ))
    @handle_errors
    async def get_similar_cases(case_id: str, limit: int = 5, page: int = 1) -> str:
        """Return cases of the same case_type ranked by shared-keyword overlap."""
        return dumps(case_service.get_similar_cases(case_id, limit=limit, page=page))

    @mcp.tool()
    @handle_errors
    async def get_case_citations(case_id: str) -> str:
        """Return what a case cites: statutes_cited (statute articles with article_id/article_no/statute_name) and cases_cited (referenced judgments). Errors CASE_NOT_FOUND."""
        return dumps(case_service.get_case_citations(case_id))
