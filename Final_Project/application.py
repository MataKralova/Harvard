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
app.debug = True

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")

# Allow access to these Insert or Edit top-of-page dropdown values when user clicks "Confirm" button
ins_sector = ""
ins_new_sector = ""
ins_sector_name = ""
ins_author = ""
ins_title = ""
ins_edition = ""
ins_firstY = ""
ins_ourY = ""
ins_language = ""
ins_country = ""
ins_fict_fact = ""
ins_art_other = ""
ins_form = ""
ins_content = ""
ins_comment = ""

# Allow access to these Search mid-page dropdown values when user clicks Edit
s_sector = ""
s_new_sector = ""
s_sector_name = ""
s_author = ""
s_title = ""
s_edition = ""
s_firstY = ""
s_ourY = ""
s_language = ""
s_country = ""
s_fict_fact = ""
s_art_other = ""
s_form = ""
s_content =""
s_comment = ""

# Allow access to these Search mid-page dropdown values when user clicks Edit
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

ins_all_sectors = []
ins_all_new_sectors = []
ins_all_sector_names = []
ins_all_editions = []
ins_all_languages = []
ins_all_countries = []
ins_all_fict_facts = []
ins_all_art_others = []
ins_all_forms = []
ins_all_contents = []

ins_nb_sectors = 0
ins_nb_new_sectors = 0
ins_nb_sector_names = 0
ins_nb_editions = 0
ins_nb_languages = 0
ins_nb_countries = 0
ins_nb_fict_facts = 0
ins_nb_art_others = 0
ins_nb_forms = 0
ins_nb_contents = 0

all_sectors = []
all_new_sectors = []
all_sector_names = []
all_editions = []
all_languages = []
all_countries = []
all_fict_facts = []
all_art_others = []
all_forms = []
all_contents = []

nb_sectors = 0
nb_new_sectors = 0
nb_sector_names = 0
nb_editions = 0
nb_languages = 0
nb_countries = 0
nb_fict_facts = 0
nb_art_others = 0
nb_forms = 0
nb_contents = 0

items = 0
rows = 0
ids = []
row = 0
book_id = 0

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """Insert, update and delete books from database"""

    # Allow access to these Insert or Edit top-of-page dropdown values when user clicks "Confirm" button
    global ins_sector
    global ins_new_sector
    global ins_sector_name
    global ins_author
    global ins_title
    global ins_edition
    global ins_firstY
    global ins_ourY
    global ins_language
    global ins_country
    global ins_fict_fact
    global ins_art_other
    global ins_form
    global ins_content
    global ins_comment

    global s_sector
    global s_new_sector
    global s_sector_name
    global s_author
    global s_title
    global s_edition
    global s_firstY
    global s_ourY
    global s_language
    global s_country
    global s_fict_fact
    global s_art_other
    global s_form
    global s_content
    global s_comment

    global sector
    global new_sector
    global sector_name
    global author
    global title
    global edition
    global firstY
    global ourY
    global language
    global country
    global fict_fact
    global art_other
    global form
    global content
    global comment

    global sectors
    global new_sectors
    global sector_names
    global authors
    global titles
    global editions
    global firstYs
    global ourYs
    global languages
    global countries
    global fict_facts
    global art_others
    global forms
    global contents
    global comments

    global ins_all_sectors
    global ins_all_new_sectors
    global ins_all_sector_names
    global ins_all_editions
    global ins_all_languages
    global ins_all_countries
    global ins_all_fict_facts
    global ins_all_art_others
    global ins_all_forms
    global ins_all_contents

    global ins_nb_sectors
    global ins_nb_new_sectors
    global ins_nb_sector_names
    global ins_nb_editions
    global ins_nb_languages
    global ins_nb_countries
    global ins_nb_fict_facts
    global ins_nb_art_others
    global ins_nb_forms
    global ins_nb_contents

    global all_sectors
    global all_new_sectors
    global all_sector_names
    global all_editions
    global all_languages
    global all_countries
    global all_fict_facts
    global all_art_others
    global all_forms
    global all_contents

    global nb_sectors
    global nb_new_sectors
    global nb_sector_names
    global nb_editions
    global nb_languages
    global nb_countries
    global nb_fict_facts
    global nb_art_others
    global nb_forms
    global nb_contents

    global items
    global rows
    global ids
    global row
    global book_id

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # User clicked on "Insert" button
        if request.form.get("insert"):


            # Populate data items to be shown for confirmation
            ins_sector = request.form.get("ins_sector")
            if request.form.get("ins_sector") == "Select...":
                ins_sector = ""

            ins_new_sector = request.form.get("ins_new_sector")
            if request.form.get("ins_new_sector") == "Select...":
                ins_new_sector = ""

            ins_sector_name = request.form.get("ins_sector_name")
            if request.form.get("ins_sector_name") == "Select...":
                ins_sector_name = ""

            ins_author = request.form.get("ins_author")
            if request.form.get("ins_author") == "Select...":
                ins_author = ""

            ins_title = request.form.get("ins_title")
            if request.form.get("ins_title") == "Select...":
                ins_title = ""

            ins_edition = request.form.get("ins_edition")
            if request.form.get("ins_edition") == "Select...":
                ins_edition = ""

            ins_firstY = request.form.get("ins_firstY")
            if request.form.get("ins_firstY") == "Select...":
                ins_firstY = ""

            ins_ourY = request.form.get("ins_ourY")
            if request.form.get("ins_ourY") == "Select...":
                ins_ourY = ""

            ins_language = request.form.get("ins_language")
            if request.form.get("ins_language") == "Select...":
                ins_language = ""

            ins_country = request.form.get("ins_country")
            if request.form.get("ins_country") == "Select...":
                ins_country = ""

            ins_fict_fact = request.form.get("ins_fict_fact")
            if request.form.get("ins_fict_fact") == "Select...":
                ins_fict_fact = ""

            ins_art_other = request.form.get("ins_art_other")
            if request.form.get("ins_art_other") == "Select...":
                ins_art_other = ""

            ins_form = request.form.get("ins_form")
            if request.form.get("ins_form") == "Select...":
                ins_form = ""

            ins_content = request.form.get("ins_content")
            if request.form.get("ins_content") == "Select...":
                ins_content = ""

            ins_comment = request.form.get("ins_comment")
            if request.form.get("ins_comment") == "Select...":
                ins_comment = ""

            return render_template("confirm.html", wording="INSERT into", action="inserted", ins_sector=ins_sector, ins_new_sector=ins_new_sector, ins_sector_name=ins_sector_name, ins_author=ins_author, ins_title=ins_title,
                                ins_edition=ins_edition, ins_firstY=ins_firstY, ins_ourY=ins_ourY, ins_language=ins_language, ins_country=ins_country, ins_fict_fact=ins_fict_fact, ins_art_other=ins_art_other,
                                ins_form=ins_form, ins_content=ins_content, ins_comment=ins_comment)

        # User clicked on "Edit" button to make changes
        if request.form.get("edit"):

            book_id = request.form.get("book_id")

            # Get all fields of book selected for editing
            lignes = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                               authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                               languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                               forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE book_id = :book_id", book_id=book_id)

            # Store fields that are input and not dropdown
            ins_author = lignes[0]["author"]
            ins_title = lignes[0]["title"]
            ins_firstY = lignes[0]["firstY"]
            ins_ourY = lignes[0]["ourY"]
            ins_comment = lignes[0]["comment"]

            # Get all existing sector categories
            lines = db.execute("SELECT sector FROM sectors")
            # Create list of dropdown menu options
            ins_all_sectors = []
            line = 0
            nb = len(lines)
            ins_nb_sectors = nb + 0         # in case of Edit, we don't want to store "Select..." as option
            # Populate dropdown menu for sector
            for line in range(nb):
                ins_sector = lines[line]["sector"]
                ins_all_sectors.append(ins_sector)
            # Sort options and store in temporary sorted list
            ins_all_sectors.sort()
            sorted_ins_all_sectors = ins_all_sectors
            ins_all_sectors = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_sector = lignes[0]["sector"]
            if ins_sector != "":
                ins_all_sectors.append(ins_sector)
                ins_nb_sectors = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_sector = sorted_ins_all_sectors[line]
                ins_all_sectors.append(ins_sector)

            # Get all existing new_sector categories
            lines = db.execute("SELECT new_sector FROM new_sectors")
            # Create list of dropdown menu options
            ins_all_new_sectors = []
            line = 0
            nb = len(lines)
            ins_nb_new_sectors = nb + 0
            # Populate dropdown menu for new_sector
            for line in range(nb):
                ins_new_sector = lines[line]["new_sector"]
                ins_all_new_sectors.append(ins_new_sector)
            # Sort options and store in temporary sorted list
            ins_all_new_sectors.sort()
            sorted_ins_all_new_sectors = ins_all_new_sectors
            ins_all_new_sectors = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_new_sector = lignes[0]["new_sector"]
            if ins_new_sector != "":
                ins_all_new_sectors.append(ins_new_sector)
                ins_nb_new_sectors = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_new_sector = sorted_ins_all_new_sectors[line]
                ins_all_new_sectors.append(ins_new_sector)

            # Get all existing sector_name categories
            lines = db.execute("SELECT sector_name FROM sector_names")
            # Create list of dropdown menu options
            ins_all_sector_names = []
            line = 0
            nb = len(lines)
            ins_nb_sector_names = nb + 0
            # Populate dropdown menu for sector_name
            for line in range(nb):
                ins_sector_name = lines[line]["sector_name"]
                ins_all_sector_names.append(ins_sector_name)
            # Sort options and store in temporary sorted list
            ins_all_sector_names.sort()
            sorted_ins_all_sector_names = ins_all_sector_names
            ins_all_sector_names = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_sector_name = lignes[0]["sector_name"]
            if ins_sector_name != "":
                ins_all_sector_names.append(ins_sector_name)
                ins_nb_sector_names = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_sector_name = sorted_ins_all_sector_names[line]
                ins_all_sector_names.append(ins_sector_name)

            # Get all existing edition categories
            lines = db.execute("SELECT edition FROM editions")
            # Create list of dropdown menu options
            ins_all_editions = []
            line = 0
            nb = len(lines)
            ins_nb_editions = nb + 0
            # Populate dropdown menu for edition
            for line in range(nb):
                ins_edition = lines[line]["edition"]
                ins_all_editions.append(ins_edition)
            # Sort options and store in temporary sorted list
            ins_all_editions.sort()
            sorted_ins_all_editions = ins_all_editions
            ins_all_editions = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_edition = lignes[0]["edition"]
            if ins_edition != "":
                ins_all_editions.append(ins_edition)
                ins_nb_editions = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_edition = sorted_ins_all_editions[line]
                ins_all_editions.append(ins_edition)

            # Get all existing language categories
            lines = db.execute("SELECT language FROM languages")
            # Create list of dropdown menu options
            ins_all_languages = []
            line = 0
            nb = len(lines)
            ins_nb_languages = nb + 0
            # Populate dropdown menu for language
            for line in range(nb):
                ins_language = lines[line]["language"]
                ins_all_languages.append(ins_language)
            # Sort options and store in temporary sorted list
            ins_all_languages.sort()
            sorted_ins_all_languages = ins_all_languages
            ins_all_languages = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_language = lignes[0]["language"]
            if ins_language != "":
                ins_all_languages.append(ins_language)
                ins_nb_languages = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_language = sorted_ins_all_languages[line]
                ins_all_languages.append(ins_language)

            # Get all existing country categories
            lines = db.execute("SELECT country FROM countries")
            # Create list of dropdown menu options
            ins_all_countries = []
            line = 0
            nb = len(lines)
            ins_nb_countries = nb + 0
            # Populate dropdown menu for country
            for line in range(nb):
                ins_country = lines[line]["country"]
                ins_all_countries.append(ins_country)
            # Sort options and store in temporary sorted list
            ins_all_countries.sort()
            sorted_ins_all_countries = ins_all_countries
            ins_all_countries = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_country = lignes[0]["country"]
            if ins_country != "":
                ins_all_countries.append(ins_country)
                ins_nb_countries = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_country = sorted_ins_all_countries[line]
                ins_all_countries.append(ins_country)

            # Get all existing fict_fact categories
            lines = db.execute("SELECT fict_fact FROM fict_facts")
            # Create list of dropdown menu options
            ins_all_fict_facts = []
            line = 0
            nb = len(lines)
            ins_nb_fict_facts = nb + 0
            # Populate dropdown menu for fict_fact
            for line in range(nb):
                ins_fict_fact = lines[line]["fict_fact"]
                ins_all_fict_facts.append(ins_fict_fact)
            # Sort options and store in temporary sorted list
            ins_all_fict_facts.sort()
            sorted_ins_all_fict_facts = ins_all_fict_facts
            ins_all_fict_facts = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_fict_fact = lignes[0]["fict_fact"]
            if ins_fict_fact != "":
                ins_all_fict_facts.append(ins_fict_fact)
                ins_nb_fict_facts = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_fict_fact = sorted_ins_all_fict_facts[line]
                ins_all_fict_facts.append(ins_fict_fact)

            # Get all existing art_other categories
            lines = db.execute("SELECT art_other FROM art_others")
            # Create list of dropdown menu options
            ins_all_art_others = []
            line = 0
            nb = len(lines)
            ins_nb_art_others = nb + 0
            # Populate dropdown menu for art_other
            for line in range(nb):
                ins_art_other = lines[line]["art_other"]
                ins_all_art_others.append(ins_art_other)
            # Sort options and store in temporary sorted list
            ins_all_art_others.sort()
            sorted_ins_all_art_others = ins_all_art_others
            ins_all_art_others = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_art_other = lignes[0]["art_other"]
            if ins_art_other != "":
                ins_all_art_others.append(ins_art_other)
                ins_nb_art_others = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_art_other = sorted_ins_all_art_others[line]
                ins_all_art_others.append(ins_art_other)

            # Get all existing form categories
            lines = db.execute("SELECT form FROM forms")
            # Create list of dropdown menu options
            ins_all_forms = []
            line = 0
            nb = len(lines)
            ins_nb_forms = nb + 0
            # Populate dropdown menu for form
            for line in range(nb):
                ins_form = lines[line]["form"]
                ins_all_forms.append(ins_form)
            # Sort options and store in temporary sorted list
            ins_all_forms.sort()
            sorted_ins_all_forms = ins_all_forms
            ins_all_forms = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_form = lignes[0]["form"]
            if ins_form != "":
                ins_all_forms.append(ins_form)
                ins_nb_forms = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_form = sorted_ins_all_forms[line]
                ins_all_forms.append(ins_form)

            # Get all existing content categories
            lines = db.execute("SELECT content FROM contents")
            # Create list of dropdown menu options
            ins_all_contents = []
            line = 0
            nb = len(lines)
            ins_nb_contents = nb + 0
            # Populate dropdown menu for content
            for line in range(nb):
                ins_content = lines[line]["content"]
                ins_all_contents.append(ins_content)
            # Sort options and store in temporary sorted list
            ins_all_contents.sort()
            sorted_ins_all_contents = ins_all_contents
            ins_all_contents = []
            # Keep selected book's data as default in Edit field (unless blank)
            ins_content = lignes[0]["content"]
            if ins_content != "":
                ins_all_contents.append(ins_content)
                ins_nb_contents = nb + 1
            # Re-populate so that selected book's data is first option and then sorted list
            for line in range(nb):
                ins_content = sorted_ins_all_contents[line]
                ins_all_contents.append(ins_content)

            return render_template("edit.html", wording="Edit", action="edit_submit", ins_author=ins_author, ins_title=ins_title, ins_firstY=ins_firstY, ins_ourY=ins_ourY, ins_comment=ins_comment, ins_all_sectors=ins_all_sectors,
                                ins_nb_sectors=ins_nb_sectors, ins_all_new_sectors=ins_all_new_sectors, ins_nb_new_sectors=ins_nb_new_sectors, ins_all_sector_names=ins_all_sector_names, ins_nb_sector_names=ins_nb_sector_names,
                                ins_all_editions=ins_all_editions, ins_nb_editions=ins_nb_editions, ins_all_languages=ins_all_languages, ins_nb_languages=ins_nb_languages, ins_all_countries=ins_all_countries,
                                ins_nb_countries=ins_nb_countries, ins_all_fict_facts=ins_all_fict_facts, ins_nb_fict_facts=ins_nb_fict_facts, ins_all_art_others=ins_all_art_others, ins_nb_art_others=ins_nb_art_others,
                                ins_all_forms=ins_all_forms, ins_nb_forms=ins_nb_forms, ins_all_contents=ins_all_contents, ins_nb_contents=ins_nb_contents, all_sectors=all_sectors, nb_sectors=nb_sectors,
                                all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names, nb_sector_names=nb_sector_names, s_author=s_author, s_title=s_title, all_editions=all_editions,
                                nb_editions=nb_editions, s_firstY=s_firstY, s_ourY=s_ourY, all_languages=all_languages, nb_languages=nb_languages, all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts,
                                nb_fict_facts=nb_fict_facts, all_art_others=all_art_others, nb_art_others=nb_art_others, all_forms=all_forms, nb_forms=nb_forms, all_contents=all_contents, nb_contents=nb_contents, s_comment=s_comment,
                                items=items, rows=rows, sectors=sectors, new_sectors=new_sectors, sector_names=sector_names, authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages,
                                countries=countries, fict_facts=fict_facts, art_others=art_others, forms=forms, contents=contents, comments=comments, ids=ids)

        # User clicked on "Delete" button to make changes
        if request.form.get("delete"):

            book_id = request.form.get("book_id")

            # Get all fields of book selected for editing
            lignes = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                               authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                               languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                               forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE book_id = :book_id", book_id=book_id)

            # There will be only 1 option for every Insert dropdown menu (the option valid for the selected book)
            line = 0

            # Store fields that are input and not dropdown
            ins_author = lignes[0]["author"]
            ins_title = lignes[0]["title"]
            ins_firstY = lignes[0]["firstY"]
            ins_ourY = lignes[0]["ourY"]
            ins_comment = lignes[0]["comment"]

            # Avoid displaying many blank options
            ins_nb_sectors = 1
            # Store selected value as the only value in dropdown
            ins_all_sectors = []
            ins_sector = lignes[0]["sector"]
            ins_all_sectors.append(ins_sector)

            # Avoid displaying many blank options
            ins_nb_new_sectors = 1
            # Store selected value as the only value in dropdown
            ins_all_new_sectors = []
            ins_new_sector = lignes[0]["new_sector"]
            ins_all_new_sectors.append(ins_new_sector)

            # Avoid displaying many blank options
            ins_nb_sector_names = 1
            # Store selected value as the only value in dropdown
            ins_all_sector_names = []
            ins_sector_name = lignes[0]["sector_name"]
            ins_all_sector_names.append(ins_sector_name)

            # Avoid displaying many blank options
            ins_nb_editions = 1
            # Store selected value as the only value in dropdown
            ins_all_editions = []
            ins_edition = lignes[0]["edition"]
            ins_all_editions.append(ins_edition)

            # Avoid displaying many blank options
            ins_nb_languages = 1
            # Store selected value as the only value in dropdown
            ins_all_languages = []
            ins_language = lignes[0]["language"]
            ins_all_languages.append(ins_language)

            # Avoid displaying many blank options
            ins_nb_countries = 1
            # Store selected value as the only value in dropdown
            ins_all_countries = []
            ins_country = lignes[0]["country"]
            ins_all_countries.append(ins_country)

            # Avoid displaying many blank options
            ins_nb_fict_facts = 1
            # Store selected value as the only value in dropdown
            ins_all_fict_facts = []
            ins_fict_fact = lignes[0]["fict_fact"]
            ins_all_fict_facts.append(ins_fict_fact)

            # Avoid displaying many blank options
            ins_nb_art_others = 1
            # Store selected value as the only value in dropdown
            ins_all_art_others = []
            ins_art_other = lignes[0]["art_other"]
            ins_all_art_others.append(ins_art_other)

            # Avoid displaying many blank options
            ins_nb_forms = 1
            # Store selected value as the only value in dropdown
            ins_all_forms = []
            ins_form = lignes[0]["form"]
            ins_all_forms.append(ins_form)

            # Avoid displaying many blank options
            ins_nb_contents = 1
            # Store selected value as the only value in dropdown
            ins_all_contents = []
            ins_content = lignes[0]["content"]
            ins_all_contents.append(ins_content)

            return render_template("edit.html", wording="Before DELETING, you can review the", action="delete_submit", ins_author=ins_author, ins_title=ins_title, ins_firstY=ins_firstY, ins_ourY=ins_ourY,
                    ins_comment=ins_comment, ins_all_sectors=ins_all_sectors, ins_nb_sectors=ins_nb_sectors, ins_all_new_sectors=ins_all_new_sectors, ins_nb_new_sectors=ins_nb_new_sectors, ins_all_sector_names=ins_all_sector_names,
                    ins_nb_sector_names=ins_nb_sector_names, ins_all_editions=ins_all_editions, ins_nb_editions=ins_nb_editions, ins_all_languages=ins_all_languages, ins_nb_languages=ins_nb_languages,
                    ins_all_countries=ins_all_countries, ins_nb_countries=ins_nb_countries, ins_all_fict_facts=ins_all_fict_facts, ins_nb_fict_facts=ins_nb_fict_facts, ins_all_art_others=ins_all_art_others,
                    ins_nb_art_others=ins_nb_art_others, ins_all_forms=ins_all_forms, ins_nb_forms=ins_nb_forms, ins_all_contents=ins_all_contents, ins_nb_contents=ins_nb_contents, all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names,
                    nb_sector_names=nb_sector_names, s_author=s_author, s_title=s_title, all_editions=all_editions, nb_editions=nb_editions, s_firstY=s_firstY, s_ourY=s_ourY, all_languages=all_languages, nb_languages=nb_languages, all_countries=all_countries,
                    nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts, all_art_others=all_art_others, nb_art_others=nb_art_others, all_forms=all_forms, nb_forms=nb_forms,
                    all_contents=all_contents, nb_contents=nb_contents, s_comment=s_comment, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors, sector_names=sector_names, authors=authors, titles=titles,
                    editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages, countries=countries, fict_facts=fict_facts, art_others=art_others, forms=forms, contents=contents, comments=comments, ids=ids)

        # User clicked on "Edit" button to submit changes
        if request.form.get("edit_submit"):

            # Populate data items to be shown for confirmation
            ins_sector = request.form.get("ins_sector")
            if request.form.get("ins_sector") == "Select...":
                ins_sector = ""

            ins_new_sector = request.form.get("ins_new_sector")
            if request.form.get("ins_new_sector") == "Select...":
                ins_new_sector = ""

            ins_sector_name = request.form.get("ins_sector_name")
            if request.form.get("ins_sector_name") == "Select...":
                ins_sector_name = ""

            ins_author = request.form.get("ins_author")
            if request.form.get("ins_author") == "Select...":
                ins_author = ""

            ins_title = request.form.get("ins_title")
            if request.form.get("ins_title") == "Select...":
                ins_title = ""

            ins_edition = request.form.get("ins_edition")
            if request.form.get("ins_edition") == "Select...":
                ins_edition = ""

            ins_firstY = request.form.get("ins_firstY")
            if request.form.get("ins_firstY") == "Select...":
                ins_firstY = ""

            ins_ourY = request.form.get("ins_ourY")
            if request.form.get("ins_ourY") == "Select...":
                ins_ourY = ""

            ins_language = request.form.get("ins_language")
            if request.form.get("ins_language") == "Select...":
                ins_language = ""

            ins_country = request.form.get("ins_country")
            if request.form.get("ins_country") == "Select...":
                ins_country = ""

            ins_fict_fact = request.form.get("ins_fict_fact")
            if request.form.get("ins_fict_fact") == "Select...":
                ins_fict_fact = ""

            ins_art_other = request.form.get("ins_art_other")
            if request.form.get("ins_art_other") == "Select...":
                ins_art_other = ""

            ins_form = request.form.get("ins_form")
            if request.form.get("ins_form") == "Select...":
                ins_form = ""

            ins_content = request.form.get("ins_content")
            if request.form.get("ins_content") == "Select...":
                ins_content = ""

            ins_comment = request.form.get("ins_comment")
            if request.form.get("ins_comment") == "Select...":
                ins_comment = ""

            return render_template("confirm.html", wording="MODIFY", wording2="with", action="edited", ins_sector=ins_sector, ins_new_sector=ins_new_sector, ins_sector_name=ins_sector_name, ins_author=ins_author, ins_title=ins_title,
                                ins_edition=ins_edition, ins_firstY=ins_firstY, ins_ourY=ins_ourY, ins_language=ins_language, ins_country=ins_country, ins_fict_fact=ins_fict_fact, ins_art_other=ins_art_other,
                                ins_form=ins_form, ins_content=ins_content, ins_comment=ins_comment)

        # User clicked on "Delete" button to submit changes
        if request.form.get("delete_submit"):

            # Populate data items to be shown for confirmation
            ins_sector = request.form.get("ins_sector")
            ins_new_sector = request.form.get("ins_new_sector")
            ins_sector_name = request.form.get("ins_sector_name")
            ins_author = request.form.get("ins_author")
            ins_title = request.form.get("ins_title")
            ins_edition = request.form.get("ins_edition")
            ins_firstY = request.form.get("ins_firstY")
            ins_ourY = request.form.get("ins_ourY")
            ins_language = request.form.get("ins_language")
            ins_country = request.form.get("ins_country")
            ins_fict_fact = request.form.get("ins_fict_fact")
            ins_art_other = request.form.get("ins_art_other")
            ins_form = request.form.get("ins_form")
            ins_content = request.form.get("ins_content")
            ins_comment = request.form.get("ins_comment")

            return render_template("confirm.html", wording="DELETE from", wording2="", action="deleteed", ins_sector=ins_sector, ins_new_sector=ins_new_sector, ins_sector_name=ins_sector_name, ins_author=ins_author, ins_title=ins_title,
                                ins_edition=ins_edition, ins_firstY=ins_firstY, ins_ourY=ins_ourY, ins_language=ins_language, ins_country=ins_country, ins_fict_fact=ins_fict_fact, ins_art_other=ins_art_other,
                                ins_form=ins_form, ins_content=ins_content, ins_comment=ins_comment)

        # User clicked on "Cancel" button
        if request.form.get("cancel"):

            return redirect("/admin")

        # User clicked on "Confirm and Insert" button on confirm.html page
        if request.form.get("inserted"):

            # Ensure title submitted
            if ins_title == "":
                return apology("must provide title", 403)

            # Define datetime (source: https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python)
            utc_now = pytz.utc.localize(datetime.datetime.utcnow())
            cet_now = utc_now.astimezone(pytz.timezone("Europe/Bratislava"))

            # Identify sect_id corresponding to the inserted sector and store in variable to be used in insert into books
            sector = db.execute("SELECT sect_id FROM sectors WHERE sector = :s", s=ins_sector)

            # Identify new_sect_id
            new_sector = db.execute("SELECT new_sect_id FROM new_sectors WHERE new_sector = :n", n=ins_new_sector)

            # Identify sect_name_id
            sector_name = db.execute("SELECT sect_name_id FROM sector_names WHERE sector_name = :s", s=ins_sector_name)

            # Query database for inserted author
            rows = db.execute("SELECT * FROM authors WHERE author = :a", a=ins_author)
            # If given author does not exist, insert him into database
            if len(rows) == 0:
                db.execute("INSERT INTO authors (author) VALUES (?)", ins_author)
            # Identify author_id
            author = db.execute("SELECT author_id FROM authors WHERE author = :a", a=ins_author)

            # Identify ed_id
            edition = db.execute("SELECT ed_id FROM editions WHERE edition = :e", e=ins_edition)

            # Query database for inserted firstY
            rows = db.execute("SELECT * FROM firstYs WHERE firstY = :f", f=ins_firstY)
            # If given firstY does not exist, insert it into database
            if len(rows) == 0:
                db.execute("INSERT INTO firstYs (firstY) VALUES (?)", ins_firstY)
            # Identify firstY_id
            firstY = db.execute("SELECT firstY_id FROM firstYs WHERE firstY = :f", f=ins_firstY)

            # Query database for inserted ourY
            rows = db.execute("SELECT * FROM ourYs WHERE ourY = :o", o=ins_ourY)
            # If given ourY does not exist, insert it into database
            if len(rows) == 0:
                db.execute("INSERT INTO ourYs (ourY) VALUES (?)", ins_ourY)
            # Identify ourY_id
            ourY = db.execute("SELECT ourY_id FROM ourYs WHERE ourY = :o", o=ins_ourY)

            # Identify lang_id
            language = db.execute("SELECT lang_id FROM languages WHERE language = :l", l=ins_language)

            # Identify ctry_id
            country = db.execute("SELECT ctry_id FROM countries WHERE country = :c", c=ins_country)

            # Identify fict_id
            fict_fact = db.execute("SELECT fict_id FROM fict_facts WHERE fict_fact = :f", f=ins_fict_fact)

            # Identify art_id
            art_other = db.execute("SELECT art_id FROM art_others WHERE art_other = :a", a=ins_art_other)

            # Identify form_id
            form = db.execute("SELECT form_id FROM forms WHERE form = :f", f=ins_form)

            # Identify cont_id
            content = db.execute("SELECT cont_id FROM contents WHERE content = :c", c=ins_content)

            # Query database for inserted comment
            rows = db.execute("SELECT * FROM comments WHERE comment = :c", c=ins_comment)
            # If given firstY does not exist, insert it into database
            if len(rows) == 0:
                db.execute("INSERT INTO comments (comment) VALUES (?)", ins_comment)
            # Identify comment_id
            comment = db.execute("SELECT comment_id FROM comments WHERE comment = :c", c=ins_comment)

            # rows = db.execute("INSERT INTO tests (test_title, author, datetime) VALUES (:test_title, :author, :datetime)", test_title=ins_title, author=ins_author, datetime=cet_now)
            rows = db.execute("INSERT INTO books (sect_id, new_sect_id, sect_name_id, author_id, title, ed_id, firstY_id, ourY_id, lang_id, ctry_id, fict_id, art_id, form_id, cont_id, comment_id, datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   sector[0]["sect_id"], new_sector[0]["new_sect_id"], sector_name[0]["sect_name_id"], author[0]["author_id"], ins_title, edition[0]["ed_id"], firstY[0]["firstY_id"], ourY[0]["ourY_id"],
                   language[0]["lang_id"], country[0]["ctry_id"], fict_fact[0]["fict_id"], art_other[0]["art_id"], form[0]["form_id"], content[0]["cont_id"], comment[0]["comment_id"], cet_now)

            # return redirect("/")
            return render_template("updated.html", wording="INSERTED into", ins_sector=ins_sector, ins_new_sector=ins_new_sector, ins_sector_name=ins_sector_name, ins_author=ins_author, ins_title=ins_title,
                                ins_edition=ins_edition, ins_firstY=ins_firstY, ins_ourY=ins_ourY, ins_language=ins_language, ins_country=ins_country, ins_fict_fact=ins_fict_fact, ins_art_other=ins_art_other,
                                ins_form=ins_form, ins_content=ins_content, ins_comment=ins_comment)

        # User clicked on "Confirm and Edit" button on confirm.html page
        if request.form.get("edited"):

            # Ensure title submitted
            if ins_title == "":
                return apology("must provide title", 403)

            # Define datetime (source: https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python)
            utc_now = pytz.utc.localize(datetime.datetime.utcnow())
            cet_now = utc_now.astimezone(pytz.timezone("Europe/Bratislava"))

            # Identify sect_id corresponding to the inserted sector and store in variable to be used in insert into books
            sector = db.execute("SELECT sect_id FROM sectors WHERE sector = :s", s=ins_sector)

            # Identify new_sect_id
            new_sector = db.execute("SELECT new_sect_id FROM new_sectors WHERE new_sector = :n", n=ins_new_sector)

            # Identify sect_name_id
            sector_name = db.execute("SELECT sect_name_id FROM sector_names WHERE sector_name = :s", s=ins_sector_name)

            # Query database for inserted author
            rows = db.execute("SELECT * FROM authors WHERE author = :a", a=ins_author)
            # If given author does not exist, insert him into database
            if len(rows) == 0:
                db.execute("INSERT INTO authors (author) VALUES (?)", ins_author)
            # Identify author_id
            author = db.execute("SELECT author_id FROM authors WHERE author = :a", a=ins_author)

            # Identify ed_id
            edition = db.execute("SELECT ed_id FROM editions WHERE edition = :e", e=ins_edition)

            # Query database for inserted firstY
            rows = db.execute("SELECT * FROM firstYs WHERE firstY = :f", f=ins_firstY)
            # If given firstY does not exist, insert it into database
            if len(rows) == 0:
                db.execute("INSERT INTO firstYs (firstY) VALUES (?)", ins_firstY)
            # Identify firstY_id
            firstY = db.execute("SELECT firstY_id FROM firstYs WHERE firstY = :f", f=ins_firstY)

            # Query database for inserted ourY
            rows = db.execute("SELECT * FROM ourYs WHERE ourY = :o", o=ins_ourY)
            # If given ourY does not exist, insert it into database
            if len(rows) == 0:
                db.execute("INSERT INTO ourYs (ourY) VALUES (?)", ins_ourY)
            # Identify ourY_id
            ourY = db.execute("SELECT ourY_id FROM ourYs WHERE ourY = :o", o=ins_ourY)

            # Identify lang_id
            language = db.execute("SELECT lang_id FROM languages WHERE language = :l", l=ins_language)

            # Identify ctry_id
            country = db.execute("SELECT ctry_id FROM countries WHERE country = :c", c=ins_country)

            # Identify fict_id
            fict_fact = db.execute("SELECT fict_id FROM fict_facts WHERE fict_fact = :f", f=ins_fict_fact)

            # Identify art_id
            art_other = db.execute("SELECT art_id FROM art_others WHERE art_other = :a", a=ins_art_other)

            # Identify form_id
            form = db.execute("SELECT form_id FROM forms WHERE form = :f", f=ins_form)

            # Identify cont_id
            content = db.execute("SELECT cont_id FROM contents WHERE content = :c", c=ins_content)

            # Query database for inserted comment
            rows = db.execute("SELECT * FROM comments WHERE comment = :c", c=ins_comment)
            # If given firstY does not exist, insert it into database
            if len(rows) == 0:
                db.execute("INSERT INTO comments (comment) VALUES (?)", ins_comment)
            # Identify comment_id
            comment = db.execute("SELECT comment_id FROM comments WHERE comment = :c", c=ins_comment)

            # rows = db.execute("INSERT INTO tests (test_title, author, datetime) VALUES (:test_title, :author, :datetime)", test_title=ins_title, author=ins_author, datetime=cet_now)
            rows = db.execute("UPDATE books SET sect_id = :sect_id, new_sect_id = :new_sect_id, sect_name_id = :sect_name_id, author_id = :author_id, title = :title, ed_id = :ed_id, firstY_id = :firstY_id, \
                            ourY_id = :ourY_id, lang_id = :lang_id, ctry_id = :ctry_id, fict_id = :fict_id, art_id = :art_id, form_id = :form_id, cont_id = :cont_id, comment_id = :comment_id, datetime = :datetime \
                            WHERE book_id = :book_id", sect_id=sector[0]["sect_id"], new_sect_id=new_sector[0]["new_sect_id"], sect_name_id=sector_name[0]["sect_name_id"], author_id=author[0]["author_id"], title=ins_title,
                            ed_id=edition[0]["ed_id"], firstY_id=firstY[0]["firstY_id"], ourY_id=ourY[0]["ourY_id"], lang_id=language[0]["lang_id"], ctry_id=country[0]["ctry_id"], fict_id=fict_fact[0]["fict_id"],
                            art_id=art_other[0]["art_id"], form_id=form[0]["form_id"], cont_id=content[0]["cont_id"], comment_id=comment[0]["comment_id"], datetime=cet_now, book_id=book_id)

            # return redirect("/")
            return render_template("updated.html", wording="MODIFIED in", ins_sector=ins_sector, ins_new_sector=ins_new_sector, ins_sector_name=ins_sector_name, ins_author=ins_author, ins_title=ins_title,
                                ins_edition=ins_edition, ins_firstY=ins_firstY, ins_ourY=ins_ourY, ins_language=ins_language, ins_country=ins_country, ins_fict_fact=ins_fict_fact, ins_art_other=ins_art_other,
                                ins_form=ins_form, ins_content=ins_content, ins_comment=ins_comment)

        # User clicked on "Confirm and Delete" button on confirm.html page
        if request.form.get("deleteed"):

            rows = db.execute("DELETE FROM books WHERE book_id = :book_id", book_id=book_id)

            # return redirect("/")
            return render_template("updated.html", wording="DELETED from", ins_sector=ins_sector, ins_new_sector=ins_new_sector, ins_sector_name=ins_sector_name, ins_author=ins_author, ins_title=ins_title,
                                ins_edition=ins_edition, ins_firstY=ins_firstY, ins_ourY=ins_ourY, ins_language=ins_language, ins_country=ins_country, ins_fict_fact=ins_fict_fact, ins_art_other=ins_art_other,
                                ins_form=ins_form, ins_content=ins_content, ins_comment=ins_comment)

        # User clicked on "OK" button on updated.html page
        if request.form.get("ok"):
            return redirect("/admin")

        # User clicked on "Search" button
        else:

            # Store fields that are input and not dropdown
            s_author = request.form.get("author")
            s_title = request.form.get("title")
            s_firstY = request.form.get("firstY")
            s_ourY = request.form.get("ourY")
            s_comment = request.form.get("comment")

            # Get all existing sector categories ------ ADMIN SEARCH
            lines = db.execute("SELECT sector FROM sectors")
            # Create list of dropdown menu options
            all_sectors = []
            line = 0
            nb = len(lines)
            nb_sectors = nb + 1
            s_sector = request.form.get("sector")
            # Populate dropdown menu for sector
            for line in range(nb):
                sector = lines[line]["sector"]
                all_sectors.append(sector)
            # Sort options and store in temporary sorted list
            all_sectors.sort()
            sorted_all_sectors = all_sectors
            all_sectors = []
            # If selection was made, keep the selected option as default
            if s_sector != "Select...":
                all_sectors.append(s_sector)
                nb_sectors = nb + 2
            # Store "Select..." as default dropdown option
            sector = "Select..."
            all_sectors.append(sector)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                sector = sorted_all_sectors[line]
                all_sectors.append(sector)

            # Get all existing new_sector categories
            lines = db.execute("SELECT new_sector FROM new_sectors")
            # Create list of dropdown menu options
            all_new_sectors = []
            line = 0
            nb = len(lines)
            nb_new_sectors = nb + 1
            s_new_sector = request.form.get("new_sector")
            # Populate dropdown menu for sector
            for line in range(nb):
                new_sector = lines[line]["new_sector"]
                all_new_sectors.append(new_sector)
            # Sort options and store in temporary sorted list
            all_new_sectors.sort()
            sorted_all_new_sectors = all_new_sectors
            all_new_sectors = []
            # If selection was made, keep the selected option as default
            if s_new_sector != "Select...":
                all_new_sectors.append(s_new_sector)
                nb_new_sectors = nb + 2
            # Store "Select..." as default dropdown option
            new_sector = "Select..."
            all_new_sectors.append(new_sector)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                new_sector = sorted_all_new_sectors[line]
                all_new_sectors.append(new_sector)

            # Get all existing sector_name categories
            lines = db.execute("SELECT sector_name FROM sector_names")
            # Create list of dropdown menu options
            all_sector_names = []
            line = 0
            nb = len(lines)
            nb_sector_names = nb + 1
            s_sector_name = request.form.get("sector_name")
            # Populate dropdown menu for sector
            for line in range(nb):
                sector_name = lines[line]["sector_name"]
                all_sector_names.append(sector_name)
            # Sort options and store in temporary sorted list
            all_sector_names.sort()
            sorted_all_sector_names = all_sector_names
            all_sector_names = []
            # If selection was made, keep the selected option as default
            if s_sector_name != "Select...":
                all_sector_names.append(s_sector_name)
                nb_sector_names = nb + 2
            # Store "Select..." as default dropdown option
            sector_name = "Select..."
            all_sector_names.append(sector_name)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                sector_name = sorted_all_sector_names[line]
                all_sector_names.append(sector_name)

            # Get all existing edition categories
            lines = db.execute("SELECT edition FROM editions")
            # Create list of dropdown menu options
            all_editions = []
            line = 0
            nb = len(lines)
            nb_editions = nb + 1
            s_edition = request.form.get("edition")
            # Populate dropdown menu for sector
            for line in range(nb):
                edition = lines[line]["edition"]
                all_editions.append(edition)
            # Sort options and store in temporary sorted list
            all_editions.sort()
            sorted_all_editions = all_editions
            all_editions = []
            # If selection was made, keep the selected option as default
            if s_edition != "Select...":
                all_editions.append(s_edition)
                nb_editions = nb + 2
            # Store "Select..." as default dropdown option
            edition = "Select..."
            all_editions.append(edition)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                edition = sorted_all_editions[line]
                all_editions.append(edition)

            # Get all existing language categories
            lines = db.execute("SELECT language FROM languages")
            # Create list of dropdown menu options
            all_languages = []
            line = 0
            nb = len(lines)
            nb_languages = nb + 1
            s_language = request.form.get("language")
            # Populate dropdown menu for sector
            for line in range(nb):
                language = lines[line]["language"]
                all_languages.append(language)
            # Sort options and store in temporary sorted list
            all_languages.sort()
            sorted_all_languages = all_languages
            all_languages = []
            # If selection was made, keep the selected option as default
            if s_language != "Select...":
                all_languages.append(s_language)
                nb_languages = nb + 2
            # Store "Select..." as default dropdown option
            language = "Select..."
            all_languages.append(language)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                language = sorted_all_languages[line]
                all_languages.append(language)

            # Get all existing country categories
            lines = db.execute("SELECT country FROM countries")
            # Create list of dropdown menu options
            all_countries = []
            line = 0
            nb = len(lines)
            nb_countries = nb + 1
            s_country = request.form.get("country")
            # Populate dropdown menu for sector
            for line in range(nb):
                country = lines[line]["country"]
                all_countries.append(country)
            # Sort options and store in temporary sorted list
            all_countries.sort()
            sorted_all_countries = all_countries
            all_countries = []
            # If selection was made, keep the selected option as default
            if s_country != "Select...":
                all_countries.append(s_country)
                nb_countries = nb + 2
            # Store "Select..." as default dropdown option
            country = "Select..."
            all_countries.append(country)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                country = sorted_all_countries[line]
                all_countries.append(country)

            # Get all existing fict_fact categories
            lines = db.execute("SELECT fict_fact FROM fict_facts")
            # Create list of dropdown menu options
            all_fict_facts = []
            line = 0
            nb = len(lines)
            nb_fict_facts = nb + 1
            s_fict_fact = request.form.get("fict_fact")
            # Populate dropdown menu for sector
            for line in range(nb):
                fict_fact = lines[line]["fict_fact"]
                all_fict_facts.append(fict_fact)
            # Sort options and store in temporary sorted list
            all_fict_facts.sort()
            sorted_all_fict_facts = all_fict_facts
            all_fict_facts = []
            # If selection was made, keep the selected option as default
            if s_fict_fact != "Select...":
                all_fict_facts.append(s_fict_fact)
                nb_fict_facts = nb + 2
            # Store "Select..." as default dropdown option
            fict_fact = "Select..."
            all_fict_facts.append(fict_fact)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                fict_fact = sorted_all_fict_facts[line]
                all_fict_facts.append(fict_fact)

            # Get all existing art_other categories
            lines = db.execute("SELECT art_other FROM art_others")
            # Create list of dropdown menu options
            all_art_others = []
            line = 0
            nb = len(lines)
            nb_art_others = nb + 1
            s_art_other = request.form.get("art_other")
            # Populate dropdown menu for sector
            for line in range(nb):
                art_other = lines[line]["art_other"]
                all_art_others.append(art_other)
            # Sort options and store in temporary sorted list
            all_art_others.sort()
            sorted_all_art_others = all_art_others
            all_art_others = []
            # If selection was made, keep the selected option as default
            if s_art_other != "Select...":
                all_art_others.append(s_art_other)
                nb_art_others = nb + 2
            # Store "Select..." as default dropdown option
            art_other = "Select..."
            all_art_others.append(art_other)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                art_other = sorted_all_art_others[line]
                all_art_others.append(art_other)

            # Get all existing form categories
            lines = db.execute("SELECT form FROM forms")
            # Create list of dropdown menu options
            all_forms = []
            line = 0
            nb = len(lines)
            nb_forms = nb + 1
            s_form = request.form.get("form")
            # Populate dropdown menu for sector
            for line in range(nb):
                form = lines[line]["form"]
                all_forms.append(form)
            # Sort options and store in temporary sorted list
            all_forms.sort()
            sorted_all_forms = all_forms
            all_forms = []
            # If selection was made, keep the selected option as default
            if s_form != "Select...":
                all_forms.append(s_form)
                nb_forms = nb + 2
            # Store "Select..." as default dropdown option
            form = "Select..."
            all_forms.append(form)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                form = sorted_all_forms[line]
                all_forms.append(form)

            # Get all existing content categories
            lines = db.execute("SELECT content FROM contents")
            # Create list of dropdown menu options
            all_contents = []
            line = 0
            nb = len(lines)
            nb_contents = nb + 1
            s_content = request.form.get("content")
            # Populate dropdown menu for sector
            for line in range(nb):
                content = lines[line]["content"]
                all_contents.append(content)
            # Sort options and store in temporary sorted list
            all_contents.sort()
            sorted_all_contents = all_contents
            all_contents = []
            # If selection was made, keep the selected option as default
            if s_content != "Select...":
                all_contents.append(s_content)
                nb_contents = nb + 2
            # Store "Select..." as default dropdown option
            content = "Select..."
            all_contents.append(content)
            # Re-populate so that Select... is first option and then sorted list
            for line in range(nb):
                content = sorted_all_contents[line]
                all_contents.append(content)

            # Convert filtered SEARCH parameters to be used in query
            if s_sector == "": sector = ""
            elif s_sector == "Select...": sector = "%"
            else: sector = "%" + s_sector + "%"

            if s_new_sector == "": new_sector = ""
            elif s_new_sector == "Select...": new_sector = "%"
            else: new_sector = "%" + s_new_sector + "%"

            if s_sector_name == "": sector_name = ""
            elif s_sector_name == "Select...": sector_name = "%"
            else: sector_name = "%" + s_sector_name + "%"

            if s_author == " ": author = ""
            elif s_author == "Select...": author = "%"
            else: author = "%" + s_author + "%"

            # Title field cannot be blank (but can be not filtered)
            if s_title == "Select...": title = "%"
            else: title = "%" + s_title + "%"

            if s_edition == "": edition = ""
            elif s_edition == "Select...": edition = "%"
            else: edition = "%" + s_edition + "%"

            if s_firstY == " ": firstY = ""
            elif s_firstY == "Select...": firstY = "%"
            else: firstY = "%" + s_firstY + "%"

            if s_ourY == " ": ourY = ""
            elif s_ourY == "Select...": ourY = "%"
            else: ourY = "%" + s_ourY + "%"

            if s_language == "": language = ""
            elif s_language == "Select...": language = "%"
            else: language = "%" + s_language + "%"

            if s_country == "": country = ""
            elif s_country == "Select...": country = "%"
            else: country = "%" + s_country + "%"

            if s_fict_fact == "": fict_fact = ""
            elif s_fict_fact == "Select...": fict_fact = "%"
            else: fict_fact = "%" + s_fict_fact + "%"

            if s_art_other == "": art_other = ""
            elif s_art_other == "Select...": art_other = "%"
            else: art_other = "%" + s_art_other + "%"

            if s_form == "": form = ""
            elif s_form == "Select...": form = "%"
            else: form = "%" + s_form + "%"

            if s_content == "": content = ""
            elif s_content == "Select...": content = "%"
            else: content = "%" + s_content + "%"

            if s_comment == " ": comment = ""
            elif s_comment == "Select...": comment = "%"
            else: comment = "%" + s_comment + "%"

            # Query books by filter parameters
            rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                               authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                               languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                               forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE sector LIKE :sector AND new_sector LIKE :new_sector AND \
                               sector_name LIKE :sector_name AND author LIKE :author AND title LIKE :title AND edition LIKE :edition AND firstY LIKE :firstY AND ourY LIKE :ourY AND language LIKE :language AND country LIKE :country AND fict_fact LIKE :fict_fact AND \
                               art_other LIKE :art_other AND form LIKE :form AND content LIKE :content AND comment LIKE :comment", sector=sector, new_sector=new_sector, sector_name=sector_name, author=author, title=title, edition=edition,
                               firstY=firstY, ourY=ourY, language=language, country=country, fict_fact=fict_fact, art_other=art_other, form=form, content=content, comment=comment)

            # Create a list of result items to be displayed
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
            ids = []
            row = 0
            items = len(rows)

            # Populate results table
            for row in range(items):
                sector = rows[row]["sector"]
                sectors.append(sector)
                new_sector = rows[row]["new_sector"]
                new_sectors.append(new_sector)
                sector_name = rows[row]["sector_name"]
                sector_names.append(sector_name)
                author = rows[row]["author"]
                authors.append(author)
                title = rows[row]["title"]
                titles.append(title)
                edition = rows[row]["edition"]
                editions.append(edition)
                firstY = rows[row]["firstY"]
                firstYs.append(firstY)
                ourY = rows[row]["ourY"]
                ourYs.append(ourY)
                language = rows[row]["language"]
                languages.append(language)
                country = rows[row]["country"]
                countries.append(country)
                fict_fact = rows[row]["fict_fact"]
                fict_facts.append(fict_fact)
                art_other = rows[row]["art_other"]
                art_others.append(art_other)
                form = rows[row]["form"]
                forms.append(form)
                content = rows[row]["content"]
                contents.append(content)
                comment = rows[row]["comment"]
                comments.append(comment)
                book_id = rows[row]["book_id"]
                ids.append(book_id)

            return render_template("admin.html", ins_all_sectors=ins_all_sectors, ins_nb_sectors=ins_nb_sectors, ins_all_new_sectors=ins_all_new_sectors, ins_nb_new_sectors=ins_nb_new_sectors, ins_all_sector_names=ins_all_sector_names,
                                ins_nb_sector_names=ins_nb_sector_names, ins_author=ins_author, ins_title=ins_title, ins_all_editions=ins_all_editions, ins_nb_editions=ins_nb_editions, ins_firstY=ins_firstY, ins_ourY=ins_ourY,
                                ins_all_languages=ins_all_languages, ins_nb_languages=ins_nb_languages, ins_all_countries=ins_all_countries, ins_nb_countries=ins_nb_countries, ins_all_fict_facts=ins_all_fict_facts,
                                ins_nb_fict_facts=ins_nb_fict_facts, ins_all_art_others=ins_all_art_others, ins_nb_art_others=ins_nb_art_others, ins_all_forms=ins_all_forms, ins_nb_forms=ins_nb_forms, ins_all_contents=ins_all_contents,
                                ins_nb_contents=ins_nb_contents, ins_comment=ins_comment, all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names,
                                nb_sector_names=nb_sector_names, s_author=s_author, s_title=s_title, all_editions=all_editions, nb_editions=nb_editions, s_firstY=s_firstY, s_ourY=s_ourY, all_languages=all_languages, nb_languages=nb_languages,
                                all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts, all_art_others=all_art_others, nb_art_others=nb_art_others, all_forms=all_forms, nb_forms=nb_forms,
                                all_contents=all_contents, nb_contents=nb_contents, s_comment=s_comment, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors, sector_names=sector_names, authors=authors, titles=titles,
                                editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages, countries=countries, fict_facts=fict_facts, art_others=art_others, forms=forms, contents=contents, comments=comments, ids=ids)


    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Reset all ins_ input fields to "Select..."
        ins_author = ""
        ins_title = ""
        ins_firstY = ""
        ins_ourY = ""
        ins_comment = ""

        # Reset all s_ input fields to "Select..."
        s_author = ""
        s_title = ""
        s_firstY = ""
        s_ourY = ""
        s_comment = ""

        # Get all existing sector categories
        lines = db.execute("SELECT sector FROM sectors")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_sectors = []
        all_sectors = []
        line = 0
        nb = len(lines)
        ins_nb_sectors = nb + 1
        nb_sectors = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_sector = lines[line]["sector"]
            sector = lines[line]["sector"]
            ins_all_sectors.append(ins_sector)
            all_sectors.append(sector)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_sectors.sort()
        sorted_ins_all_sectors = ins_all_sectors
        ins_all_sectors = []
        all_sectors.sort()
        sorted_all_sectors = all_sectors
        all_sectors = []
        # Store "Select..." as default dropdown option
        ins_sector = "Select..."
        sector = "Select..."
        ins_all_sectors.append(ins_sector)
        all_sectors.append(sector)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_sector = sorted_ins_all_sectors[line]
            sector = sorted_all_sectors[line]
            ins_all_sectors.append(ins_sector)
            all_sectors.append(sector)

        # Get all existing new_sector categories
        lines = db.execute("SELECT new_sector FROM new_sectors")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_new_sectors = []
        all_new_sectors = []
        line = 0
        nb = len(lines)
        ins_nb_new_sectors = nb + 1
        nb_new_sectors = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_new_sector = lines[line]["new_sector"]
            new_sector = lines[line]["new_sector"]
            ins_all_new_sectors.append(ins_new_sector)
            all_new_sectors.append(new_sector)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_new_sectors.sort()
        sorted_ins_all_new_sectors = ins_all_new_sectors
        ins_all_new_sectors = []
        all_new_sectors.sort()
        sorted_all_new_sectors = all_new_sectors
        all_new_sectors = []
        # Store "Select..." as default dropdown option
        ins_new_sector = "Select..."
        new_sector = "Select..."
        ins_all_new_sectors.append(ins_new_sector)
        all_new_sectors.append(new_sector)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_new_sector = sorted_ins_all_new_sectors[line]
            new_sector = sorted_all_new_sectors[line]
            ins_all_new_sectors.append(ins_new_sector)
            all_new_sectors.append(new_sector)

        # Get all existing sector_name categories
        lines = db.execute("SELECT sector_name FROM sector_names")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_sector_names = []
        all_sector_names = []
        line = 0
        nb = len(lines)
        ins_nb_sector_names = nb + 1
        nb_sector_names = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_sector_name = lines[line]["sector_name"]
            sector_name = lines[line]["sector_name"]
            ins_all_sector_names.append(ins_sector_name)
            all_sector_names.append(sector_name)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_sector_names.sort()
        sorted_ins_all_sector_names = ins_all_sector_names
        ins_all_sector_names = []
        all_sector_names.sort()
        sorted_all_sector_names = all_sector_names
        all_sector_names = []
        # Store "Select..." as default dropdown option
        ins_sector_name = "Select..."
        sector_name = "Select..."
        ins_all_sector_names.append(ins_sector_name)
        all_sector_names.append(sector_name)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_sector_name = sorted_ins_all_sector_names[line]
            sector_name = sorted_all_sector_names[line]
            ins_all_sector_names.append(ins_sector_name)
            all_sector_names.append(sector_name)

        # Get all existing edition categories
        lines = db.execute("SELECT edition FROM editions")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_editions = []
        all_editions = []
        line = 0
        nb = len(lines)
        ins_nb_editions = nb + 1
        nb_editions = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_edition = lines[line]["edition"]
            edition = lines[line]["edition"]
            ins_all_editions.append(ins_edition)
            all_editions.append(edition)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_editions.sort()
        sorted_ins_all_editions = ins_all_editions
        ins_all_editions = []
        all_editions.sort()
        sorted_all_editions = all_editions
        all_editions = []
        # Store "Select..." as default dropdown option
        ins_edition = "Select..."
        edition = "Select..."
        ins_all_editions.append(ins_edition)
        all_editions.append(edition)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_edition = sorted_ins_all_editions[line]
            edition = sorted_all_editions[line]
            ins_all_editions.append(ins_edition)
            all_editions.append(edition)

        # Get all existing language categories
        lines = db.execute("SELECT language FROM languages")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_languages = []
        all_languages = []
        line = 0
        nb = len(lines)
        ins_nb_languages = nb + 1
        nb_languages = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_language = lines[line]["language"]
            language = lines[line]["language"]
            ins_all_languages.append(ins_language)
            all_languages.append(language)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_languages.sort()
        sorted_ins_all_languages = ins_all_languages
        ins_all_languages = []
        all_languages.sort()
        sorted_all_languages = all_languages
        all_languages = []
        # Store "Select..." as default dropdown option
        ins_language = "Select..."
        language = "Select..."
        ins_all_languages.append(ins_language)
        all_languages.append(language)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_language = sorted_ins_all_languages[line]
            language = sorted_all_languages[line]
            ins_all_languages.append(ins_language)
            all_languages.append(language)

        # Get all existing country categories
        lines = db.execute("SELECT country FROM countries")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_countries = []
        all_countries = []
        line = 0
        nb = len(lines)
        ins_nb_countries = nb + 1
        nb_countries = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_country = lines[line]["country"]
            country = lines[line]["country"]
            ins_all_countries.append(ins_country)
            all_countries.append(country)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_countries.sort()
        sorted_ins_all_countries = ins_all_countries
        ins_all_countries = []
        all_countries.sort()
        sorted_all_countries = all_countries
        all_countries = []
        # Store "Select..." as default dropdown option
        ins_country = "Select..."
        country = "Select..."
        ins_all_countries.append(ins_country)
        all_countries.append(country)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_country = sorted_ins_all_countries[line]
            country = sorted_all_countries[line]
            ins_all_countries.append(ins_country)
            all_countries.append(country)

        # Get all existing fict_fact categories
        lines = db.execute("SELECT fict_fact FROM fict_facts")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_fict_facts = []
        all_fict_facts = []
        line = 0
        nb = len(lines)
        ins_nb_fict_facts = nb + 1
        nb_fict_facts = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_fict_fact = lines[line]["fict_fact"]
            fict_fact = lines[line]["fict_fact"]
            ins_all_fict_facts.append(ins_fict_fact)
            all_fict_facts.append(fict_fact)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_fict_facts.sort()
        sorted_ins_all_fict_facts = ins_all_fict_facts
        ins_all_fict_facts = []
        all_fict_facts.sort()
        sorted_all_fict_facts = all_fict_facts
        all_fict_facts = []
        # Store "Select..." as default dropdown option
        ins_fict_fact = "Select..."
        fict_fact = "Select..."
        ins_all_fict_facts.append(ins_fict_fact)
        all_fict_facts.append(fict_fact)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_fict_fact = sorted_ins_all_fict_facts[line]
            fict_fact = sorted_all_fict_facts[line]
            ins_all_fict_facts.append(ins_fict_fact)
            all_fict_facts.append(fict_fact)

        # Get all existing art_other categories
        lines = db.execute("SELECT art_other FROM art_others")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_art_others = []
        all_art_others = []
        line = 0
        nb = len(lines)
        ins_nb_art_others = nb + 1
        nb_art_others = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_art_other = lines[line]["art_other"]
            art_other = lines[line]["art_other"]
            ins_all_art_others.append(ins_art_other)
            all_art_others.append(art_other)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_art_others.sort()
        sorted_ins_all_art_others = ins_all_art_others
        ins_all_art_others = []
        all_art_others.sort()
        sorted_all_art_others = all_art_others
        all_art_others = []
        # Store "Select..." as default dropdown option
        ins_art_other = "Select..."
        art_other = "Select..."
        ins_all_art_others.append(ins_art_other)
        all_art_others.append(art_other)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_art_other = sorted_ins_all_art_others[line]
            art_other = sorted_all_art_others[line]
            ins_all_art_others.append(ins_art_other)
            all_art_others.append(art_other)

        # Get all existing form categories
        lines = db.execute("SELECT form FROM forms")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_forms = []
        all_forms = []
        line = 0
        nb = len(lines)
        ins_nb_forms = nb + 1
        nb_forms = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_form = lines[line]["form"]
            form = lines[line]["form"]
            ins_all_forms.append(ins_form)
            all_forms.append(form)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_forms.sort()
        sorted_ins_all_forms = ins_all_forms
        ins_all_forms = []
        all_forms.sort()
        sorted_all_forms = all_forms
        all_forms = []
        # Store "Select..." as default dropdown option
        ins_form = "Select..."
        form = "Select..."
        ins_all_forms.append(ins_form)
        all_forms.append(form)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_form = sorted_ins_all_forms[line]
            form = sorted_all_forms[line]
            ins_all_forms.append(ins_form)
            all_forms.append(form)

        # Get all existing content categories
        lines = db.execute("SELECT content FROM contents")
        # Create list of dropdown menu options (for Insert field and Search field separately)
        ins_all_contents = []
        all_contents = []
        line = 0
        nb = len(lines)
        ins_nb_contents = nb + 1
        nb_contents = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            ins_content = lines[line]["content"]
            content = lines[line]["content"]
            ins_all_contents.append(ins_content)
            all_contents.append(content)
        # Sort options and store in temporary sorted list (for Insert field and Search field separately)
        ins_all_contents.sort()
        sorted_ins_all_contents = ins_all_contents
        ins_all_contents = []
        all_contents.sort()
        sorted_all_contents = all_contents
        all_contents = []
        # Store "Select..." as default dropdown option
        ins_content = "Select..."
        content = "Select..."
        ins_all_contents.append(ins_content)
        all_contents.append(content)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            ins_content = sorted_ins_all_contents[line]
            content = sorted_all_contents[line]
            ins_all_contents.append(ins_content)
            all_contents.append(content)

        # Display all books
        rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                        authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                        languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                        forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE author LIKE :author", author='%Rudolf%')

        # Create a list of result items to be displayed
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
        ids = []
        row = 0
        items = len(rows)
        # items = 5

        # Populate results table
        for row in range(items):
            sector = rows[row]["sector"]
            sectors.append(sector)
            new_sector = rows[row]["new_sector"]
            new_sectors.append(new_sector)
            sector_name = rows[row]["sector_name"]
            sector_names.append(sector_name)
            author = rows[row]["author"]
            authors.append(author)
            title = rows[row]["title"]
            titles.append(title)
            edition = rows[row]["edition"]
            editions.append(edition)
            firstY = rows[row]["firstY"]
            firstYs.append(firstY)
            ourY = rows[row]["ourY"]
            ourYs.append(ourY)
            language = rows[row]["language"]
            languages.append(language)
            country = rows[row]["country"]
            countries.append(country)
            fict_fact = rows[row]["fict_fact"]
            fict_facts.append(fict_fact)
            art_other = rows[row]["art_other"]
            art_others.append(art_other)
            form = rows[row]["form"]
            forms.append(form)
            content = rows[row]["content"]
            contents.append(content)
            comment = rows[row]["comment"]
            comments.append(comment)
            book_id = rows[row]["book_id"]
            ids.append(book_id)

        return render_template("admin.html", ins_all_sectors=ins_all_sectors, ins_nb_sectors=ins_nb_sectors, ins_all_new_sectors=ins_all_new_sectors, ins_nb_new_sectors=ins_nb_new_sectors, ins_all_sector_names=ins_all_sector_names,
                                ins_nb_sector_names=ins_nb_sector_names, ins_author=ins_author, ins_title=ins_title, ins_all_editions=ins_all_editions, ins_nb_editions=ins_nb_editions, ins_firstY=ins_firstY, ins_ourY=ins_ourY,
                                ins_all_languages=ins_all_languages, ins_nb_languages=ins_nb_languages, ins_all_countries=ins_all_countries, ins_nb_countries=ins_nb_countries, ins_all_fict_facts=ins_all_fict_facts,
                                ins_nb_fict_facts=ins_nb_fict_facts, ins_all_art_others=ins_all_art_others, ins_nb_art_others=ins_nb_art_others, ins_all_forms=ins_all_forms, ins_nb_forms=ins_nb_forms, ins_all_contents=ins_all_contents,
                                ins_nb_contents=ins_nb_contents, ins_comment=ins_comment, all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names,
                                nb_sector_names=nb_sector_names, s_author=s_author, s_title=s_title, all_editions=all_editions, nb_editions=nb_editions, s_firstY=s_firstY, s_ourY=s_ourY, all_languages=all_languages,
                                nb_languages=nb_languages, all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts, all_art_others=all_art_others, nb_art_others=nb_art_others,
                                all_forms=all_forms, nb_forms=nb_forms, all_contents=all_contents, nb_contents=nb_contents, s_comment=s_comment, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors, sector_names=sector_names,
                                authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages, countries=countries, fict_facts=fict_facts, art_others=art_others,
                                forms=forms, contents=contents, comments=comments, ids=ids)


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
@login_required
def index():
    """Show main database"""

    # User clicked on "Search" button
    if request.method == "POST":

        # Store fields that are input and not dropdown
        s_author = request.form.get("author")
        s_title = request.form.get("title")
        s_firstY = request.form.get("firstY")
        s_ourY = request.form.get("ourY")
        s_comment = request.form.get("comment")

        # Get all existing sector categories
        lines = db.execute("SELECT sector FROM sectors")
        # Create list of dropdown menu options
        all_sectors = []
        line = 0
        nb = len(lines)
        nb_sectors = nb + 1
        s_sector = request.form.get("sector")
        # Populate dropdown menu for sector
        for line in range(nb):
            sector = lines[line]["sector"]
            all_sectors.append(sector)
        # Sort options and store in temporary sorted list
        all_sectors.sort()
        sorted_all_sectors = all_sectors
        all_sectors = []
        # If selection was made, keep the selected option as default
        if s_sector != "Select...":
            all_sectors.append(s_sector)
            nb_sectors = nb + 2
        # Store "Select..." as default dropdown option
        sector = "Select..."
        all_sectors.append(sector)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            sector = sorted_all_sectors[line]
            all_sectors.append(sector)

        # Get all existing new_sector categories
        lines = db.execute("SELECT new_sector FROM new_sectors")
        # Create list of items to be displayed
        all_new_sectors = []
        line = 0
        nb = len(lines)
        nb_new_sectors = nb + 1
        s_new_sector = request.form.get("new_sector")
        # Populate dropdown menu
        for line in range(nb):
            new_sector = lines[line]["new_sector"]
            all_new_sectors.append(new_sector)
        # Sort options and store in temporary sorted list
        all_new_sectors.sort()
        sorted_all_new_sectors = all_new_sectors
        all_new_sectors = []
        # If selection was made, keep the selected option as default
        if s_new_sector != "Select...":
            all_new_sectors.append(s_new_sector)
            nb_new_sectors = nb + 2
        # Store "Select..." as default dropdown option
        new_sector = "Select..."
        all_new_sectors.append(new_sector)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            new_sector = sorted_all_new_sectors[line]
            all_new_sectors.append(new_sector)

        # Get all existing sector_name categories
        lines = db.execute("SELECT sector_name FROM sector_names")
        # Create list of items to be displayed
        all_sector_names = []
        line = 0
        nb = len(lines)
        nb_sector_names = nb + 1
        s_sector_name = request.form.get("sector_name")
        # Populate dropdown menu
        for line in range(nb):
            sector_name = lines[line]["sector_name"]
            all_sector_names.append(sector_name)
        # Sort options and store in temporary sorted list
        all_sector_names.sort()
        sorted_all_sector_names = all_sector_names
        all_sector_names = []
        # If selection was made, keep the selected option as default
        if s_sector_name != "Select...":
            all_sector_names.append(s_sector_name)
            nb_sector_names = nb + 2
        # Store "Select..." as default dropdown option
        sector_name = "Select..."
        all_sector_names.append(sector_name)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            sector_name = sorted_all_sector_names[line]
            all_sector_names.append(sector_name)

        # Get all existing edition categories
        lines = db.execute("SELECT edition FROM editions")
        # Create list of items to be displayed
        all_editions = []
        line = 0
        nb = len(lines)
        nb_editions = nb + 1
        s_edition = request.form.get("edition")
        # Populate dropdown menu
        for line in range(nb):
            edition = lines[line]["edition"]
            all_editions.append(edition)
        # Sort options and store in temporary sorted list
        all_editions.sort()
        sorted_all_editions = all_editions
        all_editions = []
        # If selection was made, keep the selected option as default
        if s_edition != "Select...":
            all_editions.append(s_edition)
            nb_editions = nb + 2
        # Store "Select..." as default dropdown option
        edition = "Select..."
        all_editions.append(edition)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            edition = sorted_all_editions[line]
            all_editions.append(edition)

        # Get all existing language categories
        lines = db.execute("SELECT language FROM languages")
        # Create list of items to be displayed
        all_languages = []
        line = 0
        nb = len(lines)
        nb_languages = nb + 1
        s_language = request.form.get("language")
        # Populate dropdown menu
        for line in range(nb):
            language = lines[line]["language"]
            all_languages.append(language)
        # Sort options and store in temporary sorted list
        all_languages.sort()
        sorted_all_languages = all_languages
        all_languages = []
        # If selection was made, keep the selected option as default
        if s_language != "Select...":
            all_languages.append(s_language)
            nb_languages = nb + 2
        # Store "Select..." as default dropdown option
        language = "Select..."
        all_languages.append(language)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            language = sorted_all_languages[line]
            all_languages.append(language)

        # Get all existing country categories
        lines = db.execute("SELECT country FROM countries")
        # Create list of items to be displayed
        all_countries = []
        line = 0
        nb = len(lines)
        nb_countries = nb + 1
        s_country = request.form.get("country")
        # Populate dropdown menu
        for line in range(nb):
            country = lines[line]["country"]
            all_countries.append(country)
        # Sort options and store in temporary sorted list
        all_countries.sort()
        sorted_all_countries = all_countries
        all_countries = []
        # If selection was made, keep the selected option as default
        if s_country != "Select...":
            all_countries.append(s_country)
            nb_countries = nb + 2
        # Store "Select..." as default dropdown option
        country = "Select..."
        all_countries.append(country)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            country = sorted_all_countries[line]
            all_countries.append(country)

        # Get all existing fict_fact categories
        lines = db.execute("SELECT fict_fact FROM fict_facts")
        # Create list of items to be displayed
        all_fict_facts = []
        line = 0
        nb = len(lines)
        nb_fict_facts = nb + 1
        s_fict_fact = request.form.get("fict_fact")
        # Populate dropdown menu
        for line in range(nb):
            fict_fact = lines[line]["fict_fact"]
            all_fict_facts.append(fict_fact)
        # Sort options and store in temporary sorted list
        all_fict_facts.sort()
        sorted_all_fict_facts = all_fict_facts
        all_fict_facts = []
        # If selection was made, keep the selected option as default (and increment list range by 1)
        if s_fict_fact != "Select...":
            all_fict_facts.append(s_fict_fact)
            nb_fict_facts = nb + 2
        # Store "Select..." as default dropdown option
        fict_fact = "Select..."
        all_fict_facts.append(fict_fact)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            fict_fact = sorted_all_fict_facts[line]
            all_fict_facts.append(fict_fact)

        # Get all existing art_other categories
        lines = db.execute("SELECT art_other FROM art_others")
        # Create list of items to be displayed
        all_art_others = []
        line = 0
        nb = len(lines)
        nb_art_others = nb + 1
        s_art_other = request.form.get("art_other")
        # Populate dropdown menu
        for line in range(nb):
            art_other = lines[line]["art_other"]
            all_art_others.append(art_other)
        # Sort options and store in temporary sorted list
        all_art_others.sort()
        sorted_all_art_others = all_art_others
        all_art_others = []
        # If selection was made, keep the selected option as default
        if s_art_other != "Select...":
            all_art_others.append(s_art_other)
            nb_art_others = nb + 2
        # Store "Select..." as default dropdown option
        art_other = "Select..."
        all_art_others.append(art_other)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            art_other = sorted_all_art_others[line]
            all_art_others.append(art_other)

        # Get all existing form categories
        lines = db.execute("SELECT form FROM forms")
        # Create list of items to be displayed
        all_forms = []
        line = 0
        nb = len(lines)
        nb_forms = nb + 1
        s_form = request.form.get("form")
        # Populate dropdown menu
        for line in range(nb):
            form = lines[line]["form"]
            all_forms.append(form)
        # Sort options and store in temporary sorted list
        all_forms.sort()
        sorted_all_forms = all_forms
        all_forms = []
        # If selection was made, keep the selected option as default
        if s_form != "Select...":
            all_forms.append(s_form)
            nb_forms = nb + 2
        # Store "Select..." as default dropdown option
        form = "Select..."
        all_forms.append(form)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            form = sorted_all_forms[line]
            all_forms.append(form)

        # Get all existing content categories
        lines = db.execute("SELECT content FROM contents")
        # Create list of items to be displayed
        all_contents = []
        line = 0
        nb = len(lines)
        nb_contents = nb + 1
        s_content = request.form.get("content")
        # Populate dropdown menu
        for line in range(nb):
            content = lines[line]["content"]
            all_contents.append(content)
        # Sort options and store in temporary sorted list
        all_contents.sort()
        sorted_all_contents = all_contents
        all_contents = []
        # If selection was made, keep the selected option as default
        if s_content != "Select...":
            all_contents.append(s_content)
            nb_contents = nb + 2
        # Store "Select..." as default dropdown option
        content = "Select..."
        all_contents.append(content)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            content = sorted_all_contents[line]
            all_contents.append(content)

        # Convert filtered SEARCH parameters to be used in query
        if s_sector == "": sector = ""
        elif s_sector == "Select...": sector = "%"
        else: sector = "%" + s_sector + "%"

        if s_new_sector == "": new_sector = ""
        elif s_new_sector == "Select...": new_sector = "%"
        else: new_sector = "%" + s_new_sector + "%"

        if s_sector_name == "": sector_name = ""
        elif s_sector_name == "Select...": sector_name = "%"
        else: sector_name = "%" + s_sector_name + "%"

        if s_author == " ": author = ""
        elif s_author == "Select...": author = "%"
        else: author = "%" + s_author + "%"

        # Title field cannot be blank (but can be not filtered)
        if s_title == "Select...": title = "%"
        else: title = "%" + s_title + "%"

        if s_edition == "": edition = ""
        elif s_edition == "Select...": edition = "%"
        else: edition = "%" + s_edition + "%"

        if s_firstY == " ": firstY = ""
        elif s_firstY == "Select...": firstY = "%"
        else: firstY = "%" + s_firstY + "%"

        if s_ourY == " ": ourY = ""
        elif s_ourY == "Select...": ourY = "%"
        else: ourY = "%" + s_ourY + "%"

        if s_language == "": language = ""
        elif s_language == "Select...": language = "%"
        else: language = "%" + s_language + "%"

        if s_country == "": country = ""
        elif s_country == "Select...": country = "%"
        else: country = "%" + s_country + "%"

        if s_fict_fact == "": fict_fact = ""
        elif s_fict_fact == "Select...": fict_fact = "%"
        else: fict_fact = "%" + s_fict_fact + "%"

        if s_art_other == "": art_other = ""
        elif s_art_other == "Select...": art_other = "%"
        else: art_other = "%" + s_art_other + "%"

        if s_form == "": form = ""
        elif s_form == "Select...": form = "%"
        else: form = "%" + s_form + "%"

        if s_content == "": content = ""
        elif s_content == "Select...": content = "%"
        else: content = "%" + s_content + "%"

        if s_comment == " ": comment = ""
        elif s_comment == "Select...": comment = "%"
        else: comment = "%" + s_comment + "%"


        # Query books by filter parameters
        rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                           authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                           languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                           forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE sector LIKE :sector AND new_sector LIKE :new_sector AND \
                           sector_name LIKE :sector_name AND author LIKE :author AND title LIKE :title AND edition LIKE :edition AND firstY LIKE :firstY AND ourY LIKE :ourY AND language LIKE :language AND country LIKE :country AND fict_fact LIKE :fict_fact AND \
                           art_other LIKE :art_other AND form LIKE :form AND content LIKE :content AND comment LIKE :comment", sector=sector, new_sector=new_sector, sector_name=sector_name, author=author, title=title, edition=edition,
                           firstY=firstY, ourY=ourY, language=language, country=country, fict_fact=fict_fact, art_other=art_other, form=form, content=content, comment=comment)

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

        # Populate results table
        for row in range(items):
            sector = rows[row]["sector"]
            sectors.append(sector)
            new_sector = rows[row]["new_sector"]
            new_sectors.append(new_sector)
            sector_name = rows[row]["sector_name"]
            sector_names.append(sector_name)
            author = rows[row]["author"]
            authors.append(author)
            title = rows[row]["title"]
            titles.append(title)
            edition = rows[row]["edition"]
            editions.append(edition)
            firstY = rows[row]["firstY"]
            firstYs.append(firstY)
            ourY = rows[row]["ourY"]
            ourYs.append(ourY)
            language = rows[row]["language"]
            languages.append(language)
            country = rows[row]["country"]
            countries.append(country)
            fict_fact = rows[row]["fict_fact"]
            fict_facts.append(fict_fact)
            art_other = rows[row]["art_other"]
            art_others.append(art_other)
            form = rows[row]["form"]
            forms.append(form)
            content = rows[row]["content"]
            contents.append(content)
            comment = rows[row]["comment"]
            comments.append(comment)

        return render_template("index.html", all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names, nb_sector_names=nb_sector_names,
                                s_author=s_author, s_title=s_title, all_editions=all_editions, nb_editions=nb_editions, s_firstY=s_firstY, s_ourY=s_ourY, all_languages=all_languages, nb_languages=nb_languages,
                                all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts, all_art_others=all_art_others, nb_art_others=nb_art_others,
                                all_forms=all_forms, nb_forms=nb_forms, all_contents=all_contents, nb_contents=nb_contents, s_comment=s_comment, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors,
                                sector_names=sector_names, authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages, countries=countries, fict_facts=fict_facts,
                                art_others=art_others, forms=forms, contents=contents, comments=comments)

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Reset all s_ input fields to "Select..."
        s_author = ""
        s_title = ""
        s_firstY = ""
        s_ourY = ""
        s_comment = ""

        # Get all existing sector categories
        lines = db.execute("SELECT sector FROM sectors")
        # Create list of dropdown menu options
        all_sectors = []
        line = 0
        nb = len(lines)
        nb_sectors = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            sector = lines[line]["sector"]
            all_sectors.append(sector)
        # Sort options and store in temporary sorted list
        all_sectors.sort()
        sorted_all_sectors = all_sectors
        all_sectors = []
        # Store "Select..." as default dropdown option
        sector = "Select..."
        all_sectors.append(sector)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            sector = sorted_all_sectors[line]
            all_sectors.append(sector)

        # Get all existing new_sector categories
        lines = db.execute("SELECT new_sector FROM new_sectors")
        # Create list of items to be displayed
        all_new_sectors = []
        line = 0
        nb = len(lines)
        nb_new_sectors = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            new_sector = lines[line]["new_sector"]
            all_new_sectors.append(new_sector)
        # Sort options and store in temporary sorted list
        all_new_sectors.sort()
        sorted_all_new_sectors = all_new_sectors
        all_new_sectors = []
        # Store "Select..." as default dropdown option
        new_sector = "Select..."
        all_new_sectors.append(new_sector)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            new_sector = sorted_all_new_sectors[line]
            all_new_sectors.append(new_sector)

        # Get all existing sector_name categories
        lines = db.execute("SELECT sector_name FROM sector_names")
        # Create list of items to be displayed
        all_sector_names = []
        line = 0
        nb = len(lines)
        nb_sector_names = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            sector_name = lines[line]["sector_name"]
            all_sector_names.append(sector_name)
        # Sort options and store in temporary sorted list
        all_sector_names.sort()
        sorted_all_sector_names = all_sector_names
        all_sector_names = []
        # Store "Select..." as default dropdown option
        sector_name = "Select..."
        all_sector_names.append(sector_name)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            sector_name = sorted_all_sector_names[line]
            all_sector_names.append(sector_name)

        # Get all existing edition categories
        lines = db.execute("SELECT edition FROM editions")
        # Create list of items to be displayed
        all_editions = []
        line = 0
        nb = len(lines)
        nb_editions = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            edition = lines[line]["edition"]
            all_editions.append(edition)
        # Sort options and store in temporary sorted list
        all_editions.sort()
        sorted_all_editions = all_editions
        all_editions = []
        # Store "Select..." as default dropdown option
        edition = "Select..."
        all_editions.append(edition)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            edition = sorted_all_editions[line]
            all_editions.append(edition)

        # Get all existing language categories
        lines = db.execute("SELECT language FROM languages")
        # Create list of items to be displayed
        all_languages = []
        line = 0
        nb = len(lines)
        nb_languages = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            language = lines[line]["language"]
            all_languages.append(language)
        # Sort options and store in temporary sorted list
        all_languages.sort()
        sorted_all_languages = all_languages
        all_languages = []
        # Store "Select..." as default dropdown option
        language = "Select..."
        all_languages.append(language)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            language = sorted_all_languages[line]
            all_languages.append(language)

        # Get all existing country categories
        lines = db.execute("SELECT country FROM countries")
        # Create list of items to be displayed
        all_countries = []
        line = 0
        nb = len(lines)
        nb_countries = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            country = lines[line]["country"]
            all_countries.append(country)
        # Sort options and store in temporary sorted list
        all_countries.sort()
        sorted_all_countries = all_countries
        all_countries = []
        # Store "Select..." as default dropdown option
        country = "Select..."
        all_countries.append(country)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            country = sorted_all_countries[line]
            all_countries.append(country)

        # Get all existing fict_fact categories
        lines = db.execute("SELECT fict_fact FROM fict_facts")
        # Create list of items to be displayed
        all_fict_facts = []
        line = 0
        nb = len(lines)
        nb_fict_facts = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            fict_fact = lines[line]["fict_fact"]
            all_fict_facts.append(fict_fact)
        # Sort options and store in temporary sorted list
        all_fict_facts.sort()
        sorted_all_fict_facts = all_fict_facts
        all_fict_facts = []
        # Store "Select..." as default dropdown option
        fict_fact = "Select..."
        all_fict_facts.append(fict_fact)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            fict_fact = sorted_all_fict_facts[line]
            all_fict_facts.append(fict_fact)

        # Get all existing art_other categories
        lines = db.execute("SELECT art_other FROM art_others")
        # Create list of items to be displayed
        all_art_others = []
        line = 0
        nb = len(lines)
        nb_art_others = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            art_other = lines[line]["art_other"]
            all_art_others.append(art_other)
        # Sort options and store in temporary sorted list
        all_art_others.sort()
        sorted_all_art_others = all_art_others
        all_art_others = []
        # Store "Select..." as default dropdown option
        art_other = "Select..."
        all_art_others.append(art_other)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            art_other = sorted_all_art_others[line]
            all_art_others.append(art_other)

        # Get all existing form categories
        lines = db.execute("SELECT form FROM forms")
        # Create list of items to be displayed
        all_forms = []
        line = 0
        nb = len(lines)
        nb_forms = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            form = lines[line]["form"]
            all_forms.append(form)
        # Sort options and store in temporary sorted list
        all_forms.sort()
        sorted_all_forms = all_forms
        all_forms = []
        # Store "Select..." as default dropdown option
        form = "Select..."
        all_forms.append(form)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            form = sorted_all_forms[line]
            all_forms.append(form)

        # Get all existing content categories
        lines = db.execute("SELECT content FROM contents")
        # Create list of items to be displayed
        all_contents = []
        line = 0
        nb = len(lines)
        nb_contents = nb + 1
        # Populate dropdown menu
        for line in range(nb):
            content = lines[line]["content"]
            all_contents.append(content)
        # Sort options and store in temporary sorted list
        all_contents.sort()
        sorted_all_contents = all_contents
        all_contents = []
        # Store "Select..." as default dropdown option
        content = "Select..."
        all_contents.append(content)
        # Re-populate so that Select... is first option and then sorted list
        for line in range(nb):
            content = sorted_all_contents[line]
            all_contents.append(content)

        # Display all books
        rows = db.execute("SELECT * FROM books JOIN sectors ON books.sect_id = sectors.sect_id JOIN new_sectors ON books.new_sect_id = new_sectors.new_sect_id JOIN sector_names ON books.sect_name_id = sector_names.sect_name_id JOIN \
                       authors ON books.author_id = authors.author_id JOIN editions ON books.ed_id = editions.ed_id JOIN firstYs ON books.firstY_id = firstYs.firstY_id JOIN ourYs ON books.ourY_id = ourYs.ourY_id JOIN \
                       languages ON books.lang_id = languages.lang_id JOIN countries ON books.ctry_id = countries.ctry_id JOIN fict_facts ON books.fict_id = fict_facts.fict_id JOIN art_others ON books.art_id = art_others.art_id JOIN \
                       forms ON books.form_id = forms.form_id JOIN contents ON books.cont_id = contents.cont_id JOIN comments ON books.comment_id = comments.comment_id WHERE author LIKE :author", author='%Rudolf%')

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

        # Populate results table
        for row in range(items):
            sector = rows[row]["sector"]
            sectors.append(sector)
            new_sector = rows[row]["new_sector"]
            new_sectors.append(new_sector)
            sector_name = rows[row]["sector_name"]
            sector_names.append(sector_name)
            author = rows[row]["author"]
            authors.append(author)
            title = rows[row]["title"]
            titles.append(title)
            edition = rows[row]["edition"]
            editions.append(edition)
            firstY = rows[row]["firstY"]
            firstYs.append(firstY)
            ourY = rows[row]["ourY"]
            ourYs.append(ourY)
            language = rows[row]["language"]
            languages.append(language)
            country = rows[row]["country"]
            countries.append(country)
            fict_fact = rows[row]["fict_fact"]
            fict_facts.append(fict_fact)
            art_other = rows[row]["art_other"]
            art_others.append(art_other)
            form = rows[row]["form"]
            forms.append(form)
            content = rows[row]["content"]
            contents.append(content)
            comment = rows[row]["comment"]
            comments.append(comment)

        return render_template("index.html", all_sectors=all_sectors, nb_sectors=nb_sectors, all_new_sectors=all_new_sectors, nb_new_sectors=nb_new_sectors, all_sector_names=all_sector_names, nb_sector_names=nb_sector_names,
                                s_author=s_author, s_title=s_title, all_editions=all_editions, nb_editions=nb_editions, s_firstY=s_firstY, s_ourY=s_ourY, all_languages=all_languages, nb_languages=nb_languages,
                                all_countries=all_countries, nb_countries=nb_countries, all_fict_facts=all_fict_facts, nb_fict_facts=nb_fict_facts, all_art_others=all_art_others, nb_art_others=nb_art_others,
                                all_forms=all_forms, nb_forms=nb_forms, all_contents=all_contents, nb_contents=nb_contents, s_comment=s_comment, items=items, rows=rows, sectors=sectors, new_sectors=new_sectors,
                                sector_names=sector_names, authors=authors, titles=titles, editions=editions, firstYs=firstYs, ourYs=ourYs, languages=languages, countries=countries, fict_facts=fict_facts,
                                art_others=art_others, forms=forms, contents=contents, comments=comments)

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
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to index page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/location", methods=["GET", "POST"])
@login_required
def location():
    """Defines sector codes"""
    rows = db.execute("SELECT * FROM locations")

    locations = []
    codes = []
    racks = []
    shelves = []
    row = 0
    items = len(rows)

    for row in range(items):
        code = rows[row]["code"]
        codes.append(code)
        rack = rows[row]["rack"]
        racks.append(rack)
        shelf = rows[row]["shelf"]
        shelves.append(shelf)

    return render_template("location.html", locations=locations, codes=codes, racks=racks, shelves=shelves, items=items)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
