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
# db.execute("CREATE TABLE titles (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT, author_id INTEGER, FOREIGN KEY (author_id) REFERENCES author(author_id))")
# db.execute("CREATE TABLE sectors (sect_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sector TEXT)")
# db.execute("CREATE TABLE new_sectors (new_sect_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, new_sector TEXT)")
# db.execute("CREATE TABLE sector_names (sect_name_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sector_name TEXT)")
# db.execute("CREATE TABLE locations (loc_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, code TEXT, rack TEXT, shelf TEXT)")

# SELECT * FROM shows WHERE id IN (SELECT show_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = "Ellen DeGeneres"))


# # Open CSV file
# with open("Databaza.csv", newline="") as file:

#     # Create DictReader
#     reader = csv.DictReader(file, delimiter=",")

#     # Iterate over CSV file
#     for row in reader:

#         # Query database for sector
#         rows = db.execute("SELECT * FROM sectors WHERE sector = :s", s=row["Sektor"])
#         # Check that sector does not exist
#         if len(rows) == 0:
#             # Insert sector
#             db.execute("INSERT INTO sectors (sector) VALUES (?)", row["Sektor"])
#         # Identify corresponding sect_id and store in variable to be used in insert into books
#         sector = db.execute("SELECT sect_id FROM sectors WHERE sector = :s", s=row["Sektor"])


#         # Query database for new_sector
#         rows = db.execute("SELECT * FROM new_sectors WHERE new_sector = :n", n=row["Nový sektor"])
#         # Check that new_sector does not exist
#         if len(rows) == 0:
#             # Insert new_sector
#             db.execute("INSERT INTO new_sectors (new_sector) VALUES (?)", row["Nový sektor"])
#         # Identify new_sect_id
#         new_sector = db.execute("SELECT new_sect_id FROM new_sectors WHERE new_sector = :n", n=row["Nový sektor"])


#         # Query database for sector_name
#         rows = db.execute("SELECT * FROM sector_names WHERE sector_name = :s", s=row["Názov sektoru"])
#         # Check that sector_name does not exist
#         if len(rows) == 0:
#             # Insert sector_name
#             db.execute("INSERT INTO sector_names (sector_name) VALUES (?)", row["Názov sektoru"])
#         # Identify sect_name_id
#         sector_name = db.execute("SELECT sect_name_id FROM sector_names WHERE sector_name = :s", s=row["Názov sektoru"])


#         # Query database for author
#         rows = db.execute("SELECT * FROM authors WHERE author = :a", a=row["Autor"])
#         # Check that author does not exist
#         if len(rows) == 0:
#             # Insert author
#             db.execute("INSERT INTO authors (author) VALUES (?)", row["Autor"])
#         # Identify author_id
#         author = db.execute("SELECT author_id FROM authors WHERE author = :a", a=row["Autor"])


#         # Query database for edition
#         rows = db.execute("SELECT * FROM editions WHERE edition = :e", e=row["Edícia"])
#         # Check that edition does not exist
#         if len(rows) == 0:
#             # Insert edition
#             db.execute("INSERT INTO editions (edition) VALUES (?)", row["Edícia"])
#         # Identify ed_id
#         edition = db.execute("SELECT ed_id FROM editions WHERE edition = :e", e=row["Edícia"])


#         # Query database for firstY
#         rows = db.execute("SELECT * FROM firstYs WHERE firstY = :f", f=row["Rok 1. vydania"])
#         # Check that firstY does not exist
#         if len(rows) == 0:
#             # Insert firstY
#             db.execute("INSERT INTO firstYs (firstY) VALUES (?)", row["Rok 1. vydania"])
#         # Identify firstY_id
#         firstY = db.execute("SELECT firstY_id FROM firstYs WHERE firstY = :f", f=row["Rok 1. vydania"])


#         # Query database for ourY
#         rows = db.execute("SELECT * FROM ourYs WHERE ourY = :o", o=row["Rok nášho vydania"])
#         # Check that ourY does not exist
#         if len(rows) == 0:
#             # Insert ourY
#             db.execute("INSERT INTO ourYs (ourY) VALUES (?)", row["Rok nášho vydania"])
#         # Identify ourY_id
#         ourY = db.execute("SELECT ourY_id FROM ourYs WHERE ourY = :o", o=row["Rok nášho vydania"])


#         # Query database for language
#         rows = db.execute("SELECT * FROM languages WHERE language = :l", l=row["Jazyk"])
#         # Check that language does not exist
#         if len(rows) == 0:
#             # Insert language
#             db.execute("INSERT INTO languages (language) VALUES (?)", row["Jazyk"])
#         # Identify lang_id
#         language = db.execute("SELECT lang_id FROM languages WHERE language = :l", l=row["Jazyk"])


#         # Query database for country
#         rows = db.execute("SELECT * FROM countries WHERE country = :c", c=row["Krajina"])
#         # Check that country does not exist
#         if len(rows) == 0:
#             # Insert country
#             db.execute("INSERT INTO countries (country) VALUES (?)", row["Krajina"])
#         # Identify ctry_id
#         country = db.execute("SELECT ctry_id FROM countries WHERE country = :c", c=row["Krajina"])


#         # Query database for fict_fact
#         rows = db.execute("SELECT * FROM fict_facts WHERE fict_fact = :f", f=row["Beletria / Fakty"])
#         # Check that fict_fact does not exist
#         if len(rows) == 0:
#             # Insert fict_fact
#             db.execute("INSERT INTO fict_facts (fict_fact) VALUES (?)", row["Beletria / Fakty"])
#         # Identify fict_id
#         fict_fact = db.execute("SELECT fict_id FROM fict_facts WHERE fict_fact = :f", f=row["Beletria / Fakty"])


#         # Query database for art_other
#         rows = db.execute("SELECT * FROM art_others WHERE art_other = :a", a=row["Umenie / Ine"])
#         # Check that art_other does not exist
#         if len(rows) == 0:
#             # Insert art_other
#             db.execute("INSERT INTO art_others (art_other) VALUES (?)", row["Umenie / Ine"])
#         # Identify art_id
#         art_other = db.execute("SELECT art_id FROM art_others WHERE art_other = :a", a=row["Umenie / Ine"])


#         # Query database for form
#         rows = db.execute("SELECT * FROM forms WHERE form = :f", f=row["Format"])
#         # Check that form does not exist
#         if len(rows) == 0:
#             # Insert form
#             db.execute("INSERT INTO forms (form) VALUES (?)", row["Format"])
#         # Identify form_id
#         form = db.execute("SELECT form_id FROM forms WHERE form = :f", f=row["Format"])


#         # Query database for content
#         rows = db.execute("SELECT * FROM contents WHERE content = :c", c=row["Obsah"])
#         # Check that content does not exist
#         if len(rows) == 0:
#             # Insert content
#             db.execute("INSERT INTO contents (content) VALUES (?)", row["Obsah"])
#         # Identify cont_id
#         content = db.execute("SELECT cont_id FROM contents WHERE content = :c", c=row["Obsah"])


#         # Query database for comment
#         rows = db.execute("SELECT * FROM comments WHERE comment = :c", c=row["Poznamka"])
#         # Check that comment does not exist
#         if len(rows) == 0:
#             # Insert comment
#             db.execute("INSERT INTO comments (comment) VALUES (?)", row["Poznamka"])
#         # Identify comment_id
#         comment = db.execute("SELECT comment_id FROM comments WHERE comment = :c", c=row["Poznamka"])


#         db.execute("INSERT INTO books (sect_id, new_sect_id, sect_name_id, author_id, title, ed_id, firstY_id, ourY_id, lang_id, ctry_id, fict_id, art_id, form_id, cont_id, comment_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#                   sector[0]["sect_id"], new_sector[0]["new_sect_id"], sector_name[0]["sect_name_id"], author[0]["author_id"], row["Názov"], edition[0]["ed_id"], firstY[0]["firstY_id"], ourY[0]["ourY_id"],
#                   language[0]["lang_id"], country[0]["ctry_id"], fict_fact[0]["fict_id"], art_other[0]["art_id"], form[0]["form_id"], content[0]["cont_id"], comment[0]["comment_id"])

# Open CSV file
with open("Sektory.csv", newline="") as file:

    # Create DictReader
    reader = csv.DictReader(file, delimiter=",")

    # Iterate over CSV file
    for row in reader:
        db.execute("INSERT INTO locations (code, rack, shelf) VALUES (?, ?, ?)", row["Kod"], row["Skrina"], row["Policka"])