from ._helpers import response_check_id, structured_check_id

def s14_mock_exam_reschedule(env) -> bool:
    return structured_check_id(env, 's14_mock_exam_reschedule')

def s14_study_note_filter(env) -> bool:
    return structured_check_id(env, 's14_study_note_filter')

CHECKS = [
    ('s14_mock_exam_reschedule', s14_mock_exam_reschedule, 1.0),
    ('s14_study_note_filter', s14_study_note_filter, 1.0),
]
