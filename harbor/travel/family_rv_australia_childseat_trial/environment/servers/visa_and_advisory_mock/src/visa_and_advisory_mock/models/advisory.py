"""Advisory / subscription / notification models."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Advisory(BaseModel):
    country_code: str
    level: int
    text: str
    updated_at: Optional[str] = None


class AdvisorySubscription(BaseModel):
    sub_id: str
    country_code: str
    sink: str
    created_at: Optional[str] = None


class Notification(BaseModel):
    id: str
    created_at: str
    channel: str
    payload: Dict[str, Any] = Field(default_factory=dict)
