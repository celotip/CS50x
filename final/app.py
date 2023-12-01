from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Shows homepage"""
    return render_template("index.html")


@app.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    """Allows user to 'donate' some money"""
    if request.method == "GET":
        donate_row = db.execute("SELECT SUM(donate) FROM users")
        try:
            donate = int(donate_row[0]["SUM(donate)"])
        except TypeError:
            donate = 0
        return render_template("/donate.html", donate=donate)
    else:
        donate = int(request.form.get("donate"))
        donate_row = db.execute("SELECT donate FROM users WHERE id = ?", session["user_id"])
        try:
            donate_prev = int(donate_row[0]["donate"])
        except TypeError:
            donate_prev = 0
        donate += donate_prev
        db.execute("UPDATE users SET donate = ? WHERE id = ? ", donate, session["user_id"])
        donate_row = db.execute("SELECT SUM(donate) FROM users")
        try:
            donate = int(donate_row[0]["SUM(donate)"])
        except TypeError:
            donate = 0
        return render_template("/donate.html", donate=donate)


@app.route("/forum", methods=["GET", "POST"])
@login_required
def forum():
    """Allows user to post some questions and view replies, if any exists"""
    if request.method == "GET":
        questions =  db.execute("SELECT * FROM questions")
        return render_template("forum.html", questions=questions)
    else:
        question = request.form.get("question")
        username_row = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username_row[0]["username"]
        db.execute("INSERT INTO questions (user, question) VALUES (?, ?)", username, question)
        questions =  db.execute("SELECT * FROM questions")
        return render_template("forum.html", questions=questions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/members", methods=["GET", "POST"])
def members():
    """Shows a table of members"""
    return render_template("/members.html")


@app.route("/posts", methods=["GET", "POST"])
@login_required
def posts():
    """Shows posts"""
    return render_template("/posts.html")


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """Register user to a role"""
    if request.method == "GET":
        registrants = db.execute("SELECT * FROM registrants")
        return render_template("/register.html", registrants=registrants)
    else:
        name = request.form.get("name")
        role = request.form.get("role")
        db.execute("INSERT INTO registrants (name, role) VALUES (?, ?)", name, role)
        registrants = db.execute("SELECT * FROM registrants")
        return render_template("/register.html", registrants=registrants)

@app.route("/reply", methods=["GET"])
def reply():
    """Shows reply for a question"""
    number = int(request.args.get("reply"))
    replies = db.execute("SELECT * FROM questions WHERE number = ?", number)
    reply = replies[0]["reply_text"]
    question = replies[0]["question"]
    return render_template("/reply1.html", reply=reply, question=question)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Signs a new user up"""
    if request.method == "GET":
        return render_template("/signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users")
        for row in rows:
            if username == row["username"]:
                return apology("username already exists", 400)
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif confirmation != password:
            return apology("passwords do not match", 400)
        else:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                generate_password_hash(password),
            )
            return redirect("/login")
