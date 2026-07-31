-- Stage 17 mutation: the card issuer's verification request and the hotel's
-- pre-authorisation notice actually arrive in Lin Qiao's mailbox.
--
-- Before this stage these messages do not exist anywhere. The Stage-0 seed only
-- contains the bank's generic "cards used abroad may be held" leaflet (id 23),
-- which says a hold *can* happen; it does not say one *has* happened, to which
-- charge, or what the reference is.
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<bank-verify-9012-20260810@example.com>','Action needed: confirm a transaction on card ending 9012','security@bank.example.com','["linqiao@example.com"]','[]','[]','2026-08-10T01:25:00+08:00',
  'We have placed a transaction on hold pending your confirmation.

Reference: VRF-20260810-4471
Merchant: IBERIA / AIR TICKET SALES, ES
Amount: 1,480.00 USD
Card: ending 9012

This is larger than your usual pattern and is the first charge we have seen from this merchant, so it has not been passed to the merchant yet. The airline will not issue tickets until we release it.

Confirm or reject in the app, or reply to this message, within 72 hours. After 72 hours the request lapses, the hold is dropped and the merchant is told the transaction failed. If that happens the booking has to be made again at whatever fare is available then.

Nothing has left your account. A held transaction is not a payment.

Card Security',
  0,1,1,NULL,NULL,'{"X-Case-Ref":"VRF-20260810-4471"}',101,980,'2026-08-10T01:25:00+08:00'),

 (1,'<jardintranquilo-preauth-20260810@example.com>','Pre-authorisation for your August stay','reservas@jardintranquilo.example.com','["linqiao@example.com"]','[]','[]','2026-08-10T08:05:00-06:00',
  'Good morning,

As is standard for stays in August, we have taken a pre-authorisation of 180.00 USD against the card on file as a damage and incidentals deposit. This is a hold, not a charge: the amount is frozen on your card and is released after check-out, typically within seven to ten working days.

The room rate itself is not taken at this point. It is charged at check-out unless your rate is a prepaid one.

If you see the hold and the room charge at the same time on your statement, that is the expected appearance. Only one of the two will settle.

Reservas, Jardin Tranquilo',
  0,0,0,NULL,NULL,'{}',102,760,'2026-08-10T08:05:00-06:00'),

 (1,'<iberia-tkt-pending-20260810@carrier-ib.example.com>','Your booking is not yet ticketed','noreply@carrier-ib.example.com','["linqiao@example.com"]','[]','[]','2026-08-10T09:20:00+02:00',
  'Dear passenger,

Payment for the booking below has not completed. Your card issuer has not authorised the amount and we are holding the seats without a ticket.

Passengers: LIN QIAO, XU WEN CHENG
Fare held: 1,480.00 USD

Held seats are released automatically 72 hours after the booking is made if payment does not complete. Once released we cannot reinstate the same fare.

If your issuer contacts you about this transaction, confirming it is the fastest route. There is no need to make a second booking; a duplicate booking will be charged separately and only one can be refunded, at the fare rules of the ticket.

Iberia Customer Service',
  0,1,0,NULL,NULL,'{}',103,880,'2026-08-10T09:20:00+02:00'),

 (1,'<bank-declined-earlier-attempt@example.com>','A transaction on card ending 9012 was declined','security@bank.example.com','["linqiao@example.com"]','[]','[]','2026-08-10T01:11:00+08:00',
  'A transaction of 24.00 USD at GALAPAGOS TRANSIT CONTROL, EC was declined because the merchant terminal timed out. No funds were taken and no hold was placed.

If you were trying to pay, please try again or use another method. Repeated attempts at the same terminal within a short period sometimes appear on your statement as separate pending lines; these clear on their own.

Card Security',
  0,0,0,NULL,NULL,'{}',104,520,'2026-08-10T01:11:00+08:00');
