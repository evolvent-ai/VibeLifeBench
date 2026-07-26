-- Stage 20 mutation: the property's pre-arrival message. It is a real email in
-- the mailbox, not a floating notification, and it asks for something concrete
-- (an arrival time) that can only be answered from the flight status.
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<jardintranquilo-prearrival@example.com>','Before you arrive','reservas@jardintranquilo.example.com','["linqiao@example.com"]','[]','[]','2026-08-16T15:10:00-06:00',
  'Good afternoon,

We are expecting you today. Three things before you get here.

Arrival time. Reception is staffed until 22:00. After that the night bell is answered but the wait can be twenty minutes or more. If you know roughly when you will reach town, tell us and we will watch for you.

Room. You asked for the garden side. We have held one for you. The front rooms are the ones people complain about in August; you were right to ask.

Deposit. The incidentals hold we placed on the card last week stands until you check out. It is not a charge and nothing further is taken on arrival.

We do not run a transfer from the airport ourselves and we would not recommend waiting for a taxi at the pier at that hour. The certified operators book up; if you have not arranged one, do it before you land rather than after.

Reservas, Jardin Tranquilo',
  0,0,0,NULL,NULL,'{}',131,1050,'2026-08-16T15:10:00-06:00');
