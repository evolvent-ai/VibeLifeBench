-- Curated live initial state for email/chen_yu_inbox.
BEGIN TRANSACTION;
INSERT INTO "account_config" ("id", "email", "name", "created_at") VALUES (1, 'chen.yu@gmail.com', 'Chen Yu', '2024-01-15T10:00:00Z');
INSERT INTO "folders" ("id", "name", "delimiter", "flags_json", "message_count", "unread_count") VALUES (1, 'INBOX', '/', '[]', 15, 3);
INSERT INTO "folders" ("id", "name", "delimiter", "flags_json", "message_count", "unread_count") VALUES (2, 'Sent', '/', '[]', 2, 0);
INSERT INTO "folders" ("id", "name", "delimiter", "flags_json", "message_count", "unread_count") VALUES (3, 'Drafts', '/', '[]', 0, 0);
INSERT INTO "folders" ("id", "name", "delimiter", "flags_json", "message_count", "unread_count") VALUES (4, 'Trash', '/', '[]', 0, 0);
INSERT INTO "folders" ("id", "name", "delimiter", "flags_json", "message_count", "unread_count") VALUES (5, 'Spam', '/', '[]', 0, 0);
INSERT INTO "folders" ("id", "name", "delimiter", "flags_json", "message_count", "unread_count") VALUES (6, 'Travel', '/', '[]', 2, 0);
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (1, 1, '<sprint-w22-7f31@gamestudio.com>', 'Sprint Planning - Week 22', 'dev-team@gamestudio.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-18T09:30:00Z', 'Team,

This week sprint planning:
- Game launch preparations
- Final testing and bug fixes
- Code freeze on June 7
- Launch date: June 8

Please review the task board.', NULL, 1, 0, 0, NULL, NULL, '{}', 1001, 1024, '2026-05-18T09:30:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (2, 1, '<pr456-review-89ab@gamestudio.com>', 'Code Review Request: Animation System', 'colleague@gamestudio.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-21T14:20:00Z', 'Hi Chen Yu,

Could you review my PR for the new animation system? It includes:
- Character movement optimization
- Collision detection improvements
- Performance benchmarks

Link: https://github.com/gamestudio/project/pull/456

Thanks!', NULL, 0, 0, 0, NULL, NULL, '{}', 1002, 2048, '2026-05-21T14:20:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (3, 1, '<launch-deadline-4c2e@gamestudio.com>', 'URGENT: Game Launch Deadline Reminder', 'project-manager@gamestudio.com', '["chen.yu@gmail.com","dev-team@gamestudio.com"]', '[]', '[]', '2026-05-20T16:45:00Z', 'Team,

Reminder: Game launch deadline is June 8.

Critical path:
- Code freeze: June 7
- Final QA: June 3-6
- Marketing assets: June 5

All features must be complete by June 1.', NULL, 1, 0, 0, NULL, NULL, '{}', 1003, 1536, '2026-05-20T16:45:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (4, 1, '<prenatal-20260603-cc71@meilin.gmail.com>', 'Prenatal Checkup Reminder', 'meilin@gmail.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-22T10:15:00Z', 'Please remember our prenatal checkup on June 3 at 10 AM. The doctor will perform an ultrasound examination.\n\nCan you come with me?\n\nLove,\nMeilin\n\n---\n\nDear,\n\nDon''t forget our prenatal checkup on June 3 at 10 AM. The doctor said we need to do an ultrasound.\n\nCan you come with me?\n\nLove you\nMeilin', NULL, 1, 0, 0, NULL, NULL, '{}', 1004, 896, '2026-05-22T10:15:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (5, 1, '<bali-planning-6a22@163.com>', 'About your Bali trip', 'liufang@163.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-19T19:30:00Z', 'Yu, I heard you are planning a Bali trip in June. I would like to join around June 22, but have not bought a ticket. Please compare daytime flights from Shanghai arriving in Denpasar; do not pay until I confirm my passport renewal.\n\nMom', NULL, 0, 0, 0, NULL, NULL, '{}', 1005, 768, '2026-05-19T19:30:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (6, 1, '<loyalty-profile-review@garuda-indonesia.example>', 'GarudaMiles profile review reminder', 'members@garuda-indonesia.example', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-15T08:20:00Z', 'Your GarudaMiles contact preferences have not been reviewed in twelve months. Sign in through the member portal to verify email and notification settings. This message is not a booking confirmation and contains no itinerary.', NULL, 1, 0, 0, NULL, NULL, '{}', 1006, 1730, '2026-05-15T08:20:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (7, 1, '<travel-cover-guide@axa-insurance.example>', 'Family travel cover guide updated for 2026', 'service@axa-insurance.example', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-17T11:45:00Z', 'The 2026 family travel cover guide now separates emergency treatment, routine care, trip interruption and pre-existing-condition review. Premiums and eligibility are supplied only after traveler details and dates are submitted; this notice is not a quote.', NULL, 1, 0, 0, NULL, NULL, '{}', 1007, 1840, '2026-05-17T11:45:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (8, 1, '<statement-202604-8456@cmb.com>', 'CMB Monthly Statement May 2026', 'statement@cmb.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-01T06:00:00Z', 'Dear Mr. Chen Yu,

Your CMB credit card statement for May 2026:

Billing cycle: 2026-04-01  to  2026-04-30
Amount due: ¥8,456.00
Due date: 2026-05-20

Major expenses:
- Online shopping：¥3,200
- Dining：¥1,800
- Transportation：¥890
- Other：¥2,566

---

Dear Mr. Chen Yu,

Your CMB credit card statement (May):

Billing cycle: 2026-04-01 to 2026-04-30
Amount due: ¥8,456.00
Due date: 2026-05-20

Major expenses:
- Online shopping: ¥3,200
- Dining: ¥1,800
- Transportation: ¥890
- Other: ¥2,566', NULL, 1, 0, 0, NULL, NULL, '{}', 1008, 2048, '2026-05-01T06:00:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (9, 1, '<teambuild-jun5-rsvp@gamestudio.com>', 'Team Building Activity - June 5', 'hr@gamestudio.com', '["chen.yu@gmail.com","all-staff@gamestudio.com"]', '[]', '[]', '2026-04-28T13:00:00Z', 'Hi Team,

We are organizing a team building activity on June 5 (afternoon):
- Location: Riverside Park
- Activities: BBQ, games, team challenges
- Time: 14:00 - 18:00

Please RSVP by May 15.

HR Team', NULL, 1, 0, 0, NULL, NULL, '{}', 1009, 1280, '2026-04-28T13:00:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (10, 1, '<answer-12345678-5e91@stackoverflow.com>', 'Your question about Unity optimization has a new answer', 'noreply@stackoverflow.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-12T22:30:00Z', 'Someone answered your question: "How to optimize character rendering in Unity for mobile?"

View answer: https://stackoverflow.com/questions/12345678', NULL, 1, 0, 0, NULL, NULL, '{}', 1010, 640, '2026-05-12T22:30:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (11, 1, '<actions-1234-ab12cd34@github.com>', '[gamestudio/project] Build failed on main branch', 'notifications@github.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-14T16:20:00Z', 'Build #1234 failed

Branch: main
Commit: ab12cd34
Error: Unit test failure in AnimationController

View logs: https://github.com/gamestudio/project/actions/runs/1234', NULL, 1, 0, 0, NULL, NULL, '{}', 1011, 1024, '2026-05-14T16:20:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (12, 1, '<booking-account-security@booking.example>', 'Sign-in alert for your lodging account', 'security@booking.example', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-16T15:30:00Z', 'A sign-in from Shanghai was recorded for your lodging account. If this was you, no action is needed. No reservation was created or changed during this session.', NULL, 1, 1, 0, NULL, NULL, '{}', 1012, 1420, '2026-05-16T15:30:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (13, 1, '<event-123-sh-gamedev@meetup.com>', 'Shanghai Game Developers Meetup - May 30', 'events@meetup.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-10T09:00:00Z', 'Join us for the Shanghai Game Developers Meetup!

Date: May 30, 2026
Time: 19:00 - 21:00
Location: TechHub Shanghai
Topics: AI in Game Development, Mobile Gaming Trends

RSVP: https://meetup.com/shanghai-gamedev/event/123', NULL, 1, 0, 0, NULL, NULL, '{}', 1013, 1152, '2026-05-10T09:00:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (14, 1, '<network-digest-3req-2d8c@linkedin.com>', 'You have 3 new connection requests', 'messages@linkedin.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-20T11:00:00Z', 'Hi Chen Yu,

You have 3 new connection requests:
- Li Wei (Senior Game Developer at Tencent)
- Zhang Hua (Unity Engineer at NetEase)
- Sarah Johnson (Game Designer at EA)

View requests: https://linkedin.com/mynetwork', NULL, 1, 0, 0, NULL, NULL, '{}', 1014, 896, '2026-05-20T11:00:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (15, 1, '<shipment-112-8901234@amazon.com>', 'Your Amazon order has been shipped', 'ship-confirm@amazon.com', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-11T14:40:00Z', 'Hello Chen Yu,

Your order #112-1234567-8901234 has been shipped:

Items:
- Sunscreen SPF 50+ (2 bottles)
- Travel adapter universal plug
- Waterproof phone case

Tracking: SF1234567890
Expected delivery: May 15, 2026', NULL, 1, 0, 0, NULL, NULL, '{}', 1015, 1408, '2026-05-11T14:40:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (16, 2, '<sent001@gmail.com>', 'Re: About your Bali trip', 'chen.yu@gmail.com', '["liufang@163.com"]', '[]', '[]', '2026-05-20T08:15:00Z', 'Mom, understood.I will compare flexible daytime flights and entry documents, then book after you confirm the new passport details. No ticket has been issued for you, and I will not send passport numbers by email.\n\nYu', NULL, 1, 0, 0, NULL, NULL, '{}', 2001, 640, '2026-05-20T08:15:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (17, 2, '<sent002@gmail.com>', 'Re: Prenatal Checkup Reminder', 'chen.yu@gmail.com', '["meilin@gmail.com"]', '[]', '[]', '2026-05-22T11:00:00Z', 'Dear,

Of course I will come with you. I added the June 3, 10 AM appointment to the calendar.

We will go together.

 Love,
Yu

---

Dear,

Of course, I will go with you. Already marked June 3 at 10 AM on the calendar.

Let''s go together.

Love you
Yu', NULL, 1, 0, 0, NULL, NULL, '{}', 2002, 512, '2026-05-22T11:00:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (18, 6, '<bali-route-news@garuda-indonesia.example>', 'June network timetable newsletter', 'updates@garuda-indonesia.example', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-15T08:20:00Z', 'The June network newsletter summarizes published Southeast Asia schedules and reminds travelers that equipment, fares and seats can change before purchase. Use the booking search for current availability; this newsletter does not hold a seat.', NULL, 1, 0, 0, NULL, NULL, '{}', 6001, 1900, '2026-05-15T08:20:00Z');
INSERT INTO "messages" ("id", "folder_id", "message_id", "subject", "from_addr", "to_addr_json", "cc_addr_json", "bcc_addr_json", "date", "body_text", "body_html", "is_read", "is_important", "is_flagged", "in_reply_to", "references_header", "headers_json", "uid", "size", "created_at") VALUES (19, 6, '<privacy-update@axa-insurance.example>', 'Insurance account privacy controls', 'privacy@axa-insurance.example', '["chen.yu@gmail.com"]', '[]', '[]', '2026-05-17T11:45:00Z', 'You can now remove uploaded identity documents from expired applications while retaining payment receipts. No active policy or premium is associated with this account notice.', NULL, 1, 0, 0, NULL, NULL, '{}', 6002, 1510, '2026-05-17T11:45:00Z');
COMMIT;
