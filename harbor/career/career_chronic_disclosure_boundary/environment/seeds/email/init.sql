-- Curated Stage-0 seed for career_chronic_disclosure_boundary / email.

BEGIN;

INSERT INTO account_config (id, email, name, created_at) VALUES
  (1, 'feng.yi@163.com', 'Evan Feng', '2018-08-01T00:00:00Z');

INSERT INTO folders (id, name) VALUES
  (1, 'INBOX'),
  (2, 'Sent'),
  (3, 'Drafts'),
  (4, 'Trash'),
  (5, 'Spam');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1, 1, '<20260608.020000.u2qrcc4vlbx@liyaobio.com>', '【LuminaBio】English text', 'LuminaBio HR English text <hr.qinshuang@liyaobio.com>', '["feng.yi@163.com"]', '2026-06-08T02:00:00Z', 'English text：English text，English text，English text，English text 2026-06-30。English text。', 1, 1, '{}', 221, '2026-06-08T02:00:00Z'),
  (2, 1, '<20260607.012000.kdcxdblzugx@cmbchina.example>', 'English text', 'China Merchants Bank <service@cmbchina.example>', '["feng.yi@163.com"]', '2026-06-07T01:20:00Z', 'English text 6 English text 20 English text，English text；English text。', 1, 0, '{}', 121, '2026-06-07T01:20:00Z'),
  (3, 1, '<20260606.031000.qho7n6ncblx@mch-sh.example>', 'English text', 'English text <appointment@mch-sh.example>', '["feng.yi@163.com"]', '2026-06-06T03:10:00Z', 'English text，English text；English text。', 1, 1, '{}', 114, '2026-06-06T03:10:00Z'),
  (4, 1, '<20260605.113000.jyrpiimedpx@family.example>', 'English text', 'English text <shao.qing@family.example>', '["feng.yi@163.com"]', '2026-06-05T11:30:00Z', 'English text、English text，English text，English text。', 1, 0, '{}', 102, '2026-06-05T11:30:00Z'),
  (5, 1, '<20260604.081500.nzmajnbqaix@liyaobio.com>', 'English text', 'LuminaBio English text <architecture@liyaobio.com>', '["feng.yi@163.com"]', '2026-06-04T08:15:00Z', 'English text，English text。', 1, 0, '{}', 114, '2026-06-04T08:15:00Z'),
  (6, 1, '<20260603.064000.x5jlbyoqbgx@liyaobio.com>', 'English text', 'LuminaBio IT English text <it-service@liyaobio.com>', '["feng.yi@163.com"]', '2026-06-03T06:40:00Z', 'English text；English text、English text。', 1, 1, '{}', 120, '2026-06-03T06:40:00Z'),
  (7, 1, '<20260602.003000.3jlmmq7txrx@jobs.example>', 'English text', 'Recruiting Platform <digest@jobs.example>', '["feng.yi@163.com"]', '2026-06-02T00:30:00Z', 'English text、English text、English text；English text，English text。', 1, 0, '{}', 123, '2026-06-02T00:30:00Z'),
  (8, 1, '<20260601.090000.lddc6eiwm4x@github.example>', 'English text', 'GitHub Notifications <notifications@github.example>', '["feng.yi@163.com"]', '2026-06-01T09:00:00Z', 'English text，English text。', 0, 0, '{}', 105, '2026-06-01T09:00:00Z'),
  (9, 1, '<20260530.022000.i4jhl6q3gex@property.example>', 'English text', 'English text <service@property.example>', '["feng.yi@163.com"]', '2026-05-30T02:20:00Z', 'English text，English text。', 1, 0, '{}', 96, '2026-05-30T02:20:00Z'),
  (10, 1, '<20260528.011000.2josicfb3wx@tax.example>', 'English text', 'English text <notice@tax.example>', '["feng.yi@163.com"]', '2026-05-28T01:10:00Z', 'English text，English text。', 1, 0, '{}', 93, '2026-05-28T01:10:00Z'),
  (11, 1, '<20260526.073000.joor3ujyoyx@dev-sh.example>', 'English text：English text', 'English text <events@dev-sh.example>', '["feng.yi@163.com"]', '2026-05-26T07:30:00Z', 'English text，English text。', 1, 0, '{}', 90, '2026-05-26T07:30:00Z'),
  (12, 1, '<20260524.040000.gaofayolwtx@broadband.example>', 'English text', 'English text <customer@broadband.example>', '["feng.yi@163.com"]', '2026-05-24T04:00:00Z', 'English text，English text；English text。', 1, 0, '{}', 102, '2026-05-24T04:00:00Z'),
  (13, 1, '<20260522.120000.ox7vi2prlxx@163.com>', 'English text', 'Evan Feng <feng.yi@163.com>', '["feng.yi@163.com"]', '2026-05-22T12:00:00Z', 'English text：English text，English text、English text、English text。', 1, 1, '{}', 150, '2026-05-22T12:00:00Z'),
  (14, 1, '<20260520.024000.6fovua6is3x@library-sh.example>', 'English text', 'English text <notice@library-sh.example>', '["feng.yi@163.com"]', '2026-05-20T02:40:00Z', '《English text》English text，English text。', 1, 0, '{}', 87, '2026-05-20T02:40:00Z'),
  (15, 1, '<20260518.052000.chbn77awvfx@checkup-sh.example>', 'English text', 'English text <report@checkup-sh.example>', '["feng.yi@163.com"]', '2026-05-18T05:20:00Z', 'English text；English text，English text。', 1, 1, '{}', 135, '2026-05-18T05:20:00Z'),
  (16, 1, '<20260515.014500.r5bmcjaphlx@insurance.example>', 'English text', 'English text <policy@insurance.example>', '["feng.yi@163.com"]', '2026-05-15T01:45:00Z', 'English text，English text；English text。', 1, 0, '{}', 108, '2026-05-15T01:45:00Z'),
  (17, 1, '<20260512.091000.rukhphxsy7x@shjug.example>', 'Java English text', 'Shanghai JUG <newsletter@shjug.example>', '["feng.yi@163.com"]', '2026-05-12T09:10:00Z', 'English text、GC English text，English text。', 0, 0, '{}', 96, '2026-05-12T09:10:00Z'),
  (18, 1, '<20260509.002000.kdyzeb57tvx@cloud.example>', 'English text', 'English text <billing@cloud.example>', '["feng.yi@163.com"]', '2026-05-09T00:20:00Z', 'English text，English text。', 1, 0, '{}', 90, '2026-05-09T00:20:00Z'),
  (19, 1, '<20260506.030000.6c6xuyd7ucx@property.example>', 'English text', 'English text <engineering@property.example>', '["feng.yi@163.com"]', '2026-05-06T03:00:00Z', 'English text，English text。', 1, 0, '{}', 69, '2026-05-06T03:00:00Z'),
  (20, 1, '<20260502.100000.i62u33xeblx@163.com>', 'English text', 'Evan Feng <feng.yi@163.com>', '["feng.yi@163.com"]', '2026-05-02T10:00:00Z', 'English text：English text，English text。', 1, 1, '{}', 141, '2026-05-02T10:00:00Z');

INSERT INTO _counters (key, value) VALUES
  ('message_seq', 20),
  ('draft_seq', 0);

COMMIT;
