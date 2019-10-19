#!/usr/bin/env python3

"""Main module."""

# Import libraries
import os

from sys import argv

from PyQt5.QtWidgets import QApplication

if os.name == 'nt':
    from lm_window import MainWindow
    from fbs_runtime.application_context.PyQt5 import ApplicationContext
elif os.name == 'posix':
    from library_manager.lm_window import MainWindow

def main():
    """Main."""

    app = QApplication(argv)

    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == '__main__':
    main()
