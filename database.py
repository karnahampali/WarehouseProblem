import sqlite3
import json
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('warehouse.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    db.execute('DROP TABLE IF EXISTS layouts')
    db.execute('''
        CREATE TABLE layouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grid_data TEXT NOT NULL,
            start_pos TEXT NOT NULL,
            target_pos TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()