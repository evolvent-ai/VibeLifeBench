from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:
    """An employer listing jobs on the board."""
    company_id: str
    name: str
    industry: str
    size: str
    stage: Optional[str]
    city: str
    intro: str
    rating: float


@dataclass
class Job:
    """A job posting.

    Salary is stored as integer minor units (分) of *monthly* base pay,
    a range ``[salary_min_minor, salary_max_minor]`` paid over
    ``salary_months`` months per year (e.g. 13 for 13薪).
    """
    job_id: str
    company_id: str
    title: str
    city: str
    category: str
    salary_min_minor: int
    salary_max_minor: int
    salary_months: int
    experience: str  # intern | fresh_grad | 1-3 | 3-5 | 5-10 | 10+
    education: str  # unlimited | college | bachelor | master | phd
    jd: str
    requirements: str
    tags: Optional[str]
    status: str  # open | closed
    posted_at: str
