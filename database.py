"""
Database initialization and operations
"""
import sqlite3
from config import DB


def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB)
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


def get_db_connection():
    """Get a database connection"""
    return sqlite3.connect(DB)

