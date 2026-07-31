from dataclasses import dataclass
from typing import Optional


@dataclass
class RecurringPayment:
    """A recurring debit schedule from an account to a payee."""
    schedule_id: str
    user_id: str
    account_id: str
    payee_id: str
    amount_minor: int
    freq: str  # daily | weekly | monthly
    start_date: str
    end_date: Optional[str]
    next_run_date: str
    status: str  # active | paused | cancelled | ended


@dataclass
class PendingPayment:
    """A future-dated single payment; only the orchestrator posts these via mutation events."""
    pending_id: str
    account_id: str
    payee_id: str
    amount_minor: int
    memo: Optional[str]
    scheduled_for: str
    status: str  # pending | posted | cancelled
