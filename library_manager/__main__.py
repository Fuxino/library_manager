#!/usr/bin/env python3

"""Main module."""

# Import libraries
from sys import argv

from PyQt5.QtWidgets import QApplication

from library_manager.lm_window import MainWindow

def main():
    """Main."""

    app = QApplication(argv)

    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == '__main__':
    main()
