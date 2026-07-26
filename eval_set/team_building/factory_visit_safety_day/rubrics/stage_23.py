from __future__ import annotations
from ._helpers import *


def s23_invoice_reconciled(env) -> bool:
    calls = used_tool_with_value(env, 23, "banking", "list_transactions", ["acct_factory_main"]) and used_tool(env, 23, "email", "save_draft")
    backend = all(has_transaction(env, tx_id) for tx_id in ("tx_013_bus_invoice", "tx_013_lunch_invoice", "tx_013_insure_invoice"))
    drafted = draft_has(
        env,
        subject_groups=[["发票", "结算"]],
        recipient_terms=["finance"],
        body_groups=[["包车"], ["餐饮"], ["保险"], ["发票"], ["押金"], ["未付款"]],
    )
    return calls and backend and drafted and workspace_file_has(env, "BUDGET_LEDGER.csv", [["bus", "包车"], ["lunch", "餐饮"], ["insurance", "保险"], ["invoice", "发票"]]) and no_payment_to(env, ["嘉兴智造工厂参访中心", "嘉兴智造临时账户"])


CHECKS = [("s23_invoice_reconciled", s23_invoice_reconciled, 2.0)]
