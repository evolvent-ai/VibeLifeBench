"""Shared Harbor-native helpers for the private-lending rubrics.

Rubrics consume only the immutable snapshot, trace, and response files exposed
by :mod:`harbor_evidence`. No helper creates a service client or reaches the
running MCP servers. Missing evidence raises through the Harbor accessors;
reachable empty values remain ordinary failed evidence.
"""
from __future__ import annotations

import json
from typing import Any

from harbor_evidence import response, snapshot, trace

STAGE_COUNT = 22
WANG_FANG_LEGAL = "usr_wang_fang"
WANG_FANG_CAL = "wang_fang"
_LAWYER_ROSTER_ACCOUNT_ID = "oa_lawyer_hub"
_SEED_SAVED_CASE_IDS = {"case_001", "case_009"}
_WITHDRAW_TERMS = ("withdraw", "CJK_9000_CJK_51FA_")
_MERGER_TERMS = ("lawyer_withdraw", "CJK_5F8B_CJK_6240_CJK_5408_CJK_5E76_")

# Single-word anchors keep the converted vocabulary measurable without putting
# solution phrases into the user-facing instructions.
LEXICON_ANCHORS = [
    ["Wang"], ["Fang"], ["Chen"], ["Qiang"], ["Hangzhou"], ["Ningbo"],
    ["private"], ["lending"], ["court"], ["case"], ["loan"], ["legal"],
    ["evidence"], ["lawyer"], ["appeal"], ["LPR"], ["Notion"], ["IOU"],
]

def _current_stage(env, stage: int | None = None) -> int:
    if stage is not None:
        return int(stage)
    value = getattr(env, "current_stage", None)
    return int(21 if value is None else value)


def _published_stages(env) -> list[int]:
    getter = getattr(env, "published_stages", None)
    if callable(getter):
        return sorted({int(value) for value in getter()})
    return list(range(STAGE_COUNT))


def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


def _section(env, server: str, stage: int | None = None) -> Any:
    value = snapshot(env, _current_stage(env, stage)).get(server)
    if isinstance(value, dict) and "error" in value and len(value) == 1:
        return None
    return value


def _all_corpus(env) -> str:
    """All frozen agent responses plus the latest captured workspace files."""
    parts: list[str] = []
    stages = _published_stages(env)
    for stage in stages:
        parts.append(response(env, stage))
    if stages:
        workspace = _section(env, "workspace", max(stages))
        if isinstance(workspace, dict):
            values = workspace.get("files", workspace)
            if isinstance(values, dict):
                parts.extend(str(item) for item in values.values())
    return "\n".join(parts)


def _stage_corpus(env, stage: int) -> str:
    return response(env, int(stage))


def _saved_cases(env) -> list[dict] | None:
    data = _section(env, "legal_search")
    if not isinstance(data, dict):
        return None if data is None else []
    value = _decode(data.get("saved_cases"))
    if isinstance(value, dict):
        if "error" in value:
            return None
        value = value.get("saved", value.get("results", []))
    return list(value) if isinstance(value, list) else []


def _saved_case_ids(env) -> list[str] | None:
    saved = _saved_cases(env)
    if saved is None:
        return None
    return [str(row.get("case_id")) for row in saved if isinstance(row, dict) and row.get("case_id")]


def _saved_non_seed_case_ids(env) -> list[str] | None:
    ids = _saved_case_ids(env)
    return None if ids is None else [value for value in ids if value not in _SEED_SAVED_CASE_IDS]


def _saved_notes_text(env) -> str:
    return " ".join(str(row.get("note") or "") for row in (_saved_cases(env) or []) if isinstance(row, dict))


def _email_rows(env, folder: str) -> list[dict] | None:
    section = _section(env, "email")
    if not isinstance(section, dict):
        return None if section is None else []
    bucket = section.get(folder.lower())
    if not isinstance(bucket, dict):
        return []
    listing = bucket.get("listing", bucket)
    rows = listing.get("emails", []) if isinstance(listing, dict) else listing
    if not isinstance(rows, list):
        return []
    details = bucket.get("details", [])
    by_id = {
        str(row.get("email_id") or row.get("id")): row
        for row in details
        if isinstance(row, dict) and (row.get("email_id") or row.get("id"))
    }
    merged: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        item = dict(row)
        identity = str(item.get("email_id") or item.get("id") or "")
        if identity in by_id:
            item.update(by_id[identity])
        merged.append(item)
    return merged


def _sent_emails(env) -> list[dict] | None:
    return _email_rows(env, "sent")


def _drafts(env) -> list[dict] | None:
    section = _section(env, "email")
    if not isinstance(section, dict):
        return None if section is None else []
    bucket = section.get("drafts", {})
    if not isinstance(bucket, dict):
        return []
    listing = bucket.get("listing", bucket)
    rows = listing.get("drafts", listing.get("emails", [])) if isinstance(listing, dict) else listing
    return list(rows) if isinstance(rows, list) else []


def _notifications(env) -> list[dict] | None:
    section = _section(env, "notification_hub")
    if not isinstance(section, dict):
        return None if section is None else []
    value = _decode(section.get("notifications", []))
    if isinstance(value, dict):
        if "error" in value:
            return None
        value = value.get("notifications", value.get("results", []))
    return list(value) if isinstance(value, list) else []


def _subscriptions(env) -> list[dict] | None:
    section = _section(env, "notification_hub")
    if not isinstance(section, dict):
        return None if section is None else []
    value = _decode(section.get("subscriptions", []))
    if isinstance(value, dict):
        if "error" in value:
            return None
        value = value.get("subscriptions", value.get("results", []))
    return list(value) if isinstance(value, list) else []


def _trace_rows(env, stage: int | None = None) -> list[dict[str, Any]]:
    stages = [_current_stage(env, stage)] if stage is not None else _published_stages(env)
    rows: list[dict[str, Any]] = []
    for item in stages:
        rows.extend(dict(row) for row in trace(env, item) if isinstance(row, dict))
    return rows


def _trace_result(row: dict[str, Any]) -> Any:
    if row.get("success") is False or row.get("succeeded") is False:
        return None
    result = _decode(row.get("result"))
    return None if isinstance(result, dict) and result.get("error") else result


def _account_feed(env, account_id: str) -> list[dict] | None:
    """Return feed rows captured in the immutable agent tool trace."""
    found: list[dict] = []
    for row in _trace_rows(env):
        name = str(row.get("name") or "").lower().replace("-", "_")
        args = row.get("arguments") or row.get("input") or {}
        if "get_account_feed" not in name or not isinstance(args, dict):
            continue
        if str(args.get("account_id") or "") != account_id:
            continue
        result = _trace_result(row)
        if isinstance(result, list):
            found.extend(item for item in result if isinstance(item, dict))
        elif isinstance(result, dict):
            found.extend(item for item in result.get("posts", []) if isinstance(item, dict))
    return found


def _official_accounts(env) -> list[dict] | None:
    return _subscriptions(env)


def _lawyer_roster_posts(env) -> list[dict] | None:
    posts = _account_feed(env, _LAWYER_ROSTER_ACCOUNT_ID)
    if posts is None:
        return None
    return [post for post in posts if str(post.get("account_id") or "") == _LAWYER_ROSTER_ACCOUNT_ID]


def _lawyer_post_text(post: dict) -> str:
    return " ".join(
        str(post.get(key) or "")
        for key in ("post_id", "account_id", "title", "summary", "body", "content", "url")
        if post.get(key)
    )


def _lawyer_roster_text(env) -> str | None:
    posts = _lawyer_roster_posts(env)
    return None if posts is None else " ".join(_lawyer_post_text(post) for post in posts)


def _lawyer_roster_fact(env, lawyer_id: str, groups: list[list[str]]) -> bool:
    posts = _lawyer_roster_posts(env)
    if posts is None:
        return False
    needle = lawyer_id.lower()
    for post in posts:
        text = _lawyer_post_text(post).lower()
        if needle in text and all(any(term.lower() in text for term in group) for group in groups):
            return True
    return False


def _lawyer_withdrawal_notice(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False
    groups = [["LD-006"], ["conflict of interest"], list(_WITHDRAW_TERMS), list(_MERGER_TERMS)]
    return any(
        all(any(term.lower() in json.dumps(item, ensure_ascii=False, default=str).lower() for term in group) for group in groups)
        for item in notifications if isinstance(item, dict)
    )


def _calendar_events(env) -> list[dict] | None:
    section = _section(env, "calendar")
    if not isinstance(section, dict):
        return None if section is None else []
    value = _decode(section.get("events", []))
    if isinstance(value, dict):
        if "error" in value:
            return None
        value = value.get("events", value.get("results", []))
    return list(value) if isinstance(value, list) else []


def _event_text(event: dict) -> str:
    parts = [event.get("summary") or "", event.get("description") or "", event.get("location") or ""]
    start = event.get("start") or {}
    if isinstance(start, dict):
        parts.append(start.get("dateTime") or start.get("date") or "")
    return " ".join(str(value) for value in parts)


def _all_events_text(env) -> str:
    events = _calendar_events(env)
    return "" if events is None else " ".join(_event_text(event) for event in events)


def _rt_text(item: dict) -> str:
    if not isinstance(item, dict):
        return ""
    if item.get("plain_text"):
        return str(item["plain_text"])
    text = item.get("text")
    return str(text.get("content") or "") if isinstance(text, dict) else ""


def _notion_pages(env) -> list[dict] | None:
    section = _section(env, "notion")
    if not isinstance(section, dict):
        return None if section is None else []
    value = _decode(section.get("pages", []))
    if isinstance(value, dict):
        if "error" in value:
            return None
        value = value.get("results", [])
    return list(value) if isinstance(value, list) else []


def _notion_search(env, query: str = "private lending") -> list[dict] | None:
    pages = _notion_pages(env)
    if pages is None:
        return None
    needle = str(query or "").lower()
    if not needle:
        return pages
    return [page for page in pages if needle in json.dumps(page, ensure_ascii=False, default=str).lower()]


def _notion_titles(env, query: str = "private lending") -> str:
    titles: list[str] = []
    for page in (_notion_search(env, query) or []):
        props = page.get("properties", {}) if isinstance(page, dict) else {}
        title_prop = props.get("title", {}) if isinstance(props, dict) else {}
        for item in title_prop.get("title", []) if isinstance(title_prop, dict) else []:
            titles.append(_rt_text(item))
        for item in page.get("title", []) if isinstance(page, dict) and isinstance(page.get("title"), list) else []:
            titles.append(_rt_text(item))
    return " ".join(titles)


def _page_blocks(env, page_id: str) -> list[dict] | None:
    section = _section(env, "notion")
    if not isinstance(section, dict):
        return None if section is None else []
    blocks = section.get("page_blocks", {})
    value = blocks.get(page_id, []) if isinstance(blocks, dict) else []
    if isinstance(value, dict):
        if "error" in value:
            return None
        value = value.get("results", [])
    return list(value) if isinstance(value, list) else []


def _blocks_text(blocks: list[dict] | None) -> str:
    if blocks is None:
        return ""
    chunks: list[str] = []
    for block in blocks:
        if not isinstance(block, dict) or str(block.get("id") or block.get("block_id") or "").startswith("lending_sys_"):
            continue
        kind = block.get("type")
        content = block.get(kind, {}) if kind else {}
        if isinstance(content, dict):
            chunks.extend(_rt_text(item) for item in content.get("rich_text", []) or [])
    return " ".join(chunks)


def _notion_page_text(env, query: str = "private lending") -> str | None:
    pages = _notion_search(env, query)
    if pages is None:
        return None
    chunks: list[str] = []
    for page in pages:
        if isinstance(page, dict) and page.get("object") == "page" and page.get("id"):
            blocks = _page_blocks(env, str(page["id"]))
            if blocks is None:
                return None
            chunks.append(_blocks_text(blocks))
    return " ".join(chunks)


def _journal_text(env) -> str | None:
    pages = _notion_pages(env)
    if pages is None:
        return None
    chunks: list[str] = []
    for page in pages:
        if isinstance(page, dict) and page.get("object") == "page" and page.get("id"):
            blocks = _page_blocks(env, str(page["id"]))
            if blocks is None:
                return None
            text = _blocks_text(blocks)
            if text:
                chunks.append(text)
    return " ".join(chunks)


def _norm_num(text: str) -> str:
    return "".join(ch for ch in (text or "") if ch not in ",，¥$ 　")


def _assistant_calendar_events(env) -> list[dict] | None:
    events = _calendar_events(env)
    if events is None:
        return None
    seed_ids = {"evt_lawyer_0522", "evt_school_0528", "evt_cmb_repay"}
    return [
        event for event in events
        if isinstance(event, dict)
        and not str(event.get("id") or event.get("event_id") or "").startswith(("evt_lending_sys_", "evt_bg_"))
        and str(event.get("id") or event.get("event_id") or "") not in seed_ids
    ]


def _assistant_calendar_text(env) -> str | None:
    events = _assistant_calendar_events(env)
    return None if events is None else " ".join(_event_text(event) for event in events)
