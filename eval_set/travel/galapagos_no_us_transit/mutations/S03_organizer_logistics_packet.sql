-- Stage 3 mutation: the logistics note the coordinator promised in the
-- invitation ("a separate logistics note ... will follow closer to the date")
-- finally arrives.
--
-- Stage 1 calendar is the first exact registration cut-off release. This
-- Stage 3 organizer email independently corroborates that deadline and adds
-- the operational details needed for travel verification. Before Stage 3 the
-- mailbox only has the 6 July reply saying the time is "still being finalised".
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<gdfo-2026-logistics-note@galapagos-data.example>','Logistics note, 2026 workshop','ops@galapagos-data.example','["linqiao@example.com","participants@galapagos-data.example"]','[]','[]','2026-07-27T09:15:00-06:00',
  'Dear all,

The logistics note I promised.

Venue. Puerto Ayora Marine Data Lab, Avenida Charles Darwin 102, Puerto Ayora, Santa Cruz.

Registration. In person at the venue desk. The desk is open on 17 August from 10:00 and closes at 18:00 island time. That is the cut-off. There is no desk on the morning of the 18th; badges are printed on the mainland and I bring them over on the 10th, so anything not collected by 18:00 on the 17th sits in a box until I am back at the venue on the 18th at nine, by which time the opening session has started.

Arrival. Please be on the island by the evening of the 16th. Every year somebody plans to land on the 17th and every year at least one of them does not make it, because the mainland-to-island flights go in the morning and there is only one useful wave of them.

Getting to town. The island airport is on Baltra, not Santa Cruz. From the aircraft it is a shuttle bus, then the channel barge, then a road transfer, and the whole thing is not quick. Allow much more than you think.

Island entry. There are two charges collected from every visitor, one before you board on the mainland and one when you land. Current rates are on the park service site; they are revised periodically so please check them rather than copying an old itinerary. Cash is the practical answer on the island.

Accommodation. We do not book for participants. August is full; do not leave it.

Marisol Aguirre
Programme Coordinator',
  0,1,0,'<gdfo-2026-invite-lq@galapagos-data.example>','<gdfo-2026-invite-lq@galapagos-data.example>','{}',41,1900,'2026-07-27T09:15:00-06:00'),

 (1,'<gdfo-2026-badge-list@galapagos-data.example>','Badge list, please check your entry','ops@galapagos-data.example','["linqiao@example.com"]','[]','[]','2026-07-27T09:22:00-06:00',
  'Your entry on the badge list reads:

LIN QIAO -- participant -- bench 7

Accompanying, not a participant, no badge: XU WEN CHENG

If the spelling does not match the passport you will travel on, tell me before the 10th. The desk checks the badge against the passport and I have no way to reprint on the island.

Marisol',
  0,1,1,NULL,NULL,'{}',42,560,'2026-07-27T09:22:00-06:00');
