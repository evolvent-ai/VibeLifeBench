-- emails-mcp env1_li_wei_inbox — init.sql
-- Li Wei's personal Gmail-style mailbox snapshot.
-- Reference frame: 2026-05-01. ~30 messages spanning Mar-Apr 2026.

BEGIN;

-- Account.
DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES
  (1, 'li.wei@gmail.com', 'Li Wei (Li Wei)', '2018-06-15T00:00:00Z');

-- Folders. System folders are also auto-created on server start, but seeding
-- them here keeps the IDs deterministic for the seeded messages below.
DELETE FROM folders;
INSERT INTO folders (id, name) VALUES
  (1, 'INBOX'),
  (2, 'Sent'),
  (3, 'Drafts'),
  (4, 'Trash'),
  (5, 'Spam'),
  (6, 'Family'),
  (7, 'Receipts');

-- Messages. id is autoincrement; we hand-assign so the env is fully
-- reproducible. body_text only — no HTML in seed data to keep things compact.

-- =========================================================================
-- INBOX (folder_id = 1) — 19 emails through 2026-04-14
-- =========================================================================

-- Family — Mom
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1, 1, '<20260303-mom-001@family.local>', 'translated content，translated content', 'Zhang Fang <zhangfang.mom@163.com>', '["li.wei@gmail.com"]', '2026-03-03T07:12:00Z',
   'translated content，translated content，translated content。translated content，translated content。translated content，translated content。 — translated content', 1, 0, '{}', 180, '2026-03-03T07:12:00Z');

-- Bank statement
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (2, 1, '<20260305-cmb-statement@cmbchina.com>', '【translated content】2026translated content2translated content', 'statements@cmbchina.com', '["li.wei@gmail.com"]', '2026-03-05T09:00:00Z',
   'translated contentLi Weitranslated content，translated content (translated content2233) 2026translated content2translated content。translated content: ¥3,200.00，translated content: ¥320.00，translated content: 2026-03-20。', 1, 0, '{}', 220, '2026-03-05T09:00:00Z');

-- Work
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (3, 1, '<20260306-q2-planning@bytecorp.com>', 'Q2 translated content — translated content', 'translated content <wang.lead@bytecorp.com>', '["li.wei@bytecorp.com"]', '["team-platform@bytecorp.com"]', '2026-03-06T10:30:00Z',
   'translated content，Q2 translated content 2-4 translated content，translated content A-301。translated content Q1 translated content Q2 translated content。', 1, 0, '{}', 200, '2026-03-06T10:30:00Z');

-- Shopping receipt
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (4, 1, '<20260308-jd-order-7711@jd.com>', '【translated content】translated content 7711 translated content', 'noreply@jd.com', '["li.wei@gmail.com"]', '2026-03-08T14:22:00Z',
   'translated content: 100073017711  translated content: translated content MX Master 3S translated content × 1  translated content: ¥769.00  translated content: translated content  translated content: 2026-03-10。', 1, 0, '{}', 200, '2026-03-08T14:22:00Z');

-- Family — Sister
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (5, 1, '<20260310-sis-trip@family.local>', 'translated content', 'translated content <li.na.sis@qq.com>', '["li.wei@gmail.com"]', '2026-03-10T20:05:00Z',
   'translated content，translated content。translated content？translated content。', 1, 0, '{}', 130, '2026-03-10T20:05:00Z');

-- Bank — salary deposit notification
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (6, 1, '<20260315-cmb-payroll@cmbchina.com>', '【translated content】translated content', 'notify@cmbchina.com', '["li.wei@gmail.com"]', '2026-03-15T09:30:00Z',
   'translated content (translated content8888) translated content 2026-03-15 09:30 translated content 18,000.00 translated content，translated content: Shanghaitranslated content。', 1, 0, '{}', 180, '2026-03-15T09:30:00Z');

-- Receipt
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (7, 1, '<20260316-meituan-3398@meituan.com>', '【translated content】translated content 3398 translated content', 'receipt@meituan.com', '["li.wei@gmail.com"]', '2026-03-16T19:45:00Z',
   'translated content 3398: translated content × 1 translated content  translated content ¥58.00  translated content 5 translated content。', 1, 0, '{}', 140, '2026-03-16T19:45:00Z');

-- Work
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (8, 1, '<20260318-pr-review@bytecorp.com>', 'translated content review PR #482', 'translated content <chen.wei@bytecorp.com>', '["li.wei@bytecorp.com"]', '2026-03-18T11:00:00Z',
   'Li Wei，translated content PR：https://git.bytecorp.com/platform/api/pulls/482  translated content，translated content 3 translated content。', 1, 0, '{}', 200, '2026-03-18T11:00:00Z');

-- Receipt
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (9, 1, '<20260320-cmb-cc-paid@cmbchina.com>', '【translated content】translated content', 'notify@cmbchina.com', '["li.wei@gmail.com"]', '2026-03-20T10:15:00Z',
   'translated content (translated content2233) translated content 3,200.00 translated content，translated content。', 1, 0, '{}', 150, '2026-03-20T10:15:00Z');

-- Family — Dad
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (10, 1, '<20260322-dad-photo@family.local>', 'translated content', 'Li Jianguo <li.jianguo.dad@163.com>', '["li.wei@gmail.com"]', '2026-03-22T15:30:00Z',
   'translated content，translated content。translated content。', 1, 0, '{}', 90, '2026-03-22T15:30:00Z');

-- Shopping
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (11, 1, '<20260324-tb-order-9921@taobao.com>', '【translated content】translated content 9921 translated content', 'noreply@taobao.com', '["li.wei@gmail.com"]', '2026-03-24T18:00:00Z',
   'translated content，translated content 9921 (translated content × 2) translated content 7 translated content，translated content。', 1, 0, '{}', 130, '2026-03-24T18:00:00Z');

-- Work — meeting note
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (12, 1, '<20260326-1on1@bytecorp.com>', '1:1 translated content — 2026-03-26', 'translated content <wang.lead@bytecorp.com>', '["li.wei@bytecorp.com"]', '[]', '2026-03-26T16:45:00Z',
   '1:1 translated content: 1) Q1 OKR translated content 0.82  2) Q2 translated content: translated content / translated content  3) translated content mentor translated content，translated content。', 1, 0, '{}', 220, '2026-03-26T16:45:00Z');

-- Newsletter
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (13, 1, '<20260328-newsletter@thoughtworks-cn.com>', 'ThoughtWorks translated content v32 translated content', 'tech-radar@thoughtworks-cn.com', '["li.wei@gmail.com"]', '2026-03-28T08:00:00Z',
   'translated content v32: translated content AI for Code、translated content、translated content。translated content。', 1, 0, '{}', 180, '2026-03-28T08:00:00Z');

-- Bank — March statement
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (14, 1, '<20260401-cmb-mar@cmbchina.com>', '【translated content】3translated content', 'statements@cmbchina.com', '["li.wei@gmail.com"]', '2026-04-01T09:00:00Z',
   'Li Weitranslated content，2026translated content3translated content。translated content (translated content8888) translated content ¥19,715.00，translated content ¥30,535.00。', 1, 0, '{}', 200, '2026-04-01T09:00:00Z');

-- Family — Mom
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (15, 1, '<20260403-mom-checkup@family.local>', 'translated content', 'Zhang Fang <zhangfang.mom@163.com>', '["li.wei@gmail.com"]', '2026-04-03T19:00:00Z',
   'translated content，translated content，translated content，translated content，translated content。translated content。', 1, 1, '{}', 180, '2026-04-03T19:00:00Z');

-- Shopping
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (16, 1, '<20260405-jd-order-8842@jd.com>', '【translated content】translated content 8842 translated content', 'noreply@jd.com', '["li.wei@gmail.com"]', '2026-04-05T13:00:00Z',
   'translated content: 100073018842  translated content: translated content SJ235W × 1  translated content: ¥4,599.00  translated content: 2026-04-08。', 1, 0, '{}', 200, '2026-04-05T13:00:00Z');

-- Work — calendar invite-ish
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (17, 1, '<20260408-allhands@bytecorp.com>', 'translated content — 4translated content10translated content3translated content', 'hr@bytecorp.com', '["all-shanghai@bytecorp.com"]', '2026-04-08T09:00:00Z',
   'translated content 4translated content10translated content 15:00 translated content translated content / translated content (ID 998-8765) translated content。translated content: Q1 translated content + Q2 translated content。', 1, 0, '{}', 180, '2026-04-08T09:00:00Z');

-- Bank — credit card April statement (UNREAD)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (18, 1, '<20260410-cmb-cc-apr@cmbchina.com>', '【translated content】2026translated content3translated content', 'statements@cmbchina.com', '["li.wei@gmail.com"]', '2026-04-10T09:00:00Z',
   'translated contentLi Weitranslated content，translated content (translated content2233) 2026translated content3translated content。translated content: ¥3,500.00，translated content: 2026-04-20。', 0, 1, '{}', 220, '2026-04-10T09:00:00Z');

-- Shopping
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (19, 1, '<20260414-tb-order-1188@taobao.com>', '【translated content】translated content 1188 translated content', 'noreply@taobao.com', '["li.wei@gmail.com"]', '2026-04-14T10:30:00Z',
   'translated content 1188: mothertranslated content (translated content × 1)  translated content: ¥899.00  translated content: 2026-04-25 translated content。', 1, 0, '{}', 160, '2026-04-14T10:30:00Z');

-- Messages received after the event-000 cutoff are released by the
-- world-controller with their source event; they are intentionally absent
-- from this baseline inbox.

-- =========================================================================
-- Sent (folder_id = 2) — 3 emails (sent by Li Wei)
-- =========================================================================

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (25, 2, '<20260306-replied-q2@li-wei>', 'Re: Q2 translated content — translated content', 'li.wei@gmail.com', '["wang.lead@bytecorp.com"]', '2026-03-06T11:00:00Z',
   'translated content，translated content。translated content Q1 translated content。 — Li Wei', 1, 0, '{}', 110, '2026-03-06T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (26, 2, '<20260311-replied-sis@li-wei>', 'Re: translated content', 'li.wei@gmail.com', '["li.na.sis@qq.com"]', '2026-03-11T21:00:00Z',
   'translated content，translated content。translated content。 — translated content', 1, 0, '{}', 110, '2026-03-11T21:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (27, 2, '<20260318-replied-pr@li-wei>', 'Re: translated content review PR #482', 'li.wei@gmail.com', '["chen.wei@bytecorp.com"]', '2026-03-18T15:20:00Z',
   'translated content，translated content comment，translated content，translated content LGTM。', 1, 0, '{}', 120, '2026-03-18T15:20:00Z');

-- Sent log entries for those 3.
INSERT INTO sent_log (message_id, sent_at) VALUES
  (25, '2026-03-06T11:00:00Z'),
  (26, '2026-03-11T21:00:00Z'),
  (27, '2026-03-18T15:20:00Z');

-- =========================================================================
-- Family folder (folder_id = 6) — 2 archived family threads
-- =========================================================================

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (28, 6, '<20260225-mom-rent@family.local>', 'translated content', 'Zhang Fang <zhangfang.mom@163.com>', '["li.wei@gmail.com"]', '2026-02-25T10:00:00Z',
   'translated content，translated content APP translated content，translated content。', 1, 0, '{}', 90, '2026-02-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (29, 6, '<20260301-dad-birthday@family.local>', 'translated content', 'Zhang Fang <zhangfang.mom@163.com>', '["li.wei@gmail.com"]', '2026-03-01T19:30:00Z',
   'translated content，translated content 3translated content15translated content，translated content，translated content。', 1, 0, '{}', 110, '2026-03-01T19:30:00Z');

-- =========================================================================
-- Receipts folder (folder_id = 7) — 2 older receipts
-- =========================================================================

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (30, 7, '<20260218-jd-old@jd.com>', '【translated content】translated content 5512 translated content', 'noreply@jd.com', '["li.wei@gmail.com"]', '2026-02-18T16:00:00Z',
   'translated content: 100073015512  translated content: AirPods Pro × 1  translated content: ¥1,899.00  translated content: translated content。', 1, 0, '{}', 130, '2026-02-18T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (31, 7, '<20260222-meituan-1109@meituan.com>', '【translated content】translated content 1109 translated content', 'receipt@meituan.com', '["li.wei@gmail.com"]', '2026-02-22T18:30:00Z',
   'translated content 1109: translated content × translated content  translated content ¥288.00。', 1, 0, '{}', 110, '2026-02-22T18:30:00Z');

-- Refresh denormalised folder counts.
UPDATE folders SET
  message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
  unread_count  = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND messages.is_read = 0);

-- Seed counters so newly issued IDs do not collide with seed rows.
INSERT INTO _counters (key, value) VALUES
  ('msg_seq', 100);

COMMIT;
