from dataclasses import dataclass
from typing import Optional


@dataclass
class Calendar:
    """A named calendar owned by a user (e.g. 'Personal', 'Work')."""
    calendar_id: str
    user_id: str
    name: str
    color: Optional[str]
    timezone: str
    is_primary: bool
    created_at: str
