"""Shared helpers for private_lending_33d rubrics.

Return-shape conventions (verified against server source):
- legal_search list_saved / search_cases / get_case_citations → bare list / dict.
- email_mock get_emails / search_emails → dict with key "emails"; item field "email_id".
- notification_hub list_subscriptions / list_notifications / list_official_accounts /
  get_account_feed → bare list.
- calendar list_events → bare list; start time nested at event["start"]["dateTime"].
- notion API-post-search → dict with key "results".

Cross-server user_id (CRITICAL):
- legal_search / notification_hub user_id = "usr_wang_fang".
- calendar user_id = "wang_fang".
- email / notion have NO user_id (account/workspace scoped).

Helpers return None when evidence is unavailable; every dependent positive check fails closed.
A reachable-but-empty result returns [] / "" so "did nothing" can FAIL.
"""
from __future__ import annotations

import json

from loguru import logger

WANG_FANG_LEGAL = "usr_wang_fang"   # legal_search / notification_hub user_id
WANG_FANG_CAL = "wang_fang"         # calendar user_id


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
    """王芳收藏的判例 (含 agent 运行时新收藏的)。"""
    try:
        result = env.legal_search_mock.call_tool("list_saved", user_id=WANG_FANG_LEGAL)
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


# 种子已为 usr_wang_fang 预收藏 2 个判例 (saved_seed_001→case_001, saved_seed_002→case_009),
# 故 len(saved)>=1 从种子起就恒 True。真正做了检索的 agent 会另收藏/引用超出这两个的判例。
_SEED_SAVED_CASE_IDS = {"case_001", "case_009"}


def _saved_non_seed_case_ids(env) -> list[str] | None:
    ids = _saved_case_ids(env)
    if ids is None:
        return None
    return [cid for cid in ids if cid not in _SEED_SAVED_CASE_IDS]


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
            "list_subscriptions", user_id=WANG_FANG_LEGAL
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
            "list_notifications", user_id=WANG_FANG_LEGAL, limit=500
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
    """Posts of one official account (e.g. the lawyer roster). Bare list."""
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
            "list_official_accounts", user_id=WANG_FANG_LEGAL
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


# ── calendar ──────────────────────────────────────────────────────────────
def _calendar_events(env) -> list[dict] | None:
    try:
        result = env.calendar_mock.call_tool(
            "list_events",
            time_min="2026-05-01T00:00:00+08:00",
            time_max="2026-09-30T23:59:00+08:00",
            max_results=100,
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


def _notion_search(env, query: str = "借贷") -> list[dict] | None:
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


def _notion_titles(env, query: str = "借贷") -> str:
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


def _notion_page_text(env, query: str = "借贷") -> str | None:
    """Return assistant-authored child-block text for matching pages.

    Page titles and timeline-owned ``lending_sys_*`` blocks are world/seed state, not
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
            if block_id.startswith("lending_sys_"):
                continue
            block_type = block.get("type")
            content = block.get(block_type, {}) if block_type else {}
            if not isinstance(content, dict):
                continue
            for item in content.get("rich_text", []) or []:
                chunks.append(_rt_text(item))
    return " ".join(chunks)


# ── backend-grounded litigation journal (env-state, NOT agent prose) ─────────
# HARDENING (2026-07-25): the d_* legal-analysis checks used to score off
# _all_corpus keyword-OR (agent prose in /terrarium/agent_responses). Per manual
# §7 证据优先级 (环境状态 > 工具调用 > 文本表达), an agent that merely *mentions*
# 砍头息/保证期间/夫妻共同债务 in its reply must NOT score; the CONCLUSION must be
# persisted as a real Notion page/block the backend can read. _journal_text below
# reads assistant-authored child-block rich_text from the persisted case pages via the
# same read tools an agent uses (API-post-search / API-get-block-children).
#
# Return contract (fail-closed evidence semantics):
#   • None  → Notion server UNREACHABLE (the dependent check must fail closed)
#   • ""    → reachable but the case journal has no matching content ("did nothing"
#             / talk-only → the d_* check FAILs)
#   • str   → concatenated assistant-authored journal block text to search within.
#
# The queries cover every case-page an agent would plausibly create/maintain
# across the 22 stages (追偿主页 / 证据 / 质证 / 律师 / 庭后 / 复盘). API-post-search
# matches the query substring against page TITLE *or* properties_json, so pages
# whose title contains any of these tokens are found; child blocks are then read
# in full and flattened.
_JOURNAL_QUERIES = (
    "民间借贷追偿", "追偿", "借贷", "陈强", "证据", "质证",
    "律师", "本金", "庭后", "复盘", "案件",
)


def _journal_text(env) -> str | None:
    """Persisted assistant-authored Notion journal block text, deduped across queries.

    None ⟺ Notion unreachable. '' ⟺ reachable but nothing persisted. This is the
    backend-state channel the hardened d_* checks read instead of agent prose.
    """
    # Probe reachability once: if the very first search raises, treat as unreachable.
    probe = _notion_search(env, "民间借贷追偿")
    if probe is None:
        return None  # server unavailable; dependent checks fail closed
    seen_ids: set[str] = set()
    chunks: list[str] = []
    for q in _JOURNAL_QUERIES:
        results = _notion_search(env, q)
        if not results:
            continue
        for page in results:
            if not isinstance(page, dict) or page.get("object") != "page":
                continue
            pid = page.get("id")
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)
            # Assistant-authored child blocks (page title is world state).
            try:
                res = env.notion_mock.call_tool("API-get-block-children", block_id=pid)
            except Exception as exc:
                logger.debug(f"_journal_text: {exc}")
                return None
            data = _loads(res)
            if data is None:
                return None
            blocks = data.get("results", []) if isinstance(data, dict) else []
            for b in blocks or []:
                if not isinstance(b, dict):
                    continue
                block_id = str(b.get("id") or b.get("block_id") or "")
                if block_id.startswith("lending_sys_"):
                    continue
                btype = b.get("type")
                content = b.get(btype, {}) if btype else {}
                for rt in (content.get("rich_text", []) if isinstance(content, dict) else []):
                    chunks.append(_rt_text(rt))
    return " ".join(chunks)


def _norm_num(text: str) -> str:
    """Normalize a numeric-bearing text so 360,000 / 360000 / ¥360000 all match.

    Strips thousands separators and common currency glyphs, keeping digits and
    Chinese numerals intact, so a persisted '本金 360,000 元' satisfies a check
    that looks for the token '360000'.
    """
    if not text:
        return ""
    out = []
    for ch in text:
        if ch in ",，¥$ 　":  # thousands sep / currency / spaces
            continue
        out.append(ch)
    return "".join(out)


def _assistant_calendar_events(env) -> list[dict] | None:
    """Return calendar rows created after kickoff by the assistant/user.

    Timeline rows use ``evt_lending_sys_*``; ``evt_bg_*`` and the three named
    seed rows pre-exist Stage 0 and cannot prove an assistant action.
    """
    events = _calendar_events(env)
    if events is None:
        return None
    seed_ids = {"evt_lawyer_0522", "evt_school_0528", "evt_cmb_repay"}
    result = []
    for event in events:
        if not isinstance(event, dict):
            continue
        event_id = str(event.get("id") or event.get("event_id") or "")
        if event_id.startswith(("evt_lending_sys_", "evt_bg_")) or event_id in seed_ids:
            continue
        result.append(event)
    return result


def _assistant_calendar_text(env) -> str | None:
    events = _assistant_calendar_events(env)
    if events is None:
        return None
    return " ".join(_event_text(event) for event in events)
