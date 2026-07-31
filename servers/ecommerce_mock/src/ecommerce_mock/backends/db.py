"""SQLite schema + connection helpers for ecommerce_mock.

Schema-only. No bundled seed data — callers inject state via the env's
``init.sql``, run by ``server.py`` on cold start.
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS products (
  product_id        TEXT PRIMARY KEY,
  title             TEXT NOT NULL,
  brand             TEXT NOT NULL,
  category          TEXT NOT NULL,
  description       TEXT NOT NULL DEFAULT '',
  rating            REAL NOT NULL DEFAULT 0,
  rating_count      INTEGER NOT NULL DEFAULT 0,
  sales_count       INTEGER NOT NULL DEFAULT 0,
  base_price_minor  INTEGER NOT NULL DEFAULT 0,
  return_policy     TEXT NOT NULL DEFAULT '7天无理由退货'
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_brand    ON products(brand);

CREATE TABLE IF NOT EXISTS skus (
  sku_id        TEXT PRIMARY KEY,
  product_id    TEXT NOT NULL,
  attrs_json    TEXT NOT NULL DEFAULT '{}',
  price_minor   INTEGER NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_skus_product ON skus(product_id);

CREATE TABLE IF NOT EXISTS stocks (
  sku_id    TEXT PRIMARY KEY,
  quantity  INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (sku_id) REFERENCES skus(sku_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS addresses (
  address_id   TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL,
  recipient    TEXT NOT NULL,
  phone        TEXT NOT NULL,
  province     TEXT NOT NULL,
  city         TEXT NOT NULL,
  district     TEXT NOT NULL,
  detail       TEXT NOT NULL,
  postal_code  TEXT NOT NULL,
  is_default   INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_addresses_user ON addresses(user_id);

CREATE TABLE IF NOT EXISTS carts (
  user_id     TEXT PRIMARY KEY,
  updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cart_items (
  cart_item_id      TEXT PRIMARY KEY,
  user_id           TEXT NOT NULL,
  product_id        TEXT NOT NULL,
  sku_id            TEXT NOT NULL,
  qty               INTEGER NOT NULL CHECK (qty > 0),
  unit_price_minor  INTEGER NOT NULL,
  added_at          TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES carts(user_id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (sku_id) REFERENCES skus(sku_id)
);

CREATE INDEX IF NOT EXISTS idx_cart_items_user ON cart_items(user_id);

CREATE TABLE IF NOT EXISTS coupons (
  code                  TEXT PRIMARY KEY,
  kind                  TEXT NOT NULL CHECK(kind IN ('percent_off','flat_off','free_shipping')),
  value_bp_or_minor     INTEGER NOT NULL DEFAULT 0,
  min_spend_minor       INTEGER NOT NULL DEFAULT 0,
  valid_from            TEXT NOT NULL,
  valid_until           TEXT NOT NULL,
  category_restriction  TEXT,
  max_uses              INTEGER NOT NULL DEFAULT 0,
  used_count            INTEGER NOT NULL DEFAULT 0,
  active                INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS applied_coupons (
  user_id     TEXT NOT NULL,
  code        TEXT NOT NULL,
  applied_at  TEXT NOT NULL,
  PRIMARY KEY (user_id, code),
  FOREIGN KEY (user_id) REFERENCES carts(user_id) ON DELETE CASCADE,
  FOREIGN KEY (code) REFERENCES coupons(code)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id          TEXT PRIMARY KEY,
  user_id           TEXT NOT NULL,
  address_id        TEXT NOT NULL,
  payment_method    TEXT NOT NULL,
  subtotal_minor    INTEGER NOT NULL,
  discount_minor    INTEGER NOT NULL DEFAULT 0,
  shipping_minor    INTEGER NOT NULL DEFAULT 0,
  total_minor       INTEGER NOT NULL,
  status            TEXT NOT NULL CHECK(status IN (
                      'pending_payment','paid','shipped','delivered',
                      'completed','refund_requested','refunded','cancelled')),
  placed_at         TEXT NOT NULL,
  note              TEXT,
  tracking_no       TEXT
);

CREATE INDEX IF NOT EXISTS idx_orders_user   ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

CREATE TABLE IF NOT EXISTS order_items (
  item_id           TEXT PRIMARY KEY,
  order_id          TEXT NOT NULL,
  product_id        TEXT NOT NULL,
  sku_id            TEXT NOT NULL,
  qty               INTEGER NOT NULL CHECK (qty > 0),
  unit_price_minor  INTEGER NOT NULL,
  line_total_minor  INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);

CREATE TABLE IF NOT EXISTS order_status_history (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id  TEXT NOT NULL,
  status    TEXT NOT NULL,
  set_at    TEXT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_order_history_order ON order_status_history(order_id);

CREATE TABLE IF NOT EXISTS refunds (
  refund_id            TEXT PRIMARY KEY,
  order_id             TEXT NOT NULL,
  item_id              TEXT NOT NULL,
  qty                  INTEGER NOT NULL CHECK (qty > 0),
  reason               TEXT NOT NULL,
  status               TEXT NOT NULL CHECK(status IN ('submitted','approved','rejected','refunded')),
  opened_at            TEXT NOT NULL,
  resolved_at          TEXT,
  refund_amount_minor  INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
  FOREIGN KEY (item_id) REFERENCES order_items(item_id)
);

CREATE INDEX IF NOT EXISTS idx_refunds_order ON refunds(order_id);

CREATE TABLE IF NOT EXISTS _counters (
  key   TEXT PRIMARY KEY,
  value INTEGER NOT NULL DEFAULT 0
);
"""


def get_conn(db_path: str) -> sqlite3.Connection:
    """Return a SQLite connection with the project's PRAGMA defaults applied."""
    parent = os.path.dirname(os.path.abspath(db_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(db_path, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Create tables (idempotent)."""
    conn.executescript(SCHEMA_SQL)


def next_counter(conn: sqlite3.Connection, key: str) -> int:
    """Atomically bump and return a counter's new value."""
    conn.execute(
        "INSERT INTO _counters (key, value) VALUES (?, 0) ON CONFLICT(key) DO NOTHING",
        (key,),
    )
    conn.execute("UPDATE _counters SET value = value + 1 WHERE key = ?", (key,))
    row = conn.execute("SELECT value FROM _counters WHERE key = ?", (key,)).fetchone()
    return int(row["value"])
