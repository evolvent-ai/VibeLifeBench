from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.seeker_service import SeekerService
from ._common import dumps, handle_errors


def register_seeker_tools(mcp: FastMCP, seeker_service: SeekerService) -> None:

    # ---- resumes ---------------------------------------------------------
    @mcp.tool()
    @handle_errors
    async def create_resume(
        user_id: str,
        name: str,
        headline: str,
        years_exp: int = 0,
        education: str = "bachelor",
        skills: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> str:
        """Create a resume for a user. `headline` is the one-line title (e.g. "Backend Engineer"); `skills` is a free-text/comma-separated list; `years_exp` is whole years (>= 0). Returns the created resume."""
        return dumps(
            seeker_service.create_resume(
                user_id=user_id,
                name=name,
                headline=headline,
                years_exp=int(years_exp),
                education=education,
                skills=skills,
                summary=summary,
            )
        )

    @mcp.tool()
    @handle_errors
    async def update_resume(
        resume_id: str,
        name: Optional[str] = None,
        headline: Optional[str] = None,
        years_exp: Optional[int] = None,
        education: Optional[str] = None,
        skills: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> str:
        """Partially update a resume; only non-null fields are changed. Bumps updated_at. Errors RESUME_NOT_FOUND if unknown, BAD_ARG if no fields are supplied."""
        return dumps(
            seeker_service.update_resume(
                resume_id=resume_id,
                name=name,
                headline=headline,
                years_exp=int(years_exp) if years_exp is not None else None,
                education=education,
                skills=skills,
                summary=summary,
            )
        )

    @mcp.tool()
    @handle_errors
    async def list_resumes(user_id: str) -> str:
        """List a user's resumes, most recently updated first."""
        return dumps(seeker_service.list_resumes(user_id))

    @mcp.tool()
    @handle_errors
    async def get_resume(resume_id: str) -> str:
        """Return one resume in full. Errors RESUME_NOT_FOUND if unknown."""
        return dumps(seeker_service.get_resume(resume_id))

    # ---- saved jobs ------------------------------------------------------
    @mcp.tool()
    @handle_errors
    async def save_job(user_id: str, job_id: str) -> str:
        """Bookmark a job for a user (idempotent). Errors JOB_NOT_FOUND if the job is unknown."""
        return dumps(seeker_service.save_job(user_id=user_id, job_id=job_id))

    @mcp.tool()
    @handle_errors
    async def unsave_job(user_id: str, job_id: str) -> str:
        """Remove a job bookmark. Returns `removed: false` if it was not saved."""
        return dumps(seeker_service.unsave_job(user_id=user_id, job_id=job_id))

    @mcp.tool()
    @handle_errors
    async def list_saved_jobs(user_id: str) -> str:
        """List a user's saved (bookmarked) jobs, most recently saved first."""
        return dumps(seeker_service.list_saved_jobs(user_id))

    # ---- applications ----------------------------------------------------
    @mcp.tool()
    @handle_errors
    async def apply_job(
        user_id: str,
        job_id: str,
        resume_id: str,
        cover_letter: Optional[str] = None,
    ) -> str:
        """Apply to a job with one of the user's resumes. The new application starts at status `submitted`. Errors JOB_NOT_FOUND, JOB_CLOSED (job not open), RESUME_OWNERSHIP (resume not owned by user), or ALREADY_APPLIED (one application per user+job)."""
        return dumps(
            seeker_service.apply_job(
                user_id=user_id,
                job_id=job_id,
                resume_id=resume_id,
                cover_letter=cover_letter,
            )
        )

    @mcp.tool()
    @handle_errors
    async def list_applications(
        user_id: str, status_filter: Optional[str] = None
    ) -> str:
        """List a user's applications, newest first. Optional `status_filter` ∈ submitted/viewed/interview/offer/rejected."""
        return dumps(
            seeker_service.list_applications(
                user_id=user_id, status_filter=status_filter
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_application_status(application_id: str) -> str:
        """Return one application's current status and details (status ∈ submitted/viewed/interview/offer/rejected). Errors APPLICATION_NOT_FOUND if unknown."""
        return dumps(seeker_service.get_application_status(application_id))

    # ---- job alerts ------------------------------------------------------
    @mcp.tool()
    @handle_errors
    async def subscribe_job_alert(user_id: str, query_json: str) -> str:
        """Save a job-search alert for a user. `query_json` is a JSON string of search filters; keyword and city match the stored Chinese content, e.g. {"keyword":"后端","city":"上海","min_salary_minor":3000000} (keyword "后端" = backend, city "上海" = Shanghai). Errors BAD_ARG if `query_json` is not valid JSON."""
        return dumps(
            seeker_service.subscribe_job_alert(
                user_id=user_id, query_json=query_json
            )
        )
