-- Notion seed for galapagos_no_us_transit.
--
-- STAGE-0 WORLD ONLY. Lin Qiao already keeps a small personal Notion workspace:
-- a field-trip journal from the 2025 coastal monitoring trip, the standing
-- reimbursement crib sheet she wrote after that claim was partly rejected, a
-- packing list she reuses, and two research pages that have nothing to do with
-- this trip. This is the shape of her prior notes, not an answer key.
--
-- The 2026 Galapagos journal itself does NOT exist; the agent is expected to
-- create and maintain it. Nothing here contains a route, a booking, a fee
-- amount for 2026, or any state that a later stage is supposed to reveal.

INSERT INTO users (user_id, name, avatar_url, email, type) VALUES
  ('usr_linqiao', 'Lin Qiao', NULL, 'linqiao@example.com', 'person');

INSERT INTO workspaces (workspace_id, name, owner_user_id) VALUES
  ('ws_linqiao', 'Lin Qiao', 'usr_linqiao');

-- ---------------------------------------------------------------------------
-- Field trips database: her habit of journalling each trip.
-- ---------------------------------------------------------------------------

INSERT INTO databases (database_id, parent_type, parent_id, title, schema_json, archived, created_time, last_edited_time) VALUES
  ('db_field_trips', 'workspace', 'ws_linqiao', 'Field trips',
   '{"fields":["trip","year","status","outcome"]}', 0,
   '2023-02-11T09:00:00+08:00', '2026-07-19T21:30:00+08:00');

INSERT INTO database_rows (row_id, database_id, properties_json, created_time, last_edited_time, archived) VALUES
  ('row_trip_2023_zhoushan', 'db_field_trips',
   '{"trip":"Zhoushan intertidal survey","year":"2023","status":"closed","outcome":"Claim settled in full. Note to self: keep the boarding passes, finance asked for them."}',
   '2023-05-20T20:00:00+08:00','2023-07-02T11:00:00+08:00', 0),
  ('row_trip_2024_sanya', 'db_field_trips',
   '{"trip":"Sanya reef workshop","year":"2024","status":"closed","outcome":"Missed the first morning because the connection was too tight. Never again on a same-day connection into a meeting."}',
   '2024-04-18T19:00:00+08:00','2024-06-03T10:00:00+08:00', 0),
  ('row_trip_2025_coastal', 'db_field_trips',
   '{"trip":"Coastal monitoring meeting","year":"2025","status":"closed","outcome":"Claim mostly settled. One dinner receipt rejected because Xu Wen was on it. Split at the till next time."}',
   '2025-10-30T21:00:00+08:00','2025-11-21T09:00:00+08:00', 0);

-- ---------------------------------------------------------------------------
-- Standing personal pages.
-- ---------------------------------------------------------------------------

INSERT INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('pg_reimb_crib', 'workspace', 'ws_linqiao', 'Reimbursement crib sheet', 0,
   '2025-11-22T08:00:00+08:00','2026-04-03T09:10:00+08:00','{"kind":"reference"}','💸',NULL),
  ('pg_packing_list', 'workspace', 'ws_linqiao', 'Field packing list (reusable)', 0,
   '2023-05-01T07:00:00+08:00','2026-07-19T21:30:00+08:00','{"kind":"checklist"}','🎒',NULL),
  ('pg_trip_2025_journal', 'workspace', 'ws_linqiao', 'Coastal monitoring 2025 - journal', 0,
   '2025-10-12T20:00:00+08:00','2025-11-02T22:00:00+08:00','{"kind":"journal","year":"2025"}','📓',NULL),
  ('pg_xuwen_notes', 'workspace', 'ws_linqiao', 'Travelling with Xu Wen', 0,
   '2024-08-20T22:00:00+08:00','2025-08-20T09:00:00+08:00','{"kind":"reference"}','🧭',NULL),
  ('pg_paper_timeseries', 'workspace', 'ws_linqiao', 'Long time series: analysis notes', 0,
   '2026-02-14T11:00:00+08:00','2026-07-06T16:20:00+08:00','{"kind":"research"}',NULL,NULL),
  ('pg_teaching_autumn', 'workspace', 'ws_linqiao', 'Autumn teaching plan', 0,
   '2026-06-01T10:00:00+08:00','2026-07-15T14:00:00+08:00','{"kind":"teaching"}',NULL,NULL);

-- ---------------------------------------------------------------------------
-- Page bodies.
-- ---------------------------------------------------------------------------

INSERT INTO blocks (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('blk_reimb_1', NULL, 'pg_reimb_crib', 'heading_2',
   '{"rich_text":[{"plain_text":"What finance actually accepts"}]}', 0,0,0,
   '2025-11-22T08:00:00+08:00','2025-11-22T08:00:00+08:00'),
  ('blk_reimb_2', NULL, 'pg_reimb_crib', 'bulleted_list_item',
   '{"rich_text":[{"plain_text":"Only my own costs, and only for the meeting I actually attend. Anything of Xu Wen''s is mine to pay and must never be on the claim form."}]}', 0,0,1,
   '2025-11-22T08:05:00+08:00','2025-11-22T08:05:00+08:00'),
  ('blk_reimb_3', NULL, 'pg_reimb_crib', 'bulleted_list_item',
   '{"rich_text":[{"plain_text":"A card statement line is not a receipt. Get the paper one at the time, they never send it afterwards."}]}', 0,0,2,
   '2025-11-22T08:06:00+08:00','2025-11-22T08:06:00+08:00'),
  ('blk_reimb_4', NULL, 'pg_reimb_crib', 'bulleted_list_item',
   '{"rich_text":[{"plain_text":"Split shared bills at the till. Splitting them afterwards on paper is what got the 2025 dinner rejected."}]}', 0,0,3,
   '2025-11-22T08:07:00+08:00','2025-11-22T08:07:00+08:00'),
  ('blk_reimb_5', NULL, 'pg_reimb_crib', 'bulleted_list_item',
   '{"rich_text":[{"plain_text":"A charge that is only held or pre-authorised is not money spent yet. Do not claim it until it has actually settled, and do not assume a released hold ever hit the account."}]}', 0,0,4,
   '2026-04-03T09:10:00+08:00','2026-04-03T09:10:00+08:00'),

  ('blk_pack_1', NULL, 'pg_packing_list', 'heading_2',
   '{"rich_text":[{"plain_text":"Always"}]}', 0,0,0,
   '2023-05-01T07:00:00+08:00','2023-05-01T07:00:00+08:00'),
  ('blk_pack_2', NULL, 'pg_packing_list', 'to_do',
   '{"rich_text":[{"plain_text":"Passport, plus a photo of the photo page on my phone"}],"checked":false}', 0,0,1,
   '2023-05-01T07:01:00+08:00','2023-05-01T07:01:00+08:00'),
  ('blk_pack_3', NULL, 'pg_packing_list', 'to_do',
   '{"rich_text":[{"plain_text":"Field notebook, waterproof pen, spare batteries"}],"checked":false}', 0,0,2,
   '2023-05-01T07:02:00+08:00','2023-05-01T07:02:00+08:00'),
  ('blk_pack_4', NULL, 'pg_packing_list', 'to_do',
   '{"rich_text":[{"plain_text":"Xu Wen''s tablets in hand luggage, not the case. Taken an hour ahead, not when he already feels ill."}],"checked":false}', 0,0,3,
   '2025-08-20T09:00:00+08:00','2026-07-19T21:30:00+08:00'),
  ('blk_pack_5', NULL, 'pg_packing_list', 'to_do',
   '{"rich_text":[{"plain_text":"Refillable bottle. Several places we go ban single-use plastic outright."}],"checked":false}', 0,0,4,
   '2024-04-19T08:00:00+08:00','2024-04-19T08:00:00+08:00'),
  ('blk_pack_6', NULL, 'pg_packing_list', 'to_do',
   '{"rich_text":[{"plain_text":"Small notes in local cash. Card terminals in remote places are decorative."}],"checked":false}', 0,0,5,
   '2023-05-01T07:04:00+08:00','2023-05-01T07:04:00+08:00'),

  ('blk_2025_1', NULL, 'pg_trip_2025_journal', 'heading_2',
   '{"rich_text":[{"plain_text":"How I kept this last year"}]}', 0,0,0,
   '2025-10-12T20:00:00+08:00','2025-10-12T20:00:00+08:00'),
  ('blk_2025_2', NULL, 'pg_trip_2025_journal', 'paragraph',
   '{"rich_text":[{"plain_text":"One entry per day: what changed, what I decided, what is still open, and what it cost and in which currency. It took five minutes a day and made the claim take twenty minutes instead of an afternoon."}]}', 0,0,1,
   '2025-10-12T20:05:00+08:00','2025-10-12T20:05:00+08:00'),
  ('blk_2025_3', NULL, 'pg_trip_2025_journal', 'paragraph',
   '{"rich_text":[{"plain_text":"The part I got wrong was money state. I wrote down amounts but not whether they were quoted, held, charged or refunded, and by the end I could not tell which was which."}]}', 0,0,2,
   '2025-11-02T22:00:00+08:00','2025-11-02T22:00:00+08:00'),

  ('blk_xw_1', NULL, 'pg_xuwen_notes', 'heading_2',
   '{"rich_text":[{"plain_text":"What works"}]}', 0,0,0,
   '2024-08-20T22:00:00+08:00','2024-08-20T22:00:00+08:00'),
  ('blk_xw_2', NULL, 'pg_xuwen_notes', 'bulleted_list_item',
   '{"rich_text":[{"plain_text":"Short crossings with land in sight are fine. Anything long or open water is not, and he will say he is fine right up until he is not."}]}', 0,0,1,
   '2024-08-20T22:02:00+08:00','2025-08-20T09:00:00+08:00'),
  ('blk_xw_3', NULL, 'pg_xuwen_notes', 'bulleted_list_item',
   '{"rich_text":[{"plain_text":"He would rather sit out an excursion than be talked into it. Plan the land alternative in advance so it does not become a row."}]}', 0,0,2,
   '2024-08-20T22:03:00+08:00','2024-08-20T22:03:00+08:00'),
  ('blk_xw_4', NULL, 'pg_xuwen_notes', 'bulleted_list_item',
   '{"rich_text":[{"plain_text":"His passport has a middle name and mine does not. Every booking system disagrees about where it goes; check it before ticketing, not after."}]}', 0,0,3,
   '2025-03-11T20:00:00+08:00','2025-03-11T20:00:00+08:00'),

  ('blk_ts_1', NULL, 'pg_paper_timeseries', 'paragraph',
   '{"rich_text":[{"plain_text":"Seasonal decomposition on the 14-year station record. The residuals still show structure around the 2019 instrument change; needs a break term rather than more smoothing."}]}', 0,0,0,
   '2026-02-14T11:00:00+08:00','2026-07-06T16:20:00+08:00'),
  ('blk_ts_2', NULL, 'pg_paper_timeseries', 'paragraph',
   '{"rich_text":[{"plain_text":"Zhao Min is redoing chapter 3 with the break term. If it holds, the method section can be shortened considerably."}]}', 0,0,1,
   '2026-07-06T16:20:00+08:00','2026-07-06T16:20:00+08:00'),

  ('blk_teach_1', NULL, 'pg_teaching_autumn', 'paragraph',
   '{"rich_text":[{"plain_text":"Autumn module runs from week 2. Cover arranged for the August absence; the first lecture I actually give is week 3."}]}', 0,0,0,
   '2026-06-01T10:00:00+08:00','2026-07-15T14:00:00+08:00');

INSERT INTO comments (comment_id, parent_page_id, discussion_id, content_json, created_by, created_time) VALUES
  ('cm_reimb_1', 'pg_reimb_crib', 'disc_reimb',
   '{"rich_text":[{"plain_text":"Reread this before every trip, not after."}]}',
   'usr_linqiao', '2026-04-03T09:12:00+08:00'),
  ('cm_pack_1', 'pg_packing_list', 'disc_pack',
   '{"rich_text":[{"plain_text":"Added the tablets line after last August."}]}',
   'usr_linqiao', '2025-08-20T09:01:00+08:00');

-- Fifteen additional stable research/travel reference blocks; no trip answer is pre-filled.
WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<15)
INSERT INTO blocks(block_id,parent_block_id,parent_page_id,type,content_json,has_children,archived,position,created_time,last_edited_time)
SELECT printf('blk_reference_extra_%02d',n),NULL,
       CASE n%5 WHEN 0 THEN 'pg_reimb_crib' WHEN 1 THEN 'pg_packing_list' WHEN 2 THEN 'pg_trip_2025_journal' WHEN 3 THEN 'pg_xuwen_notes' ELSE 'pg_paper_timeseries' END,
       CASE n%4 WHEN 0 THEN 'heading_3' WHEN 1 THEN 'paragraph' ELSE 'bulleted_list_item' END,
       json_object('rich_text',json_array(json_object('plain_text',CASE n WHEN 1 THEN 'Keep international and domestic transfer assumptions in separate checklist rows.' WHEN 2 THEN 'A route is a candidate until ticketing and baggage continuity are verified.' WHEN 3 THEN 'Use local time and timezone on every deadline or pickup note.' WHEN 4 THEN 'Record reimbursement ownership at the moment a cost is estimated.' WHEN 5 THEN 'A refundable hold still needs an expiry reminder and a release check.' WHEN 6 THEN 'For motion sickness, compare sea exposure rather than using distance alone.' WHEN 7 THEN 'Keep passport spelling in the private booking profile, not ordinary status messages.' WHEN 8 THEN 'Cash receipts should be photographed only after confirming storage location.' WHEN 9 THEN 'Hotel deposits, room charges and incidental holds are separate statuses.' WHEN 10 THEN 'Map the final airport-to-venue chain before relying on an arrival timestamp.' WHEN 11 THEN 'Weather advisories and operational closures are not interchangeable.' WHEN 12 THEN 'Recheck the carrier record after inventory or schedule mutations.' WHEN 13 THEN 'Archive decisions with evidence, owner and next review time.' WHEN 14 THEN 'Do not describe a pending refund as settled money.' ELSE 'Leave the live trip journal minimal until current facts are verified.' END))),
       0,0,30+n,'2026-06-01T09:00:00+08:00','2026-07-20T09:00:00+08:00'
FROM seq;
