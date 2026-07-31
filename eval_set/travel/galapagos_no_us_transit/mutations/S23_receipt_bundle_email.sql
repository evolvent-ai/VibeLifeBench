-- Stage 23 mutation: the paperwork lands as the trip closes.
--
-- These are real documents that only exist once the services were consumed:
-- the hotel's closing invoice, the two island-entry receipts, the transfer
-- operator's receipt, and the card issuer's statement of what actually settled
-- versus what is still held. None of it can exist earlier.
--
-- SQLite allocates message primary keys at apply time so prior agent sends cannot collide.

INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (1,'<jardintranquilo-invoice-final@example.com>','Invoice for your stay','reservas@jardintranquilo.example.com','["linqiao@example.com"]','[]','[]','2026-08-23T19:20:00-06:00',
  'Thank you for staying with us.

Invoice JT-2026-0823-114
Guests: LIN QIAO, XU WEN CHENG
Nights: 16 to 23 August, 7 nights, garden-side double

Room, 7 nights at the double rate: 1,575.00 USD
Single-occupancy rate for the same room and dates, for your records: 1,190.00 USD
Breakfast, not included in the rate, 7 x 2 covers: 168.00 USD
Laundry: 22.00 USD

Total charged to the card ending 9012 at check-out: 1,765.00 USD

The 180.00 USD incidentals hold placed on 10 August has been released today. Your issuer decides when it clears; it is typically seven to ten working days and we have no visibility of it.

Reservas, Jardin Tranquilo',
  0,1,0,NULL,NULL,'{}',121,1100,'2026-08-23T19:20:00-06:00'),

 (1,'<parkservice-receipt-pair@example.ec>','Your receipts','recibos@parquegalapagos.example.ec','["linqiao@example.com"]','[]','[]','2026-08-16T12:40:00-06:00',
  'Duplicate copies of the receipts issued to you, as requested at the counter.

Receipt PNG-2026-208841: entrance fee, 100.00 USD, LIN QIAO, paid in cash 16 August.
Receipt PNG-2026-208842: entrance fee, 100.00 USD, XU WEN CHENG, paid in cash 16 August.

Receipts are issued per person and cannot be combined. Please retain them; we do not reissue.

Parque Nacional Galapagos',
  0,0,0,NULL,NULL,'{}',122,620,'2026-08-16T12:40:00-06:00'),

 (1,'<tct-counter-receipt@example.ec>','Transit control card - receipts','tct@ingala.example.ec','["linqiao@example.com"]','[]','[]','2026-08-16T06:15:00-05:00',
  'Transit control cards issued.

TCT-2026-771203, LIN QIAO, 20.00 USD, paid in cash.
TCT-2026-771204, XU WEN CHENG, 20.00 USD, paid in cash.

Cards must be surrendered at the island airport on departure. Keep the receipt: it is separate from the card and is what you will need for any claim.',
  0,0,0,NULL,NULL,'{}',123,560,'2026-08-16T06:15:00-05:00'),

 (1,'<baltra-transfer-receipt@example.ec>','Transfer receipt','reservas@transfersantacruz.example.ec','["linqiao@example.com"]','[]','[]','2026-08-16T14:50:00-06:00',
  'Receipt TSC-2026-4417.

Certified airport transfer, Baltra to Puerto Ayora, 16 August, 2 seats.
Rate per seat: 35.00 USD. Total: 70.00 USD. Paid by card.

The return leg on 23 August is on the same booking and is included in the figure above.

Transfers Santa Cruz',
  0,0,0,NULL,NULL,'{}',124,500,'2026-08-16T14:50:00-06:00'),

 (1,'<bank-statement-travel-window@example.com>','Card activity summary, 10 to 23 August','statements@bank.example.com','["linqiao@example.com"]','[]','[]','2026-08-23T20:10:00-06:00',
  'Summary for the card ending 9012 covering 10 to 23 August.

Settled:
  1,480.00 USD  IBERIA / AIR TICKET SALES, ES        settled 11 August
  1,765.00 USD  JARDIN TRANQUILO, EC                 settled 23 August
     70.00 USD  TRANSFERS SANTA CRUZ, EC             settled 16 August

Still held, not settled:
    180.00 USD  JARDIN TRANQUILO, EC                 hold placed 10 August, release instructed 23 August

Declined, no funds taken:
     24.00 USD  GALAPAGOS TRANSIT CONTROL, EC        10 August

A release can take up to ten working days to leave your available balance. A held amount is not a payment and does not appear on your statement as one.

Bank Customer Service',
  0,1,0,NULL,NULL,'{}',125,1150,'2026-08-23T20:10:00-06:00'),

 (1,'<carrier-ib-itinerary-receipt@carrier-ib.example.com>','Itinerary receipt','noreply@carrier-ib.example.com','["linqiao@example.com"]','[]','[]','2026-08-23T21:00:00-06:00',
  'Itinerary receipt for your records.

Passengers: LIN QIAO, XU WEN CHENG
Total fare, both passengers, all sectors: 1,480.00 USD
Payment: card ending 9012, settled 11 August 2026
Ticket status: flown outbound, valid for return

Your employer will normally want a fare breakdown per passenger. It is on the passenger receipts attached to each coupon, not on this document.

Iberia',
  0,0,0,NULL,NULL,'{}',126,660,'2026-08-23T21:00:00-06:00');
