from PyQt5 import QtWidgets

from tabs.Tab import *


class TabInfo(Tab):
    """Class for showing player information
    """


    def __init__(self, parent, identifier: int = -1):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Player ID
        """
        self.id = identifier
        super().__init__(parent)
    

    def createLayout(self):
        """Creating tab layout
        """
        # Creating input field for player ID
        self.identifierInput = QtWidgets.QLineEdit(self)
        if self.id > 0:
            self.identifierInput.setText(str(self.id))
        self.identifierInput.textChanged.connect(self.startLoading)
        self.layout.addWidget(self.identifierInput)
    

    def startLoading(self) -> bool:
        """Starting page (re)loading
        """
        if self.identifierInput.text() is None or self.identifierInput.text() == "":
            return False
        try:
            self.id = int(self.identifierInput.text())
        except:
            self.status.resultMessage("Entered ID is not a number", False)
            return False
        return True