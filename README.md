# Lost & Found Search System

A desktop application for registering, searching and managing lost and found items, built with object-oriented Python.

## Features
- Add lost items (with optional reward) or found items (with storage location)
- Live search by item name
- Mark items as active or resolved, or delete them
- Data saved between runs with SQLite

## Project Structure
- `models.py`: OOP classes (`Item`, `LostItem`, `FoundItem`, `LostFoundSystem`)
- `database.py`: SQLite persistence
- `gui.py`: Tkinter interface
- `main.py`: entry point

## OOP Concepts
Encapsulation, inheritance and polymorphism.

## How to Run
```bash
python main.py
```
Uses only the Python standard library (Tkinter and sqlite3), so no installation is needed.

## Author
Abanoub Rezk Gad: [LinkedIn](https://linkedin.com/in/abanoub-rezk)
