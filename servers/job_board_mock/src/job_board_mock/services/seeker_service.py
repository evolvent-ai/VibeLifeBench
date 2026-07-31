"""Seeker side: resumes, saved jobs, applications, job alerts."""
import json
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    AlreadyAppliedError,
    ApplicationNotFoundError,
    BadArgError,
    JobClosedError,
    ResumeOwnershipError,
)
from ..utils.ids import (
    alert_id as make_alert_id,
    application_id as make_application_id,
    resume_id as make_resume_id,
)
from ._fetch import fetch_job, fetch_resume, job_summary

logger = logging.getLogger(__name__)


class SeekerService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- resumes ---------------------------------------------------------
    def create_resume(
        self,
        user_id: str,
        name: str,
        headline: str,
        years_exp: int = 0,
        education: str = "bachelor",
        skills: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> dict:
        if not user_id or not name or not headline:
            raise BadArgError("user_id, name, headline are required")
        if years_exp is None or int(years_exp) < 0:
            raise BadArgError("years_exp must be >= 0")
        seq = next_counter(self.conn, "resume_seq")
        new_id = make_resume_id(seq)
        ts = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO resumes (resume_id, user_id, name, headline, years_exp,
                                 education, skills, summary, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (new_id, user_id, name, headline, int(years_exp),
             education, skills, summary, ts),
        )
        return self.get_resume(new_id)

    def update_resume(
        self,
        resume_id: str,
        name: Optional[str] = None,
        headline: Optional[str] = None,
        years_exp: Optional[int] = None,
        education: Optional[str] = None,
        skills: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> dict:
        fetch_resume(self.conn, resume_id)
        fields = {
            "name": name,
            "headline": headline,
            "years_exp": int(years_exp) if years_exp is not None else None,
            "education": education,
            "skills": skills,
            "summary": summary,
        }
        sets = {k: v for k, v in fields.items() if v is not None}
        if not sets:
            raise BadArgError("no fields to update")
        if "years_exp" in sets and sets["years_exp"] < 0:
            raise BadArgError("years_exp must be >= 0")
        sets["updated_at"] = now_iso_z()
        cols = ", ".join(f"{k} = ?" for k in sets)
        self.conn.execute(
            f"UPDATE resumes SET {cols} WHERE resume_id = ?",
            list(sets.values()) + [resume_id],
        )
        return self.get_resume(resume_id)

    def list_resumes(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            "SELECT * FROM resumes WHERE user_id = ? "
            "ORDER BY updated_at DESC, resume_id DESC",
            (user_id,),
        ).fetchall()
        return [self._resume_row(r) for r in rows]

    def get_resume(self, resume_id: str) -> dict:
        return self._resume_row(fetch_resume(self.conn, resume_id))

    @staticmethod
    def _resume_row(r: sqlite3.Row) -> dict:
        return {
            "resume_id": r["resume_id"],
            "user_id": r["user_id"],
            "name": r["name"],
            "headline": r["headline"],
            "years_exp": int(r["years_exp"]),
            "education": r["education"],
            "skills": r["skills"],
            "summary": r["summary"],
            "updated_at": r["updated_at"],
        }

    # ---- saved jobs ------------------------------------------------------
    def save_job(self, user_id: str, job_id: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        fetch_job(self.conn, job_id)  # raises JOB_NOT_FOUND
        ts = now_iso_z()
        self.conn.execute(
            "INSERT INTO saved_jobs (user_id, job_id, saved_at) VALUES (?, ?, ?) "
            "ON CONFLICT(user_id, job_id) DO NOTHING",
            (user_id, job_id, ts),
        )
        row = self.conn.execute(
            "SELECT saved_at FROM saved_jobs WHERE user_id = ? AND job_id = ?",
            (user_id, job_id),
        ).fetchone()
        return {"user_id": user_id, "job_id": job_id,
                "saved": True, "saved_at": row["saved_at"]}

    def unsave_job(self, user_id: str, job_id: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        cur = self.conn.execute(
            "DELETE FROM saved_jobs WHERE user_id = ? AND job_id = ?",
            (user_id, job_id),
        )
        return {"user_id": user_id, "job_id": job_id,
                "saved": False, "removed": cur.rowcount > 0}

    def list_saved_jobs(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            "SELECT j.*, s.saved_at AS saved_at FROM saved_jobs s "
            "JOIN jobs j ON j.job_id = s.job_id "
            "WHERE s.user_id = ? ORDER BY s.saved_at DESC, j.job_id ASC",
            (user_id,),
        ).fetchall()
        out = []
        for r in rows:
            item = job_summary(self.conn, r)
            item["saved_at"] = r["saved_at"]
            out.append(item)
        return out

    # ---- applications ----------------------------------------------------
    def apply_job(
        self,
        user_id: str,
        job_id: str,
        resume_id: str,
        cover_letter: Optional[str] = None,
    ) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        job = fetch_job(self.conn, job_id)
        if job["status"] != "open":
            raise JobClosedError(f"job {job_id} is not open for applications")
        resume = fetch_resume(self.conn, resume_id)
        if resume["user_id"] != user_id:
            raise ResumeOwnershipError(
                f"resume {resume_id} does not belong to user {user_id}"
            )
        dup = self.conn.execute(
            "SELECT application_id FROM applications WHERE user_id = ? AND job_id = ?",
            (user_id, job_id),
        ).fetchone()
        if dup:
            raise AlreadyAppliedError(
                f"already applied to {job_id} (application {dup['application_id']})"
            )
        seq = next_counter(self.conn, "application_seq")
        new_id = make_application_id(seq)
        ts = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO applications (application_id, user_id, job_id, resume_id,
                                      cover_letter, status, applied_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'submitted', ?, ?)
            """,
            (new_id, user_id, job_id, resume_id, cover_letter, ts, ts),
        )
        return self.get_application_status(new_id)

    def list_applications(
        self, user_id: str, status_filter: Optional[str] = None
    ) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        valid = ("submitted", "viewed", "interview", "offer", "rejected")
        if status_filter is not None and status_filter not in valid:
            raise BadArgError(f"status_filter must be one of {valid}")
        sql = ["SELECT * FROM applications WHERE user_id = ?"]
        args: List = [user_id]
        if status_filter:
            sql.append("AND status = ?")
            args.append(status_filter)
        sql.append("ORDER BY applied_at DESC, application_id DESC")
        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [self._application_row(r) for r in rows]

    def get_application_status(self, application_id: str) -> dict:
        row = self.conn.execute(
            "SELECT * FROM applications WHERE application_id = ?", (application_id,)
        ).fetchone()
        if not row:
            raise ApplicationNotFoundError(
                f"application not found: {application_id}"
            )
        return self._application_row(row)

    def _application_row(self, r: sqlite3.Row) -> dict:
        job = self.conn.execute(
            "SELECT title, company_id FROM jobs WHERE job_id = ?", (r["job_id"],)
        ).fetchone()
        comp_name = None
        if job:
            comp = self.conn.execute(
                "SELECT name FROM companies WHERE company_id = ?",
                (job["company_id"],),
            ).fetchone()
            comp_name = comp["name"] if comp else None
        return {
            "application_id": r["application_id"],
            "user_id": r["user_id"],
            "job_id": r["job_id"],
            "job_title": job["title"] if job else None,
            "company_name": comp_name,
            "resume_id": r["resume_id"],
            "cover_letter": r["cover_letter"],
            "status": r["status"],
            "applied_at": r["applied_at"],
            "updated_at": r["updated_at"],
        }

    # ---- job alerts ------------------------------------------------------
    def subscribe_job_alert(self, user_id: str, query_json: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        if not query_json:
            raise BadArgError("query_json is required")
        try:
            json.loads(query_json)
        except (TypeError, ValueError) as e:
            raise BadArgError(f"query_json must be valid JSON: {e}")
        seq = next_counter(self.conn, "alert_seq")
        new_id = make_alert_id(seq)
        ts = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO job_alerts (alert_id, user_id, query_json, created_at, active)
            VALUES (?, ?, ?, ?, 1)
            """,
            (new_id, user_id, query_json, ts),
        )
        return {
            "alert_id": new_id,
            "user_id": user_id,
            "query_json": query_json,
            "created_at": ts,
            "active": True,
        }
