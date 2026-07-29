from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest
from mcp.server.fastmcp import FastMCP

SERVER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER_ROOT / "src"))

from banking_mock.backends.db import init_schema  # noqa: E402
from banking_mock.services.payee_service import PayeeService  # noqa: E402
from banking_mock.tools.payee_tools import register_payee_tools  # noqa: E402
from banking_mock.utils.exceptions import BadArgError  # noqa: E402


def _connection() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    init_schema(conn)
    conn.executescript(
        """
        INSERT INTO accounts(account_id,user_id,type,name,balance_minor,currency,opened_at,frozen) VALUES
          ('acct_u1','user_1','checking','User 1 checking',100000,'CNY','2026-01-01T00:00:00Z',0),
          ('acct_u2','user_2','checking','User 2 checking',100000,'CNY','2026-01-01T00:00:00Z',0);
        INSERT INTO payees(payee_id,user_id,name,account_no,account_no_masked,bank_name,added_at) VALUES
          ('payee_u1','user_1','Hospital','11112222','****2222','Test Bank','2026-01-01T00:00:00Z'),
          ('payee_u2','user_2','Landlord','33334444','****4444','Test Bank','2026-01-01T00:00:00Z');
        INSERT INTO pending_payments(pending_id,account_id,payee_id,amount_minor,memo,scheduled_for,status) VALUES
          ('pending_late','acct_u1','payee_u1',2000,'later','2026-08-20','pending'),
          ('pending_early','acct_u1','payee_u1',1000,'earlier','2026-08-10','pending'),
          ('pending_posted','acct_u1','payee_u1',3000,'posted','2026-08-05','posted'),
          ('pending_other_user','acct_u2','payee_u2',4000,'private','2026-08-01','pending');
        """
    )
    return conn


def test_list_pending_payments_is_user_scoped_filterable_and_ordered() -> None:
    conn = _connection()
    try:
        service = PayeeService(conn)

        rows = service.list_pending_payments("user_1", status_filter="pending")

        assert [row["pending_id"] for row in rows] == ["pending_early", "pending_late"]
        assert all(row["account_id"] == "acct_u1" for row in rows)
        assert rows[0]["payee_name"] == "Hospital"
        assert service.list_pending_payments("user_1", account_id="acct_u2") == []
        assert [row["pending_id"] for row in service.list_pending_payments("user_1", limit=1)] == [
            "pending_posted"
        ]
        with pytest.raises(BadArgError):
            service.list_pending_payments("user_1", status_filter="unknown")
    finally:
        conn.close()


def test_pending_payment_tool_is_exposed_with_optional_filters() -> None:
    conn = _connection()
    try:
        mcp = FastMCP("banking-pending-payment-contract")
        register_payee_tools(mcp, PayeeService(conn))
        tool = next(
            tool for tool in mcp._tool_manager.list_tools() if tool.name == "list_pending_payments"
        )

        assert set(tool.parameters["required"]) == {"user_id"}
        assert {"account_id", "status_filter", "limit"}.issubset(tool.parameters["properties"])
    finally:
        conn.close()
