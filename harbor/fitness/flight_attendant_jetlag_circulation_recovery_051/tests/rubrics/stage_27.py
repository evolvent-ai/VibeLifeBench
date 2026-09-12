from __future__ import annotations

from ._helpers import calendar_has, email_has, stage_record, stage_service_count, weather_has


def chk_s27_delay_reschedule(env) -> bool:
    source = email_has(env, "Singapore return weather delay notice", (("Singapore",), ("thunderstorm",), ("23:40",), ("rest window",)))
    weather = weather_has(env, "Singapore", (("Singapore",),))
    calendar = calendar_has(env, (("October 3", "10/3", "2026-10-03"), ("recovery", "sleep", "rest")))
    logged = stage_record(
        env,
        "calendar_change_log.md",
        27,
        (("Singapore", "SIN"), ("delay",), ("October 3", "10/3"), ("sleep", "recovery")),
        ("Reason/source", "New window", "Backend verification"),
    )
    return source and weather and calendar and logged


def chk_s27_delay_multiservice_light(env) -> bool:
    return stage_record(env, "venue_weather_log.md", 27, (("Singapore", "SIN"), ("thunderstorms", "thunderstorm"), ("review again", "recheck")), ("Source/query time", "Calendar effect")) and stage_service_count(env, 27, ("email", "weather", "calendar")) == 3


CHECKS = [
    ("chk_s27_delay_reschedule", chk_s27_delay_reschedule, 1.5),
    ("chk_s27_delay_multiservice_light", chk_s27_delay_multiservice_light, 1.0),
]
