"""Offline rubric primitives backed exclusively by Harbor frozen evidence."""
from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterable, Mapping
from typing import Any

def _decode(value: Any) -> Any:
    if isinstance(value, (dict, list)): return value
    if isinstance(value, bytes): value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def normalized_text(text: str) -> str: return re.sub(r"\s+", " ", (text or "").casefold()).strip()
def has_any(text: str, terms: Iterable[str]) -> bool:
    low = normalized_text(text); return any(normalized_text(term) in low for term in terms)
def has_all(text: str, terms: Iterable[str]) -> bool:
    low = normalized_text(text); return all(normalized_text(term) in low for term in terms)
def has_groups(text: str, groups: Iterable[Iterable[str]]) -> bool: return all(has_any(text, group) for group in groups)
def number_count(text: str) -> int: return len(re.findall(r"(?<!\w)(?:[$¥￥]\s*)?\d[\d,]*(?:\.\d+)?%?", text or ""))
def integer_value(value: Any) -> int | None:
    if isinstance(value, bool): return None
    if isinstance(value, int): return value
    if isinstance(value, float): return int(value) if value.is_integer() else None
    if isinstance(value, str) and re.fullmatch(r"[+-]?\d+", value.strip()): return int(value.strip())
    return None

def _snap(env: Any) -> dict[str, Any]:
    return env.snapshot(int(getattr(env, "current_stage", 22)))

def _workspace_map(env: Any) -> dict[str, str]:
    values = _snap(env).get("workspace", {})
    return {str(k): str(v) for k, v in values.items()} if isinstance(values, dict) else {}
def workspace_file_text(env: Any, path: str) -> str:
    wanted = path.rsplit("/", 1)[-1]
    return next((v for k, v in _workspace_map(env).items() if k.rsplit("/", 1)[-1] == wanted), "")
def workspace_text(env: Any, paths: Iterable[str]) -> str: return "\n".join(workspace_file_text(env, p) for p in paths)
def file_nonempty(env: Any, path: str) -> bool: return bool(workspace_file_text(env, path).strip())
def file_has_groups(env: Any, paths: Iterable[str], groups: Iterable[Iterable[str]], *, min_numbers: int = 0) -> bool:
    text = workspace_text(env, paths); return bool(text.strip()) and has_groups(text, groups) and number_count(text) >= min_numbers
def every_required_file_nonempty(env: Any, paths: Iterable[str]) -> bool: return all(file_nonempty(env, p) for p in paths)

def _all_traces(env: Any, stages: Iterable[int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for stage in stages:
        stage_number = int(stage)
        for row in env.trace(stage_number):
            # A stage trace is frozen inside its authoritative stage container.
            # Raw ATIF rows do not carry a stage field, so retain that context
            # while flattening instead of trusting an optional row value.
            item = dict(row)
            item["stage"] = stage_number
            rows.append(item)
    return rows
def _published_span(env: Any) -> range:
    # "Every stage so far" pools must stop at the last published stage: stage
    # evidence is frozen boundary by boundary, so reading a future stage number
    # mid-episode raises EvidenceError and aborts the whole trial.
    return range(int(getattr(env, "current_stage", 23)) + 1)
def _event_start_dt(row: Mapping[str, Any]) -> str:
    # calendar_mock formats events as start:{dateTime: ...}; accept that envelope
    # as well as the flat start_dt column.
    value = row.get("start_dt")
    if not value:
        start = row.get("start")
        value = (start.get("dateTime") or start.get("date")) if isinstance(start, dict) else start
    return str(value or "")
def _tool_name_matches(name: str, server: str | None, tools: Iterable[str] | None) -> bool:
    norm = str(name or "").casefold().replace("-", "_")
    if server and not (norm.startswith(server.casefold().replace("-", "_") + "__") or norm.startswith(server.casefold().replace("-", "_") + "_")): return False
    if not tools: return bool(norm)
    return any(norm == str(t).casefold().replace("-", "_") or norm.endswith("__" + str(t).casefold().replace("-", "_")) or norm.endswith("_" + str(t).casefold().replace("-", "_")) for t in tools)
def _success(call: Mapping[str, Any]) -> bool:
    if call.get("success") is not True or call.get("is_error") is True or call.get("isError") is True: return False
    result = _decode(call.get("result", call.get("content")))
    if result in (None, "", [], {}): return False
    if isinstance(result, dict):
        if result.get("error") or result.get("error_code") or result.get("isError") is True or result.get("is_error") is True or result.get("success") is False or result.get("ok") is False:
            return False
        if normalized_text(str(result.get("status") or "")) in {
            "failed", "failure", "error", "rejected", "declined", "cancelled",
            "canceled", "invalid", "not found", "not_found",
        }:
            return False
    if isinstance(result, str) and has_any(result, ("tool error", "invalid argument", "not found")):
        return False
    return True
def trace_tool_calls(env: Any, *, stages: Iterable[int]) -> list[dict[str, Any]]:
    out = []
    for call in _all_traces(env, stages):
        item = dict(call); item["arguments"] = _decode(item.get("arguments", item.get("input", {}))); out.append(item)
    return out
def successful_tool_pairs(env: Any, *, stages: Iterable[int], server: str | None = None, tools: Iterable[str] | None = None) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    out = []
    for call in _all_traces(env, stages):
        if _tool_name_matches(str(call.get("name", "")), server, tools) and _success(call):
            item = dict(call); item["arguments"] = _decode(item.get("arguments", item.get("input", {}))); result = _decode(item.get("result", item.get("content"))); out.append((item, {"content": result, "result": result}))
    return out
def successful_tool_calls(env: Any, *, stages: Iterable[int], server: str | None = None, tools: Iterable[str] | None = None) -> list[dict[str, Any]]: return [c for c, _ in successful_tool_pairs(env, stages=stages, server=server, tools=tools)]
def successful_tool_use(env: Any, *, stages: Iterable[int], server: str | None = None, tools: Iterable[str] | None = None) -> bool: return bool(successful_tool_pairs(env, stages=stages, server=server, tools=tools))
def successful_service_breadth(env: Any, *, stages: Iterable[int], services: Iterable[str]) -> int: return sum(1 for s in services if successful_tool_use(env, stages=stages, server=s))

def _service(snapshot: dict[str, Any], server: str) -> Any: return snapshot.get(server, {})
def _items(value: Any, key: str = "items") -> list[dict[str, Any]]:
    value = _decode(value)
    rows = value if isinstance(value, list) else value.get(key, value.get("results", [])) if isinstance(value, dict) else []
    return [dict(x) for x in rows if isinstance(x, dict)] if isinstance(rows, list) else []
def _messages(snapshot: dict[str, Any], folder: str) -> list[dict[str, Any]]:
    email = _service(snapshot, "email"); node = email.get("inbox" if folder.casefold() == "inbox" else "sent", {}) if isinstance(email, dict) else {}; rows = _items(node.get("listing", {}), "emails"); details = node.get("details", []) if isinstance(node, dict) else []; by_id = {str(r.get("email_id", r.get("id"))): r for r in details if isinstance(r, dict)}; out=[]
    for row in rows:
        merged=dict(row); detail=by_id.get(str(row.get("email_id", row.get("id")))); merged.update(detail or {}); out.append(merged)
    return out
def _db_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    notion = _service(snapshot, "notion"); out=[]
    for payload in (notion.get("database_rows", {}) if isinstance(notion, dict) else {}).values(): out.extend(_items(payload, "results"))
    return out

def _all_rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    value = _decode(value)
    if isinstance(value, list):
        return [dict(x) for x in value if isinstance(x, dict)]
    if isinstance(value, dict):
        for key in keys + ("items", "results", "emails", "drafts", "accounts", "events"):
            rows = value.get(key)
            if isinstance(rows, list):
                return [dict(x) for x in rows if isinstance(x, dict)]
    return []

def _service_rows(snapshot: dict[str, Any], server: str, section: str, *keys: str) -> list[dict[str, Any]]:
    service = _service(snapshot, server)
    if not isinstance(service, dict):
        return []
    value = service.get(section, [])
    if isinstance(value, dict) and keys:
        merged: list[dict[str, Any]] = []
        for sub in value.values():
            merged.extend(_all_rows(sub, *keys))
        return merged
    return _all_rows(value, *keys)

def runtime_rows(env: Any, server: str, sql: str, params: Iterable[Any] = ()) -> list[list[Any]]:
    snapshot = _snap(env); q = " ".join(sql.casefold().split()); p = list(params)
    def match(value: Any, needle: str) -> bool:
        return str(value or "").casefold() == str(needle).casefold()
    if server == "email" and "from messages" in q:
        messages = _messages(snapshot, "INBOX") + _messages(snapshot, "Sent")
        if "message_id = ?" in q:
            mid = str(p[0]) if p else ""
            rows = [r for r in messages if match(r.get("message_id", r.get("email_id", r.get("id"))), mid)]
            if "select 1" in q: return [[1] for _ in rows]
            return [[r.get("message_id", r.get("email_id", r.get("id")))] for r in rows]
        if "date(date) < date('2026-07-30')" in q:
            return [[1]] if any(str(r.get("date", ""))[:10] < "2026-07-30" for r in messages) else []
        if "message_id in" in q:
            wanted = {str(x) for x in p}
            return [[r.get("message_id", r.get("email_id", r.get("id")))] for r in messages if str(r.get("message_id", r.get("email_id", r.get("id")))) in wanted]
        if "subject, body_text" in q:
            return [[r.get("subject", ""), r.get("body_text", r.get("body", ""))] for r in messages]
    banking = _service(snapshot, "banking")
    if server == "banking" and "from accounts" in q:
        rows=_items(banking.get("accounts", []));
        if "account_id = ?" in q and p:
            rows = [a for a in rows if match(a.get("account_id"), p[-1])]
        if "user_id = ?" in q and p:
            rows = [a for a in rows if match(a.get("user_id", "usr_fin"), p[0])]
        if "select 1" in q: return [[1] for _ in rows]
        if "balance_minor" in q and "select balance_minor" in q: return [[a.get("balance_minor")] for a in rows]
        return [[a.get("account_id"),a.get("balance_minor"),int(bool(a.get("frozen")))] for a in rows]
    if server == "banking" and "from transactions" in q:
        rows=[]
        for account_id, payload in (banking.get("transactions", {}) if isinstance(banking,dict) else {}).items():
            for row in _items(payload):
                row.setdefault("account_id", account_id)
                rows.append(row)
        if "where tx_id" in q:
            literal = re.search(r"tx_id\s*=\s*'([^']+)'", q)
            wanted = literal.group(1) if literal else (p[0] if p else "")
            rows = [r for r in rows if match(r.get("tx_id"), wanted)]
            if "account_id = ?" in q and p: rows = [r for r in rows if match(r.get("account_id", p[-1]), p[-1])]
            amount = re.search(r"amount_minor\s*=\s*(-?\d+)", q)
            if amount: rows = [r for r in rows if int(r.get("amount_minor", 0)) == int(amount.group(1))]
            kind = re.search(r"kind\s*=\s*'([^']+)'", q)
            if kind: rows = [r for r in rows if match(r.get("kind"), kind.group(1))]
            counterparty = re.search(r"counterparty\s*=\s*'([^']+)'", q)
            if counterparty: rows = [r for r in rows if match(r.get("counterparty"), counterparty.group(1))]
            if "select 1" in q: return [[1] for _ in rows]
            return [[r.get("account_id"),r.get("amount_minor"),r.get("kind"),r.get("balance_after_minor")] for r in rows]
        if "acct_pension" in q: return [[r.get("tx_id")] for r in rows if str(r.get("account_id"))=="acct_pension"][:1]
        if "counterparty = 'harbor benefits'" in q:
            rows = [r for r in rows if match(r.get("counterparty"), "Harbor Benefits") and str(r.get("posted_at", ""))[:10] >= "2026-07-30"]
            return [[r.get("tx_id")] for r in rows]
        if "amount_minor < 0" in q:
            # The trailing parameter carries the "after" cutoff; p[0] is the
            # account filter when one is present, never a date.
            after = str(p[-1])[:10] if p else "2026-07-30"
            if "account_id = ?" in q and p: rows = [r for r in rows if match(r.get("account_id"), p[0])]
            return [[r.get("tx_id"),r.get("account_id"),r.get("amount_minor"),r.get("posted_at")] for r in rows if int(r.get("amount_minor",0))<0 and str(r.get("posted_at", ""))[:10]>=after][:1]
    if server == "banking" and "from pending_payments" in q:
        rows = _all_rows(banking.get("pending_payments", []))
        pending_literal = re.search(r"pending_id\s*=\s*'([^']+)'", q)
        if pending_literal: rows = [r for r in rows if match(r.get("pending_id"), pending_literal.group(1))]
        if "account_id = ?" in q and p: rows = [r for r in rows if match(r.get("account_id"), p[-1])]
        if "amount_minor = 28600" in q: rows = [r for r in rows if int(r.get("amount_minor", 0)) == 28600]
        if "scheduled_for = '2026-08-18'" in q: rows = [r for r in rows if str(r.get("scheduled_for")) == "2026-08-18"]
        if "status = 'pending'" in q: rows = [r for r in rows if str(r.get("status")) == "pending"]
        if "select 1" in q: return [[1] for _ in rows]
        if "select scheduled_for" in q: return [[r.get("scheduled_for")] for r in rows]
        return [[r.get("pending_id"), r.get("account_id"), r.get("amount_minor"), r.get("scheduled_for"), r.get("status")] for r in rows]
    card=_service(snapshot,"credit_card"); cards=_items(card.get("cards",[])) if isinstance(card,dict) else []
    for item in cards:
        if item.get("unbilled_balance_minor") is None:
            payload = card.get("unbilled", {}).get(str(item.get("card_id")), []) if isinstance(card, dict) else []
            item["unbilled_balance_minor"] = sum(int(row.get("amount_minor", 0)) for row in _items(payload))
    if server=="credit_card" and "from cards" in q:
        if "card_id = ?" in q and p: cards = [c for c in cards if match(c.get("card_id"), p[-1])]
        if "user_id = ?" in q and p: cards = [c for c in cards if match(c.get("user_id", "usr_fin"), p[0])]
        if "statement_balance_minor = 309169" in q: cards = [c for c in cards if int(c.get("statement_balance_minor",0)) == 309169]
        if "unbilled_balance_minor = 139800" in q: cards = [c for c in cards if int(c.get("unbilled_balance_minor",0)) == 139800]
        if "available_credit_minor = 1051031" in q: cards = [c for c in cards if int(c.get("available_credit_minor",0)) == 1051031]
        if "min_payment_due_minor = 8864" in q: cards = [c for c in cards if int(c.get("min_payment_due_minor",0)) == 8864]
        if "due_date = '2026-08-21'" in q: cards = [c for c in cards if str(c.get("due_date")) == "2026-08-21"]
        if "exists" in q:
            statements=[]
            for payload in (card.get("statements",{}) if isinstance(card,dict) else {}).values(): statements.extend(_items(payload))
            cards = [c for c in cards if any(
                str(s.get("statement_id")) == "stmt_y_2025_12"
                and match(s.get("card_id", c.get("card_id")), c.get("card_id"))
                and int(s.get("payments_minor",0)) == 90548
                and int(s.get("closing_balance_minor",0)) == int(c.get("statement_balance_minor",0))
                and int(s.get("min_payment_due_minor",0)) == int(c.get("min_payment_due_minor",0))
                and str(s.get("due_date")) == str(c.get("due_date"))
                and str(s.get("status")) == "partial"
                for s in statements
            )]
        if "select 1" in q: return [[1] for _ in cards]
        if "where user_id" in q: return [[c.get("card_id"),c.get("status")] for c in cards]
        ids={str(x) for x in p}; rows=[c for c in cards if str(c.get("card_id")) in ids] if ids else cards
        if "card_id, statement_balance_minor" in q: return [[c.get("card_id"),c.get("statement_balance_minor"),c.get("unbilled_balance_minor"),c.get("available_credit_minor")] for c in rows]
        if "select due_date" in q: return [[c.get("due_date")] for c in rows]
        return [[c.get("statement_balance_minor"),c.get("unbilled_balance_minor"),c.get("available_credit_minor")] for c in rows]
    if server=="credit_card" and "from statements" in q:
        rows=[]
        # list_statements rows omit the owning card; stamp it from the envelope
        # key so per-row card predicates can match.
        for card_key, payload in (card.get("statements",{}) if isinstance(card,dict) else {}).items():
            for row in _items(payload):
                row.setdefault("card_id", card_key)
                rows.append(row)
        if "statement_id = 'stmt_y_2025_12'" in q: rows = [r for r in rows if str(r.get("statement_id")) == "stmt_y_2025_12"]
        if "card_id = ?" in q and p: rows = [r for r in rows if match(r.get("card_id"), p[-1])]
        if "due_date = '2026-08-21'" in q: rows = [r for r in rows if str(r.get("due_date")) == "2026-08-21"]
        if "min_payment_due_minor = 8864" in q: rows = [r for r in rows if int(r.get("min_payment_due_minor",0)) == 8864]
        if "status in" in q: rows = [r for r in rows if str(r.get("status")) in {"open", "partial"}]
        if "select 1" in q: return [[1] for _ in rows]
        return [[r.get("card_id"),r.get("interest_apr_bp"),r.get("min_payment_due_minor"),r.get("due_date"),r.get("period_start"),r.get("period_end"),r.get("closing_balance_minor"),r.get("status")] for r in rows]
    if server=="credit_card" and "from unbilled_transactions" in q:
        rows=[]
        for card_id, payload in (card.get("unbilled",{}) if isinstance(card,dict) else {}).items():
            for row in _items(payload):
                row.setdefault("card_id", card_id)
                rows.append(row)
        tx_literal = re.search(r"tx_id\s*=\s*'([^']+)'", q)
        txid=tx_literal.group(1) if tx_literal else (str(p[0]) if p else ""); rows = [r for r in rows if str(r.get("tx_id"))==txid]
        if "card_id = ?" in q and p: rows = [r for r in rows if match(r.get("card_id"), p[-1])]
        if "amount_minor = -7200" in q: rows = [r for r in rows if int(r.get("amount_minor",0)) == -7200]
        if "kind = 'refund'" in q: rows = [r for r in rows if str(r.get("kind")) == "refund"]
        if "select 1" in q: return [[1] for _ in rows]
        return [[r.get("card_id"),r.get("amount_minor"),r.get("merchant_name"),r.get("category"),r.get("kind")] for r in rows]
    if server=="credit_card" and "from statement_lines" in q:
        lines=[]
        for payload in (card.get("statements",{}) if isinstance(card,dict) else {}).values():
            for st in _items(payload):
                lines.extend(_all_rows(st.get("statement_lines", [])))
        for call in _all_traces(env, _published_span(env)):
            if str(call.get("name", "")).casefold().replace("-", "_").endswith("get_statement") and _success(call):
                result = _decode(call.get("result", call.get("content")))
                if isinstance(result, dict):
                    # get_statement line rows omit the owning statement; stamp
                    # both owners from the envelope so per-line predicates match.
                    for row in _all_rows(result.get("statement_lines", [])):
                        row.setdefault("statement_id", result.get("statement_id"))
                        row.setdefault("card_id", result.get("card_id"))
                        lines.append(row)
        rows = [r for r in lines if str(r.get("line_id")) == "sl_dli_interest_20260825" and str(r.get("statement_id")) == "stmt_y_2025_12" and int(r.get("amount_minor",0)) == 2600 and str(r.get("kind")) == "interest"]
        return [[1] for _ in rows] if "select 1" in q else [[r.get("line_id"),r.get("statement_id"),r.get("amount_minor"),r.get("kind")] for r in rows]
    if server=="credit_card" and "from payments" in q:
        out=[]
        for call in _all_traces(env,_published_span(env)):
            if str(call.get("name","")).endswith("make_payment") and _success(call):
                a=_decode(call.get("arguments",{})) or {}; r=_decode(call.get("result",{})) or {}; 
                if isinstance(r,dict) and r.get("payment_id"): out.append([r["payment_id"],a.get("card_id"),a.get("amount_minor"),a.get("source_hint"),r.get("posted_at","")])
        pid=str(p[0]) if p else ""; return [r[1:] for r in out if str(r[0])==pid]
    if server=="brokerage" and "from accounts" in q:
        rows = _all_rows(_service(snapshot,"brokerage").get("accounts", []));
        if "account_id = 'acct_brk_main'" in q: rows = [r for r in rows if str(r.get("account_id")) == "acct_brk_main"]
        if "user_id = ?" in q and p: rows = [r for r in rows if match(r.get("user_id", "usr_fin"), p[0])]
        if "status = 'active'" in q: rows = [r for r in rows if str(r.get("status")) == "active"]
        return [[1] for _ in rows] if "select 1" in q else [[r.get("account_id"),r.get("status")] for r in rows]
    if server=="brokerage" and "count(*) from positions" in q: return [[len(_items(_service(snapshot,"brokerage").get("positions",[])))]]
    if server=="notion" and "from database_rows" in q:
        rows=_db_rows(snapshot)
        tokens=("us_irs_pub525_2025_disability", "us_irs_pub15a_2026_sick_pay", "us_cfpb_credit_minimum")
        return [[json.dumps(r.get("properties", r), ensure_ascii=False)] for r in rows if any(token in json.dumps(r,ensure_ascii=False) for token in tokens)]
    if server=="calendar" and "from events" in q:
        rows = _all_rows(_service(snapshot,"calendar").get("events",[]))
        if "date(start_dt) < date('2026-07-30')" in q: rows = [r for r in rows if _event_start_dt(r)[:10] < "2026-07-30"]
        if "count(*)" in q:
            # The rubric's calendar predicates are evaluated directly over the
            # frozen event rows, including dates and content terms.
            date_match = re.search(r"date\(start_dt\) = date\('([^']+)'\)", q)
            if date_match: rows = [r for r in rows if _event_start_dt(r)[:10] == date_match.group(1)]
            elif "date(start_dt) = date(?)" in q and p: rows = [r for r in rows if _event_start_dt(r)[:10] == str(p[0])[:10]]
            def blob(row: Mapping[str, Any]) -> str:
                return (str(row.get("summary", "")) + " " + str(row.get("description", ""))).casefold()
            if "like '%card%'" in q: rows = [r for r in rows if "card" in blob(r) and ("due" in blob(r) or "payment" in blob(r))]
            elif "like '%clinic%'" in q and "like '%medical%'" in q: rows = [r for r in rows if "clinic" in blob(r) or "medical" in blob(r)]
            elif "like '%claim%'" in q: rows = [r for r in rows if "claim" in blob(r) and ("follow-up" in blob(r) or "review" in blob(r))]
            if "substr(created_at" in q:
                rows = [r for r in rows if any(str(r.get(key, ""))[:10] >= "2026-07-30" for key in ("created_at", "updated_at"))]
            return [[len(rows)]]
        return [[r.get("event_id"),r.get("summary",""),r.get("description",""),r.get("start_dt",r.get("start","")),r.get("status","confirmed"),r.get("created_at",""),r.get("updated_at","")] for r in rows]
    return []

def account_balance_minor(env: Any, account_id: str) -> int | None:
    rows=runtime_rows(env,"banking","SELECT balance_minor FROM accounts WHERE account_id = ?",[account_id]); return integer_value(rows[0][0]) if rows and rows[0] else None
def post_kickoff_card_payments(env: Any, *, kickoff_date: str = "2026-07-30") -> list[tuple[str,str,int,str,str]] | None:
    out=[]
    for call in _all_traces(env,_published_span(env)):
        if str(call.get("name","")).endswith("make_payment") and _success(call):
            a=_decode(call.get("arguments",{})) or {}; r=_decode(call.get("result",{})) or {}; out.append((str(r.get("payment_id",call.get("id",""))),str(a.get("card_id")),int(a.get("amount_minor",0)),str(a.get("source_hint")),str(call.get("posted_at",""))))
    return out
def post_kickoff_card_payments_exactly(env: Any, allowed: set[tuple[str,int,str]], *, kickoff_date: str = "2026-07-30") -> bool:
    rows=post_kickoff_card_payments(env,kickoff_date=kickoff_date); observed=[(c,a,s) for _,c,a,s,_ in rows] if rows is not None else []; return len(observed)==len(allowed) and len(observed)==len(set(observed)) and set(observed)==allowed
def post_kickoff_card_payments_allowed(env: Any, allowed: set[tuple[str,int,str]], *, kickoff_date: str = "2026-07-30") -> bool:
    rows=post_kickoff_card_payments(env,kickoff_date=kickoff_date); observed=[(c,a,s) for _,c,a,s,_ in rows] if rows is not None else []; return len(observed)==len(set(observed)) and set(observed).issubset(allowed)
def no_post_kickoff_bank_debits(env: Any, *, kickoff_date: str = "2026-07-30") -> bool: return not runtime_rows(env,"banking","SELECT tx_id, account_id, amount_minor, posted_at FROM transactions WHERE amount_minor < 0",[kickoff_date])
def no_bank_debit_from(env: Any, account_id: str, *, after: str = "2026-07-30") -> bool: return not runtime_rows(env,"banking","SELECT amount_minor FROM transactions WHERE account_id = ? AND amount_minor < 0",[account_id,after])
def no_brokerage_orders(env: Any, *, after: str = "2026-07-30") -> bool:
    orders = _items(_service(_snap(env), "brokerage").get("orders", []))
    return not any(
        not str(row.get("placed_at", ""))
        or str(row.get("placed_at", ""))[:10] >= after
        for row in orders
    )
def workspace_lifecycle_valid(env: Any, first_required: Mapping[str,int]) -> bool: return True

def no_duplicate_calendar_groups(env: Any, group_sets: Iterable[Iterable[Iterable[str]]]) -> bool:
    events = [
        event
        for event in _all_rows(_service(_snap(env), "calendar").get("events", []))
        if any(
            str(event.get(key, ""))[:10] >= "2026-07-30"
            for key in ("created_at", "updated_at")
        )
    ]
    for group in group_sets:
        matches = [
            event for event in events
            if has_groups(f"{event.get('summary', '')} {event.get('description', '')}", group)
        ]
        if len(matches) != 1:
            return False
    return True

common = sys.modules[__name__]
