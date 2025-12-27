"""
Utility functions
"""
import re


def is_strong_password(pw):
    """Check if password meets strength requirements"""
    return (
        len(pw) >= 8 and
        re.search(r"[A-Z]", pw) and
        re.search(r"[a-z]", pw) and
        re.search(r"[0-9]", pw) and
        re.search(r"[!@#$%^&*]", pw)
    )


def auto_category(title):
    """Automatically categorize expense based on title keywords"""
    SMART_CATEGORIES = {
        "Food": ["swiggy", "zomato", "restaurant", "pizza", "burger"],
        "Travel": ["uber", "ola", "bus", "metro", "flight", "cab"],
        "Entertainment": ["netflix", "prime", "movie", "spotify", "game"],
        "Shopping": ["amazon", "flipkart", "mall", "store"]
    }
    t = title.lower()
    for cat, keywords in SMART_CATEGORIES.items():
        if any(k in t for k in keywords):
            return cat
    return "Others"

