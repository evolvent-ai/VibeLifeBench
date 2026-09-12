"""Stage 21: invoice gaps - identify missing documents and remediation."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _any, _stage_corpus, _workspace_file_text,
    _text_has_backend_hotel_extension_amount,
)


def s21_identified_gaps(env) -> bool:
    """Agent identified the two missing receipts and backend-consistent hotel amount."""
    text = (
        _stage_corpus(env, 21) + "\n" +
        _workspace_file_text(env, "/workspace/evidence_log.md") + "\n" +
        _workspace_file_text(env, "/workspace/final_summary.md")
    ).lower()
    evidence = _workspace_file_text(env, "/workspace/evidence_log.md").lower()
    has_hotel_gap = (
        _any(text, ["last night", "extended stay", "2026-07-20", "7/20"])
        and _any(text, ["roppongi", "narita", "hotel"])
        and _any(text, ["invoice", "supporting document", "receipt"])
        and _text_has_backend_hotel_extension_amount(env, text)
    )
    has_hkg_gap = _any(text, ["hong kong", "hkg", "airport"]) and _any(text, ["receipt"]) and _any(text, ["200", "cny"])
    has_bank_alt = _any(text, ["bank", "transaction record", "statement", "charge"]) and _any(text, ["alternative", "supplement", "temporary", "cannot fully replace", "supporting"])
    has_next_steps = _any(text, ["download", "contact hotel", "request replacement", "upload", "submit", "contact restaurant", "screenshot"]) and len(evidence.strip()) > 80
    ok = has_hotel_gap and has_hkg_gap and has_bank_alt and has_next_steps
    logger.info(f"s21_gaps: hotel={has_hotel_gap} hkg={has_hkg_gap} bank={has_bank_alt} steps={has_next_steps} -> {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s21_identified_gaps", s21_identified_gaps, 2.0),
]
