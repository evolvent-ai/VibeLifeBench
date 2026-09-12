from __future__ import annotations

from ._helpers import _tool_call_matches, _workspace_file_text, text_has


def s3_checks_flight_inventory(env) -> bool:
    searched = _tool_call_matches(
        env,
        ["flight_booking__search_flights"],
        lambda a: a.get("destination") == "KIX"
        and a.get("departure_date") in {"2026-10-11", "2026-10-12", "2026-10-13"}
        and a.get("origin") in {"PVG", "SHA", "HGH"}
        and int(a.get("adults") or 0) == 3,
        stage=3,
    )
    durable = text_has(
        _workspace_file_text(env, "trip_plan.md") + _workspace_file_text(env, "decision_log.md"),
        [["mu737"], ["pvg"], ["kix"], ["2026-10-12"], ["10:00"], ["hold", "fare_buckets"], ["refundable", "refundability"]],
    )
    return bool(searched and durable)


CHECKS = [("s3_checks_flight_inventory", s3_checks_flight_inventory, 2.0)]
