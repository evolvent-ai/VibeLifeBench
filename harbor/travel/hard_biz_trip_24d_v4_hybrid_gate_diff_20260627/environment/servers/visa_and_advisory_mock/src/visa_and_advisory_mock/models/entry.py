"""Entry-requirement model."""

from typing import List, Optional

from pydantic import BaseModel, Field


class EntryRequirement(BaseModel):
    origin_nationality: str
    destination: str
    purpose: str
    visa_required: bool
    allowed_stay_days: int = 0
    passport_validity_months: int = 6
    docs_needed: List[str] = Field(default_factory=list)
    notes: str = ""
    updated_at: Optional[str] = None
