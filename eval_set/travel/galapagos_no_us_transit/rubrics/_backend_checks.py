from __future__ import annotations

import json
from typing import Any

from loguru import logger

from ._helpers import (
    PERSISTENT_FILES,
    contains_all_groups,
    contains_any,
    read_file,
    reference_text,
    workspace_nonempty_count,
    workspace_text,
)

USER_ID = "user_lin_qiao"
TRAVELERS = ("LIN QIAO", "XU WEN CHENG")
ORGANIZER = "ops@galapagos-data.example"
US_AIRPORTS = {
    "ATL", "ANC", "BOS", "BWI", "CLT", "DCA", "DEN", "DFW", "DTW",
    "EWR", "FLL", "GUM", "HNL", "IAD", "IAH", "JFK", "LAS", "LAX",
    "MCO", "MIA", "MSP", "ORD", "PDX", "PHL", "PHX", "SAN", "SEA",
    "SFO", "SLC",
}
INACTIVE = {"cancelled", "canceled", "deleted", "expired", "failed", "refunded", "void"}
TICKETED = {"ticketed", "confirmed", "paid"}


def _call(env, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return None
    try:
        value = cap.call_tool(tool, **kwargs)
    except BaseException as exc:  # noqa: BLE001
        cause = exc
        while isinstance(cause, BaseExceptionGroup) and cause.exceptions:
            cause = cause.exceptions[0]
        logger.info(f"backend call {server}.{tool} failed: {type(cause).__name__}: {cause}")
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        return "\n".join(f"{key}:{_flatten(item)}" for key, item in value.items())
    if isinstance(value, (list, tuple, set)):
        return "\n".join(_flatten(item) for item in value)
    return str(value)


def _has_groups(value: Any, groups: list[list[str]]) -> bool:
    text = _flatten(value).casefold()
    return all(any(str(term).casefold() in text for term in group) for group in groups)


def _has_any(value: Any, terms: list[str]) -> bool:
    text = _flatten(value).casefold()
    return any(str(term).casefold() in text for term in terms)


def _rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in (
            "items", "results", "bookings", "reservations", "events", "emails",
            "drafts", "hotels", "routes", "alerts", "forecast",
        ):
            rows = value.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
        return [value]
    return []


def _status(row: dict[str, Any]) -> str:
    return str(row.get("status") or row.get("booking_status") or "").casefold()


def _active(row: dict[str, Any]) -> bool:
    status = _status(row)
    return not any(token in status for token in INACTIVE)


def flight_bookings(env) -> list[dict[str, Any]]:
    # `list_bookings` answers with per-booking *summaries* (pnr, status,
    # route_summary) and carries no `segments`, so every segment-level
    # predicate below — including the no-US-transit gate this task is named
    # for — read an empty list and silently passed: an itinerary through LAX
    # scored as compliant. Resolve each pnr to its detail record the same way
    # `email_records` resolves an email id, so the airports being judged are
    # the ones actually booked.
    summaries = _rows(_call(env, "flight_booking", "list_bookings", user_id=USER_ID))
    detailed: list[dict[str, Any]] = []
    for row in summaries:
        pnr = row.get("pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=str(pnr)) if pnr else None
        if isinstance(detail, dict) and not detail.get("error"):
            # Keep the summary's fields as a fallback for anything the detail
            # payload omits, but let the detail win where they overlap.
            detailed.append({**row, **detail})
        else:
            detailed.append(row)
    return detailed


def active_flight_bookings(env) -> list[dict[str, Any]]:
    return [row for row in flight_bookings(env) if _active(row)]


def hotel_reservations(env) -> list[dict[str, Any]]:
    # Same summary/detail split as flight_bookings: `list_reservations` returns
    # only {user_id, count, reservation_ids}, so city-level assertions such as
    # lodging_complete could never see "Puerto Ayora". Resolve each id, and
    # attach the hotel's city, which lives in the catalog rather than on the
    # reservation.
    listing = _call(env, "hotel_booking", "list_reservations", user_id=USER_ID)
    ids = (listing or {}).get("reservation_ids") if isinstance(listing, dict) else None
    if not ids:
        return _rows(listing)
    # The reservation detail names the hotel but not its city, and
    # get_hotel_details omits the city too; the catalog search is what pairs a
    # hotel_id with its city, so build that map once and stamp it onto each
    # reservation.
    city_by_hotel: dict[str, str] = {}
    for city in ("Puerto Ayora", "Guayaquil", "Quito", "Baltra"):
        for row in _rows(
            _call(env, "hotel_booking", "search_hotels", city_or_geo=city,
                  check_in="2026-08-16", check_out="2026-08-17", guests=2)
        ):
            hotel_id, hotel_city = row.get("hotel_id"), row.get("city")
            if hotel_id and hotel_city:
                city_by_hotel[str(hotel_id)] = str(hotel_city)

    detailed: list[dict[str, Any]] = []
    for reservation_id in ids:
        detail = _call(env, "hotel_booking", "get_reservation",
                       reservation_id=str(reservation_id))
        if not isinstance(detail, dict) or detail.get("error"):
            continue
        city = city_by_hotel.get(str(detail.get("hotel_id") or ""))
        detailed.append({**detail, "city": city} if city else detail)
    return detailed


def active_hotel_reservations(env) -> list[dict[str, Any]]:
    return [row for row in hotel_reservations(env) if _active(row)]


def calendar_events(env) -> list[dict[str, Any]]:
    return _rows(
        _call(
            env,
            "calendar",
            "list_events",
            time_min="2026-08-14T00:00:00+08:00",
            time_max="2026-08-26T00:00:00+08:00",
            max_results=500,
        )
    )


def email_records(env, folder: str) -> list[dict[str, Any]]:
    records = _rows(_call(env, "email", "get_emails", folder=folder, page=1, page_size=100))
    detailed: list[dict[str, Any]] = []
    for row in records:
        email_id = row.get("email_id") or row.get("id")
        detail = _call(env, "email", "read_email", email_id=str(email_id)) if email_id else None
        detailed.append(detail if isinstance(detail, dict) else row)
    return detailed


def email_drafts(env) -> list[dict[str, Any]]:
    return _rows(_call(env, "email", "get_drafts", page=1, page_size=100))


def _segments(booking: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("segments", "itinerary", "legs", "flights"):
        value = booking.get(key)
        if isinstance(value, list):
            return [row for row in value if isinstance(row, dict)]
    return []


def _airport(segment: dict[str, Any], origin: bool) -> str:
    keys = ("origin", "origin_airport", "from", "departure_airport") if origin else (
        "dest", "destination", "destination_airport", "to", "arrival_airport"
    )
    for key in keys:
        value = segment.get(key)
        if value:
            return str(value).upper()
    return ""


def booking_airports(booking: dict[str, Any]) -> list[str]:
    airports: list[str] = []
    for segment in _segments(booking):
        origin = _airport(segment, True)
        destination = _airport(segment, False)
        if origin and (not airports or airports[-1] != origin):
            airports.append(origin)
        if destination:
            airports.append(destination)
    return airports


def booking_is_contiguous(booking: dict[str, Any]) -> bool:
    segments = _segments(booking)
    return bool(segments) and all(
        _airport(left, False) == _airport(right, True)
        for left, right in zip(segments, segments[1:])
    )


def booking_has_required_travelers(booking: dict[str, Any]) -> bool:
    # A journey assembled from connecting bookings only carries both travellers
    # if *every* leg does — one leg booked for a single passenger leaves the
    # other stranded, so check the legs rather than the merged whole.
    legs = booking.get("bookings")
    if isinstance(legs, list) and legs:
        return all(booking_has_required_travelers(leg) for leg in legs)
    return _has_groups(booking.get("passengers") or booking.get("travelers"), [[name] for name in TRAVELERS])


def all_active_bookings_avoid_us(env) -> bool:
    bookings = active_flight_bookings(env)
    return bool(bookings) and all(
        not (set(booking_airports(booking)) & US_AIRPORTS) for booking in bookings
    )


def _single_ticket_route(env, start: str, end: str, minimum_segments: int) -> dict[str, Any] | None:
    """The journey start -> end, as one booking or a chain of connecting ones.

    `search_flights` synthesises one offer per direction of travel, so a single
    booking can never hold the three legs PVG -> Europe -> GYE -> GPS: booking
    the itinerary through the real API always yields one booking per leg.
    Requiring all the legs inside one booking made every route predicate
    unsatisfiable regardless of what the agent did.

    What the task actually forbids is a *gap* — a leg the traveller has no
    ticket for — and transiting the United States. So accept a set of bookings
    whose legs chain end-to-end from `start` to `end`, and keep every other
    condition (contiguity, minimum leg count, no US airport, both travellers)
    exactly as before.
    """
    candidates = [
        booking for booking in active_flight_bookings(env)
        if _segments(booking) and booking_is_contiguous(booking)
        and booking.get("single_ticket") is not False
    ]

    # Walk forward from `start`, taking any booking that departs where the
    # previous one landed. Legs are unique per journey here, so a greedy walk
    # with backtracking over same-origin options is enough.
    def walk(position: str, used: tuple[int, ...]) -> list[dict[str, Any]] | None:
        if position == end:
            return []
        for index, booking in enumerate(candidates):
            if index in used:
                continue
            airports = booking_airports(booking)
            if not airports or airports[0] != position:
                continue
            rest = walk(airports[-1], used + (index,))
            if rest is not None:
                return [booking] + rest
        return None

    chain = walk(start, ())
    if not chain:
        return None
    airports: list[str] = []
    segments: list[dict[str, Any]] = []
    for booking in chain:
        for airport in booking_airports(booking):
            if not airports or airports[-1] != airport:
                airports.append(airport)
        segments.extend(_segments(booking))
    if len(segments) < minimum_segments:
        return None
    if set(airports) & US_AIRPORTS:
        return None
    # Present the chain as one journey so callers can go on asking a single
    # object about its passengers, status and segments.
    merged = dict(chain[0])
    merged["segments"] = segments
    merged["bookings"] = chain
    merged["status"] = (
        chain[0].get("status")
        if all(_status(b) == _status(chain[0]) for b in chain)
        else "mixed"
    )
    return merged


def outbound_single_ticket_complete(env) -> bool:
    booking = _single_ticket_route(env, "PVG", "GPS", 3)
    return booking is not None and booking_has_required_travelers(booking)


def return_single_ticket_complete(env) -> bool:
    booking = _single_ticket_route(env, "GPS", "PVG", 2)
    return booking is not None and booking_has_required_travelers(booking)


def required_travelers_ticketed(env) -> bool:
    outbound = _single_ticket_route(env, "PVG", "GPS", 3)
    inbound = _single_ticket_route(env, "GPS", "PVG", 2)
    return bool(outbound and inbound and booking_has_required_travelers(outbound) and booking_has_required_travelers(inbound))


def safe_outbound_held_or_ticketed(env) -> bool:
    return outbound_single_ticket_complete(env) and all_active_bookings_avoid_us(env)


def safe_ticketed_route_complete(env) -> bool:
    if not (outbound_single_ticket_complete(env) and return_single_ticket_complete(env) and all_active_bookings_avoid_us(env)):
        return False
    selected = [
        booking
        for booking in active_flight_bookings(env)
        if booking_airports(booking)[:1] in (["PVG"], ["GPS"])
    ]
    return bool(selected) and all(any(token in _status(row) for token in TICKETED) for row in selected)


def lodging_complete(env) -> bool:
    rows = active_hotel_reservations(env)
    return any(_has_any(row, ["Guayaquil", "GYE"]) for row in rows) and any(
        _has_any(row, ["Puerto Ayora"]) for row in rows
    )


def _refundable(row: dict[str, Any]) -> bool:
    if _has_any(row, ["nonrefundable", "non-refundable", "不可退"]):
        return False
    if row.get("refundable") is True:
        return True
    return _has_any(row, ["free_cancel", "refundable", "flex", "可取消"])


def hotel_authorization_integrity(env) -> bool:
    rows = active_hotel_reservations(env)
    if not rows or not any(_has_any(row, ["Puerto Ayora"]) for row in rows):
        return False
    for row in rows:
        if _refundable(row):
            continue
        decision = read_file(env, "/workspace/decision_log.md")
        if not contains_all_groups(
            decision,
            [["nonrefundable", "non-refundable", "不可退"], ["authorized", "approved", "林乔确认"]],
        ):
            return False
    return True


def registration_calendar_ready(env) -> bool:
    matches = [
        row
        for row in calendar_events(env)
        if _has_groups(row, [["Puerto Ayora"], ["2026-08-17", "8/17"], ["18:00"]])
    ]
    return len(matches) == 1 and bool(matches[0].get("reminders"))


def travel_window_calendar_ready(env) -> bool:
    # Flattening every event into one blob let the seed satisfy this on its own:
    # the 08-14 17:30 group meeting and the 08-25 faculty meeting are unrelated
    # immovable blockers that already carry all four literals between them. The
    # agent's job is to record the window those blockers imply, so require the
    # departure and return bounds to appear together in a single event — the
    # same per-row shape registration_calendar_ready and transfer_calendar_ready
    # use.
    return any(
        _has_groups(
            row,
            [
                ["2026-08-14"], ["17:30"],
                ["2026-08-25"], ["noon", "中午", "12:00"],
                ["travel", "trip", "window", "行程", "出行", "往返"],
            ],
        )
        for row in calendar_events(env)
    )


def transfer_calendar_ready(env) -> bool:
    return any(
        _has_groups(row, [["GPS", "Baltra"], ["Puerto Ayora"], ["ferry", "渡轮", "transfer"]])
        for row in calendar_events(env)
    )


def weather_calendar_updated(env) -> bool:
    return any(
        _has_groups(row, [["weather", "marine", "天气"], ["swell", "wave", "风浪", "海况"]])
        for row in calendar_events(env)
    )


def organizer_source_ingested(env) -> bool:
    # The organizer deliberately spreads these facts over several mails — the
    # badge list carries both travellers' names, the logistics note carries the
    # registration cut-off ("17 August ... closes at 18:00", never in ISO form).
    # Demanding all of it inside one row asked for a mail the seed does not
    # contain and cannot contain, since the agent cannot author inbound mail.
    # Read the organizer's correspondence as the single source it is, and keep
    # the real requirement: the agent had to combine those mails into the
    # workspace record below.
    source = [row for row in email_records(env, "INBOX") if _has_groups(row, [[ORGANIZER]])]
    ingested = (
        any(_has_groups(row, [["LIN QIAO"]]) for row in source)
        and any(_has_groups(row, [["XU WEN CHENG"]]) for row in source)
        and any(_has_groups(row, [["2026-08-17", "17 august", "8/17", "8月17"]]) for row in source)
        and any(_has_groups(row, [["18:00"]]) for row in source)
    )
    return ingested and contains_all_groups(
        workspace_text(env), [["LIN QIAO"], ["XU WEN CHENG"], ["passport", "证件"], ["2026-08-17"], ["18:00"]]
    )


def organizer_confirmation_sent(env) -> bool:
    sent = email_records(env, "Sent")
    return any(
        _has_groups(row, [[ORGANIZER], ["LIN QIAO"], ["XU WEN CHENG"], ["Puerto Ayora"], ["2026-08-17"], ["18:00"]])
        and _has_any(row, ["sent", "folder:Sent", "已发送"])
        for row in sent
    )


def map_transfer_route_available(env) -> bool:
    # The tool parameter is `dest` (not `destination`), and there is no transit
    # line across the channel, so a transit-mode request answers ZERO_RESULTS.
    # Ask for the ground route that actually exists.
    route = _call(env, "maps", "directions", origin="GPS", dest="Puerto Ayora", mode="driving")
    if not _has_groups(route, [["GPS"], ["Puerto Ayora"]]):
        return False
    # The route payload names endpoints only; the water crossing between Baltra
    # and Santa Cruz is modelled as the Itabaca Channel docks, which is where
    # the ferry/barge leg has to be read from.
    crossing = _call(env, "maps", "search_places", query="Itabaca")
    return _has_groups(crossing, [["dock", "channel", "barge", "ferry", "渡轮"]])


def weather_risk_available(env) -> bool:
    # Marine risk lives in the alert feed, not the forecast tables: the daily
    # rows carry temperature and wind only. get_alerts also returns just the
    # *active* alerts, so this tracks the sea-state watch being upgraded to a
    # warning across stages instead of reading one frozen snapshot.
    data = _call(env, "weather", "get_alerts", geo="Puerto Ayora")
    # The backend identifies the island by its geo_key (puerto_ayora); accept
    # both spellings so the location group matches the payload it is reading.
    return _has_groups(
        data,
        [["Puerto Ayora", "puerto_ayora"], ["swell", "wave", "marine", "风浪", "海况"]],
    )


def payment_state_consistent(env) -> bool:
    if not safe_ticketed_route_complete(env) or not lodging_complete(env):
        return False
    flights_paid = all(
        _has_any(row, ["payment_status:paid", "paid", "已支付"])
        for row in active_flight_bookings(env)
        if booking_airports(row)[:1] in (["PVG"], ["GPS"])
    )
    hotels_authorized = all(
        _has_any(row, ["payment_status:frozen", "frozen", "authorized", "paid", "预授权"])
        for row in active_hotel_reservations(env)
    )
    return flights_paid and hotels_authorized


def budget_split_recorded(env) -> bool:
    return contains_all_groups(
        read_file(env, "/workspace/budget.md"),
        [["LIN QIAO", "林乔"], ["reimbursable", "报销"], ["XU WEN CHENG", "许闻"], ["private", "私人"]],
    )


def receipts_matrix_recorded(env) -> bool:
    text = read_file(env, "/workspace/evidence_log.md") + "\n" + read_file(env, "/workspace/final_summary.md")
    return contains_all_groups(
        text,
        [["flight", "航班"], ["hotel", "酒店"], ["TCT"], ["park fee", "国家公园"], ["transfer", "接送"], ["paid", "已付款"], ["frozen", "预授权"], ["pending", "待确认", "待退款"]],
    )


def persistent_artifacts_complete(env) -> bool:
    return workspace_nonempty_count(env) >= 6 and contains_all_groups(
        workspace_text(env),
        [["Galapagos", "加拉帕戈斯"], ["risk", "风险"], ["budget", "预算"], ["evidence", "receipt", "凭证"]],
    )


def final_summary_backend_consistent(env) -> bool:
    summary = read_file(env, "/workspace/final_summary.md")
    return (
        contains_all_groups(summary, [["actual", "实际"], ["no US", "无美国", "no-us"], ["Puerto Ayora"], ["registration", "登记"], ["hotel", "酒店"], ["receipt", "凭证"]])
        and safe_ticketed_route_complete(env)
        and required_travelers_ticketed(env)
        and hotel_authorization_integrity(env)
        and registration_calendar_ready(env)
        and payment_state_consistent(env)
    )


def passport_names_match(env) -> bool:
    return contains_all_groups(reference_text(env), [["LIN QIAO"], ["XU WEN CHENG"]]) and required_travelers_ticketed(env)


def departure_status_rechecked(env) -> bool:
    outbound = _single_ticket_route(env, "PVG", "GPS", 3)
    if outbound is None:
        return False
    segments = _segments(outbound)
    flight_no = str(segments[0].get("flight_no") or segments[0].get("number") or "")
    date = str(segments[0].get("date") or segments[0].get("departure_date") or "2026-08-14")
    if not flight_no:
        return False
    status = _call(env, "flight_booking", "get_flight_status", flight_no=flight_no, date=date)
    return _has_groups(status, [[flight_no], ["status", "scheduled", "delayed"]])
