from ._helpers import final_contract, trace_stage, text_stage


def s23_tenant_listing_only_confirmed(env) -> bool:
    return (
        trace_stage(env, 23)
        and text_stage(env, 23, [["listing"], ["confirmed"], ["egress"], ["alarm"], ["parking"]])
        and final_contract(env, "listing")
    )


CHECKS = [
    ("s23_tenant_listing_only_confirmed", s23_tenant_listing_only_confirmed, 5.0),
]
