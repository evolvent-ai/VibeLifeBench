from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.catalog_service import CatalogService
from ._common import dumps, handle_errors


def register_catalog_tools(mcp: FastMCP, catalog_service: CatalogService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_jobs(
        keyword: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        min_salary_minor: Optional[int] = None,
        experience: Optional[str] = None,
        education: Optional[str] = None,
        sort: str = "relevance",
        limit: int = 20,
    ) -> str:
        """Search open job postings. `keyword` matches title/JD/requirements/tags. `city`/`category` are exact matches. `min_salary_minor` filters jobs whose monthly salary ceiling (in cents) is at least that value. `experience` ∈ intern/fresh_grad/1-3/3-5/5-10/10+. `education` ∈ unlimited/college/bachelor/master/phd. `sort` ∈ relevance/salary_desc/salary_asc/newest. Returns up to `limit` (max 100) compact job summaries."""
        return dumps(
            catalog_service.search_jobs(
                keyword=keyword,
                city=city,
                category=category,
                min_salary_minor=int(min_salary_minor) if min_salary_minor is not None else None,
                experience=experience,
                education=education,
                sort=sort,
                limit=int(limit),
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_job(job_id: str) -> str:
        """Return full detail for one job: JD, requirements, monthly salary range (cents) over salary_months, experience/education levels, tags, and status. Errors JOB_NOT_FOUND if unknown."""
        return dumps(catalog_service.get_job(job_id))

    @mcp.tool()
    @handle_errors
    async def get_company(company_id: str) -> str:
        """Return a company's profile: industry, size, funding stage, city, intro, rating, and current open job count. Errors COMPANY_NOT_FOUND if unknown."""
        return dumps(catalog_service.get_company(company_id))

    @mcp.tool()
    @handle_errors
    async def get_recommended_jobs(user_id: str, limit: int = 10) -> str:
        """Return up to `limit` (max 100) open jobs recommended for a user, ranked by deterministic skill/title overlap with the user's most recently updated resume (jobs already applied to are excluded). Each result includes a `match_score`."""
        return dumps(
            catalog_service.get_recommended_jobs(user_id=user_id, limit=int(limit))
        )
