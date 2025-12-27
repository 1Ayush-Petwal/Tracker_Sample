"""
HTML templates for the Expense Tracker application
"""

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

