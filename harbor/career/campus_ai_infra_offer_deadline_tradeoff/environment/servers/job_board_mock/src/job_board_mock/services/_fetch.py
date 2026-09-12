"""Shared row-fetch + serialization helpers for job_board services."""
import sqlite3

from ..utils.exceptions import (
    CompanyNotFoundError,
    JobNotFoundError,
    ResumeNotFoundError,
)


def fetch_job(conn: sqlite3.Connection, job_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
    ).fetchone()
    if not row:
        raise JobNotFoundError(f"job not found: {job_id}")
    return row


def fetch_company(conn: sqlite3.Connection, company_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM companies WHERE company_id = ?", (company_id,)
    ).fetchone()
    if not row:
        raise CompanyNotFoundError(f"company not found: {company_id}")
    return row


def fetch_resume(conn: sqlite3.Connection, resume_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM resumes WHERE resume_id = ?", (resume_id,)
    ).fetchone()
    if not row:
        raise ResumeNotFoundError(f"resume not found: {resume_id}")
    return row


def job_summary(conn: sqlite3.Connection, row: sqlite3.Row) -> dict:
    """Compact job dict for list/search results (joins company name)."""
    comp = conn.execute(
        "SELECT name FROM companies WHERE company_id = ?", (row["company_id"],)
    ).fetchone()
    return {
        "job_id": row["job_id"],
        "title": row["title"],
        "company_id": row["company_id"],
        "company_name": comp["name"] if comp else None,
        "city": row["city"],
        "category": row["category"],
        "salary_min_minor": int(row["salary_min_minor"]),
        "salary_max_minor": int(row["salary_max_minor"]),
        "salary_months": int(row["salary_months"]),
        "experience": row["experience"],
        "education": row["education"],
        "tags": row["tags"],
        "status": row["status"],
        "posted_at": row["posted_at"],
    }
