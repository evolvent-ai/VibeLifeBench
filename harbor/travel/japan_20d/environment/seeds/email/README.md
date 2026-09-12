# li_wei_inbox

Single-user personal Gmail-style snapshot used by the benchmark.

## What this env represents

- **User**: `usr_li_wei` — Li Wei (Li Wei), a Shanghai-based individual.
- **Account**: `li.wei@gmail.com` (display name `Li Wei (Li Wei)`).
- **Reference date**: 2026-05-01. Inbox spans Feb 18 – Apr 30 2026;
  the server has no runtime clock.

## Folders

| folder_id | name      | total | unread |
| --------- | --------- | ----- | ------ |
| 1         | `INBOX`   | 24    | 4      |
| 2         | `Sent`    | 3     | 0      |
| 3         | `Drafts`  | 0     | 0      |
| 4         | `Trash`   | 0     | 0      |
| 5         | `Spam`    | 0     | 0      |
| 6         | `Family`  | 2     | 0      |
| 7         | `Receipts`| 2     | 0      |

System folders (`INBOX`, `Sent`, `Drafts`, `Trash`, `Spam`) are always
present even without a seed; `Family` and `Receipts` are custom folders
specific to this env.

## Inbox themes

- **Family** (Mom Zhang Fang, Dad Li Jianguo, Sister translated content): casual updates,
  health note about Dad, May-1 trip planning, May-1 menu request.
  Sister's trip-planning thread spans an INBOX message and a Sent reply.
- **Bank** (`statements@cmbchina.com` / `notify@cmbchina.com`):
  monthly credit-card statements, salary deposit notification, March
  account statement. The April 10 credit-card statement (id `18`) is
  **unread** and marked important — payment is due 2026-04-20.
- **Shopping receipts** (`jd.com`, `taobao.com`, `meituan.com`,
  `ele.me`): order-shipped / order-paid / order-completed receipts.
- **Work** (`bytecorp.com`): Q2 planning meeting confirmation, PR
  review request, 1:1 weekly notes, all-hands notice, **unread**
  Q1 perf-review reminder (id `21`) with a deadline of 2026-04-24.
- **Newsletter**: ThoughtWorks Tech Radar + InfoQ weekly digest.

Two folder-level archives sit alongside INBOX:

- `Family` — older mom-asks (translated content, dad's birthday) from late Feb.
- `Receipts` — older AirPods + translated content receipts from late Feb.

## How to load

```bash
email-mock \
  --env ../../envs/email/li_wei_inbox \
  --host 0.0.0.0 --port 8000
```

Or via Docker:

```bash
docker run --rm -p 8000:8000 \
  -v "$PWD/envs/email/li_wei_inbox:/env-seed:ro" \
  vibe-agent-benchmark/email_mock:latest
```

## Notes for benchmark authors

- All message IDs are stable integers (`1..31`) — tasks can reference them.
- `is_read=0` only on ids `18`, `21`, `22`, `24` (1 bank, 1 work, 1
  newsletter, 1 family). Total `unread_count = 4` in INBOX.
- `is_important=1` is set on the two unread items that genuinely need
  attention (id `18`, `21`) plus id `15` (Dad's checkup result) and
  id `20` (Sister's trip ticket confirmation request).
- `account_config.email = li.wei@gmail.com` — outgoing mail from this
  env will show this address as `From:`.
