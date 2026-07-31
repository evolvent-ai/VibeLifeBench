-- Stage 9 mutation: the carriers respond to the ash situation. Before this
-- stage the environment holds the ash alert itself (stage 8) but nothing from
-- any airline: no waiver, no window, no rebooking terms.
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<klm-waiver-uio-20260802@carrier-kl.example.com>','Flexibility for travel via Quito','noreply@carrier-kl.example.com','["linqiao@example.com"]','[]','[]','2026-08-02T17:20:00+02:00',
  'Notice to passengers holding or considering travel through Quito.

Because of ash activity affecting operations at UIO, we are waiving the change fee on itineraries touching Quito between 14 and 18 August. Affected passengers may move the date or change the Ecuadorian arrival point at no charge, subject to availability in the original booking class.

The waiver window closes 24 hours from this notice. After that, normal fare rules apply and a change is repriced at the fare available on the day.

We are still operating. A waiver is not a cancellation and we are not able to tell you in advance whether any individual departure will run.

Passengers connecting onward to the islands should note that a delay into Quito of more than about two hours will not leave time for the following morning''s domestic departure, as there is only one useful wave.

KLM Customer Service',
  0,1,0,NULL,NULL,'{}',51,1150,'2026-08-02T17:20:00+02:00'),

 (1,'<avianca-domestic-notice-20260802@carrier-av.example.com>','Galapagos services: schedule note','noreply@carrier-av.example.com','["linqiao@example.com"]','[]','[]','2026-08-02T18:05:00-05:00',
  'Passengers travelling to the Galapagos.

Domestic services to the islands depart in the morning only. There is no afternoon departure. Passengers arriving on the mainland after roughly 22:00 should plan an overnight rather than an immediate connection.

Services from Guayaquil are not affected by the current Quito situation. Guayaquil is the closer of the two mainland gateways to the islands and its services are running to schedule.

Avianca',
  0,0,0,NULL,NULL,'{}',52,620,'2026-08-02T18:05:00-05:00'),

 (1,'<iberia-gye-note-20260802@carrier-ib.example.com>','Your enquiry about arrival points in Ecuador','service@carrier-ib.example.com','["linqiao@example.com"]','[]','[]','2026-08-02T20:40:00+02:00',
  'Thank you for your enquiry.

We serve both Ecuadorian gateways from Madrid. Both are on the same aircraft type and the same through-check arrangement applies.

Whether one arrival point is better than the other for your onward domestic connection is a question about the domestic carrier''s schedule, not about our service, and we cannot advise on it.

Changes to a held booking that has not yet been ticketed carry no fee. Once ticketed, the fare rules of the ticket apply.

Iberia Customer Service',
  0,0,0,NULL,NULL,'{}',53,700,'2026-08-02T20:40:00+02:00');
