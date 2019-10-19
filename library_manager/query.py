#!/usr/bin/env python3

"""Module for querying the database

This module creates the layout that allows to query
the Library database and show the results.
It implements the functions for the database queries,
and allows to save the search results and backup the
whole database.
It also implements the function to update existing
records in the database.
"""

import os

import subprocess
from subprocess import CalledProcessError

from PyQt5.QtWidgets import QFileDialog, QWidget, QLineEdit, QComboBox,\
        QPushButton, QTableWidget, QTableWidgetItem, QFormLayout,\
        QHBoxLayout, QVBoxLayout, QStackedLayout
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery

if os.name == 'nt':
    import _globals
    from info_dialogs import ErrorDialog, InfoDialog
elif os.name == 'posix':
    import library_manager._globals as _globals
    from library_manager.info_dialogs import ErrorDialog, InfoDialog

try:
    from isbnlib import canonical, is_isbn10, is_isbn13, mask

    ISBN_CHECK = True
except ImportError:
    ISBN_CHECK = False

# Form to search books
class SearchBookForm(QWidget):
    """Widget to search for books in the database."""

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
        self.subseries = QLineEdit()
        self.subseries.returnPressed.connect(query_db)

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
        layout.addRow('Subseries:', self.subseries)
        layout.addRow('Category:', self.category)
        layout.addRow('Language:', self.language)
        layout.addRow('Owner:', self.owner)
        layout.addRow('Type:', self.booktype)

        # Set layout
        self.setLayout(layout)

# Form to search authors
class SearchAuthorForm(QWidget):
    """Widget to search for authors in the database."""

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
    """Widget to search for publishers in the database."""

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
    """Widget to search for series in the database."""

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
    """Main widget to search records in the database

    This class creates a stacked layout containing four search form widgets
    (Books, Authors, Publishers, Series) and table widgets to display the query results.
    It implements functions to query the database, save the query results to file and backup
    the whole database and update records in the database.
    """

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
        self.table.setColumnCount(14)

        id_header = QTableWidgetItem('Id')
        isbn_header = QTableWidgetItem('ISBN')
        title_header = QTableWidgetItem('Title')
        author_header = QTableWidgetItem('Author')
        otherauthors_header = QTableWidgetItem('OtherAuthors')
        publisher_header = QTableWidgetItem('Publisher')
        series_header = QTableWidgetItem('Series')
        subseries_header = QTableWidgetItem('Subseries')
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
        self.table.setHorizontalHeaderItem(7, subseries_header)
        self.table.setHorizontalHeaderItem(8, category_header)
        self.table.setHorizontalHeaderItem(9, language_header)
        self.table.setHorizontalHeaderItem(10, year_header)
        self.table.setHorizontalHeaderItem(11, pages_header)
        self.table.setHorizontalHeaderItem(12, owner_header)
        self.table.setHorizontalHeaderItem(13, type_header)

        self.table.resizeColumnsToContents()

        self.current_item = None

        self.table.cellDoubleClicked.connect(self.get_current_item)
        self.table.cellChanged.connect(self.update_db)

        # Add table to layout
        layout_left.addWidget(self.table)

        # Add buttons
        layout_button_l = QHBoxLayout()

        # Add backup and save buttons
        save_button = QPushButton('Save to file')
        backup_button = QPushButton('Backup database')
        save_button.setMinimumSize(200, 30)
        save_button.setMaximumSize(200, 30)
        backup_button.setMinimumSize(200, 30)
        backup_button.setMaximumSize(200, 30)

        # Define buttons behavior
        save_button.clicked.connect(self.save_to_file)
        backup_button.clicked.connect(self.backup_db)

        # Add buttons to layout
        layout_button_l.addWidget(save_button)
        layout_button_l.addWidget(backup_button)
        layout_button_l.addWidget(QWidget())
        layout_button_l.addWidget(QWidget())
        layout_button_l.setAlignment(save_button, Qt.AlignLeft)
        layout_button_l.setAlignment(backup_button, Qt.AlignLeft)
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

        # Create buttons
        layout_button_r = QHBoxLayout()
        search_button = QPushButton('Search')
        clear_button = QPushButton('Clear')
        search_button.setMinimumSize(200, 30)
        search_button.setMaximumSize(200, 30)
        clear_button.setMinimumSize(200, 30)
        clear_button.setMaximumSize(200, 30)

        # Define buttons behavior
        search_button.clicked.connect(self.query_db)
        clear_button.clicked.connect(self.clear)

        # Add buttons to layout
        layout_button_r.addWidget(search_button)
        layout_button_r.addWidget(clear_button)
        layout_button_r.addWidget(QWidget())
        layout_button_r.addWidget(QWidget())
        layout_button_r.setAlignment(search_button, Qt.AlignLeft)
        layout_button_r.setAlignment(clear_button, Qt.AlignLeft)
        layout_right.addLayout(layout_button_r)

        # Add right layout to main layout
        layout.addLayout(layout_right)

        # Set main layout
        self.setLayout(layout)

    # Function to clear all query result table and search fields
    def clear(self):
        """Clear the result table and the search form."""

        self.table.blockSignals(True)

        self.table.setRowCount(0)

        self.book_search.isbn.clear()
        self.book_search.title.clear()
        self.book_search.author.clear()
        self.book_search.author_gender.setCurrentIndex(0)
        self.book_search.author_nationality.clear()
        self.book_search.publisher.clear()
        self.book_search.series.clear()
        self.book_search.subseries.clear()
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
        """Select the search form (Books, Authors, Publishers or Series)."""

        self.clear()

        self.table.blockSignals(True)

        # Books
        if table_name == 'Books':
            self.table.setColumnCount(14)

            id_header = QTableWidgetItem('Id')
            isbn_header = QTableWidgetItem('ISBN')
            title_header = QTableWidgetItem('Title')
            author_header = QTableWidgetItem('Author')
            otherauthors_header = QTableWidgetItem('OtherAuthors')
            publisher_header = QTableWidgetItem('Publisher')
            series_header = QTableWidgetItem('Series')
            subseries_header = QTableWidgetItem('Subseries')
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
            self.table.setHorizontalHeaderItem(7, subseries_header)
            self.table.setHorizontalHeaderItem(8, category_header)
            self.table.setHorizontalHeaderItem(9, language_header)
            self.table.setHorizontalHeaderItem(10, year_header)
            self.table.setHorizontalHeaderItem(11, pages_header)
            self.table.setHorizontalHeaderItem(12, owner_header)
            self.table.setHorizontalHeaderItem(13, type_header)

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
        """Search Boosk, Authors, Publishers or Series in the database

        The method reads the informations in the active search form
        (Books, Authors, Publishers or Series) and uses them to query
        the database, displaying the result in the table.
        """

        self.table.blockSignals(True)

        sql_query = QSqlQuery()

        # Query Books
        if self.layout_search.currentIndex() == 0:
            query = 'SELECT Books.Id, ISBN, Title, Authors.Name, OtherAuthors, Publishers.Name, \
                    Series.Name, Subseries, Category, Language, Year, Pages, Owner, Type FROM Books \
                    LEFT JOIN Authors ON Books.Author=Authors.Id LEFT JOIN Publishers ON \
                    Books.Publisher=Publishers.Id LEFT JOIN Series ON Books.Series=Series.Id WHERE '

            # Get text from search form
            isbn = self.book_search.isbn.text()
            title = self.book_search.title.text()
            author_n = self.book_search.author.text()
            author_g = self.book_search.author_gender.currentText()
            author_c = self.book_search.author_nationality.text()
            publisher = self.book_search.publisher.text()
            series = self.book_search.series.text()
            subseries = self.book_search.subseries.text()
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
                query = query + '(Authors.Name LIKE \'%' + author_n +\
                        '%\' OR OtherAuthors LIKE \'%' + author_n + '%\') AND '
            if author_g != '':
                if author_g == 'Other':
                    query = query + 'Authors.Gender!=\'M\' AND Authors.Gender!=\'F\' AND '
                else:
                    query = query + 'Authors.Gender=\'' + author_g + '\' AND '
            if author_c != '':
                query = query + 'Authors.Nationality LIKE \'%' + author_c + '%\' AND '
            if publisher != '':
                query = query + 'Publishers.Name LIKE \'%' + publisher + '%\' AND '
            if series != '':
                query = query + 'Series.Name LIKE \'%' + series + '%\' AND '
            if subseries != '':
                query = query + 'Subseries LIKE \'%' + subseries + '%\' AND '
            if category != '':
                if category == 'Fiction':
                    query = query + 'Category LIKE \'%Fiction%\' AND ' +\
                            'Category NOT LIKE \'%Non-fiction%\' AND '
                elif category == 'Novel':
                    query = query + 'Category LIKE \'%Novel%\' AND ' +\
                            'Category NOT LIKE \'%Graphic novel%\' AND '
                else:
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

            query = query + 'ORDER BY Authors.Name, Series.Name, Year'

            sql_query.prepare(query)

            # Execute the query
            if sql_query.exec_():
                # Clear the results table
                self.table.setRowCount(0)

                # Get values for each result of the query
                while sql_query.next():
                    record = sql_query.record()
                    Id = str(record.value(0))
                    ISBN = str(record.value(1))
                    Title = str(record.value(2))
                    Author = str(record.value(3))
                    OtherAuthors = str(record.value(4))
                    Publisher = str(record.value(5))
                    Series = str(record.value(6))
                    Subseries = str(record.value(7))
                    Category = str(record.value(8))
                    Language = str(record.value(9))
                    Year = str(record.value(10))
                    Pages = str(record.value(11))
                    Owner = str(record.value(12))
                    Type = str(record.value(13))

                    # Hyphenate ISBN
                    if ISBN != '' and ISBN_CHECK:
                        ISBN = mask(ISBN, '-')

                    if Year == '0':
                        Year = ''

                    if Pages == '0':
                        Pages = ''

                    # Insert values in table
                    i = self.table.rowCount()
                    self.table.insertRow(i)

                    id_item = QTableWidgetItem(Id)
                    id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, QTableWidgetItem(ISBN))
                    self.table.setItem(i, 2, QTableWidgetItem(Title))
                    self.table.setItem(i, 3, QTableWidgetItem(Author))
                    self.table.setItem(i, 4, QTableWidgetItem(OtherAuthors))
                    self.table.setItem(i, 5, QTableWidgetItem(Publisher))
                    self.table.setItem(i, 6, QTableWidgetItem(Series))
                    self.table.setItem(i, 7, QTableWidgetItem(Subseries))
                    self.table.setItem(i, 8, QTableWidgetItem(Category))
                    self.table.setItem(i, 9, QTableWidgetItem(Language))
                    self.table.setItem(i, 10, QTableWidgetItem(Year))
                    self.table.setItem(i, 11, QTableWidgetItem(Pages))
                    self.table.setItem(i, 12, QTableWidgetItem(Owner))
                    self.table.setItem(i, 13, QTableWidgetItem(Type))

                # Resize columns
                self.table.resizeColumnsToContents()

                if self.table.columnWidth(2) > 300:
                    self.table.setColumnWidth(2, 300)

                if self.table.columnWidth(4) > 300:
                    self.table.setColumnWidth(4, 300)
            else:
                # Create error message box
                error = ErrorDialog(sql_query.lastError().databaseText())
                error.show()

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

            query = query + 'ORDER BY Name'

            sql_query.prepare(query)

            # Execute the query
            if sql_query.exec_():

                # Clear the results table
                self.table.setRowCount(0)

                # Get values for each result of the query
                while sql_query.next():
                    Id = str(sql_query.value(0))
                    Name = str(sql_query.value(1))
                    Gender = str(sql_query.value(2))
                    Nationality = str(sql_query.value(3))
                    BirthYear = str(sql_query.value(4))
                    DeathYear = str(sql_query.value(5))

                    if BirthYear == '0':
                        BirthYear = ''

                    if DeathYear == '0':
                        DeathYear = ''

                    # Insert values in table
                    i = self.table.rowCount()
                    self.table.insertRow(i)

                    id_item = QTableWidgetItem(Id)
                    id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, QTableWidgetItem(Name))
                    self.table.setItem(i, 2, QTableWidgetItem(Gender))
                    self.table.setItem(i, 3, QTableWidgetItem(Nationality))
                    self.table.setItem(i, 4, QTableWidgetItem(BirthYear))
                    self.table.setItem(i, 5, QTableWidgetItem(DeathYear))

                # Resize columns
                self.table.resizeColumnsToContents()
            else:
                # Create error message box
                error = ErrorDialog(sql_query.lastError().databaseText())
                error.show()

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

            query = query + 'ORDER BY Name'

            sql_query.prepare(query)

            # Execute the query
            if sql_query.exec_():
                # Clear the results table
                self.table.setRowCount(0)

                # Get values for each result of the query
                while sql_query.next():
                    Id = str(sql_query.value(0))
                    Name = str(sql_query.value(1))

                    i = self.table.rowCount()
                    self.table.insertRow(i)

                    # Insert values in table
                    id_item = QTableWidgetItem(Id)
                    id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, QTableWidgetItem(Name))

                # Resize columns
                self.table.resizeColumnsToContents()
            else:
                # Create error message box
                error = ErrorDialog(sql_query.lastError().databaseText())
                error.show()

                self.table.blockSignals(False)

        # Query series
        else:
            query = 'SELECT Series.Id, Series.Name, Authors.Name FROM Series \
                    LEFT JOIN Authors ON Series.Author=Authors.Id WHERE '

            # Get text from search form
            name = self.series_search.name.text()
            author = self.series_search.author.text()

            # Prepare SQL query
            if name != '':
                query = query + 'Series.Name LIKE \'%' + name + '%\' AND '
            if author != '':
                query = query + 'Authors.Name LIKE \'%' + author + '%\' '

            # Remove trailing 'AND' and/or 'WHERE' from query
            if query[-4:] == 'AND ':
                query = query[:-4]

            if query[-6:] == 'WHERE ':
                query = query[:-6]

            query = query + 'ORDER BY Authors.Name, Series.Name'

            sql_query.prepare(query)

            # Execute the query
            if sql_query.exec_():
                # Clear the results table
                self.table.setRowCount(0)

                # Get values for each result of the query
                while sql_query.next():
                    Id = str(sql_query.value(0))
                    Name = str(sql_query.value(1))
                    Author = str(sql_query.value(2))

                    i = self.table.rowCount()
                    self.table.insertRow(i)

                    # Insert values in table
                    id_item = QTableWidgetItem(Id)
                    id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, 0, id_item)
                    self.table.setItem(i, 1, QTableWidgetItem(Name))
                    self.table.setItem(i, 2, QTableWidgetItem(Author))

                # Resize columns
                self.table.resizeColumnsToContents()
            else:
                # Create error message box
                error = ErrorDialog(sql_query.lastError().databaseText())
                error.show()

                self.table.blockSignals(False)

        self.table.blockSignals(False)

    # Function to save current cell item
    def get_current_item(self):
        """Save the item of the current table cell.

        Used to restore the value displayed when update command fails.
        """

        self.current_item = self.table.currentItem().text()

    # Function to update database
    def update_db(self):
        """Update a record in the database

        When the user edits a value, corresponding to a field of a record in the database,
        in the search results table, this method automatically updates the database
        with the new value.
        """

        sql_query = QSqlQuery()

        field_index = self.table.currentColumn()
        field = self.table.horizontalHeaderItem(field_index).text()
        value = self.table.currentItem().text()
        record_index = self.table.currentRow()
        id_n = self.table.item(record_index, 0).text()

        if field == 'ISBN':
            if value != '' and ISBN_CHECK:
                if '-' in value:
                    value = canonical(value)
                if len(value) == 10:
                    if not is_isbn10(value):
                        # Show an error if the ISBN is invalid
                        error = ErrorDialog('The ISBN inserted is invalid. Operation failed.')
                        error.show()

                        self.table.blockSignals(True)

                        self.table.removeCellWidget(record_index, field_index)
                        self.table.setItem(record_index, field_index,\
                                QTableWidgetItem(self.current_item))

                        self.table.blockSignals(False)

                        return
                elif len(value) == 13:
                    if not is_isbn13(value):
                        # Show an error if the ISBN is invalid
                        error = ErrorDialog('The ISBN inserted is invalid. Operation failed.')
                        error.show()

                        self.table.blockSignals(True)

                        self.table.removeCellWidget(record_index, field_index)
                        self.table.setItem(record_index, field_index,\
                                QTableWidgetItem(self.current_item))

                        self.table.blockSignals(False)

                        return
                else:
                    # Show an error if the ISBN is invalid
                    error = ErrorDialog('The ISBN inserted is invalid. Operation failed.')
                    error.show()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index,\
                            QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return
        elif field == 'Author':
            if value == '':
                # Author cannot be NULL, show error
                error = ErrorDialog('Author cannot be NULL. Operation failed')
                error.show()

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                self.table.blockSignals(False)

                return

            query = f'SELECT Id FROM Authors WHERE Name LIKE \'%{value}%\''
            sql_query.prepare(query)
            sql_query.exec_()

            if sql_query.size() == 0:
                # Author cannot be NULL, show error
                error = ErrorDialog('Author not found in Authors table. Operation failed')
                error.show()

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                self.table.blockSignals(False)

                return

            if sql_query.size() == 1:
                sql_query.next()
                value = sql_query.value(0)
            else:
                # Create error message box
                error = ErrorDialog('Multiple authors match name string. Operation failed')
                error.show()

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

                self.table.blockSignals(False)

                return
        elif field == 'Publisher':
            if value != '':
                query = f'SELECT Id FROM Publishers WHERE Name LIKE \'%{value}%\''
                sql_query.prepare(query)
                sql_query.exec_()

                if sql_query.size() == 0:
                    error = ErrorDialog('No publisher matches name string. Operation failed')
                    error.show()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index,\
                            QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return

                if sql_query.size() == 1:
                    sql_query.next()
                    value = sql_query.value(0)
                else:
                    # Create error message box
                    error = ErrorDialog('Multiple publishers match name string. Operation failed')
                    error.show()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index,\
                            QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return
        elif field == 'Series':
            if value != '':
                query = f'SELECT Id FROM Series WHERE Name LIKE \'%{value}%\''
                sql_query.prepare(query)
                sql_query.exec_()

                if sql_query.size() == 0:
                    error = ErrorDialog('No series matches name string. Operation failed')
                    error.show()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index,\
                            QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return

                if sql_query.size() == 1:
                    sql_query.next()
                    value = sql_query.value(0)
                else:
                    # Create error message box
                    error = ErrorDialog('Multiple series match name string. Operation failed.')
                    error.show()

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index,\
                            QTableWidgetItem(self.current_item))

                    self.table.blockSignals(False)

                    return

        if self.layout_search.currentIndex() == 0:
            if value != '':
                query = f'UPDATE Books SET {field}="{value}" WHERE Id={id_n}'
            else:
                query = f'UPDATE Books SET {field}=NULL WHERE Id={id_n}'
        elif self.layout_search.currentIndex() == 1:
            if value != '':
                query = f'UPDATE Authors SET {field}="{value}" WHERE Id={id_n}'
            else:
                query = f'UPDATE Authors SET {field}=NULL WHERE Id={id_n}'
        elif self.layout_search.currentIndex() == 2:
            if value != '':
                query = f'UPDATE Publishers SET {field}="{value}" WHERE Id={id_n}'
            else:
                query = f'UPDATE Publishers SET {field}=NULL WHERE Id={id_n}'
        else:
            if value != '':
                query = f'UPDATE Series SET {field}="{value}" WHERE Id={id_n}'
            else:
                query = f'UPDATE Series SET {field}=NULL WHERE Id={id_n}'

        sql_query.prepare(query)

        if sql_query.exec_():
            if field == 'ISBN':
                if value != '':
                    value = mask(value, '-')

                    self.table.blockSignals(True)

                    self.table.removeCellWidget(record_index, field_index)
                    self.table.setItem(record_index, field_index, QTableWidgetItem(value))

                    self.table.blockSignals(False)
            elif field == 'Author':
                query = f'SELECT Name FROM Authors WHERE Id={value}'
                sql_query.prepare(query)
                sql_query.exec_()

                author = sql_query.result()
                author.fetchFirst()
                value = author.boundValue(0)

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(value))

                self.table.blockSignals(False)
            elif field == 'Publisher':
                query = f'SELECT Name FROM Publishers WHERE Id={value}'
                sql_query.prepare(query)
                sql_query.exec_()

                publisher = sql_query.result()
                publisher.fetchFirst()
                value = publisher.boundValue(0)

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(value))

                self.table.blockSignals(False)
            elif field == 'Series':
                query = f'SELECT Name FROM Series WHERE Id={value}'
                sql_query.prepare(query)
                sql_query.exec_()

                series = sql_query.result()
                series.fetchFirst()
                value = series.boundValue(0)

                self.table.blockSignals(True)

                self.table.removeCellWidget(record_index, field_index)
                self.table.setItem(record_index, field_index, QTableWidgetItem(value))

                self.table.blockSignals(False)

            # Resize columns
            self.table.resizeColumnsToContents()

            if self.table.columnWidth(2) > 300:
                self.table.setColumnWidth(2, 300)

            if self.table.columnWidth(4) > 300:
                self.table.setColumnWidth(4, 300)

            info = InfoDialog('Record modified successfully')
            info.show()
        else:
            # Create error message box
            error = ErrorDialog(sql_query.lastError().databaseText())
            error.show()

            self.table.blockSignals(True)

            self.table.removeCellWidget(record_index, field_index)
            self.table.setItem(record_index, field_index, QTableWidgetItem(self.current_item))

            self.table.blockSignals(False)

    # Function to save query result to file
    def save_to_file(self):
        """Save the query results to a file."""

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
                    text = str(self.table.item(row, col).text())
                    if text.find(',') != -1:
                        text = '\"' + text + '\"'
                    text = text + ','
                    file_p.write(text)
                file_p.write('\n')

            file_p.close()

            info = InfoDialog(f'{filename[0]} saved successfully')
            info.show()
        except PermissionError as err:
            # Create error message box
            error = ErrorDialog(str(err))
            error.show()
        except FileNotFoundError:
            pass

    def backup_db(self):
        """Backup the database to a file."""

        file_dialog = QFileDialog()

        if os.name == 'nt':
            file_dialog.setDefaultSuffix('.sql')
            filename = file_dialog.getSaveFileName(self, 'Backup database', 'Library.sql')

            # Define backup command
            cmd = 'mysqldump.exe --single-transaction --master-data=2 ' +\
                    f'--host={_globals.HOSTNAME} --databases Library -u {_globals.USER} ' +\
                    f'-p{_globals.PWD} > {filename[0]}'
        elif os.name == 'posix':
            file_dialog.setDefaultSuffix('.gz')
            filename = file_dialog.getSaveFileName(self, 'Backup database', 'Library.sql.gz')

            # Define backup command
            cmd = 'mysqldump --single-transaction --master-data=2 ' +\
                    f'--host={_globals.HOSTNAME} --databases Library -u {_globals.USER} ' +\
                    f'-p{_globals.PWD} | gzip > {filename[0]}'

        # Execute the backup command
        try:
            proc_status = subprocess.run(cmd, shell=True, check=True, capture_output=True)
            # Show message if backup succeeded
            info = InfoDialog('Backup completed successfully ' +\
                    f'(return code: {proc_status.returncode})')
            info.show()
        except CalledProcessError as err:
            # Create error message box
            error = ErrorDialog(str(err.stderr))
            error.show()
