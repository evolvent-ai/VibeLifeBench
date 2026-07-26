-- Stage 14 mutation: the park service publishes its current rates in answer to
-- the enquiry, and the coordinator forwards the practical island-entry note.
--
-- Before this stage the environment says only that "two charges are collected
-- from every visitor" and that "rates are published by the ministry and are
-- revised from time to time; check the current figures" (seed message 29 and
-- the stage-3 logistics note). The actual numbers exist for the first time
-- here.
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<parkservice-current-rates-2026@example.ec>','Current rates, as requested','visitantes@parquegalapagos.example.ec','["linqiao@example.com"]','[]','[]','2026-08-07T10:20:00-06:00',
  'In reply to your enquiry about the figures in force this season.

The transit control card is 20 US dollars per person. It is issued at the mainland airport, before the domestic departure, and cannot be bought once you have landed on the islands.

The park entrance fee for foreign adult visitors is 100 US dollars per person, collected on arrival at the island airport.

Both charges apply to every visitor. There is no exemption for an accompanying visitor and no reduction for a conference delegate.

Card terminals exist at both points and fail often; the queue does not wait for a retry. Bring the amount in cash, in small notes. Keep both receipts. They are the only proof of payment and neither office reissues one.

No single-use plastics may be brought into the park. Bottles are checked at the island airport.

Parque Nacional Galapagos',
  0,1,0,NULL,NULL,'{}',81,1100,'2026-08-07T10:20:00-06:00'),

 (1,'<gdfo-2026-arrival-practicalities@galapagos-data.example>','Landing day: what actually happens','ops@galapagos-data.example','["linqiao@example.com","participants@galapagos-data.example"]','[]','[]','2026-08-07T11:00:00-06:00',
  'For those who have not done this route before, the sequence on the day you fly out to the islands.

At the mainland airport, before you check in, there is a separate counter where the transit card is issued. It opens two hours before the domestic departure and the queue is long. Your bag is screened there as well.

On landing, the entrance fee is collected in the arrivals hall before you reach the bags. Cash. Then the shuttle to the barge, the barge, and the road transfer into town.

Budget several hours between wheels down and being in Puerto Ayora. People who allow ninety minutes are the ones who arrive after the desk has shut.

Partners and guests go through exactly the same two counters and pay exactly the same two charges. The programme does not cover them and I cannot get them through on my list.

Marisol',
  0,0,0,NULL,NULL,'{}',82,1150,'2026-08-07T11:00:00-06:00'),

 (1,'<bank-fx-cash-advice@example.com>','Using your card and cash abroad','service@bank.example.com','["linqiao@example.com"]','[]','[]','2026-08-07T09:40:00+08:00',
  'Ahead of your travel dates, a note on cash.

Cash withdrawals abroad carry a 3 per cent fee with a minimum charge, so several small withdrawals cost noticeably more than one larger one. Withdrawals in a currency other than the local one are converted twice.

Where a merchant offers to charge you in your home currency, decline: their rate is worse than ours.

We cannot guarantee that any individual terminal or machine will accept the card. Carry enough of the local currency for anything that must be paid on the spot, and be aware that some destinations are effectively cash-only despite what the guidebooks say.

Bank Customer Service',
  0,0,0,NULL,NULL,'{}',83,860,'2026-08-07T09:40:00+08:00');
