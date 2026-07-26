from ._helpers import (
    durable_workspace,
    inspection_fail_then_pass_recorded,
    rent_figure_persisted,
    trace_stage,
)


def s24_closeout_cross_check(env) -> bool:
    # HARDENING: was `trace_stage AND text_stage([permit/inspection/budget/listing/
    # risk])` -- pure keyword. Stage 24 is the final cross-service reconciliation.
    # Now ENVIRONMENT-STATE: the durable dossier must actually reconcile the
    # COMPUTED facts -- the ¥240,000 budget cap with the persisted rent figure
    # (rent_figure_persisted), the permit case, and the completed fail->pass
    # inspection chain (inspection_fail_then_pass_recorded) plus an open-risk /
    # go-no-go line. This forces a real reconciliation of backend-derived numbers,
    # not a narration listing the topic words. Two-valued: False if the computed
    # rent figure or the inspection chain is absent from the durable audit.
    return (
        trace_stage(env, 24)
        and rent_figure_persisted(env)
        and inspection_fail_then_pass_recorded(env)
        and durable_workspace(env, [["audit_journal", "adu_control"], ["permit", "许可", "ADU-26-0803"], ["240000", "24万", "budget", "预算"], ["risk", "风险", "未决", "open", "go/no-go", "待确认"]])
    )


CHECKS = [
    ("s24_closeout_cross_check", s24_closeout_cross_check, 1.5),
]
