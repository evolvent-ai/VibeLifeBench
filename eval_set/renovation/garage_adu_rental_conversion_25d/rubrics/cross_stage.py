from ._helpers import (
    final_contract,
    has_order_egress_and_safe_alarm,
    has_owned_listing,
    listing_has_forbidden_use,
    listing_not_published_before_pass,
    listing_published_after_pass,
    own_listing_blob,
)


def cross_zoning_to_listing_consistent(env) -> bool:
    return final_contract(env, 'zoning')


def cross_false_description_never_used(env) -> bool:
    return final_contract(env, 'no_false_description')


def cross_failed_inspection_blocked_listing(env) -> bool:
    return final_contract(env, 'inspection_fail') and listing_not_published_before_pass(env)


def cross_passed_inspection_before_public_listing(env) -> bool:
    return final_contract(env, 'inspection_pass') and listing_published_after_pass(env)


def cross_budget_under_240k_with_payback(env) -> bool:
    return final_contract(env, 'budget')


def cross_material_price_mutation_reflected(env) -> bool:
    return final_contract(env, 'materials')


def cross_parking_access_retained(env) -> bool:
    return final_contract(env, 'parking_neighbor')


def cross_final_listing_confirmed_only(env) -> bool:
    return final_contract(env, 'listing')


# --- HARDENING (2026-07-25): added backend-grounded difficulty ---------------
def cross_materials_order_egress_safe_alarm(env) -> bool:
    # DIFFICULTY: the real placed ecommerce order must contain BOTH the egress
    # casement window AND the in-stock SafeNest smoke/CO alarm (the replacement
    # for the A12 out-of-stock CodeGuard bundle). place_order hard-fails on stock
    # 0, so this is a backend-enforced correctness fact: an agent that "orders the
    # alarm" without switching to SafeNest cannot have a successful order carrying
    # it. Two-valued: empty when no order; False when the order lacks the correct
    # code items (has_order_egress_and_safe_alarm reads list_orders -> get_order
    # -> get_product titles/ids).
    return has_order_egress_and_safe_alarm(env)


def cross_listing_after_passed_inspection(env) -> bool:
    # DIFFICULTY: the FULL fail -> re-inspect -> pass -> publish chain. Require a
    # real agent-owned public listing to exist AND the durable inspection_handoff
    # to record the completed fail->pass transition (listing_published_after_pass).
    # This asserts the publish followed a PASSED inspection (not before/without),
    # WITHOUT the dead-False `not has_owned_listing` anti-pattern -- the correct
    # end-state DOES post after re-inspection passes. Two-valued: False if a
    # listing exists but no pass is recorded (published prematurely), or if no
    # listing exists yet (chain incomplete).
    return listing_published_after_pass(env)


def cross_permit_inspection_listing_aligned(env) -> bool:
    # DIFFICULTY (cross-service consistency): permit legitimacy + inspection pass +
    # listing content must ALIGN. Require (1) the no-false-description backend
    # contract to hold (permit legitimacy: no workshop/storage/studio/office framing leaked),
    # (2) the fail->pass inspection chain recorded, and (3) the agent's OWN public
    # listing to describe the confirmed compliant features (egress + alarm +
    # parking) and NOT contain any prohibited non-residential use framing. Ties three services (legal_search
    # permit stance, email/inspection outcome, listing_platform post) to one
    # coherent end-state. Two-valued: False if any leg is missing or the listing
    # carries a forbidden framing.
    return (
        final_contract(env, 'no_false_description')
        and listing_published_after_pass(env)
        and has_owned_listing(env, [["egress", "逃生"], ["alarm", "报警", "一氧化碳", "烟感"], ["parking", "停车"]])
        and not listing_has_forbidden_use(env)
    )


CHECKS = [
    ("cross_zoning_to_listing_consistent", cross_zoning_to_listing_consistent, 2.0),
    ("cross_false_description_never_used", cross_false_description_never_used, 2.0),
    ("cross_failed_inspection_blocked_listing", cross_failed_inspection_blocked_listing, 2.0),
    ("cross_passed_inspection_before_public_listing", cross_passed_inspection_before_public_listing, 1.5),
    ("cross_budget_under_240k_with_payback", cross_budget_under_240k_with_payback, 1.0),
    ("cross_material_price_mutation_reflected", cross_material_price_mutation_reflected, 1.0),
    ("cross_parking_access_retained", cross_parking_access_retained, 1.0),
    ("cross_final_listing_confirmed_only", cross_final_listing_confirmed_only, 1.5),
    # HARDENING: backend-grounded difficulty (env-state carries the weight).
    ("cross_materials_order_egress_safe_alarm", cross_materials_order_egress_safe_alarm, 2.0),
    ("cross_listing_after_passed_inspection", cross_listing_after_passed_inspection, 2.0),
    ("cross_permit_inspection_listing_aligned", cross_permit_inspection_listing_aligned, 2.0),
]
