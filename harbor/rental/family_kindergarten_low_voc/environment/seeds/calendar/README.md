# Family kindergarten rental — calendar data

This environment stores the household calendar known at Stage 0. It contains one calendar and eight distinct events covering work meetings, childcare routines, an existing family commitment, and time windows relevant to later viewing coordination.

Later schedule changes are not preloaded here. They enter through the task's dated mutations, so the Agent must re-read the calendar when a new notice arrives. Event titles, times, and descriptions represent separate commitments rather than numbered filler records.

`init.sql` is deterministic and contains no real personal data.
