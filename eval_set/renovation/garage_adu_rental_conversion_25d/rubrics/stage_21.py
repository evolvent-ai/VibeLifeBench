from ._helpers import inspection_fail_then_pass_recorded, own_listing_blob, trace_stage


def s21_passed_recheck_before_listing(env) -> bool:
    # HARDENING: was `trace_stage AND text_stage([passed/egress/alarm/vent/listing])`
    # -- pure keyword. Stage 21 is the re-inspection PASS (ADU-FI-0822) that must
    # be reconciled against the earlier fail. Now ENVIRONMENT-STATE / cross-stage
    # transition: require the durable inspection_handoff to record the FULL chain
    # -- the failed rough inspection WITH its egress/exhaust deficiencies AND the
    # later re-inspection pass keyed to ADU-FI-0822 (inspection_fail_then_pass_
    # recorded). This proves the agent tracked the real fail->pass state
    # transition, not just wrote "passed". Immediate Stage-21 scoring also
    # requires that no agent-owned public listing exists yet. Two-valued: False
    # if either transition leg is absent or publication happened prematurely.
    return (
        trace_stage(env, 21)
        and inspection_fail_then_pass_recorded(env)
        and "marina" not in own_listing_blob(env).lower()
    )


CHECKS = [
    ("s21_passed_recheck_before_listing", s21_passed_recheck_before_listing, 1.6),
]
