def event_id(seq: int) -> str:
    return f"evt_{seq:08d}"


def calendar_id(seq: int) -> str:
    return f"cal_{seq:06d}"


def attendee_id(seq: int) -> str:
    return f"att_{seq:08d}"


def reminder_id(seq: int) -> str:
    return f"rem_{seq:08d}"
