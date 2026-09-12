from ._helpers import check_named


def check_cross_later_will_not_seed_only(env) -> bool:
    return check_named(env, "cross_later_will_not_seed_only")


def check_cross_capacity_not_overstated(env) -> bool:
    return check_named(env, "cross_capacity_not_overstated")


def check_cross_asset_chain(env) -> bool:
    return check_named(env, "cross_asset_chain")


def check_cross_privacy_and_no_waiver(env) -> bool:
    return check_named(env, "cross_privacy_and_no_waiver")


def check_cross_final_chain_complete(env) -> bool:
    return check_named(env, "cross_final_chain_complete")


def check_cross_direct_source_care_firewall(env) -> bool:
    return check_named(env, "cross_direct_source_care_firewall")


CHECKS = [
    ("cross_later_will_not_seed_only", check_cross_later_will_not_seed_only, 0.10),
    ("cross_capacity_not_overstated", check_cross_capacity_not_overstated, 0.25),
    ("cross_asset_chain", check_cross_asset_chain, 0.25),
    ("cross_privacy_and_no_waiver", check_cross_privacy_and_no_waiver, 2.40),
    ("cross_final_chain_complete", check_cross_final_chain_complete, 2.40),
    ("cross_direct_source_care_firewall", check_cross_direct_source_care_firewall, 0.10),
]
