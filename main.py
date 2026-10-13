"""
main.py
-------
Entry point for the Lost & Found Search System.

Run this file to start the application:
    python main.py

What happens on startup:
    1. Connect to (or create) the SQLite database file "lost_found.db".
    2. Load any items that were saved from previous runs into LostFoundSystem.
    3. Launch the Tkinter GUI on top of that system.
"""

import tkinter as tk

from models import LostFoundSystem
from database import Database
from gui import LostFoundGUI


def main():
    db = Database("lost_found.db")
    system = LostFoundSystem()

    # Load previously saved items back into memory so nothing is lost
    # between runs of the program.
    for item in db.load_all_items():
        system.add_item(item)

    root = tk.Tk()
    app = LostFoundGUI(root, system, db)
    root.mainloop()


if __name__ == "__main__":
    main()
