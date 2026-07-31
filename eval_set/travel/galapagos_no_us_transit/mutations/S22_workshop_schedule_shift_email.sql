-- Stage 22 mutation: the organiser's schedule change lands in the mailbox.
--
-- The day-three outdoor transect is moved; a shore-based alternative is offered
-- and there is a small charge for the reserve entry that comes with it. None of
-- this is knowable before the marine warning verifies on 20 August, so none of
-- it exists in the seed. The seed only says the transect "depends on marine
-- conditions" (message 4, the June draft programme).
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<gdfo-2026-transect-moved@galapagos-data.example>','Change to Thursday: transect is off the water','ops@galapagos-data.example','["linqiao@example.com","participants@galapagos-data.example"]','[]','[]','2026-08-20T07:30:00-06:00',
  'All,

The port captain has the marine warning in force through Friday, so the boat-supported leg of Thursday''s transect is cancelled. We are not going out.

The session runs instead as a shore transect from Tortuga Bay, walked from the trailhead, followed by data cleaning in the lab in the afternoon. Same content, same datasets, no boat.

The walk to the trailhead is about forty minutes each way in full sun. Bring water, a hat and closed shoes. There is no shade at the far end and there is nowhere to buy anything.

Anyone who booked the optional Sunday excursion separately should speak to their operator directly; we have no arrangement with them.

Partners and guests are welcome on the shore walk. There is a reserve entry charge of 12 USD per person for anyone who is not a registered participant, collected at the trailhead in cash. Participants are covered by the programme.

Marisol Aguirre',
  0,1,0,NULL,NULL,'{}',111,1180,'2026-08-20T07:30:00-06:00'),

 (1,'<portcaptain-marine-warning@example.ec>','Marine warning: Santa Cruz and Baltra channel','capitania@puertoayora.example.ec','["operadores@puertoayora.example.ec","linqiao@example.com"]','[]','[]','2026-08-20T06:10:00-06:00',
  'Marine warning in force from 20 August 06:00 until further notice.

Small craft movements between Santa Cruz and the outer islands are suspended. The Itabaca Channel barge continues to operate on a reduced timetable at the discretion of the operator; expect waits.

Operators must not carry passengers on open-water routes while the warning stands. Bookings affected by this notice are refundable under the standard regulation.

Capitania de Puerto, Puerto Ayora',
  0,0,0,NULL,NULL,'{}',112,660,'2026-08-20T06:10:00-06:00'),

 (1,'<islandtours-refund-offer@example.com>','Your Sunday excursion: options','reservas@islandtours.example.com','["linqiao@example.com"]','[]','[]','2026-08-20T10:40:00-06:00',
  'Good morning,

Because of the port captain''s notice we are not sailing this week. Your enquiry for the 23 August excursion has not been confirmed and no payment has been taken, so there is nothing for us to refund.

If conditions improve we will contact anyone still holding a place. We are not taking new bookings while the warning stands.

Reservas, Island Tours',
  0,0,0,NULL,NULL,'{}',113,520,'2026-08-20T10:40:00-06:00');
