"""
Authentication routes (login, logout, forgot password, reset password)
"""
from flask import Blueprint, request, redirect, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from utils import is_strong_password
from templates import LOGIN_HTML, FORGOT_HTML, RESET_HTML

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    """Handle user login and registration"""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id,password FROM users WHERE email=?", (email,))
        user = c.fetchone()

        if user:
            if check_password_hash(user[1], password):
                session["uid"] = user[0]
                conn.close()
                return redirect("/home")
            else:
                conn.close()
                return "Invalid password"
        else:
            if not is_strong_password(password):
                conn.close()
                return "Password not strong enough"
            hashed = generate_password_hash(password)
            c.execute("INSERT INTO users(username,email,password) VALUES(?,?,?)",
                      (username, email, hashed))
            session["uid"] = c.lastrowid
            conn.commit()
            conn.close()
            return redirect("/home")
    return render_template_string(LOGIN_HTML)


@auth_bp.route("/forgot", methods=["GET", "POST"])
def forgot():
    """Handle forgot password request"""
    if request.method == "POST":
        email = request.form["email"]
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()
        if user:
            session["reset_uid"] = user[0]
            return redirect("/reset_password")
        return "Email not registered"
    return render_template_string(FORGOT_HTML)


@auth_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    """Handle password reset"""
    if "reset_uid" not in session:
        return redirect("/")
    if request.method == "POST":
        pw = request.form["password"]
        if not is_strong_password(pw):
            return "Weak password"
        hashed = generate_password_hash(pw)
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET password=? WHERE id=?",
                  (hashed, session["reset_uid"]))
        conn.commit()
        conn.close()
        session.pop("reset_uid")
        return redirect("/")
    return render_template_string(RESET_HTML)


@auth_bp.route("/logout")
def logout():
    """Handle user logout"""
    session.clear()
    return redirect("/")

