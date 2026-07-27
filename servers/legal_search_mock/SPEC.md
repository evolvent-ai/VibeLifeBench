# legal_search_mock — implementer SPEC

## Purpose

Offline mock of Chinese legal research (裁判文书网 + 国家法律法规检索): search and
read anonymized case judgments, browse statutes and their articles, follow
citations from a case to the statute articles / cases it relies on, and maintain
a per-user saved-case library with notes. Powers the 打官司 (litigation prep)
benchmark scenario.

## Non-goals

- No legal advice, outcome prediction, or document drafting.
- No clock / RNG / uuid / admin CLI. IDs come from `_counters`.
- No bundled seed data — all rows arrive via the env `init.sql`.
- No reproduction of copyrighted text; judgments are synthesized, statutes are
  simplified public-domain text.

## Stack

FastMCP (`mcp.server.fastmcp`) over streamable-HTTP at `/mcp`; stdlib `sqlite3`
(autocommit, WAL, `foreign_keys=ON`). Layering: `tools/` → `services/` →
`backends/db` + `utils/`. All tool returns are `json.dumps(..., ensure_ascii=False)`
strings.

## Tables

- `courts(court_id PK, name, level∈{基层法院,中级法院,高级法院,最高法院,仲裁委员会}, region)`
- `cases(case_id PK, case_number, title, court_id→courts, case_type∈{劳动争议,合同纠纷,侵权责任,婚姻家庭,劳动仲裁,其他}, cause, judgment_date(YYYY-MM-DD), parties(anonymized), summary, facts, reasoning, holding, ruling, outcome∈{支持,部分支持,驳回,调解,其他}, keywords(comma-joined))`
- `statutes(statute_id PK, name, short_name, issuer, effective_date, status∈{现行有效,已修订,已废止}, summary)`
- `statute_articles(article_id PK, statute_id→statutes, article_no, seq, heading, text)`
- `citations(citation_id PK, case_id→cases, target_type∈{article,case}, target_id, label)`
- `saved_cases(saved_id PK, user_id, case_id→cases, note nullable, saved_at); UNIQUE(user_id,case_id)`
- `_counters(key PK, value)` — keys: `saved_seq`, `citation_seq`.

## Tools — request → response

### search_cases
Req: `{keyword?, court?, case_type?, date_from?, date_to?, limit?=20}`
Res: `[{case_id, case_number, title, court_id, court_name, case_type, cause, judgment_date, outcome, summary}]` (newest first).
Errors: `BAD_ARG` (limit<1, bad case_type), `BAD_DATE`.

### get_case
Req: `{case_id}` → `{case_id, case_number, title, court_id, court_name, case_type, cause, judgment_date, parties, summary, facts, reasoning, holding, ruling, outcome, keywords:[...]}`.
Errors: `CASE_NOT_FOUND`.

### get_similar_cases
Req: `{case_id, limit?=5}` → `[<case summary> + {shared_keyword_count}]`, same case_type, sorted by overlap desc then recency.
Errors: `CASE_NOT_FOUND`, `BAD_ARG`.

### get_case_citations
Req: `{case_id}` → `{case_id, statutes_cited:[{citation_id, article_id, article_no, statute_id, statute_name, label}], cases_cited:[{citation_id, case_id, case_number, title, label}]}`.
Errors: `CASE_NOT_FOUND`.

### search_statutes
Req: `{keyword?, limit?=20}` → `[{statute_id, name, short_name, issuer, effective_date, status, summary}]`.
Errors: `BAD_ARG`.

### get_statute
Req: `{statute_id}` → statute fields + `{article_count}`.
Errors: `STATUTE_NOT_FOUND`.

### list_statute_articles
Req: `{statute_id}` → `[{article_id, statute_id, article_no, heading}]` (doc order).
Errors: `STATUTE_NOT_FOUND`.

### get_article
Req: `{article_id}` → `{article_id, statute_id, statute_name, article_no, heading, text}`.
Errors: `ARTICLE_NOT_FOUND`.

### list_courts / get_court
`list_courts()` → `[{court_id, name, level, region}]`.
`get_court(court_id)` → court fields + `{case_count}`. Errors: `COURT_NOT_FOUND`.

### save_case / list_saved / add_note_to_case
`save_case(user_id, case_id)` → `{saved_id, user_id, case_id, note, saved_at}` (idempotent; re-save returns existing). Errors: `CASE_NOT_FOUND`, `BAD_ARG`.
`list_saved(user_id)` → `[{saved_id, user_id, case_id, note, saved_at, case:<summary>}]` (oldest first). Errors: `BAD_ARG`.
`add_note_to_case(user_id, case_id, note)` → updated saved entry; auto-saves first if absent. Errors: `CASE_NOT_FOUND`, `BAD_ARG`.

## Error-code contract

`BAD_ARG`, `BAD_DATE`, `CASE_NOT_FOUND`, `STATUTE_NOT_FOUND`,
`ARTICLE_NOT_FOUND`, `COURT_NOT_FOUND`, `SAVED_CASE_NOT_FOUND`.
All surfaced as `{"error": <msg>, "code": <code>}`.
