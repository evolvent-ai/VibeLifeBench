"""Cross-stage continuity checks for east_asia_group_trip_24d.

5 checkers. Each anchored to persisted workspace state.
"""
from __future__ import annotations
import re

from loguru import logger

from ._helpers import (
    _any,
    _count_any,
    _number_count,
    _workspace_file_text,
)


def cs_budget_continuity(env) -> bool:
    """budget.md estimated→actual→settled ≥2 + AA/4p/3p + nums≥8."""
    budget = _workspace_file_text(env, "/workspace/budget.md").lower()
    if not budget.strip():
        logger.info("cs_budget_continuity: budget.md empty → FAIL")
        return False
    stage_markers = {
        "estimated": _any(budget, ["estimated", "budget", "estimate"]),
        "actual": _any(budget, ["actual", "paid"]),
        "settled": _any(budget, ["settled", "final", "settlement complete"]),
    }
    found_stages = [k for k, v in stage_markers.items() if v]
    has_aa = _any(budget, ["per person", "equal split", "aa", "split"])
    has_4person = _any(budget, ["4 people", "4 travelers", "tokyo 4", "tokyo_split_count=4"])
    has_3person = _any(budget, ["3 people", "3 travelers", "seoul 3", "seoul_split_count=3"])
    num_count = _number_count(budget)
    has_cap = _any(budget, ["5400", "540000", "per-person cap", "hard per-person cap"])
    ok = (len(found_stages) >= 2 and has_aa and has_4person and has_3person
          and num_count >= 8 and has_cap)
    logger.info(
        f"cs_budget_continuity: stages={found_stages}({len(found_stages)}/2) "
        f"aa={has_aa} 4p={has_4person} 3p={has_3person} nums={num_count}(need>=8) "
        f"cap={has_cap} → {'PASS' if ok else 'FAIL'}"
    )
    return ok


def cs_incident_chain(env) -> bool:
    """incident_log.md contains all five incident chains."""
    ilog = _workspace_file_text(env, "/workspace/incident_log.md").lower()
    if not ilog.strip():
        logger.info("cs_incident_chain: incident_log.md empty → FAIL")
        return False
    incidents = [
        ("flight_cancel", _any(ilog, ["flight cancelled", "cancelled", "mu501", "rebook", "connection"])),
        ("hotel_oversell", _any(ilog, ["hotel", "oversell", "reservation cancelled", "rebook"])),
        ("bp_spike", _any(ilog, ["blood pressure", "above", "158", "li ting", "health"])),
        ("account_frozen", _any(ilog, ["frozen", "account_frozen", "wang hao"])),
        ("advisory_upgrade", _any(ilog, ["advisory", "south korea", "level", "upgrade"])),
    ]
    found = [n for n, v in incidents if v]
    ok = len(found) >= 5
    logger.info(f"cs_incident_chain: found={found} ({len(found)}/5) → {'PASS' if ok else 'FAIL'}")
    return ok


def cs_constraint_memory(env) -> bool:
    """Passport, blood-pressure, and split constraints persist across workspace files."""
    files = {
        "risk_register": _workspace_file_text(env, "/workspace/risk_register.md").lower(),
        "profiles": _workspace_file_text(env, "/workspace/profiles.md").lower(),
        "health_watch": _workspace_file_text(env, "/workspace/health_watch.md").lower(),
        "incident_log": _workspace_file_text(env, "/workspace/incident_log.md").lower(),
        "budget": _workspace_file_text(env, "/workspace/budget.md").lower(),
        "bookings": _workspace_file_text(env, "/workspace/bookings.md").lower(),
        "decision_log": _workspace_file_text(env, "/workspace/decision_log.md").lower(),
    }
    passport_files = [
        n for n, t in files.items()
        if n in ("risk_register", "profiles", "decision_log")
        and _any(t, ["passport", "wang hao", "validity", "6 months"])
    ]
    bp_files = [
        n for n, t in files.items()
        if n in ("health_watch", "incident_log", "risk_register")
        and _any(t, ["blood pressure", "li ting", "above", "monitor", "health", "blood_pressure"])
    ]
    aa_files = [
        n for n, t in files.items()
        if n in ("budget", "bookings", "decision_log")
        and _any(t, ["3 people", "3 travelers", "aa", "split", "seoul segment", "zhao min", "4 people"])
    ]
    constraint_files = set(passport_files + bp_files + aa_files)
    ok = (
        len(passport_files) >= 3
        and len(bp_files) >= 3
        and len(aa_files) >= 3
        and len(constraint_files) >= 6
    )
    logger.info(
        f"cs_constraint_memory: passport={passport_files}(need>=3) bp={bp_files}(need>=3) "
        f"aa={aa_files}(need>=3) total_files={len(constraint_files)}(need>=6) → {'PASS' if ok else 'FAIL'}"
    )
    return ok


def cs_risk_register_updated(env) -> bool:
    """risk_register.md covers passport risk and at least three travel risks."""
    risk = _workspace_file_text(env, "/workspace/risk_register.md").lower()
    if not risk.strip():
        logger.info("cs_risk_register_updated: risk_register.md empty → FAIL")
        return False
    has_passport = _any(risk, ["passport", "wang hao", "validity", "6 months"])
    travel_risk_types = [
        _any(risk, ["level 3", "advisory", "travel advisory"]),
        _any(risk, ["frozen", "account_frozen", "account"]),
        _any(risk, ["oversell", "hotel oversell"]),
        _any(risk, ["blood pressure", "158", "above"]),
        _any(risk, ["flight cancelled", "mu501", "cancelled", "rebook"]),
    ]
    has_travel_risk = sum(travel_risk_types) >= 3
    ok = has_passport and has_travel_risk
    logger.info(f"cs_risk_register_updated: passport={has_passport} travel_risks={sum(travel_risk_types)}/5(need>=3) → {'PASS' if ok else 'FAIL'}")
    return ok


def cs_itinerary_complete(env) -> bool:
    """itinerary.md covers all routes, meeting, traveler difference, dates, and flights."""
    itin = _workspace_file_text(env, "/workspace/itinerary.md").lower()
    if not itin.strip():
        logger.info("cs_itinerary_complete: itinerary.md empty → FAIL")
        return False
    has_sh_tyo = _any(itin, ["shanghai", "sha", "pvg", "tokyo", "nrt", "tyo"])
    has_tyo_icn = _any(itin, ["tokyo", "tyo", "nrt", "seoul", "icn", "sel"])
    has_icn_sh = _any(itin, ["seoul", "icn", "sel", "shanghai", "sha", "pvg"])
    all_routes = has_sh_tyo and has_tyo_icn and has_icn_sh
    has_meeting = _any(itin, ["meeting", "06-06", "anchor"])
    has_zhao = _any(itin, ["zhao min", "zhao", "does not travel to seoul", "only tokyo", "seoul segment"])
    has_depart = _any(itin, ["6/5", "06-05", "2026-06-05"])
    has_transfer = _any(itin, ["6/8", "06-08", "2026-06-08"])
    has_return = _any(itin, ["6/10", "06-10", "2026-06-10"])
    has_dates = has_depart and has_transfer and has_return
    has_airline = _any(itin, ["mu", "ca", "oz", "ana", "jal", "asiana", "flight no"])
    ok = all_routes and has_meeting and has_zhao and has_dates and has_airline
    logger.info(f"cs_itinerary_complete: routes={all_routes} meeting={has_meeting} zhao={has_zhao} dates={has_dates} airline={has_airline} → {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("cs_budget_continuity",     cs_budget_continuity,     4.5),
    ("cs_incident_chain",        cs_incident_chain,        4.5),
    ("cs_constraint_memory",     cs_constraint_memory,     4.5),
    ("cs_risk_register_updated", cs_risk_register_updated, 4.5),
    ("cs_itinerary_complete",    cs_itinerary_complete,    4.5),
]
