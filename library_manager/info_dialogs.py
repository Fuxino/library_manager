#!/usr/bin/env python3

"""Information, warning and error dialogs."""

from PyQt5.QtWidgets import QMessageBox

class ErrorDialog(QMessageBox):
    """Show an error dialog box."""

    def __init__(self, error, *args, **kwargs):
        super(ErrorDialog, self).__init__(*args, **kwargs)

        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle('Error')
        self.setText(error)
        self.setStandardButtons(QMessageBox.Ok)

    def show(self):
        """Show the dialog."""

        self.exec_()

class WarningDialog(QMessageBox):
    """Show a warning dialog box."""

    def __init__(self, warning, *args, **kwargs):
        super(WarningDialog, self).__init__(*args, **kwargs)

        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle('Warning')
        self.setText(warning)
        self.setStandardButtons(QMessageBox.Ok)

    def show(self):
        """Show the dialog."""

        self.exec_()

class InfoDialog(QMessageBox):
    """Show an information dialog box."""

    def __init__(self, info, *args, **kwargs):
        super(InfoDialog, self).__init__(*args, **kwargs)

        self.setIcon(QMessageBox.Information)
        self.setWindowTitle('Success')
        self.setText(info)
        self.setStandardButtons(QMessageBox.Ok)

    def show(self):
        """Show the dialog."""

        self.exec_()

class ConfirmDialog(QMessageBox):
    """Show a confirmation dialog box."""

    def __init__(self, message, *args, **kwargs):
        super(ConfirmDialog, self).__init__(*args, **kwargs)

        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle('Confirm')
        self.setText(message)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def show(self):
        """Show the dialog."""

        return self.exec_()
