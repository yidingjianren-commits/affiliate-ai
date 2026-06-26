"""
Conversion tracking & analytics engine.

Stores everything in SQLite:
  - generated_content: what content was created
  - published_items: what was published where
  - clicks: tracked link clicks
  - conversions: confirmed conversions/commissions

This is the feedback loop that tells you what's working.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional


DB_PATH = Path(__file__).parent.parent / "data" / "tracking.db"


class Tracker:
    """Tracks all content, publishing, and conversion activity."""

    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS generated_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    region TEXT DEFAULT 'us',
                    keyword TEXT,
                    title TEXT,
                    file_path TEXT,
                    word_count INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now'))
                );

                CREATE TABLE IF NOT EXISTS published_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id INTEGER,
                    platform TEXT NOT NULL,
                    url TEXT,
                    status TEXT DEFAULT 'draft',
                    published_at TEXT,
                    notes TEXT,
                    FOREIGN KEY (content_id) REFERENCES generated_content(id)
                );

                CREATE TABLE IF NOT EXISTS clicks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    published_id INTEGER,
                    source TEXT,
                    clicked_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (published_id) REFERENCES published_items(id)
                );

                CREATE TABLE IF NOT EXISTS conversions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    published_id INTEGER,
                    product TEXT NOT NULL,
                    commission REAL DEFAULT 0,
                    currency TEXT DEFAULT 'USD',
                    confirmed_at TEXT DEFAULT (datetime('now')),
                    notes TEXT,
                    FOREIGN KEY (published_id) REFERENCES published_items(id)
                );

                CREATE TABLE IF NOT EXISTS performance_snapshot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_date TEXT UNIQUE,
                    total_content INTEGER DEFAULT 0,
                    total_published INTEGER DEFAULT 0,
                    total_clicks INTEGER DEFAULT 0,
                    total_conversions INTEGER DEFAULT 0,
                    total_commission REAL DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now'))
                );
            """)

    def log_generation(self, product: str, platform: str, title: str,
                       file_path: str, keyword: str = "", region: str = "us",
                       word_count: int = 0) -> int:
        """Record content generation event."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                """INSERT INTO generated_content
                   (product, platform, region, keyword, title, file_path, word_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (product, platform, region, keyword, title, file_path, word_count),
            )
            return cur.lastrowid

    def log_publish(self, content_id: int, platform: str, url: str = "",
                    status: str = "published", notes: str = "") -> int:
        """Record content publishing event."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                """INSERT INTO published_items
                   (content_id, platform, url, status, published_at, notes)
                   VALUES (?, ?, ?, ?, datetime('now'), ?)""",
                (content_id, platform, url, status, notes),
            )
            return cur.lastrowid

    def log_click(self, published_id: int, source: str = "") -> int:
        """Track a link click."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO clicks (published_id, source) VALUES (?, ?)",
                (published_id, source),
            )
            return cur.lastrowid

    def log_conversion(self, published_id: int, product: str,
                       commission: float = 0.0, notes: str = "") -> int:
        """Track a confirmed conversion."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                """INSERT INTO conversions
                   (published_id, product, commission, notes)
                   VALUES (?, ?, ?, ?)""",
                (published_id, product, commission, notes),
            )
            return cur.lastrowid

    def get_stats(self) -> dict:
        """Get aggregate statistics."""
        with sqlite3.connect(self.db_path) as conn:
            stats = conn.execute("""
                SELECT
                    (SELECT COUNT(*) FROM generated_content) as total_content,
                    (SELECT COUNT(*) FROM published_items) as total_published,
                    (SELECT COUNT(*) FROM clicks) as total_clicks,
                    (SELECT COUNT(*) FROM conversions) as total_conversions,
                    (SELECT COALESCE(SUM(commission), 0) FROM conversions) as total_commission
            """).fetchone()

            by_product = conn.execute("""
                SELECT product, COUNT(*) as count
                FROM generated_content GROUP BY product ORDER BY count DESC
            """).fetchall()

            return {
                "total_content": stats[0],
                "total_published": stats[1],
                "total_clicks": stats[2],
                "total_conversions": stats[3],
                "total_commission": stats[4],
                "by_product": dict(by_product),
            }

    def get_best_performers(self, limit: int = 5) -> list:
        """Get best-converting products."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT gc.product, gc.platform, gc.title, COUNT(c.id) as clicks
                FROM generated_content gc
                LEFT JOIN published_items pi ON gc.id = pi.content_id
                LEFT JOIN clicks c ON pi.id = c.published_id
                GROUP BY gc.id
                ORDER BY clicks DESC
                LIMIT ?
            """, (limit,)).fetchall()
            return [{"product": r[0], "platform": r[1], "title": r[2], "clicks": r[3]} for r in rows]
