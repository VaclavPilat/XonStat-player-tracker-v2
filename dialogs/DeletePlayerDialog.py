from PyQt5 import QtCore

from dialogs.Dialog import *
from misc.Functions import *
from misc.Config import *


class DeletePlayerDialog(Dialog):
    """Class for creating a dialog window for delting players
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
        self.player = checkPlayerExistence(self.id)
        self.setWindowTitle("Delete player #" + str(self.id) + " ?")
        # Checking if player is tracked
        if self.player is not None:
            label = ColoredLabel(self, "Are you sure you want to stop tracking this player?\n\n" + parseTextFromHTML(self.player["nick"]))
        else:
            label = ColoredLabel(self, "Player #" + str(self.id) + " is not being tracked and thus cannot be deleted.")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        self.layout.addWidget(label)


    def dialogAccepted(self):
        """Called when this dialog is accepted
        """
        # Deleting player
        if self.player is not None:
            Config.instance()["Players"].remove(self.player)
            Config.instance().save("Players")
            