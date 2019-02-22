import os
import datetime
import pytz

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Done by Mata

    # Display which user's portfolio is displayed
    rows = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    user = rows[0]["username"]

    # Select all companies in user's portfolio with non-zero total amount of shares
    rows = db.execute("SELECT symbol, SUM(total), SUM(number) FROM history WHERE id = :id GROUP BY symbol HAVING SUM(number) > 0",
                      id=session["user_id"])

    # Create a list of items to be displayed
    symbols = []
    companies = []
    numbers = []
    prices = []
    totals = []
    profits = []
    row = 0
    items = len(rows)

    # Iterate over all selected rows to populate template table with variable values
    for row in range(items):

        # Query stock symbol
        symbol = rows[row]["symbol"]
        symbols.append(symbol)

        # Query company name
        quotation = lookup(symbol)
        company = quotation["name"]
        companies.append(company)

        # Query number of shares
        num = rows[row]["SUM(number)"]
        numbers.append(num)

        # Query current stock price
        price = quotation["price"]
        prices.append(price)

        # Calculate total value per stock owned
        total = float(price) * float(num)
        totals.append(total)

        # Calculate profitability per stock owned
        paid = rows[row]["SUM(total)"]

        # Select all rows with non-zero owned_num for given company
        lines = db.execute("SELECT price, owned_num FROM history WHERE id = :id AND symbol = :symbol AND owned_num > 0",
                           id=session["user_id"], symbol=symbol)

        # Create variable for total owned number of shares of given company and total paid amount for given owned shares
        nums = 0
        line_totals = 0
        lenght = len(lines)

        # Iterate over all rows to calculate average unit price
        for line in range(lenght):

            line_price = lines[line]["price"]
            line_owned = lines[line]["owned_num"]
            line_price = float(line_price)
            line_owned = float(line_owned)

            # Update total paid for the number owned
            line_total = line_price * line_owned
            line_totals = line_totals + line_total

            # Update total owned number of shares of given company
            nums = nums + lines[line]["owned_num"]

        # Calculate average paid unit price
        avg_price = line_totals / nums

        # Calculate profit as delta of current and paid price times number of shares owned
        profit = (price - avg_price) * num

        # Update profits (to be displayed in html)
        profits.append(profit)

    # Query current available cash
    cashnow = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = cashnow[0]["cash"]

    # Update available cash after purchase
    wealth = 0
    for total in totals:
        wealth = wealth + total
    wealth = wealth + cash

    return render_template("index.html", user=user, items=items, rows=rows, symbols=symbols,
                           companies=companies, numbers=numbers, prices=prices, totals=totals,
                           profits=profits, usd=usd, cash=cash, wealth=wealth)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Done by Mata

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure stock symbol submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Ensure user provided valid stock symbol
        if not lookup(request.form.get("symbol")):
            return apology("must provide valid stock symbol", 400)

        # Ensure number of shares submitted
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        # Store number of shares in a variable
        number = request.form.get("shares")

        # Ensure user provided positive integer
        if not number.isdigit():
            return apology("must provide positive integer", 400)

        # Calculate total value of stock to buy
        quotation = lookup(request.form.get("symbol"))
        price = quotation["price"]
        total = float(price) * float(number)

        # Define datetime (source: https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python)
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        cet_now = utc_now.astimezone(pytz.timezone("Europe/Bratislava"))

        # Query cash that the user has
        rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        # If user can afford it, buy stock
        if rows[0]["cash"] > total:
            rows = db.execute("INSERT INTO history (id, symbol, price, number, total, datetime, owned_num) VALUES (:id, :symbol, \
                              :price, :number, :total, :datetime, :number)", id=session["user_id"], symbol=quotation["symbol"],
                              price=price, number=int(number), total=total, datetime=cet_now)

            # Update cash
            rows = db.execute("UPDATE users SET cash = cash - :total WHERE id = :id", id=session["user_id"], total=total)

            # Query if symbol exists in companies table
            rows = db.execute("SELECT symbol FROM companies WHERE symbol = :symbol", symbol=quotation["symbol"])

            # If symbol does not exist in database
            if len(rows) == 0:

                # Insert company name into companies table
                companies = db.execute("INSERT INTO companies (symbol, name) VALUES (:symbol, :name)",
                                       symbol=quotation["symbol"], name=quotation["name"])

            return redirect("/")

        # Else return apology
        else:
            return apology("you don't have enough cash", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Done by Mata

    # Display sentence informing which user's history is displayed
    rows = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    user = rows[0]["username"]

    # Select all rows in user's portfolio
    rows = db.execute("SELECT * FROM history WHERE id = :id", id=session["user_id"])

    # Create a list of items to be displayed
    symbols = []
    companies = []
    num_buy = []
    num_sell = []
    prices = []
    totals = []
    profits = []
    datetimes = []
    balance = 0
    row = 0
    items = len(rows)

    # Iterate over all selected rows to populate template table with variable values
    for row in range(items):

        # Query symbol
        symbol = rows[row]["symbol"]
        symbols.append(symbol)

        # Query company name in companies
        company = db.execute("SELECT name FROM companies WHERE symbol = :symbol", symbol=symbol)
        company = company[0]["name"]
        companies.append(company)

        # Query number of shares bought
        num = rows[row]["number"]
        if num > 0:
            num_buy.append(num)
            num_sell.append("")

        # Treat number of shares sold
        else:
            num_sell.append(num)
            num_buy.append("")

        # Query price at purchase/sale
        price = float(rows[row]["price"])
        prices.append(price)

        # Query total value of purchase/sale
        total = price * num
        totals.append(total)

        # Query date and time of purchase/sale
        datetime = rows[row]["datetime"]
        datetimes.append(datetime)

        # Query profit
        profit = rows[row]["profit"]
        profits.append(profit)

        # Store total profit/loss amount in variable to display at end of history table
        balance = balance + profit

    return render_template("history.html", user=user, usd=usd, row=row, items=items, symbols=symbols, companies=companies,
                           num_buy=num_buy, num_sell=num_sell, prices=prices, totals=totals, profits=profits, datetimes=datetimes,
                           balance=balance)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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
    # Done by Mata

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure stock symbol is valid
        if not lookup(request.form.get("symbol")):
            return apology("must provide valid stock symbol", 400)

        # Lookup stock value
        else:
            quotation = lookup(request.form.get("symbol"))

        # Render quote to user
        return render_template("quoted.html", name=quotation["name"], price=usd(quotation["price"]),
                               symbol=quotation["symbol"])

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Done by Mata

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure 2nd instance of password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Store user's input in variables
        u = request.form.get("username")
        p = request.form.get("password")
        c = request.form.get("confirmation")

        # Generate password hash and store it in variable
        hash = generate_password_hash(p)

        # Ensure same password inputted twice
        if p != c:
            return apology("passwords do not match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :u", u=u)

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Insert user into database
        rows = db.execute("INSERT INTO users (username, hash, cash) VALUES (:u, :hash, '10000')",
                          u=u, hash=hash)

        # Query database again to assign id to session
        rows = db.execute("SELECT * FROM users WHERE username = :u", u=u)

        # Log in user automatically
        session["user_id"] = rows[0]["id"]

        # Redirect user to index page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Done by Mata

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure stock symbol was selected
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Query number of shares of given stock owned by user
        rows = db.execute("SELECT SUM(number) FROM history WHERE id = :id AND symbol = :symbol",
                          id=session["user_id"], symbol=request.form.get("symbol"))

        # Store owned number of shares in a variable and convert to integer
        owned_shares = rows[0]["SUM(number)"]
        owned_shares = int(owned_shares)

        # Ensure user owns selected stock
        if not owned_shares > 0:
            return apology("you don't own given stock", 400)

        # Store number of shares in a variable
        shares = request.form.get("shares")

        # Ensure user provided integer as number of shares
        if not shares.isdigit():
            return apology("must provide positive integer", 400)

        # Convert shares to integer
        shares = int(shares)

        # Ensure user provided positive integer as number of shares
        if not shares > 0:
            return apology("must provide positive integer", 400)

        # Ensure user owns enough shares
        if not shares < owned_shares and not shares == owned_shares:
            return apology("you don't own enough shares", 400)

        # Query the current price per share
        quotation = lookup(request.form.get("symbol"))

        # Calculate total
        total = quotation["price"] * shares * -1

        # Define datetime (source: https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python)
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        cet_now = utc_now.astimezone(pytz.timezone("Europe/Bratislava"))

        # Update owned number of shares of given company by selecting purchase rows with still existing shares
        rows = db.execute("SELECT number, owned_num, price, hist_id FROM history WHERE id = :id AND symbol = :symbol AND owned_num > 0",
                          id=session["user_id"], symbol=quotation["symbol"])

        lenth = len(rows)
        paid = 0
        shares_sold = shares

        # Iterate over rows to find correct row(s) to update
        for row in range(lenth):

            # Calculate delta between owned shares in given row and shares being sold
            remaining = int(rows[row]["owned_num"]) - shares

            # If shares being sold are fewer than shares owned
            if remaining >= 0:

                # Calculate paid
                paid = paid + (shares * float(rows[row]["price"]))

                # Update owned_num with new amount
                update = db.execute("UPDATE history SET owned_num = :remaining WHERE hist_id = :hist_id",
                                    remaining=remaining, hist_id=rows[row]["hist_id"])

                # Since all sold shares have been substracted from owned shares, update shares to zero and break loop
                shares = 0
                break

            # If shares being sold are greater than shares owned in given row
            else:

                # Calculate paid
                paid = paid + (int(rows[row]["owned_num"]) * float(rows[row]["price"]))

                # Update owned_num with zero (i.e. decrease value by maximum possible amount)
                update = db.execute("UPDATE history SET owned_num = '0' WHERE hist_id = :hist_id", hist_id=rows[row]["hist_id"])

                # Calculate remaining number of shares to be substracted from owned shares (in subsequent rows)
                shares = remaining * -1

        # Calculate average paid price per share
        avg_price = paid / shares_sold

        # Calculate profit as delta btw current price and average price paid times shares sold
        profit = (quotation["price"] - avg_price) * shares_sold

        # Insert sale into history
        rows = db.execute("INSERT INTO history (id, symbol, price, number, total, datetime, profit) VALUES (:id, :symbol, :price, \
                          :number, :total, :datetime, :profit)", id=session["user_id"], symbol=quotation["symbol"],
                          price=quotation["price"], number=(shares_sold * -1), total=total, datetime=cet_now, profit=profit)

        # Update cash in users
        cashnow = db.execute("UPDATE users SET cash = cash - :total WHERE id = :id", id=session["user_id"], total=total)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Query all the stock symbols the user owns
        rows = db.execute("SELECT symbol FROM history GROUP BY symbol HAVING id = :id", id=session["user_id"])

        # Iterate over selected rows to populate template table with variable values
        symbols = []
        row = 0
        items = len(rows)
        for row in range(items):
            symbol = rows[row]["symbol"]
            symbols.append(symbol)

        return render_template("sell.html", symbols=symbols, items=items)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
