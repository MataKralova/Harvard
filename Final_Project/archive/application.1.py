import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/")
# @login_required
def index():
    """Show portfolio of stocks"""

    # Display which user's portfolio is displayed
    # rows = db.execute("SELECT username FROM users WHERE user_id = :user_id", user_id=session["user_id"])
    # user = rows[0]["username"]

    # Select all companies in user's portfolio with non-zero total amount of shares
    # rows = db.execute("SELECT symbol, SUM(total), SUM(number) FROM history WHERE id = :id GROUP BY symbol HAVING SUM(number) > 0",
    #                   id=session["user_id"])

    # Display all books
    rows = db.execute("SELECT * FROM books")

    # Create a list of items to be displayed
    sectors = []
    # companies = []
    # numbers = []
    # prices = []
    # totals = []
    # profits = []
    row = 0
    items = len(rows)


    # Create a list of items to be displayed
        sectors = []
        new_sectors = []
        sector_names = []
        authors = []
        titles = []
        editions = []
        firstYs = []
        ourYs = []
        languages = []
        countries = []
        fict_facts = []
        art_others = []
        forms = []
        contents = []
        comments = []
        row = 0
        # items = len(rows)
        items = 20

        # Iterate over all selected rows to populate template table with variable values
        for row in range(items):

            # Query sector
            lines = db.execute("SELECT sector FROM sectors WHERE sect_id = :sect_id", sect_id=rows[row]["sector"])
            sector = lines[0]["sector"]
            sectors.append(sector)

            # Query new_sector
            lines = db.execute("SELECT new_sector FROM new_sectors WHERE new_sect_id = :new_sect_id", new_sect_id=rows[row]["new_sector"])
            new_sector = lines[0]["new_sector"]
            new_sectors.append(new_sector)

            # Query sector_name
            lines = db.execute("SELECT sector_name FROM sector_names WHERE sect_name_id = :sect_name_id", sect_name_id=rows[row]["sector_name"])
            sector_name = lines[0]["sector_name"]
            sector_names.append(sector_name)

            # Query author
            lines = db.execute("SELECT author FROM authors WHERE author_id = :author_id", author_id=rows[row]["author"])
            author = lines[0]["author"]
            authors.append(author)

            # Query title
            title = rows[row]["title"]
            titles.append(title)

            # Query edition
            lines = db.execute("SELECT edition FROM editions WHERE ed_id = :ed_id", ed_id=rows[row]["edition"])
            edition = lines[0]["edition"]
            editions.append(edition)

            # Query firstY
            lines = db.execute("SELECT firstY FROM firstYs WHERE firstY_id = :firstY_id", firstY_id=rows[row]["firstY"])
            firstY = lines[0]["firstY"]
            firstYs.append(firstY)

            # Query ourY
            lines = db.execute("SELECT ourY FROM ourYs WHERE ourY_id = :ourY_id", ourY_id=rows[row]["ourY"])
            ourY = lines[0]["ourY"]
            ourYs.append(ourY)

            # Query language
            lines = db.execute("SELECT language FROM languages WHERE lang_id = :lang_id", lang_id=rows[row]["language"])
            language = lines[0]["language"]
            languages.append(language)

            # Query country
            lines = db.execute("SELECT country FROM countries WHERE ctry_id = :ctry_id", ctry_id=rows[row]["country"])
            country = lines[0]["country"]
            countries.append(country)

            # Query fict_fact
            lines = db.execute("SELECT fict_fact FROM fict_facts WHERE fict_id = :fict_id", fict_id=rows[row]["fict_fact"])
            fict_fact = rows[row]["fict_fact"]
            fict_facts.append(fict_fact)

            # Query art_other
            lines = db.execute("SELECT art_other FROM art_others WHERE art_id = :art_id", art_id=rows[row]["art_other"])
            art_other = lines[0]["art_other"]
            art_others.append(art_other)

            # Query form
            lines = db.execute("SELECT form FROM forms WHERE form_id = :form_id", form_id=rows[row]["form"])
            form = lines[0]["form"]
            forms.append(form)

            # Query content
            lines = db.execute("SELECT content FROM contents WHERE cont_id = :cont_id", cont_id=rows[row]["content"])
            content = lines[0]["content"]
            contents.append(content)

            # Query comment
            lines = db.execute("SELECT comment FROM comments WHERE comment_id = :comment_id", comment_id=rows[row]["comment"])
            comment = lines[0]["comment"]
            comments.append(comment)

        return render_template("index.html", items=items, rows=rows, sectors=sectors, new_sectors=new_sectors, sector_names=sector_names, authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages,
                                countries=countries, fict_facts=fict_facts, art_others=art_others, forms=forms, contents=contents, comments=comments)








    # Iterate over all selected rows to populate template table with variable values
    for row in range(items):

        # Query sector
        sector = rows[row]["sector"]
        sectors.append(sector)

        # Query company name
        # quotation = lookup(symbol)
        # company = quotation["name"]
        # companies.append(company)

        # Query number of shares
        # num = rows[row]["SUM(number)"]
        # numbers.append(num)

        # Query current stock price
        # price = quotation["price"]
        # prices.append(price)

        # Calculate total value per stock owned
        # total = float(price) * float(num)
        # totals.append(total)

        # Calculate profitability per stock owned
        # paid = rows[row]["SUM(total)"]

        # Select all rows with non-zero owned_num for given company
        # lines = db.execute("SELECT price, owned_num FROM history WHERE id = :id AND symbol = :symbol AND owned_num > 0",
        #                    id=session["user_id"], symbol=symbol)

        # Create variable for total owned number of shares of given company and total paid amount for given owned shares
        # nums = 0
        # line_totals = 0
        # lenght = len(lines)

        # Iterate over all rows to calculate average unit price
        # for line in range(lenght):

        #     line_price = lines[line]["price"]
        #     line_owned = lines[line]["owned_num"]
        #     line_price = float(line_price)
        #     line_owned = float(line_owned)

            # Update total paid for the number owned
        #     line_total = line_price * line_owned
        #     line_totals = line_totals + line_total

            # Update total owned number of shares of given company
            # nums = nums + lines[line]["owned_num"]

        # Calculate average paid unit price
        # avg_price = line_totals / nums

        # Calculate profit as delta of current and paid price times number of shares owned
        # profit = (price - avg_price) * num

        # Update profits (to be displayed in html)
        # profits.append(profit)

    # Query current available cash
    # cashnow = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    # cash = cashnow[0]["cash"]

    # Update available cash after purchase
    # wealth = 0
    # for total in totals:
    #     wealth = wealth + total
    # wealth = wealth + cash

    return render_template("index.html", items=items, rows=rows, sectors=sectors)
    # return render_template("index.html", user=user, items=items, rows=rows, symbols=symbols,
    #                        companies=companies, numbers=numbers, prices=prices, totals=totals,
    #                        profits=profits, usd=usd, cash=cash, wealth=wealth)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

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

        # Ensure 2nd instance of password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # Store user's input in variables
        u = request.form.get("username")
        p = request.form.get("password")
        c = request.form.get("confirmation")

        # Generate password hash and store it in variable
        hash = generate_password_hash(p)

        # Ensure same password inputted twice
        if p != c:
            return apology("passwords do not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :u", u=u)

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("username already exists", 403)

        # Insert user into database
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:u, :hash)",
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
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
