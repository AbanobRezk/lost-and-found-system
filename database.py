"""
database.py
------------
Handles all persistence (SQLite) for the Lost & Found Search System.

This module does NOT change any of the OOP logic in models.py.
It simply knows how to:
    1. Create the items table if it doesn't exist.
    2. Save a LostItem/FoundItem object into the database.
    3. Load all rows back from the database as LostItem/FoundItem objects.
    4. Delete a row by item_id.
    5. Update the status of a row by item_id.

The GUI and LostFoundSystem stay in sync with the database through this class.
"""

import sqlite3
from models import LostItem, FoundItem


class Database:
    def __init__(self, db_path="lost_found.db"):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                brand TEXT,
                color TEXT,
                location TEXT,
                date TEXT,
                description TEXT,
                item_type TEXT NOT NULL,
                status TEXT NOT NULL,
                reward REAL,
                storage_loc TEXT
            )
        """)
        conn.commit()
        conn.close()

    def insert_item(self, item):
        """
        Accepts a LostItem or FoundItem object and stores it in the database.
        reward is only filled for LostItem; storage_loc only for FoundItem.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        reward = item.get_reward() if isinstance(item, LostItem) else None
        storage_loc = item.get_storage_loc() if isinstance(item, FoundItem) else None

        cursor.execute("""
            INSERT INTO items
            (item_id, name, brand, color, location, date, description, item_type, status, reward, storage_loc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get_item_id(), item.get_name(), item.get_brand(), item.get_color(),
            item.get_location(), item.get_date(), item.get_description(),
            item.get_type(), item.get_status(), reward, storage_loc
        ))

        conn.commit()
        conn.close()

    def delete_item(self, item_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
        conn.commit()
        conn.close()

    def update_status(self, item_id, new_status):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET status = ? WHERE item_id = ?", (new_status, item_id))
        conn.commit()
        conn.close()

    def load_all_items(self):
        """
        Reads every row from the database and rebuilds it as a
        LostItem or FoundItem object (depending on item_type).
        Returns a list of objects ready to be handed to LostFoundSystem.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        conn.close()

        items = []
        for row in rows:
            (item_id, name, brand, color, location, date, description,
             item_type, status, reward, storage_loc) = row

            if item_type == "lost":
                obj = LostItem(
                    name, item_id, brand, color, location, date, description,
                    item_type, status, reward if reward is not None else 0
                )
            else:
                obj = FoundItem(
                    name, item_id, brand, color, location, date, description,
                    item_type, status, storage_loc if storage_loc is not None else ""
                )
            items.append(obj)

        return items
