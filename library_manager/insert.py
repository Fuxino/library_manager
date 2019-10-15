#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QMessageBox,\
        QHBoxLayout, QVBoxLayout, QFormLayout, QStackedLayout
from PyQt5.QtCore import Qt

from mysql.connector import Error

import library_manager._globals as _globals

try:
    from isbnlib import canonical, is_isbn10, is_isbn13

    isbn_check = True
except:
    isbn_check = False

# Form to insert books
class InsertBookForm(QWidget):

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
        self.book_insert = InsertBookForm(self.insert_record)
        self.author_insert = InsertAuthorForm(self.insert_record)
        self.publisher_insert = InsertPublisherForm(self.insert_record)
        self.series_insert = InsertSeriesForm(self.insert_record)

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
        clear_button.clicked.connect(self.clear_text)

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
    def clear_text(self):
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
        # Clear all fields
        self.clear_text()

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
                if isbn_check:
                    if '-' in isbn:
                        isbn = canonical(isbn)
                    if len(isbn) == 10:
                        if not is_isbn10(isbn):
                            # Show an error if the ISBN is invalid
                            error = QMessageBox()
                            error.setIcon(QMessageBox.Critical)
                            error.setWindowTitle('Error')
                            error.setText('The ISBN inserted is invalid. Operation failed.')
                            error.setStandardButtons(QMessageBox.Ok)
                            error.exec_()

                            return
                    elif len(isbn) == 13:
                        if not is_isbn13(isbn):
                            # Show an error if the ISBN is invalid
                            error = QMessageBox()
                            error.setIcon(QMessageBox.Critical)
                            error.setWindowTitle('Error')
                            error.setText('The ISBN inserted is invalid. Operation failed.')
                            error.setStandardButtons(QMessageBox.Ok)
                            error.exec_()

                            return
                    else:
                        # Show an error if the ISBN is invalid
                        error = QMessageBox()
                        error.setIcon(QMessageBox.Critical)
                        error.setWindowTitle('Error')
                        error.setText('The ISBN inserted is invalid. Operation failed.')
                        error.setStandardButtons(QMessageBox.Ok)
                        error.exec_()

                        return
            if title == '':
                # Title cannot be NULL, show error
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Title cannot be NULL. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                return
            if author == '':
                # Author cannot be NULL, show error
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Author cannot be NULL. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

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
            mySql_select_query = """SELECT Id FROM Authors WHERE Name LIKE %s"""
            _globals.cursor.execute(mySql_select_query, ('%'+author+'%',))
            author_id = _globals.cursor.fetchall()
            if len(author_id) == 0:
                # Author cannot be NULL, show error
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Author not found in Authors table. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                return
            elif len(author_id) == 1:
                author = author_id[0][0]
            else:
                # Show warning if string matches multiple authors
                warning = QMessageBox()
                warning.setIcon(QMessageBox.Information)
                warning.setWindowTitle('Warning')
                warning.setText('String matches multiple authors. Using exact match')
                warning.setStandardButtons(QMessageBox.Ok)
                warning.exec_()

                # Get Author Id from Name using exact match
                mySql_select_query = """SELECT Id FROM Authors WHERE Name=%s"""
                _globals.cursor.execute(mySql_select_query, (author,))
                author_id = _globals.cursor.fetchall()
                if len(author_id) == 0:
                    # Author cannot be NULL, show error
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setWindowTitle('Error')
                    error.setText('No exact match found in table Authors. Operation failed')
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()

                    return
                elif len(author_id) == 1:
                    author = author_id[0][0]

            # Get Publisher Id from Name
            if publisher is not None:
                mySql_select_query = """SELECT Id FROM Publishers WHERE Name LIKE %s"""
                _globals.cursor.execute(mySql_select_query, ('%'+publisher+'%',))
                publisher_id = _globals.cursor.fetchall()
                if len(publisher_id) == 0:
                    publisher = None
                    # Show warning if string doesn't match any Publisher
                    warning = QMessageBox()
                    warning.setIcon(QMessageBox.Warning)
                    warning.setWindowTitle('Warning')
                    warning.setText('Publisher not found, set to \'NULL\'')
                    warning.setStandardButtons(QMessageBox.Ok)
                    warning.exec_()
                elif len(publisher_id) == 1:
                    publisher = publisher_id[0][0]
                else:
                    # Show warning if string matches multiple publishers
                    warning = QMessageBox()
                    warning.setIcon(QMessageBox.Information)
                    warning.setWindowTitle('Warning')
                    warning.setText('String matches multiple publishers. Using exact match')
                    warning.setStandardButtons(QMessageBox.Ok)
                    warning.exec_()

                    # Get Publisher Id from Name using exact match
                    mySql_select_query = """SELECT Id FROM Publishers WHERE Name=%s"""
                    _globals.cursor.execute(mySql_select_query, (publisher,))
                    publisher_id = _globals.cursor.fetchall()
                    if len(publisher_id) == 0:
                        publisher = None
                        # Show warning if exact match is not found
                        warning = QMessageBox()
                        warning.setIcon(QMessageBox.Warning)
                        warning.setWindowTitle('Warning')
                        warning.setText('Publisher not found, set to \'NULL\'')
                        warning.setStandardButtons(QMessageBox.Ok)
                        warning.exec_()
                    elif len(publisher_id) == 1:
                        publisher = publisher_id[0][0]

            # Get Series Id from Name
            if series is not None:
                mySql_select_query = """SELECT Id FROM Series WHERE Name LIKE %s"""
                _globals.cursor.execute(mySql_select_query, ('%'+series+'%',))
                series_id = _globals.cursor.fetchall()
                if len(series_id) == 0:
                    series = None
                    # Show warning if string doesn't match any Series
                    warning = QMessageBox()
                    warning.setIcon(QMessageBox.Warning)
                    warning.setWindowTitle('Warning')
                    warning.setText('Series not found, set to \'NULL\'')
                    warning.setStandardButtons(QMessageBox.Ok)
                    warning.exec_()
                elif len(series_id) == 1:
                    series = series_id[0][0]
                else:
                    # Show warning is string matches multiple Series
                    warning = QMessageBox()
                    warning.setIcon(QMessageBox.Information)
                    warning.setWindowTitle('Warning')
                    warning.setText('String matches multiple series. Using exact match')
                    warning.setStandardButtons(QMessageBox.Ok)
                    warning.exec_()

                    # Get Series Id from Name using exact match
                    mySql_select_query = """SELECT Id FROM Series WHERE Name=%s"""
                    _globals.cursor.execute(mySql_select_query, (series,))
                    series_id = _globals.cursor.fetchall()
                    if len(series_id) == 0:
                        series = None
                        # Show warning if exact match is not found
                        warning = QMessageBox()
                        warning.setIcon(QMessageBox.Warning)
                        warning.setWindowTitle('Warning')
                        warning.setText('Series not found, set to \'NULL\'')
                        warning.setStandardButtons(QMessageBox.Ok)
                        warning.exec_()
                    elif len(series_id) == 1:
                        series = series_id[0][0]

            mySql_insert_query = """INSERT INTO Books(ISBN, Title, Author, OtherAuthors, Publisher, Series, Subseries,
                                                      Category, Language, Year, Pages, Owner,  Type)
                                    Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (isbn, title, author, otherauthors, publisher, series, subseries, category, language, year, pages, owner, booktype)

            # Execute the query
            try:
                _globals.cursor.execute(mySql_insert_query, values)
                _globals.connection.commit()

                # Show message if insertion succeeded
                info = QMessageBox()
                info.setIcon(QMessageBox.Information)
                info.setWindowTitle('Success')
                info.setText('Record inserted successfully into Books')
                info.setStandardButtons(QMessageBox.Ok)
                info.exec_()
            except Error as e:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

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
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Name cannot be NULL. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                return
            if gender == '':
                gender = None
            if nationality == '':
                nationality = None
            if birthyear == '':
                birthyear = None
            if deathyear == '':
                deathyear = None

            mySql_insert_query = """INSERT INTO Authors(Name, Gender, Nationality, BirthYear, DeathYear)
                                    Values(%s, %s, %s, %s, %s)"""
            values = (name, gender, nationality, birthyear, deathyear)

            # Execute the query
            try:
                _globals.cursor.execute(mySql_insert_query, values)
                _globals.connection.commit()

                # Show message if insertion succeeded
                info = QMessageBox()
                info.setIcon(QMessageBox.Information)
                info.setWindowTitle('Success')
                info.setText('Record inserted successfully into Authors')
                info.setStandardButtons(QMessageBox.Ok)
                info.exec_()
            except Error as e:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

        elif self.layout_insert.currentIndex() == 2:
            # Get text from insert form
            name = self.publisher_insert.name.text()

            # Set value to None if string is empty
            if name == '':
                # Name cannot be NULL, show error
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Name cannot be NULL. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                return

            mySql_insert_query = """INSERT INTO Publishers(Name) Values(%s)"""

            # Execute the query
            try:
                _globals.cursor.execute(mySql_insert_query, (name,))
                _globals.connection.commit()

                # Show message if insertion succeeded
                info = QMessageBox()
                info.setIcon(QMessageBox.Information)
                info.setWindowTitle('Success')
                info.setText('Record inserted successfully into Publishers')
                info.setStandardButtons(QMessageBox.Ok)
                info.exec_()
            except Error as e:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

        elif self.layout_insert.currentIndex() == 3:
            # Get text from insert form
            name = self.series_insert.name.text()
            author = self.series_insert.author.text()

            # Set values to None where strings are empty
            if name == '':
                # Name cannot be NULL, show error
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Name cannot be NULL. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                return

            if author == '':
                author = None

            if author != None:
                # Get Author Id from Name
                mySql_select_query = """SELECT Id FROM Authors WHERE Name LIKE %s"""
                _globals.cursor.execute(mySql_select_query, ('%'+author+'%',))
                author_id = _globals.cursor.fetchall()
                if len(author_id) == 0:
                    # Author cannot be NULL, show error
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setWindowTitle('Error')
                    error.setText('Author not found in Authors table. Operation failed')
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()

                    return
                elif len(author_id) == 1:
                    author = author_id[0][0]
                else:
                    # Show warning if string matches multiple authors
                    warning = QMessageBox()
                    warning.setIcon(QMessageBox.Information)
                    warning.setWindowTitle('Warning')
                    warning.setText('String matches multiple authors. Using exact match')
                    warning.setStandardButtons(QMessageBox.Ok)
                    warning.exec_()

                    # Get Author Id from Name using exact match
                    mySql_select_query = """SELECT Id FROM Authors WHERE Name=%s"""
                    _globals.cursor.execute(mySql_select_query, (author,))
                    author_id = _globals.cursor.fetchall()
                    if len(author_id) == 0:
                        # Author cannot be NULL, show error
                        error = QMessageBox()
                        error.setIcon(QMessageBox.Critical)
                        error.setWindowTitle('Error')
                        error.setText('No exact match found in table Authors. Operation failed')
                        error.setStandardButtons(QMessageBox.Ok)
                        error.exec_()

                        return
                    elif len(author_id) == 1:
                        author = author_id[0][0]

            mySql_insert_query = """INSERT INTO Series(Name, Author) Values(%s, %s)"""
            values = (name, author)

            # Execute the query
            try:
                _globals.cursor.execute(mySql_insert_query, values)
                _globals.connection.commit()

                # Show message if insertion succeeded
                info = QMessageBox()
                info.setIcon(QMessageBox.Information)
                info.setWindowTitle('Success')
                info.setText('Record inserted successfully into Series')
                info.setStandardButtons(QMessageBox.Ok)
                info.exec_()
            except Error as e:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
