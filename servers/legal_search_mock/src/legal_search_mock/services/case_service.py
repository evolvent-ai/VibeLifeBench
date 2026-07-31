"""Read-side case queries: search, detail, similar cases, citations."""
import logging
import sqlite3
from typing import List, Optional

from ..utils.dates import parse_date
from ..utils.exceptions import BadArgError
from ._common import (
    case_summary_dict,
    court_name,
    fetch_case,
    fetch_statute,
)

logger = logging.getLogger(__name__)

VALID_CASE_TYPES = (
    "劳动争议", "合同纠纷", "侵权责任", "婚姻家庭", "劳动仲裁", "其他",
)


class CaseService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- search ----------------------------------------------------------
    def search_cases(
        self,
        keyword: Optional[str] = None,
        court: Optional[str] = None,
        case_type: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 20,
    ) -> List[dict]:
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 100:
            limit = 100
        if case_type is not None and case_type not in VALID_CASE_TYPES:
            raise BadArgError(f"case_type must be one of {VALID_CASE_TYPES}")
        if date_from:
            parse_date(date_from)
        if date_to:
            parse_date(date_to)

        sql = ["SELECT * FROM cases WHERE 1=1"]
        args: List = []
        if keyword:
            like = f"%{keyword}%"
            sql.append(
                "AND (title LIKE ? OR cause LIKE ? OR summary LIKE ? "
                "OR keywords LIKE ? OR holding LIKE ?)"
            )
            args.extend([like, like, like, like, like])
        if court:
            # accept either court_id or (substring of) court name
            sql.append(
                "AND (court_id = ? OR court_id IN "
                "(SELECT court_id FROM courts WHERE name LIKE ?))"
            )
            args.extend([court, f"%{court}%"])
        if case_type:
            sql.append("AND case_type = ?")
            args.append(case_type)
        if date_from:
            sql.append("AND judgment_date >= ?")
            args.append(date_from)
        if date_to:
            sql.append("AND judgment_date <= ?")
            args.append(date_to)
        sql.append("ORDER BY judgment_date DESC, case_id ASC LIMIT ?")
        args.append(int(limit))

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [case_summary_dict(self.conn, r) for r in rows]

    # ---- detail ----------------------------------------------------------
    def get_case(self, case_id: str) -> dict:
        row = fetch_case(self.conn, case_id)
        return {
            "case_id": row["case_id"],
            "case_number": row["case_number"],
            "title": row["title"],
            "court_id": row["court_id"],
            "court_name": court_name(self.conn, row["court_id"]),
            "case_type": row["case_type"],
            "cause": row["cause"],
            "judgment_date": row["judgment_date"],
            "parties": row["parties"],
            "summary": row["summary"],
            "facts": row["facts"],
            "reasoning": row["reasoning"],
            "holding": row["holding"],
            "ruling": row["ruling"],
            "outcome": row["outcome"],
            "keywords": [k for k in (row["keywords"] or "").split(",") if k],
        }

    # ---- similar ---------------------------------------------------------
    def get_similar_cases(self, case_id: str, limit: int = 5) -> List[dict]:
        base = fetch_case(self.conn, case_id)
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 50:
            limit = 50

        base_kw = [k for k in (base["keywords"] or "").split(",") if k]
        rows = self.conn.execute(
            """
            SELECT * FROM cases
            WHERE case_id != ? AND case_type = ?
            ORDER BY judgment_date DESC, case_id ASC
            """,
            (case_id, base["case_type"]),
        ).fetchall()

        scored = []
        for r in rows:
            r_kw = set(k for k in (r["keywords"] or "").split(",") if k)
            overlap = len(r_kw & set(base_kw))
            scored.append((overlap, r))
        # higher keyword overlap first, then recency (rows already date-desc)
        scored.sort(key=lambda t: t[0], reverse=True)

        out = []
        for overlap, r in scored[:limit]:
            d = case_summary_dict(self.conn, r)
            d["shared_keyword_count"] = overlap
            out.append(d)
        return out

    # ---- citations -------------------------------------------------------
    def get_case_citations(self, case_id: str) -> dict:
        fetch_case(self.conn, case_id)  # raises CASE_NOT_FOUND
        rows = self.conn.execute(
            "SELECT * FROM citations WHERE case_id = ? ORDER BY citation_id ASC",
            (case_id,),
        ).fetchall()

        statutes_cited: List[dict] = []
        cases_cited: List[dict] = []
        for r in rows:
            if r["target_type"] == "article":
                art = self.conn.execute(
                    "SELECT * FROM statute_articles WHERE article_id = ?",
                    (r["target_id"],),
                ).fetchone()
                if art:
                    stat = fetch_statute(self.conn, art["statute_id"])
                    statutes_cited.append({
                        "citation_id": r["citation_id"],
                        "article_id": art["article_id"],
                        "article_no": art["article_no"],
                        "statute_id": stat["statute_id"],
                        "statute_name": stat["name"],
                        "label": r["label"],
                    })
            else:  # case
                tgt = self.conn.execute(
                    "SELECT * FROM cases WHERE case_id = ?", (r["target_id"],)
                ).fetchone()
                if tgt:
                    cases_cited.append({
                        "citation_id": r["citation_id"],
                        "case_id": tgt["case_id"],
                        "case_number": tgt["case_number"],
                        "title": tgt["title"],
                        "label": r["label"],
                    })
        return {
            "case_id": case_id,
            "statutes_cited": statutes_cited,
            "cases_cited": cases_cited,
        }
