import sqlite3
from typing import List

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    BadRedemptionError,
    CardNotFoundError,
    InsufficientPointsError,
)
from ..utils.ids import ledger_id


REDEMPTION_CATALOG = {
    "STMT_CREDIT_50":  {"points": 5000,  "value_minor": 5000,  "label": "¥50 statement credit"},
    "STMT_CREDIT_200": {"points": 20000, "value_minor": 20000, "label": "¥200 statement credit"},
    "MILES_AIR_CHINA": {"points": 10000, "value_minor": 0,     "label": "Convert 10000 points to Air China miles"},
    "GIFT_JD_100":     {"points": 12000, "value_minor": 10000, "label": "¥100 JD.com e-gift card"},
}


def _redemption_options() -> List[dict]:
    return [
        {"redemption_code": code, **meta}
        for code, meta in REDEMPTION_CATALOG.items()
    ]


class RewardsService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _assert_card(self, card_id: str) -> None:
        row = self.conn.execute(
            "SELECT 1 FROM cards WHERE card_id = ?", (card_id,)
        ).fetchone()
        if not row:
            raise CardNotFoundError(f"card not found: {card_id}")

    def _balance_row(self, card_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM rewards_balances WHERE card_id = ?", (card_id,)
        ).fetchone()
        if row is None:
            # Initialise an empty balance lazily.
            self.conn.execute(
                """
                INSERT INTO rewards_balances (card_id, points_balance, ytd_earned,
                                              lifetime_earned, updated_at)
                VALUES (?, 0, 0, 0, ?)
                """,
                (card_id, now_iso_z()),
            )
            row = self.conn.execute(
                "SELECT * FROM rewards_balances WHERE card_id = ?", (card_id,)
            ).fetchone()
        return row

    def get_rewards(self, card_id: str) -> dict:
        self._assert_card(card_id)
        bal = self._balance_row(card_id)
        recent = self.conn.execute(
            """
            SELECT posted_at, kind, delta, balance_after, note
            FROM rewards_ledger
            WHERE card_id = ?
            ORDER BY posted_at DESC, ledger_id DESC
            LIMIT 10
            """,
            (card_id,),
        ).fetchall()
        return {
            "card_id": card_id,
            "points_balance": int(bal["points_balance"]),
            "ytd_earned": int(bal["ytd_earned"]),
            "lifetime_earned": int(bal["lifetime_earned"]),
            "updated_at": bal["updated_at"],
            "recent_earnings": [
                {
                    "posted_at": r["posted_at"],
                    "kind": r["kind"],
                    "delta": int(r["delta"]),
                    "balance_after": int(r["balance_after"]),
                    "note": r["note"],
                }
                for r in recent
            ],
            "redemption_options": _redemption_options(),
        }

    def redeem_rewards(self, card_id: str, redemption_code: str) -> dict:
        self._assert_card(card_id)
        code = (redemption_code or "").strip().upper()
        meta = REDEMPTION_CATALOG.get(code)
        if not meta:
            raise BadRedemptionError(f"unknown redemption_code: {redemption_code}")

        bal = self._balance_row(card_id)
        cost = int(meta["points"])
        current = int(bal["points_balance"])
        if current < cost:
            raise InsufficientPointsError(
                f"redemption requires {cost} points; balance is {current}"
            )

        new_balance = current - cost
        now = now_iso_z()
        self.conn.execute(
            """
            UPDATE rewards_balances
            SET points_balance = ?, updated_at = ?
            WHERE card_id = ?
            """,
            (new_balance, now, card_id),
        )
        seq = next_counter(self.conn, "ledger_seq")
        lid = ledger_id(seq)
        self.conn.execute(
            """
            INSERT INTO rewards_ledger (ledger_id, card_id, posted_at, kind, delta,
                                        balance_after, note)
            VALUES (?, ?, ?, 'redeem', ?, ?, ?)
            """,
            (lid, card_id, now, -cost, new_balance, f"redeem:{code}"),
        )

        return {
            "card_id": card_id,
            "redemption_code": code,
            "points_spent": cost,
            "points_balance": new_balance,
            "value_minor": int(meta["value_minor"]),
            "label": meta["label"],
            "ledger_id": lid,
        }
