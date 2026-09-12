from __future__ import annotations

from ._helpers import calendar_has, ecommerce_product_has, no_orders, stage_record, weather_has


def chk_s17_weather_indoor_alt(env) -> bool:
    observed = weather_has(env, "Shanghai", (("thunderstorm_heat", "thunderstorm"), ("128", "unhealthy")))
    logged = stage_record(
        env,
        "venue_weather_log.md",
        17,
        (("Shanghai", "PVG"), ("thunderstorms", "thunderstorm"), ("128",), ("indoors",), ("review again", "recheck")),
        ("Weather/AQI observed", "Source/query time", "Indoor alternative", "Calendar effect", "Recheck time"),
    )
    calendar = calendar_has(env, (("indoors", "hotel room", "elliptical", "recovery"),))
    return observed and logged and calendar


def chk_s17_refresh_stock_before_buy(env) -> bool:
    stock = ecommerce_product_has(env, "compression socks", (("M", "m"), ("22000", "220"), ("2", "in_stock")))
    logged = stage_record(
        env,
        "equipment_budget.md",
        17,
        (("compression socks",), ("M", "size M"), ("inventory", "stock"), ("awaiting confirmation", "pending")),
        ("Product/SKU", "Price/stock", "Authorization scope", "Order/status", "Verified at"),
    )
    return stock and logged and no_orders(env)


CHECKS = [
    ("chk_s17_weather_indoor_alt", chk_s17_weather_indoor_alt, 1.75),
    ("chk_s17_refresh_stock_before_buy", chk_s17_refresh_stock_before_buy, 1.5),
]
