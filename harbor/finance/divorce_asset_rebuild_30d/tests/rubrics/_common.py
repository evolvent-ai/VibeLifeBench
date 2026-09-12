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

def _snap_at(env: Any, stage: int) -> dict[str, Any]:
    return env.snapshot(int(stage))

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
        for call in env.trace(int(stage)):
            item = dict(call)
            item.setdefault("stage", int(stage))
            rows.append(item)
    return rows
def _tool_name_matches(name: str, server: str | None, tools: Iterable[str] | None) -> bool:
    norm = str(name or "").casefold().replace("-", "_")
    if server and not (norm.startswith(server.casefold().replace("-", "_") + "__") or norm.startswith(server.casefold().replace("-", "_") + "_")): return False
    if not tools: return bool(norm)
    return any(norm == str(t).casefold().replace("-", "_") or norm.endswith("__" + str(t).casefold().replace("-", "_")) or norm.endswith("_" + str(t).casefold().replace("-", "_")) for t in tools)
def _success(call: Mapping[str, Any]) -> bool:
    if call.get("success") is not True or call.get("is_error") is True or call.get("isError") is True: return False
    result = result_payload(call)
    if result in (None, "", [], {}): return False
    return not (isinstance(result, dict) and (result.get("error") or result.get("isError") is True or result.get("is_error") is True or result.get("success") is False or result.get("ok") is False))

def result_payload(call: Mapping[str, Any]) -> Any:
    value = _decode(call.get("result", call.get("content")))
    for _ in range(4):
        if isinstance(value, dict):
            structured = value.get("structuredContent", value.get("structured_content"))
            if isinstance(structured, dict) and "result" in structured:
                value = _decode(structured["result"])
                continue
            content = value.get("content")
            if isinstance(content, list):
                texts = [row.get("text") for row in content if isinstance(row, dict) and row.get("type") == "text"]
                if texts:
                    value = _decode("\n".join(str(text) for text in texts))
                    continue
        break
    return value
def trace_tool_calls(env: Any, *, stages: Iterable[int]) -> list[dict[str, Any]]:
    out = []
    for call in _all_traces(env, stages):
        item = dict(call); item["arguments"] = _decode(item.get("arguments", item.get("input", {}))); out.append(item)
    return out
def successful_tool_pairs(env: Any, *, stages: Iterable[int], server: str | None = None, tools: Iterable[str] | None = None) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    out = []
    for call in _all_traces(env, stages):
        if _tool_name_matches(str(call.get("name", "")), server, tools) and _success(call):
            item = dict(call); item["arguments"] = _decode(item.get("arguments", item.get("input", {}))); result = result_payload(item); out.append((item, {"content": result, "result": result}))
    return out
def successful_tool_calls(env: Any, *, stages: Iterable[int], server: str | None = None, tools: Iterable[str] | None = None) -> list[dict[str, Any]]: return [c for c, _ in successful_tool_pairs(env, stages=stages, server=server, tools=tools)]
def successful_tool_use(env: Any, *, stages: Iterable[int], server: str | None = None, tools: Iterable[str] | None = None) -> bool: return bool(successful_tool_pairs(env, stages=stages, server=server, tools=tools))
def successful_service_breadth(env: Any, *, stages: Iterable[int], services: Iterable[str]) -> int: return sum(1 for s in services if successful_tool_use(env, stages=stages, server=s))

def _service(snapshot: dict[str, Any], server: str) -> Any: return snapshot.get(server, {})
def _items(value: Any, key: str = "items") -> list[dict[str, Any]]:
    value = _decode(value)
    rows = value if isinstance(value, list) else value.get(key, value.get("results", [])) if isinstance(value, dict) else []
    return [dict(x) for x in rows if isinstance(x, dict)] if isinstance(rows, list) else []
def _messages(env: Any, folder: str) -> list[dict[str, Any]]:
    snapshot = _snap(env)
    email = _service(snapshot, "email"); node = email.get("inbox" if folder.casefold() == "inbox" else "sent", {}) if isinstance(email, dict) else {}; rows = _items(node.get("listing", {}), "emails"); details = node.get("details", []) if isinstance(node, dict) else []; by_id = {str(r.get("email_id", r.get("id"))): r for r in details if isinstance(r, dict)}; out=[]
    if folder.casefold() == "inbox":
        for call in _all_traces(env, range(int(getattr(env, "current_stage", 22)) + 1)):
            if not _tool_name_matches(str(call.get("name", "")), "email", ("read_email",)) or not _success(call):
                continue
            detail = result_payload(call)
            if isinstance(detail, dict) and str(detail.get("folder", "INBOX")).casefold() == "inbox":
                email_id = str(detail.get("email_id", detail.get("id", "")))
                if email_id:
                    by_id[email_id] = detail
    for row in rows:
        merged=dict(row); detail=by_id.get(str(row.get("email_id", row.get("id")))); merged.update(detail or {}); out.append(merged)
    return out

def _transaction_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    banking = _service(snapshot, "banking"); out=[]
    for account_id, payload in (banking.get("transactions", {}) if isinstance(banking, dict) else {}).items():
        for row in _items(payload):
            row.setdefault("account_id", account_id); out.append(row)
    return out

def _card_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    card = _service(snapshot, "credit_card"); rows=_items(card.get("cards", [])) if isinstance(card, dict) else []
    unbilled = card.get("unbilled", {}) if isinstance(card, dict) else {}
    for row in rows:
        card_id = str(row.get("card_id", ""))
        if row.get("unbilled_balance_minor") is None and isinstance(unbilled, dict):
            row["unbilled_balance_minor"] = sum(int(item.get("amount_minor", 0)) for item in _items(unbilled.get(card_id, [])))
    return rows
def _db_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    notion = _service(snapshot, "notion"); out=[]
    for payload in (notion.get("database_rows", {}) if isinstance(notion, dict) else {}).values(): out.extend(_items(payload, "results"))
    return out

def runtime_rows(env: Any, server: str, sql: str, params: Iterable[Any] = ()) -> list[list[Any]]:
    snapshot = _snap(env); q = " ".join(sql.casefold().split()); p = list(params)
    if server == "email" and "from messages" in q and "subject, body_text" in q:
        mid = str(p[0]) if p else ""; return [[r.get("subject", ""), r.get("body_text", r.get("body", ""))] for r in _messages(env, "INBOX") + _messages(env, "Sent") if str(r.get("message_id", r.get("email_id", r.get("id", "")))) == mid]
    if server == "email" and "message_id from messages" in q:
        wanted={str(x) for x in p}; return [[r.get("message_id", r.get("email_id", r.get("id", "")))] for r in _messages(env,"INBOX") + _messages(env,"Sent") if str(r.get("message_id", r.get("email_id", r.get("id", "")))) in wanted]
    banking = _service(snapshot, "banking")
    if server == "banking" and "from accounts" in q:
        rows=_items(banking.get("accounts", []));
        if "where user_id" in q: return [[a.get("account_id"),a.get("balance_minor"),int(bool(a.get("frozen")))] for a in rows]
        return [[a.get("balance_minor")] for a in rows if str(a.get("account_id")) == str(p[0] if p else "")]
    if server == "banking" and "from transactions" in q:
        rows=_transaction_rows(snapshot)
        if "where tx_id" in q: return [[r.get("account_id"),r.get("amount_minor"),r.get("kind"),r.get("balance_after_minor")] for r in rows if str(r.get("tx_id"))==str(p[0] if p else "")]
        if "account_id = ?" in q:
            account_id=str(p[0]) if p else ""; rows=[r for r in rows if str(r.get("account_id")) == account_id]
        if "posted_at >= ?" in q:
            after=str(p[1] if "account_id = ?" in q and len(p)>1 else p[0] if p else "")[:10]; rows=[r for r in rows if str(r.get("posted_at", ""))[:10] >= after]
        if "amount_minor < 0" in q:
            if "posted_at >= ?" not in q:
                after=str(p[1] if "account_id = ?" in q and len(p)>1 else p[0] if p else "2026-07-30")[:10]; rows=[r for r in rows if str(r.get("posted_at", ""))[:10] >= after]
            rows=[r for r in rows if int(r.get("amount_minor",0)) < 0]
        return [[r.get("tx_id"),r.get("account_id"),r.get("amount_minor"),r.get("posted_at")] for r in rows[:1]]
    card=_service(snapshot,"credit_card"); cards=_card_rows(snapshot)
    if server=="credit_card" and "from cards" in q and "join statements" not in q:
        if "where user_id" in q: return [[c.get("card_id"),c.get("status")] for c in cards]
        ids={str(x) for x in p}; rows=[c for c in cards if str(c.get("card_id")) in ids] if ids else cards
        if "card_id, statement_balance_minor" in q: return [[c.get("card_id"),c.get("statement_balance_minor"),c.get("unbilled_balance_minor"),c.get("available_credit_minor")] for c in rows]
        return [[c.get("statement_balance_minor"),c.get("unbilled_balance_minor"),c.get("available_credit_minor")] for c in rows]
    if server=="credit_card" and ("from statements" in q or "join statements" in q):
        rows=[]
        cards_by_id={str(row.get("card_id")):row for row in cards}
        for card_id,payload in (card.get("statements",{}) if isinstance(card,dict) else {}).items():
            for row in _items(payload):
                row.setdefault("card_id",card_id); rows.append(row)
        return [[r.get("card_id"),cards_by_id.get(str(r.get("card_id")),{}).get("interest_apr_bp"),cards_by_id.get(str(r.get("card_id")),{}).get("min_payment_due_minor",r.get("min_payment_due_minor")),cards_by_id.get(str(r.get("card_id")),{}).get("due_date",r.get("due_date")),r.get("period_start"),r.get("period_end"),r.get("closing_balance_minor"),r.get("status")] for r in rows if str(r.get("period_end"))=="2026-07-28"]
    if server=="credit_card" and "from unbilled_transactions" in q:
        rows=[]
        for card_id,payload in (card.get("unbilled",{}) if isinstance(card,dict) else {}).items():
            for row in _items(payload): row.setdefault("card_id",card_id); rows.append(row)
        txid=str(p[0]) if p else ""; return [[r.get("card_id"),r.get("amount_minor"),r.get("merchant_name"),r.get("category"),r.get("kind")] for r in rows if str(r.get("tx_id"))==txid]
    if server=="brokerage" and "from accounts" in q: return [[r.get("account_id"),r.get("status")] for r in _items(_service(snapshot,"brokerage").get("accounts",[]))]
    if server=="brokerage" and "count(*) from positions" in q: return [[len(_items(_service(snapshot,"brokerage").get("positions",[])))]]
    if server=="notion" and "from database_rows" in q:
        rows=_db_rows(snapshot); return [[r.get("id",r.get("row_id",""))] for r in rows if "public_rate_anchor" in json.dumps(r,ensure_ascii=False) and "2026-07-20" in json.dumps(r,ensure_ascii=False) and "3.0%" in json.dumps(r,ensure_ascii=False) and "3.5%" in json.dumps(r,ensure_ascii=False) and "not a personal mortgage execution rate" in json.dumps(r,ensure_ascii=False).lower()]
    if server=="calendar" and "from events" in q:
        def start_value(row: dict[str, Any]) -> Any:
            value=row.get("start_dt",row.get("start","")); return value.get("dateTime",value.get("date","")) if isinstance(value,dict) else value
        rows=_items(_service(snapshot,"calendar").get("events",[]))
        if "start_dt >= ?" in q:
            after=str(p[0]) if p else ""; rows=[r for r in rows if str(start_value(r)) >= after]
        return [[r.get("event_id"),r.get("summary",""),r.get("description",""),start_value(r),r.get("status","confirmed"),r.get("created_at",""),r.get("updated_at","")] for r in rows]
    return []

def account_balance_minor(env: Any, account_id: str) -> int | None:
    rows=runtime_rows(env,"banking","SELECT balance_minor FROM accounts WHERE account_id = ?",[account_id]); return integer_value(rows[0][0]) if rows and rows[0] else None
def post_kickoff_card_payments(env: Any, *, kickoff_date: str = "2026-07-30") -> list[tuple[str,str,int,str,str]] | None:
    out=[]
    for call in _all_traces(env,range(int(getattr(env,"current_stage",22))+1)):
        if str(call.get("name","")).endswith("make_payment") and _success(call):
            a=_decode(call.get("arguments",{})) or {}; r=result_payload(call) or {}
            if isinstance(a,dict) and isinstance(r,dict): out.append((str(r.get("payment_id",call.get("id",""))),str(a.get("card_id")),int(a.get("amount_minor",0)),str(a.get("source_hint")),str(call.get("posted_at",""))))
    return out
def post_kickoff_card_payments_exactly(env: Any, allowed: set[tuple[str,int,str]], *, kickoff_date: str = "2026-07-30") -> bool:
    rows=post_kickoff_card_payments(env,kickoff_date=kickoff_date); observed=[(c,a,s) for _,c,a,s,_ in rows] if rows is not None else []; return len(observed)==len(allowed) and len(observed)==len(set(observed)) and set(observed)==allowed
def post_kickoff_card_payments_allowed(env: Any, allowed: set[tuple[str,int,str]], *, kickoff_date: str = "2026-07-30") -> bool:
    rows=post_kickoff_card_payments(env,kickoff_date=kickoff_date); observed=[(c,a,s) for _,c,a,s,_ in rows] if rows is not None else []; return len(observed)==len(set(observed)) and set(observed).issubset(allowed)
def no_post_kickoff_bank_debits(env: Any, *, kickoff_date: str = "2026-07-30") -> bool: return not runtime_rows(env,"banking","SELECT tx_id, account_id, amount_minor, posted_at FROM transactions WHERE amount_minor < 0",[kickoff_date])
def no_bank_debit_from(env: Any, account_id: str, *, after: str = "2026-07-30") -> bool: return not runtime_rows(env,"banking","SELECT amount_minor FROM transactions WHERE account_id = ? AND amount_minor < 0",[account_id,after])
def no_brokerage_orders(env: Any, *, after: str = "2026-07-30") -> bool: return not _items(_service(_snap(env),"brokerage").get("orders",[]))
def workspace_lifecycle_valid(env: Any, first_required: Mapping[str,int], update_stages: Mapping[str,Iterable[int]]) -> bool:
    current=int(getattr(env,"current_stage",22)); published=set(env.published_stages()) if hasattr(env,"published_stages") else set(range(current+1))
    if not set(range(current+1)).issubset(published): return False
    stages=[stage for stage in range(current+1) if stage in published]
    if not stages: return False
    for name, first in first_required.items():
        updates={int(stage) for stage in update_stages.get(name, ()) if int(stage) <= current}
        previous=""
        for stage in stages:
            workspace=_snap_at(env,stage).get("workspace",{}); text=""
            if isinstance(workspace,dict):
                text=next((str(v) for k,v in workspace.items() if str(k).rsplit("/",1)[-1]==name),"")
            text=text.strip()
            if stage < int(first) and text: return False
            if stage >= int(first) and not text: return False
            if stage in updates and stage > int(first) and text == previous: return False
            previous=text
    return True

common = sys.modules[__name__]
