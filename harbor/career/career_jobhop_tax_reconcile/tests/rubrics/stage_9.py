from . import _helpers as H


def authorized_applications_are_backend_compliant(env):
    applications = H.apps(env)
    return bool(applications) and len(applications) == len(H.compliant_apps(env)) and H.pipeline_covers_backend_applications(env)


CHECKS = [("tax_s09_authorized_applications_are_backend_compliant", authorized_applications_are_backend_compliant, 3.0)]
