from PyQt5 import QtWidgets

from widgets.ColoredButtons import *
from widgets.Status import *


class Dialog(QtWidgets.QDialog):
    """Class for creating a dialog window
    """


    def __init__(self, parent, identifier: int = None):
        """Initializes a dialog window

        Args:
            parent (QMainWindow): Dialog parent
            identifier (int): Player ID. Optional. Defaults to None
        """
        self.id = identifier
        super().__init__(parent)
        # Adding common layout settings
        self.accepted.connect(self.dialogAccepted)
        self.rejected.connect(self.dialogRejected)
        self.setFixedSize(500, 250)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addStretch(2)
        # Adding custom layout settings
        self.createLayout()
        # Adding the rest of common layout settings
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Accept button
        acceptButton = AcceptButton(self)
        acceptButton.setDefault(True)
        self.buttonBox.addButton(acceptButton, QtWidgets.QDialogButtonBox.AcceptRole)
        # Reject button
        deleteButton = RejectButton(self)
        deleteButton.setAutoDefault(False)
        self.buttonBox.addButton(deleteButton, QtWidgets.QDialogButtonBox.RejectRole)
        # Adding stretch and status
        self.layout.addStretch(1)
        self.layout.addWidget(self.buttonBox)
        self.layout.addStretch(1)
        self.status = Status(self)
        self.layout.addWidget(self.status)
        # Showing dialog window
        self.exec()
    
    
    def createLayout(self):
        """Creating dialog layout
        """
        pass


    def dialogAccepted(self):
        """Called when this dialog is accepted
        """
        print("Dialog accepted")


    def dialogRejected(self):
        """Called when this dialog is rejected
        """
        print("Dialog rejected")