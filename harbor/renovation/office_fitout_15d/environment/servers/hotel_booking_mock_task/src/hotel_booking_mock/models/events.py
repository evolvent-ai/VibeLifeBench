from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AdminEvent:
    type: str
    payload: dict = field(default_factory=dict)


@dataclass
class Notification:
    id: int
    created_at: str
    channel: str
    payload_json: dict = field(default_factory=dict)
