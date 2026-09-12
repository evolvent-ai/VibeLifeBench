# chen_yu_inbox

Single-user personal email snapshot for the Bali 22-day benchmark task.

## What this env represents

- **User**: `usr_chen_yu` -- Chen Yu, Shanghai-based backend engineer.
- **Account**: `chen.yu@gmail.com` (display name `Chen Yu`).
- **Reference date**: 2026-06-01. Inbox spans Apr-May 2026.

## Folders

| folder_id | name | total | unread |
|-----------|------|-------|--------|
| 1 | INBOX | 15 | 3 |
| 2 | Sent | 2 | 0 |
| 3 | Drafts | 0 | 0 |
| 4 | Trash | 0 | 0 |
| 5 | Spam | 0 | 0 |
| 6 | Travel | 2 | 0 |

## Inbox themes

- **Work** (gaming company): sprint planning, code review request,
  game launch timeline
- **Family**: wife's prenatal checkup reminder, mother asking about
  trip logistics
- **Travel**: Garuda Indonesia booking confirmation, AXA insurance quote
- **Bank**: monthly statement notification
- **Unread**: insurance quote, code review, mother's message

## How to load

```bash
email-mock \
  --env ../../envs/email/chen_yu_inbox \
  --host 0.0.0.0 --port 8000
```
