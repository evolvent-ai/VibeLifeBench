# content-platform-mock

A FastMCP-based, fully-offline mock of a 小红书/XHS-style UGC content community —
notes (笔记), comments, users, topics (话题), and the like/collect/follow social
graph. Runs over **streamable-HTTP** (no stdio) with a local SQLite database.
This is the namesake server of the vibe-agent-benchmark repo.

Images are **text captions only** (`image_captions`) — the server is fully
offline and stores no binaries. Engagement counts are plain integers.

See [SPEC.md](./SPEC.md) for the full implementer-facing specification.

## Tools (agent-facing)

Notes:
- `search_notes(keyword, category?, sort?, limit?)` — `sort` ∈ {hot, latest, most_collected}.
- `get_note(note_id)` — title, body, image_captions, tags, author, like/collect/comment/view counts.
- `get_note_comments(note_id, limit?)`
- `post_comment(note_id, user_id, body)`
- `get_trending(category?, limit?)` — ranked by weighted engagement, with a 1-based rank.
- `publish_note(user_id, title, body, tags?, category?, image_captions?)`

Users / social graph:
- `get_user_profile(user_id)`
- `list_user_notes(user_id)`
- `follow_user(user_id, target_user_id)` / `unfollow_user(user_id, target_user_id)`

Engagement:
- `like_note(user_id, note_id)`
- `collect_note(user_id, note_id)` / `uncollect_note(user_id, note_id)`
- `list_collections(user_id)`

Topics:
- `search_topics(keyword)`
- `get_topic_feed(topic, limit?)` — `topic` is the exact topic name.

`category` ∈ {备考, 装修, 健身, 旅行, 母婴, 其他}. `limit` defaults to 20, capped at 100.

The server has no simulated clock and no management CLI. Stage-driven state
changes are applied as SQL mutations by the task orchestrator.

## Quick start

```bash
# From this directory
pip install -e .

# Run with an env directory.
content-mock \
  --port 8015 \
  --env ../../envs/content_platform/xhs_2026q2
```

On startup the server unlinks any `<env>/runtime.db`, creates the schema,
executes `<env>/init.sql` if present, and binds streamable-HTTP at
`http://<host>:<port>/mcp`.

## CLI flags

- `--env PATH` — required; path to an `envs/<server>/<env_name>/` directory.
- `--host` (default `0.0.0.0`)
- `--port` (default `8015` for dev; pass `8000` for Docker/Terrarium parity)
- `--debug` — verbose logging.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Spins up the server in a subprocess against `envs/content_platform/xhs_2026q2`
and round-trips `search_notes`, `get_note`, `get_trending`, `collect_note`,
`list_collections`, `follow_user`, `publish_note`, plus a `get_note` on a missing
id expecting `NOTE_NOT_FOUND`. Prints `PASS` or `FAIL`.

## Errors

Every tool returns valid JSON. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — never as exceptions. Stable codes:

`NOTE_NOT_FOUND`, `USER_NOT_FOUND`, `TOPIC_NOT_FOUND`, `ALREADY_EXISTS`,
`NOT_FOLLOWING`, `NOT_COLLECTED`, `SELF_FOLLOW`, `BAD_DATE`, `BAD_ARG`.
