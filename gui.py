"""
gui.py
------
Tkinter GUI for the Lost & Found Search System.

This file only handles the visual side (windows, buttons, forms).
All the real logic (adding, searching, deleting, updating) is delegated
to LostFoundSystem (models.py) and Database (database.py) — nothing here
duplicates that logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import uuid
import datetime

from models import LostItem, FoundItem
from database import Database


class LostFoundGUI:
    def __init__(self, root, system, db):
        self.root = root
        self.system = system   # LostFoundSystem instance (in-memory logic)
        self.db = db           # Database instance (persistence)

        self.root.title("Lost & Found Search System")
        self.root.geometry("880x600")

        self._build_form_section()
        self._build_search_section()
        self._build_results_section()

        self.refresh_results(self.system.search(""))  # show everything at start

    # ---------------------------------------------------------------
    # FORM: Add a new lost/found item
    # ---------------------------------------------------------------
    def _build_form_section(self):
        frame = ttk.LabelFrame(self.root, text="Add New Item")
        frame.pack(fill="x", padx=10, pady=10)

        labels = ["Name", "Brand", "Color", "Location", "Date (YYYY-MM-DD)", "Description"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i // 3, column=(i % 3) * 2, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(frame, width=25)
            entry.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=5, pady=5)
            self.entries[label] = entry

        # Item type: lost or found
        ttk.Label(frame, text="Type").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.type_var = tk.StringVar(value="lost")
        type_menu = ttk.Combobox(frame, textvariable=self.type_var, values=["lost", "found"], width=22, state="readonly")
        type_menu.grid(row=2, column=1, padx=5, pady=5)
        type_menu.bind("<<ComboboxSelected>>", self._toggle_extra_field)

        # Extra field: reward (lost) or storage_loc (found)
        self.extra_label = ttk.Label(frame, text="Reward")
        self.extra_label.grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.extra_entry = ttk.Entry(frame, width=25)
        self.extra_entry.grid(row=2, column=3, padx=5, pady=5)

        add_btn = ttk.Button(frame, text="Add Item", command=self.handle_add_item)
        add_btn.grid(row=3, column=0, columnspan=4, pady=10)

    def _toggle_extra_field(self, event=None):
        if self.type_var.get() == "lost":
            self.extra_label.config(text="Reward")
        else:
            self.extra_label.config(text="Storage Location")
        self.extra_entry.delete(0, tk.END)

    def handle_add_item(self):
        try:
            name = self.entries["Name"].get()
            brand = self.entries["Brand"].get()
            color = self.entries["Color"].get()
            location = self.entries["Location"].get()
            date = self.entries["Date (YYYY-MM-DD)"].get()
            description = self.entries["Description"].get()
            item_type = self.type_var.get()
            item_id = str(uuid.uuid4())[:8]   # short unique id, auto-generated
            status = "active"

            if item_type == "lost":
                reward_text = self.extra_entry.get()
                reward = float(reward_text) if reward_text else 0
                item = LostItem(name, item_id, brand, color, location, date,
                                 description, item_type, status, reward)
            else:
                storage_loc = self.extra_entry.get()
                item = FoundItem(name, item_id, brand, color, location, date,
                                  description, item_type, status, storage_loc)

            self.system.add_item(item)
            self.db.insert_item(item)

            messagebox.showinfo("Success", f"Item added with ID: {item_id}")
            self._clear_form()
            self.refresh_results(self.system.search(""))

        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please check that every field is filled in correctly.")

    def _clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.extra_entry.delete(0, tk.END)

    # ---------------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------------
    def _build_search_section(self):
        frame = ttk.LabelFrame(self.root, text="Search")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Item name (partial match):").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.handle_search)

        ttk.Button(frame, text="Show All", command=self.handle_show_all).pack(side="left", padx=5)

    def handle_search(self, event=None):
        term = self.search_entry.get()
        results = self.system.search(term)
        self.refresh_results(results)

    def handle_show_all(self):
        self.search_entry.delete(0, tk.END)
        self.refresh_results(self.system.search(""))

    # ---------------------------------------------------------------
    # RESULTS TABLE + actions (delete / update status)
    # ---------------------------------------------------------------
    def _build_results_section(self):
        frame = ttk.LabelFrame(self.root, text="Items")
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "name", "brand", "color", "location", "date", "type", "status", "extra")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        headings = {
            "id": "ID", "name": "Name", "brand": "Brand", "color": "Color",
            "location": "Location", "date": "Date", "type": "Type",
            "status": "Status", "extra": "Reward / Storage"
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=90)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        action_frame = ttk.Frame(frame)
        action_frame.pack(fill="x", pady=5)

        ttk.Button(action_frame, text="Mark Resolved", command=self.handle_mark_resolved).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Mark Active", command=self.handle_mark_active).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self.handle_delete).pack(side="left", padx=5)

    def refresh_results(self, items):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in items:
            info = item.display_info()
            extra = info.get("reward", info.get("storage_loc", ""))
            self.tree.insert("", "end", values=(
                info["Item ID"], info["Name"], info["Brand"], info["Color"],
                info["Location"], info["Date"], info["Type"], info["Status"], extra
            ))

    def _get_selected_item_id(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item from the list first.")
            return None
        values = self.tree.item(selection[0], "values")
        return values[0]  # the "id" column

    def handle_delete(self):
        item_id = self._get_selected_item_id()
        if item_id is None:
            return
        self.system.remove_item(item_id)
        self.db.delete_item(item_id)
        self.refresh_results(self.system.search(""))

    def handle_mark_resolved(self):
        self._update_selected_status("resolved")

    def handle_mark_active(self):
        self._update_selected_status("active")

    def _update_selected_status(self, new_status):
        item_id = self._get_selected_item_id()
        if item_id is None:
            return
        self.system.update_status(item_id, new_status)
        self.db.update_status(item_id, new_status)
        self.refresh_results(self.system.search(""))
