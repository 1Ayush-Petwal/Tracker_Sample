"""
Configuration file for the Expense Tracker application
"""
import os

# Database configuration
DB = os.getenv("DATABASE_URL", "expenses.db")

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