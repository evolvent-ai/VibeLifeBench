-- Stage 11 mutation: finance answers the specific question about a companion.
--
-- The Stage-0 seed has the general 2026 claim rules (message 7) and the 2025
-- settlement letter that rejected one shared restaurant bill (message 8). What
-- did not exist before now is a ruling on THIS trip: which of the shared costs
-- of a two-person booking are claimable when only one traveller is a delegate.
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<fin-2026-companion-ruling-lq@example.edu>','Re: August trip, my husband travels with me','finance.travel@example.edu','["linqiao@example.com"]','[]','[]','2026-08-04T21:00:00+08:00',
  'Dr. Lin,

In reply to your query, and to save you a rejected claim afterwards.

Claimable: your own airfare; your own island entry charges; the room for the nights of the meeting and reasonable travel days, at the single-occupancy rate the property publishes, not the double rate; airport and venue transfers for you.

Not claimable: your husband''s airfare; his island entry charges; the difference between the single and double room rate; any transfer seat booked for him; his insurance; anything either of you does that is not the meeting.

Where you book one room for two people, claim the single rate and carry the difference yourself. Ask the property to state the single rate on the invoice at the time of booking. They will not do it afterwards.

Where a charge is only pre-authorised or held, it is not an expense yet and must not be on the form. Claim it when it settles, and only if it settles.

Office of Finance',
  0,1,1,NULL,NULL,'{}',61,1200,'2026-08-04T21:00:00+08:00'),

 (2,'<lq-2026-companion-query@example.com>','August trip, my husband travels with me','linqiao@example.com','["finance.travel@example.edu"]','[]','[]','2026-08-04T20:35:00+08:00',
  'We are booking one room for the two of us and one transfer for the two of us. I would rather split it correctly at the time than argue about it in September. What exactly can I put on the claim?',
  1,0,0,NULL,NULL,'{}',62,260,'2026-08-04T20:35:00+08:00');
