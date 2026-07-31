# job_board_mock — Specification

Status: v1 (implementer-facing)
Scope: implementation spec for the `job-board-mock` MCP server.

## 1. Purpose

`job_board_mock` is a self-contained, fully-offline mock of a job board
(job-seeker side) — companies, job postings, resumes, saved jobs,
applications, recruiter chat, and job alerts. It exists so benchmark tasks can
exercise an agent's ability to search jobs, read postings/companies, manage
resumes, bookmark and apply to jobs, talk to recruiters, and react to
deterministic state changes (application status, recruiter replies) the task
orchestrator injects via out-of-band SQL mutations.

The server makes **no** network calls and ships **no** bundled seed data —
state enters only through the env-directory `init.sql` script.

Non-goals:

- No recruiter/employer side (no posting/editing jobs, no candidate review).
- No real ATS workflow. Application status only advances via out-of-band
  mutations; the seeker cannot self-promote an application.
- No authentication. Identity is whatever the caller passes as `user_id`.
- No multi-currency FX (CNY held constant per env). No i18n.

## 2. Stack

- Python ≥ 3.12, stdlib `sqlite3`, `fastmcp ≥ 2.10.5`, `mcp[cli] ≥ 1.11.0`.
- No network libraries in the package.
- Transport: **streamable-HTTP only** at path `/mcp`. No stdio.
- Determinism: no clock, no RNG, no uuid. IDs come from a `_counters` table.

## 3. Tools

All tools are `async def`, return `json.dumps(result, ensure_ascii=False)`,
and surface errors as `{"error": "...", "code": "..."}` rather than raising
across the MCP boundary. Salary is integer minor units (分/cents) of **monthly**
base pay. Dates are ISO `YYYY-MM-DD`; timestamps are ISO-8601 `...Z`. IDs are
domain-prefixed strings.

### 3.1 `search_jobs(keyword?, city?, category?, min_salary_minor?, experience?, education?, sort?, limit?) -> str`

Searches `status='open'` jobs. `keyword` LIKE-matches title/jd/requirements/tags.
`city`/`category` exact match. `min_salary_minor` keeps jobs whose
`salary_max_minor >= min_salary_minor`. `experience` ∈
{`intern`,`fresh_grad`,`1-3`,`3-5`,`5-10`,`10+`}; `education` ∈
{`unlimited`,`college`,`bachelor`,`master`,`phd`}; `sort` ∈
{`relevance`,`salary_desc`,`salary_asc`,`newest`} (default `relevance`, which
orders newest-first deterministically). `limit` default 20, max 100. Returns a
list of compact job summaries:

```json
[
  {"job_id": "job_0001", "title": "后端工程师（Java）", "company_id": "comp_pdd",
   "company_name": "拼多多", "city": "上海", "category": "backend",
   "salary_min_minor": 3500000, "salary_max_minor": 6000000, "salary_months": 16,
   "experience": "3-5", "education": "bachelor", "tags": "Java,分布式,高并发,微服务",
   "status": "open", "posted_at": "2026-05-12"}
]
```

### 3.2 `get_job(job_id) -> str`

Full job detail (summary fields + `jd`, `requirements`). Errors `JOB_NOT_FOUND`.

### 3.3 `get_company(company_id) -> str`

```json
{"company_id": "comp_pdd", "name": "拼多多", "industry": "电商",
 "size": "10000人以上", "stage": "上市", "city": "上海", "intro": "...",
 "rating": 3.6, "open_job_count": 4}
```

Errors `COMPANY_NOT_FOUND`.

### 3.4 `get_recommended_jobs(user_id, limit?) -> str`

Ranks open jobs (excluding those already applied to) by deterministic overlap
between the user's most-recently-updated resume skills/headline and each job's
title/tags/requirements; ties keep newest-first order. Each item is a job
summary plus `"match_score": <int>`. `limit` default 10, max 100.

### 3.5 `create_resume(user_id, name, headline, years_exp?, education?, skills?, summary?) -> str`

Creates a resume (`years_exp` default 0, `education` default `bachelor`).
Returns the resume. Errors `BAD_ARG`.

### 3.6 `update_resume(resume_id, name?, headline?, years_exp?, education?, skills?, summary?) -> str`

Partial update (only non-null fields), bumps `updated_at`. Errors
`RESUME_NOT_FOUND`, `BAD_ARG` (no fields).

### 3.7 `list_resumes(user_id) -> str` / `3.8 get_resume(resume_id) -> str`

List (newest-updated first) / fetch one. `get_resume` errors `RESUME_NOT_FOUND`.

```json
{"resume_id": "resume_li_wei_swe", "user_id": "usr_li_wei", "name": "李伟",
 "headline": "后端工程师", "years_exp": 4, "education": "bachelor",
 "skills": "Java,Go,...", "summary": "...", "updated_at": "2026-05-18T09:00:00Z"}
```

### 3.9 `save_job(user_id, job_id) -> str` / `3.10 unsave_job(...)` / `3.11 list_saved_jobs(user_id)`

`save_job` is idempotent (`{"saved": true, "saved_at": ...}`); errors
`JOB_NOT_FOUND`. `unsave_job` returns `{"saved": false, "removed": <bool>}`.
`list_saved_jobs` returns job summaries each with a `saved_at`.

### 3.12 `apply_job(user_id, job_id, resume_id, cover_letter?) -> str`

Creates an application at status `submitted`. Errors `JOB_NOT_FOUND`,
`JOB_CLOSED` (job not open), `RESUME_OWNERSHIP` (resume not owned by user),
`ALREADY_APPLIED` (one application per user+job). Returns the application.

### 3.13 `list_applications(user_id, status_filter?) -> str` / `3.14 get_application_status(application_id)`

```json
{"application_id": "app_li_0001", "user_id": "usr_li_wei", "job_id": "job_0001",
 "job_title": "后端工程师（Java）", "company_name": "拼多多",
 "resume_id": "resume_li_wei_swe", "cover_letter": "...", "status": "interview",
 "applied_at": "2026-05-13T09:30:00Z", "updated_at": "2026-05-19T14:00:00Z"}
```

`status` ∈ {`submitted`,`viewed`,`interview`,`offer`,`rejected`}.
`get_application_status` errors `APPLICATION_NOT_FOUND`.

### 3.15 `chat_with_recruiter(user_id, job_id, message) -> str`

Appends a `user` message to the thread for (user, job), creating the thread on
first contact. The recruiter does not auto-reply. Errors `JOB_NOT_FOUND`.

### 3.16 `list_chats(user_id) -> str`

Threads (most recently active first), each with full `messages` (sender ∈
{`user`,`recruiter`}) in chronological order.

### 3.17 `subscribe_job_alert(user_id, query_json) -> str`

Saves a search alert; `query_json` must be a valid JSON string of filters.
Errors `BAD_ARG` if not valid JSON.

## 4. Data model (tables)

`companies`, `jobs` (FK company), `resumes`, `saved_jobs` (PK user+job, FK job),
`applications` (FK job, resume; status enum), `chats` (FK job, company) +
`chat_messages` (FK chat; sender enum), `job_alerts`, `_counters`. Salaries in
integer minor units (monthly). See `backends/db.py` for the authoritative DDL.

## 5. Error-code contract

`JOB_NOT_FOUND`, `COMPANY_NOT_FOUND`, `RESUME_NOT_FOUND`,
`APPLICATION_NOT_FOUND`, `CHAT_NOT_FOUND`, `JOB_CLOSED`, `ALREADY_APPLIED`,
`RESUME_OWNERSHIP`, `BAD_DATE`, `BAD_ARG`.
