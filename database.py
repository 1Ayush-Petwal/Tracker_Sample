"""
Database initialization and operations
"""
import sqlite3
import os
from config import DB


def init_db():
    """Initialize the database with required tables"""
    try:
        # Ensure directory exists for database file
        db_path = DB
        if "/" in db_path or "\\" in db_path:
            db_dir = os.path.dirname(db_path)
            if db_dir:  # Only create if there's a directory component
                os.makedirs(db_dir, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Users table with savings_goal
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            savings_goal REAL DEFAULT 0
        )""")
        
        # Salary table
        c.execute("""CREATE TABLE IF NOT EXISTS salary(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            month INTEGER,
            year INTEGER,
            amount REAL
        )""")
        
        # Personal expense table
        c.execute("""CREATE TABLE IF NOT EXISTS personal(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            amount REAL,
            category TEXT,
            date TEXT DEFAULT (DATE('now'))
        )""")
        
        # Split expense table
        c.execute("""CREATE TABLE IF NOT EXISTS split(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            amount REAL,
            payer TEXT,
            participants TEXT,
            date TEXT DEFAULT (DATE('now'))
        )""")
        
        conn.commit()
        conn.close()
    except Exception as e:
        # Log error and re-raise for visibility
        import sys
        print(f"Error initializing database at {DB}: {e}", file=sys.stderr)
        if 'conn' in locals():
            conn.close()
        raise


def get_db_connection():
    """Get a database connection"""
    try:
        return sqlite3.connect(DB)
    except Exception as e:
        import sys
        print(f"Error connecting to database at {DB}: {e}", file=sys.stderr)
        raise

