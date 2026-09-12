from __future__ import annotations

from ._helpers import _check


def stage_20_final_packet_complete(env) -> bool:
    return _check("stage_20_final_packet_complete", env)


def stage_20_final_refresh_four_services_with_packet(env) -> bool:
    return _check("stage_20_final_refresh_four_services_with_packet", env)


def stage_20_recommendation_balances_constraints_and_decision_reserved(env) -> bool:
    return _check("stage_20_recommendation_balances_constraints_and_decision_reserved", env)


CHECKS = [
    ("stage_20_final_packet_complete", stage_20_final_packet_complete, 2.0),
    ("stage_20_final_refresh_four_services_with_packet", stage_20_final_refresh_four_services_with_packet, 1.0),
    ("stage_20_recommendation_balances_constraints_and_decision_reserved", stage_20_recommendation_balances_constraints_and_decision_reserved, 2.0),
]
