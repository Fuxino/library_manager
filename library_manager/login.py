#!/usr/bin/env python3

"""Login module

This module creates a login dialog box that take username, password
and hostname and allows to connect to the Library database
"""

# Import libraries
import os

from functools import partial

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit,\
        QComboBox, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon

import mysql.connector
from mysql.connector import Error

import library_manager._globals as _globals
from library_manager.info_dialogs import ErrorDialog

# Login dialog box
class Login_dialog(QDialog):
    """Login dialog"""

    def __init__(self, *args, **kwargs):
        super(Login_dialog, self).__init__(*args, **kwargs)

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
        self.host.setEditable(True)
        self.host.setInsertPolicy(QComboBox.InsertAtCurrent)

        # Add fields to layout
        layout_login.addRow(QLabel('Username:'), self.username)
        layout_login.addRow(QLabel('Password:'), self.password)
        layout_login.addRow(QLabel('Hostname:'), self.host)

        # Create buttons
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # Define button behavior
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.db_connect)
        buttonBox.rejected.connect(partial(exit, 0))

        # Add login form and button to main layout
        layout.addLayout(layout_login)
        layout.addWidget(buttonBox)

        # Set layout
        self.setLayout(layout)

    # Function to connect to the database
    def db_connect(self):
        try:
            _globals.hostname = self.host.currentText()
            _globals.user = self.username.text()
            _globals.pwd = self.password.text()

            # Create connection
            _globals.connection = mysql.connector.connect(host=_globals.hostname,
                                                          database='Library',
                                                          user=_globals.user,
                                                          password=_globals.pwd)

            _globals.cursor = _globals.connection.cursor(prepared=True)

            # Close login dialog
            self.accept()

        # If error occurred during connection
        except Error as e:
            # Create error message box
            error = ErrorDialog(str(e))
            error.show()
