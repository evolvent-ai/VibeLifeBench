"""Row-shape dataclasses (optional, for typing/docs only).

Services build plain dicts for JSON responses; these mirror the table
columns for reference.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Court:
    court_id: str
    name: str
    level: str
    region: str


@dataclass
class Case:
    case_id: str
    case_number: str
    title: str
    court_id: str
    case_type: str
    cause: str
    judgment_date: str
    parties: str
    summary: str
    facts: str
    reasoning: str
    holding: str
    ruling: str
    outcome: str
    keywords: str


@dataclass
class Statute:
    statute_id: str
    name: str
    short_name: str
    issuer: str
    effective_date: str
    status: str
    summary: str


@dataclass
class StatuteArticle:
    article_id: str
    statute_id: str
    article_no: str
    seq: int
    heading: str
    text: str


@dataclass
class Citation:
    citation_id: str
    case_id: str
    target_type: str
    target_id: str
    label: str


@dataclass
class SavedCase:
    saved_id: str
    user_id: str
    case_id: str
    note: Optional[str]
    saved_at: str


__all__ = [
    "Court",
    "Case",
    "Statute",
    "StatuteArticle",
    "Citation",
    "SavedCase",
]
