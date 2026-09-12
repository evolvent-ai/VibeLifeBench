#        — east_asia_group_trip_24d

   provide   8   mock   ，           initialize    mcp-session-id。

    ：
- `flight_booking_mock` — flight  、  、  、  、check-in、status  
- `hotel_booking_mock` — hotel  、  、    、  please 
- `banking_mock` — accountbalance、    、transfer、repayment、payee   
- `health_tracker_mock` —     record、blood pressure  、    、    
- `visa_and_advisory_mock` —   requirements  、travel advisory  、visa  
- `email_mock` — email  、  、  、  
- `calendar_mock` —       、  、  、    
- `notion_mock` —     、block     、  

---

## 1. `flight_booking_mock` — flight  

**    **
- `search_flights(origin, destination, departure_date, adults, cabin, non_stop)` —   flight offer
- `price_offer(offer_id)` —   （       ，      ）
- `create_booking(offer_id, passengers, contact, payment)` —   
- `get_booking(pnr)` —       
- `list_bookings(user_id)` —           
- `get_flight_status(flight_no, date)` —     flightstatus（cancelled/delayed/scheduled）
- `change_booking(pnr, new_offer_id)` —   
- `check_in(pnr, segment_idx)` — check-in（T-48h   T-45min      ）
- `get_seat_map(offer_id)` —    

**note**
-        `price_offer`   `create_booking`，         。
- check-in     ：    48h      45min，          。
-         banking_mock confirm    。
-                ：return   （`isError:true` +   ），  JSON code   。

## 2. `hotel_booking_mock` — hotel  

**    **
- `search_hotels(city_or_geo, check_in, check_out, guests)` —   hotel
- `get_hotel_details(hotel_id)` — hotel  （  、   ）
- `get_room_availability(hotel_id, check_in, check_out, guests)` —    
- `create_reservation(rate_plan_id, guest_profile, payment_method_id)` —     
  - `guest_profile`     ：`{"user_id": ..., "first_name": ..., "last_name": ...}`
- `get_reservation(reservation_id)` —       
- `list_reservations(user_id)` —       
- `modify_reservation(reservation_id, ...)` —     
- `cancel_reservation(reservation_id)` —     
- `submit_special_request(reservation_id, text)` —     please （lost property/  /   ）

**note**
-           `RES_NOT_FOUND`（  RESERVATION_NOT_FOUND）。
-      `guest_profile`      `user_id`、`first_name`、`last_name`，    。

## 3. `banking_mock` —     

**    **
- `list_accounts(user_id)` —     account（   account_id     ）
- `get_account(account_id)` — account  （balance、frozen status）
- `list_transactions(account_id, since=None, until=None, limit=50, kind_filter=None)` —     
- `transfer(from_account_id, to_account_id, amount_minor)` — transfer
- `pay_payee(account_id, payee_id, amount_minor, memo=None, scheduled_for=None)` — repayment/    payee
- `add_payee(user_id, name, account_no, bank_name)` —     people
- `list_payees(user_id)` —     people
- `schedule_recurring(account_id, payee_id, amount_minor, freq, start_date)` —     

**note**
-  members AA      `list_payees(user_id)`    people   actual  people ID，    `pay_payee`。`transfer`       user    account，     members  。
- `pay_payee`    `ACCOUNT_FROZEN`      ， confirm   posted transaction，      。
- `amount_minor`    fen（¥1 = 100 fen），1 CNY = 100，5400 CNY = 540000 fen。
- account frozen status        ，banking      。

## 4. `health_tracker_mock` —     

**    **
- `log_metric(user_id, type, value, recorded_at, unit=None, value_text=None)` — record  （blood_pressure/heart_rate/steps  ）
- `get_metric_summary(user_id, type, period)` —       
- `list_health_alerts(user_id)` —       （flag   ：above_typical_range/below_typical_range）
- `set_goal(user_id, type, target, period, unit=None, direction="at_least", start_date=None)` —       
- `get_goals(user_id, status=None)` —        
- `log_workout(user_id, type, duration_min, started_at, calories=None, distance_m=None)` — record  

**note**
- `list_health_alerts`   type     ，return    ，        type=blood_pressure。
- blood pressure flag=`above_typical_range`    ；     itinerary，      。

## 5. `visa_and_advisory_mock` —      

**    **
- `check_entry_requirements(nationality, destination, purpose)` —    requirements
  -   ：nationality="CN"，destination="JP"/"KR"，purpose="tourism"
- `get_advisory(country_code)` —  travel advisory（level   ：1=  ,2=note,3=warning,4=  ）
- `list_visa_products(nationality, destination)` —   visa  

**note**
-    actual    （nationality=CN, destination=JP/KR），  default_fallback。
-    level        surface        。

## 6. `email_mock` — email

**    **
- `search_emails(query, folder)` —   email（INBOX/Sent/All）
- `read_email(email_id)` —   email  
- `send_email(to, subject, body)` —   email
- `move_email(email_id, target_folder)` —   email

## 7. `calendar_mock` —   

**    **
- `create_event(summary, start, end, description=None, location=None, calendar_id=None, attendees=None, reminders=None)` —     
- `list_events(time_min, time_max, max_results)` —     
- `get_event(event_id)` —       
- `update_event(event_id, ...)` — update  
- `delete_event(event_id)` —     

**note**
- Tokyo、Seoul   UTC+09:00；`create_event`      `timezone`   ，         `start`/`end` ISO   。
- 6/6 meeting   ，    itinerary      。

## 8. `notion_mock` —     Journal

**    **
- `API-post-page(parent, properties, children)` —     （  page parent，  database）
- `API-patch-block-children(block_id, children)` —     block     
- `API-get-block-children(block_id)` —    block   
- `API-post-search(query, filter)` —     

**note**
- Journal   page+block   ，   database（database     return NOT_IMPL）。
-       Journal   ："East Asia Group Trip 2026 - Journal"。
-    stage     ，     record。

---

##     

-         ，      。
- amount    amount_minor（fen），        CNY。
-   /  /transfer      ，   PERSONA.md      。
-   status   workspace     Notion，          stage   。
