from ._helpers import (
    has_rent_separated_from_build,
    read_updated_market_rent,
    rent_figure_persisted,
    trace_stage,
)


def s22_rent_payback_recomputed(env) -> bool:
    # HARDENING: was `trace_stage AND text_stage([rent/Oakview/payback/separate])`
    # -- pure keyword. Stage 22 re-estimates rent/payback from the refreshed
    # market sample and must keep it separate from build cost. Now
    # ENVIRONMENT-STATE: require the agent to have read the mutated Oakview ADU
    # stat (read_updated_market_rent) AND to persist the specific figure
    # (rent_figure_persisted = ¥9100 / 910000) AND to keep payback separate
    # (has_rent_separated_from_build). Identical backend fact as s02 but re-frozen
    # at the later stage (the figure survived the refresh). Two-valued: False if
    # the figure or the separation is missing from the durable ledger.
    return (
        trace_stage(env, 22)
        and read_updated_market_rent(env)
        and rent_figure_persisted(env)
        and has_rent_separated_from_build(env)
    )


CHECKS = [
    ("s22_rent_payback_recomputed", s22_rent_payback_recomputed, 1.6),
]
