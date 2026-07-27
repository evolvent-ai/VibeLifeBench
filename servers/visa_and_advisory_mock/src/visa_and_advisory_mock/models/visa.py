"""Visa product / application / document models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class VisaProduct(BaseModel):
    product_id: str
    destination: str
    nationality: str
    name: str
    processing_time_days: int
    fee_amount: int
    fee_currency: str
    delivery: str
    form_schema: Dict[str, Any] = Field(default_factory=dict)


class VisaApplication(BaseModel):
    application_id: str
    user_id: str
    product_id: str
    status: str
    applicant: Dict[str, Any] = Field(default_factory=dict)
    answers: Dict[str, Any] = Field(default_factory=dict)
    decision_day: Optional[int] = None
    decision_note: Optional[str] = None
    evisa_doc_ref: Optional[str] = None
    history: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ApplicationDocument(BaseModel):
    doc_id: str
    application_id: str
    kind: str
    ref: str
    uploaded_at: Optional[str] = None
