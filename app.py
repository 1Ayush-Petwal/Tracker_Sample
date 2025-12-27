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
init_db()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(split_bp)

if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)

