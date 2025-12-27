"""
Split expense routes
"""
from flask import Blueprint, request, redirect, render_template_string, session
from collections import defaultdict
from database import get_db_connection
from templates import SPLIT_HTML

split_bp = Blueprint('split', __name__)


@split_bp.route("/split")
def split():
    """Display split expenses page"""
    if "uid" not in session:
        return redirect("/")
    
    uid = session["uid"]
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT title,amount,payer,participants FROM split WHERE user_id=?", (uid,))
    rows = c.fetchall()
    net_balance = defaultdict(float)
    
    for title, amt, payer, parts in rows:
        people = [p.strip() for p in parts.split(",")]
        share = amt / len(people)
        for p in people:
            if p != payer:
                net_balance[p] -= share
                net_balance[payer] += share
    
    conn.close()
    net_balance = dict(net_balance)
    return render_template_string(SPLIT_HTML, net_balance=net_balance)


@split_bp.route("/add_split", methods=["POST"])
def add_split():
    """Add a split expense"""
    if "uid" not in session:
        return redirect("/")
    
    uid = session["uid"]
    title = request.form["title"]
    amount = float(request.form["amount"])
    payer = request.form["payer"]
    participants = request.form["participants"]
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO split(user_id,title,amount,payer,participants) VALUES(?,?,?,?,?)",
            (uid, title, amount, payer, participants))
    
    people = [p.strip() for p in participants.split(",")]
    share = amount / len(people)
    # Add split portion to personal expenses
    c.execute("INSERT INTO personal(user_id,title,amount,category) VALUES(?,?,?,?)",
            (uid, f"{title} (Split Paid)", share, "Split"))
    
    conn.commit()
    conn.close()
    return redirect("/split")

