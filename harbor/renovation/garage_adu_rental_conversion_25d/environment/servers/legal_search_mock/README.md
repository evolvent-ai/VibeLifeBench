# legal-search-mock

A FastMCP-based, fully-offline mock of a national judgements database + statute database
(Chinese legal research: case judgments + statutes + citations). Runs over
**streamable-HTTP** (no stdio) with a local SQLite database.

All party names are anonymized (placeholder style, e.g. Zhang A / Li B); all judgment text is
original/synthesized and statute text is simplified public-domain-style
(the Labour Contract Law and Labour Law are public domain). There is **no clock, no RNG, no CLI** —
issued IDs come from a `_counters` table, and state changes mid-task arrive as
out-of-band SQL mutations from the orchestrator (the server is oblivious).

The package ships **schema-only**; all rows enter via the env directory's
`init.sql`.

## Tools (agent-facing)

Cases (case judgments):
- `search_cases(keyword?, court?, case_type?, date_from?, date_to?, limit?=20)` — search judgments, newest first; `case_type` values are corpus data defined by the task's seed; `court` accepts a court_id or a court-name substring; dates `YYYY-MM-DD`; `limit` 1–100.
- `get_case(case_id)` — full judgment: anonymized parties, cause of action, facts, reasoning, holding, disposition, outcome and keywords.
- `get_similar_cases(case_id, limit?=5)` — same `case_type`, ranked by shared-keyword overlap then recency; `limit` 1–50.
- `get_case_citations(case_id)` — `statutes_cited` (statute articles) + `cases_cited` (referenced judgments).

Statutes:
- `search_statutes(keyword?, limit?=20)` — search statutes by name, short name or summary; `limit` 1–100.
- `get_statute(statute_id)` — statute metadata + `article_count`; `status` is corpus data, reported verbatim.
- `list_statute_articles(statute_id)` — articles in document order (id/article_no/heading).
- `get_article(article_id)` — full text of one article + statute_name/article_no.

Courts:
- `list_courts()` — all courts and arbitration commissions (id/name/level/region); `level` is corpus data, reported verbatim.
- `get_court(court_id)` — one court + `case_count`.

Library (per-user saved cases):
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
