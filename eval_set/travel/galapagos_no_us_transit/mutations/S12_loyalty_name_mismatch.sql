-- Stage 12 mutation: the hotel chain's loyalty system sends its periodic
-- profile confirmation, and the truncated name on Xu Wen's record becomes a
-- concrete, checkable fact rather than something Lin Qiao vaguely noticed.
--
-- The Stage-0 seed already carried the enrolment confirmation (message 13,
-- 22 May) which reads "Member: XU WEN" -- the discrepancy has always been
-- there in the data. What arrives now is the system telling them the profile
-- name is what will be sent to the property, which is what makes it matter.
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<islasverdes-profile-annual-check@example.com>','Please confirm your member details','members@islasverdes.example.com','["linqiao@example.com"]','[]','[]','2026-08-05T09:00:00-06:00',
  'We send this once a year and before any stay in a peak period.

The details we hold for the guests on your account:

Member 1: LIN QIAO
Member 2: XU WEN

The name we hold is the name we pass to the property when a reservation is made, and the property matches it against the identity document at check-in. Where they differ, the property may ask for the booking to be corrected before the room is released, and in high season that can mean a wait.

Amend a member name in the account settings. Amendments take effect on reservations made afterwards, not on reservations already in the system.

Islas Verdes Collection',
  0,0,0,NULL,NULL,'{}',71,900,'2026-08-05T09:00:00-06:00'),

 (1,'<carrier-ib-name-policy@carrier-ib.example.com>','Re: name on ticket','service@carrier-ib.example.com','["linqiao@example.com"]','[]','[]','2026-08-05T11:30:00+02:00',
  'In reply to your question about names.

The name on the ticket must match the travel document exactly, including any middle name that appears on the document''s machine-readable zone.

Before ticketing, a name can be corrected at no charge. After ticketing, a name change is not permitted on this fare: the ticket must be voided if still within the void window, or reissued at the fare available on the day.

A frequent-flyer or hotel loyalty profile is a separate record and has no bearing on the ticket. A mismatch there is a matter for that programme, not for us.

Iberia Customer Service',
  0,0,0,NULL,NULL,'{}',72,780,'2026-08-05T11:30:00+02:00');
