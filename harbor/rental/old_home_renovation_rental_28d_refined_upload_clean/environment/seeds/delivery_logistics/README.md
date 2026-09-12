# Old-home renovation rental — delivery data

The Stage-0 state contains eleven saved addresses, nineteen shipments, thirty-six shipment events, six issue tickets, and twelve status subscriptions. The records cover ordinary delivery, returns, damage, address correction, missing scans, and completed household-maintenance shipments.

The refrigerator and washer deliveries used later in the renovation sequence are absent initially and are inserted by the dated mutation after the appliance decision. This preserves the acceptance-to-order-to-delivery sequence.

`init.sql` is deterministic and uses synthetic tracking and address data.
