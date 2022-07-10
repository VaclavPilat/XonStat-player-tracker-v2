from PyQt5 import QtWidgets, QtCore

from widgets.ColoredButtons import *
from widgets.Status import *


class Dialog(QtWidgets.QDialog):
    """Class for creating a dialog window
    """


    reloadAllTabs = QtCore.pyqtSignal()


    def __init__(self, parent, identifier: int = None):
        """Initializes a dialog window

        Args:
            parent (QMainWindow): Dialog parent
            identifier (int): Player ID. Optional. Defaults to None
        """
        self.id = identifier
        super().__init__(parent)
        self.reloadAllTabs.connect(parent.reloadAllTabs)
        # Adding common layout settings
        self.accepted.connect(self.dialogAccepted)
        self.rejected.connect(self.dialogRejected)
        self.setFixedSize(450, 200)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addStretch()
        # Adding custom layout settings
        self.createLayout()
        # Adding the rest of common layout settings
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Accept button
        self.acceptButton = AcceptButton(self)
        self.acceptButton.setDefault(True)
        self.buttonBox.addButton(self.acceptButton, QtWidgets.QDialogButtonBox.AcceptRole)
        # Reject button
        self.deleteButton = RejectButton(self)
        self.deleteButton.setAutoDefault(False)
        self.buttonBox.addButton(self.deleteButton, QtWidgets.QDialogButtonBox.RejectRole)
        # Adding stretch and status
        self.layout.addStretch()
        self.layout.addWidget(self.buttonBox)
        self.layout.addStretch()
        self.status = Status(self)
        self.layout.addWidget(self.status)
        # Showing dialog window
        self.dialogCreated()
        self.exec()
    
    
    def createLayout(self):
        """Creating dialog layout
        """
        pass
    
    
    def dialogCreated(self):
        """Called after the dialog layout is created
        """
        pass


    def dialogAccepted(self):
        """Called when this dialog is accepted
        """
        pass


    def dialogRejected(self):
        """Called when this dialog is rejected
        """
        pass