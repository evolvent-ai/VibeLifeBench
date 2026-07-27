"""Listing discovery + detail, agent lookup/contact, self-listing, subscriptions."""
import json
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.exceptions import (
    BadArgError,
    BadCategoryError,
    BadPriceError,
    ListingDelistedError,
    NotOwnerError,
)
from ..utils.ids import (
    contact_id as make_contact_id,
    listing_id as make_listing_id,
    subscription_id as make_subscription_id,
)
from ._repo import (
    agent_view,
    fetch_agent,
    fetch_listing,
    listing_detail,
    listing_summary,
    synth_timestamp,
)

logger = logging.getLogger(__name__)

VALID_CATEGORIES = ("rent", "sale_house", "used_car", "secondhand")
VALID_SORTS = ("price_asc", "price_desc", "newest", "area_desc")


class ListingService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- search ----------------------------------------------------------
    def search_listings(
        self,
        category: str,
        city: Optional[str] = None,
        district: Optional[str] = None,
        min_price_minor: Optional[int] = None,
        max_price_minor: Optional[int] = None,
        min_rooms: Optional[int] = None,
        max_rooms: Optional[int] = None,
        keyword: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
    ) -> List[dict]:
        if category not in VALID_CATEGORIES:
            raise BadCategoryError(f"category must be one of {VALID_CATEGORIES}")
        if sort is not None and sort not in VALID_SORTS:
            raise BadArgError(f"sort must be one of {VALID_SORTS}")
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 200:
            limit = 200

        sql = ["SELECT * FROM listings WHERE category = ? AND status = 'active'"]
        args: List = [category]
        if city:
            sql.append("AND city = ?")
            args.append(city)
        if district:
            sql.append("AND district = ?")
            args.append(district)
        if min_price_minor is not None:
            sql.append("AND price_minor >= ?")
            args.append(int(min_price_minor))
        if max_price_minor is not None:
            sql.append("AND price_minor <= ?")
            args.append(int(max_price_minor))
        if min_rooms is not None:
            sql.append("AND rooms >= ?")
            args.append(int(min_rooms))
        if max_rooms is not None:
            sql.append("AND rooms <= ?")
            args.append(int(max_rooms))
        if keyword:
            sql.append("AND (title LIKE ? OR community LIKE ? OR description LIKE ?)")
            like = f"%{keyword}%"
            args.extend([like, like, like])

        order = {
            "price_asc": "price_minor ASC, listing_id ASC",
            "price_desc": "price_minor DESC, listing_id ASC",
            "area_desc": "area_sqm DESC, listing_id ASC",
            "newest": "listed_at DESC, listing_id DESC",
        }.get(sort or "newest", "listed_at DESC, listing_id DESC")
        sql.append(f"ORDER BY {order} LIMIT ?")
        args.append(int(limit))

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [listing_summary(r) for r in rows]

    # ---- get / detail ----------------------------------------------------
    def get_listing(self, listing_id: str) -> dict:
        return listing_summary(fetch_listing(self.conn, listing_id))

    def get_listing_detail(self, listing_id: str) -> dict:
        row = fetch_listing(self.conn, listing_id)
        detail = listing_detail(row)
        if row["agent_id"]:
            try:
                detail["agent"] = agent_view(fetch_agent(self.conn, row["agent_id"]))
            except Exception:
                detail["agent"] = None
        else:
            detail["agent"] = None
        return detail

    # ---- agent -----------------------------------------------------------
    def get_agent(self, agent_id: str) -> dict:
        return agent_view(fetch_agent(self.conn, agent_id))

    def contact_agent(self, user_id: str, listing_id: str, message: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        if not message:
            raise BadArgError("message is required")
        row = fetch_listing(self.conn, listing_id)
        if row["status"] != "active":
            raise ListingDelistedError(f"listing {listing_id} is delisted")
        agent_id = row["agent_id"]
        seq = next_counter(self.conn, "contact_seq")
        cid = make_contact_id(seq)
        created = synth_timestamp(seq)
        self.conn.execute(
            """
            INSERT INTO contacts (contact_id, user_id, listing_id, agent_id, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (cid, user_id, listing_id, agent_id, message, created),
        )
        agent = None
        if agent_id:
            try:
                agent = agent_view(fetch_agent(self.conn, agent_id))
            except Exception:
                agent = None
        return {
            "contact_id": cid,
            "listing_id": listing_id,
            "agent_id": agent_id,
            "agent": agent,
            "message": message,
            "created_at": created,
            "status": "sent",
        }

    # ---- self-listing ----------------------------------------------------
    def post_listing(
        self,
        user_id: str,
        category: str,
        title: str,
        price_minor: int,
        city: str,
        district: Optional[str] = None,
        community: Optional[str] = None,
        area_sqm: Optional[float] = None,
        rooms: Optional[int] = None,
        metro: Optional[str] = None,
        description: Optional[str] = None,
        attrs: Optional[dict] = None,
        photos: Optional[list] = None,
    ) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        if category not in VALID_CATEGORIES:
            raise BadCategoryError(f"category must be one of {VALID_CATEGORIES}")
        if not title:
            raise BadArgError("title is required")
        if not city:
            raise BadArgError("city is required")
        if price_minor is None or int(price_minor) <= 0:
            raise BadPriceError("price_minor must be a positive integer (分)")

        seq = next_counter(self.conn, "listing_seq")
        lid = make_listing_id(seq)
        listed = synth_timestamp(seq)
        attrs_json = json.dumps(attrs or {}, ensure_ascii=False)
        photos_json = json.dumps(photos or [], ensure_ascii=False)
        self.conn.execute(
            """
            INSERT INTO listings (
                listing_id, category, title, city, district, community,
                price_minor, area_sqm, rooms, metro, attrs_json, description,
                photos_json, agent_id, owner_user_id, status, listed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, 'active', ?)
            """,
            (
                lid, category, title, city, district, community,
                int(price_minor), area_sqm, rooms, metro, attrs_json,
                description, photos_json, user_id, listed,
            ),
        )
        return listing_detail(fetch_listing(self.conn, lid))

    def delist(self, listing_id: str, user_id: Optional[str] = None) -> dict:
        row = fetch_listing(self.conn, listing_id)
        if user_id is not None and row["owner_user_id"] != user_id:
            raise NotOwnerError(
                f"user {user_id} does not own listing {listing_id}"
            )
        self.conn.execute(
            "UPDATE listings SET status = 'delisted' WHERE listing_id = ?",
            (listing_id,),
        )
        return {
            "listing_id": listing_id,
            "status": "delisted",
        }

    # ---- saved-search subscription --------------------------------------
    def subscribe_search(self, user_id: str, query_json: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        if not query_json:
            raise BadArgError("query_json is required")
        # Validate it parses as JSON (stored verbatim regardless).
        try:
            json.loads(query_json)
        except (TypeError, ValueError) as e:
            raise BadArgError(f"query_json must be valid JSON: {e}")
        seq = next_counter(self.conn, "subscription_seq")
        sid = make_subscription_id(seq)
        created = synth_timestamp(seq)
        self.conn.execute(
            """
            INSERT INTO search_subscriptions (subscription_id, user_id, query_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (sid, user_id, query_json, created),
        )
        return {
            "subscription_id": sid,
            "user_id": user_id,
            "query": json.loads(query_json),
            "created_at": created,
        }
