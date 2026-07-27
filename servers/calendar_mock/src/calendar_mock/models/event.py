from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    """A calendar event. ``start_dt`` / ``end_dt`` are ISO 8601 strings."""
    event_id: str
    calendar_id: str
    summary: str
    description: Optional[str]
    location: Optional[str]
    start_dt: str
    end_dt: str
    all_day: bool
    status: str  # confirmed | tentative | cancelled
    created_at: str
    updated_at: str
    recurrence_rule: Optional[str]
    parent_event_id: Optional[str] = None


@dataclass
class Attendee:
    """An invitee on an event."""
    id: int
    event_id: str
    email: str
    name: Optional[str]
    response_status: str  # needsAction | accepted | declined | tentative


@dataclass
class Reminder:
    """A pre-event reminder for the calendar owner."""
    id: int
    event_id: str
    method: str  # popup | email
    minutes_before: int
