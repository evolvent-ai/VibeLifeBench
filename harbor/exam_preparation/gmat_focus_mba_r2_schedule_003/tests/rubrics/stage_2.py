from __future__ import annotations
from . import _helpers as H

def s2_program_matrix_started(env) -> bool:
    return H.s2_program_matrix_started(env)

def s2_deadline_calendar_seeded(env) -> bool:
    return H.s2_deadline_calendar_seeded(env)

def s2_requirement_programs_complete(env) -> bool:
    return H.s2_requirement_programs_complete(env)

CHECKS = [
    ("s2_program_matrix_started", s2_program_matrix_started, 1.5),
    ("s2_deadline_calendar_seeded", s2_deadline_calendar_seeded, 1.25),
    ("s2_requirement_programs_complete", s2_requirement_programs_complete, 1.25)
]
