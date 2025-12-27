"""
Profile routes (user profile, monthly details)
"""
from flask import Blueprint, request, redirect, render_template_string, session
import datetime
from database import get_db_connection
from templates import PROFILE_HTML, MONTH_DETAIL_HTML

profile_bp = Blueprint('profile', __name__)


@profile_bp.route("/profile")
def profile():
    """Display user profile with yearly statistics"""
    if "uid" not in session:
        return redirect("/")

    uid = session["uid"]
    now = datetime.datetime.now()
    current_year = now.year

    conn = get_db_connection()
    c = conn.cursor()

    # User info
    c.execute("SELECT username,email FROM users WHERE id=?", (uid,))
    username, email = c.fetchone()

    # Salary data
    c.execute("SELECT month,amount FROM salary WHERE user_id=? AND year=?", 
              (uid, current_year))
    salary_data = c.fetchall()
    salary_dict = {m: 0 for m in range(1, 13)}
    for m, a in salary_data:
        salary_dict[m] = a

    # Expense data
    c.execute("""
        SELECT strftime('%m',date), SUM(amount)
        FROM personal
        WHERE user_id=? AND strftime('%Y',date)=?
        GROUP BY strftime('%m',date)
    """, (uid, str(current_year)))

    expense_data = c.fetchall()
    expense_dict = {m: 0 for m in range(1, 13)}
    for m, a in expense_data:
        expense_dict[int(m)] = a

    conn.close()

    months = [datetime.date(1900, m, 1).strftime('%b') for m in range(1, 13)]
    expenses = [expense_dict[m] for m in range(1, 13)]
    salary = [salary_dict[m] for m in range(1, 13)]

    yearly_savings = sum(salary) - sum(expenses)

    return render_template_string(
        PROFILE_HTML,
        username=username,
        email=email,
        current_year=current_year,
        months=months,
        expenses=expenses,
        salary=salary,
        yearly_savings=yearly_savings
    )


@profile_bp.route("/profile/month/<int:month>")
def month_details(month):
    """Display detailed expenses for a specific month"""
    if "uid" not in session:
        return redirect("/")

    uid = session["uid"]
    year = datetime.datetime.now().year

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
        SELECT date,title,category,amount
        FROM personal
        WHERE user_id=?
        AND strftime('%m',date)=?
        AND strftime('%Y',date)=?
        ORDER BY date
    """, (uid, f"{month:02d}", str(year)))

    rows = c.fetchall()
    conn.close()

    expenses = [{
        "date": r[0],
        "title": r[1],
        "category": r[2],
        "amount": r[3]
    } for r in rows]

    month_name = datetime.date(1900, month, 1).strftime('%B')

    return render_template_string(
        MONTH_DETAIL_HTML,
        expenses=expenses,
        month_name=month_name,
        year=year
    )

