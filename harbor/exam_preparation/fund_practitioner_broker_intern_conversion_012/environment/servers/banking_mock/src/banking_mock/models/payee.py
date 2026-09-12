from dataclasses import dataclass


@dataclass
class Payee:
    """An external payment recipient saved by a user."""
    payee_id: str
    user_id: str
    name: str
    account_no: str           # full account number, stored
    account_no_masked: str    # masked form returned over MCP
    bank_name: str
    added_at: str
