import csv
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")    # foreign_keys=True)

db.execute("PRAGMA foreign_keys = ON")

# Create tables
# db.execute("CREATE TABLE geo (geo_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, country TEXT)")
# db.execute("CREATE TABLE language (lang_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, language TEXT)")
# db.execute("CREATE TABLE comment (comment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, comment TEXT)")
# db.execute("CREATE TABLE content (cont_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, content TEXT)")
# db.execute("CREATE TABLE format (form_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, format TEXT)")
# db.execute("CREATE TABLE art_other (art_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, art_other TEXT)")
# db.execute("CREATE TABLE fict_fact (fict_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, fict_fact TEXT)")
# db.execute("CREATE TABLE author (author_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, author TEXT)")
# db.execute("CREATE TABLE firstY (firstY_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, firstY TEXT)")
# db.execute("CREATE TABLE ourY (ourY_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, ourY TEXT)")
# db.execute("CREATE TABLE edition (ed_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, edition TEXT)")
# db.execute("CREATE TABLE title (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT, author_id INTEGER, FOREIGN KEY (author_id) REFERENCES author(author_id))")
# db.execute("CREATE TABLE sector (sect_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sector TEXT)")
# db.execute("CREATE TABLE new_sector (new_sect_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, new_sector TEXT)")
# db.execute("CREATE TABLE sector_name (sect_name_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sector_name TEXT)")

# Create tables
# db.execute("CREATE TABLE countries (ctry_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, country TEXT)")
# db.execute("CREATE TABLE languages (lang_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, language TEXT)")
# db.execute("CREATE TABLE comments (comment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, comment TEXT)")
# db.execute("CREATE TABLE contents (cont_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, content TEXT)")
# db.execute("CREATE TABLE forms (form_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, form TEXT)")
# db.execute("CREATE TABLE art_others (art_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, art_other TEXT)")
# db.execute("CREATE TABLE fict_facts (fict_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, fict_fact TEXT)")
# db.execute("CREATE TABLE authors (author_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, author TEXT)")
# db.execute("CREATE TABLE firstYs (firstY_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, firstY TEXT)")
# db.execute("CREATE TABLE ourYs (ourY_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, ourY TEXT)")
# db.execute("CREATE TABLE editions (ed_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, edition TEXT)")
db.execute("CREATE TABLE titles (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT, author_id INTEGER, FOREIGN KEY (author_id) REFERENCES author(author_id))")
# db.execute("CREATE TABLE sectors (sect_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sector TEXT)")
# db.execute("CREATE TABLE new_sectors (new_sect_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, new_sector TEXT)")
# db.execute("CREATE TABLE sector_names (sect_name_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sector_name TEXT)")

# SELECT * FROM shows WHERE id IN (SELECT show_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = "Ellen DeGeneres"))


# Open CSV file
with open("Test file.csv", newline="") as file:

    # Create DictReader
    reader = csv.DictReader(file, delimiter=",")

    # Iterate over CSV file
    for row in reader:

        # Query database for sector_name
        rows = db.execute("SELECT * FROM sector_names WHERE sector_name = :s", s=row["Názov sektoru"])
        # Check that sector_name does not exist
        if len(rows) == 0:
            # Insert sector_name
            db.execute("INSERT INTO sector_names (sector_name) VALUES (?)", row["Názov sektoru"])
        # Identify sect_name_id
        sector_name = db.execute("SELECT sect_name_id FROM sector_names WHERE sector_name = :s", s=row["Názov sektoru"])


        # Query database for author
        rows = db.execute("SELECT * FROM authors WHERE author = :a", a=row["Autor"])
        # Check that author does not exist
        if len(rows) == 0:
            # Insert author
            db.execute("INSERT INTO authors (author) VALUES (?)", row["Autor"])
        # Identify author_id
        author = db.execute("SELECT author_id FROM authors WHERE author = :a", a=row["Autor"])


        

        db.execute("INSERT INTO titles (sector, new_sector, sector_name, author, title, edition, firstY, ourY, language, country, fict_fact, art_other, form, content, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   sector[0]["sect_id"], new_sector[0]["new_sect_id"], sector_name[0]["sect_name_id"], author[0]["author_id"], row["Názov"], edition[0]["ed_id"], firstY[0]["firstY_id"], ourY[0]["ourY_id"],
                   language[0]["lang_id"], country[0]["ctry_id"], fict_fact[0]["fict_id"], art_other[0]["art_id"], form[0]["form_id"], content[0]["cont_id"], comment[0]["comment_id"])
