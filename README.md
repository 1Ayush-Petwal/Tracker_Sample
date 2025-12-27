# Expense Tracker - Modular Structure

This application has been refactored into a modular structure for better maintainability and organization.

## Project Structure

```
sample-/
├── app.py                 # Main Flask application entry point
├── config.py              # Configuration constants
├── database.py            # Database initialization and connection utilities
├── utils.py               # Utility functions (password validation, auto-categorization)
├── templates.py           # All HTML template strings
├── routes/                 # Route handlers organized by feature
│   ├── __init__.py
│   ├── auth.py            # Authentication routes (login, logout, password reset)
│   ├── dashboard.py       # Dashboard routes (home, expenses, salary, goals)
│   ├── profile.py          # Profile routes (user profile, monthly details)
│   └── split.py            # Split expense routes
└── sample.py              # Original monolithic file (can be removed)
```

## Module Descriptions

### `app.py`
Main Flask application file that:
- Initializes the Flask app
- Sets up the secret key
- Initializes the database
- Registers all route blueprints

### `config.py`
Contains all configuration constants:
- Database filename
- Secret key
- Debug mode
- Host and port settings

### `database.py`
Database-related functions:
- `init_db()`: Creates all required database tables
- `get_db_connection()`: Returns a database connection

### `utils.py`
Utility functions:
- `is_strong_password()`: Validates password strength
- `auto_category()`: Automatically categorizes expenses based on title keywords

### `templates.py`
Contains all HTML template strings used throughout the application:
- BASE_HTML
- LOGIN_HTML
- FORGOT_HTML
- RESET_HTML
- SET_GOAL_HTML
- HOME_CONTENT
- MONTH_DETAIL_HTML
- SPLIT_HTML
- PROFILE_HTML

### `routes/auth.py`
Authentication-related routes:
- `/` - Login/Registration
- `/forgot` - Forgot password
- `/reset_password` - Reset password
- `/logout` - Logout

### `routes/dashboard.py`
Dashboard and expense management routes:
- `/home` - Main dashboard
- `/add_personal` - Add personal expense
- `/update_salary` - Update monthly salary
- `/delete_expense/<id>` - Delete expense
- `/enable_ai` - Enable AI advisor
- `/set_goal` - Set savings goal

### `routes/profile.py`
User profile routes:
- `/profile` - User profile with yearly statistics
- `/profile/month/<month>` - Monthly expense details

### `routes/split.py`
Split expense routes:
- `/split` - Split expenses page
- `/add_split` - Add split expense

## Running the Application

To run the application, use:

```bash
python app.py
```

The application will start on `http://0.0.0.0:5001` (or as configured in `config.py`).

## Benefits of Modular Structure

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Maintainability**: Easier to locate and modify specific functionality
3. **Scalability**: Simple to add new features by creating new route modules
4. **Testability**: Individual modules can be tested in isolation
5. **Code Reusability**: Utility functions and database operations can be reused across modules
6. **Team Collaboration**: Multiple developers can work on different modules simultaneously
