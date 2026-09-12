# Family kindergarten rental — delivery and moving data

Stage 0 contains two saved household addresses used to obtain moving-service estimates. No shipment or booked pickup exists initially.

Quote-only moving records are introduced by later task mutations. They carry different service scopes, dates, prices, and capacity constraints so the household can compare costs without booking, paying, or implying that a carrier has been selected.

`init.sql` is deterministic and contains synthetic contact details.
