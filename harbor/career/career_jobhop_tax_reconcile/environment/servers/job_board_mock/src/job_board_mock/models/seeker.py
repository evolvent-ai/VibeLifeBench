from dataclasses import dataclass
from typing import Optional


@dataclass
class Resume:
    """A job-seeker's resume."""
    resume_id: str
    user_id: str
    name: str
    headline: str
    years_exp: int
    education: str
    skills: Optional[str]
    summary: Optional[str]
    updated_at: str


@dataclass
class SavedJob:
    """A bookmarked job."""
    user_id: str
    job_id: str
    saved_at: str


@dataclass
class Application:
    """A submitted job application.

    ``status`` advances through submitted → viewed → interview → offer
    (or rejected). Status transitions are driven out-of-band by the
    orchestrator's SQL mutations, not by the seeker.
    """
    application_id: str
    user_id: str
    job_id: str
    resume_id: str
    cover_letter: Optional[str]
    status: str  # submitted | viewed | interview | offer | rejected
    applied_at: str
    updated_at: str


@dataclass
class Chat:
    """A recruiter conversation thread tied to one job."""
    chat_id: str
    user_id: str
    job_id: str
    company_id: str
    recruiter_name: str
    created_at: str
    last_at: str


@dataclass
class ChatMessage:
    """One message inside a recruiter chat."""
    message_id: str
    chat_id: str
    sender: str  # user | recruiter
    body: str
    sent_at: str


@dataclass
class JobAlert:
    """A saved search that notifies the user of matching new jobs."""
    alert_id: str
    user_id: str
    query_json: str
    created_at: str
    active: bool
