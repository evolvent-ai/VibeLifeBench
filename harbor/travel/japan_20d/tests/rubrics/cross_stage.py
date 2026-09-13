"""Cross-stage (d_*) checker bodies for japan_20d.

Each per-stage rubric module imports the d_* checkers it references and
includes them in its own CHECKS list. The hard budget cap and the final
dimension d_* checks are included in rubrics/final.py.

NOT INCLUDED (turn_log dependency, dropped per design):
  - ``six_of_nine_services_used`` (C1 tool-use distribution)
"""
from __future__ import annotations

import json
import re

from .shared._helpers import (
    _all_corpus,
    _all_calendar_events,
    _any_kw,
    _agent_responses,
    _call,
    _cron_reminders,
    _emails_for,
    _list_flight_bookings,
    _list_hotel_reservations,
    _list_visa_apps,
    _notion_text,
    _sent_email_rows,
    to_cny,
)

from loguru import logger


# ── F1..F5 — PERSONA implicit-constraint stubs ──────────────────────


def first_international_explain(env) -> bool:
    """PERSONA F1: parents' first international trip — agent explains
    airport / customs / SIM-payment mechanics. Lenient if corpus empty.
    """
    corpus = _all_corpus(env)
    if not corpus:
        return False
    airport = _any_kw(corpus, ["airport", "terminal", "departure lounge"])
    customs = _any_kw(corpus, ["customs", "immigration", "entry", "exit"])
    sim_pay = _any_kw(corpus, ["sim", "esim", "roaming", "payment",
                               "payment", "suica", "ic card", "visa/master",
                               "unionpay"])
    ok = airport and customs and sim_pay
    logger.info(f"F1 first-intl explain: airport={airport} customs={customs} sim/pay={sim_pay} → {'PASS' if ok else 'FAIL'}")
    return ok


def mother_raw_fish_avoid(env) -> bool:
    """PERSONA F2: mother stomach-sensitive → avoid raw fish."""
    corpus = _all_corpus(env)
    if not corpus:
        return False
    ok = _any_kw(corpus, ["cooked", "well done", "avoid raw",
                          "no raw", "sashimi avoid",
                          "no sashimi", "sushi avoid", "well-cooked"])
    logger.info(f"F2 raw-fish avoid: {'PASS' if ok else 'FAIL'}")
    return ok


def hotel_minifridge_insulin(env) -> bool:
    """PERSONA F3: father's insulin needs refrigeration → hotel notes /
    special_requests reference fridge. Lenient if no channel.
    """
    hotels = _list_hotel_reservations(env)
    for r in hotels:
        blob = json.dumps(r, ensure_ascii=False, default=str).lower()
        if ("mini" in blob and "fridge" in blob) or "refriger" in blob \
                or "refrigerator" in blob or "cool storage" in blob \
                or ("insulin" in blob and ("cool" in blob or "cold" in blob)):
            logger.info("F3 minifridge insulin: PASS via hotel notes")
            return True

    corpus = _all_corpus(env)
    if not corpus and not hotels:
        return False
    if corpus and (_any_kw(corpus, ["mini-fridge", "mini fridge", "minifridge",
                                    "refrigerat", "fridge", "cool storage"])
                   and _any_kw(corpus, ["insulin"])):
        logger.info("F3 minifridge insulin: PASS via corpus")
        return True
    logger.info("F3 minifridge insulin: FAIL")
    return False


def timezone_meal_adjust(env) -> bool:
    """PERSONA F4: +1h JST meal-timing plan for diabetic father."""
    corpus = _all_corpus(env)
    if not corpus:
        return False
    tz = _any_kw(corpus, ["time zone", "time-zone", "timezone", "jst",
                          "+1h", "-1h", "+60", "adjust schedule"])
    meal = _any_kw(corpus, ["meal", "insulin timing", "meal time", "meal schedule"])
    ok = tz and meal
    logger.info(f"F4 tz meal adjust: tz={tz} meal={meal} → {'PASS' if ok else 'FAIL'}")
    return ok


def unionpay_kix_nrt_cash(env) -> bool:
    """PERSONA F5: UnionPay ATM cash drawdown at KIX/NRT airport."""
    corpus = _all_corpus(env)
    if not corpus:
        return False
    has_airport = _any_kw(corpus, ["kix", "nrt", "narita", "kansai airport",
                                    "kansai airport", "narita"])
    has_cash = _any_kw(corpus, ["withdraw", "atm", "cash"])
    has_unionpay = _any_kw(corpus, ["unionpay", "union pay",
                                     "seven bank", "7-eleven atm"])
    ok = (has_airport and has_cash) or (has_unionpay and has_cash)
    logger.info(f"F5 unionpay KIX/NRT cash: airport={has_airport} cash={has_cash} unionpay={has_unionpay} → {'PASS' if ok else 'FAIL'}")
    return ok


# ── A-series cross-stage timing/coupling checks ─────────────────────


def passport_raised_first_3_stages(env) -> bool:
    """A3: Agent-authored state records the short-margin confirmation task."""
    body = _all_corpus(env)
    passport = _any_kw(body, ["passport", "zhang lan"])
    dates = _any_kw(body, ["2026-11-08"]) and _any_kw(body, ["2026-05-16"])
    confirmation = (
        _any_kw(body, ["carrier", "operating airline", "airline"])
        and _any_kw(body, ["official", "transit"])
        and _any_kw(body, ["confirm", "verify"])
    )
    ok = passport and dates and confirmation
    logger.info(f"A3 passport ≤s2: passport={passport} dates={dates} confirmation={confirmation} -> {ok}")
    return bool(ok)


def budget_warning_before_60k_cap(env) -> bool:
    """A2: budget warning raised before cumulative spend ≥ ¥60k."""
    corpus = _all_corpus(env)
    msgs = _emails_for(env, "li_wei") or []
    for m in msgs:
        corpus += "\n" + str(m.get("subject") or "") + " " + str(m.get("body") or "")
    if not corpus.strip():
        logger.info("A2 budget warn: lenient pass — no reachable channel")
        return False
    budget_markers = ["60000", "60,000", "60k", "¥60", "50000", "50k",
                      "budget", "remaining", "balance"]
    warn_markers = ["warn", "approach", "close to", "near", "exceed", "over",
                    "over", "near", "warning", "alert", "overspend"]
    ok = _any_kw(corpus, budget_markers) and _any_kw(corpus, warn_markers)
    logger.info(f"A2 budget warn: {'PASS' if ok else 'FAIL'}")
    return ok


_BUDGET_CAP_CNY = 60_000


def spend_under_60k_hard(env) -> bool:
    """Hard budget: sum flight (CNY) + hotel (JPY) bookings ≤ ¥60k."""
    flights = _list_flight_bookings(env)
    hotels = _list_hotel_reservations(env)
    if not flights and not hotels:
        logger.info("hard budget: lenient pass — no reachable booking mock")
        return False

    total_cny = 0.0
    for b in flights:
        # list_bookings persists the charged figure under ``total_paid`` —
        # read it, or the flight spend is silently counted as zero.
        tp = (b.get("total_paid") or b.get("total_price")
              or b.get("priced_total") or {})
        amt = tp.get("amount") if isinstance(tp, dict) else None
        cur = tp.get("currency") if isinstance(tp, dict) else None
        if isinstance(amt, (int, float)):
            pass
        elif isinstance(tp, (int, float)):
            amt, cur = tp, b.get("currency")
        if amt is None:
            amt = b.get("total_amount") or b.get("amount") or 0
            cur = b.get("currency") or "CNY"
        try:
            total_cny += to_cny(float(amt or 0), str(cur or "CNY"))
        except KeyError:
            logger.warning(f"hard budget: unknown flight currency {cur!r}; skipping")

    for r in hotels:
        amt = r.get("total_charged") or r.get("total_amount") or 0
        cur = r.get("currency") or "JPY"
        try:
            total_cny += to_cny(float(amt or 0), str(cur))
        except KeyError:
            logger.warning(f"hard budget: unknown hotel currency {cur!r}; skipping")

    ok = total_cny <= _BUDGET_CAP_CNY
    logger.info(f"hard budget: spend={total_cny:.0f} CNY cap={_BUDGET_CAP_CNY} → {'PASS' if ok else 'FAIL'}")
    return ok


def weather_advisory_surfaced_timely(env) -> bool:
    """A1: within one stage of first typhoon mention (D10), advisory surfaced."""
    corpus = _all_corpus(env)
    storm_terms = ["typhoon", "maya", "t2602", "kansai"]
    if corpus and _any_kw(corpus, storm_terms):
        logger.info("A1 weather surfaced: PASS via corpus")
        return True

    events = _all_calendar_events(env)
    for e in events or []:
        blob = str(e.get("summary") or "") + " " + str(e.get("description") or "")
        if _any_kw(blob, storm_terms):
            logger.info("A1 weather surfaced: PASS via calendar")
            return True

    if not corpus and not events:
        logger.info("A1 weather surfaced: lenient pass — no reachable channel")
        return False
    logger.info("A1 weather surfaced: FAIL")
    return False


def doctor_letter_reminder_before_s13(env) -> bool:
    """A4: doctor's-letter follow-up persisted BEFORE stage 13.

    This task exposes Notion/workspace/calendar persistence but no cron service,
    so a dated durable follow-up is the canonical evidence. Cron records remain
    accepted for compatibility with older snapshots.
    """
    kw = ["doctor", "letter", "prescription"]
    for r in _cron_reminders(env):
        if int(r.get("registered_by_day", 99)) <= 12 and _any_kw(
            str(r.get("text") or ""), kw,
        ):
            logger.info("A4 doctor letter: PASS via cron")
            return True

    durable = _all_corpus(env)
    time_anchor = [
        "2026-04", "2026-05-01", "before departure", "pre-departure",
        "due", "deadline", "before departure", "stage 12", "s12",
    ]
    if durable and _any_kw(durable, kw) and _any_kw(durable, time_anchor):
        logger.info("A4 doctor letter: PASS via durable follow-up")
        return True

    logger.info("A4 doctor letter: FAIL — no pre-s13 durable follow-up")
    return False


# ── B-series precision / no-mutation guards ─────────────────────────


def s6_no_booking_mutations(env) -> bool:
    """B1: neither flight nor hotel mutation on 2026-04-23."""
    if not _agent_responses(env).strip() or not env.trace(env.current_stage):
        logger.info("B1 s6 precision: no agent activity; FAIL")
        return False
    stage_date = "2026-04-23"
    for b in _list_flight_bookings(env):
        pnr = b.get("pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr) if pnr else None
        created = (detail or {}).get("created_at") or b.get("created_at") or ""
        if stage_date in str(created):
            logger.info("B1 s6 precision: FAIL — flight booking created on s6")
            return False
    for r in _list_hotel_reservations(env):
        created = str(r.get("created_at") or "")
        hist = r.get("history") or []
        if stage_date in created:
            logger.info("B1 s6 precision: FAIL — hotel reservation created on s6")
            return False
        for h in hist if isinstance(hist, list) else []:
            ts = str(h.get("at") or h.get("ts") or h.get("timestamp") or "")
            evt = str(h.get("event") or "")
            if stage_date in ts and evt and evt.lower() not in ("read", "get"):
                logger.info(f"B1 s6 precision: FAIL — hotel mutation on s6 ({evt})")
                return False
    logger.info("B1 s6 precision: PASS")
    return True


def s12_no_overexplain_confirmations(env) -> bool:
    """B2: stage 12 precision. ≤2 agent-authored summary emails (non-vendor).

    Agent-authored mail lives in the Sent folder (the agent acts on Li Wei's
    account); the inbox only ever carries world-originated mail, so count Sent.
    """
    if not _agent_responses(env).strip() or not env.trace(env.current_stage):
        logger.info("B2 s12 precision: no agent activity; FAIL")
        return False
    msgs = _sent_email_rows(env, "li_wei")
    extra = 0
    for m in msgs:
        frm = str(m.get("from_addr") or m.get("from") or "").lower()
        if "li.wei" not in frm:
            # not authored by the agent account
            continue
        subj = str(m.get("subject") or "").lower()
        body = str(m.get("body_text") or m.get("body") or "").lower()
        if (("confirm" in subj or "confirmation" in subj
                or "summary" in subj or "recap" in subj
                or "confirm" in body or "summary" in body)
                and "booking" not in subj):
            extra += 1
    if extra > 2:
        logger.info(f"B2 s12 precision: FAIL — {extra} agent summary emails")
        return False
    logger.info(f"B2 s12 precision: PASS (extra={extra})")
    return True


def no_premature_cancel_d10_d11(env) -> bool:
    """B3: no cancellations on 2026-04-27/28 (typhoon-watch window)."""
    bad_dates = ("2026-04-27", "2026-04-28")
    any_reachable = False
    for b in _list_flight_bookings(env):
        pnr = b.get("pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr) if pnr else None
        if isinstance(detail, dict):
            any_reachable = True
            for h in detail.get("history") or []:
                if not isinstance(h, dict):
                    continue
                if str(h.get("event") or "").upper() not in ("CANCELLED", "CANCEL"):
                    continue
                ts = str(h.get("at") or h.get("timestamp") or h.get("ts") or "")
                if any(d in ts for d in bad_dates):
                    logger.info(f"B3 no premature cancel: FAIL — flight cancel on {ts}")
                    return False
    for r in _list_hotel_reservations(env):
        any_reachable = True
        if str(r.get("status") or "").lower() != "cancelled":
            continue
        for h in r.get("history") or []:
            if not isinstance(h, dict):
                continue
            ts = str(h.get("at") or h.get("timestamp") or h.get("ts") or "")
            if any(d in ts for d in bad_dates):
                logger.info(f"B3 no premature cancel: FAIL — hotel cancel on {ts}")
                return False

    if not any_reachable:
        logger.info("B3 no premature cancel: lenient pass — no reachable state")
        return False
    logger.info("B3 no premature cancel: PASS")
    return True


# ── D1/D2/D3: cross-channel decision propagation ────────────────────


def hotel_walk_calendar_updated(env) -> bool:
    """D1: after D16 walk, hotel calendar event updated (Tokyu / walked)."""
    events = _all_calendar_events(env)
    if events is None:
        logger.info("D1 calendar update: lenient pass — calendar unreachable")
        return False
    if not events:
        logger.info("D1 calendar update: lenient pass — no events")
        return False
    property_terms = ["tokyu stay", "granbell", "shibuya hotel"]
    relocation_terms = [
        "walked", "hotel walk", "overbook", "rebook", "hotel change",
        "new hotel", "relocat", "transferred",
    ]
    for e in events:
        blob = str(e.get("summary") or "") + " " + str(e.get("description") or "")
        if _any_kw(blob, property_terms) and _any_kw(blob, relocation_terms):
            logger.info(f"D1 calendar update: PASS — {blob[:80]!r}")
            return True
    logger.info("D1 calendar update: FAIL")
    return False


def shinkansen_alt_with_notion_decision(env) -> bool:
    """D2: alt-route + notion decision note."""
    corpus = _all_corpus(env)
    if not corpus:
        logger.info("D2 shinkansen+notion: lenient pass — no corpus")
        return False
    alt_terms = ["limited express", "haruka", "thunderbird", "nozomi",
                 "kodama", "hikari", "bus", "taxi", "rental car",
                 "overnight", "later train", "after 15:00", "afternoon departure"]
    decision_terms = ["reroute", "switch", "substitute", "change flight",
                      "instead", "decided", "plan b", "plan-b", "alt route",
                      "alternative"]
    suspension_terms = ["suspension", "suspended", "stop", "shinkansen",
                        "tokaido", "jr advisory", "nagoya", "shin-osaka"]
    maps_hit = _any_kw(corpus, alt_terms)
    decision_hit = _any_kw(corpus, decision_terms)
    suspension_hit = _any_kw(corpus, suspension_terms)
    ok = maps_hit and (decision_hit or suspension_hit)
    logger.info(f"D2 shinkansen: alt={maps_hit} decision={decision_hit} suspension={suspension_hit} → {'PASS' if ok else 'FAIL'}")
    return ok


def flight_delay_communication(env) -> bool:
    """D3: agent communicated the delay via email or notion."""
    # The agent sends from Li Wei's account, so agent-authored mail lands in
    # Sent; the inbox only carries the world's mail.
    msgs = _sent_email_rows(env, "li_wei")
    for m in msgs:
        blob = (str(m.get("subject") or "") + "\n"
                + str(m.get("body_text") or m.get("body") or "")).lower()
        if "mu550" in blob or "delay" in blob:
            logger.info("D3 delay comm: PASS via email")
            return True

    corpus = _all_corpus(env)
    if corpus and (_any_kw(corpus, ["mu550", "delay", "delayed", "etd"])
                   and _any_kw(corpus, ["update", "status", "notify",
                                         "inform", "heads up"])):
        logger.info("D3 delay comm: PASS via notion/workspace")
        return True

    if not msgs and not corpus:
        logger.info("D3 delay comm: lenient pass — no reachable channel")
        return False
    logger.info("D3 delay comm: FAIL")
    return False


# ── C2/C3 / E1/E2: data-freshness checks ────────────────────────────


def flight_search_realistic_dates(env) -> bool:
    """C2: any booking has a segment in 2026-05-01..17 window."""
    bookings = _list_flight_bookings(env)
    probe = _call(
        env, "flight_booking", "search_flights",
        origin="PVG", destination="NRT", departure_date="2026-05-01",
        return_date="2026-05-16", adults=3, max_results=1,
    )
    probe_reachable = probe is not None
    if not bookings and not probe_reachable:
        logger.info("C2 flight dates: lenient pass — flight_booking unreachable")
        return False

    depart_re = re.compile(r"2026-05-(\d{2})")
    for b in bookings:
        pnr = b.get("pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr) if pnr else None
        if not isinstance(detail, dict):
            continue
        for seg in detail.get("segments") or []:
            blob = (str(seg.get("depart_dt") or "") + " "
                    + str(seg.get("arrive_dt") or "") + " "
                    + str(seg.get("date") or ""))
            m = depart_re.search(blob)
            if m and 1 <= int(m.group(1)) <= 17:
                logger.info(f"C2 flight dates: PASS via seg {blob}")
                return True
            if "2026-04-29" in blob or "2026-04-30" in blob:
                logger.info("C2 flight dates: PASS via slack edge")
                return True

    if not bookings and probe_reachable and (isinstance(probe, (list, dict)) and probe):
        logger.info("C2 flight dates: lenient pass — probe OK, no booking yet")
        return False
    logger.info("C2 flight dates: FAIL")
    return False


def weather_queried_pretrip_weeks(env) -> bool:
    """C3: ≥1 weather signal per pre-trip week (cron or notion-date)."""
    hits_days: set[int] = set()
    for r in _cron_reminders(env):
        if _any_kw(str(r.get("text") or ""),
                   ["weather", "forecast", "typhoon"]):
            d = int(r.get("registered_by_day", 99))
            if d <= 13:
                hits_days.add(d)

    body = _notion_text(env)
    date_re = re.compile(r"2026-04-(1[7-9]|2\d|30)")
    notion_hits: set[str] = set()
    if body and _any_kw(body, ["forecast", "weather", "°c"]):
        for m in date_re.finditer(body):
            notion_hits.add(m.group(0))

    ok = bool(hits_days) or len(notion_hits) >= 2

    if not hits_days and not notion_hits and not body:
        logger.info("C3 weather queries: lenient pass — no reachable channel")
        return False
    logger.info(f"C3 weather queries: cron_hits={sorted(hits_days)} notion_dates={sorted(notion_hits)} → {'PASS' if ok else 'FAIL'}")
    return ok


def flight_status_requeried_on_departure(env) -> bool:
    """E1: flight status re-queried on departure day."""
    bookings = _list_flight_bookings(env)
    if not bookings:
        logger.info("E1 status requery: lenient pass — no bookings")
        return False

    corpus = _all_corpus(env)
    if corpus and _any_kw(corpus, ["mu549"]) and _any_kw(
        corpus, ["landed", "arrived", "on time", "gate", "eta",
                 "carousel", "delay", "17:38", "nrt"],
    ):
        logger.info("E1 status requery: PASS via arrival trace")
        return True

    for b in bookings:
        pnr = b.get("pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr) if pnr else None
        if not isinstance(detail, dict):
            continue
        hist_events = [str(h.get("event") or "")
                       for h in detail.get("history") or []
                       if isinstance(h, dict)]
        if any("CHECK" in e.upper() or "STATUS" in e.upper()
               or "ARRIVED" in e.upper() or "SUBSCRIBE" in e.upper()
               for e in hist_events):
            logger.info("E1 status requery: PASS via booking history")
            return True

    logger.info("E1 status requery: FAIL")
    return False


def weather_alerts_requeried(env) -> bool:
    """E2: weather alerts re-queried pre- and post-upgrade."""
    body = _notion_text(env)
    if not body:
        logger.info("E2 alerts requery: lenient pass — notion empty")
        return False

    storm_dates = re.findall(r"2026-0(?:4-2[5-9]|4-30|5-(?:0[1-9]|1[0-2]))", body)
    unique_dates = {d for d in storm_dates}

    has_storm = _any_kw(body, ["maya", "t2602", "typhoon", "alerts"])
    refreshed = has_storm and len(unique_dates) >= 2

    logger.info(f"E2 alerts requery: storm={has_storm} unique_dates={sorted(unique_dates)} → {'PASS' if refreshed else 'FAIL'}")
    return refreshed
