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
    return env.snapshot(int(getattr(env, "current_stage", 23)))

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
    # Trace evidence is valid only when the collector explicitly recorded a
    # successful call. A result without success=True is incomplete evidence.
    if call.get("success") is not True or call.get("is_error") is True or call.get("isError") is True: return False
    result = _decode(call.get("result", call.get("content")))
    if result in (None, "", [], {}): return False
    return not (isinstance(result, dict) and (result.get("error") or result.get("isError") is True or result.get("is_error") is True or result.get("success") is False or result.get("ok") is False))
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
    if isinstance(value, list):
        rows = value
    elif isinstance(value, dict):
        rows = value.get(key)
        if not isinstance(rows, list):
            for candidate in ("items", "results", "emails", "events", "cards", "statements", "transactions", "unbilled"):
                if isinstance(value.get(candidate), list):
                    rows = value[candidate]
                    break
        if not isinstance(rows, list):
            rows = []
    else:
        rows = []
    return [dict(x) for x in rows if isinstance(x, dict)] if isinstance(rows, list) else []
def _messages(snapshot: dict[str, Any], folder: str) -> list[dict[str, Any]]:
    email = _service(snapshot, "email"); node = email.get("inbox" if folder.casefold() == "inbox" else "sent", {}) if isinstance(email, dict) else {}; rows = _items(node.get("listing", {}), "emails"); details = node.get("details", []) if isinstance(node, dict) else []; by_id = {str(r.get("email_id", r.get("id"))): r for r in details if isinstance(r, dict)}; out=[]
    for row in rows:
        merged=dict(row); detail=by_id.get(str(row.get("email_id", row.get("id")))); merged.update(detail or {}); out.append(merged)
    return out

def _walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_dicts(child)

def _trace_result_rows(env: Any, stages: Iterable[int]) -> Iterable[dict[str, Any]]:
    for call in _all_traces(env, stages):
        if _success(call):
            yield from _walk_dicts(_decode(call.get("result", call.get("content"))))

def card_state(env: Any, card_id: str) -> dict[str, Any] | None:
    card = _service(_snap(env), "credit_card")
    rows = _items(card.get("cards", []))
    if not rows and isinstance(card.get("card_details"), dict):
        rows = [dict(v, card_id=k) for k, v in card["card_details"].items() if isinstance(v, dict)]
    return next((row for row in rows if str(row.get("card_id")) == str(card_id)), None)
def _db_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    notion = _service(snapshot, "notion"); out=[]
    for payload in (notion.get("database_rows", {}) if isinstance(notion, dict) else {}).values(): out.extend(_items(payload, "results"))
    return out

def runtime_rows(env: Any, server: str, sql: str, params: Iterable[Any] = ()) -> list[list[Any]]:
    snapshot = _snap(env); q = " ".join(sql.casefold().split()); p = list(params)
    if server == "email" and "from messages" in q and "subject, body_text" in q:
        mid = str(p[0]) if p else ""
        messages = _messages(snapshot, "INBOX") + _messages(snapshot, "Sent")
        messages.extend(_trace_result_rows(env, range(int(getattr(env, "current_stage", 23)) + 1)))
        matches: dict[str, list[Any]] = {}
        for row in messages:
            entity_id = str(row.get("message_id", row.get("email_id", row.get("id", ""))))
            if entity_id != mid:
                continue
            candidate = [
                row.get("subject", ""),
                row.get("body_text", row.get("body", row.get("content", ""))),
            ]
            previous = matches.get(entity_id)
            if previous is None or len(str(candidate[1])) > len(str(previous[1])):
                matches[entity_id] = candidate
        return list(matches.values())
    if server == "email" and "from messages" in q and "from_addr" in q:
        wanted = str(p[0]) if p else ""
        messages = _messages(snapshot, "INBOX") + _messages(snapshot, "Sent")
        messages.extend(_trace_result_rows(env, range(int(getattr(env, "current_stage", 23)) + 1)))
        return [[r.get("from_addr", r.get("from", ""))] for r in messages if str(r.get("id", r.get("email_id", ""))) == wanted]
    if server == "email" and "message_id from messages" in q:
        wanted={str(x) for x in p}; return [[r.get("message_id", r.get("email_id", r.get("id", "")))] for r in _messages(snapshot,"INBOX") + _messages(snapshot,"Sent") if str(r.get("message_id", r.get("email_id", r.get("id", "")))) in wanted]
    banking = _service(snapshot, "banking")
    if server == "banking" and "from accounts" in q:
        rows=_items(banking.get("accounts", []));
        if not rows and isinstance(banking.get("account_details"), dict):
            rows=[dict(v, account_id=k) for k,v in banking["account_details"].items() if isinstance(v, dict)]
        if "where user_id" in q: return [[a.get("account_id"),a.get("balance_minor"),int(bool(a.get("frozen")))] for a in rows]
        return [[a.get("balance_minor")] for a in rows if str(a.get("account_id")) == str(p[0] if p else "")]
    if server == "banking" and "from transactions" in q:
        rows=[]
        # The collector unwraps list_transactions' pagination envelope into a
        # bare row list (snapshot_capture._unwrap_envelope); older dict shapes
        # (envelope or per-account map) stay readable so both shapes score.
        tx = banking.get("transactions", {}) if isinstance(banking, dict) else {}
        if isinstance(tx, list): rows.extend(_items(tx))
        elif isinstance(tx, dict):
            for payload in tx.values(): rows.extend(_items(payload))
        if "where tx_id" in q: return [[r.get("account_id"),r.get("amount_minor"),r.get("kind"),r.get("balance_after_minor")] for r in rows if str(r.get("tx_id"))==str(p[0] if p else "")]
        if "acct_pension" in q: return [[r.get("tx_id")] for r in rows if str(r.get("account_id"))=="acct_pension"][:1]
        if "amount_minor < 0" in q:
            # Account-scoped checks pass account_id and cutoff; the global
            # post-kickoff check passes only the cutoff date.
            account_id = str(p[0]) if "account_id = ?" in q and p else None
            cutoff = str(p[-1] if p else "2026-07-30")[:10]
            return [[r.get("tx_id"),r.get("account_id"),r.get("amount_minor"),r.get("posted_at")] for r in rows if int(r.get("amount_minor",0))<0 and str(r.get("posted_at", ""))[:10]>=cutoff and (account_id is None or str(r.get("account_id")) == account_id)][:1]
    card=_service(snapshot,"credit_card"); cards=_items(card.get("cards",[])) if isinstance(card,dict) else []
    if server=="credit_card" and "from cards" in q:
        if "where user_id" in q: return [[c.get("card_id"),c.get("status")] for c in cards]
        ids={str(x) for x in p}; rows=[c for c in cards if str(c.get("card_id")) in ids] if ids else cards
        if "card_id, statement_balance_minor" in q: return [[c.get("card_id"),c.get("statement_balance_minor"),c.get("unbilled_balance_minor"),c.get("available_credit_minor")] for c in rows]
        return [[c.get("statement_balance_minor"),c.get("unbilled_balance_minor"),c.get("available_credit_minor")] for c in rows]
    if server=="credit_card" and "from statements" in q:
        rows=[]
        stmts = card.get("statements", {}) if isinstance(card, dict) else {}
        if isinstance(stmts, list): rows.extend(_items(stmts))
        elif isinstance(stmts, dict):
            for payload in stmts.values(): rows.extend(_items(payload))
        return [[r.get("card_id"),r.get("interest_apr_bp"),r.get("min_payment_due_minor"),r.get("due_date"),r.get("period_start"),r.get("period_end"),r.get("closing_balance_minor"),r.get("status")] for r in rows if str(r.get("period_end"))=="2026-07-28"]
    if server=="credit_card" and "from unbilled_transactions" in q:
        rows=[]
        unbilled = card.get("unbilled", {}) if isinstance(card, dict) else {}
        if isinstance(unbilled, list): rows.extend(_items(unbilled))
        elif isinstance(unbilled, dict):
            for payload in unbilled.values(): rows.extend(_items(payload))
        txid=str(p[0]) if p else ""; return [[r.get("card_id"),r.get("amount_minor"),r.get("merchant_name"),r.get("category"),r.get("kind")] for r in rows if str(r.get("tx_id"))==txid]
    if server=="credit_card" and "from statement_lines" in q:
        # Statement lines are nested in some provider projections. Walk the
        # frozen card snapshot so the scoring side never needs a live query.
        found: list[dict[str, Any]] = list(_trace_result_rows(env, range(int(getattr(env, "current_stage", 23)) + 1)))
        def walk(value: Any) -> None:
            if isinstance(value, dict):
                if value.get("line_id") is not None:
                    found.append(value)
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(card)
        wanted = str(p[0]) if p else ""
        return [[r.get("amount_minor"), r.get("kind"), r.get("merchant_name")] for r in found if str(r.get("line_id")) == wanted]
    if server=="credit_card" and "from payments" in q:
        out=[]
        # Payments are judged from the trace; only stages published so far
        # exist, so walk the observable prefix rather than the full 24.
        for call in _all_traces(env,range(int(getattr(env, "current_stage", 23)) + 1)):
            if str(call.get("name","")).endswith("make_payment") and _success(call):
                a=_decode(call.get("arguments",{})) or {}; r=_decode(call.get("result",{})) or {}; 
                if isinstance(r,dict) and r.get("payment_id"): out.append([r["payment_id"],a.get("card_id"),a.get("amount_minor"),a.get("source_hint"),r.get("posted_at","")])
        pid=str(p[0]) if p else ""; return [r[1:] for r in out if str(r[0])==pid]
    if server=="brokerage" and "from accounts" in q: return [[r.get("account_id"),r.get("status")] for r in _items(_service(snapshot,"brokerage").get("accounts",[]))]
    if server=="brokerage" and "count(*) from positions" in q: return [[len(_items(_service(snapshot,"brokerage").get("positions",[])))]]
    if server=="notion" and "from database_rows" in q:
        rows=_db_rows(snapshot); return [[r.get("id",r.get("row_id",""))] for r in rows if "public_rate_anchor" in json.dumps(r,ensure_ascii=False) and "2026-07-20" in json.dumps(r,ensure_ascii=False) and "3.0%" in json.dumps(r,ensure_ascii=False) and "3.5%" in json.dumps(r,ensure_ascii=False) and "not a personal mortgage execution rate" in json.dumps(r,ensure_ascii=False).lower()]
    if server=="calendar" and "from events" in q:
        return [[r.get("event_id"),r.get("summary",""),r.get("description",""),r.get("start_dt",r.get("start","")),r.get("status","confirmed"),r.get("created_at",""),r.get("updated_at","")] for r in _items(_service(snapshot,"calendar").get("events",[]))]
    return []

def account_balance_minor(env: Any, account_id: str) -> int | None:
    rows=runtime_rows(env,"banking","SELECT balance_minor FROM accounts WHERE account_id = ?",[account_id]); return integer_value(rows[0][0]) if rows and rows[0] else None
def post_kickoff_card_payments(env: Any, *, kickoff_date: str = "2026-07-30") -> list[tuple[str,str,int,str,str]] | None:
    out=[]
    # Same observable-prefix bound as every other trace walk: future stage
    # sidecars are not frozen yet at a stage boundary, and reading them raised
    # EvidenceError instead of judging the stage.
    for call in _all_traces(env,range(int(getattr(env, "current_stage", 23)) + 1)):
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
    brokerage = _service(_snap(env), "brokerage")
    orders = _items(brokerage.get("orders", []))
    cutoff = str(after)[:10]
    return not [row for row in orders if str(row.get("placed_at", ""))[:10] >= cutoff]

def sent_email_rows(env: Any) -> list[dict[str, Any]]:
    return _messages(_snap(env), "Sent")

def sent_email_matches(env: Any, *, recipient: str, groups: Iterable[Iterable[str]]) -> bool:
    wanted = recipient.casefold()
    sent = sent_email_rows(env)
    for row in sent:
        addresses = " ".join(str(row.get(k, "")) for k in ("to_addr", "to", "recipients", "to_addr_json"))
        body = f"{row.get('subject', '')}\n{row.get('body_text', row.get('body', ''))}"
        if wanted in addresses.casefold() and has_groups(body, groups):
            return True
    # The collector's Sent listing is metadata-only. Bind the persisted row to
    # the successful send/reply call and use that call's immutable arguments
    # for the body that the listing deliberately omits.
    sent_ids = {
        str(row.get("message_id", row.get("email_id", row.get("id", ""))))
        for row in sent
    }
    for call in _all_traces(env, range(int(getattr(env, "current_stage", 23)) + 1)):
        name = str(call.get("name", "")).casefold().replace("-", "_")
        if not (name.endswith("send_email") or name.endswith("reply_email")) or not _success(call):
            continue
        args = _decode(call.get("arguments", call.get("input", {})))
        result = _decode(call.get("result", call.get("content", {})))
        if not isinstance(args, dict) or not isinstance(result, dict):
            continue
        message_id = str(result.get("message_id", result.get("email_id", result.get("id", ""))))
        addresses = str(args.get("to", args.get("recipient", "")))
        if name.endswith("reply_email") and not addresses:
            source_id = str(args.get("email_id", ""))
            source = next((row for row in _messages(_snap(env), "INBOX") if str(row.get("id", row.get("email_id", ""))) == source_id), {})
            addresses = str(source.get("from_addr", source.get("from", "")))
        body = f"{args.get('subject', '')}\n{args.get('body', args.get('body_text', ''))}"
        if message_id in sent_ids and wanted in addresses.casefold() and has_groups(body, groups):
            return True
    return False

def _calendar_rows(env: Any) -> list[dict[str, Any]]:
    calendar = _service(_snap(env), "calendar")
    return _items(calendar.get("events", []))

def _calendar_touched(row: Mapping[str, Any], after: str = "2026-07-30") -> bool:
    cutoff = after[:10]
    return any(str(row.get(key, ""))[:10] >= cutoff for key in ("created_at", "updated_at"))

def no_duplicate_calendar_groups(env: Any, group_sets: Iterable[Iterable[Iterable[str]]], *, after: str = "2026-07-30") -> bool:
    rows = _calendar_rows(env)
    for groups in group_sets:
        matches = [row for row in rows if has_groups(f"{row.get('summary', '')}\n{row.get('description', '')}", groups)]
        if len(matches) != 1 or not _calendar_touched(matches[0], after):
            return False
    return True

def workspace_lifecycle_valid(env: Any, first_required: Mapping[str,int]) -> bool:
    raw = workspace_file_text(env, "/workspace/workspace_provenance.json")
    if not raw:
        current = int(getattr(env, "current_stage", 23))
        stages = [stage for stage in env.published_stages() if stage <= current]
        first_seen: dict[str, int] = {}
        for stage in stages:
            values = env.snapshot(stage).get("workspace", {})
            if not isinstance(values, dict):
                continue
            for path, text in values.items():
                name = str(path).rsplit("/", 1)[-1]
                if str(text).strip() and name not in first_seen:
                    first_seen[name] = stage
        current = int(getattr(env, "current_stage", 23))
        due = {name: expected for name, expected in first_required.items() if int(expected) <= current}
        return all(name in first_seen and first_seen[name] >= expected for name, expected in due.items())
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return False
    observed = payload.get("first_seen_stage") if isinstance(payload, dict) else None
    if not isinstance(observed, dict):
        return False
    # A provenance file must enumerate exactly the files whose first-required
    # stage has arrived. Partial maps would let due files evade the lifecycle
    # constraint; future or unknown keys are not valid evidence at this stage.
    current = int(getattr(env, "current_stage", 23))
    due = {name: expected for name, expected in first_required.items() if int(expected) <= current}
    if set(observed) != set(due):
        return False
    for name, expected in due.items():
        stage = observed[name]
        if isinstance(stage, bool):
            return False
        try:
            actual = int(stage)
        except (TypeError, ValueError):
            return False
        if actual < int(expected) or actual > current:
            return False
    return True

common = sys.modules[__name__]
