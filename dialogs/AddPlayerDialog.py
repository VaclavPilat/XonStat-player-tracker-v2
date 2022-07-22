from PyQt5 import QtWidgets

from dialogs.Dialog import *
from misc.Functions import *
from misc.Config import *
from workers.AddPlayerDialogWorker import *


class AddPlayerDialog(Dialog):
    """Class for creating a dialog window for adding new players
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
        self.setWindowTitle("Add player #" + str(self.id))
        # Checking if player is tracked
        self.player = checkPlayerExistence(self.id)
        if self.player is None:
            # Player nick input
            self.nick = QtWidgets.QLineEdit(self)
            self.nick.setPlaceholderText("Nick")
            self.nick.textChanged.connect(self.checkInputValidity)
            self.nick.textChanged.connect(self.cancel)
            self.layout.addWidget(self.nick)
            # Player description input
            self.description = QtWidgets.QLineEdit(self)
            self.description.setPlaceholderText("Description")
            self.description.textEdited.connect(self.checkInputValidity)
            self.layout.addWidget(self.description)
        else:
            label = ColoredLabel(self, "Player #" + str(self.id) + " is already tracked and thus cannot be added.")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setWordWrap(True)
            self.layout.addWidget(label)
    

    def cancel(self):
        """Calcels worker
        """
        try:
            self.worker.cancel = True
        except:
            pass
    

    def checkInputValidity(self):
        """Disabling accept button based on input validity
        """
        if len(self.nick.text()) > 0:
            self.status.resultMessage("Input is valid", True)
            self.acceptButton.setEnabled(True)
        else:
            self.status.resultMessage("Please enter player nickname", False)
            self.acceptButton.setEnabled(False)
    
    
    def dialogCreated(self):
        """Called after the dialog layout is created
        """
        if self.player is None:
            self.checkInputValidity()
            # Starting worker for loading player name
            self.worker = AddPlayerDialogWorker(self)
            self.worker.start()


    def dialogAccepted(self):
        """Called when this dialog is accepted
        """
        if self.player is None:
            # Adding new player
            player = {}
            player["id"] = self.id
            player["nick"] = self.nick.text()
            player["description"] = self.description.text()
            Config.instance()["Players"].append(player)
            Config.instance().save("Players")
            self.reloadAllTabs.emit()