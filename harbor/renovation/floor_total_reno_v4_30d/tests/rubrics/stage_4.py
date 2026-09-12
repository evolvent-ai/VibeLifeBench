"""Stage 4 — verify the released manufacturer protocol and its attachment lineage."""
from .shared import _helpers as R
from .shared import _helpers as H

def s4_servers(env):
    message = R.backend_exists(env, "email", "SELECT COUNT(*) FROM messages WHERE id=4001 AND message_id=?", ("<qflr-protocol-0618@thermal.example>",))
    attachment = R.backend_exists(env, "email", "SELECT COUNT(*) FROM attachments WHERE id=4101 AND message_id=4001", ())
    return message and attachment and R.trace_has_success(env, 4, ("email",), min_count=1)

def s4_reject(env):
    return H.protocol(env) and (R.artifact_has(env, "/workspace/evidence_log.md", (("qflr-coil-controller-protocol-v2.pdf",), ("supply and return water temperature",), ("pressure",), ("batch",), ("does not constitute", "cannot replace"), ("flooring acceptance", "acceptance"))))

CHECKS = [("s4_servers", s4_servers, 0.5), ("s4_reject", s4_reject, 4.0)]
