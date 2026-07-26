from ._helpers import PROHIBIT_TERMS, trace_stage, text_stage, final_contract, own_listing_blob


def s18_failed_inspection_no_listing(env) -> bool:
    # Text/trace: agent reports the failed rough inspection and states the "no
    # public rental listing until re-inspection passes" boundary. AND-in
    # final_contract('inspection_fail') (the same durable guard as
    # cross_failed_inspection_blocked_listing) so the 5.0 also requires the
    # DURABLE backend fact: inspection_handoff.md records failed + egress/exhaust
    # deficiencies + the 不得/不能 出租/advertis block. This stops a run that
    # narrates the block but never persists the failed-inspection listing hold.
    # Immediate Stage-18 scoring freezes the environment before later stages, so
    # the correct state here is directly observable: no agent-owned listing yet.
    mutation_servers = ["email", "notification_hub"]
    return (
        bool(mutation_servers)
        and trace_stage(env, 18)
        and text_stage(env, 18, [["failed", "未通过"], ["egress", "逃生"], ["exhaust", "排风", "ventilation"], ["alarm", "报警"], PROHIBIT_TERMS, ["出租", "rent", "listing", "advertis"]])
        and final_contract(env, "inspection_fail")
        and "marina" not in own_listing_blob(env).lower()
    )


CHECKS = [
    ("s18_failed_inspection_no_listing", s18_failed_inspection_no_listing, 5.0),
]
