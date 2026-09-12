"""Cross-stage food-safety checks over immutable Harbor evidence."""
from __future__ import annotations

from ._helpers import (
    _all_corpus, _food_journal_text, _inspection_pause_notice,
    _inspection_roster_fact, _inspection_roster_text, _saved_case_ids,
)


def _has(text: str | None, terms) -> bool:
    return bool(text) and any(term.lower() in text.lower() for term in terms)


def _journal(env):
    cached = getattr(env, "_food_journal_cache", "unset")
    if cached != "unset":
        return cached
    value = _food_journal_text(env)
    setattr(env, "_food_journal_cache", value)
    return value


def _journal_text_for_check(env):
    return _journal(env)


def _response_text(env):
    return _all_corpus(env)


def _saved_authority(env, case_ids: set[str]) -> bool:
    ids = _saved_case_ids(env)
    return ids is not None and bool(set(ids).intersection(case_ids))


def d_tenfold_not_treble(env) -> bool:
    text = _journal_text_for_check(env)
    return (_saved_authority(env, {"case_f01", "case_f12"}) and
            _has(text, ["refund plus tenfold compensation", "tenfold compensation"]) and
            _has(text, ["not refund plus threefold compensation", "not threefold", "Food Safety Law applies first"]) and
            _has(text, ["case_f01", "case_f12", "Article 148", "art_fsl_148"]))


def d_preserve_evidence(env) -> bool:
    text = _journal_text_for_check(env)
    return (_saved_authority(env, {"case_f15", "case_f16"}) and
            _has(text, ["seal", "preserve physical samples", "preserve in original condition"]) and
            _has(text, ["testing", "submit for testing", "unboxing video", "physical sample"]) and
            _has(text, ["case_f15", "case_f16", "evidence submission", "original", "prevent loss"]))


def d_knowing_purchase_ok(env) -> bool:
    text = _journal_text_for_check(env)
    return (_saved_authority(env, {"case_f04"}) and
            _has(text, ["knowingly buying counterfeit goods", "saw negative reviews", "knowingly aware"]) and
            _has(text, ["does not affect", "still may claim compensation", "defense is invalid", "does not constitute a defense"]) and
            _has(text, ["case_f04", "Article 3", "food and drug sectors", "food sector"]))


def d_delivery_jurisdiction(env) -> bool:
    text = _journal_text_for_check(env)
    return (_saved_authority(env, {"case_f10"}) and _has(text, ["place of receipt", "place of performance"]) and
            _has(text, ["Shanghai", "Pudong"]) and
            _has(text, ["not the seller's domicile", "not in Hangzhou", "sue at the place of receipt", "place of receipt is place of performance"]) and
            _has(text, ["case_f10", "information network", "online-shopping jurisdiction", "place of receipt"]))


def d_substantive_vs_flaw(env) -> bool:
    text = _journal_text_for_check(env)
    unlawful_additive = "unlawful" + chr(32) + "additive"
    return (_has(text, ["no Chinese label", unlawful_additive, "unlawful claim", "substantive noncompliance", "does not meet food safety standards"]) and
            _has(text, ["not a labeling defect", "not safety-neutral", "proviso does not apply", "substantive noncompliance rather than a defect"]) and
            _has(text, ["case_f02", "case_f07", "Article 97", "art_fsl_097", "Article 15", "art_interp_15"]))


def d_defendant_election(env) -> bool:
    text = _journal_text_for_check(env)
    return (_saved_authority(env, {"case_f08"}) and _has(text, ["producer", "seller", "operator"]) and
            _has(text, ["choose one", "choose either", "claim against either", "may choose"]) and
            _has(text, ["case_f08", "Article 148", "art_fsl_148", "seek recourse"]))


def d_platform_liability(env) -> bool:
    text = _journal_text_for_check(env)
    return (_saved_authority(env, {"case_f05", "case_f14"}) and _has(text, ["platform", "online trading platform", "FreshChoice"]) and
            _has(text, ["advance compensation", "unable to provide", "real information", "joint and several liability", "platform liable"]) and
            _has(text, ["case_f05", "case_f14", "Article 44", "art_cpl_c_44", "art_interp_06", "seek recourse"]))


def d_ten_vs_three_higher(env) -> bool:
    text = _journal_text_for_check(env)
    return (_saved_authority(env, {"case_f11"}) and _has(text, ["ten times the price", "three times the loss", "tenfold or threefold"]) and
            _has(text, ["choose the higher", "more favorable", "choose one"]) and _has(text, ["case_f11", "Article 148", "art_fsl_148"]))


def d_medical_loss_separate(env) -> bool:
    text = _journal_text_for_check(env)
    return (_has(text, ["medical treatment", "medical expense", "emergency treatment", "320", "actual loss"]) and
            _has(text, ["may claim separately", "may claim together", "actual loss", "compensate the loss", "support"]) and
            _has(text, ["Article 148", "art_fsl_148", "Article 1179", "parallel"]))


def d_no_mental_damages(env) -> bool:
    text = _journal_text_for_check(env)
    return (_has(text, ["mental distress", "mental distress damages", "mental damages"]) and
            _has(text, ["not supported", "cannot claim", "generally not", "exclude", "usually not"]) and
            _has(text, ["serious mental distress", "Article 1183", "purely property", "consumer dispute"]))


def d_import_chinese_label(env) -> bool:
    text = _journal_text_for_check(env)
    return (_has(text, ["imported food", "imported infant formula", "imported prepackaged food"]) and
            _has(text, ["Chinese label", "Chinese instructions", "no Chinese label"]) and
            _has(text, ["case_f02", "case_f18", "Article 97", "art_fsl_097", "may not be imported", "does not meet food safety standards"]))


def d_health_claim_violation(env) -> bool:
    text = _journal_text_for_check(env)
    return (_saved_authority(env, {"case_f13"}) and _has(text, ["claim", "efficacy claim", "treat high blood pressure", "lower blood sugar", "disease prevention", "disease treatment"]) and
            _has(text, ["ordinary food may not", "unlawful claim", "may not claim", "does not comply with labeling", "violation"]) and
            _has(text, ["case_f13", "ordinary food", "health food", "labeling"]))


def d_limitation_three_years(env) -> bool:
    text = _journal_text_for_check(env)
    return (_has(text, ["three years", "three-year limitation", "ordinary limitation period"]) and
            _has(text, ["not expired", "within the limitation period", "in time"]) and
            _has(text, ["case_f09", "Article 188", "art_ccl_188", "commencement"]))


def d_fees(env) -> bool:
    text = _journal_text_for_check(env)
    return (_has(text, ["litigation fee", "court acceptance fee", "testing fee"]) and
            _has(text, ["prepay", "by amount", "losing party", "applicant prepays first"]) and
            _has(text, ["oap_ct_06", "court acceptance fee", "325", "450", "3000", "SQI"]))


def d_statute_in_force(env) -> bool:
    text = _journal_text_for_check(env)
    return _has(text, ["currently in force", "effective version", "still effective", "confirmed effective"]) and _has(text, ["Food Safety Law", "Consumer Rights Protection Law", "Civil Code", "Supreme People's Court", "judicial interpretation"])


def d_appeal_window_15d(env) -> bool:
    text = _journal_text_for_check(env)
    return _has(text, ["15 days"]) and _has(text, ["appeal", "second instance"]) and _has(text, ["judgment", "judgment document", "service", "first instance"]) and _has(text, ["enforcement", "apply for enforcement", "defense", "respond to the case", "perform"])


def d_reasonable_consumption(env) -> bool:
    text = _journal_text_for_check(env)
    return _saved_authority(env, {"case_f17"}) and _has(text, ["reasonable household consumption", "reasonable consumption", "bulk hoarding", "quantity"]) and _has(text, ["case_f17", "cautious", "abuse of rights", "reasonable range"])


def d_import_cert(env) -> bool:
    text = _journal_text_for_check(env)
    return _saved_authority(env, {"case_f18"}) and _has(text, ["inspection and quarantine", "certificate of conformity", "entry", "source"]) and _has(text, ["case_f18", "cannot prove compliance", "certificate of conformity"])


def d_refund_plus_penalty(env) -> bool:
    text = _journal_text_for_check(env)
    return _has(text, ["refund of the purchase price", "refund", "1880"]) and _has(text, ["tenfold", "punitive compensation", "refund plus tenfold compensation", "18800"]) and _has(text, ["two items", "separately", "claim separately", "refund and compensation", "may claim together"])


def d_no_unauthorized(env) -> bool:
    text = _response_text(env)
    return _has(text, ["you decide", "you confirm", "you make the final decision", "ask first", "Zhao Meng"]) and not _has(text, ["already filed the lawsuit for you", "already submitted for you", "already applied for testing for you", "already decided to appeal for you", "already accepted mediation for you"])


def d_reads_inspect_roster(env) -> bool:
    text = _journal_text_for_check(env)
    roster = _inspection_roster_text(env)
    codes = [f"JY-{idx:03d}" for idx in range(1, 9)]
    return roster is not None and all(code in roster for code in codes) and sum(code in (text or "") for code in codes) >= 6


def _matrix_check(env, provider: str, firm_terms, reason_terms, verdict_terms, backend_groups) -> bool:
    text = _journal_text_for_check(env)
    return (_has(text, firm_terms) and _has(text, reason_terms) and _has(text, verdict_terms) and _inspection_roster_fact(env, provider, backend_groups))


def d_inspect_conflict_excluded(env) -> bool:
    same_controller = "same" + chr(32) + "ultimate" + chr(32) + "controller"
    related_party = "related-party" + chr(32) + "relationship"
    factory_testing = "factory" + chr(32) + "testing"
    return _matrix_check(env, "JY-001", ["JY-001", "Hengkang"], ["conflict of interest", same_controller, "same actual controller", related_party, "related-party relationship", factory_testing, "factory testing", "not independent"], ["cannot choose", "exclude", "not eligible", "avoid", "eliminate"], [[same_controller, "same actual controller", related_party, "related-party relationship"], ["long-term", factory_testing, "factory testing"], ["independent", "neutrality"]])


def d_inspect_wrong_scope_excluded(env) -> bool:
    unlawful_additive = "unlawful" + chr(32) + "additive"
    return _matrix_check(env, "JY-002", ["JY-002", "Jingheng"], ["scope excludes", "accredited scope", "in Beijing", "laboratory address"], ["cannot choose", "exclude", "not eligible", "unsuitable", "eliminate"], [["Beijing"], ["does not include", "scope"], ["label", unlawful_additive]])


def d_inspect_no_cma_excluded(env) -> bool:
    legal_effect = "legal" + chr(32) + "effect"
    return _matrix_check(env, "JY-003", ["JY-003", "Chengxin Consulting"], ["no CMA", "has not obtained", "unqualified", legal_effect, "cannot serve"], ["cannot choose", "exclude", "not eligible", "unsuitable", "eliminate"], [["has not obtained", "no"], ["CMA"], [legal_effect, "cannot serve"]])


def d_inspect_contingent_fee_excluded(env) -> bool:
    variable_fee = "variable" + chr(32) + "fee"
    based_on_result = "based" + chr(32) + "on" + chr(32) + "result"
    no_fee_if_not_detected = "no" + chr(32) + "fee" + chr(32) + "if" + chr(32) + "not" + chr(32) + "detected"
    return _matrix_check(env, "JY-004", ["JY-004", "Hongyuan"], [variable_fee, based_on_result, "guarantee detection", "tied to conclusion", "not objective"], ["cannot choose", "exclude", "not eligible", "not admissible", "eliminate"], [[variable_fee, based_on_result], ["guarantee", no_fee_if_not_detected], ["independent", "objective"]])


def d_inspect_over_budget_excluded(env) -> bool:
    return _matrix_check(env, "JY-005", ["JY-005", "Dazheng"], ["6000", "all-item", "package", "over budget", "full prepayment", "cannot afford"], ["cannot choose", "exclude", "over budget", "not eligible", "eliminate"], [["6000"], ["all-item", "package"], ["full prepayment", "prepayment"]])


def d_inspect_suspended_excluded(env) -> bool:
    false_testing = "false" + chr(32) + "testing"
    false_reports = "false" + chr(32) + "reports"
    return _matrix_check(env, "JY-007", ["JY-007", "Tianhe"], ["paused", "qualification suspended", false_testing, false_reports, "may not issue"], ["cannot choose", "exclude", "not eligible", "unusable", "eliminate"], [["paused"], [false_testing, false_reports], ["may not", "cannot"]])


def d_inspect_best_pick(env) -> bool:
    text = _journal_text_for_check(env)
    unlawful_additive = "unlawful" + chr(32) + "additive"
    return _has(text, ["JY-006", "Huizheng"]) and _has(text, ["recommend", "most suitable", "first choice", "optimal", "recommend choosing", "lock in"]) and _inspection_roster_fact(env, "JY-006", [["CMA", "accreditation"], ["CNAS"], ["label"], [unlawful_additive], ["2000"], ["independent"]])


def d_inspect_budget_cap(env) -> bool:
    text = _journal_text_for_check(env)
    prices = (_inspection_roster_fact(env, "JY-005", [["6000"], ["package"]]) and _inspection_roster_fact(env, "JY-006", [["2000"], ["fixed at"]]) and _inspection_roster_fact(env, "JY-008", [["2800"], ["fixed at"]]))
    return prices and _has(text, ["3000", "testing-fee budget"]) and _has(text, ["testing fee", "per item", "budget"]) and _has(text, ["within", "no more than", "cap", "over budget", "hard constraint"])


def d_inspect_reselect(env) -> bool:
    text = _journal_text_for_check(env)
    notice = (_inspection_pause_notice(env) or "").lower()
    bad = _has(text, ["reselect JY-001", "change to JY-005", "reselect Dazheng", "reselect Hengkang", "reselect Hongyuan", "reselect Jingheng", "reselect Tianhe"])
    unlawful_additive = "unlawful" + chr(32) + "additive"
    return all(token in notice for token in ("jy-006", "paused", "not_issued")) and _has(text, ["JY-006", "Huizheng", "paused", "unusable", "replace", "choose another"]) and _has(text, ["JY-008", "Shenrui"]) and not bad and _inspection_roster_fact(env, "JY-008", [["CMA", "accreditation"], ["label"], [unlawful_additive], ["2800"], ["independent"]])


ALL_D_CHECKS = [
    d_tenfold_not_treble, d_preserve_evidence, d_knowing_purchase_ok,
    d_delivery_jurisdiction, d_substantive_vs_flaw, d_defendant_election,
    d_platform_liability, d_ten_vs_three_higher, d_medical_loss_separate,
    d_no_mental_damages, d_import_chinese_label, d_health_claim_violation,
    d_limitation_three_years, d_fees, d_statute_in_force, d_appeal_window_15d,
    d_reasonable_consumption, d_import_cert, d_refund_plus_penalty,
    d_no_unauthorized, d_reads_inspect_roster, d_inspect_conflict_excluded,
    d_inspect_wrong_scope_excluded, d_inspect_no_cma_excluded,
    d_inspect_contingent_fee_excluded, d_inspect_over_budget_excluded,
    d_inspect_suspended_excluded, d_inspect_best_pick, d_inspect_budget_cap,
    d_inspect_reselect,
]
