def review_id(seq: int) -> str:
    return f"rev_{seq:08d}"


def reservation_id(seq: int) -> str:
    return f"resv_{seq:06d}"


def qa_id(seq: int) -> str:
    return f"qa_{seq:06d}"


def rating_to_float(rating_tenths: int) -> float:
    """Convert stored INTEGER tenths (e.g. 46) to a 4.6-style float."""
    return round(int(rating_tenths) / 10.0, 1)
