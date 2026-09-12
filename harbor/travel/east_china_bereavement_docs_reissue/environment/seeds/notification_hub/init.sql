-- Reviewed notification history: 45 distinct account/subscription/post/message records.
INSERT INTO official_accounts(account_id,name,category,description) VALUES
 ('acct_order_watch','family itinerary order monitor','travel','scenario textordersscenario textstatusscenario text。'),
 ('acct_doc_watch','document materials reminder','documents','scenario textdocumentsscenario textServicescenario text。'),
 ('acct_city_service','city public services','government','scenario text、service windowscenario textServicescenario text。'),
 ('acct_family_care','family care assistant','care','scenario textelderscenario text、scenario textreminder。');
INSERT INTO official_account_subscriptions(user_id,account_id,subscribed_at) VALUES
 ('user_lin_che','acct_order_watch','2025-01-01T09:00:00+08:00'),('user_lin_che','acct_doc_watch','2025-01-02T09:00:00+08:00'),
 ('user_lin_che','acct_city_service','2025-01-03T09:00:00+08:00'),('user_lin_che','acct_family_care','2025-01-04T09:00:00+08:00');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<12)
INSERT INTO official_account_posts(post_id,account_id,title,summary,url,published_at)
SELECT printf('post_service_%02d',n),CASE n%4 WHEN 0 THEN 'acct_order_watch' WHEN 1 THEN 'acct_doc_watch' WHEN 2 THEN 'acct_city_service' ELSE 'acct_family_care' END,
       CASE n WHEN 1 THEN 'pre-departure rail checklist' WHEN 2 THEN 'minimum document-sharing rule' WHEN 3 THEN 'government-window appointment reminder' WHEN 4 THEN 'elder meeting template' WHEN 5 THEN 'hotel cancellation deadline log' WHEN 6 THEN 'flight status review point' WHEN 7 THEN 'road construction detour note' WHEN 8 THEN 'sensitive-email domain verification' WHEN 9 THEN 'separate waitlist and refund states' WHEN 10 THEN 'large-print e-ticket points' WHEN 11 THEN 'expense ledger categories' ELSE 'post-trip data cleanup' END,
       CASE n WHEN 1 THEN 'before departureverifyscenario text、scenario text、scenario text。' WHEN 2 THEN 'scenario text，scenario text。' WHEN 3 THEN 'appointment numberscenario text、placesscenario texttimescenario textreminder。' WHEN 4 THEN 'scenario text、scenario texttime、scenario text。' WHEN 5 THEN 'scenario texttime、Timezonescenario textexpense。' WHEN 6 THEN 'scenario text、scenario text。' WHEN 7 THEN 'constructionscenario texttimescenario textroute。' WHEN 8 THEN 'unknownscenario textrequestingscenario text。' WHEN 9 THEN 'scenario text、scenario textstatus。' WHEN 10 THEN 'scenario text、scenario text、timescenario text。' WHEN 11 THEN 'scenario text、scenario text、scenario textfamilyscenario text。' ELSE 'cleanupscenario text，scenario textauthorizationscenario text。' END,
       printf('https://service.example.test/posts/%02d',n),strftime('%Y-%m-%dT09:00:00+08:00','2026-02-01','+'||(n-1)||' days')
FROM seq;

INSERT INTO subscriptions(subscription_id,user_id,source,type,target,condition_json,status,created_at,updated_at) VALUES
 ('sub_train_status','user_lin_che','rail_booking','policy_update','scenario textorders','{"channel":"in_app"}','active','2025-12-01T09:00:00+08:00','2026-03-01T09:00:00+08:00'),
 ('sub_flight_status','user_lin_che','flight_booking','price_drop','scenario text','{"currency":"CNY"}','active','2025-12-02T09:00:00+08:00','2026-03-02T09:00:00+08:00'),
 ('sub_hotel_terms','user_lin_che','hotel_booking','policy_update','scenario text','{"refundable":true}','active','2025-12-03T09:00:00+08:00','2026-03-03T09:00:00+08:00'),
 ('sub_city_route','user_lin_che','maps','keyword','scenario text','{"cities":["Beijing","Shanghai","Suzhou","Ningbo"]}','active','2025-12-04T09:00:00+08:00','2026-03-04T09:00:00+08:00'),
 ('sub_document_rules','user_lin_che','legal_search','new_content','scenario text','{"language":"zh"}','active','2025-12-05T09:00:00+08:00','2026-03-05T09:00:00+08:00');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<20)
INSERT INTO notifications(notification_id,user_id,source,type,subscription_id,title,body,payload_json,created_at,read)
SELECT printf('notification_history_%03d',n),'user_lin_che',
       CASE n%5 WHEN 0 THEN 'rail_booking' WHEN 1 THEN 'flight_booking' WHEN 2 THEN 'hotel_booking' WHEN 3 THEN 'maps' ELSE 'legal_search' END,
       CASE n%5 WHEN 0 THEN 'policy_update' WHEN 1 THEN 'price_drop' WHEN 2 THEN 'policy_update' WHEN 3 THEN 'keyword' ELSE 'new_content' END,
       CASE n%5 WHEN 0 THEN 'sub_train_status' WHEN 1 THEN 'sub_flight_status' WHEN 2 THEN 'sub_hotel_terms' WHEN 3 THEN 'sub_city_route' ELSE 'sub_document_rules' END,
       CASE n%10 WHEN 0 THEN 'scenario textServicetimescenario text' WHEN 1 THEN 'scenario textpricesscenario text' WHEN 2 THEN 'scenario text' WHEN 3 THEN 'scenario text' WHEN 4 THEN 'scenario textServicescenario text' WHEN 5 THEN 'scenario text' WHEN 6 THEN 'scenario textreminder' WHEN 7 THEN 'scenario text' WHEN 8 THEN 'scenario texttime' ELSE 'scenario text' END,
       CASE n%10 WHEN 0 THEN 'scenario textServiceservice windowscenario texttimescenario text，before departurescenario text。' WHEN 1 THEN 'scenario textpricesscenario text，scenario text。' WHEN 2 THEN 'scenario texttimescenario text，scenario textordersscenario text。' WHEN 3 THEN 'scenario text，scenario text。' WHEN 4 THEN 'scenario text，scenario textdocumentsscenario textverify。' WHEN 5 THEN 'scenario text，scenario textstatus。' WHEN 6 THEN 'scenario text，scenario textverifyscenario text。' WHEN 7 THEN 'scenario text，scenario text。' WHEN 8 THEN 'scenario texttimescenario text，scenario text。' ELSE 'Servicescenario text。' END,
       json_object('record',n,'action','review_when_relevant'),strftime('%Y-%m-%dT%H:00:00+08:00','2026-03-01 08:00:00','+'||(n-1)||' days','+'||(n%8)||' hours'),CASE WHEN n%4=0 THEN 0 ELSE 1 END
FROM seq;
