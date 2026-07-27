# legal-search-mock

A FastMCP-based, fully-offline mock of China's 裁判文书网 + 国家法律法规检索
(Chinese legal research: case judgments + statutes + citations). Runs over
**streamable-HTTP** (no stdio) with a local SQLite database.

All party names are anonymized (张某/李某 style); all judgment text is
original/synthesized and statute text is simplified public-domain-style
(劳动合同法 / 劳动法 are public domain). There is **no clock, no RNG, no CLI** —
issued IDs come from a `_counters` table, and state changes mid-task arrive as
out-of-band SQL mutations from the orchestrator (the server is oblivious).

The package ships **schema-only**; all rows enter via the env directory's
`init.sql`.

## Tools (agent-facing)

Cases (裁判文书):
- `search_cases(keyword?, court?, case_type?, date_from?, date_to?, limit?=20)` — search judgments, newest first; `case_type` ∈ {劳动争议, 合同纠纷, 侵权责任, 婚姻家庭, 劳动仲裁, 其他}; `court` accepts a court_id or a 法院名称 substring; dates `YYYY-MM-DD`; `limit` 1–100.
- `get_case(case_id)` — full judgment: 当事人(脱敏)/案由/事实/裁判理由/裁判要旨/判决主文/结果/关键词.
- `get_similar_cases(case_id, limit?=5)` — same `case_type`, ranked by shared-keyword overlap then recency; `limit` 1–50.
- `get_case_citations(case_id)` — `statutes_cited` (法条) + `cases_cited` (referenced judgments).

Statutes (法律法规):
- `search_statutes(keyword?, limit?=20)` — search statutes by 名称/简称/摘要; `limit` 1–100.
- `get_statute(statute_id)` — statute metadata + `article_count`; `status` ∈ {现行有效, 已修订, 已废止}.
- `list_statute_articles(statute_id)` — articles (法条) in document order (id/article_no/heading).
- `get_article(article_id)` — full text (法条全文) of one article + statute_name/article_no.

Courts (法院):
- `list_courts()` — all courts/仲裁委 (id/name/level/region); `level` ∈ {基层法院, 中级法院, 高级法院, 最高法院, 仲裁委员会}.
- `get_court(court_id)` — one court + `case_count`.

Library (per-user 收藏):
- `save_case(user_id, case_id)` — save a case (idempotent).
- `list_saved(user_id)` — saved cases (oldest first) with note + embedded case summary.
- `add_note_to_case(user_id, case_id, note)` — set/replace a note; auto-saves if not already saved.

## Quick start

```
legal-search-mock --host 0.0.0.0 --port 8019 \
                  --env <repo>/envs/legal_search/labor_dispute_2026
```

Served at `http://<host>:<port>/mcp` (streamable-HTTP). Inside Docker the
server listens on port 8000.

## CLI flags

- `--env` (required) — path to `envs/legal_search/<env_name>/`.
- `--host` (default `0.0.0.0`)
- `--port` (default `8019`)
- `--debug` — verbose logging.

## Smoke test

```
uv run python servers/legal_search_mock/scripts/smoke_http.py
```

Boots the server against `envs/legal_search/labor_dispute_2026`, round-trips
several tools (incl. a `CASE_NOT_FOUND` error path), and prints `PASS`/`FAIL`.

## Errors

Every tool returns `{"error": <msg>, "code": <code>}` on failure. Stable codes:

- `BAD_ARG` — missing/invalid argument (bad enum, limit < 1, …).
- `BAD_DATE` — date not parseable as `YYYY-MM-DD`.
- `CASE_NOT_FOUND` — unknown `case_id`.
- `STATUTE_NOT_FOUND` — unknown `statute_id`.
- `ARTICLE_NOT_FOUND` — unknown `article_id`.
- `COURT_NOT_FOUND` — unknown `court_id`.
- `SAVED_CASE_NOT_FOUND` — no saved entry for the given user/case.
