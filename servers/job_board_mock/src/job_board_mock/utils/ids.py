def resume_id(seq: int) -> str:
    return f"resume_{seq:06d}"


def application_id(seq: int) -> str:
    return f"app_{seq:06d}"


def chat_id(seq: int) -> str:
    return f"chat_{seq:06d}"


def message_id(seq: int) -> str:
    return f"msg_{seq:08d}"


def alert_id(seq: int) -> str:
    return f"alert_{seq:06d}"
