#!/usr/bin/env python3

"""Create the main window."""

import os

import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from library_manager.login import LoginDialog
from library_manager.query import SearchDatabase
from library_manager.insert import InsertRecord

import library_manager._globals as _globals

# Main window
class MainWindow(QMainWindow):
    """Main window layout."""

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Run the login window
        login_window = LoginDialog()
        login_window.exec_()

        # Set window title and icon
        if _globals.HOSTNAME == 'localhost':
            window_title = 'Library database - Local'
        else:
            window_title = 'Library database - Remote'

        self.setWindowTitle(window_title)

        if os.name == 'nt':
            self.setWindowIcon(QIcon('Icon.ico'))
        elif os.name == 'posix':
            self.setWindowIcon(QIcon(f'{sys.prefix}' +\
                    '/share/icons/hicolor/32x32/apps/library_manager.png'))

        # Define main layout
        layout = QVBoxLayout()

        # Define exit button
        exit_button = QPushButton('Exit')
        exit_button.setMinimumSize(400, 30)
        exit_button.setMaximumSize(600, 30)

        # Define buttons behavior
        exit_button.clicked.connect(self.close)

        # Define main window tabs
        tabs = QTabWidget()
        tabs.addTab(SearchDatabase(), 'Search')
        tabs.addTab(InsertRecord(), 'Insert')
        tabs.setDocumentMode(True)

        layout.addWidget(tabs)
        layout.addWidget(exit_button)
        layout.setAlignment(exit_button, Qt.AlignRight)

        widget = QWidget()
        widget.setLayout(layout)

        # Show tabs
        self.setCentralWidget(widget)

        # Maximize window size
        self.showMaximized()
