from dataclasses import dataclass
from typing import Optional


@dataclass
class Card:
    card_id: str
    user_id: str
    issuer: str
    product_name: str
    masked_no: str
    type: str
    credit_limit_minor: int
    available_credit_minor: int
    statement_balance_minor: int
    unbilled_balance_minor: int
    min_payment_due_minor: int
    due_date: Optional[str]
    cycle_start_day: int
    cycle_end_day: int
    grace_period_days: int
    status: str
    interest_apr_bp: int


@dataclass
class Statement:
    statement_id: str
    card_id: str
    period_start: str
    period_end: str
    opening_balance_minor: int
    new_charges_minor: int
    payments_minor: int
    closing_balance_minor: int
    min_payment_due_minor: int
    due_date: str
    status: str


@dataclass
class StatementLine:
    line_id: str
    statement_id: str
    posted_at: str
    amount_minor: int
    merchant_name: str
    mcc: Optional[str]
    category: Optional[str]
    kind: str
