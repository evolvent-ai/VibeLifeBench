# email-mock — Implementer-facing Spec

This document describes the SQLite-backed mock email server. The agent-facing
tool surface mirrors the upstream `emails-mcp` package so existing benchmark
tasks keep working — but the backend has been swapped from PostgreSQL +
IMAP/SMTP to pure SQLite, and the transport is streamable-HTTP only.

## 1. Process model

- One server process per env.
- Transport: `streamable-http` only. Endpoint: `http://<host>:<port>/mcp`.
- Terrarium/Docker runs the server on container port **8000**.
- No stdio fallback. No `--transport` flag.
- No admin tool / no clock. Stage-driven row changes are applied by the
  orchestrator's event-overlay channel directly against `runtime.db`.

## 2. CLI

```
email-mock [--host 0.0.0.0] [--port 8000]
           --env <env_dir> [--debug]
```

State injection:

- On cold start the server writes a fresh `<env>/runtime.db`, applies the
  bundled schema, then executes `<env>/init.sql` if present.
- The package ships no bundled seed data; the empty env at
  `envs/email/empty/` boots a stateless instance.

## 3. Schema

All tables are flat (no PG-style schema prefix). The shape mirrors the
upstream PG `email.*` schema for parity with existing seed files.

### account_config

| col          | type | notes                                |
| ------------ | ---- | ------------------------------------ |
| id           | INT  | PK, autoincrement                    |
| email        | TEXT | configured `From:` address            |
| name         | TEXT | display name                         |
| created_at   | TEXT | ISO-8601 UTC `Z`                     |

A single row is expected; the first row's `email` is used as `From:` on
all outgoing messages.

### folders

| col            | type | notes                                  |
| -------------- | ---- | -------------------------------------- |
| id             | INT  | PK, autoincrement                      |
| name           | TEXT | unique                                 |
| delimiter      | TEXT | default `/`                            |
| flags_json     | TEXT | JSON array (currently informational)   |
| message_count  | INT  | denormalised, refreshed on writes      |
| unread_count   | INT  | denormalised, refreshed on writes      |

System folders (`INBOX`, `Sent`, `Drafts`, `Trash`, `Spam`) are
auto-created on every server start so a fresh-container call to
`get_emails(INBOX)` returns an empty list rather than `FOLDER_NOT_FOUND`.
Deletion of those names is rejected with `FOLDER_PROTECTED`.

### messages

| col                | type | notes                                                          |
| ------------------ | ---- | -------------------------------------------------------------- |
| id                 | INT  | PK, autoincrement; exposed to agents as `email_id` (string)    |
| folder_id          | INT  | FK → folders.id (ON DELETE CASCADE)                            |
| message_id         | TEXT | RFC-5322 `Message-ID:` value                                   |
| subject            | TEXT |                                                                |
| from_addr          | TEXT |                                                                |
| to_addr_json       | TEXT | JSON array of addresses                                        |
| cc_addr_json       | TEXT | JSON array of addresses                                        |
| bcc_addr_json      | TEXT | JSON array of addresses                                        |
| date               | TEXT | ISO-8601 (env data may use date-only `YYYY-MM-DD`)             |
| body_text          | TEXT |                                                                |
| body_html          | TEXT |                                                                |
| is_read            | INT  | 0/1                                                            |
| is_important       | INT  | 0/1                                                            |
| is_flagged         | INT  | 0/1                                                            |
| in_reply_to        | TEXT |                                                                |
| references_header  | TEXT |                                                                |
| headers_json       | TEXT | JSON object — raw headers map for `get_email_headers`          |
| uid                | INT  | optional UID (parity with IMAP)                                |
| size               | INT  | approximate byte size                                          |
| created_at         | TEXT | ISO-8601 UTC `Z`                                               |

### attachments

| col           | type | notes                                                  |
| ------------- | ---- | ------------------------------------------------------ |
| id            | INT  | PK, autoincrement                                      |
| message_id    | INT  | FK → messages.id (ON DELETE CASCADE)                   |
| filename      | TEXT |                                                        |
| content_type  | TEXT | default `application/octet-stream`                     |
| size          | INT  | bytes                                                  |
| content_b64   | TEXT | base64-encoded payload (or NULL for placeholder rows)  |
| content_id    | TEXT | optional Content-ID                                    |

### drafts

| col            | type | notes                                            |
| -------------- | ---- | ------------------------------------------------ |
| id             | INT  | PK; exposed to agents as `draft_id` (string)     |
| subject        | TEXT |                                                  |
| from_addr      | TEXT | usually `account_config.email`                   |
| to_addr_json   | TEXT |                                                  |
| cc_addr_json   | TEXT |                                                  |
| bcc_addr_json  | TEXT |                                                  |
| body_text      | TEXT |                                                  |
| body_html      | TEXT |                                                  |
| in_reply_to    | TEXT |                                                  |
| created_at     | TEXT | ISO-8601 UTC `Z`                                 |
| updated_at     | TEXT | ISO-8601 UTC `Z`                                 |

### sent_log

| col           | type | notes                                            |
| ------------- | ---- | ------------------------------------------------ |
| id            | INT  | PK                                               |
| message_id    | INT  | FK → messages.id (ON DELETE SET NULL)            |
| sent_at       | TEXT | ISO-8601 UTC `Z`                                 |

A row is inserted every time `send_email` / `reply_email` / `forward_email`
files a message in the `Sent` folder.

### _counters

`(key, value)` pairs. `msg_seq` drives generated Message-ID headers for
new outbound mail. Leading underscore signals "control table, not part
of the agent-visible domain".

The server never reads a notion of "today" in any tool path; dates are
baked into init.sql rows.

## 4. Tools

Every tool is `async def`, returns `json.dumps(...)`, and never raises
across the MCP boundary. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — see Appendix A for codes.

### Read

- `get_emails(folder="INBOX", page=1, page_size=20) → SearchPage` —
  metadata only, newest first.
- `read_email(email_id) → EmailDetail` — includes body + attachments;
  marks the message as read.
- `search_emails(query, folder=None, page=1, page_size=20) → SearchPage` —
  case-sensitive substring search on subject/from/body. Limits to one
  folder if `folder` is supplied; otherwise searches across all folders.
- `get_email_headers(email_id) → HeaderInfo` — Message-ID, In-Reply-To,
  References, and the raw `headers_json` map.

### Send

- `send_email(to, subject, body, html_body=None, cc=None, bcc=None)` —
  inserts a row in `Sent` and `sent_log`. Returns the new `email_id`.
- `reply_email(email_id, body, html_body=None, cc=None, bcc=None,
  reply_all=False)` — quotes the original, stamps `in_reply_to`. With
  `reply_all=True`, the original's To+CC are added to the reply CC
  (minus our own address).
- `forward_email(email_id, to, body=None, html_body=None, cc=None,
  bcc=None)` — copies original attachments onto the new message.

### Mutate

- `delete_email(email_id)` / `delete_emails(email_ids[])`
- `move_email(email_id, target_folder)` / `move_emails(email_ids[],
  target_folder)` — target folder is auto-created.
- `mark_emails(email_ids[], status)` — status ∈ {`read`, `unread`,
  `important`, `not_important`}.

### Folder

- `get_folders()` — list with denormalised counts (refreshed on every call).
- `create_folder(folder_name)` — rejects collisions with `FOLDER_EXISTS`.
- `delete_folder(folder_name)` — refuses system folders with
  `FOLDER_PROTECTED`. Cascades into messages + attachments.
- `get_mailbox_stats(folder_name=None)` — per-folder or aggregate.
- `get_unread_count(folder_name=None)` — per-folder or aggregate.

### Drafts

- `save_draft(subject, body, html_body=None, to=None, cc=None,
  bcc=None)` — returns `{draft_id, created_at, updated_at}`.
- `get_drafts(page=1, page_size=20)` — most-recently-updated first.
- `update_draft(draft_id, ...)` — patch in place; only supplied fields change.
- `delete_draft(draft_id)`.

### I/O & management

- `check_connection()` — always ok in the mock.
- `download_attachment(email_id, attachment_filename, download_path=None)` —
  decodes `content_b64` to bytes, writes to disk. Collisions become
  `<name>(1)<ext>`, `<name>(2)<ext>`, …
- `export_emails(folder=None, export_path="emails_export.json",
  max_emails=None, export_all_folders=False)` — writes a JSON file with
  attachments inlined as base64.
- `import_emails(import_path, target_folder=None,
  preserve_folders=True)` — reads such a file. Folders that don't exist
  are auto-created.

## 5. Address handling

The wire protocol uses comma-separated strings for `to` / `cc` / `bcc`
because that's what the upstream tool surface exposes. Internally the
service splits/joins on commas and stores a JSON array
(`to_addr_json` etc) so the underlying schema remains structured. The
helpers live in `utils/addrs.py`.

## 6. Pagination

All list-style tools accept `page` (1-based) and `page_size`. Defaults:
20. Clamped to `[1, 50]`. Pages past the last page return the last page
(never empty unless the folder is empty).

## 7. What this server does NOT do

- No real IMAP / SMTP. Outgoing mail just lands in `Sent`.
- No attachment upload (i.e. no upload via MCP — attachments arrive via
  `init.sql` or `import_emails`).
- No path-restriction sandbox on `download_attachment` / `export_emails` /
  `import_emails`. The harness controls the filesystem the server can see.
- No multi-account routing. One process = one `account_config`.
- No pagination beyond `page` / `page_size`.

## Appendix A — Error codes

| code                   | when                                                         |
| ---------------------- | ------------------------------------------------------------ |
| `BAD_ARG`              | missing / wrong-type argument                                |
| `VALIDATION_ERROR`     | argument fails a more nuanced validator                      |
| `EMAIL_NOT_FOUND`      | no message row with that id                                  |
| `FOLDER_NOT_FOUND`     | folder lookup by name failed                                 |
| `FOLDER_EXISTS`        | `create_folder` collision                                    |
| `FOLDER_PROTECTED`     | tried to delete a system folder                              |
| `DRAFT_NOT_FOUND`      | no draft row with that id                                    |
| `ATTACHMENT_NOT_FOUND` | filename not present on that message                         |
| `FILE_ERROR`           | export/import/download disk error                            |
