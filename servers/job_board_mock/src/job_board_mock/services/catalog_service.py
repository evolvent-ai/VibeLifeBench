"""Read-side job & company catalog: search, detail, recommendations."""
import logging
import sqlite3
from typing import List, Optional

from ..utils.exceptions import BadArgError
from ._fetch import fetch_company, fetch_job, job_summary

logger = logging.getLogger(__name__)

VALID_EXPERIENCE = ("intern", "fresh_grad", "1-3", "3-5", "5-10", "10+")
VALID_EDUCATION = ("unlimited", "college", "bachelor", "master", "phd")
VALID_SORT = ("relevance", "salary_desc", "salary_asc", "newest")


class CatalogService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- search ----------------------------------------------------------
    def search_jobs(
        self,
        keyword: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        min_salary_minor: Optional[int] = None,
        experience: Optional[str] = None,
        education: Optional[str] = None,
        sort: str = "relevance",
        limit: int = 20,
    ) -> List[dict]:
        if experience is not None and experience not in VALID_EXPERIENCE:
            raise BadArgError(f"experience must be one of {VALID_EXPERIENCE}")
        if education is not None and education not in VALID_EDUCATION:
            raise BadArgError(f"education must be one of {VALID_EDUCATION}")
        if sort not in VALID_SORT:
            raise BadArgError(f"sort must be one of {VALID_SORT}")
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 100:
            limit = 100

        sql = [
            "SELECT j.* FROM jobs j WHERE j.status = 'open'"
        ]
        args: List = []
        if keyword:
            like = f"%{keyword}%"
            sql.append(
                "AND (j.title LIKE ? OR j.jd LIKE ? OR j.requirements LIKE ? "
                "OR IFNULL(j.tags,'') LIKE ?)"
            )
            args.extend([like, like, like, like])
        if city:
            sql.append("AND j.city = ?")
            args.append(city)
        if category:
            sql.append("AND j.category = ?")
            args.append(category)
        if min_salary_minor is not None:
            sql.append("AND j.salary_max_minor >= ?")
            args.append(int(min_salary_minor))
        if experience:
            sql.append("AND j.experience = ?")
            args.append(experience)
        if education:
            sql.append("AND j.education = ?")
            args.append(education)

        if sort == "salary_desc":
            sql.append("ORDER BY j.salary_max_minor DESC, j.job_id ASC")
        elif sort == "salary_asc":
            sql.append("ORDER BY j.salary_min_minor ASC, j.job_id ASC")
        elif sort == "newest":
            sql.append("ORDER BY j.posted_at DESC, j.job_id ASC")
        else:  # relevance — stable: newest first then id
            sql.append("ORDER BY j.posted_at DESC, j.job_id ASC")
        sql.append("LIMIT ?")
        args.append(int(limit))

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [job_summary(self.conn, r) for r in rows]

    # ---- detail ----------------------------------------------------------
    def get_job(self, job_id: str) -> dict:
        row = fetch_job(self.conn, job_id)
        comp = self.conn.execute(
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
            "jd": row["jd"],
            "requirements": row["requirements"],
            "tags": row["tags"],
            "status": row["status"],
            "posted_at": row["posted_at"],
        }

    def get_company(self, company_id: str) -> dict:
        row = fetch_company(self.conn, company_id)
        open_jobs = self.conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE company_id = ? AND status = 'open'",
            (company_id,),
        ).fetchone()
        return {
            "company_id": row["company_id"],
            "name": row["name"],
            "industry": row["industry"],
            "size": row["size"],
            "stage": row["stage"],
            "city": row["city"],
            "intro": row["intro"],
            "rating": float(row["rating"]),
            "open_job_count": int(open_jobs["n"]),
        }

    # ---- recommendations -------------------------------------------------
    def get_recommended_jobs(self, user_id: str, limit: int = 10) -> List[dict]:
        """Recommend open jobs for a user based on their latest resume.

        Deterministic heuristic: rank open jobs by overlap between the
        resume's skills/headline and each job's title/tags/requirements,
        tie-broken by newest posting. No clock, no RNG.
        """
        if not user_id:
            raise BadArgError("user_id is required")
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 100:
            limit = 100

        resume = self.conn.execute(
            "SELECT * FROM resumes WHERE user_id = ? "
            "ORDER BY updated_at DESC, resume_id DESC LIMIT 1",
            (user_id,),
        ).fetchone()

        terms: List[str] = []
        if resume:
            for field in ("skills", "headline"):
                val = resume[field] or ""
                for tok in val.replace("、", ",").replace("/", ",").replace(" ", ",").split(","):
                    tok = tok.strip()
                    if len(tok) >= 2:
                        terms.append(tok)

        applied = {
            r["job_id"]
            for r in self.conn.execute(
                "SELECT job_id FROM applications WHERE user_id = ?", (user_id,)
            ).fetchall()
        }

        rows = self.conn.execute(
            "SELECT * FROM jobs WHERE status = 'open' "
            "ORDER BY posted_at DESC, job_id ASC"
        ).fetchall()

        scored = []
        for r in rows:
            if r["job_id"] in applied:
                continue
            hay = " ".join(
                [r["title"] or "", r["tags"] or "", r["requirements"] or ""]
            ).lower()
            score = sum(1 for t in terms if t.lower() in hay)
            scored.append((score, r))
        # Sort by score desc, then keep the existing newest-first order (stable).
        scored.sort(key=lambda sr: sr[0], reverse=True)

        out = []
        for score, r in scored[:limit]:
            item = job_summary(self.conn, r)
            item["match_score"] = int(score)
            out.append(item)
        return out
