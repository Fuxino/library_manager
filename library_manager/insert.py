#!/usr/bin/env python3

"""Module for inserting records in the database

This module creates the layout and the functions that allow
to insert new records in the database.
"""

import os

from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton,\
        QHBoxLayout, QVBoxLayout, QFormLayout, QStackedLayout
from PyQt5.QtCore import Qt

from mysql.connector import Error

if os.name == 'nt':
    import _globals
    from info_dialogs import ErrorDialog, WarningDialog, InfoDialog
elif os.name == 'posix':
    import library_manager._globals as _globals
    from library_manager.info_dialogs import ErrorDialog, WarningDialog, InfoDialog

try:
    from isbnlib import canonical, is_isbn10, is_isbn13

    ISBN_CHECK = True
except ImportError:
    ISBN_CHECK = False

# Form to insert books
class InsertBookForm(QWidget):
    """Widget to insert new book records in the database."""

    def __init__(self, *args, **kwargs):
        super(InsertBookForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.isbn = QLineEdit()
        self.title = QLineEdit()
        self.author = QLineEdit()
        self.otherauthors = QLineEdit()
        self.publisher = QLineEdit()
        self.series = QLineEdit()
        self.subseries = QLineEdit()
        self.category = QLineEdit()
        self.language = QLineEdit()
        self.year = QLineEdit()
        self.pages = QLineEdit()
        self.owner = QComboBox()
        self.owner.addItem('')
        self.owner.addItem('Daniele')
        self.owner.addItem('Nicole')

        self.booktype = QComboBox()
        self.booktype.addItem('')
        self.booktype.addItem('Printed')
        self.booktype.addItem('E-book')

        # Add fields to layout
        layout.addRow('ISBN:', self.isbn)
        layout.addRow('Title:', self.title)
        layout.addRow('Author:', self.author)
        layout.addRow('OtherAuthors:', self.otherauthors)
        layout.addRow('Publisher:', self.publisher)
        layout.addRow('Series:', self.series)
        layout.addRow('Subseries:', self.subseries)
        layout.addRow('Category:', self.category)
        layout.addRow('Language:', self.language)
        layout.addRow('Year:', self.year)
        layout.addRow('Pages:', self.pages)
        layout.addRow('Owner:', self.owner)
        layout.addRow('Type:', self.booktype)

        # Set layout
        self.setLayout(layout)

# Form to insert authors
class InsertAuthorForm(QWidget):
    """Widget to insert new author records in the database."""

    def __init__(self, *args, **kwargs):
        super(InsertAuthorForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.name = QLineEdit()

        self.gender = QComboBox()
        self.gender.addItem('')
        self.gender.addItem('M')
        self.gender.addItem('F')
        self.gender.addItem('TM')
        self.gender.addItem('TW')
        self.gender.addItem('NB')

        self.nationality = QLineEdit()
        self.birthyear = QLineEdit()
        self.deathyear = QLineEdit()

        # Add fields to layout
        layout.addRow('Name:', self.name)
        layout.addRow('Gender:', self.gender)
        layout.addRow('Nationality:', self.nationality)
        layout.addRow('BirthYear', self.birthyear)
        layout.addRow('DeathYear:', self.deathyear)

        # Set layout
        self.setLayout(layout)

# Form to insert publishers
class InsertPublisherForm(QWidget):
    """Widget to insert new publisher records in the database."""

    def __init__(self, *args, **kwargs):
        super(InsertPublisherForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.name = QLineEdit()

        # Add field to layout
        layout.addRow('Name:', self.name)

        # Set layout
        self.setLayout(layout)

# Form to insert series
class InsertSeriesForm(QWidget):
    """Widget to insert new series records in the database."""

    def __init__(self, *args, **kwargs):
        super(InsertSeriesForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.name = QLineEdit()
        self.author = QLineEdit()

        # Add fields to layout
        layout.addRow('Name:', self.name)
        layout.addRow('Author:', self.author)

        # Set layout
        self.setLayout(layout)

# Insert into database widget
class InsertRecord(QWidget):
    """Main widget for inserting new records in the database

    This class creates a stacked layout containing four insert form widgets
    (Books, Authors, Publishers, Series) selected with a drop down menu.
    It implements the function to insert the record in the database.
    """

    def __init__(self, *args, **kwargs):
        super(InsertRecord, self).__init__(*args, **kwargs)

        # Define main layout
        layout = QVBoxLayout()

        # Create menu with the database tables
        menu = QComboBox()
        menu.addItem('Books')
        menu.addItem('Authors')
        menu.addItem('Publishers')
        menu.addItem('Series')
        menu.currentIndexChanged[str].connect(self.change_table)

        layout.addWidget(menu)

        # Define stacked layout for the different tables in database
        self.layout_insert = QStackedLayout()

        # Create insert form for each table in database
        self.book_insert = InsertBookForm()
        self.author_insert = InsertAuthorForm()
        self.publisher_insert = InsertPublisherForm()
        self.series_insert = InsertSeriesForm()

        # Add search forms to layout
        self.layout_insert.addWidget(self.book_insert)
        self.layout_insert.addWidget(self.author_insert)
        self.layout_insert.addWidget(self.publisher_insert)
        self.layout_insert.addWidget(self.series_insert)

        layout.addLayout(self.layout_insert)

        # Define layout for buttons
        layout_button = QHBoxLayout()
        # Create buttons
        insert_button = QPushButton('Insert')
        clear_button = QPushButton('Clear')
        insert_button.setMinimumSize(400, 30)
        insert_button.setMaximumSize(500, 30)
        clear_button.setMinimumSize(400, 30)
        clear_button.setMaximumSize(500, 30)

        # Define buttons behavior
        insert_button.clicked.connect(self.insert_record)
        clear_button.clicked.connect(self.clear)

        # Add buttons to layout
        layout_button.addWidget(insert_button)
        layout_button.addWidget(clear_button)
        layout_button.addWidget(QWidget())
        layout_button.addWidget(QWidget())
        layout_button.setAlignment(insert_button, Qt.AlignLeft)
        layout_button.setAlignment(clear_button, Qt.AlignLeft)
        layout.addLayout(layout_button)

        # Set main layout
        self.setLayout(layout)

    # Function to clear all insert fields
    def clear(self):
        """Clear the text in the insert form."""

        self.book_insert.isbn.clear()
        self.book_insert.title.clear()
        self.book_insert.author.clear()
        self.book_insert.otherauthors.clear()
        self.book_insert.publisher.clear()
        self.book_insert.series.clear()
        self.book_insert.subseries.clear()
        self.book_insert.category.clear()
        self.book_insert.language.clear()
        self.book_insert.year.clear()
        self.book_insert.pages.clear()
        self.book_insert.owner.setCurrentIndex(0)
        self.book_insert.booktype.setCurrentIndex(0)

        self.author_insert.name.clear()
        self.author_insert.gender.setCurrentIndex(0)
        self.author_insert.nationality.clear()
        self.author_insert.birthyear.clear()
        self.author_insert.deathyear.clear()

        self.publisher_insert.name.clear()

        self.series_insert.name.clear()
        self.series_insert.author.clear()

    # Function to set insert form according to database table selected
    def change_table(self, table_name):
        """Select the insert form (Books, Authors, Publishers or Series)."""

        # Clear all fields
        self.clear()

        # Books
        if table_name == 'Books':
            self.layout_insert.setCurrentIndex(0)
        # Authors
        elif table_name == 'Authors':
            self.layout_insert.setCurrentIndex(1)
        # Publishers
        elif table_name == 'Publishers':
            self.layout_insert.setCurrentIndex(2)
        # Series
        else:
            self.layout_insert.setCurrentIndex(3)

    # Function to insert record in database
    def insert_record(self):
        """Insert record in the database

        The method reads the informations in the active insert form
        (Books, Authors, Publishers or Series) and uses them to insert
        a new record in the database.
        """

        if self.layout_insert.currentIndex() == 0:
            # Get text from insert form
            isbn = self.book_insert.isbn.text()
            title = self.book_insert.title.text()
            author = self.book_insert.author.text()
            otherauthors = self.book_insert.otherauthors.text()
            publisher = self.book_insert.publisher.text()
            series = self.book_insert.series.text()
            subseries = self.book_insert.subseries.text()
            category = self.book_insert.category.text()
            language = self.book_insert.language.text()
            year = self.book_insert.year.text()
            pages = self.book_insert.pages.text()
            owner = self.book_insert.owner.currentText()
            booktype = self.book_insert.booktype.currentText()

            # Set values to None where strings are empty
            if isbn == '':
                isbn = None
            else:
                # Check is the ISBN is valid
                if ISBN_CHECK:
                    if '-' in isbn:
                        isbn = canonical(isbn)
                    if len(isbn) == 10:
                        if not is_isbn10(isbn):
                            # Show an error if the ISBN is invalid
                            error = ErrorDialog('The ISBN inserted is invalid. Operation failed.')
                            error.show()

                            return
                    elif len(isbn) == 13:
                        if not is_isbn13(isbn):
                            # Show an error if the ISBN is invalid
                            error = ErrorDialog('The ISBN inserted is invalid. Operation failed.')
                            error.show()

                            return
                    else:
                        # Show an error if the ISBN is invalid
                        error = ErrorDialog('The ISBN inserted is invalid. Operation failed.')
                        error.show()

                        return
            if title == '':
                # Title cannot be NULL, show error
                error = ErrorDialog('Title cannot be NULL. Operation failed.')
                error.show()

                return
            if author == '':
                # Author cannot be NULL, show error
                error = ErrorDialog('Author cannot be NULL. Operation failed')
                error.show()

                return
            if otherauthors == '':
                otherauthors = None
            if publisher == '':
                publisher = None
            if series == '':
                series = None
            if subseries == '':
                subseries = None
            if category == '':
                category = None
            if language == '':
                language = None
            if year == '':
                year = None
            if pages == '':
                pages = None
            if owner == '':
                owner = None
            if booktype == '':
                booktype = None

            # Get Author Id from Name
            mysql_select_query = """SELECT Id FROM Authors WHERE Name LIKE %s"""
            _globals.CURSOR.execute(mysql_select_query, ('%'+author+'%',))
            author_id = _globals.CURSOR.fetchall()
            if not author_id:
                # Author cannot be NULL, show error
                error = ErrorDialog('Author not found in Authors table. Operation failed')
                error.show()

                return

            if len(author_id) == 1:
                author = author_id[0][0]
            else:
                # Show warning if string matches multiple authors
                warning = WarningDialog('String matches multiple authors. Using exact match')
                warning.show()

                # Get Author Id from Name using exact match
                mysql_select_query = """SELECT Id FROM Authors WHERE Name=%s"""
                _globals.CURSOR.execute(mysql_select_query, (author,))
                author_id = _globals.CURSOR.fetchall()
                if not author_id:
                    # Author cannot be NULL, show error
                    error = ErrorDialog('No exact match found in table Authors. Operation failed')
                    error.show()

                    return

                if len(author_id) == 1:
                    author = author_id[0][0]

            # Get Publisher Id from Name
            if publisher is not None:
                mysql_select_query = """SELECT Id FROM Publishers WHERE Name LIKE %s"""
                _globals.CURSOR.execute(mysql_select_query, ('%'+publisher+'%',))
                publisher_id = _globals.CURSOR.fetchall()
                if not publisher_id:
                    publisher = None
                    # Show warning if string doesn't match any Publisher
                    warning = WarningDialog('Publisher not found, set to \'NULL\'')
                    warning.show()
                elif len(publisher_id) == 1:
                    publisher = publisher_id[0][0]
                else:
                    # Show warning if string matches multiple publishers
                    warning = WarningDialog('String matches multiple publishers. Using exact match')
                    warning.show()

                    # Get Publisher Id from Name using exact match
                    mysql_select_query = """SELECT Id FROM Publishers WHERE Name=%s"""
                    _globals.CURSOR.execute(mysql_select_query, (publisher,))
                    publisher_id = _globals.CURSOR.fetchall()
                    if not publisher_id:
                        publisher = None
                        # Show warning if exact match is not found
                        warning = WarningDialog('Publisher not found, set to \'NULL\'')
                        warning.show()
                    elif len(publisher_id) == 1:
                        publisher = publisher_id[0][0]

            # Get Series Id from Name
            if series is not None:
                mysql_select_query = """SELECT Id FROM Series WHERE Name LIKE %s"""
                _globals.CURSOR.execute(mysql_select_query, ('%'+series+'%',))
                series_id = _globals.CURSOR.fetchall()
                if not series_id:
                    series = None
                    # Show warning if string doesn't match any Series
                    warning = WarningDialog('Series not found, set to \'NULL\'')
                    warning.show()
                elif len(series_id) == 1:
                    series = series_id[0][0]
                else:
                    # Show warning is string matches multiple Series
                    warning = WarningDialog('String matches multiple series. Using exact match')
                    warning.show()

                    # Get Series Id from Name using exact match
                    mysql_select_query = """SELECT Id FROM Series WHERE Name=%s"""
                    _globals.CURSOR.execute(mysql_select_query, (series,))
                    series_id = _globals.CURSOR.fetchall()
                    if not series_id:
                        series = None
                        # Show warning if exact match is not found
                        warning = WarningDialog('Series not found, set to \'NULL\'')
                        warning.show()
                    elif len(series_id) == 1:
                        series = series_id[0][0]

            mysql_insert_query = """INSERT INTO Books(ISBN, Title, Author, OtherAuthors,
            Publisher, Series, Subseries, Category, Language, Year, Pages, Owner, Type)
            Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (isbn, title, author, otherauthors, publisher, series, subseries,\
                    category, language, year, pages, owner, booktype)

            # Execute the query
            try:
                _globals.CURSOR.execute(mysql_insert_query, values)
                _globals.CONNECTION.commit()

                # Show message if insertion succeeded
                info = InfoDialog('Record inserted successfully into Books')
                info.show()
            except Error as err:
                # Create error message box
                error = ErrorDialog(str(err))
                error.show()

        elif self.layout_insert.currentIndex() == 1:
            # Get text from insert form
            name = self.author_insert.name.text()
            gender = self.author_insert.gender.currentText()
            nationality = self.author_insert.nationality.text()
            birthyear = self.author_insert.birthyear.text()
            deathyear = self.author_insert.deathyear.text()

            # Set values to None where strings are empty
            if name == '':
                # Name cannot be NULL, show error
                error = ErrorDialog('Name cannot be NULL. Operation failed')
                error.show()

                return
            if gender == '':
                gender = None
            if nationality == '':
                nationality = None
            if birthyear == '':
                birthyear = None
            if deathyear == '':
                deathyear = None

            mysql_insert_query = """INSERT INTO Authors(Name, Gender, Nationality,
            BirthYear, DeathYear) Values(%s, %s, %s, %s, %s)"""
            values = (name, gender, nationality, birthyear, deathyear)

            # Execute the query
            try:
                _globals.CURSOR.execute(mysql_insert_query, values)
                _globals.CONNECTION.commit()

                # Show message if insertion succeeded
                info = InfoDialog('Record inserted successfully into Authors')
                info.show()
            except Error as err:
                # Create error message box
                error = ErrorDialog(str(err))
                error.show()

        elif self.layout_insert.currentIndex() == 2:
            # Get text from insert form
            name = self.publisher_insert.name.text()

            # Set value to None if string is empty
            if name == '':
                # Name cannot be NULL, show error
                error = ErrorDialog('Name cannot be NULL. Operation failed')
                error.show()

                return

            mysql_insert_query = """INSERT INTO Publishers(Name) Values(%s)"""

            # Execute the query
            try:
                _globals.CURSOR.execute(mysql_insert_query, (name,))
                _globals.CONNECTION.commit()

                # Show message if insertion succeeded
                info = InfoDialog('Record inserted successfully into Publishers')
                info.show()
            except Error as err:
                # Create error message box
                error = ErrorDialog(str(err))
                error.show()

        elif self.layout_insert.currentIndex() == 3:
            # Get text from insert form
            name = self.series_insert.name.text()
            author = self.series_insert.author.text()

            # Set values to None where strings are empty
            if name == '':
                # Name cannot be NULL, show error
                error = ErrorDialog('Name cannot be NULL. Operation failed')
                error.show()

                return

            if author == '':
                author = None

            if author is not None:
                # Get Author Id from Name
                mysql_select_query = """SELECT Id FROM Authors WHERE Name LIKE %s"""
                _globals.CURSOR.execute(mysql_select_query, ('%'+author+'%',))
                author_id = _globals.CURSOR.fetchall()
                if not author_id:
                    # Author cannot be NULL, show error
                    error = ErrorDialog('Author not found in Authors table. Operation failed')
                    error.show()

                    return

                if len(author_id) == 1:
                    author = author_id[0][0]
                else:
                    # Show warning if string matches multiple authors
                    warning = WarningDialog('String matches multiple authors. Using exact match')
                    warning.show()

                    # Get Author Id from Name using exact match
                    mysql_select_query = """SELECT Id FROM Authors WHERE Name=%s"""
                    _globals.CURSOR.execute(mysql_select_query, (author,))
                    author_id = _globals.CURSOR.fetchall()

                    if not author_id:
                        # Author cannot be NULL, show error
                        error = ErrorDialog('No exact match found in table Authors. ' +\
                                'Operation failed')
                        error.show()

                        return

                    if len(author_id) == 1:
                        author = author_id[0][0]

            mysql_insert_query = """INSERT INTO Series(Name, Author) Values(%s, %s)"""
            values = (name, author)

            # Execute the query
            try:
                _globals.CURSOR.execute(mysql_insert_query, values)
                _globals.CONNECTION.commit()

                # Show message if insertion succeeded
                info = InfoDialog('Record inserted successfully into Series')
                info.show()
            except Error as err:
                # Create error message box
                error = ErrorDialog(str(err))
                error.show()
