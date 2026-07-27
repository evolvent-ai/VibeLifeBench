"""Inter-account transfers (same user only)."""
import logging
import sqlite3
from typing import Optional

from ..utils.dates import today_utc
from ..utils.exceptions import BadAmountError, CrossUserTransferError
from ._posting import fetch_account, post_transaction

logger = logging.getLogger(__name__)


class TransferService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def transfer(
        self,
        from_account_id: str,
        to_account_id: str,
        amount_minor: int,
        memo: Optional[str] = None,
    ) -> dict:
        if from_account_id == to_account_id:
            raise BadAmountError("from_account_id and to_account_id must differ")
        if amount_minor is None or int(amount_minor) <= 0:
            raise BadAmountError("amount_minor must be a positive integer")
        amt = int(amount_minor)

        # Both accounts exist; same user (external use add_payee/pay_payee).
        from_acct = fetch_account(self.conn, from_account_id)
        to_acct = fetch_account(self.conn, to_account_id)
        if from_acct["user_id"] != to_acct["user_id"]:
            raise CrossUserTransferError(
                "transfers must be between accounts of the same user; "
                "use add_payee + pay_payee for external recipients"
            )

        sim_date = today_utc()
        from_name = from_acct["name"]
        to_name = to_acct["name"]

        self.conn.execute("SAVEPOINT xfer;")
        try:
            out = post_transaction(
                self.conn,
                account_id=from_account_id,
                amount_minor=-amt,
                kind="transfer_out",
                sim_date=sim_date,
                counterparty=to_name,
                memo=memo,
            )
            in_ = post_transaction(
                self.conn,
                account_id=to_account_id,
                amount_minor=amt,
                kind="transfer_in",
                sim_date=sim_date,
                counterparty=from_name,
                memo=memo,
            )
            self.conn.execute("RELEASE SAVEPOINT xfer;")
        except Exception:
            self.conn.execute("ROLLBACK TO SAVEPOINT xfer;")
            self.conn.execute("RELEASE SAVEPOINT xfer;")
            raise

        return {
            "tx_id": out["tx_id"],
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "amount_minor": amt,
            "from_new_balance_minor": out["balance_after_minor"],
            "to_new_balance_minor": in_["balance_after_minor"],
            "posted_at": out["posted_at"],
        }
