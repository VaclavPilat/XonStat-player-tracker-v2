from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *


class PlayerInfo(Tab):
    """Class for showing player information
    """


    def __init__(self, parent, id: int = -1):
        """Init

        Args:
            parent (MainWindow): Parent window
            id (int): Player ID
        """
        self.id = id
        super().__init__(parent)
        self.name = "Player Info"
    

    def createLayout(self):
        """Creating tab layout
        """
        # Creating input field for player ID
        self.identifierInput = QtWidgets.QLineEdit(self)
        self.identifierInput.setPlaceholderText("Enter player ID")
        if self.id > 0:
            self.identifierInput.setText(str(self.id))
        self.identifierInput.textChanged.connect(self.startLoading)
        self.layout.addWidget(self.identifierInput)
        self.layout.addStretch()
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.identifierInput.text() is None or self.identifierInput.text() == "":
            return
        try:
            self.id = int(self.identifierInput.text())
        except:
            self.status.resultMessage("Entered ID is not a number", False)
        else:
            self.status.message("Loading player profile")