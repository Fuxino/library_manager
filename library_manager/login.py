#!/usr/bin/env python3

"""Login module

This module creates a login dialog box that take username, password
and hostname and allows to connect to the Library database.
"""

# Import libraries
import os

import sys

from functools import partial

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit,\
        QComboBox, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase

if os.name == 'nt':
    import _globals
    from info_dialogs import ErrorDialog
    from sys import exit
elif os.name == 'posix':
    import library_manager._globals as _globals
    from library_manager.info_dialogs import ErrorDialog

# Login dialog box
class LoginDialog(QDialog):
    """Login dialog."""

    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        # Set dialog title
        self.setWindowTitle('Login to Library')

        if os.name == 'nt':
            self.setWindowIcon(QIcon('Icon.ico'))
        elif os.name == 'posix':
            self.setWindowIcon(QIcon(f'{sys.prefix}' +\
                    '/share/icons/hicolor/32x32/apps/library_manager.png'))

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
        self.host.setEditable(True)
        self.host.setInsertPolicy(QComboBox.InsertAtCurrent)

        # Add fields to layout
        layout_login.addRow(QLabel('Username:'), self.username)
        layout_login.addRow(QLabel('Password:'), self.password)
        layout_login.addRow(QLabel('Hostname:'), self.host)

        # Create buttons
        q_button = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # Define button behavior
        button_box = QDialogButtonBox(q_button)
        button_box.accepted.connect(self.db_connect)
        button_box.rejected.connect(partial(exit, 0))

        # Add login form and button to main layout
        layout.addLayout(layout_login)
        layout.addWidget(button_box)

        # Set layout
        self.setLayout(layout)

        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setDatabaseName('Library')

    # Function to connect to the database
    def db_connect(self):
        """Connect to the database

        The method takes the username, password and hostname inserted by the user
        in the Login dialog  and uses them to connect to the database with mysql-connector.
        """

        _globals.HOSTNAME = self.host.currentText()
        _globals.USER = self.username.text()
        _globals.PWD = self.password.text()

        # Create connection
        self.db.setHostName(_globals.HOSTNAME)
        self.db.setUserName(_globals.USER)
        self.db.setPassword(_globals.PWD)

        if self.db.open():
            # Close login dialog
            self.accept()
        # If error occurred during connection
        else:
            # Create error message box
            self.db.close()
            error = ErrorDialog(str(self.db.lastError().databaseText()))
            error.show()
