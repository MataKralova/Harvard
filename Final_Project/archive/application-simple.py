import datetime
import os
import pytz

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
# from pytz import timezone
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

# Define global variables to be used accross admin function
sector = ""
new_sector = ""
sector_name = ""
author = ""
title = ""
edition = ""
firstY = ""
ourY = ""
language = ""
country = ""
fict_fact = ""
art_other = ""
form = ""
content = ""
comment = ""


@app.route("/admin", methods=["GET", "POST"])
# @login_required
def admin():
    """Insert, update and delete books from database"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":



        # User clicked on "Insert" button
        if request.form.get("insert"):

            # Allow access to these values when user clicks "Confirm" button
            global sector
            global title

            # Populate data items to be shown for confirmation
            if not request.form.get("ins_sector") == "Select...":
                sector = request.form.get("ins_sector")

            if not request.form.get("ins_title") == "Select...":
                title = request.form.get("ins_title")

            return render_template("confirm.html", action="INSERT into", sector=sector, title=title)

        # User clicked on "Cancel" button
        if request.form.get("cancel"):

            return redirect("/admin")

        # User clicked on "Confirm" button meaning "Insert" on confirm.html page
        if request.form.get("INSERT into"):

            # if request.form.get("add_new_book"):
            rows = db.execute("INSERT INTO tests (test_title, author, datetime) VALUES (:test_title, :author, :datetime)", test_title=title, author=author, datetime=cet_now)

            # return redirect("/")
            return render_template("updated.html", action="INSERTED into", sector=sector, new_sector=new_sector, sector_name=sector_name, author=author, title=title, edition=edition,
                                 firstY=firstY, ourY=ourY, language=language, country=country, fict_fact=fict_fact, art_other=art_other, form=form, content=content, comment=comment)

        # User clicked on "OK" button on updated.html page
        if request.form.get("ok"):
            return redirect("/admin")

        # User clicked on "Search" button
        else:

            # Query all sector categories
            lines = db.execute("SELECT sector FROM sectors")
            # Create list of items to be displayed
            all_sectors = []
            line = 0
            nb_sectors = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("sector") and request.form.get("sector") != "Select...":
                sector = request.form.get("sector")
                all_sectors.append(sector)

            # Store "Select..." as default dropdown option
            sector = "Select..."
            all_sectors.append(sector)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_sectors):
                # Populate dropdown filter menu for sector
                sector = lines[line]["sector"]
                all_sectors.append(sector)


            # Query all new_sector categories
            lines = db.execute("SELECT new_sector FROM new_sectors")
            # Create list of items to be displayed
            all_new_sectors = []
            line = 0
            nb_new_sectors = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("new_sector") and request.form.get("new_sector") != "Select...":
                new_sector = request.form.get("new_sector")
                all_new_sectors.append(new_sector)

            # Store "Select..." as default dropdown option
            new_sector = "Select..."
            all_new_sectors.append(new_sector)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_new_sectors):
                # Populate dropdown filter menu for new_sector
                new_sector = lines[line]["new_sector"]
                all_new_sectors.append(new_sector)


            # Query all sector_name categories
            lines = db.execute("SELECT sector_name FROM sector_names")
            # Create list of items to be displayed
            all_sector_names = []
            line = 0
            nb_sector_names = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("sector_name") and request.form.get("sector_name") != "Select...":
                sector_name = request.form.get("sector_name")
                all_sector_names.append(sector_name)

            # Store "Select..." as default dropdown option
            sector_name = "Select..."
            all_sector_names.append(sector_name)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_sector_names):
                # Populate dropdown filter menu for sector_name
                sector_name = lines[line]["sector_name"]
                all_sector_names.append(sector_name)


            # Query all edition categories
            lines = db.execute("SELECT edition FROM editions")
            # Create list of items to be displayed
            all_editions = []
            line = 0
            nb_editions = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("edition") and request.form.get("edition") != "Select...":
                edition = request.form.get("edition")
                all_editions.append(edition)

            # Store "Select..." as default dropdown option
            edition = "Select..."
            all_editions.append(edition)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_editions):
                # Populate dropdown filter menu for edition
                edition = lines[line]["edition"]
                all_editions.append(edition)


            # Query all language categories
            lines = db.execute("SELECT language FROM languages")
            # Create list of items to be displayed
            all_languages = []
            line = 0
            nb_languages = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("language") and request.form.get("language") != "Select...":
                language = request.form.get("language")
                all_languages.append(language)

            # Store "Select..." as default dropdown option
            language = "Select..."
            all_languages.append(language)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_languages):
                # Populate dropdown filter menu for language
                language = lines[line]["language"]
                all_languages.append(language)


            # Query all country categories
            lines = db.execute("SELECT country FROM countries")
            # Create list of items to be displayed
            all_countries = []
            line = 0
            nb_countries = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("country") and request.form.get("country") != "Select...":
                country = request.form.get("country")
                all_countries.append(country)

            # Store "Select..." as default dropdown option
            country = "Select..."
            all_countries.append(country)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_countries):
                # Populate dropdown filter menu for country
                country = lines[line]["country"]
                all_countries.append(country)


            # Query all fict_fact categories
            lines = db.execute("SELECT fict_fact FROM fict_facts")
            # Create list of items to be displayed
            all_fict_facts = []
            line = 0
            nb_fict_facts = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("fict_fact") and request.form.get("fict_fact") != "Select...":
                fict_fact = request.form.get("fict_fact")
                all_fict_facts.append(fict_fact)

            # Store "Select..." as default dropdown option
            fict_fact = "Select..."
            all_fict_facts.append(fict_fact)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_fict_facts):
                # Populate dropdown filter menu for fict_fact
                fict_fact = lines[line]["fict_fact"]
                all_fict_facts.append(fict_fact)


            # Query all art_other categories
            lines = db.execute("SELECT art_other FROM art_others")
            # Create list of items to be displayed
            all_art_others = []
            line = 0
            nb_art_others = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("art_other") and request.form.get("art_other") != "Select...":
                art_other = request.form.get("art_other")
                all_art_others.append(art_other)

            # Store "Select..." as default dropdown option
            art_other = "Select..."
            all_art_others.append(art_other)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_art_others):
                # Populate dropdown filter menu for art_other
                art_other = lines[line]["art_other"]
                all_art_others.append(art_other)


            # Query all form categories
            lines = db.execute("SELECT form FROM forms")
            # Create list of items to be displayed
            all_forms = []
            line = 0
            nb_forms = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("form") and request.form.get("form") != "Select...":
                form = request.form.get("form")
                all_forms.append(form)

            # Store "Select..." as default dropdown option
            form = "Select..."
            all_forms.append(form)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_forms):
                # Populate dropdown filter menu for form
                form = lines[line]["form"]
                all_forms.append(form)


            # Query all content categories
            lines = db.execute("SELECT content FROM contents")
            # Create list of items to be displayed
            all_contents = []
            line = 0
            nb_contents = len(lines)

            # If selection was made, keep the selected option as default
            if request.form.get("content") and request.form.get("content") != "Select...":
                content = request.form.get("content")
                all_contents.append(content)

            # Store "Select..." as default dropdown option
            content = "Select..."
            all_contents.append(content)

            # Iterate over all selected rows to populate template table with all categories
            for line in range(nb_contents):
                # Populate dropdown filter menu for content
                content = lines[line]["content"]
                all_contents.append(content)


            # Convert filtered SEARCH parameters to be used in query
            if request.form.get("sector") == "":
                sector = ""
            elif request.form.get("sector") == "Select...":
                sector = "%"
            else:
                sector = "%" + request.form.get("sector") + "%"

            if request.form.get("new_sector") == "":
                new_sector = ""
            elif request.form.get("new_sector") == "Select...":
                new_sector = "%"
            else:
                new_sector = "%" + request.form.get("new_sector") + "%"

            if request.form.get("sector_name") == "":
                sector_name = ""
            elif request.form.get("sector_name") == "Select...":
                sector_name = "%"
            else:
                sector_name = "%" + request.form.get("sector_name") + "%"

            if request.form.get("author") == " ":
                author = ""
            elif request.form.get("author") == "Select...":
                author = "%"
            else:
                author = "%" + request.form.get("author") + "%"

            # Title field cannot be blank (but can be not filtered)
            if request.form.get("title") == "Select...":
                title = "%"
            else:
                title = "%" + request.form.get("title") + "%"

            if request.form.get("edition") == "":
                edition = ""
            elif request.form.get("edition") == "Select...":
                edition = "%"
            else:
                edition = "%" + request.form.get("edition") + "%"

            if request.form.get("firstY") == " ":
                firstY = ""
            elif request.form.get("firstY") == "Select...":
                firstY = "%"
            else:
                firstY = "%" + request.form.get("firstY") + "%"

            if request.form.get("ourY") == " ":
                ourY = ""
            elif request.form.get("ourY") == "Select...":
                ourY = "%"
            else:
                ourY = "%" + request.form.get("ourY") + "%"

            if request.form.get("language") == "":
                language = ""
            elif request.form.get("language") == "Select...":
                language = "%"
            else:
                language = "%" + request.form.get("language") + "%"

            if request.form.get("country") == "":
                country = ""
            elif request.form.get("country") == "Select...":
                country = "%"
            else:
                country = "%" + request.form.get("country") + "%"

            if request.form.get("fict_fact") == "":
                fict_fact = ""
            elif request.form.get("fict_fact") == "Select...":
                fict_fact = "%"
            else:
                fict_fact = "%" + request.form.get("fict_fact") + "%"

            if request.form.get("art_other") == "":
                art_other = ""
            elif request.form.get("art_other") == "Select...":
                art_other = "%"
            else:
                art_other = "%" + request.form.get("art_other") + "%"

            if request.form.get("form") == "":
                form = ""
            elif request.form.get("form") == "Select...":
                form = "%"
            else:
                form = "%" + request.form.get("form") + "%"

            if request.form.get("content") == "":
                content = ""
            elif request.form.get("content") == "Select...":
                content = "%"
            else:
                content = "%" + request.form.get("content") + "%"

            if request.form.get("comment") == " ":
                comment = ""
            elif request.form.get("comment") == "Select...":
                comment = "%"
            else:
                comment = "%" + request.form.get("comment") + "%"


            # Query books by filter parameters
            rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                               authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                               languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                               forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE sector LIKE :sector AND new_sector LIKE :new_sector AND \
                               sector_name LIKE :sector_name AND author LIKE :author AND title LIKE :title AND edition LIKE :edition AND firstY LIKE :firstY AND ourY LIKE :ourY AND language LIKE :language AND country LIKE :country AND fict_fact LIKE :fict_fact AND \
                               art_other LIKE :art_other AND form LIKE :form AND content LIKE :content AND comment LIKE :comment", sector=sector, new_sector=new_sector, sector_name=sector_name, author=author, title=title, edition=edition,
                               firstY=firstY, ourY=ourY, language=language, country=country, fict_fact=fict_fact, art_other=art_other, form=form, content=content, comment=comment)
            # rows = db.execute("SELECT * FROM books WHERE sector = :sector AND new_sector = :new_sector AND sector_name = :sector_name AND author = :author AND title = :title AND edition = :edition AND firstY = :firstY AND ourY = :ourY \
            #                    AND language = :language AND country = :country AND fict_fact = :fict_fact AND art_other = :art_other AND form = :form AND content = :content AND comment = :comment",
            #                   sector=request.form.get("sector"), new_sector=request.form.get("new_sector"), sector_name=request.form.get("sector_name"), author=request.form.get("author"), title=request.form.get("title"), edition=request.form.get("edition"),
            #                   firstY=request.form.get("firstY"), ourY=request.form.get("ourY"), language=request.form.get("language"), country=request.form.get("country"), fict_fact=request.form.get("fict_fact"), art_other=request.form.get("art_other"),
            #                   form=request.form.get("form"), content=request.form.get("content"), comment=request.form.get("comment"))

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
            items = len(rows)

            # Iterate over all selected rows to populate template table with variable values
            for row in range(items):

                # Populate list with sector
                sector = rows[row]["sector"]
                sectors.append(sector)

                # Populate list with new_sector
                new_sector = rows[row]["new_sector"]
                new_sectors.append(new_sector)

                # Query sector_name
                sector_name = rows[row]["sector_name"]
                sector_names.append(sector_name)

                # Query author
                author = rows[row]["author"]
                authors.append(author)

                # Query title
                title = rows[row]["title"]
                titles.append(title)

                # Query edition
                edition = rows[row]["edition"]
                editions.append(edition)

                # Query firstY
                firstY = rows[row]["firstY"]
                firstYs.append(firstY)

                # Query ourY
                ourY = rows[row]["ourY"]
                ourYs.append(ourY)

                # Query language
                language = rows[row]["language"]
                languages.append(language)

                # Query country
                country = rows[row]["country"]
                countries.append(country)

                # Query fict_fact
                fict_fact = rows[row]["fict_fact"]
                fict_facts.append(fict_fact)

                # Query art_other
                art_other = rows[row]["art_other"]
                art_others.append(art_other)

                # Query form
                form = rows[row]["form"]
                forms.append(form)

                # Query content
                content = rows[row]["content"]
                contents.append(content)

                # Query comment
                comment = rows[row]["comment"]
                comments.append(comment)


            return render_template("admin.html", all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names, nb_sector_names=nb_sector_names,
                                   all_editions=all_editions, nb_editions=nb_editions, all_languages=all_languages, nb_languages=nb_languages, all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts,
                                   all_art_others=all_art_others, nb_art_others=nb_art_others, all_forms=all_forms, nb_forms=nb_forms, all_contents=all_contents, nb_contents=nb_contents, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors, sector_names=sector_names, authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages,
                                   countries=countries, fict_facts=fict_facts, art_others=art_others, forms=forms, contents=contents, comments=comments)


    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Query all sector categories
        lines = db.execute("SELECT sector FROM sectors")
        # Create list of items to be displayed
        all_sectors = []
        line = 0
        nb_sectors = len(lines)

        # Store "Select..." as default dropdown option
        sector = "Select..."
        all_sectors.append(sector)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_sectors):
            # Populate dropdown filter menu for sector
            sector = lines[line]["sector"]
            all_sectors.append(sector)


        # Query all new_sector categories
        lines = db.execute("SELECT new_sector FROM new_sectors")
        # Create list of items to be displayed
        all_new_sectors = []
        line = 0
        nb_new_sectors = len(lines)

        # Store "Select..." as default dropdown option
        new_sector = "Select..."
        all_new_sectors.append(new_sector)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_new_sectors):
            # Populate dropdown filter menu for sector
            new_sector = lines[line]["new_sector"]
            all_new_sectors.append(new_sector)


        # Query all sector_name categories
        lines = db.execute("SELECT sector_name FROM sector_names")
        # Create list of items to be displayed
        all_sector_names = []
        line = 0
        nb_sector_names = len(lines)

        # Store "Select..." as default dropdown option
        sector_name = "Select..."
        all_sector_names.append(sector_name)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_sector_names):
            # Populate dropdown filter menu for sector
            sector_name = lines[line]["sector_name"]
            all_sector_names.append(sector_name)


        # Query all edition categories
        lines = db.execute("SELECT edition FROM editions")
        # Create list of items to be displayed
        all_editions = []
        line = 0
        nb_editions = len(lines)

        # Store "Select..." as default dropdown option
        edition = "Select..."
        all_editions.append(edition)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_editions):
            # Populate dropdown filter menu for sector
            edition = lines[line]["edition"]
            all_editions.append(edition)


        # Query all language categories
        lines = db.execute("SELECT language FROM languages")
        # Create list of items to be displayed
        all_languages = []
        line = 0
        nb_languages = len(lines)

        # Store "Select..." as default dropdown option
        language = "Select..."
        all_languages.append(language)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_languages):
            # Populate dropdown filter menu for language
            language = lines[line]["language"]
            all_languages.append(language)


        # Query all country categories
        lines = db.execute("SELECT country FROM countries")
        # Create list of items to be displayed
        all_countries = []
        line = 0
        nb_countries = len(lines)

        # Store "Select..." as default dropdown option
        country = "Select..."
        all_countries.append(country)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_countries):
            # Populate dropdown filter menu for country
            country = lines[line]["country"]
            all_countries.append(country)


        # Query all fict_fact categories
        lines = db.execute("SELECT fict_fact FROM fict_facts")
        # Create list of items to be displayed
        all_fict_facts = []
        line = 0
        nb_fict_facts = len(lines)

        # Store "Select..." as default dropdown option
        fict_fact = "Select..."
        all_fict_facts.append(fict_fact)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_fict_facts):
            # Populate dropdown filter menu for fict_fact
            fict_fact = lines[line]["fict_fact"]
            all_fict_facts.append(fict_fact)


        # Query all art_other categories
        lines = db.execute("SELECT art_other FROM art_others")
        # Create list of items to be displayed
        all_art_others = []
        line = 0
        nb_art_others = len(lines)

        # Store "Select..." as default dropdown option
        art_other = "Select..."
        all_art_others.append(art_other)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_art_others):
            # Populate dropdown filter menu for art_other
            art_other = lines[line]["art_other"]
            all_art_others.append(art_other)


        # Query all form categories
        lines = db.execute("SELECT form FROM forms")
        # Create list of items to be displayed
        all_forms = []
        line = 0
        nb_forms = len(lines)

        # Store "Select..." as default dropdown option
        form = "Select..."
        all_forms.append(form)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_forms):
            # Populate dropdown filter menu for form
            form = lines[line]["form"]
            all_forms.append(form)


        # Query all content categories
        lines = db.execute("SELECT content FROM contents")
        # Create list of items to be displayed
        all_contents = []
        line = 0
        nb_contents = len(lines)

        # Store "Select..." as default dropdown option
        content = "Select..."
        all_contents.append(content)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_contents):
            # Populate dropdown filter menu for content
            content = lines[line]["content"]
            all_contents.append(content)


        # Display all books
        # rows = db.execute("SELECT * FROM books WHERE title = :title", title="The Great Gatsby")
        # rows = db.execute("SELECT * FROM books WHERE sect_name_id = :sect_name_id", sect_name_id=26)
        rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                        authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                        languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                        forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE author LIKE :author", author='%Rudolf%')
        # rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
        #                   authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
        #                   languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
        #                   forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id")


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
        items = len(rows)
        # items = 5

        # Iterate over all selected rows to populate template table with variable values
        for row in range(items):

            # Populate list with sector
            sector = rows[row]["sector"]
            sectors.append(sector)

            # Populate list with new_sector
            new_sector = rows[row]["new_sector"]
            new_sectors.append(new_sector)

            # Query sector_name
            sector_name = rows[row]["sector_name"]
            sector_names.append(sector_name)

            # Query author
            author = rows[row]["author"]
            authors.append(author)

            # Query title
            title = rows[row]["title"]
            titles.append(title)

            # Query edition
            edition = rows[row]["edition"]
            editions.append(edition)

            # Query firstY
            firstY = rows[row]["firstY"]
            firstYs.append(firstY)

            # Query ourY
            ourY = rows[row]["ourY"]
            ourYs.append(ourY)

            # Query language
            language = rows[row]["language"]
            languages.append(language)

            # Query country
            country = rows[row]["country"]
            countries.append(country)

            # Populate list with fict_fact
            fict_fact = rows[row]["fict_fact"]
            fict_facts.append(fict_fact)

            # Query art_other
            art_other = rows[row]["art_other"]
            art_others.append(art_other)

            # Query form
            form = rows[row]["form"]
            forms.append(form)

            # Query content
            content = rows[row]["content"]
            contents.append(content)

            # Query comment
            comment = rows[row]["comment"]
            comments.append(comment)

        return render_template("admin.html", all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names, nb_sector_names=nb_sector_names,
                                all_editions=all_editions, nb_editions=nb_editions, all_languages=all_languages, nb_languages=nb_languages, all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts,
                                all_art_others=all_art_others, nb_art_others=nb_art_others, all_forms=all_forms, nb_forms=nb_forms, all_contents=all_contents, nb_contents=nb_contents, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors,
                                sector_names=sector_names, authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages,
                                countries=countries, fict_facts=fict_facts, art_others=art_others, forms=forms, contents=contents, comments=comments)


@app.route("/confirm", methods=["GET", "POST"])
# @login_required
def confirm():
    """Insert, update and delete books from database"""

    # User reached route via POST (as by submitting a form via POST)
    # if request.method == "POST":
    #     if request.form.get("add_new_book"):

    #     return render_template("confirm.html", action="insert")

    # User reached route via GET (as by clicking a link or via redirect)
    # else:

        # if request.form.get("add_new_book"):
    return render_template("confirm.html", action=request.form.get("add_new_book"))

        # else:
        #     return render_template("confirm.html", action="problem")

@app.route("/", methods=["GET", "POST"])
# @login_required
def index():
    """Show main database"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query all sector categories
        lines = db.execute("SELECT sector FROM sectors")
        # Create list of items to be displayed
        all_sectors = []
        line = 0
        nb_sectors = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("sector") and request.form.get("sector") != "Select...":
            sector = request.form.get("sector")
            all_sectors.append(sector)

        # Store "Select..." as default dropdown option
        sector = "Select..."
        all_sectors.append(sector)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_sectors):
            # Populate dropdown filter menu for sector
            sector = lines[line]["sector"]
            all_sectors.append(sector)


        # Query all new_sector categories
        lines = db.execute("SELECT new_sector FROM new_sectors")
        # Create list of items to be displayed
        all_new_sectors = []
        line = 0
        nb_new_sectors = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("new_sector") and request.form.get("new_sector") != "Select...":
            new_sector = request.form.get("new_sector")
            all_new_sectors.append(new_sector)

        # Store "Select..." as default dropdown option
        new_sector = "Select..."
        all_new_sectors.append(new_sector)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_new_sectors):
            # Populate dropdown filter menu for new_sector
            new_sector = lines[line]["new_sector"]
            all_new_sectors.append(new_sector)


        # Query all sector_name categories
        lines = db.execute("SELECT sector_name FROM sector_names")
        # Create list of items to be displayed
        all_sector_names = []
        line = 0
        nb_sector_names = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("sector_name") and request.form.get("sector_name") != "Select...":
            sector_name = request.form.get("sector_name")
            all_sector_names.append(sector_name)

        # Store "Select..." as default dropdown option
        sector_name = "Select..."
        all_sector_names.append(sector_name)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_sector_names):
            # Populate dropdown filter menu for sector_name
            sector_name = lines[line]["sector_name"]
            all_sector_names.append(sector_name)


        # Query all edition categories
        lines = db.execute("SELECT edition FROM editions")
        # Create list of items to be displayed
        all_editions = []
        line = 0
        nb_editions = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("edition") and request.form.get("edition") != "Select...":
            edition = request.form.get("edition")
            all_editions.append(edition)

        # Store "Select..." as default dropdown option
        edition = "Select..."
        all_editions.append(edition)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_editions):
            # Populate dropdown filter menu for edition
            edition = lines[line]["edition"]
            all_editions.append(edition)


        # Query all language categories
        lines = db.execute("SELECT language FROM languages")
        # Create list of items to be displayed
        all_languages = []
        line = 0
        nb_languages = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("language") and request.form.get("language") != "Select...":
            language = request.form.get("language")
            all_languages.append(language)

        # Store "Select..." as default dropdown option
        language = "Select..."
        all_languages.append(language)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_languages):
            # Populate dropdown filter menu for language
            language = lines[line]["language"]
            all_languages.append(language)


        # Query all country categories
        lines = db.execute("SELECT country FROM countries")
        # Create list of items to be displayed
        all_countries = []
        line = 0
        nb_countries = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("country") and request.form.get("country") != "Select...":
            country = request.form.get("country")
            all_countries.append(country)

        # Store "Select..." as default dropdown option
        country = "Select..."
        all_countries.append(country)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_countries):
            # Populate dropdown filter menu for country
            country = lines[line]["country"]
            all_countries.append(country)


        # Query all fict_fact categories
        lines = db.execute("SELECT fict_fact FROM fict_facts")
        # Create list of items to be displayed
        all_fict_facts = []
        line = 0
        nb_fict_facts = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("fict_fact") and request.form.get("fict_fact") != "Select...":
            fict_fact = request.form.get("fict_fact")
            all_fict_facts.append(fict_fact)

        # Store "Select..." as default dropdown option
        fict_fact = "Select..."
        all_fict_facts.append(fict_fact)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_fict_facts):
            # Populate dropdown filter menu for fict_fact
            fict_fact = lines[line]["fict_fact"]
            all_fict_facts.append(fict_fact)


        # Query all art_other categories
        lines = db.execute("SELECT art_other FROM art_others")
        # Create list of items to be displayed
        all_art_others = []
        line = 0
        nb_art_others = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("art_other") and request.form.get("art_other") != "Select...":
            art_other = request.form.get("art_other")
            all_art_others.append(art_other)

        # Store "Select..." as default dropdown option
        art_other = "Select..."
        all_art_others.append(art_other)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_art_others):
            # Populate dropdown filter menu for art_other
            art_other = lines[line]["art_other"]
            all_art_others.append(art_other)


        # Query all form categories
        lines = db.execute("SELECT form FROM forms")
        # Create list of items to be displayed
        all_forms = []
        line = 0
        nb_forms = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("form") and request.form.get("form") != "Select...":
            form = request.form.get("form")
            all_forms.append(form)

        # Store "Select..." as default dropdown option
        form = "Select..."
        all_forms.append(form)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_forms):
            # Populate dropdown filter menu for form
            form = lines[line]["form"]
            all_forms.append(form)


        # Query all content categories
        lines = db.execute("SELECT content FROM contents")
        # Create list of items to be displayed
        all_contents = []
        line = 0
        nb_contents = len(lines)

        # If selection was made, keep the selected option as default
        if request.form.get("content") and request.form.get("content") != "Select...":
            content = request.form.get("content")
            all_contents.append(content)

        # Store "Select..." as default dropdown option
        content = "Select..."
        all_contents.append(content)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_contents):
            # Populate dropdown filter menu for content
            content = lines[line]["content"]
            all_contents.append(content)


        # Convert filtered parameters to be used in query
        if request.form.get("sector") == "":
            sector = ""
        elif request.form.get("sector") == "Select...":
            sector = "%"
        else:
            sector = "%" + request.form.get("sector") + "%"

        if request.form.get("new_sector") == "":
            new_sector = ""
        elif request.form.get("new_sector") == "Select...":
            new_sector = "%"
        else:
            new_sector = "%" + request.form.get("new_sector") + "%"

        if request.form.get("sector_name") == "":
            sector_name = ""
        elif request.form.get("sector_name") == "Select...":
            sector_name = "%"
        else:
            sector_name = "%" + request.form.get("sector_name") + "%"

        if request.form.get("author") == " ":
            author = ""
        elif request.form.get("author") == "Select...":
            author = "%"
        else:
            author = "%" + request.form.get("author") + "%"

        # Title field cannot be blank (but can be not filtered)
        if request.form.get("title") == "Select...":
            title = "%"
        else:
            title = "%" + request.form.get("title") + "%"

        if request.form.get("edition") == "":
            edition = ""
        elif request.form.get("edition") == "Select...":
            edition = "%"
        else:
            edition = "%" + request.form.get("edition") + "%"

        if request.form.get("firstY") == " ":
            firstY = ""
        elif request.form.get("firstY") == "Select...":
            firstY = "%"
        else:
            firstY = "%" + request.form.get("firstY") + "%"

        if request.form.get("ourY") == " ":
            ourY = ""
        elif request.form.get("ourY") == "Select...":
            ourY = "%"
        else:
            ourY = "%" + request.form.get("ourY") + "%"

        if request.form.get("language") == "":
            language = ""
        elif request.form.get("language") == "Select...":
            language = "%"
        else:
            language = "%" + request.form.get("language") + "%"

        if request.form.get("country") == "":
            country = ""
        elif request.form.get("country") == "Select...":
            country = "%"
        else:
            country = "%" + request.form.get("country") + "%"

        if request.form.get("fict_fact") == "":
            fict_fact = ""
        elif request.form.get("fict_fact") == "Select...":
            fict_fact = "%"
        else:
            fict_fact = "%" + request.form.get("fict_fact") + "%"

        if request.form.get("art_other") == "":
            art_other = ""
        elif request.form.get("art_other") == "Select...":
            art_other = "%"
        else:
            art_other = "%" + request.form.get("art_other") + "%"

        if request.form.get("form") == "":
            form = ""
        elif request.form.get("form") == "Select...":
            form = "%"
        else:
            form = "%" + request.form.get("form") + "%"

        if request.form.get("content") == "":
            content = ""
        elif request.form.get("content") == "Select...":
            content = "%"
        else:
            content = "%" + request.form.get("content") + "%"

        if request.form.get("comment") == " ":
            comment = ""
        elif request.form.get("comment") == "Select...":
            comment = "%"
        else:
            comment = "%" + request.form.get("comment") + "%"


        # Query books by filter parameters
        rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                           authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                           languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                           forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE sector LIKE :sector AND new_sector LIKE :new_sector AND \
                           sector_name LIKE :sector_name AND author LIKE :author AND title LIKE :title AND edition LIKE :edition AND firstY LIKE :firstY AND ourY LIKE :ourY AND language LIKE :language AND country LIKE :country AND fict_fact LIKE :fict_fact AND \
                           art_other LIKE :art_other AND form LIKE :form AND content LIKE :content AND comment LIKE :comment", sector=sector, new_sector=new_sector, sector_name=sector_name, author=author, title=title, edition=edition,
                           firstY=firstY, ourY=ourY, language=language, country=country, fict_fact=fict_fact, art_other=art_other, form=form, content=content, comment=comment)
        # rows = db.execute("SELECT * FROM books WHERE sector = :sector AND new_sector = :new_sector AND sector_name = :sector_name AND author = :author AND title = :title AND edition = :edition AND firstY = :firstY AND ourY = :ourY \
        #                    AND language = :language AND country = :country AND fict_fact = :fict_fact AND art_other = :art_other AND form = :form AND content = :content AND comment = :comment",
        #                   sector=request.form.get("sector"), new_sector=request.form.get("new_sector"), sector_name=request.form.get("sector_name"), author=request.form.get("author"), title=request.form.get("title"), edition=request.form.get("edition"),
        #                   firstY=request.form.get("firstY"), ourY=request.form.get("ourY"), language=request.form.get("language"), country=request.form.get("country"), fict_fact=request.form.get("fict_fact"), art_other=request.form.get("art_other"),
        #                   form=request.form.get("form"), content=request.form.get("content"), comment=request.form.get("comment"))

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
        items = len(rows)
        # items = 20

        # Iterate over all selected rows to populate template table with variable values
        for row in range(items):

            # Populate list with sector
            sector = rows[row]["sector"]
            sectors.append(sector)

            # Populate list with new_sector
            new_sector = rows[row]["new_sector"]
            new_sectors.append(new_sector)

            # Query sector_name
            sector_name = rows[row]["sector_name"]
            sector_names.append(sector_name)

            # Query author
            author = rows[row]["author"]
            authors.append(author)

            # Query title
            title = rows[row]["title"]
            titles.append(title)

            # Query edition
            edition = rows[row]["edition"]
            editions.append(edition)

            # Query firstY
            firstY = rows[row]["firstY"]
            firstYs.append(firstY)

            # Query ourY
            ourY = rows[row]["ourY"]
            ourYs.append(ourY)

            # Query language
            language = rows[row]["language"]
            languages.append(language)

            # Query country
            country = rows[row]["country"]
            countries.append(country)

            # Populate list with fict_fact
            # lines = db.execute("SELECT fict_fact FROM fict_facts WHERE fict_id = :fict_id", fict_id=rows[row]["fict_fact"])
            fict_fact = rows[row]["fict_fact"]
            fict_facts.append(fict_fact)

            # Query art_other
            art_other = rows[row]["art_other"]
            art_others.append(art_other)

            # Query form
            form = rows[row]["form"]
            forms.append(form)

            # Query content
            content = rows[row]["content"]
            contents.append(content)

            # Query comment
            comment = rows[row]["comment"]
            comments.append(comment)


            # Store selected value to be displyed in Filter field after page refresh
            old_sector = request.form.get("sector")





        return render_template("index.html", old_sector=request.form.get('sector'), all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names, nb_sector_names=nb_sector_names,
                                all_editions=all_editions, nb_editions=nb_editions, all_languages=all_languages, nb_languages=nb_languages, all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts,
                                all_art_others=all_art_others, nb_art_others=nb_art_others, all_forms=all_forms, nb_forms=nb_forms, all_contents=all_contents, nb_contents=nb_contents, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors, sector_names=sector_names, authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages,
                                countries=countries, fict_facts=fict_facts, art_others=art_others, forms=forms, contents=contents, comments=comments)

    # Display which user's portfolio is displayed
    # rows = db.execute("SELECT username FROM users WHERE user_id = :user_id", user_id=session["user_id"])
    # user = rows[0]["username"]

    # Select all companies in user's portfolio with non-zero total amount of shares
    # rows = db.execute("SELECT symbol, SUM(total), SUM(number) FROM history WHERE id = :id GROUP BY symbol HAVING SUM(number) > 0",
    #                   id=session["user_id"])


    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Query all sector categories
        lines = db.execute("SELECT sector FROM sectors")
        # Create list of items to be displayed
        all_sectors = []
        line = 0
        nb_sectors = len(lines)

        # Store "Select..." as default dropdown option
        sector = "Select..."
        all_sectors.append(sector)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_sectors):
            # Populate dropdown filter menu for sector
            sector = lines[line]["sector"]
            all_sectors.append(sector)


        # Query all new_sector categories
        lines = db.execute("SELECT new_sector FROM new_sectors")
        # Create list of items to be displayed
        all_new_sectors = []
        line = 0
        nb_new_sectors = len(lines)

        # Store "Select..." as default dropdown option
        new_sector = "Select..."
        all_new_sectors.append(new_sector)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_new_sectors):
            # Populate dropdown filter menu for sector
            new_sector = lines[line]["new_sector"]
            all_new_sectors.append(new_sector)


        # Query all sector_name categories
        lines = db.execute("SELECT sector_name FROM sector_names")
        # Create list of items to be displayed
        all_sector_names = []
        line = 0
        nb_sector_names = len(lines)

        # Store "Select..." as default dropdown option
        sector_name = "Select..."
        all_sector_names.append(sector_name)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_sector_names):
            # Populate dropdown filter menu for sector
            sector_name = lines[line]["sector_name"]
            all_sector_names.append(sector_name)


        # Query all edition categories
        lines = db.execute("SELECT edition FROM editions")
        # Create list of items to be displayed
        all_editions = []
        line = 0
        nb_editions = len(lines)

        # Store "Select..." as default dropdown option
        edition = "Select..."
        all_editions.append(edition)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_editions):
            # Populate dropdown filter menu for sector
            edition = lines[line]["edition"]
            all_editions.append(edition)


        # Query all language categories
        lines = db.execute("SELECT language FROM languages")
        # Create list of items to be displayed
        all_languages = []
        line = 0
        nb_languages = len(lines)

        # Store "Select..." as default dropdown option
        language = "Select..."
        all_languages.append(language)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_languages):
            # Populate dropdown filter menu for language
            language = lines[line]["language"]
            all_languages.append(language)


        # Query all country categories
        lines = db.execute("SELECT country FROM countries")
        # Create list of items to be displayed
        all_countries = []
        line = 0
        nb_countries = len(lines)

        # Store "Select..." as default dropdown option
        country = "Select..."
        all_countries.append(country)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_countries):
            # Populate dropdown filter menu for country
            country = lines[line]["country"]
            all_countries.append(country)


        # Query all fict_fact categories
        lines = db.execute("SELECT fict_fact FROM fict_facts")
        # Create list of items to be displayed
        all_fict_facts = []
        line = 0
        nb_fict_facts = len(lines)

        # Store "Select..." as default dropdown option
        fict_fact = "Select..."
        all_fict_facts.append(fict_fact)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_fict_facts):
            # Populate dropdown filter menu for fict_fact
            fict_fact = lines[line]["fict_fact"]
            all_fict_facts.append(fict_fact)


        # Query all art_other categories
        lines = db.execute("SELECT art_other FROM art_others")
        # Create list of items to be displayed
        all_art_others = []
        line = 0
        nb_art_others = len(lines)

        # Store "Select..." as default dropdown option
        art_other = "Select..."
        all_art_others.append(art_other)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_art_others):
            # Populate dropdown filter menu for art_other
            art_other = lines[line]["art_other"]
            all_art_others.append(art_other)


        # Query all form categories
        lines = db.execute("SELECT form FROM forms")
        # Create list of items to be displayed
        all_forms = []
        line = 0
        nb_forms = len(lines)

        # Store "Select..." as default dropdown option
        form = "Select..."
        all_forms.append(form)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_forms):
            # Populate dropdown filter menu for form
            form = lines[line]["form"]
            all_forms.append(form)


        # Query all content categories
        lines = db.execute("SELECT content FROM contents")
        # Create list of items to be displayed
        all_contents = []
        line = 0
        nb_contents = len(lines)

        # Store "Select..." as default dropdown option
        content = "Select..."
        all_contents.append(content)

        # Iterate over all selected rows to populate template table with all categories
        for line in range(nb_contents):
            # Populate dropdown filter menu for content
            content = lines[line]["content"]
            all_contents.append(content)


        # Display all books
        # rows = db.execute("SELECT * FROM books WHERE title = :title", title="The Great Gatsby")
        # rows = db.execute("SELECT * FROM books WHERE sect_name_id = :sect_name_id", sect_name_id=26)
        rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                       authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                       languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                       forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE author LIKE :author", author='%Rudolf%')
        # rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
        #                   authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
        #                   languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
        #                   forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id")


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
        items = len(rows)
        # items = 5

        # Iterate over all selected rows to populate template table with variable values
        for row in range(items):

            # Populate list with sector
            sector = rows[row]["sector"]
            sectors.append(sector)

            # Populate list with new_sector
            new_sector = rows[row]["new_sector"]
            new_sectors.append(new_sector)

            # Query sector_name
            sector_name = rows[row]["sector_name"]
            sector_names.append(sector_name)

            # Query author
            author = rows[row]["author"]
            authors.append(author)

            # Query title
            title = rows[row]["title"]
            titles.append(title)

            # Query edition
            edition = rows[row]["edition"]
            editions.append(edition)

            # Query firstY
            firstY = rows[row]["firstY"]
            firstYs.append(firstY)

            # Query ourY
            ourY = rows[row]["ourY"]
            ourYs.append(ourY)

            # Query language
            language = rows[row]["language"]
            languages.append(language)

            # Query country
            country = rows[row]["country"]
            countries.append(country)

            # Populate list with fict_fact
            fict_fact = rows[row]["fict_fact"]
            fict_facts.append(fict_fact)

            # Query art_other
            art_other = rows[row]["art_other"]
            art_others.append(art_other)

            # Query form
            form = rows[row]["form"]
            forms.append(form)

            # Query content
            content = rows[row]["content"]
            contents.append(content)

            # Query comment
            comment = rows[row]["comment"]
            comments.append(comment)

        return render_template("index.html", all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names, nb_sector_names=nb_sector_names,
                                all_editions=all_editions, nb_editions=nb_editions, all_languages=all_languages, nb_languages=nb_languages, all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts,
                                all_art_others=all_art_others, nb_art_others=nb_art_others, all_forms=all_forms, nb_forms=nb_forms, all_contents=all_contents, nb_contents=nb_contents, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors,
                                sector_names=sector_names, authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages,
                                countries=countries, fict_facts=fict_facts, art_others=art_others, forms=forms, contents=contents, comments=comments)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Insert, update and delete books from database"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure title submitted
        if not request.form.get("title"):
            return apology("must provide title", 403)

        # Ensure user provided valid stock symbol
        if not lookup(request.form.get("symbol")):
            return apology("must provide valid stock symbol", 403)

        # Ensure number of shares submitted
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 403)

        # Store number of shares in a variable
        number = request.form.get("shares")

        # Ensure user provided positive integer
        if not number.isdigit():
            return apology("must provide positive integer", 403)

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
            return apology("you don't have enough cash", 403)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


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
