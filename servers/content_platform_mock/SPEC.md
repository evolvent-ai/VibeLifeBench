# content_platform_mock — Specification

Status: v1 (implementer-facing)
Scope: implementation spec for the `content-platform-mock` MCP server.

## 1. Purpose

`content_platform_mock` is a self-contained, fully-offline mock of a
小红书/XHS-style UGC content community — notes (笔记), comments, users, topics
(话题), and the like/collect/follow social graph. It exists so benchmark tasks
can exercise an agent's ability to discover and read UGC, engage with it (like /
collect / comment / follow), publish notes, and react to deterministic state
changes the orchestrator injects via out-of-band SQL mutations.

The server makes **no** network calls and ships **no** bundled seed data — state
enters only through the env-directory `init.sql` script.

Non-goals:

- No image/video binaries. Notes carry `image_captions` (text descriptions) only.
- No recommendation ML. `get_trending` / `search` ranking is a deterministic
  SQL ordering, not a learned model.
- No authentication. Identity is whatever the caller passes as `user_id`.
- No private/blocked accounts, no DMs, no notifications (see `notification_hub_mock`).
- No i18n.

## 2. Stack

- Python ≥ 3.12, stdlib `sqlite3`, `fastmcp ≥ 2.10.5`, `mcp[cli] ≥ 1.11.0`.
- No network libraries in the package.
- Transport: **streamable-HTTP only** at path `/mcp`. No stdio.

## 3. Tools

All tools are `async def`, return `json.dumps(result, ensure_ascii=False)`, and
surface errors as `{"error": "...", "code": "..."}` rather than raising across
the MCP boundary. Dates are ISO `YYYY-MM-DD`; timestamps are ISO-8601 `Z`. IDs
are domain-prefixed strings (`note_00000001`, `cmt_00000001`, `topic_000001`).
`category` ∈ {备考, 装修, 健身, 旅行, 母婴, 其他}. `limit` defaults to 20, capped at 100.

### 3.1 `search_notes(keyword, category?, sort?, limit?) -> str`

Substring match over `title`/`body`/`tags`. `sort` ∈ {`hot`, `latest`,
`most_collected`} (default `hot`; hot = `likes + 2*collects + 3*comments`).
Returns a list of compact summaries:

```json
[
  {"note_id": "note_00000001", "title": "二战上岸｜...",
   "category": "备考", "author_id": "usr_kaoyan_jiejie",
   "author_nickname": "考研姐姐Anna", "tags": ["考研","时间规划"],
   "like_count": 18420, "collect_count": 26310, "comment_count": 1203,
   "published_at": "2026-02-14"}
]
```

### 3.2 `get_note(note_id) -> str`

```json
{
  "note_id": "note_00000001",
  "title": "...", "body": "...",
  "category": "备考",
  "tags": ["考研","时间规划"],
  "image_captions": ["全年复习甘特图...", "..."],
  "author": {"user_id": "usr_kaoyan_jiejie", "handle": "kaoyan_jiejie",
             "nickname": "考研姐姐Anna", "is_official": false,
             "follower_count": 248300},
  "like_count": 18420, "collect_count": 26310,
  "comment_count": 1203, "view_count": 210400,
  "published_at": "2026-02-14"
}
```

`NOTE_NOT_FOUND` if missing.

### 3.3 `get_note_comments(note_id, limit?) -> str`

Oldest first.

```json
[{"comment_id": "cmt_00000001", "note_id": "note_00000001",
  "user_id": "usr_li_wei", "nickname": "李伟", "body": "...",
  "like_count": 320, "created_at": "2026-02-15T09:12:00Z"}]
```

### 3.4 `post_comment(note_id, user_id, body) -> str`

Inserts a comment and increments the note's `comment_count`.

```json
{"comment_id": "cmt_00000015", "note_id": "note_00000001",
 "user_id": "usr_li_wei", "body": "...", "created_at": "<now>Z"}
```

Errors: `NOTE_NOT_FOUND`, `USER_NOT_FOUND`, `BAD_ARG` (empty body).

### 3.5 `get_trending(category?, limit?) -> str`

Hottest notes by weighted engagement, each with a 1-based `rank` and `view_count`.
Optional category filter.

### 3.6 `publish_note(user_id, title, body, tags?, category?, image_captions?) -> str`

Mints a new `note_id`, increments the author's `note_count`. `tags` and
`image_captions` are string lists; `category` defaults to `其他`.

```json
{"note_id": "note_00000033", "author_id": "usr_li_wei",
 "title": "...", "category": "备考", "tags": ["考研"],
 "image_captions": [], "published_at": "<today>"}
```

Errors: `USER_NOT_FOUND`, `BAD_ARG` (empty title/body, bad category).

### 3.7 `get_user_profile(user_id) -> str`

```json
{"user_id": "usr_li_wei", "handle": "li_wei", "nickname": "李伟",
 "bio": "...", "is_official": false, "follower_count": 128,
 "following_count": 6, "note_count": 0, "joined_at": "2021-04-12T08:00:00Z"}
```

`following_count` is derived from the `follows` table at read time.

### 3.8 `list_user_notes(user_id) -> str`

Compact summaries authored by the user, newest first.

### 3.9 `follow_user(user_id, target_user_id) -> str` / `3.10 unfollow_user(...)`

`follow_user` inserts a `follows` row and bumps the target's `follower_count`;
`unfollow_user` reverses it.

```json
{"follower_id": "usr_li_wei", "followee_id": "usr_kaoyan_jiejie",
 "following": true, "followee_follower_count": 248301}
```

Errors: `SELF_FOLLOW`, `USER_NOT_FOUND`, `ALREADY_EXISTS` (follow),
`NOT_FOLLOWING` (unfollow).

### 3.11 `like_note(user_id, note_id) -> str`

Inserts a `likes` row, bumps `like_count`. Errors: `USER_NOT_FOUND`,
`NOTE_NOT_FOUND`, `ALREADY_EXISTS`.

### 3.12 `collect_note(...)` / `3.13 uncollect_note(...)`

Insert/remove a `collections` row and adjust `collect_count`. Errors:
`USER_NOT_FOUND`, `NOTE_NOT_FOUND`, `ALREADY_EXISTS` (collect),
`NOT_COLLECTED` (uncollect).

### 3.14 `list_collections(user_id) -> str`

Notes the user collected, most-recently-collected first, each with `collected_at`.

### 3.15 `search_topics(keyword) -> str`

Topics by name/description, ranked by `view_count`.

```json
[{"topic_id": "topic_000001", "name": "考研上岸", "category": "备考",
  "description": "...", "note_count": 4, "view_count": 5120000}]
```

### 3.16 `get_topic_feed(topic, limit?) -> str`

`topic` is the exact topic name. Returns topic metadata plus its notes ranked by
engagement. `TOPIC_NOT_FOUND` if the name is unknown.

## 4. Storage

SQLite, one file per server. `PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL`.

| table         | purpose                                                              |
| ------------- | -------------------------------------------------------------------- |
| `users`       | community users / creators; pre-aggregated follower/note counts      |
| `notes`       | UGC notes; `tags` + `image_captions` are JSON-array TEXT columns     |
| `comments`    | comments on notes                                                    |
| `follows`     | directed follower→followee edges                                     |
| `likes`       | (user, note) like edges                                              |
| `collections` | (user, note) collect/收藏 edges                                       |
| `topics`      | topics/话题 with `note_count` + `view_count`                          |
| `note_topics` | note↔topic linkage                                                   |
| `_counters`   | atomic seq counters used to mint stable ids                          |

## 5. State injection

No JSON seed. The server takes `--env <dir>` and on cold start:

1. Unlinks `<env>/runtime.db` (and WAL sidecars).
2. Creates the schema.
3. `executescript`s `<env>/init.sql` if present.
4. Opens streamable-HTTP on `<host>:<port>/mcp`.

The minimal stateless env is `envs/content_platform/empty/`. The rich scenario
env is `envs/content_platform/xhs_2026q2/`.

## 6. State evolution across stages

The task orchestrator drives state changes through `mutation` events in each
task's `event.yaml` — one or more SQL statements against this server's runtime
DB. This server has no management CLI, no sweep loop, and no runtime clock.

## 7. Determinism

- No clock, no RNG, no `uuid4`. New IDs come from `_counters` via `next_counter`.
- `publish_note` / `post_comment` stamp `published_at` (date) / `created_at`
  (timestamp) from wall-clock UTC; tasks that assert on these should match by
  shape, or stage the timestamp via mutation.
- `json.dumps(..., ensure_ascii=False)` so Chinese stays readable.

## 8. Logging & ops

- `logging.getLogger(__name__)` everywhere; handler on stderr only.
- No `print()` in the package.

## 9. Appendix — error codes

| code              | meaning                                                       |
| ----------------- | ------------------------------------------------------------- |
| `NOTE_NOT_FOUND`  | `note_id` does not exist                                      |
| `USER_NOT_FOUND`  | `user_id` / `target_user_id` does not exist                   |
| `TOPIC_NOT_FOUND` | topic name unknown                                            |
| `ALREADY_EXISTS`  | duplicate follow / like / collect                             |
| `NOT_FOLLOWING`   | unfollow when no follow edge exists                           |
| `NOT_COLLECTED`   | uncollect a note not in the user's collection                 |
| `SELF_FOLLOW`     | `user_id` == `target_user_id`                                 |
| `BAD_DATE`        | non-ISO date string                                           |
| `BAD_ARG`         | catch-all for malformed inputs (empty keyword/body, bad enum) |
