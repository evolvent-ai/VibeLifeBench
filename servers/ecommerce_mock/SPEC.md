# ecommerce-mock SPEC

Implementer-facing reference. Money is integer 分 (1 RMB = 100 分),
dates are ISO `YYYY-MM-DD`, all IDs are domain-prefixed strings, and
all tools return `json.dumps(result, ensure_ascii=False)`.

The server runs over **streamable-http only** on `/mcp`. The server has
no simulated clock; stage-driven state transitions (orders → shipped /
delivered, refunds → approved, etc.) are applied by the v3
orchestrator as SQL `mutation` events against this server's runtime DB.

---

## 1. Tools

### 1.1 Catalog

#### `search_products(query, category=None, filters=None, sort=None, limit=20) -> str`

Substring match against `title`, `brand`, `description`. Filters:

- `max_price_minor`, `min_price_minor` — bound on per-product SKU price.
- `brand` — exact match.
- `in_stock_only` — drop products whose every SKU has 0 stock.
- `min_rating` — float.

Sorts: `relevance` (default) | `price_asc` | `price_desc` | `rating_desc` | `sales_desc`.

Returns an array of:
```
{product_id, title, brand, category, price_minor, min_sku_price_minor,
 max_sku_price_minor, rating, sales_count, in_stock, thumbnail_url}
```

#### `get_product(product_id) -> str`

Returns the full product:
```
{product_id, title, brand, category, description, rating, rating_count,
 sales_count,
 skus: [{sku_id, attrs: {color|size, ...}, price_minor, stock}, ...],
 reviews_summary: {average_rating, count},
 return_policy}
```

### 1.2 Cart

All cart tools return the same shape:
```
{user_id, items: [{cart_item_id, product_id, sku_id, qty,
                   unit_price_minor, line_total_minor}, ...],
 subtotal_minor, applied_coupons: [{code, kind, discount_minor}, ...],
 discount_minor, total_minor}
```

- `get_cart(user_id)`
- `add_to_cart(user_id, product_id, sku_id, qty)` — same `(user, sku)` line merges.
- `update_cart_item(user_id, cart_item_id, qty)` — `qty=0` removes the line.
- `remove_from_cart(user_id, cart_item_id)`

### 1.3 Coupons

- `apply_coupon(user_id, code)`
- `remove_coupon(user_id, code)`

Validation order: existence → `active=1` → `current_date in [valid_from, valid_until]`
→ `used_count < max_uses` → eligible subtotal ≥ `min_spend_minor` → category
restriction holds.

Kinds:

- `percent_off` — `discount = floor(eligible_subtotal * value_bp / 10000)`,
  where `value_bp` is basis points (1500 = 15%).
- `flat_off` — `discount = min(value_minor, eligible_subtotal)`.
- `free_shipping` — contributes 0 to cart discount; at `place_order`
  time, `shipping_minor` is set to 0.

When the cart is recomputed after add/update/remove, any coupon that
no longer qualifies is silently detached.

### 1.4 Addresses

- `list_addresses(user_id)` — returns the list, default first.
- `add_address(user_id, recipient, phone, province, city, district,
  detail, postal_code, is_default=False)` — if `is_default`, demotes
  other addresses for the same user.

### 1.5 Orders

- `place_order(user_id, address_id, payment_method, note=None)` — converts
  the current cart into a paid order: decrements stock, bumps each
  product's `sales_count`, increments each applied coupon's `used_count`,
  clears `cart_items` and `applied_coupons` for the user, and writes a
  `pending_payment` → `paid` status history. Returns
  `{order_id, total_minor, item_count, status: "paid"}`.

  - `shipping_minor` is `0` when any applied coupon kind is
    `free_shipping`, else `800` (¥8 flat).

- `list_orders(user_id, status_filter=None, limit=20)` — newest first.
- `get_order(order_id)` — header + `items[]` + `status_history[]` + `refunds[]`.
- `cancel_order(order_id, reason)` — only when status is
  `pending_payment` or `paid`. Releases reserved stock; transitions to
  `cancelled`.
- `track_order(order_id)` — `{order_id, tracking_no, latest_status, updated_at}`.

### 1.6 Refunds

- `request_refund(order_id, item_id, qty, reason)` — eligible when order
  status is `paid | shipped | delivered | completed | refund_requested`
  and within 7 calendar days of `placed_at`. Returns
  `{refund_id, order_id, item_id, qty, status: "submitted",
    refund_amount_minor, opened_at}` and bumps the parent order to
  `refund_requested` (if not already past it).
  Approval is applied by orchestrator-issued mutation events.

---

## 2. Tables (created by `backends/db.py`)

```
products(product_id PK, title, brand, category, description,
         rating, rating_count, sales_count, base_price_minor, return_policy)
skus(sku_id PK, product_id FK, attrs_json, price_minor)
stocks(sku_id PK FK, quantity)
addresses(address_id PK, user_id, recipient, phone, province, city,
          district, detail, postal_code, is_default)
carts(user_id PK, updated_at)
cart_items(cart_item_id PK, user_id FK, product_id, sku_id, qty,
           unit_price_minor, added_at)
coupons(code PK, kind, value_bp_or_minor, min_spend_minor, valid_from,
        valid_until, category_restriction, max_uses, used_count, active)
applied_coupons(user_id FK, code FK, applied_at, PRIMARY KEY (user_id, code))
orders(order_id PK, user_id, address_id, payment_method,
       subtotal_minor, discount_minor, shipping_minor, total_minor,
       status, placed_at, note, tracking_no)
order_items(item_id PK, order_id FK, product_id, sku_id, qty,
            unit_price_minor, line_total_minor)
order_status_history(id PK, order_id FK, status, set_at)
refunds(refund_id PK, order_id FK, item_id FK, qty, reason, status,
        opened_at, resolved_at, refund_amount_minor)
_counters(key PK, value)
```

Order status enum (CHECK constraint):
`pending_payment | paid | shipped | delivered | completed
 | refund_requested | refunded | cancelled`.

Refund status enum: `submitted | approved | rejected | refunded`.

Coupon kind enum: `percent_off | flat_off | free_shipping`.

---

## 3. State evolution across stages

This server has no management CLI and no internal sweep. State transitions
(paid → shipped, shipped → delivered, refunds submitted → approved,
parent-order rolled to `refunded` when every line item is fully
refunded) are applied by the v3 orchestrator as `mutation` events in
each task's `event.yaml`. A mutation is one or more SQL statements
executed against this server's runtime DB.

If a task wants D3 to feel "later than D2", the task writes the new
`orders.status`, `order_status_history` row, and `refunds.status`
updates directly in its stage-N overlay SQL.

---

## Appendix A — error codes

| Code                       | When                                                                   |
| -------------------------- | ---------------------------------------------------------------------- |
| `BAD_ARG`                  | Argument missing / wrong type / out of range; also the catch-all.      |
| `PRODUCT_NOT_FOUND`        | `get_product` for an unknown product_id; `add_to_cart` sku/product mismatch. |
| `SKU_NOT_FOUND`            | `add_to_cart` with an unknown sku_id.                                  |
| `OUT_OF_STOCK`             | Cart add / update / order would exceed `stocks.quantity`.              |
| `CART_EMPTY`               | `place_order` with no cart items.                                      |
| `CART_ITEM_NOT_FOUND`      | `update_cart_item` / `remove_from_cart` against a missing line.        |
| `ADDRESS_NOT_FOUND`        | `place_order` with an address_id not owned by the user.                |
| `COUPON_INVALID`           | Unknown / inactive / not-yet-active / used-up / cart empty.            |
| `COUPON_EXPIRED`           | `current_date > valid_until`.                                          |
| `COUPON_BELOW_MIN`         | Eligible subtotal < `min_spend_minor`.                                 |
| `COUPON_CATEGORY_MISMATCH` | Restricted category has no eligible items in cart.                     |
| `COUPON_NOT_APPLIED`       | `remove_coupon` for a code not on the cart.                            |
| `ORDER_NOT_FOUND`          | Order lookup with unknown order_id.                                    |
| `ORDER_NOT_CANCELABLE`     | `cancel_order` when status is not in {pending_payment, paid}.          |
| `ORDER_ITEM_NOT_FOUND`     | `request_refund` with an item not on the named order.                  |
| `REFUND_WINDOW_CLOSED`     | Status not eligible, or > 7 sim days since `placed_at`.                |
