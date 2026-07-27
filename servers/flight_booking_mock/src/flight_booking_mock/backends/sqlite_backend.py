"""SQLite-backed repository. One process-wide connection guarded by a lock."""
from __future__ import annotations

import json
import logging
import os
import sqlite3
import threading
from contextlib import contextmanager
from typing import Any, Iterator, Optional

logger = logging.getLogger(__name__)


SCHEMA_DDL = """
CREATE TABLE IF NOT EXISTS flights (
  flight_no     TEXT NOT NULL,
  origin        TEXT NOT NULL,
  dest          TEXT NOT NULL,
  depart_dt     TEXT NOT NULL,
  arrive_dt     TEXT NOT NULL,
  equipment     TEXT NOT NULL,
  base_price    REAL NOT NULL,
  currency      TEXT NOT NULL DEFAULT 'CNY',
  carrier       TEXT NOT NULL,
  PRIMARY KEY (flight_no, depart_dt)
);

CREATE INDEX IF NOT EXISTS idx_flights_route_date
  ON flights(origin, dest, substr(depart_dt,1,10));

CREATE TABLE IF NOT EXISTS fare_buckets (
  flight_no       TEXT NOT NULL,
  date            TEXT NOT NULL,
  cabin           TEXT NOT NULL,
  price           REAL NOT NULL,
  seats_remaining INTEGER NOT NULL,
  PRIMARY KEY (flight_no, date, cabin)
);

CREATE TABLE IF NOT EXISTS offers (
  offer_id      TEXT PRIMARY KEY,
  created_at    TEXT NOT NULL,
  expires_at    TEXT NOT NULL,
  payload_json  TEXT NOT NULL,
  priced_price  REAL,
  priced_at     TEXT,
  price_guarantee_until TEXT
);

CREATE INDEX IF NOT EXISTS idx_offers_expires ON offers(expires_at);

CREATE TABLE IF NOT EXISTS bookings (
  pnr           TEXT PRIMARY KEY,
  user_id       TEXT,
  offer_id      TEXT NOT NULL,
  status        TEXT NOT NULL,
  paid_amount   REAL NOT NULL,
  currency      TEXT NOT NULL DEFAULT 'CNY',
  created_at    TEXT NOT NULL,
  segments_json TEXT NOT NULL,
  passengers_json TEXT NOT NULL,
  contact_json  TEXT NOT NULL,
  history_json  TEXT NOT NULL DEFAULT '[]'
);

CREATE INDEX IF NOT EXISTS idx_bookings_user ON bookings(user_id);

CREATE TABLE IF NOT EXISTS seat_assignments (
  pnr           TEXT NOT NULL,
  segment_idx   INTEGER NOT NULL,
  pax_idx       INTEGER NOT NULL,
  seat          TEXT NOT NULL,
  checked_in    INTEGER NOT NULL DEFAULT 0,
  boarding_pass_id TEXT,
  PRIMARY KEY (pnr, segment_idx, pax_idx),
  FOREIGN KEY (pnr) REFERENCES bookings(pnr)
);

CREATE TABLE IF NOT EXISTS flight_status (
  flight_no      TEXT NOT NULL,
  date           TEXT NOT NULL,
  status         TEXT NOT NULL,
  actual_depart  TEXT,
  actual_arrive  TEXT,
  gate           TEXT,
  terminal       TEXT,
  delay_min      INTEGER NOT NULL DEFAULT 0,
  last_updated   TEXT NOT NULL,
  PRIMARY KEY (flight_no, date)
);

CREATE TABLE IF NOT EXISTS status_subscriptions (
  sub_id        TEXT PRIMARY KEY,
  flight_no     TEXT NOT NULL,
  date          TEXT NOT NULL,
  sink          TEXT NOT NULL,
  webhook_url   TEXT,
  created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_subs_flight_date
  ON status_subscriptions(flight_no, date);

CREATE TABLE IF NOT EXISTS notifications (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at    TEXT NOT NULL,
  channel       TEXT NOT NULL,
  payload_json  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notifs_created ON notifications(created_at);

CREATE TABLE IF NOT EXISTS _counters (
  name  TEXT PRIMARY KEY,
  value INTEGER NOT NULL
);
"""


class SQLiteBackend:
    """Thin repository over sqlite3 with thread-lock + row_factory."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._lock = threading.Lock()
        parent = os.path.dirname(os.path.abspath(db_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON;")
        self._conn.execute("PRAGMA journal_mode = WAL;")
        self._init_schema()

    # --------------- schema ---------------
    def _init_schema(self) -> None:
        with self._lock:
            self._conn.executescript(SCHEMA_DDL)
            self._conn.commit()

    def apply_init_sql(self, init_sql_path: str) -> None:
        """Execute an env-supplied ``init.sql`` against the freshly-created DB."""
        with self._lock:
            with open(init_sql_path, "r", encoding="utf-8") as f:
                self._conn.executescript(f.read())
            self._conn.commit()

    # --------------- connection helpers ---------------
    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        with self._lock:
            try:
                yield self._conn
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise

    @property
    def conn(self) -> sqlite3.Connection:
        return self._conn

    def query_all(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._lock:
            cur = self._conn.execute(sql, params)
            return cur.fetchall()

    def query_one(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        with self._lock:
            cur = self._conn.execute(sql, params)
            return cur.fetchone()

    def execute(self, sql: str, params: tuple = ()) -> None:
        with self._lock:
            self._conn.execute(sql, params)
            self._conn.commit()

    # --------------- flights ---------------
    def list_flights_for_route_date(self, origin: str, dest: str, date: str) -> list[sqlite3.Row]:
        sql = (
            "SELECT * FROM flights WHERE origin=? AND dest=? AND substr(depart_dt,1,10)=?"
            " ORDER BY depart_dt"
        )
        return self.query_all(sql, (origin, dest, date))

    def get_flight(self, flight_no: str, depart_dt_date: str) -> Optional[sqlite3.Row]:
        sql = "SELECT * FROM flights WHERE flight_no=? AND substr(depart_dt,1,10)=?"
        return self.query_one(sql, (flight_no, depart_dt_date))

    def get_flight_any_date(self, flight_no: str) -> Optional[sqlite3.Row]:
        sql = "SELECT * FROM flights WHERE flight_no=? LIMIT 1"
        return self.query_one(sql, (flight_no,))

    # --------------- fare_buckets ---------------
    def get_fare_buckets(self, flight_no: str, date: str) -> list[sqlite3.Row]:
        sql = "SELECT * FROM fare_buckets WHERE flight_no=? AND date=?"
        return self.query_all(sql, (flight_no, date))

    def get_fare_bucket(self, flight_no: str, date: str, cabin: str) -> Optional[sqlite3.Row]:
        sql = "SELECT * FROM fare_buckets WHERE flight_no=? AND date=? AND cabin=?"
        return self.query_one(sql, (flight_no, date, cabin))

    def all_fare_buckets(self) -> list[sqlite3.Row]:
        return self.query_all("SELECT * FROM fare_buckets")

    def update_fare_bucket_price(self, flight_no: str, date: str, cabin: str,
                                 price: float) -> None:
        self.execute(
            "UPDATE fare_buckets SET price=? WHERE flight_no=? AND date=? AND cabin=?",
            (price, flight_no, date, cabin),
        )

    def update_fare_bucket_seats(self, flight_no: str, date: str, cabin: str,
                                 seats_remaining: int) -> None:
        self.execute(
            "UPDATE fare_buckets SET seats_remaining=? WHERE flight_no=? AND date=? AND cabin=?",
            (seats_remaining, flight_no, date, cabin),
        )

    def decrement_fare_bucket_seats(self, flight_no: str, date: str, cabin: str,
                                    n: int) -> None:
        self.execute(
            "UPDATE fare_buckets SET seats_remaining = MAX(0, seats_remaining - ?) "
            "WHERE flight_no=? AND date=? AND cabin=?",
            (n, flight_no, date, cabin),
        )

    def increment_fare_bucket_seats(self, flight_no: str, date: str, cabin: str,
                                    n: int) -> None:
        self.execute(
            "UPDATE fare_buckets SET seats_remaining = seats_remaining + ? "
            "WHERE flight_no=? AND date=? AND cabin=?",
            (n, flight_no, date, cabin),
        )

    def all_flights(self) -> list[sqlite3.Row]:
        return self.query_all("SELECT * FROM flights")

    # --------------- offers ---------------
    def upsert_offer(self, offer_id: str, created_at: str, expires_at: str,
                     payload: dict[str, Any]) -> None:
        self.execute(
            "INSERT OR REPLACE INTO offers "
            "(offer_id, created_at, expires_at, payload_json, priced_price, priced_at, price_guarantee_until) "
            "VALUES (?,?,?,?,NULL,NULL,NULL)",
            (offer_id, created_at, expires_at, json.dumps(payload)),
        )

    def get_offer(self, offer_id: str) -> Optional[sqlite3.Row]:
        return self.query_one("SELECT * FROM offers WHERE offer_id=?", (offer_id,))

    def set_offer_pricing(self, offer_id: str, priced_price: float,
                          priced_at: str, guarantee_until: str) -> None:
        self.execute(
            "UPDATE offers SET priced_price=?, priced_at=?, price_guarantee_until=? "
            "WHERE offer_id=?",
            (priced_price, priced_at, guarantee_until, offer_id),
        )

    # --------------- bookings ---------------
    def insert_booking(self, row: dict[str, Any]) -> None:
        self.execute(
            "INSERT INTO bookings (pnr,user_id,offer_id,status,paid_amount,currency,"
            "created_at,segments_json,passengers_json,contact_json,history_json) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                row["pnr"], row.get("user_id"), row["offer_id"], row["status"],
                row["paid_amount"], row.get("currency", "CNY"), row["created_at"],
                json.dumps(row["segments"]), json.dumps(row["passengers"]),
                json.dumps(row["contact"]), json.dumps(row.get("history", [])),
            ),
        )

    def get_booking(self, pnr: str) -> Optional[sqlite3.Row]:
        return self.query_one("SELECT * FROM bookings WHERE pnr=?", (pnr,))

    def update_booking(self, pnr: str, **fields: Any) -> None:
        if not fields:
            return
        cols = ",".join(f"{k}=?" for k in fields.keys())
        vals = tuple(fields.values()) + (pnr,)
        self.execute(f"UPDATE bookings SET {cols} WHERE pnr=?", vals)

    def list_bookings(self, user_id: Optional[str] = None,
                      email: Optional[str] = None,
                      status: Optional[str] = None) -> list[sqlite3.Row]:
        clauses = []
        params: list[Any] = []
        if user_id:
            clauses.append("user_id = ?")
            params.append(user_id)
        if email:
            clauses.append("json_extract(contact_json, '$.email') = ?")
            params.append(email)
        if status:
            clauses.append("status = ?")
            params.append(status)
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"SELECT * FROM bookings {where} ORDER BY created_at DESC"
        return self.query_all(sql, tuple(params))

    # --------------- seat assignments ---------------
    def insert_seat_assignment(self, pnr: str, segment_idx: int, pax_idx: int,
                               seat: str) -> None:
        self.execute(
            "INSERT OR REPLACE INTO seat_assignments (pnr,segment_idx,pax_idx,seat,checked_in) "
            "VALUES (?,?,?,?,0)",
            (pnr, segment_idx, pax_idx, seat),
        )

    def get_seat_assignments(self, pnr: str) -> list[sqlite3.Row]:
        return self.query_all(
            "SELECT * FROM seat_assignments WHERE pnr=? ORDER BY segment_idx, pax_idx",
            (pnr,),
        )

    def mark_checked_in(self, pnr: str, segment_idx: int, pax_idx: int,
                        seat: str, boarding_pass_id: str) -> None:
        self.execute(
            "INSERT INTO seat_assignments (pnr,segment_idx,pax_idx,seat,checked_in,boarding_pass_id) "
            "VALUES (?,?,?,?,1,?) "
            "ON CONFLICT(pnr,segment_idx,pax_idx) DO UPDATE SET "
            "seat=excluded.seat, checked_in=1, boarding_pass_id=excluded.boarding_pass_id",
            (pnr, segment_idx, pax_idx, seat, boarding_pass_id),
        )

    def seat_taken_on_segment(self, flight_no: str, date: str, seat: str) -> bool:
        sql = (
            "SELECT 1 FROM seat_assignments sa "
            "JOIN bookings b ON b.pnr = sa.pnr "
            "WHERE sa.seat = ? AND b.status IN ('TICKETED','HOLD','CHANGED') "
            "AND EXISTS (SELECT 1 FROM json_each(b.segments_json) j "
            "WHERE json_extract(j.value,'$.segment_idx') = sa.segment_idx "
            "AND json_extract(j.value,'$.flight_no') = ? "
            "AND substr(json_extract(j.value,'$.depart_dt'),1,10) = ?) LIMIT 1"
        )
        return self.query_one(sql, (seat, flight_no, date)) is not None

    # --------------- flight status ---------------
    def get_flight_status(self, flight_no: str, date: str) -> Optional[sqlite3.Row]:
        return self.query_one(
            "SELECT * FROM flight_status WHERE flight_no=? AND date=?",
            (flight_no, date),
        )

    def upsert_flight_status(self, flight_no: str, date: str,
                             status: str, last_updated: str,
                             actual_depart: Optional[str] = None,
                             actual_arrive: Optional[str] = None,
                             gate: Optional[str] = None,
                             terminal: Optional[str] = None,
                             delay_min: Optional[int] = None) -> None:
        # When delay_min is None, preserve the existing value on conflict.
        insert_delay = 0 if delay_min is None else int(delay_min)
        self.execute(
            "INSERT INTO flight_status (flight_no,date,status,actual_depart,actual_arrive,"
            "gate,terminal,delay_min,last_updated) VALUES (?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(flight_no,date) DO UPDATE SET "
            "status=excluded.status, "
            "actual_depart=COALESCE(excluded.actual_depart, flight_status.actual_depart), "
            "actual_arrive=COALESCE(excluded.actual_arrive, flight_status.actual_arrive), "
            "gate=COALESCE(excluded.gate, flight_status.gate), "
            "terminal=COALESCE(excluded.terminal, flight_status.terminal), "
            "delay_min=COALESCE(?, flight_status.delay_min), "
            "last_updated=excluded.last_updated",
            (flight_no, date, status, actual_depart, actual_arrive,
             gate, terminal, insert_delay, last_updated, delay_min),
        )

    def all_flight_status_on_date(self, date: str) -> list[sqlite3.Row]:
        return self.query_all("SELECT * FROM flight_status WHERE date=?", (date,))

    # --------------- subscriptions + notifications ---------------
    def insert_subscription(self, sub_id: str, flight_no: str, date: str,
                            sink: str, webhook_url: Optional[str],
                            created_at: str) -> None:
        self.execute(
            "INSERT INTO status_subscriptions "
            "(sub_id, flight_no, date, sink, webhook_url, created_at) "
            "VALUES (?,?,?,?,?,?)",
            (sub_id, flight_no, date, sink, webhook_url, created_at),
        )

    def get_subscriptions_for(self, flight_no: str, date: str) -> list[sqlite3.Row]:
        return self.query_all(
            "SELECT * FROM status_subscriptions WHERE flight_no=? AND date=?",
            (flight_no, date),
        )

    def insert_notification(self, created_at: str, channel: str,
                            payload: dict[str, Any]) -> None:
        self.execute(
            "INSERT INTO notifications (created_at, channel, payload_json) "
            "VALUES (?,?,?)",
            (created_at, channel, json.dumps(payload)),
        )

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass
