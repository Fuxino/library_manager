#!/usr/bin/python3

# Import libraries
import os

import sys
from sys import exit, argv

import subprocess
from subprocess import CalledProcessError, PIPE

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import mysql.connector
from mysql.connector import Error

if os.name == 'nt':
    from fbs_runtime.application_context.PyQt5 import ApplicationContext

# Login dialog box
class Login(QDialog):

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)

        # Set dialog title
        self.setWindowTitle('Login to Library')

        if os.name == 'nt':
            self.setWindowIcon(QIcon('Icon.ico'))
        elif os.name == 'posix':
            self.setWindowIcon(QIcon('/usr/share/icons/hicolor/32x32/apps/library_manager.png'))

        # Define layouts
        layout = QVBoxLayout()
        layout_login = QFormLayout()

        # Define login fields
        self.username = QLineEdit()
        self.password = QLineEdit()
        # Hide password when typing
        self.password.setEchoMode(QLineEdit.Password)
        self.host = QComboBox()
        self.host.addItem('192.168.0.100')
        self.host.addItem('localhost')

        # Add fields to layout
        layout_login.addRow(QLabel('Username:'), self.username)
        layout_login.addRow(QLabel('Password:'), self.password)
        layout_login.addRow(QLabel('Hostname:'), self.host)

        # Create buttons
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # Define button behavior
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.db_connect)
        buttonBox.rejected.connect(self.exit_program)

        # Add login form and button to main layout
        layout.addLayout(layout_login)
        layout.addWidget(buttonBox)

        # Set layout
        self.setLayout(layout)

    # Function to connect to the database
    def db_connect(self):
        try:
            # Global variable because we need them later
            global connection
            global cursor
            global hostname
            global user
            global pwd

            hostname = self.host.currentText()
            user = self.username.text()
            pwd = self.password.text()

            # Create connection
            connection = mysql.connector.connect(host=hostname,
                                                 database='Library',
                                                 user=user,
                                                 password=pwd)

            cursor = connection.cursor(prepared=True)

            # Close login dialog
            self.accept()

        # If error occurred during connection
        except Error as e:
            # Create error message box
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setWindowTitle('Error')
            error.setText(str(e))
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    # Function to exit the program
    def exit_program(self):
        exit(0)

# Form to search books
class SearchBookForm(QWidget):

    def __init__(self, query_db, *args, **kwargs):
        super(SearchBookForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.isbn = QLineEdit()
        self.isbn.returnPressed.connect(query_db)
        self.title = QLineEdit()
        self.title.returnPressed.connect(query_db)
        self.author = QLineEdit()
        self.author.returnPressed.connect(query_db)

        self.author_gender = QComboBox()
        self.author_gender.addItem('')
        self.author_gender.addItem('M')
        self.author_gender.addItem('F')
        self.author_gender.addItem('Other')

        self.author_nationality = QLineEdit()
        self.author_nationality.returnPressed.connect(query_db)
        self.publisher = QLineEdit()
        self.publisher.returnPressed.connect(query_db)
        self.series = QLineEdit()
        self.series.returnPressed.connect(query_db)

        self.category = QComboBox()
        self.category.addItem('')
        self.category.addItem('Non-fiction')
        self.category.addItem('Novel')
        self.category.addItem('Graphic novel')
        self.category.addItem('Short stories')
        self.category.addItem('Mythology')
        self.category.addItem('Fiction')
        self.category.addItem('Play')
        self.category.addItem('Poetry')
        self.category.addItem('Collection')
        self.category.addItem('Chronicle')
        self.category.addItem('Children\'s book')
        self.category.addItem('Textbook')

        self.language = QComboBox()
        self.language.addItem('')
        self.language.addItem('English')
        self.language.addItem('Italian')

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
        layout.addRow('Author\'s gender:', self.author_gender)
        layout.addRow('Author\'s nationality:', self.author_nationality)
        layout.addRow('Publisher:', self.publisher)
        layout.addRow('Series:', self.series)
        layout.addRow('Category:', self.category)
        layout.addRow('Language:', self.language)
        layout.addRow('Owner:', self.owner)
        layout.addRow('Type:', self.booktype)

        # Set layout
        self.setLayout(layout)

# Form to search authors
class SearchAuthorForm(QWidget):

    def __init__(self, query_db, *args, **kwargs):
        super(SearchAuthorForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.name = QLineEdit()
        self.name.returnPressed.connect(query_db)

        self.gender = QComboBox()
        self.gender.addItem('')
        self.gender.addItem('M')
        self.gender.addItem('F')
        self.gender.addItem('Other')

        self.nationality = QLineEdit()
        self.nationality.returnPressed.connect(query_db)

        # Add fields to layout
        layout.addRow('Name:', self.name)
        layout.addRow('Gender:', self.gender)
        layout.addRow('Nationality:', self.nationality)

        # Set layout
        self.setLayout(layout)

# Form to search publishers
class SearchPublisherForm(QWidget):

    def __init__(self, query_db, *args, **kwargs):
        super(SearchPublisherForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.name = QLineEdit()
        self.name.returnPressed.connect(query_db)

        # Add field to layout
        layout.addRow('Name:', self.name)

        # Set layout
        self.setLayout(layout)

# Form to search series
class SearchSeriesForm(QWidget):

    def __init__(self, query_db, *args, **kwargs):
        super(SearchSeriesForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.name = QLineEdit()
        self.name.returnPressed.connect(query_db)
        self.author = QLineEdit()
        self.author.returnPressed.connect(query_db)

        # Add fields to layout
        layout.addRow('Name:', self.name)
        layout.addRow('Author:', self.author)

        # Set layout
        self.setLayout(layout)

# Search database widget
class SearchDatabase(QWidget):

    def __init__(self, *args, **kwargs):
        super(SearchDatabase, self).__init__(*args, **kwargs)

        # Define main layout
        layout = QHBoxLayout()

        # Define layout for left part of the window
        layout_left = QVBoxLayout()

        # Create menu with the database tables
        menu = QComboBox()
        menu.addItem('Books')
        menu.addItem('Authors')
        menu.addItem('Publishers')
        menu.addItem('Series')
        menu.currentIndexChanged[str].connect(self.change_table)

        # Add menu to layout
        layout_left.addWidget(menu)

        # Create table to show database queries results
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(13)

        id_header = QTableWidgetItem('Id')
        isbn_header = QTableWidgetItem('ISBN')
        title_header = QTableWidgetItem('Title')
        author_header = QTableWidgetItem('Author')
        otherauthors_header = QTableWidgetItem('OtherAuthors')
        publisher_header = QTableWidgetItem('Publisher')
        series_header = QTableWidgetItem('Series')
        category_header = QTableWidgetItem('Category')
        language_header = QTableWidgetItem('Language')
        year_header = QTableWidgetItem('Year')
        pages_header = QTableWidgetItem('Pages')
        owner_header = QTableWidgetItem('Owner')
        type_header = QTableWidgetItem('Type')
        
        self.table.setHorizontalHeaderItem(0, id_header)
        self.table.setHorizontalHeaderItem(1, isbn_header)
        self.table.setHorizontalHeaderItem(2, title_header)
        self.table.setHorizontalHeaderItem(3, author_header)
        self.table.setHorizontalHeaderItem(4, otherauthors_header)
        self.table.setHorizontalHeaderItem(5, publisher_header)
        self.table.setHorizontalHeaderItem(6, series_header)
        self.table.setHorizontalHeaderItem(7, category_header)
        self.table.setHorizontalHeaderItem(8, language_header)
        self.table.setHorizontalHeaderItem(9, year_header)
        self.table.setHorizontalHeaderItem(10, pages_header)
        self.table.setHorizontalHeaderItem(11, owner_header)
        self.table.setHorizontalHeaderItem(12, type_header)

        self.table.resizeColumnsToContents()

        self.current_item = None

        self.table.cellDoubleClicked.connect(self.get_current_item)
        self.table.cellChanged.connect(self.update_db)

        # Add table to layout
        layout_left.addWidget(self.table)

        # Add buttons
        layout_button_l = QHBoxLayout()

        # Add backup and save buttons
        backup_button = QPushButton('Backup database')
        clear_button = QPushButton('Clear')
        save_button = QPushButton('Save to file')

        # Define buttons behavior
        backup_button.clicked.connect(self.backup_db)
        save_button.clicked.connect(self.save_to_file)
        clear_button.clicked.connect(self.clear)

        # Add buttons to layout
        layout_button_l.addWidget(backup_button)
        layout_button_l.addWidget(save_button)
        layout_button_l.addWidget(clear_button)
        layout_left.addLayout(layout_button_l)

        # Add left layout to main layout
        layout.addLayout(layout_left)

        # Define layout for right part of the window
        layout_right = QVBoxLayout()

        # Define stacked layout for the different tables in database
        self.layout_search = QStackedLayout()

        # Create search form for each table in database
        self.book_search = SearchBookForm(self.query_db)
        self.author_search = SearchAuthorForm(self.query_db)
        self.publisher_search = SearchPublisherForm(self.query_db)
        self.series_search = SearchSeriesForm(self.query_db)

        # Add search forms to layout
        self.layout_search.addWidget(self.book_search)
        self.layout_search.addWidget(self.author_search)
        self.layout_search.addWidget(self.publisher_search)
        self.layout_search.addWidget(self.series_search)

        # Add stacked layout to right layout
        layout_right.addLayout(self.layout_search)

        # Define layout for buttons
        layout_button_r = QHBoxLayout()
        # Create buttons
        search_button = QPushButton('Search')
        close_button = QPushButton('Exit')

        # Define buttons behavior
        search_button.clicked.connect(self.query_db)
        close_button.clicked.connect(self.exit_program)

        # Add buttons to layout
        layout_button_r.addWidget(search_button)
        layout_button_r.addWidget(close_button)
        layout_right.addLayout(layout_button_r)

        # Add right layout to main layout
        layout.addLayout(layout_right)

        # Set main layout
        self.setLayout(layout)

    # Function to clear all query result table and search fields 
    def clear(self):
        self.table.blockSignals(True)

        self.table.setRowCount(0)
        
        self.book_search.isbn.clear()
        self.book_search.title.clear()
        self.book_search.author.clear()
        self.book_search.author_gender.setCurrentIndex(0)
        self.book_search.author_nationality.clear()
        self.book_search.publisher.clear()
        self.book_search.series.clear()
        self.book_search.category.setCurrentIndex(0)
        self.book_search.language.setCurrentIndex(0)
        self.book_search.owner.setCurrentIndex(0)
        self.book_search.booktype.setCurrentIndex(0)

        self.author_search.name.clear()
        self.author_search.gender.setCurrentIndex(0)
        self.author_search.nationality.clear()

        self.publisher_search.name.clear()

        self.series_search.name.clear()
        self.series_search.author.clear()

        self.table.blockSignals(False)

    # Function to set table columns according to database table selected
    def change_table(self, table_name):
        self.clear()

        self.table.blockSignals(True)

        # Books
        if table_name == 'Books':
            self.table.setColumnCount(13)

            id_header = QTableWidgetItem('Id')
            isbn_header = QTableWidgetItem('ISBN')
            title_header = QTableWidgetItem('Title')
            author_header = QTableWidgetItem('Author')
            otherauthors_header = QTableWidgetItem('OtherAuthors')
            publisher_header = QTableWidgetItem('Publisher')
            series_header = QTableWidgetItem('Series')
            category_header = QTableWidgetItem('Category')
            language_header = QTableWidgetItem('Language')
            year_header = QTableWidgetItem('Year')
            pages_header = QTableWidgetItem('Pages')
            owner_header = QTableWidgetItem('Owner')
            type_header = QTableWidgetItem('Type')
        
            self.table.setHorizontalHeaderItem(0, id_header)
            self.table.setHorizontalHeaderItem(1, isbn_header)
            self.table.setHorizontalHeaderItem(2, title_header)
            self.table.setHorizontalHeaderItem(3, author_header)
            self.table.setHorizontalHeaderItem(4, otherauthors_header)
            self.table.setHorizontalHeaderItem(5, publisher_header)
            self.table.setHorizontalHeaderItem(6, series_header)
            self.table.setHorizontalHeaderItem(7, category_header)
            self.table.setHorizontalHeaderItem(8, language_header)
            self.table.setHorizontalHeaderItem(9, year_header)
            self.table.setHorizontalHeaderItem(10, pages_header)
            self.table.setHorizontalHeaderItem(11, owner_header)
            self.table.setHorizontalHeaderItem(12, type_header)

            self.table.resizeColumnsToContents()

            self.layout_search.setCurrentIndex(0)
        # Authors
        elif table_name == 'Authors':
            self.table.setColumnCount(6)

            id_header = QTableWidgetItem('Id')
            name_header = QTableWidgetItem('Name')
            gender_header = QTableWidgetItem('Gender')
            nationality_header = QTableWidgetItem('Nationality')
            birthyear_header = QTableWidgetItem('BirthYear')
            deathyear_header = QTableWidgetItem('DeathYear')
            
            self.table.setHorizontalHeaderItem(0, id_header)
            self.table.setHorizontalHeaderItem(1, name_header)
            self.table.setHorizontalHeaderItem(2, gender_header)
            self.table.setHorizontalHeaderItem(3, nationality_header)
            self.table.setHorizontalHeaderItem(4, birthyear_header)
            self.table.setHorizontalHeaderItem(5, deathyear_header)

            self.table.resizeColumnsToContents()

            self.layout_search.setCurrentIndex(1)
        # Publishers
        elif table_name == 'Publishers':
            self.table.setColumnCount(2)

            id_header = QTableWidgetItem('Id')
            name_header = QTableWidgetItem('Name')
            
            self.table.setHorizontalHeaderItem(0, id_header)
            self.table.setHorizontalHeaderItem(1, name_header)

            self.table.resizeColumnsToContents()

            self.layout_search.setCurrentIndex(2)
        # Series
        else:
            self.table.setColumnCount(3)

            id_header = QTableWidgetItem('Id')
            name_header = QTableWidgetItem('Name')
            author_header = QTableWidgetItem('Author')

            self.table.setHorizontalHeaderItem(0, id_header)
            self.table.setHorizontalHeaderItem(1, name_header)
            self.table.setHorizontalHeaderItem(2, author_header)

            self.table.resizeColumnsToContents()

            self.layout_search.setCurrentIndex(3)

        self.table.blockSignals(False)

    # Function to query the database
    def query_db(self):
        self.table.blockSignals(True)

        # Query Books
        if self.layout_search.currentIndex() == 0:
            query = 'SELECT Id, ISBN, Title, Author, OtherAuthors, Publisher, Series, \
                    Category, Language, Year, Pages, Owner, Type FROM Books WHERE '

            # Get text from search form
            isbn = self.book_search.isbn.text()
            title = self.book_search.title.text()
            author_n = self.book_search.author.text()
            author_g = self.book_search.author_gender.currentText()
            author_c = self.book_search.author_nationality.text()
            publisher = self.book_search.publisher.text()
            series = self.book_search.series.text()
            category = self.book_search.category.currentText()
            language = self.book_search.language.currentText()
            owner = self.book_search.owner.currentText()
            booktype = self.book_search.booktype.currentText()

            # Prepare SQL query
            if isbn != '':
                query = query + 'ISBN LIKE \'%' + isbn + '%\' AND '
            if title != '':
                query = query + 'Title LIKE \'%' + title + '%\' AND '
            if author_n != '':
                # Get Authors Id from Name
                mySql_select_query = """SELECT Id FROM Authors WHERE Name LIKE %s"""
                cursor.execute(mySql_select_query, ('%'+author_n+'%',))
                author = cursor.fetchall()
                if len(author) == 0:
                    author_id = 0
                else:
                    author_id = ''

                    i = 0
                    for row in author:
                        author_id = author_id + str(author[i][0]) + ', '
                        i = i + 1

                    author_id = author_id[:-2]

                query = query + '(Author IN (' + str(author_id) + ') OR OtherAuthors LIKE \'%' + author_n + '%\') AND '
            if author_g != '':
                # Get Authors Id from Gender
                if author_g == 'Other':
                    mySql_select_query = """SELECT Id FROM Authors WHERE Gender!='M' AND Gender!='F'"""
                    cursor.execute(mySql_select_query)
                    author = cursor.fetchall()
                    if len(author) == 0:
                        author_id = 0
                    else:
                        author_id = ''

                        i = 0
                        for row in author:
                            author_id = author_id + str(author[i][0]) + ', '
                            i= i + 1

                        author_id = author_id[:-2]

                    query = query + 'Author IN (' + str(author_id) + ') AND '
                else:
                    mySql_select_query = """SELECT Id FROM Authors WHERE Gender=%s"""
                    cursor.execute(mySql_select_query, (author_g,))
                    author = cursor.fetchall()
                    if len(author) == 0:
                        author_id = 0
                    else:
                        author_id = ''

                        i = 0
                        for row in author:
                            author_id = author_id + str(author[i][0]) + ', '
                            i = i + 1

                        author_id = author_id[:-2]

                    query = query + 'Author IN (' + str(author_id) + ') AND '
            if author_c != '':
                # Get Authors Id from Nationality
                mySql_select_query = """SELECT Id FROM Authors WHERE Nationality LIKE %s"""
                cursor.execute(mySql_select_query, ('%'+author_c+'%',))
                author = cursor.fetchall()
                if len(author) == 0:
                    author_id = 0
                else:
                    author_id = ''

                    i = 0
                    for row in author:
                        author_id = author_id + str(author[i][0]) + ', '
                        i = i + 1

                    author_id = author_id[:-2]

                query = query + 'Author IN (' + str(author_id) + ') AND '
            if publisher != '':
                # Get Publishers Id from Name
                mySql_select_query = """SELECT Id FROM Publishers WHERE Name LIKE %s"""
                cursor.execute(mySql_select_query, ('%'+publisher+'%',))
                publisher = cursor.fetchall()
                if len(publisher) == 0:
                    publisher_id = 0
                else:
                    publisher_id = ''

                    i = 0
                    for row in publisher:
                        publisher_id = publisher_id + str(publisher[i][0]) + ', '
                        i = i + 1

                    publisher_id = publisher_id[:-2]

                query = query + 'Publisher IN (' + str(publisher_id) + ') AND '
            if series != '':
                # Get Series Id from Name
                mySql_select_query = """SELECT Id FROM Series WHERE Name LIKE %s"""
                cursor.execute(mySql_select_query, ('%'+series+'%',))
                series = cursor.fetchall()
                if len(series) == 0:
                    series_id = 0
                else:
                    series_id = ''

                    i = 0
                    for row in series:
                        series_id = series_id + str(series[i][0]) + ', '
                        i = i + 1

                    series_id = series_id[:-2]

                query = query + 'Series IN (' + str(series_id) + ') AND '
            if category != '':
                query = query + 'Category LIKE \'%' + category + '%\' AND '
            if language != '':
                query = query + 'Language LIKE \'%' + language + '%\' AND '
            if owner != '':
                query = query + 'Owner LIKE \'%' + owner + '%\' AND '
            if booktype != '':
                query = query + 'Type LIKE \'%' + booktype + '%\' '

            # Remove trailing 'AND' and/or 'WHERE' from query
            if query[-4:] == 'AND ':
                query = query[:-4]

            if query[-6:] == 'WHERE ':
                query = query[:-6]

            try:
                # Execute the query
                cursor.execute(query)
                results = cursor.fetchall()

                # Clear the results table
                self.table.setRowCount(0)

                # Get values for each result of the query
                for row in results:
                    Id = row[0]
                    ISBN = row[1]
                    Title = row[2]
                    Author = row[3]
                    OtherAuthors = row[4]
                    Publisher = row[5]
                    Series = row[6]
                    Category = row[7]
                    Language = row[8]
                    Year = row[9]
                    Pages = row[10]
                    Owner = row[11]
                    Type = row[12]

                    # Get Author Name from Id
                    mySql_select_query = """SELECT Name FROM Authors WHERE Id = %s"""
                    cursor.execute(mySql_select_query, (Author,))
                    Author = cursor.fetchall()
                    Author = Author[0][0]

                    # Get Publisher Name from Id
                    if Publisher is not None:
                        mySql_select_query = """SELECT Name FROM Publishers WHERE Id = %s"""
                        cursor.execute(mySql_select_query, (Publisher,))
                        Publisher = cursor.fetchall()
                        Publisher = Publisher[0][0]

                    # Get Series Name from Id
                    if Series is not None:
                        mySql_select_query = """SELECT Name FROM Series WHERE Id = %s"""
                        cursor.execute(mySql_select_query, (Series,))
                        Series = cursor.fetchall()
                        Series = Series[0][0]

                    # If Year and/or Pages is NULL, show empty string
                    if Year == None:
                        Year = ''

                    if Pages == None:
                        Pages = ''

                    # Insert values in table
                    i = self.table.rowCount()
                    self.table.insertRow(i)

                    id_item = QTableWidgetItem(str(Id))
                    id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, QTableWidgetItem(ISBN))
                    self.table.setItem(i, 2, QTableWidgetItem(Title))
                    self.table.setItem(i, 3, QTableWidgetItem(Author))
                    self.table.setItem(i, 4, QTableWidgetItem(OtherAuthors))
                    self.table.setItem(i, 5, QTableWidgetItem(Publisher))
                    self.table.setItem(i, 6, QTableWidgetItem(Series))
                    self.table.setItem(i, 7, QTableWidgetItem(Category))
                    self.table.setItem(i, 8, QTableWidgetItem(Language))
                    self.table.setItem(i, 9, QTableWidgetItem(str(Year)))
                    self.table.setItem(i, 10, QTableWidgetItem(str(Pages)))
                    self.table.setItem(i, 11, QTableWidgetItem(Owner))
                    self.table.setItem(i, 12, QTableWidgetItem(Type))

                # Resize columns
                self.table.resizeColumnsToContents()

                if self.table.columnWidth(2) > 300:
                    self.table.setColumnWidth(2, 300)

                if self.table.columnWidth(4) > 300:
                    self.table.setColumnWidth(4, 300)

                # Sort table
                self.table.sortItems(9)
                self.table.sortItems(6)
                self.table.sortItems(3)
            except Error as e:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                self.table.blockSignals(False)

        # Query Authors
        elif self.layout_search.currentIndex() == 1:
            query = 'SELECT Id, Name, Gender, Nationality, BirthYear, DeathYear FROM Authors WHERE '

            # Get text from search form
            name = self.author_search.name.text()
            gender = self.author_search.gender.currentText()
            nationality = self.author_search.nationality.text()

            # Prepare SQL query
            if name != '':
                query = query + 'Name LIKE \'%' + name + '%\' AND '
            if gender != '':
                if gender == 'Other':
                    query = query + 'Gender!=\'M\' AND Gender !=\'F\' AND '
                else:
                    query = query + 'Gender =\'' + gender + '\' AND '
            if nationality != '':
                query = query + 'Nationality LIKE \'%' + nationality + '%\' '

            # Remove trailing 'AND' and/or 'WHERE' from query
            if query[-4:] == 'AND ':
                query = query[:-4]

            if query[-6:] == 'WHERE ':
                query = query[:-6]

            try:
                # Execute the query
                cursor.execute(query)
                results = cursor.fetchall()

                # Clear the results table
                self.table.setRowCount(0)

                # Get values for each result of the query
                for row in results:
                    Id = row[0]
                    Name = row[1]
                    Gender = row[2]
                    Nationality = row[3]
                    BirthYear = row[4]
                    DeathYear = row[5]

                    # If BirthYear and/or DeathYear is NULL, show empty string
                    if BirthYear == None:
                        BirthYear = ''

                    if DeathYear == None:
                        DeathYear = ''

                    # Insert values in table
                    i = self.table.rowCount()
                    self.table.insertRow(i)

                    id_item = QTableWidgetItem(str(Id))
                    id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, QTableWidgetItem(Name))
                    self.table.setItem(i, 2, QTableWidgetItem(Gender))
                    self.table.setItem(i, 3, QTableWidgetItem(Nationality))
                    self.table.setItem(i, 4, QTableWidgetItem(str(BirthYear)))
                    self.table.setItem(i, 5, QTableWidgetItem(str(DeathYear)))

                # Resize columns
                self.table.resizeColumnsToContents()
                
                # Sort table
                self.table.sortItems(1)
            except Error as e:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                self.table.blockSignals(False)

        # Query Publishers
        elif self.layout_search.currentIndex() == 2:
            query = 'SELECT Id, Name FROM Publishers WHERE '

            # Get text from search form
            name = self.publisher_search.name.text()

            # Prepare SQL query
            if name != '':
                query = query + 'Name LIKE \'%' + name + '%\' '

            # Remove trailing 'WHERE' from query
            if query[-6:] == 'WHERE ':
                query = query[:-6]

            try:
                # Execute the query
                cursor.execute(query)
                results = cursor.fetchall()

                # Clear the results table
                self.table.setRowCount(0)

                # Get values for each result of the query
                for row in results:
                    Id = row[0]
                    Name = row[1]

                    i = self.table.rowCount()
                    self.table.insertRow(i)

                    # Insert values in table
                    id_item = QTableWidgetItem(str(Id))
                    id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, QTableWidgetItem(Name))

                # Resize columns
                self.table.resizeColumnsToContents()

                # Sort table
                self.table.sortItems(1)
            except Error as e:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                self.table.blockSignals(False)

        # Query series
        else:
            query = 'SELECT Id, Name, Author FROM Series WHERE '

            # Get text from search form
            name = self.series_search.name.text()
            author = self.series_search.author.text()

            # Prepare SQL query
            if name != '':
                query = query + 'Name LIKE \'%' + name + '%\' AND '
            if author != '':
                # Get Authors Id from Name
                mySql_select_query = """SELECT Id FROM Authors WHERE Name LIKE %s"""
                cursor.execute(mySql_select_query, ('%'+author+'%',))
                author = cursor.fetchall()
                if len(author) == 0:
                    author_id = 0
                else:
                    author_id = ''

                    i = 0
                    for row in author:
                        author_id = author_id + str(author[i][0]) + ', '
                        i = i + 1

                    author_id = author_id[:-2]

                query = query + 'Author IN (' + str(author_id) + ') '

            # Remove trailing 'AND' and/or 'WHERE' from query
            if query[-4:] == 'AND ':
                query = query[:-4]

            if query[-6:] == 'WHERE ':
                query = query[:-6]

            try:
                # Execute the query
                cursor.execute(query) 
                results = cursor.fetchall()

                # Clear the results table
                self.table.setRowCount(0)

                # Get values for each result of the query
                for row in results:
                    Id = row[0]
                    Name = row[1]
                    Author = row[2]

                    # Get Author Name from Id
                    if Author is not None:
                        mySql_select_query = """SELECT Name FROM Authors WHERE Id = %s"""
                        cursor.execute(mySql_select_query, (Author,))
                        Author = cursor.fetchall()
                        Author = Author[0][0]

                    i = self.table.rowCount()
                    self.table.insertRow(i)

                    # Insert values in table
                    id_item = QTableWidgetItem(str(Id))
                    id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, QTableWidgetItem(Name))
                    self.table.setItem(i, 2, QTableWidgetItem(Author))

                # Resize columns
                self.table.resizeColumnsToContents()

                # Sort table
                self.table.sortItems(1)
                self.table.sortItems(2)
            except Error as e:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                self.table.blockSignals(False)

        self.table.blockSignals(False)

    # Function to save current cell item
    def get_current_item(self):
        self.current_item = self.table.currentItem().text()

    # Function to update database
    def update_db(self):
        field_index = self.table.currentColumn()
        field = self.table.horizontalHeaderItem(field_index).text()
        value = self.table.currentItem().text()
        record_index = self.table.currentRow()
        id_n = self.table.item(record_index, 0).text()

        if field == 'Author':
            if value == '':
                # Author cannot be NULL, show error
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Author cannot be NULL. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                self.table.blockSignals(False)

                return

            mySql_select_query = """SELECT Id FROM Authors WHERE Name LIKE %s"""
            cursor.execute(mySql_select_query, ('%'+value+'%',))
            author = cursor.fetchall()
            if len(author) == 0:
                # Author cannot be NULL, show error
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Author not found in Authors table. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                self.table.blockSignals(False)

                return
            elif len(author) == 1:
                value = author[0][0]
            else:
                # Create error message box
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle('Error')
                error.setText('Multiple authors match name string. Operation failed')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                self.table.blockSignals(False)

                return
        elif field == 'Publisher':
            if value != '':
                mySql_select_query = """SELECT Id FROM Publishers WHERE Name LIKE %s"""
                cursor.execute(mySql_select_query, ('%'+value+'%',))
                publisher = cursor.fetchall()
                if len(publisher) == 0:
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setWindowTitle('Error')
                    error.setText('No publisher matches name string. Operation failed')
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return
                elif len(publisher) == 1:
                    value = publisher[0][0]
                else:
                    # Create error message box
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setWindowTitle('Error')
                    error.setText('Multiple publishers match name string. Operation failed')
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return
        elif field == 'Series':
            if value != '':
                mySql_select_query = """SELECT Id FROM Series WHERE Name LIKE %s"""
                cursor.execute(mySql_select_query, ('%'+value+'%',))
                series = cursor.fetchall()
                if len(series) == 0:
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setWindowTitle('Error')
                    error.setText('No series matches name string. Operation failed')
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return
                elif len(series) == 1:
                    value = series[0][0]
                else:
                    # Create error message box
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setWindowTitle('Error')
                    error.setText('Multiple series match name string. Operation failed')
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return

        if self.layout_search.currentIndex() == 0:
            if value != '':
                query = 'UPDATE Books SET {}="{}" WHERE Id={}'.format(field, value, id_n)
            else:
                query = 'UPDATE Books SET {}=NULL WHERE Id={}'.format(field, id_n)
        elif self.layout_search.currentIndex() == 1:
            if value != '':
                query = 'UPDATE Authors SET {}="{}" WHERE Id={}'.format(field, value, id_n)
            else:
                query = 'UPDATE Authors SET {}=NULL WHERE Id={}'.format(field, id_n)
        elif self.layout_search.currentIndex() == 2:
            if value != '':
                query = 'UPDATE Publishers SET {}="{}" WHERE Id={}'.format(field, value, id_n)
            else:
                query = 'UPDATE Publishers SET {}=NULL WHERE Id={}'.format(field, id_n)
        else:
            if value != '':
                query = 'UPDATE Series SET {}="{}" WHERE Id={}'.format(field, value, id_n)
            else:
                query = 'UPDATE Series SET {}=NULL WHERE Id={}'.format(field, id_n)

        try:
            cursor.execute(query)
            connection.commit()

            if field == 'Author':
                mySql_select_query = """SELECT Name FROM Authors WHERE Id=%s"""
                cursor.execute(mySql_select_query, (value,))
                author = cursor.fetchall()
                value = author[0][0]

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(value))

                self.table.blockSignals(False)
            elif field == 'Publisher':
                mySql_select_query = """SELECT Name FROM Publishers WHERE Id=%s"""
                cursor.execute(mySql_select_query, (value,))
                publisher = cursor.fetchall()
                value = publisher[0][0]

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(value))

                self.table.blockSignals(False)
            elif field == 'Series':
                mySql_select_query = """SELECT Name FROM Series WHERE Id=%s"""
                cursor.execute(mySql_select_query, (value,))
                series = cursor.fetchall()
                value = series[0][0]

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(value))

                self.table.blockSignals(False)

            info = QMessageBox()
            info.setIcon(QMessageBox.Information)
            info.setWindowTitle('Success')
            info.setText('Record modified successfully')
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

            self.table.blockSignals(True)

            self.table.removeCellWidget(record_index, field_index)
            self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

            self.table.blockSignals(False)

    # Function to save query result to file
    def save_to_file(self):
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('.csv')
        filename = file_dialog.getSaveFileName(self, 'Save query results', 'Results.csv')

        try:
            file_p = open(filename[0], 'w')

            for col in range(self.table.columnCount()):
                header = self.table.horizontalHeaderItem(col).text() + ','
                file_p.write(header)

            file_p.write('\n')

            for row in range(self.table.rowCount()):
                for col in range(self.table.columnCount()):
                    text = str(self.table.item(row, col).text());
                    if text.find(',') != -1:
                        text = '\"' + text + '\"'
                    text = text + ','
                    file_p.write(text)
                file_p.write('\n')

            file_p.close()
        except PermissionError as e:
            # Create error message box
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setWindowTitle('Error')
            error.setText(e.strerror)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
        except FileNotFoundError:
            pass

    def backup_db(self):
        file_dialog = QFileDialog()

        if os.name == 'nt':
            file_dialog.setDefaultSuffix('.sql')
            filename = file_dialog.getSaveFileName(self, 'Backup database', 'Library.sql')

            # Define backup command
            cmd = 'mysqldump.exe --single-transaction --master-data=2 --host={} Library -u {} -p{} > {}'.format(hostname, user, pwd, filename[0])
        elif os.name == 'posix':
            file_dialog.setDefaultSuffix('.gz')
            filename = file_dialog.getSaveFileName(self, 'Backup database', 'Library.sql.gz')

            # Define backup command
            cmd = 'mysqldump --single-transaction --master-data=2 --host={} Library -u {} -p{} | gzip > {}'.format(hostname, user, pwd, filename[0])

        # Execute the backup command
        try:
            subprocess.run(cmd, shell=True, check=True, stdout=PIPE).stdout
            # Show message if backup succeeded
            info = QMessageBox()
            info.setIcon(QMessageBox.Information)
            info.setWindowTitle('Success')
            info.setText('Backup completed successfully')
            info.setStandardButtons(QMessageBox.Ok)
            info.exec_()
        except CalledProcessError as e:
            # Create error message box
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setWindowTitle('Error')
            error.setText('Backup failed: {}'.format(e))
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def exit_program(self):
        exit(0)

# Form to insert books
class InsertBookForm(QWidget):

    def __init__(self, insert_record, *args, **kwargs):
        super(InsertBookForm, self).__init__(*args, **kwargs)

        # Define layout
        layout = QFormLayout()
        self.isbn = QLineEdit()
        self.title = QLineEdit()
        self.author = QLineEdit()
        self.otherauthors = QLineEdit()
        self.publisher = QLineEdit()
        self.series = QLineEdit()
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

    def __init__(self, insert_record, *args, **kwargs):
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

    def __init__(self, insert_record, *args, **kwargs):
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

    def __init__(self, insert_record, *args, **kwargs):
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
        close_button = QPushButton('Exit')

        # Define buttons behavior
        insert_button.clicked.connect(self.insert_record)
        clear_button.clicked.connect(self.clear_text)
        close_button.clicked.connect(self.exit_program)

        # Add buttons to layout
        layout_button.addWidget(insert_button)
        layout_button.addWidget(clear_button)
        layout_button.addWidget(close_button)
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
            category = self.book_insert.category.text()
            language = self.book_insert.language.text()
            year = self.book_insert.year.text()
            pages = self.book_insert.pages.text()
            owner = self.book_insert.owner.currentText()
            booktype = self.book_insert.booktype.currentText()

            # Set values to None where strings are empty
            if isbn == '':
                isbn = None
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
            cursor.execute(mySql_select_query, ('%'+author+'%',))
            author_id = cursor.fetchall()
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
                cursor.execute(mySql_select_query, (author,))
                author_id = cursor.fetchall()
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
                cursor.execute(mySql_select_query, ('%'+publisher+'%',))
                publisher_id = cursor.fetchall()
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
                    cursor.execute(mySql_select_query, (publisher,))
                    publisher_id = cursor.fetchall()
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
                cursor.execute(mySql_select_query, ('%'+series+'%',))
                series_id = cursor.fetchall()
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
                    cursor.execute(mySql_select_query, (series,))
                    series_id = cursor.fetchall()
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

            mySql_insert_query = """INSERT INTO Books(Id, ISBN, Title, Author, OtherAuthors, Publisher, Series, Category,
                                                      Language, Year, Pages, Owner,  Type)
                                    Values(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (isbn, title, author, otherauthors, publisher, series, category, language, year, pages, owner, booktype)

            # Execute the query
            try:
                cursor.execute(mySql_insert_query, values)
                connection.commit()

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
                name = None
            if gender == '':
                gender = None
            if nationality == '':
                nationality = None
            if birthyear == '':
                birthyear = None
            if deathyear == '':
                deathyear = None

            mySql_insert_query = """INSERT INTO Authors(Id, Name, Gender, Nationality, BirthYear, DeathYear) 
                                    Values(NULL, %s, %s, %s, %s, %s)"""
            values = (name, gender, nationality, birthyear, deathyear)

            # Execute the query
            try:
                cursor.execute(mySql_insert_query, values)
                connection.commit()

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

            mySql_insert_query = """INSERT INTO Publishers(Id, Name) Values(NULL, %s)"""

            # Execute the query
            try:
                cursor.execute(mySql_insert_query, (name,))
                connection.commit()

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
                cursor.execute(mySql_select_query, ('%'+author+'%',))
                author_id = cursor.fetchall()
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
                    cursor.execute(mySql_select_query, (author,))
                    author_id = cursor.fetchall()
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

            mySql_insert_query = """INSERT INTO Series(Id, Name, Author) Values(NULL, %s, %s)"""
            values = (name, author)

            # Execute the query
            try:
                cursor.execute(mySql_insert_query, values)
                connection.commit()

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

    # Function to exit the program
    def exit_program(self):
        exit(0)

# Main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Run the login window
        login_window = Login()
        login_window.exec_()
        
        # Set window title and icon
        if hostname == 'localhost':
            window_title = 'Library database - Local'
        else:
            window_title = 'Library database - Raspberry Pi'

        self.setWindowTitle(window_title)

        if os.name == 'nt':
            self.setWindowIcon(QIcon('Icon.ico'))
        elif os.name == 'posix':
            self.setWindowIcon(QIcon('/usr/share/icons/hicolor/32x32/apps/library_manager.png'))

        # Define main window tabs
        tabs = QTabWidget()
        tabs.addTab(SearchDatabase(), 'Search')
        tabs.addTab(InsertRecord(), 'Insert')
        tabs.setDocumentMode(True)

        # Show tabs
        self.setCentralWidget(tabs)

        # Maximize window size
        self.showMaximized()

def main():
    app = QApplication(argv)

    window = MainWindow()
    window.show()

    app.exec_()

    if connection.is_connected():
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main()
