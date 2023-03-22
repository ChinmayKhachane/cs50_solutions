import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    use_id = session["user_id"]

    Transactions_db = db.execute("SELECT symbol, SUM(shares) AS shares, price FROM Transactions WHERE user_id = ? GROUP BY symbol", use_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", use_id)
    cash_amount = cash_db[0]["cash"]

    return render_template("index.html", database = Transactions_db, cash = cash_amount)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        try:

            shares = int(request.form.get("shares"))

        except ValueError:

            return apology("Number must be integer")

        if not symbol:
            return apology("Must provide Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Please provide a valid symbol")

        if shares < 0:
            return apology("Please provide a valid number of shares")

        value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < value:
            return apology("Not enough funds to complete transaction")

        new_cash = user_cash - value

        db.execute("UPDATE users SET cash = ? WHERE id =?", new_cash, user_id)

        date = datetime.datetime.now()

        db.execute("INSERT INTO Transactions(user_id, symbol, price, shares, Date) VALUES(?, ?, ?, ?, ?)", user_id, stock["symbol"], stock["price"], shares, date)

        flash("Transaction successful!")

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show trasaction history"""
    use_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM Transactions WHERE user_id = :id", id=use_id)
    return render_template("history.html", transactions = transactions_db)

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to users account"""
    if request.method == "GET":
        return render_template("addcash.html")
    else:
        new = request.form.get("new_cash")

        if not new:
            return apology("Must give money")

        use_id = session["user_id"]

        use_id = session["user_id"]
        cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id = use_id)
        cash = cash_db[0]["cash"]

        up_cash = cash + new

        db.execute("UPDATE users SET cash = ? WHERE id =?", up_cash, use_id)

        return redirect("/")



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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must provide Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Please provide a valid symbol")

        return render_template("quoted.html", name = stock["name"], price = stock["price"], )



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("You must enter a username")
        if not password:
            return apology("You must enter a password")
        if not confirmation:
            return apology("You must re-enter your password")
        if confirmation != password:
            return apology("Confirmation must match password")

        pswd_hash = generate_password_hash(confirmation)

        try:
            new_user = db.execute("INSERT into users (username, hash) VALUES(?, ?)", username, pswd_hash)
        except:
            return apology("Username is already taken")

        session["user_id"] = new_user

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        use_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM Transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id = use_id)
        return render_template("sell.html", symbs = [row["symbol"] for row in symbols])

    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Must provide Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Share not allowed")

        if shares < 0:
            return apology("Please provide a valid number of shares")

        value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id = use_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id=:id AND symbol = :symbol")
        share = user_shares[0]["shares"]

        if shares > share:
            return apology("You dont have those shares")

        new_cash = user_cash + value

        db.execute("UPDATE users SET cash = ? WHERE id =?", new_cash, user_id)

        date = datetime.datetime.now()

        db.execute("INSERT INTO Transactions(user_id, symbol, price, shares, Date) VALUES(?, ?, ?, ?, ?)", user_id, stock["symbol"], stock["price"], (-1)*shares, date)

        flash("Transaction successful!")

        return redirect("/")



