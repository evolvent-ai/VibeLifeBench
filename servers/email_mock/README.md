# email-mock

A FastMCP-based, fully-offline mock email server. Runs over **streamable-HTTP**
(no stdio, no IMAP, no SMTP) with a local SQLite database — outgoing mail is
filed in the `Sent` folder and logged in `sent_log`.

See [SPEC.md](./SPEC.md) for the full implementer-facing specification.

## Tools (agent-facing, 24 total)

| group           | tools                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------- |
| read            | `get_emails`, `read_email`, `search_emails`, `get_email_headers`                            |
| send            | `send_email`, `reply_email`, `forward_email`                                                |
| mutate          | `delete_email`, `delete_emails`, `move_email`, `move_emails`, `mark_emails`                 |
| folder          | `get_folders`, `create_folder`, `delete_folder`, `get_mailbox_stats`, `get_unread_count`    |
| draft           | `save_draft`, `get_drafts`, `update_draft`, `delete_draft`                                  |
| io / mgmt       | `check_connection`, `download_attachment`, `export_emails`, `import_emails`                 |

No management tool is exposed over MCP. Stage-driven row changes flow through the orchestrator's
event-overlay channel, which executes SQL directly against the server's
`runtime.db`.

## Quick start

### Direct (Python)

```bash
# From this directory
pip install -e .

# Run against the bundled env.
email-mock \
  --port 8000 \
  --env ../../envs/email/li_wei_inbox
```

The server writes a fresh `runtime.db` inside the env directory on every
cold start, applies the bundled schema, then executes
`<env>/init.sql` if present.

### Docker

```bash
docker build -t vibe-agent-benchmark/email_mock:latest .
docker run --rm -p 8000:8000 \
  -v $PWD/../../envs/email/li_wei_inbox:/env-seed:ro \
  vibe-agent-benchmark/email_mock:latest
```

The streamable-HTTP endpoint is at `http://<host>:<port>/mcp`.

## CLI flags

- `--host` (default `0.0.0.0`)
- `--port` (pass `8000` for Docker/Terrarium parity)
- `--env PATH` — env directory (`runtime.db` lives inside; optional `init.sql` is applied)
- `--debug` — verbose logging

To boot stateless, point `--env` at `../../envs/email/empty`.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Spins up the server in a subprocess on a free port, applies
`envs/email/li_wei_inbox/init.sql`, and round-trips `check_connection`,
`get_folders`, `get_emails`, `search_emails`, and `send_email`. Prints
`PASS` or `FAIL`.

## Errors

Every tool returns valid JSON. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — never as exceptions. Stable codes:

`EMAIL_NOT_FOUND`, `FOLDER_NOT_FOUND`, `FOLDER_EXISTS`,
`FOLDER_PROTECTED`, `DRAFT_NOT_FOUND`, `ATTACHMENT_NOT_FOUND`,
`VALIDATION_ERROR`, `FILE_ERROR`, `BAD_ARG`.

## Migration Note

This package was migrated from a Postgres + IMAP/SMTP facade to pure
SQLite + streamable-HTTP. Removed: psycopg2, IMAP fallback, SMTP
fallback, `--config_file`, attachment upload/download path restrictions,
all `print()` statements. Schema mirrors the upstream `email.*` PG
schema but flattened (no schema prefix).
