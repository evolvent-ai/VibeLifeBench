from . import _helpers as H


def official_privacy_rules_are_cited(env):
    text = H.privacy_log(env)
    semantics = H.has_terms(text, ("Personal Information Protection Law",), ("sensitive personal information",), ("separate consent",), ("specific purpose", "sufficient necessity", "minimum necessity"), ("article",))
    return bool(H.legal_statutes(env, "personal information") and H.real_legal_references(env, text, min_count=3) and semantics)


CHECKS = [("med_s03_official_privacy_rules_are_cited", official_privacy_rules_are_cited, 2.5)]
