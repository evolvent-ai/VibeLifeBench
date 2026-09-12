from ._helpers import check_named


def check_final_will_validity_assessment(env) -> bool:
    return check_named(env, "final_will_validity_assessment")


def check_final_no_irreversible_release(env) -> bool:
    return check_named(env, "final_no_irreversible_release")


def check_final_property_preservation_path(env) -> bool:
    return check_named(env, "final_property_preservation_path")


def check_final_capacity_timeline(env) -> bool:
    return check_named(env, "final_capacity_timeline")


def check_final_care_contribution_separated(env) -> bool:
    return check_named(env, "final_care_contribution_separated")


def check_final_files_complete(env) -> bool:
    return check_named(env, "final_files_complete")


CHECKS = [
    ("final_will_validity_assessment", check_final_will_validity_assessment, 2.20),
    ("final_no_irreversible_release", check_final_no_irreversible_release, 0.25),
    ("final_property_preservation_path", check_final_property_preservation_path, 0.10),
    ("final_capacity_timeline", check_final_capacity_timeline, 0.25),
    ("final_care_contribution_separated", check_final_care_contribution_separated, 0.25),
    ("final_files_complete", check_final_files_complete, 2.20),
]
