from __future__ import annotations
from ._helpers import (
    final_sailing_plan_ok,
    health_privacy_after_closure_ok,
    insurance_after_certificate,
    minors_boundary_after_closure_ok,
    no_premature_irreversible,
    payment_authorization_ok,
    photo_authorization_after_closure_ok,
    sailing_reservations_after_readiness_ok,
    weather_rechecked_after_clear,
    workspace_business_complete,
)


CHECKS = [
    ("cross_no_sailing_before_weather_and_insurance", no_premature_irreversible, 2.508),
    ("cross_capacity_after_boat_mutation", sailing_reservations_after_readiness_ok, 2.508),
    ("cross_weather_rechecked_after_clear", weather_rechecked_after_clear, 1.004),
    ("cross_insurance_order_after_certificate", insurance_after_certificate, 1.504),
    ("cross_minors_never_board", minors_boundary_after_closure_ok, 2.508),
    ("cross_no_private_or_premature_payment", payment_authorization_ok, 2.508),
    ("cross_photo_consent_survives_revocation", photo_authorization_after_closure_ok, 1.504),
    ("cross_health_privacy_survives_final_notice", health_privacy_after_closure_ok, 1.504),
    ("cross_final_closure_uses_all_gates", final_sailing_plan_ok, 1.504),
    ("cross_workspace_handoff_complete", workspace_business_complete, 0.502),
]
