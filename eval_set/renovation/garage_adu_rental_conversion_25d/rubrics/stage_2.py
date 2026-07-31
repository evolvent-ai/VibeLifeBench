from ._helpers import (
    read_updated_market_rent,
    rent_figure_persisted,
    trace_stage,
)


def s02_rent_separate(env) -> bool:
    # HARDENING: was `trace_stage AND text_stage([rent/payback/separate/budget])`
    # -- pure keyword. Now ENVIRONMENT-STATE: the A02 silent mutation inserts the
    # Oakview ADU rent stat (stat_oakview_adu_update, avg_price_minor 910000 =
    # ¥9100/mo). Require (1) the agent actually read that mutated backend row
    # (read_updated_market_rent = a real get_market_stats("Oakview ADU") reaching
    # stat_oakview_adu_update / 910000 / period 2026-08-update) AND (2) the
    # SPECIFIC updated figure (¥9100 or 910000 分) persisted in the durable ledger
    # (rent_figure_persisted) -- a computed value, not the word "rent". The stale
    # baselines (940000 / 880000) and a generic "~9000" guess do NOT satisfy the
    # exact-figure token set. Two-valued: False if the market server is reachable
    # but the exact figure was never recorded. trace_stage retained only as a cheap
    # gate that a real listing_platform call happened.
    return (
        trace_stage(env, 2)
        and read_updated_market_rent(env)
        and rent_figure_persisted(env)
    )


CHECKS = [
    ("s02_rent_separate", s02_rent_separate, 1.6),
]
