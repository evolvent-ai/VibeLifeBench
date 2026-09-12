# Family kindergarten rental — notification data

Stage 0 contains one subscription and three ordinary notifications about rental monitoring, household scheduling, and service updates. The notifications are short channel summaries with distinct sources and timestamps.

Construction, payment-pressure, and other later notices are not present initially; they are inserted by the corresponding dated mutations after their source facts are available.

`init.sql` is deterministic and uses synthetic account data.
