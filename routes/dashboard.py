"""
Dashboard routes (home, expenses, salary, goals, AI)
"""
from flask import Blueprint, request, redirect, render_template_string, session
import datetime
from collections import defaultdict
from database import get_db_connection
from utils import auto_category
from templates import BASE_HTML, HOME_CONTENT, SET_GOAL_HTML

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/home")
def home():
    """Display the home dashboard"""
    if "uid" not in session:
        return redirect("/")
    
    uid = session["uid"]
    now = datetime.datetime.now()
    month, current_year = now.month, now.year
    conn = get_db_connection()
    c = conn.cursor()

    # Salary
    c.execute("SELECT amount FROM salary WHERE user_id=? AND month=? AND year=?", 
              (uid, month, current_year))
    salary = c.fetchone()
    salary = salary[0] if salary else 0

    # Expenses
    c.execute("""
    SELECT id,title,amount,category
    FROM personal
    WHERE user_id=?
    AND strftime('%m',date)=?
    AND strftime('%Y',date)=?
    """, (uid, f"{month:02d}", str(current_year)))

    personal = [{'id': r[0], 'title': r[1], 'amount': r[2], 'category': r[3]} 
                for r in c.fetchall()]
    spent = sum(r['amount'] for r in personal)
    savings = salary - spent
    budget_warning = None
    
    if salary > 0:
        used_percent = (spent / salary) * 100
        if used_percent >= 80:
            budget_warning = f"⚠ You have used {int(used_percent)}% of your salary!"

    # Savings goal
    c.execute("SELECT savings_goal FROM users WHERE id=?", (uid,))
    row = c.fetchone()
    goal = row[0] if row and row[0] else 0

    # Category totals
    cat = defaultdict(float)
    for r in personal:
        cat[r['category']] += r['amount']

    # AI advice
    ai_advice = []
    ai_warning = False

    if salary > 0:
        for k, v in cat.items():
            limit = 0.2 * salary if k != "Split" else 0.1 * salary
            if v > limit:
                ai_advice.append(f"⚠ Warning! Your {k} spending is too high. You spent ₹{int(v)}.")
                ai_warning = True
            else:
                ai_advice.append(f"✅ {k} spending is under control.")

        if savings < goal:
            ai_advice.append(f"⚠ You are below your savings goal by ₹{int(goal - savings)}.")
            ai_warning = True
        else:
            ai_advice.append("✅ You are on track to meet your savings goal.")

    conn.close()
    
    return render_template_string(
        BASE_HTML,
        title="Dashboard",
        content=render_template_string(
            HOME_CONTENT,
            salary=salary,
            spent=spent,
            savings=savings,
            goal=goal,
            labels=list(cat.keys()),
            values=list(cat.values()),
            ai_advice=ai_advice,
            ai_warning=ai_warning,
            budget_warning=budget_warning
        )
    )


@dashboard_bp.route("/add_personal", methods=["POST"])
def add_personal():
    """Add a personal expense"""
    if "uid" not in session:
        return redirect("/")
    
    uid = session["uid"]
    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form.get("category") or auto_category(title)
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO personal(user_id,title,amount,category) VALUES(?,?,?,?)",
              (uid, title, amount, category))
    conn.commit()
    conn.close()
    return redirect("/home")


@dashboard_bp.route("/update_salary", methods=["POST"])
def update_salary():
    """Update monthly salary"""
    if "uid" not in session:
        return redirect("/")
    
    uid = session["uid"]
    amount = float(request.form["salary"])
    month = int(request.form["month"])
    year = datetime.datetime.now().year
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM salary WHERE user_id=? AND month=? AND year=?", 
              (uid, month, year))
    exists = c.fetchone()
    
    if exists:
        c.execute("UPDATE salary SET amount=? WHERE id=?", (amount, exists[0]))
    else:
        c.execute("INSERT INTO salary(user_id,month,year,amount) VALUES(?,?,?,?)", 
                  (uid, month, year, amount))
    
    conn.commit()
    conn.close()
    return redirect("/home")


@dashboard_bp.route("/delete_expense/<int:id>")
def delete_expense(id):
    """Delete a personal expense"""
    if "uid" not in session:
        return redirect("/")
    
    uid = session["uid"]
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM personal WHERE id=? AND user_id=?", (id, uid))
    conn.commit()
    conn.close()
    return redirect("/home")


@dashboard_bp.route("/enable_ai", methods=["POST"])
def enable_ai():
    """Enable AI advisor"""
    if "uid" not in session:
        return redirect("/")
    session["ai_enabled"] = True
    return redirect("/home")


@dashboard_bp.route("/set_goal", methods=["GET", "POST"])
def set_goal():
    """Set or update savings goal"""
    if "uid" not in session:
        return redirect("/")
    
    uid = session["uid"]
    conn = get_db_connection()
    c = conn.cursor()
    
    if request.method == "POST":
        goal = float(request.form["goal"])
        c.execute("UPDATE users SET savings_goal=? WHERE id=?", (goal, uid))
        conn.commit()
        conn.close()
        return redirect("/home")
    
    c.execute("SELECT savings_goal FROM users WHERE id=?", (uid,))
    row = c.fetchone()
    goal = row[0] if row else 0
    conn.close()
    return render_template_string(SET_GOAL_HTML, goal=goal)

