#!/usr/bin/python3

import sys
from sys import exit, argv

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import mysql.connector
from mysql.connector import Error

class Login(QDialog):

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)

        self.setWindowTitle('Login to Library')

        layout = QVBoxLayout()
        layout_login = QFormLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.host = QComboBox()
        self.host.addItem('192.168.0.100')
        self.host.addItem('localhost')
    
        layout_login.addRow(QLabel('Username:'), self.username)
        layout_login.addRow(QLabel('Password:'), self.password)
        layout_login.addRow(QLabel('Hostname:'), self.host)
        
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.db_connect)
        buttonBox.rejected.connect(self.exit_program)

        layout.addLayout(layout_login)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def db_connect(self):
        try:
            global connection
            global cursor

            connection = mysql.connector.connect(host=self.host.currentText(),
                                                 database='Library',
                                                 user=self.username.text(),
                                                 password=self.password.text())

            cursor = connection.cursor(prepared=True)

            self.accept()

        except Error as e:
            error = QMessageBox(self)
            error.setIcon(QMessageBox.Critical)
            error.setWindowTitle('Error')
            error.setText(str(e))
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def exit_program(self):
        exit(0)

class SearchBook(QWidget):

    def __init__(self, *args, **kwargs):
        super(SearchBook, self).__init__(*args, **kwargs)

        layout = QFormLayout()
        self.isbn = QLineEdit()
        self.title = QLineEdit()
        self.author = QLineEdit()

        self.author_gender = QComboBox()
        self.author_gender.addItem('')
        self.author_gender.addItem('M')
        self.author_gender.addItem('F')
        self.author_gender.addItem('Other')

        self.author_nationality = QLineEdit()
        self.publisher = QLineEdit()
        self.series = QLineEdit()

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

        self.language = QLineEdit()

        self.owner = QComboBox()
        self.owner.addItem('')
        self.owner.addItem('Daniele')
        self.owner.addItem('Nicole')

        self.booktype = QComboBox()
        self.booktype.addItem('')
        self.booktype.addItem('Printed')
        self.booktype.addItem('E-book')

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

        self.setLayout(layout)

class SearchAuthor(QWidget):

    def __init__(self, *args, **kwargs):
        super(SearchAuthor, self).__init__(*args, **kwargs)

        layout = QFormLayout()
        self.name = QLineEdit()
        self.gender = QComboBox()
        self.gender.addItem('')
        self.gender.addItem('M')
        self.gender.addItem('F')
        self.gender.addItem('Other')
        self.nationality = QLineEdit()
        layout.addRow('Name:', self.name)
        layout.addRow('Gender:', self.gender)
        layout.addRow('Nationality:', self.nationality)

        self.setLayout(layout)
        
class SearchPublisher(QWidget):

    def __init__(self, *args, **kwargs):
        super(SearchPublisher, self).__init__(*args, **kwargs)

        layout = QFormLayout()
        self.name = QLineEdit()
        layout.addRow('Name:', self.name)

        self.setLayout(layout)

class SearchSeries(QWidget):

    def __init__(self, *args, **kwargs):
        super(SearchSeries, self).__init__(*args, **kwargs)

        layout = QFormLayout()
        self.name = QLineEdit()
        self.author = QLineEdit()
        layout.addRow('Name:', self.name)
        layout.addRow('Author:', self.author)

        self.setLayout(layout)

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('Library database')
        self.setWindowIcon(QIcon('Books_icon.png'))

        login_window = Login()
        login_window.exec_()

        layout = QHBoxLayout()
        
        layout_left = QVBoxLayout()

        menu = QComboBox()
        menu.addItem('Books')
        menu.addItem('Authors')
        menu.addItem('Publishers')
        menu.addItem('Series')
        menu.currentIndexChanged[str].connect(self.change_table)

        layout_left.addWidget(menu)

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setRowCount(0)
        self.table.setColumnCount(13)
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem('Id'))
        self.table.setItem(0, 1, QTableWidgetItem('ISBN'))
        self.table.setItem(0, 2, QTableWidgetItem('Title'))
        self.table.setItem(0, 3, QTableWidgetItem('Author'))
        self.table.setItem(0, 4, QTableWidgetItem('OtherAuthors'))
        self.table.setItem(0, 5, QTableWidgetItem('Publisher'))
        self.table.setItem(0, 6, QTableWidgetItem('Series'))
        self.table.setItem(0, 7, QTableWidgetItem('Category'))
        self.table.setItem(0, 8, QTableWidgetItem('Language'))
        self.table.setItem(0, 9, QTableWidgetItem('Year'))
        self.table.setItem(0, 10, QTableWidgetItem('Pages'))
        self.table.setItem(0, 11, QTableWidgetItem('Owner'))
        self.table.setItem(0, 12, QTableWidgetItem('Type'))
        self.table.resizeColumnsToContents()

        layout_left.addWidget(self.table)

        layout.addLayout(layout_left)

        layout_right = QVBoxLayout()
        
        self.layout_search = QStackedLayout()

        self.book_search = SearchBook()
        self.author_search = SearchAuthor()
        self.publisher_search = SearchPublisher()
        self.series_search = SearchSeries()

        self.layout_search.addWidget(self.book_search)
        self.layout_search.addWidget(self.author_search)
        self.layout_search.addWidget(self.publisher_search)
        self.layout_search.addWidget(self.series_search)

        layout_right.addLayout(self.layout_search)

        layout_button = QHBoxLayout()
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.query_db)
        close_button = QPushButton('Exit')
        close_button.clicked.connect(self.close)
        layout_button.addWidget(search_button)
        layout_button.addWidget(close_button)
        layout_right.addLayout(layout_button)

        layout.addLayout(layout_right)

        self.setLayout(layout)
        self.showMaximized()

    def change_table(self, table_name):
        if table_name == 'Books':
            self.table.setRowCount(0)
            self.table.setColumnCount(13)
            self.table.insertRow(0)
            self.table.setItem(0, 0, QTableWidgetItem('Id'))
            self.table.setItem(0, 1, QTableWidgetItem('ISBN'))
            self.table.setItem(0, 2, QTableWidgetItem('Title'))
            self.table.setItem(0, 3, QTableWidgetItem('Author'))
            self.table.setItem(0, 4, QTableWidgetItem('OtherAuthors'))
            self.table.setItem(0, 5, QTableWidgetItem('Publisher'))
            self.table.setItem(0, 6, QTableWidgetItem('Series'))
            self.table.setItem(0, 7, QTableWidgetItem('Category'))
            self.table.setItem(0, 8, QTableWidgetItem('Language'))
            self.table.setItem(0, 9, QTableWidgetItem('Year'))
            self.table.setItem(0, 10, QTableWidgetItem('Pages'))
            self.table.setItem(0, 11, QTableWidgetItem('Owner'))
            self.table.setItem(0, 12, QTableWidgetItem('Type'))

            self.table.resizeColumnsToContents()
            
            self.layout_search.setCurrentIndex(0)
        elif table_name == 'Authors':
            self.table.setRowCount(0)
            self.table.setColumnCount(6)
            self.table.insertRow(0)
            self.table.setItem(0, 0, QTableWidgetItem('Id'))
            self.table.setItem(0, 1, QTableWidgetItem('Name'))
            self.table.setItem(0, 2, QTableWidgetItem('Gender'))
            self.table.setItem(0, 3, QTableWidgetItem('Nationality'))
            self.table.setItem(0, 4, QTableWidgetItem('BirthYear'))
            self.table.setItem(0, 5, QTableWidgetItem('DeathYear'))

            self.table.resizeColumnsToContents()

            self.layout_search.setCurrentIndex(1)
        elif table_name == 'Publishers':
            self.table.setRowCount(0)
            self.table.setColumnCount(2)
            self.table.insertRow(0)
            self.table.setItem(0, 0, QTableWidgetItem('Id'))
            self.table.setItem(0, 1, QTableWidgetItem('Name'))

            self.table.resizeColumnsToContents()

            self.layout_search.setCurrentIndex(2)
        else:
            self.table.setRowCount(0)
            self.table.setColumnCount(3)
            self.table.insertRow(0)
            self.table.setItem(0, 0, QTableWidgetItem('Id'))
            self.table.setItem(0, 1, QTableWidgetItem('Name'))
            self.table.setItem(0, 2, QTableWidgetItem('Author'))
            
            self.table.resizeColumnsToContents()

            self.layout_search.setCurrentIndex(3)

    def query_db(self):
        if self.layout_search.currentIndex() == 0:
            query = 'SELECT Id, ISBN, Title, Author, OtherAuthors, Publisher, Series, \
                    Category, Language, Year, Pages, Owner, Type FROM Books WHERE '

            isbn = self.book_search.isbn.text()
            title = self.book_search.title.text()
            author_n = self.book_search.author.text()
            author_g = self.book_search.author_gender.currentText()
            author_c = self.book_search.author_nationality.text()
            publisher = self.book_search.publisher.text()
            series = self.book_search.series.text()
            category = self.book_search.category.currentText()
            language = self.book_search.language.text()
            owner = self.book_search.owner.currentText()
            booktype = self.book_search.booktype.currentText()

            if isbn != '':
                query = query + 'ISBN LIKE \'%' + isbn + '%\' AND '
            if title != '':
                query = query + 'Title LIKE \'%' + title + '%\' AND '
            if author_n != '':
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

            if query[-4:] == 'AND ':
                query = query[:-4]

            if query[-6:] == 'WHERE ':
                query = query[:-6]
            
            query = query + 'ORDER BY Author, Series, Year'

            cursor.execute(query)
            results = cursor.fetchall()

            self.table.setRowCount(1)

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
            
                mySql_select_query = """SELECT Name FROM Authors WHERE Id = %s"""
                cursor.execute(mySql_select_query, (Author,))
                Author = cursor.fetchall()
                Author = Author[0][0]
            
                if Publisher is not None:
                    mySql_select_query = """SELECT Name FROM Publishers WHERE Id = %s"""
                    cursor.execute(mySql_select_query, (Publisher,))
                    Publisher = cursor.fetchall()
                    Publisher = Publisher[0][0]

                if Series is not None:
                    mySql_select_query = """SELECT Name FROM Series WHERE Id = %s"""
                    cursor.execute(mySql_select_query, (Series,))
                    Series = cursor.fetchall()
                    Series = Series[0][0]

                if Year == None:
                    Year = ''

                if Pages == None:
                    Pages = ''

                i = self.table.rowCount()
                self.table.insertRow(i)
            
                self.table.setItem(i, 0, QTableWidgetItem(str(Id)))
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
                
            self.table.resizeColumnsToContents()

            if self.table.columnWidth(2) > 300:
                self.table.setColumnWidth(2, 300)

            if self.table.columnWidth(4) > 300:
                self.table.setColumnWidth(4, 300)

        elif self.layout_search.currentIndex() == 1:
            query = 'SELECT Id, Name, Gender, Nationality, BirthYear, DeathYear FROM Authors WHERE '

            name = self.author_search.name.text()
            gender = self.author_search.gender.currentText()
            nationality = self.author_search.nationality.text()

            if name != '':
                query = query + 'Name LIKE \'%' + name + '%\' AND '
            if gender != '':
                if gender == 'Other':
                    query = query + 'Gender!=\'M\' AND Gender !=\'F\' AND '
                else:
                    query = query + 'Gender =\'' + gender + '\' AND '
            if nationality != '':
                query = query + 'Nationality LIKE \'%' + nationality + '%\' '

            if query[-4:] == 'AND ':
                query = query[:-4]

            if query[-6:] == 'WHERE ':
                query = query[:-6]

            query = query + 'ORDER BY Name'

            cursor.execute(query)
            results = cursor.fetchall()
            self.table.setRowCount(1)

            for row in results:
                Id = row[0]
                Name = row[1]
                Gender = row[2]
                Nationality = row[3]
                BirthYear = row[4]
                DeathYear = row[5]

                if BirthYear == None:
                    BirthYear = ''

                if DeathYear == None:
                    DeathYear = ''

                i = self.table.rowCount()
                self.table.insertRow(i)

                self.table.setItem(i, 0, QTableWidgetItem(str(Id)))
                self.table.setItem(i, 1, QTableWidgetItem(Name))
                self.table.setItem(i, 2, QTableWidgetItem(Gender))
                self.table.setItem(i, 3, QTableWidgetItem(Nationality))
                self.table.setItem(i, 4, QTableWidgetItem(str(BirthYear)))
                self.table.setItem(i, 5, QTableWidgetItem(str(DeathYear)))

            self.table.resizeColumnsToContents()

        elif self.layout_search.currentIndex() == 2:
            query = 'SELECT Id, Name FROM Publishers WHERE '

            name = self.publisher_search.name.text()

            if name != '':
                query = query + 'Name LIKE \'%' + name + '%\' '

            if query[-6:] == 'WHERE ':
                query = query[:-6]

            query = query + 'ORDER BY Name'

            cursor.execute(query)
            results = cursor.fetchall()
            self.table.setRowCount(1)

            for row in results:
                Id = row[0]
                Name = row[1]

                i = self.table.rowCount()
                self.table.insertRow(i)

                self.table.setItem(i, 0, QTableWidgetItem(str(Id)))
                self.table.setItem(i, 1, QTableWidgetItem(Name))
            
            self.table.resizeColumnsToContents()

        else:
            query = 'SELECT Id, Name, Author FROM Series WHERE '

            name = self.series_search.name.text()
            author = self.series_search.author.text()

            if name != '':
                query = query + 'Name LIKE \'%' + name + '%\' AND '
            if author != '':
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
        
            if query[-4:] == 'AND ':
                query = query[:-4]

            if query[-6:] == 'WHERE ':
                query = query[:-6]

            query = query + 'ORDER BY Author, Name'

            cursor.execute(query) 
            results = cursor.fetchall()
            self.table.setRowCount(1)

            for row in results:
                Id = row[0]
                Name = row[1]
                Author = row[2]

                mySql_select_query = """SELECT Name FROM Authors WHERE Id = %s"""
                cursor.execute(mySql_select_query, (Author,))
                Author = cursor.fetchall()
                Author = Author[0][0]
                
                i = self.table.rowCount()
                self.table.insertRow(i)

                self.table.setItem(i, 0, QTableWidgetItem(str(Id)))
                self.table.setItem(i, 1, QTableWidgetItem(Name))
                self.table.setItem(i, 2, QTableWidgetItem(Author))

            self.table.resizeColumnsToContents()

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
