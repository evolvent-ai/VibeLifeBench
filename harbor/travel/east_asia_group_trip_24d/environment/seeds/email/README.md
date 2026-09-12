# email_mock — east_asia_group_trip_24d

## Key IDs

| Item | ID | Notes |
|------|----|-------|
| Tokyohotelconfirmemail | `email_id: "1"` |     INBOX，S19 lost property    |

##     

- **  **: Booking Confirmation - Shinjuku Grand Hotel (Ref: HB-TYO-2026-8841)
- **   **: INBOX
- **  people**: li.ting@mock.local
- **    **:
  - hotel  : +81-3-5322-1234
  - lost property   : +81-3-5322-1299
  -   : lostandfound@shinjuku-grand.example.com
  - check-in 2026-06-05 / check-out 2026-06-08

## S19   

Agent      INBOX   hotel  email， email   found Lost & Found     ，    email       hotel  lost property 。

   agent    `search_emails(query="Shinjuku")`   `get_emails(folder="INBOX")` found email，    `read_email(email_id="1")`       。

## Schema（   ）

- `emails(id, message_id, folder, from_addr, to_addr, cc_addr, bcc_addr, subject, body_text, body_html, date, is_read, is_important)`
- account  : `user@mock.local`
