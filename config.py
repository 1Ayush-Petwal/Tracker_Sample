"""
Configuration file for the Expense Tracker application
"""
import os

# Database configuration - use DB_PATH to avoid conflict with Railway's DATABASE_URL
# In production (Railway/Heroku), prefer /tmp for writable storage
# Railway provides PORT env var, so we can detect production environment
if os.getenv("PORT") and not os.getenv("DB_PATH"):
    # Production environment detected - use /tmp for database
    default_db_path = os.path.join("/tmp", "expenses.db")
else:
    # Development - use current directory
    default_db_path = os.path.join(os.getcwd(), "expenses.db")

DB = os.getenv("DB_PATH", default_db_path)

# Secret key - use environment variable in production
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

# Debug mode - disabled in production
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Host and Port - Railway provides PORT environment variable
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5001))

# DB = "expenses.db"
# SECRET_KEY = "supersecretkey"
# DEBUG = True
# HOST = "0.0.0.0"
# PORT = 5001