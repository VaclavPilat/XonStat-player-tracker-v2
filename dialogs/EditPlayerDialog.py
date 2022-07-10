from PyQt5 import QtWidgets

from dialogs.Dialog import *
from misc.Functions import *
from misc.Config import *


class EditPlayerDialog(Dialog):
    """Class for creating a dialog window for editing player information
    """


    def __init__(self, parent, identifier: int = None):
        """Initializes a dialog window

        Args:
            parent (QMainWindow): Dialog parent
            identifier (int): Player ID. Optional. Defaults to None
        """
        super().__init__(parent, identifier)
    
    
    def createLayout(self):
        """Creating dialog layout
        """
        self.setWindowTitle("Edit player #" + str(self.id))
        # Checking if player is tracked
        self.player = checkPlayerExistence(self.id)
        if self.player is not None:
            # Player nick input
            self.nick = QtWidgets.QLineEdit(self)
            self.nick.setPlaceholderText("Nick")
            self.nick.textEdited.connect(self.checkInputValidity)
            self.nick.setText(self.player["nick"])
            self.layout.addWidget(self.nick)
            # Player description input
            self.description = QtWidgets.QLineEdit(self)
            self.description.setPlaceholderText("Description")
            self.description.textEdited.connect(self.checkInputValidity)
            self.description.setText(self.player["description"])
            self.layout.addWidget(self.description)
        else:
            label = ColoredLabel(self, "Player #" + str(self.id) + " is not being tracked and thus cannot be edited.")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setWordWrap(True)
            self.layout.addWidget(label)
    

    def checkInputValidity(self):
        """Disabling accept button based on input validity
        """
        if len(self.nick.text()) > 0:
            self.status.resultMessage("Input is valid", True)
            self.acceptButton.setEnabled(True)
        else:
            self.status.resultMessage("Please enter player nickname", False)
            self.acceptButton.setEnabled(False)


    def dialogAccepted(self):
        """Called when this dialog is accepted
        """
        if self.player is not None:
            # Saving edited information
            index = Config.instance()["Players"].index(self.player)
            Config.instance()["Players"][index]["nick"] = self.nick.text()
            Config.instance()["Players"][index]["description"] = self.description.text()
            Config.instance().save("Players")
            self.reloadAllTabs.emit()