"""Shared helpers for food_safety_dispute_33d rubrics.

Return-shape conventions (verified against server source):
- legal_search list_saved / search_cases / get_case_citations → bare list / dict.
- email_mock get_emails / search_emails → dict with key "emails"; item field "email_id".
- notification_hub list_subscriptions / list_notifications / list_official_accounts /
  get_account_feed → bare list.
- calendar list_events → bare list; start time nested at event["start"]["dateTime"].
- notion API-post-search → dict with key "results".

Cross-server user_id (CRITICAL):
- legal_search / notification_hub user_id = "usr_zhao_meng".
- calendar user_id = "zhao_meng".
- email / notion have NO user_id (account/workspace scoped).

Helpers return None when evidence is unavailable; every dependent positive check fails closed.
A reachable-but-empty result returns [] / "" so "did nothing" can FAIL.
"""
from __future__ import annotations

import json

from loguru import logger

ZHAO_LEGAL = "usr_zhao_meng"   # legal_search / notification_hub user_id
ZHAO_CAL = "zhao_meng"         # calendar user_id


def _loads(result):
    if result is None:
        return None
    if isinstance(result, str):
        try:
            return json.loads(result)
        except Exception:
            return None
    return result


# ── agent response corpus ────────────────────────────────────────────────
def _all_corpus(env) -> str:
    dir_path = "/terrarium/agent_responses"
    try:
        files = env.workspace.fs.list_dir(dir_path)
    except Exception:
        return ""
    texts = []
    for f in files or []:
        try:
            content = env.workspace.fs.read_file(f"{dir_path}/{f}")
            if isinstance(content, bytes):
                content = content.decode("utf-8", errors="replace")
            texts.append(content)
        except Exception:
            continue
    return "\n".join(texts)


def _stage_corpus(env, stage: int) -> str:
    path = f"/terrarium/agent_responses/stage_{stage}.txt"
    try:
        content = env.workspace.fs.read_file(path)
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="replace")
        return content
    except Exception:
        return ""


# ── legal_search ───────────────────────────────────────────────────────────
def _saved_cases(env) -> list[dict] | None:
    """赵萌收藏的判例 (含 agent 运行时新收藏的)。"""
    try:
        result = env.legal_search_mock.call_tool("list_saved", user_id=ZHAO_LEGAL)
    except Exception as e:
        logger.debug(f"_saved_cases: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        return [] if "error" in data else data.get("saved", []) or []
    return data if isinstance(data, list) else []


def _saved_case_ids(env) -> list[str] | None:
    saved = _saved_cases(env)
    if saved is None:
        return None
    return [s.get("case_id") for s in saved if s.get("case_id")]


def _saved_non_seed_case_ids(env) -> list[str] | None:
    ids = _saved_case_ids(env)
    if ids is None:
        return None
    seed_ids = {"case_f02", "case_f07"}
    return [cid for cid in ids if cid not in seed_ids]


def _saved_notes_text(env) -> str:
    """Concatenate all notes on saved cases (so we can check agent's annotations)."""
    saved = _saved_cases(env)
    if not saved:
        return ""
    return " ".join(str(s.get("note") or "") for s in saved)


# ── email ────────────────────────────────────────────────────────────────
def _sent_emails(env) -> list[dict] | None:
    try:
        result = env.email_mock.call_tool("get_emails", folder="Sent", page_size=100)
    except Exception as e:
        logger.debug(f"_sent_emails: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        if "error" in data:
            return []
        return data.get("emails", []) or []
    return data if isinstance(data, list) else []


def _drafts(env) -> list[dict] | None:
    try:
        result = env.email_mock.call_tool("get_emails", folder="Drafts", page_size=100)
    except Exception as e:
        logger.debug(f"_drafts: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        if "error" in data:
            return []
        return data.get("emails", []) or []
    return data if isinstance(data, list) else []


# ── notification_hub ──────────────────────────────────────────────────────
def _subscriptions(env) -> list[dict] | None:
    try:
        result = env.notification_hub_mock.call_tool(
            "list_subscriptions", user_id=ZHAO_LEGAL
        )
    except Exception as e:
        logger.debug(f"_subscriptions: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        return [] if "error" in data else data.get("subscriptions", []) or []
    return data if isinstance(data, list) else []


def _notifications(env) -> list[dict] | None:
    try:
        result = env.notification_hub_mock.call_tool(
            "list_notifications", user_id=ZHAO_LEGAL, limit=500
        )
    except Exception as e:
        logger.debug(f"_notifications: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        return [] if "error" in data else data.get("notifications", []) or []
    return data if isinstance(data, list) else []


def _account_feed(env, account_id: str) -> list[dict] | None:
    """Posts of one official account (e.g. the inspection roster). Bare list."""
    try:
        result = env.notification_hub_mock.call_tool(
            "get_account_feed", account_id=account_id, limit=50
        )
    except Exception as e:
        logger.debug(f"_account_feed: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        return [] if "error" in data else data.get("posts", []) or []
    return data if isinstance(data, list) else []


def _official_accounts(env) -> list[dict] | None:
    try:
        result = env.notification_hub_mock.call_tool(
            "list_official_accounts", user_id=ZHAO_LEGAL
        )
    except Exception as e:
        logger.debug(f"_official_accounts: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        return [] if "error" in data else data.get("accounts", []) or []
    return data if isinstance(data, list) else []


_INSPECTION_ROSTER_ACCOUNT_ID = "oa_jianyan_hub"


def _inspection_roster_posts(env) -> list[dict] | None:
    """Rows returned by the official inspection-roster account only."""
    posts = _account_feed(env, _INSPECTION_ROSTER_ACCOUNT_ID)
    if posts is None:
        return None
    return [
        post
        for post in posts
        if isinstance(post, dict)
        and str(post.get("account_id") or "") == _INSPECTION_ROSTER_ACCOUNT_ID
    ]


def _inspection_post_text(post: dict) -> str:
    return " ".join(
        str(post.get(key) or "")
        for key in ("post_id", "account_id", "title", "summary", "body", "content", "url")
        if post.get(key)
    )


def _inspection_roster_text(env) -> str | None:
    """Current official inspector-roster facts, or ``None`` when unreachable."""
    posts = _inspection_roster_posts(env)
    if posts is None:
        return None
    return " ".join(_inspection_post_text(post) for post in posts)


def _inspection_roster_fact(env, provider_id: str, groups: list[list[str]]) -> bool:
    """Bind one recommendation/exclusion to one provider-specific official row."""
    posts = _inspection_roster_posts(env)
    if posts is None:
        return False
    provider = provider_id.lower()
    for post in posts:
        low = _inspection_post_text(post).lower()
        if provider not in low:
            continue
        if all(any(term.lower() in low for term in group) for group in groups):
            return True
    return False


def _inspection_pause_notice(env) -> str | None:
    """Return the one notification that binds JY-006, pause, and unissued report."""
    notifications = _notifications(env)
    if notifications is None:
        return None
    groups = [
        ["JY-006"],
        ["暂停"],
        ["not_issued"],
        ["inspection_provider_paused", "尚未出具"],
    ]
    for item in notifications:
        if not isinstance(item, dict):
            continue
        text = json.dumps(item, ensure_ascii=False, default=str)
        low = text.lower()
        if all(any(term.lower() in low for term in group) for group in groups):
            return text
    return ""


# ── calendar ──────────────────────────────────────────────────────────────
def _calendar_events(env) -> list[dict] | None:
    try:
        result = env.calendar_mock.call_tool(
            "list_events",
            time_min="2026-05-01T00:00:00+08:00",
            time_max="2026-09-30T23:59:00+08:00",
            max_results=500,
        )
    except Exception as e:
        logger.debug(f"_calendar_events: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        return [] if "error" in data else data.get("events", []) or []
    return data if isinstance(data, list) else []


def _event_text(ev: dict) -> str:
    """Flatten an event into searchable text (summary + description + location + start)."""
    parts = [ev.get("summary") or "", ev.get("description") or "", ev.get("location") or ""]
    start = ev.get("start") or {}
    if isinstance(start, dict):
        parts.append(start.get("dateTime") or start.get("date") or "")
    return " ".join(str(p) for p in parts)


def _all_events_text(env) -> str:
    """All calendar events flattened; '' if none, None if unreachable."""
    evs = _calendar_events(env)
    if evs is None:
        return None
    return " ".join(_event_text(e) for e in evs)


# ── notion ────────────────────────────────────────────────────────────────
def _rt_text(rt: dict) -> str:
    """Extract text from a Notion rich_text item.

    Tool-created rich_text has {"type":"text","text":{"content":...}} with NO
    plain_text field; seeded rows may carry plain_text. Handle both.
    """
    if not isinstance(rt, dict):
        return ""
    pt = rt.get("plain_text")
    if pt:
        return pt
    txt = rt.get("text")
    if isinstance(txt, dict) and txt.get("content"):
        return txt["content"]
    return ""


def _notion_search(env, query: str = "食品") -> list[dict] | None:
    try:
        result = env.notion_mock.call_tool("API-post-search", query=query)
    except Exception as e:
        logger.debug(f"_notion_search: {e}")
        return None
    data = _loads(result)
    if data is None:
        return None
    if isinstance(data, dict):
        return data.get("results", []) or []
    return []


def _notion_titles(env, query: str = "食品") -> str:
    results = _notion_search(env, query)
    if not results:
        return ""
    titles = []
    for page in results:
        props = page.get("properties", {}) if isinstance(page, dict) else {}
        title_prop = props.get("title", {})
        for t in (title_prop.get("title", []) if isinstance(title_prop, dict) else []):
            titles.append(_rt_text(t))
        for t in (page.get("title", []) if isinstance(page.get("title"), list) else []):
            titles.append(_rt_text(t))
    return " ".join(titles)


def _notion_page_text(env, query: str = "食品") -> str | None:
    """Return assistant-authored child-block text for matching pages.

    Page titles and timeline-owned ``food_sys_*`` blocks are world/seed state, not
    evidence that the assistant persisted an analysis or follow-up. ``None``
    means the Notion evidence channel is unavailable; callers must fail closed.
    """
    results = _notion_search(env, query)
    if results is None:
        return None
    if not results:
        return ""
    chunks: list[str] = []
    for page in results:
        if not isinstance(page, dict) or page.get("object") != "page":
            continue
        pid = page.get("id")
        if not pid:
            continue
        try:
            res = env.notion_mock.call_tool("API-get-block-children", block_id=pid)
        except Exception as exc:
            logger.debug(f"_notion_page_text: {exc}")
            return None
        data = _loads(res)
        if data is None:
            return None
        blocks = data.get("results", []) if isinstance(data, dict) else []
        for block in blocks or []:
            if not isinstance(block, dict):
                continue
            block_id = str(block.get("id") or block.get("block_id") or "")
            if block_id.startswith("food_sys_"):
                continue
            block_type = block.get("type")
            content = block.get(block_type, {}) if block_type else {}
            if not isinstance(content, dict):
                continue
            for item in content.get("rich_text", []) or []:
                chunks.append(_rt_text(item))
    return " ".join(chunks)


# ── backend-grounded food litigation journal ────────────────────────────────
# Positive legal/selection checks read persisted Notion state rather than
# /terrarium/agent_responses. Blocks inserted by timeline mutations use the
# reserved `food_sys_*` prefix and are intentionally excluded: a newly revealed
# world fact is context, not evidence that the assistant analyzed or acted on it.
_FOOD_JOURNAL_QUERIES = (
    "食品安全维权",
    "食品安全",
    "维权",
    "证据",
    "诉求",
    "质证",
    "检验",
    "庭后",
    "上诉",
    "复盘",
    "案件",
)


def _food_journal_text(env) -> str | None:
    """Return persisted assistant-authored case-journal text.

    ``None`` means Notion is unreachable; ``""`` means reachable but no
    assistant-authored journal content exists. Timeline-owned blocks whose IDs
    begin with ``food_sys_`` are excluded from scoring evidence.
    """
    probe = _notion_search(env, "食品安全维权")
    if probe is None:
        return None

    seen_pages: set[str] = set()
    chunks: list[str] = []
    for query in _FOOD_JOURNAL_QUERIES:
        results = _notion_search(env, query)
        if not results:
            continue
        for page in results:
            if not isinstance(page, dict) or page.get("object") != "page":
                continue
            page_id = page.get("id")
            if not page_id or page_id in seen_pages:
                continue
            seen_pages.add(page_id)

            try:
                result = env.notion_mock.call_tool("API-get-block-children", block_id=page_id)
            except Exception as exc:
                logger.debug(f"_food_journal_text: {exc}")
                return None
            data = _loads(result)
            if data is None:
                return None
            blocks = data.get("results", []) if isinstance(data, dict) else []
            for block in blocks or []:
                if not isinstance(block, dict):
                    continue
                block_id = str(block.get("id") or block.get("block_id") or "")
                if block_id.startswith("food_sys_"):
                    continue
                block_type = block.get("type")
                content = block.get(block_type, {}) if block_type else {}
                if not isinstance(content, dict):
                    continue
                for item in content.get("rich_text", []) or []:
                    chunks.append(_rt_text(item))
    return " ".join(chunk for chunk in chunks if chunk)


def _norm_num(text: str) -> str:
    """Normalize common currency/thousands separators in persisted text."""
    if not text:
        return ""
    return "".join(ch for ch in text if ch not in ",，¥$ 　")


def _assistant_calendar_events(env) -> list[dict] | None:
    """Calendar events not seeded or injected by the task timeline.

    ``evt_food_sys_*`` are timeline-owned sync rows and ``evt_bg_*``/the three
    named seed rows pre-exist Stage 0. Only remaining events are assistant/user
    persisted actions suitable as positive scoring evidence.
    """
    events = _calendar_events(env)
    if events is None:
        return None
    seed_ids = {"evt_lawyer_0522", "evt_clinic_0527", "evt_card_repay"}
    result = []
    for event in events:
        if not isinstance(event, dict):
            continue
        event_id = str(event.get("id") or event.get("event_id") or "")
        if event_id.startswith(("evt_food_sys_", "evt_bg_")) or event_id in seed_ids:
            continue
        result.append(event)
    return result


def _assistant_calendar_text(env) -> str | None:
    events = _assistant_calendar_events(env)
    if events is None:
        return None
    return " ".join(_event_text(event) for event in events)
