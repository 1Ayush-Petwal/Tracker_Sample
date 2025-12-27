"""
Main Flask application file
"""
from flask import Flask
from config import SECRET_KEY, DEBUG, HOST, PORT
from database import init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.profile import profile_bp
from routes.split import split_bp

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize database
try:
    init_db()
except Exception as e:
    import sys
    print(f"Failed to initialize database: {e}", file=sys.stderr)
    # In production, we want to fail fast if DB can't be initialized
    if not DEBUG:
        raise

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(split_bp)

@app.route("/")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)

