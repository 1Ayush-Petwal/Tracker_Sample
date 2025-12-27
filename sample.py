from flask import Flask, request, redirect, render_template_string, session
import sqlite3, datetime, re
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB = "expenses.db"

BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{ title }}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
:root{
  --bg:#0f1221;
  --card:#1b1f3b;
  --accent:#7c3aed;
  --accent-light:#a78bfa;
  --text:#ffffff;
  --muted:#b6b6d6;
  --danger:#ef4444;
  --success:#22c55e;
}

*{box-sizing:border-box}
body{
  margin:0;
  font-family:'Inter',sans-serif;
  background:linear-gradient(135deg,#0f1221,#1b1f3b);
  color:var(--text);
}

/* NAVBAR */
.nav{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:18px 30px;
  background:rgba(255,255,255,0.05);
  backdrop-filter:blur(12px);
}
.nav h2{margin:0;font-weight:600}
.nav a{
  color:white;
  text-decoration:none;
  margin-left:15px;
  padding:8px 14px;
  border-radius:10px;
  background:var(--accent);
  font-size:14px;
}
.nav a:hover{background:var(--accent-light)}

/* LAYOUT */
.container{
  max-width:1200px;
  margin:auto;
  padding:30px;
}

/* CARDS */
.card{
  background:rgba(255,255,255,0.08);
  border-radius:18px;
  padding:22px;
  box-shadow:0 20px 40px rgba(0,0,0,.25);
  margin-bottom:20px;
}

/* GRID */
.grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
  gap:20px;
}

/* STATS */
.stat h3{color:var(--muted);margin-bottom:5px}
.stat h2{color:var(--accent-light);margin:0}

/* FORMS */
input,select,button{
  width:100%;
  padding:12px;
  border-radius:12px;
  border:none;
  margin-top:10px;
  font-size:15px;
  box-sizing:border-box; 
  
}
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  appearance: textfield;
}

input,select{
  background:#11142b;
  color:white;
}
button{
  background:var(--accent);
  color:white;
  font-weight:600;
  cursor:pointer;
}
button:hover{background:var(--accent-light)}

/* TABLE */
table{
  width:100%;
  border-collapse:collapse;
}
th,td{
  padding:12px;
  border-bottom:1px solid rgba(255,255,255,.1);
  text-align:center;
}
th{color:var(--accent-light)}

.warning{
  background:var(--danger);
  padding:14px;
  border-radius:12px;
  text-align:center;
  font-weight:600;
}
</style>
</head>

<body>

<div class="nav">
  <h2>💰 Expense Tracker</h2>
  <div>
    <a href="/home">Dashboard</a>
    <a href="/profile">Profile</a>
    <a href="/split">Split</a>
    <a href="/logout">Logout</a>
  </div>
</div>

<div class="container">
{{ content|safe }}
</div>

</body>
</html>
"""

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # Users table with savings_goal
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        savings_goal REAL DEFAULT 0
    )""")
    # Salary table
    c.execute("""CREATE TABLE IF NOT EXISTS salary(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        month INTEGER,
        year INTEGER,
        amount REAL
    )""")
    # Personal expense table
    c.execute("""CREATE TABLE IF NOT EXISTS personal(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        amount REAL,
        category TEXT,
        date TEXT DEFAULT (DATE('now'))
    )""")
    # Split expense table
    c.execute("""CREATE TABLE IF NOT EXISTS split(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        amount REAL,
        payer TEXT,
        participants TEXT,
        date TEXT DEFAULT (DATE('now'))
    )""")
    conn.commit()
    conn.close()
init_db()

# ---------- UTIL ----------
def is_strong_password(pw):
    return (
        len(pw) >= 8 and
        re.search(r"[A-Z]", pw) and
        re.search(r"[a-z]", pw) and
        re.search(r"[0-9]", pw) and
        re.search(r"[!@#$%^&*]", pw)
    )

def auto_category(title):
    SMART_CATEGORIES = {
        "Food": ["swiggy","zomato","restaurant","pizza","burger"],
        "Travel": ["uber","ola","bus","metro","flight","cab"],
        "Entertainment": ["netflix","prime","movie","spotify","game"],
        "Shopping": ["amazon","flipkart","mall","store"]
    }
    t = title.lower()
    for cat, keywords in SMART_CATEGORIES.items():
        if any(k in t for k in keywords):
            return cat
    return "Others"

# ---------- LOGIN ----------
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Login</title>
<style>
body{margin:0;height:100vh;display:flex;justify-content:center;align-items:center;
background:linear-gradient(135deg,#141e30,#243b55);font-family:'Segoe UI'}
.card{background:rgba(255,255,255,.15);padding:40px;width:360px;border-radius:20px;color:white}
input,button{width:100%;padding:12px;margin:10px 0;border-radius:10px;border:none}
button{background:#ff6a00;color:white;font-weight:bold}
a{color:#ffb347;text-decoration:none;font-size:14px}
</style>
<script>
function togglePassword(){
  const p = document.getElementById("password");
  p.type = p.type === "password" ? "text" : "password";
}
</script>
</head>
<body>
<div class="card">
<h2 align="center">Expense Tracker</h2>
<form method="post">
<input name="username" placeholder="Username" required>
<input name="email" type="email" placeholder="Email" required>
<input id="password" name="password" type="password" placeholder="Password" required>
<div style="text-align:left;font-size:14px;margin-top:-5px">
  <input type="checkbox" onclick="togglePassword()"> Show Password
</div>
<button>Login / Register</button>
</form>
<p align="right"><a href="/forgot">Forgot Password?</a></p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT id,password FROM users WHERE email=?", (email,))
        user = c.fetchone()

        if user:
            if check_password_hash(user[1], password):
                session["uid"] = user[0]
                return redirect("/home")
            else:
                return "Invalid password"
        else:
            if not is_strong_password(password):
                return "Password not strong enough"
            hashed = generate_password_hash(password)
            c.execute("INSERT INTO users(username,email,password) VALUES(?,?,?)",
                      (username,email,hashed))
            session["uid"] = c.lastrowid
            conn.commit()
            return redirect("/home")
    return render_template_string(LOGIN_HTML)

# ---------- FORGOT PASSWORD ----------
FORGOT_HTML = """
<!DOCTYPE html>
<html>
<head><title>Forgot Password</title></head>
<body style="background:#141e30;color:white;font-family:Segoe UI;text-align:center">
<h2>Reset Password</h2>
<form method="post">
<input name="email" placeholder="Registered Email" required>
<button>Verify</button>
</form>
</body>
</html>
"""

@app.route("/forgot", methods=["GET","POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()
        if user:
            session["reset_uid"] = user[0]
            return redirect("/reset_password")
        return "Email not registered"
    return render_template_string(FORGOT_HTML)

# ---------- RESET PASSWORD ----------
RESET_HTML = """
<!DOCTYPE html>
<html>
<head><title>Set New Password</title></head>
<body style="background:#141e30;color:white;font-family:Segoe UI;text-align:center">
<h2>Set New Password</h2>
<form method="post">
<input name="password" type="password" placeholder="New Password" required>
<button>Update Password</button>
</form>
</body>
</html>
"""

@app.route("/reset_password", methods=["GET","POST"])
def reset_password():
    if "reset_uid" not in session:
        return redirect("/")
    if request.method == "POST":
        pw = request.form["password"]
        if not is_strong_password(pw):
            return "Weak password"
        hashed = generate_password_hash(pw)
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("UPDATE users SET password=? WHERE id=?",
                  (hashed, session["reset_uid"]))
        conn.commit()
        conn.close()
        session.pop("reset_uid")
        return redirect("/")
    return render_template_string(RESET_HTML)

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- ENABLE AI ----------
@app.route("/enable_ai", methods=["POST"])
def enable_ai():
    if "uid" not in session: return redirect("/")
    session["ai_enabled"] = True
    return redirect("/home")

# ---------- SET SAVINGS GOAL ----------
SET_GOAL_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Set Savings Goal</title>
<style>
body{background:#141e30;color:white;font-family:'Segoe UI';text-align:center;padding-top:50px}
input,button{padding:12px;margin:10px;border-radius:10px;border:none;width:200px}
button{background:#8e2de2;color:white;font-weight:bold;cursor:pointer}
button:hover{background:#6a11cb}
.rupee-box { position: relative; }
.rupee-box span {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #aaa;
  font-weight: bold;
}
.rupee-input { padding-left: 28px; }
</style>
</head>
<body>
<h2>Set Your Monthly Savings Goal</h2>
<form method="post">
<div class="rupee-box">
  <span>₹</span>
  <input type="number" name="goal" class="rupee-input"
         placeholder="Monthly Savings Goal" value="{{goal}}" required>
</div>
<br>
<button>Update Goal</button>
</form>
<a href="/home">⬅ Back to Dashboard</a>
</body>
</html>
"""

@app.route("/set_goal", methods=["GET","POST"])
def set_goal():
    if "uid" not in session: return redirect("/")
    uid = session["uid"]
    conn = sqlite3.connect(DB)
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

# ---------- HOME DASHBOARD ----------
HOME_HTML = """<!DOCTYPE html>
<html>
<head>
<title>Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{margin:0;font-family:'Segoe UI';background:#1a1a1a;color:white}
.nav{background:#6a11cb;color:white;padding:16px;display:flex;justify-content:space-between;align-items:center}
.nav a{color:white;text-decoration:none;font-size:16px;padding:6px 12px;background:#8e2de2;border-radius:8px}
.container{max-width:1100px;margin:auto;padding:20px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.stat{background:#2b2b2b;padding:20px;border-radius:18px;text-align:center;box-shadow:0 10px 25px rgba(0,0,0,.1)}
.stat h2{margin:5px 0;color:#8e2de2}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:25px}
.card{background:#2b2b2b;padding:22px;border-radius:18px;box-shadow:0 10px 25px rgba(0,0,0,.1)}
input,button,select{width:100%;padding:10px;margin:8px 0;border-radius:10px;border:1px solid #ccc}
button{background:#8e2de2;color:white;font-weight:bold;border:none;cursor:pointer}
button:hover{background:#6a11cb}
.center{text-align:center}
table{width:100%;border-collapse: collapse;margin-top:15px;color:white}
th, td{border:1px solid #ccc;padding:8px;text-align:center}
th{background:#6a11cb;color:white}
tr:nth-child(even){background:#2b2b2b}
a{color:#ffb347;text-decoration:underline;font-size:14px}

/* ===== RUPEE INPUT STYLE ===== */
.rupee-box {
  position: relative;
}

.rupee-box span {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #aaa;
  font-weight: bold;
}

.rupee-input {
  padding-left: 28px;
}

</style>
</head>
<body>
<div class="nav"><span>Dashboard</span>
<a href="/split">Splitwise ➗</a><a href="/profile">Profile 👤</a><a href="/logout">Logout</a></div>
<div class="container">
<div class="card">
<h3>Monthly Salary</h3>
<form method="post" action="/update_salary">
<div class="rupee-box">
  <span>₹</span>
  <input name="salary" type="number" class="rupee-input"
         placeholder="Monthly Salary" value="{{salary}}" required>
</div>
<select name="month">{% for m in range(1,13) %}
<option value="{{m}}" {% if m==current_month %}selected{% endif %}>{{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1]}}</option>
{% endfor %}</select>
<button>Update</button>
</form>
</div>

{% if budget_warning %}
<div style="
    background:#ff4d4d;
    color:white;
    padding:12px;
    border-radius:10px;
    text-align:center;
    margin-bottom:15px;
    font-weight:bold;">
  {{ budget_warning }}
</div>
{% endif %}

<div class="stats">
<div class="stat"><h3>Salary</h3><h2>₹{{salary}}</h2></div>
<div class="stat"><h3>Expenses</h3><h2>₹{{ "%.2f"|format(spent) }}
</h2></div>
<div class="stat"><h3>Savings</h3><h2>₹{{ "%.2f"|format(savings) }}</h2></div>
<div class="stat"><h3>Goal</h3><h2>₹{{goal}}</h2>
<p><a href="/set_goal">Set/Update Goal</a></p>
</div>
</div>

<div class="card">
<form method="post" action="/enable_ai">
<button>Enable AI Advisor 🤖</button>
</form>
</div>

<div class="grid">
<div class="card">
<h3>Add Personal Expense</h3>
<form method="post" action="/add_personal">
<input name="title" placeholder="Title" required>
<div class="rupee-box">
  <span>₹</span>
  <input name="amount" type="number" class="rupee-input"
         placeholder="Expense Amount" required>
</div>
<input name="category" placeholder="Category / Leave blank for auto">
<button>Add Expense</button>
</form>
</div>

<div class="card center">
<h3>Expense Distribution</h3>
<canvas id="pie" width="180" height="180"></canvas>
<table><tr><th>Title</th><th>Amount</th><th>Category</th><th>Delete</th></tr>
{% for r in personal %}
<tr><td>{{r.title}}</td><td>₹{{r.amount}}</td><td>{{r.category}}</td>
<td><a href="/delete_expense/{{r.id}}">Delete</a></td></tr>
{% endfor %}
</table>

{% if ai_advice %}
<h3>AI Advisor</h3>
<ul id="aiList">
{% for adv in ai_advice %}
<li>{{adv}}</li>
{% endfor %}
</ul>
<button onclick="speakAI()">🔊 Speak Advice</button>
<script>
function speakAI(){
    const msg = new SpeechSynthesisUtterance();
    let text = "";
    document.querySelectorAll("#aiList li").forEach(li => text += li.innerText + ". ");
    msg.text = text;
    window.speechSynthesis.speak(msg);
}
</script>
{% endif %}
</div>
</div>
</div>

<script>
const colors = {{labels|safe}}.map(_ => '#' + Math.floor(Math.random()*16777215).toString(16));
new Chart(document.getElementById("pie"),{type:"pie",
data:{labels:{{labels|safe}},datasets:[{data:{{values|safe}},backgroundColor:colors}]},
options:{responsive:false,plugins:{legend:{position:'bottom'}}}});
</script>
</body></html>
"""
HOME_CONTENT = """
<div class="card">
  <h3>Set Monthly Salary</h3>
  <form method="post" action="/update_salary">
    <input type="number" name="salary" placeholder="Enter your monthly salary" required>

    <select name="month">
      <option value="1">Jan</option>
      <option value="2">Feb</option>
      <option value="3">Mar</option>
      <option value="4">Apr</option>
      <option value="5">May</option>
      <option value="6">Jun</option>
      <option value="7">Jul</option>
      <option value="8">Aug</option>
      <option value="9">Sep</option>
      <option value="10">Oct</option>
      <option value="11">Nov</option>
      <option value="12">Dec</option>
    </select>

    <button>Save Salary</button>
  </form>
</div>

<div class="grid">
  <div class="card stat">
    <h3>Salary</h3>
    <h2>₹{{salary}}</h2>
  </div>

  <div class="card stat">
    <h3>Expenses</h3>
    <h2>₹{{ "%.2f"|format(spent) }}</h2>
  </div>

  <div class="card stat">
    <h3>Savings</h3>
    <h2>₹{{ "%.2f"|format(savings) }}</h2>
  </div>

  <div class="card stat">
    <h3>Goal</h3>
    <h2>₹{{goal}}</h2>
    <a href="/set_goal">Update Goal</a>
  </div>
</div>

{% if budget_warning %}
<div class="warning">{{ budget_warning }}</div>
{% endif %}

<div class="grid">
  <div class="card">
    <h3>Add Expense</h3>
    <form method="post" action="/add_personal">
      <input name="title" placeholder="Expense title" required>
      <input type="number" name="amount" placeholder="Amount" required>
      <input name="category" placeholder="Category (optional)">
      <button>Add Expense</button>
    </form>
  </div>

  <div class="card">
    <h3>Expense Breakdown</h3>
    <canvas id="pie"></canvas>
  </div>
</div>

{% if ai_advice %}
<div class="card">
<h3>🤖 AI Advisor</h3>

<ul id="aiList">
{% for adv in ai_advice %}
<li>{{adv}}</li>
{% endfor %}
</ul>

<button onclick="speakAI()">🔊 Speak Advice</button>

<script>
function speakAI(){
    let text = "";
    document.querySelectorAll("#aiList li").forEach(li => {
        text += li.innerText + ". ";
    });

    if(text.trim() !== ""){
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = "en-IN";
        msg.rate = 1;
        msg.pitch = 1;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    }
}

// 🔥 AUTO SPEAK WHEN WARNING EXISTS
{% if ai_warning %}
window.onload = function(){
    setTimeout(speakAI, 800);
};
{% endif %}
</script>
</div>
{% endif %}


<script>
new Chart(document.getElementById("pie"),{
  type:"doughnut",
  data:{
    labels:{{labels|safe}},
    datasets:[{data:{{values|safe}}}]
  }
});
</script>
"""

# ---------- HOME ----------

@app.route("/home")
def home():

    if "uid" not in session: return redirect("/")
    uid = session["uid"]
    now = datetime.datetime.now()
    month, current_year = now.month, now.year
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Salary
    c.execute("SELECT amount FROM salary WHERE user_id=? AND month=? AND year=?", (uid, month, current_year))
    salary = c.fetchone(); salary = salary[0] if salary else 0

    # Expenses
    c.execute("""
    SELECT id,title,amount,category
    FROM personal
    WHERE user_id=?
    AND strftime('%m',date)=?
    AND strftime('%Y',date)=?
    """, (uid, f"{month:02d}", str(current_year)))

    personal = [{'id':r[0],'title':r[1],'amount':r[2],'category':r[3]} for r in c.fetchall()]
    spent = sum(r['amount'] for r in personal)
    savings = salary - spent
    budget_warning = None
    
    if salary > 0:
        used_percent = (spent / salary) * 100
        if used_percent >= 80:
            budget_warning = f"⚠ You have used {int(used_percent)}% of your salary!"


    # Savings goal
    c.execute("SELECT savings_goal FROM users WHERE id=?", (uid,))
    row = c.fetchone(); goal = row[0] if row and row[0] else 0

    # Category totals
    cat = defaultdict(float)
    for r in personal: cat[r['category']] += r['amount']

    # AI advice
    # AI advice (AUTO SPEAK ENABLED)
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

# ---------- Add personal expense ----------
@app.route("/add_personal", methods=["POST"])
def add_personal():
    if "uid" not in session: return redirect("/")
    uid = session["uid"]
    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form.get("category") or auto_category(title)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO personal(user_id,title,amount,category) VALUES(?,?,?,?)",
              (uid,title,amount,category))
    conn.commit()
    conn.close()
    return redirect("/home")

# ---------- Update salary ----------
@app.route("/update_salary", methods=["POST"])
def update_salary():
    if "uid" not in session: return redirect("/")
    uid = session["uid"]
    amount = float(request.form["salary"])
    month = int(request.form["month"])
    year = datetime.datetime.now().year
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id FROM salary WHERE user_id=? AND month=? AND year=?", (uid, month, year))
    exists = c.fetchone()
    if exists:
        c.execute("UPDATE salary SET amount=? WHERE id=?", (amount, exists[0]))
    else:
        c.execute("INSERT INTO salary(user_id,month,year,amount) VALUES(?,?,?,?)", (uid, month, year, amount))
    conn.commit()
    conn.close()
    return redirect("/home")

# ---------- Delete expense ----------
@app.route("/delete_expense/<int:id>")
def delete_expense(id):
    if "uid" not in session: return redirect("/")
    uid = session["uid"]
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM personal WHERE id=? AND user_id=?", (id, uid))
    conn.commit()
    conn.close()
    return redirect("/home")
MONTH_DETAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Monthly Expense Details</title>
<style>
body{background:#1a1a1a;color:white;font-family:'Segoe UI'}
.container{max-width:900px;margin:auto;padding:20px}
table{width:100%;border-collapse:collapse}
th,td{border:1px solid #555;padding:10px;text-align:center}
th{background:#6a11cb}
a{color:#ffb347}
</style>
</head>
<body>
<div class="container">
<h2>{{month_name}} {{year}} - Expense Details</h2>
<table>
<tr>
<th>Date</th>
<th>Title</th>
<th>Category</th>
<th>Amount (₹)</th>
</tr>
{% for e in expenses %}
<tr>
<td>{{e.date}}</td>
<td>{{e.title}}</td>
<td>{{e.category}}</td>
<td>{{e.amount}}</td>
</tr>
{% endfor %}
</table>
<br>
<a href="/profile">⬅ Back to Profile</a>
</div>
</body>
</html>
"""
@app.route("/profile/month/<int:month>")
def month_details(month):
    if "uid" not in session:
        return redirect("/")

    uid = session["uid"]
    year = datetime.datetime.now().year

    conn = sqlite3.connect(DB)
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


# ---------- Splitwise ----------
SPLIT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Split Expenses</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body{
    margin:0;
    font-family:'Segoe UI',sans-serif;
    background:linear-gradient(135deg,#141e30,#131629);
    color:white;
}
.nav{
    background:linear-gradient(90deg,#6a11cb,#131629);
    padding:16px 22px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    box-shadow:0 4px 12px rgba(0,0,0,.3);
}
.nav span{font-size:20px;font-weight:600}
.nav a{
    color:white;
    text-decoration:none;
    margin-left:10px;
    padding:6px 14px;
    border-radius:10px;
    background:rgba(255,255,255,.15);
}
.nav a:hover{background:rgba(255,255,255,.3)}

.container{
    max-width:900px;
    margin:auto;
    padding:20px;
}
.card{
    background:#131629;
    backdrop-filter:blur(12px);
    padding:24px;
    margin-bottom:22px;
    border-radius:20px;
    box-shadow:0 12px 30px rgba(0,0,0,.25);
}
h3{margin-top:0}

input,button{
    width:100%;
    padding:12px;
    margin:10px 0;
    border-radius:12px;
    border:none;
    outline:none;
    font-size:15px;
    box-sizing:border-box; 
}
input{
    background:rgba(255,255,255,.15);
    color:white;
}
input::placeholder{color:#ddd}

button{
    background:linear-gradient(90deg,#8e2de2,#4a00e0);
    color:white;
    font-weight:600;
    cursor:pointer;
}
button:hover{opacity:.9}

.center{text-align:center}

.rupee-box{position:relative}
.rupee-box span{
    position:absolute;
    left:14px;
    top:50%;
    transform:translateY(-50%);
    color:#ddd;
    font-weight:bold;
}
.rupee-input{padding-left:32px}

table{
    width:100%;
    border-collapse:collapse;
    margin-top:15px;
}
th,td{
    padding:10px;
    border-bottom:1px solid rgba(255,255,255,.2);
    text-align:center;
}
th{
    background:rgba(0,0,0,.3);
}
tr:hover{background:rgba(255,255,255,.05)}

canvas{
    margin:15px auto;
    display:block;
    max-width:260px !important;
}
</style>
</head>

<body>

<div class="nav">
    <span>Split Expenses</span>
    <div>
        <a href="/home">Home 🏠</a>
        <a href="/logout">Logout</a>
    </div>
</div>

<div class="container">

<div class="card">
<h3>Add Split Expense</h3>
<form method="post" action="/add_split">
<input name="title" placeholder="Title" required>

<div class="rupee-box">
<span>₹</span>
<input name="amount" type="number" class="rupee-input" placeholder="Total Amount" required>
</div>

<input name="payer" placeholder="Paid By" required>
<input name="participants" placeholder="Participants (comma separated)" required>

<button>Add Split</button>
</form>
</div>

<div class="card center">
<h3>Who Owes How Much</h3>

<canvas id="pie" width="240" height="240"></canvas>

<table>
<tr><th>Person</th><th>Status</th></tr>
{% for person, amt in net_balance.items() %}
<tr>
<td>{{person}}</td>
<td>
{% if amt>0 %}
Receives ₹{{amt}}
{% elif amt<0 %}
Owes ₹{{-amt}}
{% else %}
Settled
{% endif %}
</td>
</tr>
{% endfor %}
</table>
</div>

</div>

<script>
const data = {{ net_balance|safe }};
const colors = Object.keys(data).map(
  _ => 'hsl(' + Math.random()*360 + ',70%,60%)'
);

new Chart(document.getElementById("pie"), {
  type: "pie",
  data: {
    labels: Object.keys(data),
    datasets: [{
      data: Object.values(data).map(Math.abs),
      backgroundColor: colors
    }]
  },
  options: {
    plugins: {
      legend: { position: 'bottom', labels:{color:'white'} }
    }
  }
});
</script>

</body>
</html>
"""

@app.route("/split")
def split():
    if "uid" not in session: return redirect("/")
    uid = session["uid"]
    conn = sqlite3.connect(DB)
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

@app.route("/add_split",methods=["POST"])
def add_split():
    if "uid" not in session: return redirect("/")
    uid=session["uid"]
    title=request.form["title"]
    amount=float(request.form["amount"])
    payer=request.form["payer"]
    participants=request.form["participants"]
    conn=sqlite3.connect(DB)
    c=conn.cursor()
    c.execute("INSERT INTO split(user_id,title,amount,payer,participants) VALUES(?,?,?,?,?)",(uid,title,amount,payer,participants))
    people=[p.strip() for p in participants.split(",")]
    share=amount/len(people)
    # Add split portion to personal expenses
    c.execute("INSERT INTO personal(user_id,title,amount,category) VALUES(?,?,?,?)",(uid,f"{title} (Split Paid)",share,"Split"))
    conn.commit()
    conn.close()
    return redirect("/split")

# ---------- PROFILE ----------
PROFILE_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Profile</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{
    margin:0;
    font-family:'Segoe UI';
    background:#131629;
    color:white;
}
.nav{
    background:#6a11cb;
    padding:16px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}
.nav a{
    color:white;
    text-decoration:none;
    background:#131629;
    padding:6px 12px;
    border-radius:8px;
}
.container{
    max-width:1000px;
    margin:auto;
    padding:20px;
}
.card{
    background:#2b2b2b;
    padding:22px;
    border-radius:18px;
    margin-bottom:20px;
    box-shadow:0 10px 25px rgba(0,0,0,.2);
}
h2,h3{
    color:#8e2de2;
    text-align:center;
}
.info p{
    font-size:16px;
}
table{
    width:100%;
    border-collapse:collapse;
    margin-top:15px;
}
th,td{
    border:1px solid #555;
    padding:10px;
    text-align:center;
}
th{
    background:#6a11cb;
}
tr:nth-child(even){
    background:#252525;
}
.click-note{
    text-align:center;
    font-size:14px;
    color:#ffb347;
}
</style>
</head>

<body>

<div class="nav">
<span>Profile</span>
<div>
<a href="/home">Home 🏠</a>
<a href="/logout">Logout</a>
</div>
</div>

<div class="container">

<!-- USER INFO -->
<div class="card info">
<h2>{{username}}'s Profile</h2>
<p><b>Email:</b> {{email}}</p>
<p><b>Year:</b> {{current_year}}</p>
<p><b>Total Savings This Year:</b> ₹{{yearly_savings}}</p>
</div>

<!-- MONTHLY CHART -->
<div class="card">
<h3>Month-wise Expenses & Salary</h3>
<p class="click-note">Click on any month bar to view date-wise expenses</p>
<canvas id="monthlyChart" height="120"></canvas>
</div>

<!-- MONTH SUMMARY TABLE -->
<div class="card">
<h3>Monthly Summary</h3>
<table>
<tr>
<th>Month</th>
<th>Salary (₹)</th>
<th>Expenses (₹)</th>
<th>Details</th>
</tr>
{% for i in range(12) %}
<tr>
<td>{{months[i]}}</td>
<td>{{salary[i]}}</td>
<td>{{expenses[i]}}</td>
<td>
<a href="/profile/month/{{i+1}}">View</a>
</td>
</tr>
{% endfor %}
</table>
</div>

</div>

<script>
const ctx = document.getElementById('monthlyChart').getContext('2d');

new Chart(ctx,{
    type:'bar',
    data:{
        labels: {{months|safe}},
        datasets:[
            {
                label:'Expenses (₹)',
                data: {{expenses|safe}},
                backgroundColor:'#6a11cb'
            },
            {
                label:'Salary (₹)',
                data: {{salary|safe}},
                backgroundColor:'#8e2de2'
            }
        ]
    },
    options:{
        responsive:true,
        onClick:(evt,items)=>{
            if(items.length>0){
                const index = items[0].index;
                window.location.href = "/profile/month/" + (index+1);
            }
        },
        plugins:{
            legend:{position:'bottom'}
        }
    }
});
</script>

</body>
</html>
"""


@app.route("/profile")
def profile():
    if "uid" not in session:
        return redirect("/")

    uid = session["uid"]
    now = datetime.datetime.now()
    current_year = now.year

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # User info
    c.execute("SELECT username,email FROM users WHERE id=?", (uid,))
    username, email = c.fetchone()

    # Salary data
    c.execute("SELECT month,amount FROM salary WHERE user_id=? AND year=?", (uid,current_year))
    salary_data = c.fetchall()
    salary_dict = {m:0 for m in range(1,13)}
    for m,a in salary_data:
        salary_dict[m] = a

    # Expense data
    c.execute("""
        SELECT strftime('%m',date), SUM(amount)
        FROM personal
        WHERE user_id=? AND strftime('%Y',date)=?
        GROUP BY strftime('%m',date)
    """,(uid,str(current_year)))

    expense_data = c.fetchall()
    expense_dict = {m:0 for m in range(1,13)}
    for m,a in expense_data:
        expense_dict[int(m)] = a

    conn.close()

    months = [datetime.date(1900,m,1).strftime('%b') for m in range(1,13)]
    expenses = [expense_dict[m] for m in range(1,13)]
    salary = [salary_dict[m] for m in range(1,13)]

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

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)