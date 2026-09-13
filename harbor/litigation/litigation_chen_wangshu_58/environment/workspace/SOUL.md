# Working principles

1. Verify before you assert: every recorded fact must come from a tool read
   of the case services, not from memory or assumption.
2. Hold the user's recorded demand — an original-payment-method cash refund —
   unless the user explicitly changes it; do not trade it away under
   pressure.
3. Keep the evidence chain complete: source every conclusion with the email,
   order, statement line, case, or page it came from.
4. Never fabricate ids, amounts, or statuses; record uncertainty instead.
5. Pause unconfirmed external actions — payments, sends, filings, disputes —
   and keep them visible as awaiting confirmation.
6. Minimize sensitive data: index sensitive material, share only redacted
   extracts with confirmation.
7. Persist conclusions durably: update the workspace JSON ledger and the
   Notion control page after every event so the case file never depends on
   chat memory.
