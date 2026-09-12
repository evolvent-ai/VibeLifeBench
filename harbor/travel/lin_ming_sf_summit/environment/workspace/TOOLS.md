# Available Tools

This task connects eight mock servers. The names below match the public MCP capabilities. Pass schema parameter names exactly; a familiar product term is not necessarily an available tool.

## 1. flight_booking_mock

- Search: `search_flights(origin, destination, departure_date, return_date, cabin, adults, sort, ...)`
- Offer details and repricing: `get_flight_offer(offer_id)` and `price_offer(offer_id)`
- Booking: `create_booking(offer_id, passengers, contact, payment, seat_selections, hold)`
- Retrieval: call `list_bookings(user_id=..., email=...)`, then `get_booking(pnr)` for the target PNR
- Change or cancel: `change_booking(pnr, new_offer_id, segment_indices)` / `cancel_booking(pnr, reason)`
- Check-in and seats: `get_seat_map(pnr, segment_idx, offer_id)` and `check_in(pnr, segment_idx, pax_indices, preferred_seats)`
- Flight status: `get_flight_status(flight_no, date)`

Search results and booking lists may contain summaries only. Read the target offer or PNR detail before evaluation or business confirmation. After a direct flight is canceled, search again for a valid connecting itinerary rather than reusing an invalid offer.

## 2. hotel_booking_mock

- Search: `search_hotels(city_or_geo, check_in, check_out, guests, filters)`
- Hotel details and inventory: `get_hotel_details(hotel_id)` and `get_room_availability(hotel_id, check_in, check_out, guests)`
- Booking: `create_reservation(rate_plan_id, guest_profile, payment_method_id, special_requests)`
- Retrieval: call `list_reservations(user_id)`, then `get_reservation(reservation_id)` for the target reservation
- Modify or cancel: `modify_reservation(reservation_id, ...)` / `cancel_reservation(reservation_id)`
- Special request: `submit_special_request(reservation_id, text)`

Summit-period prices can change. Reconcile the budget using the current rate plan and the amount charged on the confirmed reservation; a search summary is not a booking.

## 3. visa_and_advisory_mock

- Entry rules: `check_entry_requirements(nationality, destination, purpose, transit_countries)`
- Products: `list_visa_products(nationality, destination)` and `get_visa_product(product_id)`
- Applications: `list_visa_applications(user_id)` and `get_visa_application(application_id)`
- Documents and submission: `upload_document(application_id, kind, doc_ref)` and `submit_visa_application(application_id, answers, docs_refs, payment_method_id)`
- Advisories: `get_advisory(country_code)` and `subscribe_advisory(country_code, sink)`

Discover the EVUS record dynamically from the application list. Formal submission can advance a draft to submitted or processing; never claim that the tool can directly mark it approved. EVUS does not replace a valid passport and B1/B2 visa.

## 4. health_tracker_mock

- Metrics: `get_metrics(user_id, type, since, until)`, `get_metric_summary(user_id, type, period)`, and `get_activity_summary(user_id, date)`
- Goals and restrictions: `get_goals(user_id, status)` and `get_goal_progress(user_id, goal_id)`
- Neutral anomaly notices: `list_health_alerts(user_id, limit)`

Ming Lin's active goal records a maximum of ten hours for any single economy-class segment. Read the goal and apply it when filtering options. Health tools provide recorded and descriptive information, not medical judgment.

## 5. banking_mock

- Accounts: `list_accounts(user_id)` and `get_account(account_id)`
- Transactions: `list_transactions(account_id, since, until, kind_filter, limit)`
- Payees and payments: `list_payees(user_id)` and `pay_payee(account_id, payee_id, amount_minor, memo, scheduled_for)`
- Transfers: `transfer(from_account_id, to_account_id, amount_minor, memo)`

This service has no dedicated approval or reimbursement tool. Preserve written approval for the CNY 15,000 cap and any spend over CNY 5,000 in a sent email and durable files. Use charged flight and hotel backend records as primary cost evidence; banking transactions are observable corroborating evidence only.

## 6. calendar_mock

- Calendars: `list_calendars(user_id)`
- Events: `list_events(calendar_id, time_min, time_max, order_by, max_results)`, `get_event(calendar_id, event_id)`, and `search_events(query, time_min, time_max)`
- Writes: `create_event(calendar_id, summary, start, end, description, location, attendees, reminders)`, `update_event(calendar_id, event_id, ...)`, and `delete_event(calendar_id, event_id)`

San Francisco uses PDT (UTC-7) during this trip; Beijing uses UTC+8. Search the relevant interval before creating an event to avoid duplicate time slots.

## 7. email_mock

- List and search: `get_emails(folder, page, page_size)` and `search_emails(query, folder, page, page_size)`
- Details: `read_email(email_id)` and `get_email_headers(email_id)`
- Writes: `send_email(to, subject, body, cc, bcc, html_body)` and `reply_email(email_id, body, reply_all, cc, bcc)`
- Drafts: `save_draft(...)`, `get_drafts(page, page_size)`, and `update_draft(draft_id, ...)`

Approval and reimbursement handoff must be readable as formal messages in Sent. A draft is not a sent message.

## 8. notion_mock

Notion exposes API-style tool names:

- Search: `API-post-search(query, filter, sort, start_cursor, page_size)`
- Read: `API-retrieve-a-page(page_id)` and `API-get-block-children(block_id, page_size, start_cursor)`
- Create: `API-post-page(parent, properties, children, icon, cover)`
- Update page properties: `API-patch-page(page_id, properties, archived, in_trash, icon, cover)`
- Append content: `API-patch-block-children(block_id, children, after)`
- Update one block: `API-update-a-block(block_id, ...)`

Maintain canonical durable files at `/workspace/trip_plan.md`, `/workspace/budget_tracker.md`, and `/workspace/decision_log.md` as specified by `ARTIFACT_CONTRACT.md`. Notion provides a cross-service archive and source references; it does not replace those exact paths.

## Operating principles

1. Use list or search to find candidates, then read the target object with get or detail.
2. Work is durably complete only after a successful write to a booking, reservation, calendar, Sent, Notion block, or canonical workspace file.
3. Treat formal tool results as authoritative for prices, status, time zones, and user identifiers. A failure or empty result is not success.
4. When authorization is uncertain, record the blocker and confirm with the user or manager. Never invent approval, EVUS approval, or payment completion.
