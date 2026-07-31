# ecommerce-mock

A self-contained, fully offline FastMCP server that mocks a Chinese
e-commerce marketplace (taobao / JD style). All money is integer 分
(RMB minor units). The server speaks **streamable-http only** — no
stdio fallback.

The server has no simulated clock and no management CLI. Stage-driven state
changes (order shipping, refund approvals, etc.) are applied as SQL
mutations by the task orchestrator.

**See [SPEC.md](./SPEC.md) for the full tool / schema / error spec.**

## Install & run

```bash
# From this directory:
pip install -e .
ecommerce-mock --port 8000 --env ../../envs/ecommerce/618_setup
```

Flags:

- `--env PATH` — required; path to an `envs/<server>/<env_name>/` directory.
- `--host HOST` — bind address (default `0.0.0.0`).
- `--port PORT` — listening port (pass `8000` for Docker/Terrarium parity).
- `--debug` — verbose logging.

On startup the server unlinks `<env>/runtime.db`, creates the schema,
runs `<env>/init.sql` if present, and binds streamable-HTTP at
`http://<host>:<port>/mcp`.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Boots the server on an ephemeral port against
`envs/ecommerce/618_setup`, then drives `search_products → add_to_cart →
list_addresses → place_order → get_order → request_refund` over HTTP
and verifies the structured error envelope for missing products.

## Agent-facing tools

Catalog: `search_products`, `get_product`.
Cart: `get_cart`, `add_to_cart`, `update_cart_item`, `remove_from_cart`.
Coupons: `apply_coupon`, `remove_coupon`.
Addresses: `list_addresses`, `add_address`.
Orders: `place_order`, `list_orders`, `get_order`, `cancel_order`, `track_order`.
Refunds: `request_refund`.

All tools return JSON strings. Errors use `{"error": "...", "code": "..."}`;
see SPEC.md Appendix A for the full code list.
