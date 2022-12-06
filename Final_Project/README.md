Mata's Books

My parents have a lot of books and during the COVID quarantine, my sister and I set up to do an inventory of all those books,
donate those that don't spark joy and create a database for the remaining ~3,000 ones that do.
We did all the heavy lifting (literally!) of picking up every single book and inserting its details into an Excel spreadsheet.
This project is an upgrade to the original excel file - it is a web-based app, using Python, SQL (SQLite database), flask, HTML, CSS and Jinja.

Apart from Register, Log In and Log Out functions, Mata's Books contains 3 directly accessible pages:
The Home page, which contains the Main database where you can search for a book by any combination of the 15 pre-defined parameters
The Location page, a static table that lists the code names of all the racks and shelves in our apartment (i.e. locations of books)
The Admin page, where you can not only search like in the Main page, but also Insert new books and Edit or Delete existing books

The Main page is split into 2 parts: the search section on top and the results section at the bottom.
Out of the 15 searchable fields, 10 are dropdown and 5 are input fields.
The dropdowns are always sorted alphabetically with "Select..." the default option if no selection has been made.
If selection was made, the selected option will always be listed as default, followed by the "Select..." option and then followed by blank and
all the other pre-defined options sorted alphabetically.

The Admin page is split into 3 parts: The editing section on top, the search section in the middle and the results section at the bottom.
By default, the Editing section serves for Inserting a book and the button is called "Insert". When Inserting a new book, the only restriction
is that the book has to have a title, all other parameters can be blank - apology will be triggered in case of non-compliance.

All book results have 2 additional buttons not shown in the Home page - Edit and Delete. When clicked, all the 15
parameters of the given book will be displayed in the Editing section at the top of the page as default options of dropdown/input fields
and the button name will change to "Edit" or "Delete" respectively.

In case of Editing a book, "Select..." is not an option, since all fields have to be filled out (or left blank). So the dropdowns will contain
the default value, followed by blank and all the pre-defined options. If, however, the default option is blank, it will
not be followed by another blank, as that would look awkward, but by all the remaining alphabetical options.

In case of Deleting a book, the dropdowns will not be populated by any other option than the default option, because by deleting,
the user will remove the book with all its existing parameters, so giving dropdown options would not serve any purpose and would confuse the user.

Once you click on Insert, Edit or Delete in the Editing section, you are re-directed to a Confirmation page that lists all the details of your choice
and asks for your confirmation to proceed with modifying the database. From there you are either re-directed back to the Admin page
(if you clicked Cancel) or to an Update page that lists all the details of the database modification that has just been processed
(if you clicked Confirm). From there, clicking OK will re-direct you back to the Admin page.