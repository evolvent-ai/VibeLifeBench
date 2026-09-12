"""Stage 21: retrospective and second-instance direction."""
from __future__ import annotations
from ._helpers import _food_journal_text

def s21_persisted_retrospective(env) -> bool:
    text = _food_journal_text(env)
    return bool(text) and any(k in text for k in ("retrospective", "summary", "lessons")) and sum(k in text for k in ("milestones", "evidence", "statutory provisions", "precedent", "testing")) >= 3 and any(k in text for k in ("cost", "litigation fee", "testing fee", "time cost"))

def s21_persisted_second_instance_direction(env) -> bool:
    text = _food_journal_text(env)
    return bool(text) and any(k in text for k in ("second instance", "respondent", "defense")) and sum(k in text for k in ("testing report", "first-instance judgment", "evidence", "appeal claims", "uphold the original judgment")) >= 2
CHECKS = [("s21_persisted_retrospective", s21_persisted_retrospective, 0.75), ("s21_persisted_second_instance_direction", s21_persisted_second_instance_direction, 0.5)]

