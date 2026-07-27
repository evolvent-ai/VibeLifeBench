def message_id_header(seq: int) -> str:
    """Generate an RFC-5322 style Message-ID header for an outgoing message."""
    return f"<emails-mcp-{seq:08d}@mock.local>"


def attachment_id(seq: int) -> str:
    return f"att_{seq:08d}"
