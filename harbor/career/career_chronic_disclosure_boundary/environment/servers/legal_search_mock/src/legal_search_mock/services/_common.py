"""Row-fetch + serialization helpers shared across services.

These operate on an existing ``sqlite3.Connection`` and never manage
transactions of their own.
"""
import sqlite3

from ..utils.exceptions import (
    ArticleNotFoundError,
    CaseNotFoundError,
    CourtNotFoundError,
    StatuteNotFoundError,
)


def fetch_case(conn: sqlite3.Connection, case_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM cases WHERE case_id = ?", (case_id,)
    ).fetchone()
    if not row:
        raise CaseNotFoundError(f"case not found: {case_id}")
    return row


def fetch_statute(conn: sqlite3.Connection, statute_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM statutes WHERE statute_id = ?", (statute_id,)
    ).fetchone()
    if not row:
        raise StatuteNotFoundError(f"statute not found: {statute_id}")
    return row


def fetch_article(conn: sqlite3.Connection, article_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM statute_articles WHERE article_id = ?", (article_id,)
    ).fetchone()
    if not row:
        raise ArticleNotFoundError(f"article not found: {article_id}")
    return row


def fetch_court(conn: sqlite3.Connection, court_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM courts WHERE court_id = ?", (court_id,)
    ).fetchone()
    if not row:
        raise CourtNotFoundError(f"court not found: {court_id}")
    return row


def court_name(conn: sqlite3.Connection, court_id: str) -> str:
    row = conn.execute(
        "SELECT name FROM courts WHERE court_id = ?", (court_id,)
    ).fetchone()
    return row["name"] if row else court_id


def case_summary_dict(conn: sqlite3.Connection, row: sqlite3.Row) -> dict:
    """A compact case shape used in search results / similar lists."""
    return {
        "case_id": row["case_id"],
        "case_number": row["case_number"],
        "title": row["title"],
        "court_id": row["court_id"],
        "court_name": court_name(conn, row["court_id"]),
        "case_type": row["case_type"],
        "cause": row["cause"],
        "judgment_date": row["judgment_date"],
        "outcome": row["outcome"],
        "summary": row["summary"],
    }
