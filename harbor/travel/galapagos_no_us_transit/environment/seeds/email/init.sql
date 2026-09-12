-- Email seed for galapagos_no_us_transit.
--
-- STAGE-0 WORLD ONLY. Every message below is something Lin Qiao's mailbox
-- already contained on 2026-07-24 (the task start): the workshop invitation
-- thread, her own replies, standing university finance policy, insurance and
-- membership paperwork, and ordinary unrelated traffic.
--
-- Facts that are only learned later (the organizer logistics packet, the
-- airline weather waiver, the entry-fee notice, the card verification request,
-- the workshop schedule shift, the receipt bundle) are NOT here. They are
-- injected by the mutations under mutations/S*.sql at their own stage.
--
-- Message ids 1-38 are reserved for this seed; stage mutations use 100+.

INSERT INTO account_config(id,email,name,created_at) VALUES
  (1,'linqiao@example.com','Lin Qiao','2019-09-01T09:00:00+08:00');

INSERT INTO folders(id,name,delimiter,flags_json,message_count,unread_count) VALUES
  (1,'INBOX','/','[]',0,0),
  (2,'Sent','/','[]',0,0),
  (3,'Drafts','/','[]',0,0),
  (4,'Trash','/','[]',0,0),
  (5,'Spam','/','[]',0,0),
  (6,'Archive','/','[]',0,0);

-- ---------------------------------------------------------------------------
-- Workshop invitation thread (the reason this trip exists).
-- ---------------------------------------------------------------------------

INSERT INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,1,'<gdfo-2026-invite-lq@galapagos-data.example>','Invitation: Galapagos Ecology Data Workshop 2026','ops@galapagos-data.example','["linqiao@example.com"]','[]','[]','2026-06-12T10:20:00-06:00',
  'Dear Dr. Lin,

The Galapagos Data Field Office invites you to the Galapagos Ecology Data Workshop 2026, held at the Puerto Ayora Marine Data Lab, Avenida Charles Darwin 102, Puerto Ayora, Santa Cruz.

Opening session: 18 August 2026, 09:00.
Closing session: 22 August 2026, 12:00.

Participation is by named invitation and is not transferable. Please confirm by 30 June so we can reserve your bench space and the shared field tablets.

A separate logistics note covering registration, island entry formalities and accommodation guidance will follow closer to the date.

With best regards,
Marisol Aguirre
Programme Coordinator, Galapagos Data Field Office',
  1,1,1,NULL,NULL,'{"X-Mailer":"GDFO Programme Office"}',1,1180,'2026-06-12T10:20:00-06:00'),

 (2,2,'<lq-2026-invite-accept@example.com>','Re: Invitation: Galapagos Ecology Data Workshop 2026','linqiao@example.com','["ops@galapagos-data.example"]','[]','[]','2026-06-15T21:05:00+08:00',
  'Dear Marisol,

Thank you, I am delighted to accept. I will attend the full programme, 18 to 22 August.

Two notes for your records. My passport name is LIN QIAO. My husband, XU WEN CHENG, will travel with me privately; he is not attending the workshop and does not need bench space or materials, but he will be staying with me in Puerto Ayora.

I will book my own travel. Please send the logistics note whenever it is ready.

Best regards,
Lin Qiao',
  1,0,0,'<gdfo-2026-invite-lq@galapagos-data.example>','<gdfo-2026-invite-lq@galapagos-data.example>','{}',2,760,'2026-06-15T21:05:00+08:00'),

 (3,1,'<gdfo-2026-accept-ack@galapagos-data.example>','Confirmed: your place at the 2026 workshop','ops@galapagos-data.example','["linqiao@example.com"]','[]','[]','2026-06-16T08:40:00-06:00',
  'Dear Dr. Lin,

Your place is confirmed and your name badge will read LIN QIAO. Noted that Xu Wen Cheng travels with you privately and is not a participant; he is welcome at the closing reception as your guest but is not covered by the programme.

Please keep this address for anything urgent. Our office is staffed 08:00-16:00 Galapagos time and we are slower to answer at weekends.

Marisol Aguirre',
  1,0,0,'<lq-2026-invite-accept@example.com>','<gdfo-2026-invite-lq@galapagos-data.example> <lq-2026-invite-accept@example.com>','{}',3,620,'2026-06-16T08:40:00-06:00'),

 (4,1,'<gdfo-2026-programme-draft@galapagos-data.example>','Draft programme, 2026 workshop','ops@galapagos-data.example','["linqiao@example.com","participants@galapagos-data.example"]','[]','[]','2026-07-03T15:10:00-06:00',
  'All,

Attached is the draft programme. Day one is instrumentation and station metadata, day two is the shore transect and sample logging, day three is the tortoise-reserve dataset, day four is joint analysis and the closing session.

The shore transect on day two is the only outdoor session and depends on marine conditions. Bring closed shoes, a hat and a refillable bottle. Single-use plastics are not permitted anywhere in the park.

Marisol',
  1,0,0,NULL,NULL,'{}',4,690,'2026-07-03T15:10:00-06:00'),

 (5,2,'<lq-2026-programme-q@example.com>','Re: Draft programme, 2026 workshop','linqiao@example.com','["ops@galapagos-data.example"]','[]','[]','2026-07-05T09:30:00+08:00',
  'Marisol,

Two questions about the draft programme.

1. Is there a fixed time by which participants must have registered in person, or is registration open through the opening morning?
2. My husband is prone to motion sickness. Is any part of the programme, or any of the informal social events, on the water?

Lin Qiao',
  1,0,0,'<gdfo-2026-programme-draft@galapagos-data.example>','<gdfo-2026-programme-draft@galapagos-data.example>','{}',5,480,'2026-07-05T09:30:00+08:00'),

 (6,1,'<gdfo-2026-programme-a@galapagos-data.example>','Re: Draft programme, 2026 workshop','ops@galapagos-data.example','["linqiao@example.com"]','[]','[]','2026-07-06T11:00:00-06:00',
  'Lin Qiao,

1. Registration closes at the venue desk on 17 August. The exact cut-off time is in the logistics note I am still finalising; it is an evening cut-off, not the following morning, because the badge printer goes back to the mainland overnight.
2. The shore transect is walked from the beach, not from a boat. The optional Sunday excursion is a boat trip, but it is optional and your husband can skip it without missing any programme content.

Marisol',
  1,0,1,'<lq-2026-programme-q@example.com>','<gdfo-2026-programme-draft@galapagos-data.example> <lq-2026-programme-q@example.com>','{}',6,690,'2026-07-06T11:00:00-06:00'),

-- ---------------------------------------------------------------------------
-- University finance: the standing rules that already applied before the trip.
-- The companion-cost clarification is NOT here; it arrives at stage 11.
-- ---------------------------------------------------------------------------

 (7,1,'<fin-2026-intl-travel-policy@example.edu>','2026 international academic travel: claim rules','finance.travel@example.edu','["faculty-all@example.edu"]','[]','[]','2026-04-02T14:00:00+08:00',
  'Colleagues,

The 2026 rules for international academic travel claims are now in force.

- Claims are made against the meeting the traveller attends, and only for the named participant.
- Economy airfare, accommodation for the nights of the meeting plus reasonable travel days, mandatory registration or entry charges, and airport or venue transfers are claimable.
- Upgrades, companions, personal excursions, personal insurance and minibar are not claimable and must not appear on the claim form.
- Original receipts are required. A card statement line alone is not a receipt.
- Claims must be filed within 30 days of return.

Questions to this address.
Office of Finance',
  1,0,0,NULL,NULL,'{}',7,880,'2026-04-02T14:00:00+08:00'),

 (8,6,'<fin-2025-claim-settled-lq@example.edu>','Your 2025 claim has been settled','finance.travel@example.edu','["linqiao@example.com"]','[]','[]','2025-11-20T16:30:00+08:00',
  'Dr. Lin,

Your claim for the 2025 coastal monitoring meeting has been settled. Reimbursed: airfare, three nights accommodation, conference fee. Rejected: one restaurant receipt with two covers, as the second cover was not a meeting participant.

Please continue to split shared bills at the point of payment rather than at claim time; it is much easier for everyone.

Office of Finance',
  1,0,0,NULL,NULL,'{}',8,560,'2025-11-20T16:30:00+08:00'),

 (9,1,'<dept-2026-aug-cover@example.edu>','August teaching cover and the 25 August meeting','wang.rong@example.edu','["linqiao@example.com"]','[]','[]','2026-07-10T17:20:00+08:00',
  'Lin Qiao,

Cover for your August absence is arranged. Two things I cannot move:

- the online group meeting on 14 August, 16:30-17:30, you are chairing;
- the faculty meeting on 25 August, 14:00-16:00, in person, where your funding line is on the agenda.

Everything between those two is yours.

Wang Rong',
  1,1,0,NULL,NULL,'{}',9,470,'2026-07-10T17:20:00+08:00'),

-- ---------------------------------------------------------------------------
-- Documents, insurance, memberships: paperwork already on file.
-- ---------------------------------------------------------------------------

 (10,6,'<mfa-passport-issued-lq@example.gov.cn>','Passport issued','no-reply@example.gov.cn','["linqiao@example.com"]','[]','[]','2021-11-18T10:00:00+08:00',
  'Your passport has been issued and is valid until 18 November 2031. The name printed is LIN QIAO. Please check that the spelling matches the name you use for airline bookings; airlines will not correct a mismatch after ticketing.',
  1,0,0,NULL,NULL,'{}',10,300,'2021-11-18T10:00:00+08:00'),

 (11,6,'<us-consulate-visa-expiry-lq@example.gov>','Your US B1/B2 visa has expired','no-reply@travel.example.gov','["linqiao@example.com"]','[]','[]','2024-11-01T09:00:00-05:00',
  'This is an automated notice. The B1/B2 visa issued to LIN QIAO expired on 31 October 2024. An expired visa cannot be used for entry or for transit through the United States. There is no transit-without-visa facility at US airports; all passengers connecting through the United States are admitted through immigration and therefore require a valid visa or an approved travel authorisation.

To travel through the United States you must apply again.',
  1,0,1,NULL,NULL,'{}',11,700,'2024-11-01T09:00:00-05:00'),

 (12,1,'<insurance-2026-policy-lq@example.com>','Travel insurance policy INS-2026-LQ-4471','policy@insure.example.com','["linqiao@example.com"]','[]','[]','2026-07-08T11:15:00+08:00',
  'Policy INS-2026-LQ-4471 is active for the period 10 August to 30 August 2026, single named insured: LIN QIAO.

Covered: medical treatment abroad, emergency repatriation, trip curtailment for medical reasons, baggage delay over 12 hours.
Not covered: travel companions who are not named on the policy, pre-existing conditions, and cancellation for change of plans.

The 24 hour assistance line is +86-400-820-0033. Quote the policy number.',
  0,0,0,NULL,NULL,'{}',12,650,'2026-07-08T11:15:00+08:00'),

 (13,1,'<hotelchain-loyalty-profile-xw@example.com>','Your Islas Verdes Collection membership profile','members@islasverdes.example.com','["linqiao@example.com"]','[]','[]','2026-05-22T08:00:00-06:00',
  'Thank you for enrolling a second guest in the Islas Verdes Collection.

Member: XU WEN
Tier: base
Enrolled by: LIN QIAO
Preferences on file: quiet room, high floor, late check-out when available.

Member benefits apply to the room, not to individual guests. Please review your profile details from time to time.',
  0,0,0,NULL,NULL,'{}',13,520,'2026-05-22T08:00:00-06:00'),

 (14,6,'<xuwen-2025-boat-trip@example.com>','That boat again','xuwen@example.com','["linqiao@example.com"]','[]','[]','2025-08-19T22:40:00+08:00',
  'I am never doing a two hour speedboat again. I was useless for the rest of the day and the tablets did nothing because I took them too late.

Next time: something short, something I can see land from, and I take the tablets an hour before, not when I already feel bad.',
  1,0,0,NULL,NULL,'{}',14,380,'2025-08-19T22:40:00+08:00'),

 (15,2,'<lq-2026-passport-check@example.com>','Passport details for the booking','linqiao@example.com','["xuwen@example.com"]','[]','[]','2026-07-14T20:10:00+08:00',
  'Send me a photo of your passport page again so I get the spelling right on the ticket. Yours has the middle name on it and mine does not, and I do not want to guess.

Also tell me now if you want to skip anything on the water so I can plan around it instead of arguing about it there.',
  1,0,0,NULL,NULL,'{}',15,340,'2026-07-14T20:10:00+08:00'),

 (16,1,'<xuwen-2026-passport-reply@example.com>','Re: Passport details for the booking','xuwen@example.com','["linqiao@example.com"]','[]','[]','2026-07-14T21:30:00+08:00',
  'Photo attached. It reads XU WEN CHENG, born 2 September 1989, valid to 22 June 2030.

And yes, please, nothing long on the water. Short crossings are fine if the sea is calm.',
  1,0,0,'<lq-2026-passport-check@example.com>','<lq-2026-passport-check@example.com>','{}',16,300,'2026-07-14T21:30:00+08:00'),

-- ---------------------------------------------------------------------------
-- Ordinary background traffic: a realistic inbox, not a keyword container.
-- ---------------------------------------------------------------------------

 (17,1,'<journal-review-request-lq@example.org>','Review request: manuscript MEE-2026-0417','editorial@marineecology.example.org','["linqiao@example.com"]','[]','[]','2026-07-16T19:00:00+02:00',
  'Dear Dr. Lin, we would value your opinion on manuscript MEE-2026-0417, on intertidal survey repeatability. The review window is four weeks. Please decline promptly if you cannot take it.',
  0,0,0,NULL,NULL,'{}',17,300,'2026-07-16T19:00:00+02:00'),

 (18,2,'<lq-review-decline@example.com>','Re: Review request: manuscript MEE-2026-0417','linqiao@example.com','["editorial@marineecology.example.org"]','[]','[]','2026-07-17T08:15:00+08:00',
  'I am travelling for most of August and would return the review late. Please pass it to someone else this time.',
  1,0,0,'<journal-review-request-lq@example.org>','<journal-review-request-lq@example.org>','{}',18,220,'2026-07-17T08:15:00+08:00'),

 (19,1,'<lab-freezer-alarm@example.edu>','Freezer 3 temperature alarm cleared','lab.ops@example.edu','["linqiao@example.com","lab-all@example.edu"]','[]','[]','2026-07-19T06:05:00+08:00',
  'The overnight alarm on freezer 3 was a door seal, not a compressor. Contents held at -78 C throughout. No samples affected. The seal has been replaced.',
  1,0,0,NULL,NULL,'{}',19,250,'2026-07-19T06:05:00+08:00'),

 (20,1,'<student-thesis-draft@example.edu>','Chapter 3 draft before you go','zhao.min@example.edu','["linqiao@example.com"]','[]','[]','2026-07-20T23:50:00+08:00',
  'Professor Lin, chapter 3 is attached. I have redone the seasonal decomposition the way you suggested and the residual structure is much cleaner. No rush while you are away.',
  0,0,0,NULL,NULL,'{}',20,290,'2026-07-20T23:50:00+08:00'),

 (21,1,'<airline-status-statement-lq@example.com>','Your frequent flyer statement','statements@skypass.example.com','["linqiao@example.com"]','[]','[]','2026-07-01T02:00:00+08:00',
  'Balance: 41,280 miles. Miles expiring in the next 12 months: 6,400. Award seats on long-haul routes to South America are limited and typically require booking several months ahead.',
  1,0,0,NULL,NULL,'{}',21,270,'2026-07-01T02:00:00+08:00'),

 (22,5,'<promo-cheap-flights@example.net>','SOUTH AMERICA FROM $499 THIS WEEK ONLY','deals@flightdeals.example.net','["linqiao@example.com"]','[]','[]','2026-07-18T04:00:00+00:00',
  'Unbeatable fares to South America. Limited seats. Book now. Terms apply. Routing and connection points at carrier discretion.',
  0,0,0,NULL,NULL,'{}',22,190,'2026-07-18T04:00:00+00:00'),

 (23,1,'<bank-card-travel-notice@example.com>','Travelling soon? Tell us first','service@bank.example.com','["linqiao@example.com"]','[]','[]','2026-07-21T10:00:00+08:00',
  'Cards used abroad may be held for verification, particularly for large first-time charges in an unfamiliar country. Letting us know your travel dates in advance reduces, but does not remove, the chance of a hold. Verification requests are sent to the address registered on the account.',
  0,0,0,NULL,NULL,'{}',23,420,'2026-07-21T10:00:00+08:00'),

 (24,1,'<pharmacy-order-ready@example.com>','Your order is ready for collection','orders@pharmacy.example.com','["linqiao@example.com"]','[]','[]','2026-07-22T13:30:00+08:00',
  'Order 88231 is ready: motion sickness tablets (2 packs), oral rehydration sachets, high factor sun cream. Please bring the collection code.',
  0,0,0,NULL,NULL,'{}',24,240,'2026-07-22T13:30:00+08:00'),

 (25,6,'<gdfo-2024-alumni-note@galapagos-data.example>','From the 2024 cohort','ops@galapagos-data.example','["participants@galapagos-data.example"]','[]','[]','2024-09-02T09:00:00-06:00',
  'Thank you all for a good week. The most common piece of feedback was the same as in 2023: arrive a day earlier than you think you need to. Every year somebody misses the first morning because of a connection.',
  1,0,0,NULL,NULL,'{}',25,320,'2024-09-02T09:00:00-06:00'),

 (26,1,'<santa-cruz-lodging-enquiry-reply@example.com>','Re: rooms in August','reservas@jardintranquilo.example.com','["linqiao@example.com"]','[]','[]','2026-07-11T17:45:00-06:00',
  'Good afternoon,

August is our busiest month. We hold a small number of flexible-rate rooms and release the rest as prepaid. Prepaid rooms are cheaper and cannot be refunded or moved.

We are about fifteen minutes on foot from the Marine Data Lab. Rooms at the front are lively in the evening; the garden side is quiet.

Reservas, Jardin Tranquilo',
  1,0,0,NULL,NULL,'{}',26,600,'2026-07-11T17:45:00-06:00'),

 (27,2,'<lq-lodging-enquiry@example.com>','rooms in August','linqiao@example.com','["reservas@jardintranquilo.example.com"]','[]','[]','2026-07-10T22:00:00+08:00',
  'Good evening, do you have a quiet double for two adults for the nights around 16 to 23 August? We would prefer something we can still change if our flights move.',
  1,0,0,NULL,NULL,'{}',27,250,'2026-07-10T22:00:00+08:00'),

 (28,1,'<ferry-operator-general-info@example.com>','Itabaca Channel crossing: general information','info@canaldeitabaca.example.com','["linqiao@example.com"]','[]','[]','2026-07-13T09:00:00-06:00',
  'Thank you for your enquiry. The channel crossing between Baltra and Santa Cruz is a short barge, a few minutes, and runs through the day in normal conditions. It is not a substitute for the road transfer on either side; allow for the bus, the crossing and the drive.

We do not take reservations. Crossings pause in bad weather.',
  1,0,0,NULL,NULL,'{}',28,470,'2026-07-13T09:00:00-06:00'),

 (29,1,'<parkservice-general-visitor-info@example.ec>','Visiting the Galapagos National Park','visitantes@parquegalapagos.example.ec','["linqiao@example.com"]','[]','[]','2026-06-28T12:00:00-06:00',
  'General visitor information.

Every visitor to the archipelago must hold a transit control card, obtained before boarding the domestic flight, and must pay the national park entrance fee. Both are per person and both are collected in cash at the airport in practice, although card terminals exist and sometimes work.

Rates are published by the ministry and are revised from time to time; check the current figures shortly before you travel rather than relying on an older itinerary.

No single-use plastics may be brought into the park.',
  1,0,0,NULL,NULL,'{}',29,780,'2026-06-28T12:00:00-06:00'),

 (30,1,'<embassy-ec-entry-general@example.gov>','Entry requirements for Ecuador','consular@example.gov','["linqiao@example.com"]','[]','[]','2026-06-30T15:00:00-05:00',
  'In reply to your enquiry: holders of ordinary Chinese passports do not require a visa for tourist stays in Ecuador within the published limit. A return or onward ticket and proof of accommodation may be requested on arrival.

Requirements for any country you transit are a separate matter and are set by that country, not by Ecuador.',
  1,0,0,NULL,NULL,'{}',30,520,'2026-06-30T15:00:00-05:00'),

 (31,1,'<airline-cx-baggage-policy@example.com>','Through-checked baggage on connecting itineraries','service@carrier-cx.example.com','["linqiao@example.com"]','[]','[]','2026-07-15T14:00:00+08:00',
  'In reply to your question: baggage is through-checked to the final destination when all sectors are held on a single ticket and the carriers have an interline arrangement. If sectors are bought separately, baggage is checked only to the end of the first ticket and you must clear customs and check in again.

Where a connection is made airside on a single ticket, no local entry permission is needed for the connecting airport, subject to that country''s own transit rules.',
  1,0,1,NULL,NULL,'{}',31,700,'2026-07-15T14:00:00+08:00'),

 (32,2,'<lq-baggage-question@example.com>','Through-checked baggage on connecting itineraries','linqiao@example.com','["service@carrier-cx.example.com"]','[]','[]','2026-07-15T09:20:00+08:00',
  'If I buy a multi-sector journey as one ticket, is the baggage checked all the way through, and do I need to enter the connecting country?',
  1,0,0,NULL,NULL,'{}',32,220,'2026-07-15T09:20:00+08:00'),

 (33,1,'<building-water-shutoff@example.com>','Water shut off 26 July, 09:00-15:00','property@example.com','["residents@example.com"]','[]','[]','2026-07-22T18:00:00+08:00',
  'Scheduled maintenance to the riser. Water will be off in block C on 26 July between 09:00 and 15:00. Please store what you need the night before.',
  0,0,0,NULL,NULL,'{}',33,230,'2026-07-22T18:00:00+08:00'),

 (34,1,'<conference-unrelated-cfp@example.org>','Call for abstracts: coastal resilience 2027','cfp@coastalresilience.example.org','["linqiao@example.com"]','[]','[]','2026-07-23T11:00:00+01:00',
  'Abstracts for the 2027 meeting are open until 15 November. Sessions on monitoring networks, community science and long time series are particularly encouraged.',
  0,0,0,NULL,NULL,'{}',34,260,'2026-07-23T11:00:00+01:00'),

 (35,6,'<gdfo-2026-badge-name-confirm@galapagos-data.example>','Badge name confirmation','ops@galapagos-data.example','["linqiao@example.com"]','[]','[]','2026-07-09T10:30:00-06:00',
  'Your badge will be printed as LIN QIAO, matching your passport. Badges are printed on the mainland and travel over with the coordinator, so corrections after 10 August cannot be made on the island.',
  1,0,0,NULL,NULL,'{}',35,340,'2026-07-09T10:30:00-06:00'),

 (36,1,'<xuwen-work-leave-approved@example.com>','Leave approved','xuwen@example.com','["linqiao@example.com"]','[]','[]','2026-07-17T12:10:00+08:00',
  'Leave approved for 14 to 25 August. I have to be back at work on the 26th, so the return on the 25th cannot slip.',
  1,0,0,NULL,NULL,'{}',36,200,'2026-07-17T12:10:00+08:00'),

 (37,1,'<credit-card-statement-jul@example.com>','Your July statement is ready','statements@bank.example.com','["linqiao@example.com"]','[]','[]','2026-07-20T03:00:00+08:00',
  'Your statement for the card ending 9012 is ready. Statement balance settled in full by direct debit. Available credit is sufficient for a large travel purchase, but individual foreign transactions above the usual pattern may still be referred for verification.',
  1,0,0,NULL,NULL,'{}',37,400,'2026-07-20T03:00:00+08:00'),

 (38,3,'<lq-draft-to-marisol@example.com>','(draft) arrival day','linqiao@example.com','["ops@galapagos-data.example"]','[]','[]','2026-07-23T22:00:00+08:00',
  'Marisol, I am still working out the flights. Once I know which day we land on the island I will tell you, in case anything about registration depends on it.',
  1,0,0,NULL,NULL,'{}',38,230,'2026-07-23T22:00:00+08:00');

-- Historical attachment and sent-message metadata; message ids 41+ remain free for stage mutations.
WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<20)
INSERT INTO attachments(message_id,filename,content_type,size,content_b64,content_id)
SELECT n,
       CASE n%10 WHEN 0 THEN 'meeting-agenda.pdf' WHEN 1 THEN 'lab-schedule.ics' WHEN 2 THEN 'policy-summary.pdf' WHEN 3 THEN 'packing-checklist.txt' WHEN 4 THEN 'expense-guide.pdf' WHEN 5 THEN 'seminar-notes.pdf' WHEN 6 THEN 'equipment-list.csv' WHEN 7 THEN 'insurance-contacts.pdf' WHEN 8 THEN 'hotel-map.png' ELSE 'reading-list.pdf' END,
       CASE n%4 WHEN 0 THEN 'text/plain' WHEN 1 THEN 'application/pdf' WHEN 2 THEN 'text/calendar' ELSE 'image/png' END,
       1200+n*73,NULL,printf('cid-history-%02d',n)
FROM seq;
WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<20)
INSERT INTO sent_log(message_id,sent_at)
SELECT 18+n,strftime('%Y-%m-%dT%H:%M:00+08:00','2026-05-20 08:00:00','+'||((n-1)*2)||' days','+'||(n%7)||' hours') FROM seq;
