# job-board-mock

A FastMCP-based, fully-offline mock of a job board (Boss直聘 / 猎聘 / LinkedIn,
job-seeker side). Runs over **streamable-HTTP** (no stdio) with a local SQLite
database. Salaries are stored as integer 分 (cents) of *monthly* base pay; the
example env uses CNY.

See [SPEC.md](./SPEC.md) for the full implementer-facing specification.

## Tools (agent-facing)

- `search_jobs(keyword?, city?, category?, min_salary_minor?, experience?, education?, sort?, limit?)`
- `get_job(job_id)` — JD, requirements, monthly salary range (分) over `salary_months`.
- `get_company(company_id)` — profile + open job count.
- `get_recommended_jobs(user_id, limit?)` — ranked by resume/skill overlap.
- `create_resume(user_id, name, headline, years_exp?, education?, skills?, summary?)`
- `update_resume(resume_id, name?, headline?, years_exp?, education?, skills?, summary?)`
- `list_resumes(user_id)` / `get_resume(resume_id)`
- `save_job(user_id, job_id)` / `unsave_job(user_id, job_id)` / `list_saved_jobs(user_id)`
- `apply_job(user_id, job_id, resume_id, cover_letter?)`
- `list_applications(user_id, status_filter?)` / `get_application_status(application_id)`
- `chat_with_recruiter(user_id, job_id, message)` / `list_chats(user_id)`
- `subscribe_job_alert(user_id, query_json)`

The server has no simulated clock and no management CLI. Stage-driven state
changes (application status advancing, recruiter replies) are applied as SQL
mutations by the task orchestrator.

## Quick start

```bash
# From this directory
pip install -e .

# Run with an env directory.
job-board-mock \
  --port 8018 \
  --env ../../envs/job_board/swe_shanghai_2026
```

On startup the server unlinks any `<env>/runtime.db`, creates the schema,
executes `<env>/init.sql` if present, and binds streamable-HTTP at
`http://<host>:<port>/mcp`.

## CLI flags

- `--env PATH` — required; path to an `envs/<server>/<env_name>/` directory.
- `--host` (default `0.0.0.0`)
- `--port` (default `8018`; pass `8000` for Docker/Terrarium parity)
- `--debug` — verbose logging.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Spins up the server in a subprocess against `envs/job_board/swe_shanghai_2026`
and round-trips `search_jobs`, `get_job`, `list_saved_jobs`, `apply_job`,
`list_chats`, plus an `apply_job` against a closed job expecting `JOB_CLOSED`.
Prints `PASS` or `FAIL`.

## Errors

Every tool returns valid JSON. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — never as exceptions. Stable codes:

`JOB_NOT_FOUND`, `COMPANY_NOT_FOUND`, `RESUME_NOT_FOUND`,
`APPLICATION_NOT_FOUND`, `CHAT_NOT_FOUND`, `JOB_CLOSED`, `ALREADY_APPLIED`,
`RESUME_OWNERSHIP`, `BAD_DATE`, `BAD_ARG`.
