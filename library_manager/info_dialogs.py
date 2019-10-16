#!/usr/bin/env python3

"""Information, warning and error dialogs"""

from PyQt5.QWidgets import QMessageBox

class ErrorDialog(QMessageBox)

    def __init__(self, error, *args, **kwargs):
        super(ErrorDialog, self).__init__(*args, **kwargs)

        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle('Error')
        self.setText(error)
        self.setStandardButtons(QMessageBox.Ok)
        
    def show(self):
        self.exec_()
