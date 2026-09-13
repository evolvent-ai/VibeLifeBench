"""Stage 1 rubric — visa rule change + typhoon season notice (D1)."""
from __future__ import annotations

import re


from .shared._helpers import (
    _all_corpus,
    _any_kw,
)

from loguru import logger


def s1_visa_rule_surface(env) -> bool:
    """Agent persists the official eVisa-channel and jurisdiction review."""
    text = _all_corpus(env)
    official = _any_kw(text, ["mofa", "ministry of foreign affairs", "official portal", "official channel"])
    channel = _any_kw(text, ["japan evisa", "evisa", "consular jurisdiction", "jurisdiction"])
    # The instruction (event-001) words it "rather than an age-based
    # shortcut"; accept that faithful paraphrase, not only the literal
    # "not age-based" token.
    no_shortcut = _any_kw(text, ["not age-based", "no age shortcut",
                                 "age-based"])
    insurance_context = (
        _any_kw(text, ["travel insurance", "insurance"])
        and _any_kw(text, ["risk", "trip evidence", "risk coverage", "not a visa form"])
    )
    ok = official and channel and no_shortcut and insurance_context
    logger.info(
        f"s1 visa rule: official={official} channel={channel} "
        f"no_shortcut={no_shortcut} insurance_context={insurance_context} -> {ok}"
    )
    return bool(ok)


def s1_passport_validity_catch(env) -> bool:
    """Agent persists exact validity dates and the official confirmation task."""
    text = _all_corpus(env)
    passport = _any_kw(text, ["passport", "zhang lan"])
    expiry = _any_kw(text, ["2026-11-08", "2026/11/08"])
    return_date = _any_kw(text, ["2026-05-16", "2026/05/16"])
    explicitly_invalid = any(
        re.search(pattern, text)
        for pattern in (
            r"\b(?:not|isn't|is not|won't|will not)\s+(?:remain\s+)?valid\b",
            r"\b(?:does not|doesn't|won't|will not)\s+cover\b",
            r"\bexpires?\s+before\s+(?:the\s+)?return\b",
        )
    )
    valid_through = not explicitly_invalid and (
        _any_kw(text, ["valid through", "covers the trip"])
        or any(
            re.search(pattern, text)
            for pattern in (
                r"\bcovers?\s+(?:the\s+|our\s+)?(?:2026[-/]05[-/]16\s+)?return\b",
                r"\b(?:remains?|is|will be)\s+valid\s+(?:on|for|through|until)\s+(?:the\s+)?(?:2026[-/]05[-/]16\s+)?return(?:\s+date)?\b",
            )
        )
    )
    confirmation = (
        _any_kw(text, ["carrier", "operating airline", "airline"])
        and _any_kw(text, ["official visa", "transit", "official channel"])
        and _any_kw(text, ["confirm", "verify"])
    )
    ok = passport and expiry and return_date and valid_through and confirmation
    logger.info(
        f"s1 passport: passport={passport} expiry={expiry} return={return_date} "
        f"valid_through={valid_through} confirmation={confirmation} -> {ok}"
    )
    return bool(ok)


CHECKS = [
    ("s1_visa_rule_surface",       s1_visa_rule_surface,       1.5),
    ("s1_passport_validity_catch", s1_passport_validity_catch, 3),
]
