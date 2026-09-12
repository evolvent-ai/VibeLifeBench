from ._helpers import (
    budget_refresh_recorded,
    trace_stage,
)


def s10_budget_and_payback_ledger(env) -> bool:
    # HARDENING: was `trace_stage AND text_stage([240000/budget/payback/separate])`
    # -- pure keyword. Now ENVIRONMENT-STATE / computed-value: the budget ledger
    # must (1) hold the ¥240,000 cap, (2) carry the SPECIFIC computed rent figure
    # derived from the mutated market stat (rent_figure_persisted = ¥9100 /
    # 910000, NOT just the word "payback"), and (3) explicitly keep rent/payback
    # SEPARATE from the build budget (has_rent_separated_from_build). This forces
    # the agent to have actually done the market read + payback math, not narrate
    # it. Two-valued: False if the ledger lacks the computed figure or the
    # separation statement.
    return trace_stage(env, 10) and budget_refresh_recorded(env)


CHECKS = [
    ("s10_budget_and_payback_ledger", s10_budget_and_payback_ledger, 1.6),
]
