def tx_id(seq: int, sim_date: str) -> str:
    return f"tx_{sim_date.replace('-', '')}_{seq:08d}"


def payee_id(seq: int) -> str:
    return f"pay_{seq:06d}"


def schedule_id(seq: int) -> str:
    return f"sch_{seq:06d}"


def pending_id(seq: int) -> str:
    return f"pend_{seq:06d}"


def mask_account_no(account_no: str) -> str:
    """Mask all but the last 4 chars of an account number with a single ``*`` run."""
    s = (account_no or "").strip()
    if len(s) <= 4:
        return "*" * len(s)
    return "*" * (len(s) - 4) + s[-4:]
